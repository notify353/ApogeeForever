"""Install exact aggregate ZIPs. Normal runs update DEV only; PROD retrofit is explicit."""
import argparse
import copy
import json
from pathlib import Path
import sys
import subprocess

sys.dont_write_bytecode = True
import distribution as d
import dual_distribution as dual
import migrate_distribution as m
import support_distribution as support


def payloads(lock, sources_root, artifacts, initial=False):
    result = {}
    for family in (('PROD', 'DEV') if initial else ('DEV',)):
        expected, _ = dual.family_files(lock, sources_root, family)
        archive = Path(artifacts) / ('Apogee-' + lock['version'] + '-' + family + '.zip')
        result.update(dual.validate(archive.read_bytes(), expected))
    return result


def prepare(client, payload, known, initial=False, previous=None, retire_files=()):
    roots = {p.split('/')[0] for p in payload}
    current = {d.MARKER + 'Dev', *(n + 'Dev' for n in d.ACTIVE_CHILDREN)}
    historical = set(m.DEV_NAMES)
    if initial:
        current |= {d.MARKER, *d.ACTIVE_CHILDREN}
        historical |= set(m.NAMES)
    support_roots = {'ApogeeUIDev', 'ApogeeUI'} if initial else {'ApogeeUIDev'}
    d.require(roots in (current, historical, current | support_roots), 'Exact family roots required')
    # Omitted retired roots stay untouched; uninstall is a separate explicit action.
    names = tuple(sorted(roots))
    d.require(set(p.split('/')[0] for p in payload) == set(names), 'Exact family roots required')
    if support.master_payload(payload) and not initial:
        names = tuple(sorted(roots | {'ApogeeUIDev'}))
    before = m.managed(Path(client) / 'Interface/AddOns', names)
    known = copy.deepcopy(known)
    if previous is not None:
        d.require(previous['schema'] == 1 and previous['status'] == 'installed', 'Prior installed receipt required')
        d.require(Path(previous['client']).absolute() == Path(client).absolute(), 'Receipt belongs to another client')
        for p, h in previous['after'].items():
            d.safe_path(p)
            d.require(p.split('/')[0] in m.NAMES + m.DEV_NAMES + m.LOCAL_DEV_NAMES + ('ApogeeUI', 'ApogeeUIDev'), 'Receipt escapes families')
            known['files'].setdefault(p, []).append(h)
            if p.startswith(d.MARKER + '/') and p.lower().endswith('.toc'):
                known['legacyTocHashes'].append(h)
    for p, b in payload.items():
        known['files'].setdefault(p, []).append(d.sha(b))
    preserved_docs = []
    desired = dict(payload)
    # Documentation is not needed to activate the artifact; never replace local edited notes.
    for p, b in before.items():
        if p in desired and b != desired[p] and p.lower().endswith(('.md', '.txt')):
            preserved_docs.append(p)
            del desired[p]
    retired = support.retire_support(payload, before, previous)
    for p in retire_files:
        d.safe_path(p)
        d.require(not initial and p.split('/')[0] in names and p.endswith('.lua'),
                  'Retirement is limited to explicit DEV Lua files')
        d.require(previous is not None and p in previous['after'], 'Retirement requires previous receipt')
        d.require(p not in payload and p in before and d.sha(before[p]) == previous['after'][p],
                  'Retired file missing, modified, or still packaged: ' + p)
        retired[p] = previous['after'][p]
    preview = m.plan(client, desired, known, names, retired)
    preview['retired'] = retired
    return desired, known, names, preview, preserved_docs


def activation(preview, live_update=False):
    writes = preview['writes']
    if live_update:
        return {'action': 'user-reload-after-install' if writes else 'none',
                'discoveryChanges': [], 'restartRequired': False}
    discovery = sorted(p for p in writes if p not in preview['before'] or p.lower().endswith('.toc'))
    support_added = any(p.startswith('ApogeeUIDev/') for p in preview.get('retired', {})) or any((p.startswith('ApogeeUIDev/') or '/SharedUI/' in p) and p not in preview['before'] for p in writes)
    return {'action': 'user-full-restart-after-install' if support_added else 'user-reload-after-install' if writes else 'none',
            'discoveryChanges': discovery,
            'restartRequired': True if support_added else 'unverified-if-reload-does-not-discover-changes' if discovery else False}


def verify_live_update(payload, preview, previous, initial=False):
    """A running client may reload known DEV files, never discover a new loading graph."""
    d.require(not initial, 'Live Forever updates cannot retrofit PROD')
    d.require(previous is not None, 'Live updates require a prior installed Forever receipt')
    d.require(not preview['retired'], 'Live Forever updates cannot retire files')
    before = preview['before']
    def runtime_paths(files):
        return {p for p in files if p.lower().endswith(('.lua', '.xml', '.toc'))}
    paths = runtime_paths(payload)
    d.require(paths == runtime_paths(before) == runtime_paths(previous['after']),
              'Live Forever updates cannot add or remove runtime files; close the client')
    for path in paths:
        d.require(d.sha(before[path]) == previous['after'][path],
                  'Installed Forever bytes differ from receipt: ' + path)
        if path.lower().endswith('.toc'):
            old_meta, old_runtime = d.toc_info(before[path])
            new_meta, new_runtime = d.toc_info(payload[path])
            old_meta.pop('Version', None); new_meta.pop('Version', None)
            d.require(old_meta == new_meta and old_runtime == new_runtime,
                      'Live Forever updates cannot change loading metadata/order; close the client')


def install(client, payload, known, backup, initial=False, previous=None, retire_files=(), live_update=False,
            client_running=False, api_review_deferral=None):
    d.require(api_review_deferral is None or (live_update and not initial and previous is not None),
              'Deferred API review requires a receipt-backed DEV update')
    desired, known, names, preview, docs = prepare(client, payload, known, initial, previous, retire_files)
    if live_update:
        verify_live_update(payload, preview, previous, initial)
    result = m.apply(client, desired, known, backup, preview, names, atomic_dev=not initial, retired=preview['retired'])
    result['activation'] = activation(preview, live_update)
    result['liveUpdate'] = live_update
    result['clientRunningAtPreflight'] = client_running
    if api_review_deferral is not None:
        result['apiReview'] = api_review_deferral
    result['preservedDocumentation'] = docs
    result['mode'] = 'initial-production-retrofit-and-dev' if initial else 'dev-only'
    result['packageFilesVerified'] = len(desired)
    if support.master_payload(payload):
        result['packageRoots'] = sorted({p.split('/')[0] for p in payload})
        result['supportLayout'] = 'embedded-master'
    (Path(backup) / 'transaction.json').write_bytes(d.canonical(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client-root', type=Path, required=True)
    parser.add_argument('--sources-root', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--backup', type=Path, required=True)
    parser.add_argument('--target', choices=('forever', 'classic-era'), default='forever')
    parser.add_argument('--lock', type=Path)
    parser.add_argument('--previous-install', type=Path)
    parser.add_argument('--retire-file', action='append', default=[], help='Exact obsolete DEV Lua path; requires unchanged prior receipt')
    parser.add_argument('--initial-retrofit', action='store_true', help='One-time explicitly authorized PROD safety migration')
    parser.add_argument('--inspect-only', action='store_true')
    parser.add_argument('--allow-running-era-update', action='store_true',
                        help='Explicit Era DEV update with prior receipt and unchanged runtime paths/loading metadata')
    parser.add_argument('--allow-running-forever-update', action='store_true',
                        help='Explicit Forever DEV update with prior receipt and unchanged runtime paths/loading metadata')
    parser.add_argument('--defer-forever-api-review', action='store_true',
                        help='Owner-authorized local DEV test without refreshing API export; requires prior receipt and checked live-update path')
    args = parser.parse_args()
    try:
        d.require(not args.defer_forever_api_review or (args.target == 'forever'
                  and args.allow_running_forever_update and args.previous_install is not None
                  and not args.initial_retrofit and not args.retire_file),
                  'Deferred API review is limited to receipt-backed Forever DEV updates without retirement')
        if args.target == 'classic-era':
            d.require(not args.allow_running_forever_update, 'Live Forever opt-in requires --target forever')
            import era_distribution
            print(json.dumps(era_distribution.install_target(args)))
            return
        d.require(not args.allow_running_era_update, 'Live Era opt-in requires --target classic-era')
        live_update = args.allow_running_forever_update
        d.require(not live_update or not args.initial_retrofit, 'Live Forever updates cannot retrofit PROD')
        lock = d.read_lock(args.lock or dual.LOCK)
        preflight_options = {'allow_running_dev': live_update or (not args.initial_retrofit and not lock.get('supportModules'))}
        if args.defer_forever_api_review:
            preflight_options['defer_api_review'] = True
        running = m.real_client_preflight(args.client_root, lock, **preflight_options)
        deferral = m.deferred_live_dev_review(args.client_root, lock) if args.defer_forever_api_review else None
        files = payloads(lock, args.sources_root, args.artifacts, args.initial_retrofit)
        known = m.catalog(d.ROOT / 'distribution/migration-known.json')
        previous = json.loads(args.previous_install.read_text()) if args.previous_install else None
        if args.inspect_only:
            _, _, _, preview, docs = prepare(args.client_root, files, known, args.initial_retrofit, previous, args.retire_file)
            if live_update:
                verify_live_update(files, preview, previous, args.initial_retrofit)
            print(json.dumps({'writeCount': len(preview['writes']), 'preservedDocumentation': docs,
                              'inventory': preview['inventory'], 'retired': preview['retired'], 'clientRunning': running,
                              'liveUpdate': live_update, 'activation': activation(preview, live_update),
                              'apiReview': deferral}))
        else:
            result = install(args.client_root, files, known, args.backup, args.initial_retrofit, previous, args.retire_file,
                             live_update=live_update, client_running=running, api_review_deferral=deferral)
            print(json.dumps({k: result[k] for k in ('status', 'mode', 'packageFilesVerified', 'preservedDocumentation', 'activation')}))
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, 'Family install stopped: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
