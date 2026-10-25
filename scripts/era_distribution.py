"""Isolated, unpublished Classic Era DEV target. Never reads a Forever client export."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
import distribution as d
import dual_distribution as dual
import support_distribution as support
import migrate_distribution as m

CONFIG = d.ROOT / 'distribution/era'
LOCK = CONFIG / 'candidate.lock.json'
HISTORICAL_MEMBERS = ('ApogeeHeals', 'ApogeeKeybinds', 'ApogeeGroupAlert', 'ApogeeEssentials')
MEMBERS = HISTORICAL_MEMBERS + ('ApogeeStats',)
LEGACY_NAMES = tuple(n + 'Dev' for n in (d.MARKER, *MEMBERS))
NAMES = LEGACY_NAMES + ('ApogeeUIDev',)
HISTORICAL_NAMES = tuple(n + 'Dev' for n in (d.MARKER, *HISTORICAL_MEMBERS))
RECEIPT_ROOTS = (set(NAMES), set(LEGACY_NAMES), set(HISTORICAL_NAMES), set(HISTORICAL_NAMES + ('ApogeeUIDev',)))
CLIENT = {'flavor': 'classic-era', 'product': 'wow_classic_era',
          'directory': '_classic_era_', 'reviewedBuild': '1.15.9.70003', 'interface': 11509}


def read_lock(path=LOCK):
    lock = json.loads(Path(path).read_bytes())
    d.require(lock['schema'] == 1 and lock['target'] == 'classic-era'
              and lock['family'] == 'DEV' and lock['publicationAllowed'] is False,
              'Unpublished Era DEV lock required')
    d.require(lock['client'] == CLIENT, 'Unexpected Era client/build')
    d.require(re.fullmatch(r'\d+\.\d+\.\d+-era\.\d+', lock['version']), 'Invalid Era version')
    inventory = lock.get('moduleInventoryVersion', 1)
    d.require(inventory in (1, 2), 'Unknown Era module inventory')
    d.require(tuple(c['name'] for c in lock['children']) == (MEMBERS if inventory == 2 else HISTORICAL_MEMBERS),
              'Exact versioned Era modules required')
    for child in lock['children']:
        name = child['name']
        d.require(re.fullmatch('[0-9a-f]{40}', child['commit']), 'Immutable source required')
        d.require(child['repository'] == 'https://github.com/notify353/' + name + '.git', 'Unexpected source')
        d.require(child['toc'] == name + '_Era.toc', 'Explicit Era load list required')
        for path, digest in child['files'].items():
            d.safe_path(path)
            d.require(re.fullmatch('[0-9a-f]{64}', digest), 'Invalid source hash')
        d.require(child['toc'] in child['files'] and 'Era/Adapter.lua' in child['files'], 'Era adapter missing')
    d.require(support.descriptor(lock) is not None, 'Era launcher support required')
    return lock


def verify_api(client, lock):
    """Verify product, executable and every selected export reference; no game operation."""
    client = m.ordinary(client)
    d.require(client.name == CLIENT['directory'], 'Only the Classic Era directory is allowed')
    lines = m.under(client.parent, '.build.info').read_text(encoding='utf-8-sig').splitlines()
    keys = [k.split('!')[0] for k in lines[0].split('|')]
    rows = [dict(zip(keys, line.split('|'))) for line in lines[1:]]
    d.require([r.get('Version') for r in rows if r.get('Product') == CLIENT['product']]
              == [CLIENT['reviewedBuild']], 'Era product build changed; fresh review required')
    record = json.loads((CONFIG / 'api-evidence.json').read_bytes())
    d.require(d.sha(d.canonical(record)) == lock['apiEvidenceSha256'], 'Era evidence differs from lock')
    exe = m.under(client, 'WowClassic.exe')
    d.require(d.sha(exe.read_bytes()) == record['executableSha256'], 'Era executable changed; fresh export required')
    root = m.under(client, 'BlizzardInterfaceCode/Interface/AddOns')
    for item in record['files']:
        path = m.under(root, item['path'])
        d.require(path.stat().st_mtime_ns >= exe.stat().st_mtime_ns, 'Stale Era export: ' + item['path'])
        d.require(d.sha(path.read_bytes()) == item['sha256'], 'Era API reference changed: ' + item['path'])
    return {'build': CLIENT['reviewedBuild'], 'referencesVerified': len(record['files']),
            'evidenceSha256': lock['apiEvidenceSha256']}


def family_files(lock, sources_root):
    output, changes = {}, {}
    gate = (CONFIG / 'ClientGate.lua').read_bytes() + b'\n' + support.gate_bytes(lock, dual.GATE.read_bytes())
    gate += b'\nif namespace.__ApogeeFamilyAdmission and namespace.__ApogeeFamilyAdmission(name) then\n namespace.__ApogeeClient = "classic-era"\nend\n'
    marker = d.MARKER + 'Dev'
    for child in lock['children']:
        old, name = child['name'], child['name'] + 'Dev'
        tree = d.source_tree(Path(sources_root) / old, child['commit'])
        source = {}
        for path, digest in child['files'].items():
            d.require(path in tree and d.sha(tree[path]) == digest, 'Era pinned file mismatch: ' + old + '/' + path)
            source[path] = tree[path]
        meta, runtime = d.toc_info(source[child['toc']])
        d.require(meta['Interface'] == '11509' and len(runtime) == len(set(runtime)), 'Invalid Era TOC')
        d.require(all(p.endswith('.lua') and p in source for p in runtime), 'Only pinned direct Lua loaders supported')
        d.require(runtime[-2:] == ['Era/Adapter.lua', old + '.lua'], 'Era adapter must immediately precede startup')
        d.require({p for p in source if p.endswith('.lua')} == set(runtime), 'Unloaded runtime in Era lock')
        d.require({p for p in source if p.endswith('.toc')} == {child['toc']}, 'Alternate loaders forbidden')
        meta = {k: v for k, v in meta.items() if not k.startswith(('X-Curse', 'X-Wago', 'X-WoWI'))}
        meta = {k: v.replace(old, name) if k.startswith('SavedVariables') or k == 'IconTexture' else v
                for k, v in meta.items()}
        meta.update({'Title': dual.LABELS[old] + ' Era DEV', 'Version': lock['version'],
                     'Group': marker, 'Category': 'Apogee Era DEV', 'X-Apogee-Client': 'classic-era',
                     'X-Apogee-Family': 'DEV', 'X-Apogee-Family-Schema': '1'})
        d.require(meta.get('Dependencies') == 'ApogeeUI' and meta.get('X-Apogee-UI-API') == '1', 'Missing matching UI dependency')
        meta['Dependencies'] = support.owner(lock, 'DEV')
        if support.embedded(lock): meta['X-Apogee-Requires-Master'] = '1'
        renamed = {p: name + '.lua' if p == old + '.lua' else p for p in runtime}
        toc = ''.join('## ' + k + ': ' + v + '\n' for k, v in meta.items()) + '\n'
        toc += dual.GATE_PATH + '\n' + ''.join(renamed[p] + '\n' for p in runtime)
        output[name + '/' + name + '.toc'] = toc.encode()
        output[name + '/' + dual.GATE_PATH] = gate.replace(b'@NAME@', name.encode()).replace(b'@FAMILY@', b'DEV')
        for p, data in source.items():
            if p == child['toc']:
                continue
            target = name + '/' + renamed.get(p, p)
            if p in runtime:
                body, audit = dual.transform_lua(data, old)
                output[target] = dual.prefix(name, 'DEV') + body
                changes[target] = {'source': old + '/' + p, 'sourceSha256': d.sha(data),
                                   'bodySha256': d.sha(body), 'identityEdits': audit}
            else:
                output[target] = data
        output[name + '/README.md'] = source['Era/README.md']
    for p in ('LICENSE', 'Media/Textures/ApogeeLogo.png'):
        output[marker + '/' + p] = output['ApogeeKeybindsDev/' + p]
    meta = {'Interface': '11509', 'Title': 'Apogee Era DEV', 'Version': lock['version'],
            'Group': marker, 'Category': 'Apogee Era DEV', 'X-Apogee-Client': 'classic-era',
            'X-Apogee-Family': 'DEV', 'X-Apogee-Family-Schema': '1',
            'X-Apogee-Distribution-Only': '1', 'X-Apogee-Distribution-Schema': '1',
            'IconTexture': 'Interface/AddOns/' + marker + '/Media/Textures/ApogeeLogo.png'}
    output[marker + '/' + marker + '.toc'] = ''.join('## ' + k + ': ' + v + '\n' for k, v in meta.items()).encode()
    support.add_files(lock, sources_root, 'DEV', output, changes, gate, dual)
    output[marker + '/README.md'] = (CONFIG / 'PLAYER_README.md').read_bytes()
    if support.embedded(lock):
        output[marker + '/README.md'] = (d.ROOT / 'distribution/MASTER_PLAYER_README.md').read_bytes()
    roots = {d.MARKER + 'Dev', *(c['name'] + 'Dev' for c in lock['children'])}
    if not support.embedded(lock): roots.add('ApogeeUIDev')
    d.require({p.split('/')[0] for p in output} == roots, 'Era roots differ')
    return output, changes


def build(lock, sources_root, output, evidence):
    files, changes = family_files(lock, sources_root)
    data = d.zip_bytes(files)
    dual.validate(data, files)
    output = m.ordinary(output)
    output.mkdir(parents=True, exist_ok=False)
    archive = 'Apogee-' + lock['version'] + '-DEV.zip'
    (output / archive).write_bytes(data)
    manifest = {'schema': 1, 'target': 'classic-era', 'family': 'DEV', 'publicationAllowed': False,
                'lockSha256': d.sha(d.canonical(lock)), 'apiEvidence': evidence,
                'archive': archive, 'archiveSha256': d.sha(data),
                'files': m.hashes(files), 'runtimeChanges': changes,
                'children': [{'name': c['name'], 'commit': c['commit']} for c in lock['children']],
                'supportModules': lock['supportModules']}
    (output / 'ERA-DEV-manifest.json').write_bytes(d.canonical(manifest))
    return manifest


def prepare(client, payload, previous=None):
    """Only Era DEV roots. Receipts from other clients/targets cannot authorize overwrites."""
    client = m.ordinary(client)
    d.require(client.name == CLIENT['directory'], 'Era client required')
    roots = {p.split('/')[0] for p in payload}
    allowed = (set(LEGACY_NAMES), set(HISTORICAL_NAMES)) if support.master_payload(payload) else (set(NAMES), set(HISTORICAL_NAMES + ('ApogeeUIDev',)))
    d.require(roots in allowed, 'Exact Era roots required')
    known = {'schema': 1, 'files': {}, 'legacyTocHashes': []}
    if previous is not None:
        d.require(previous['schema'] == 1 and previous['status'] == 'installed'
                  and previous.get('target') == 'classic-era' and previous.get('family') == 'DEV'
                  and set(previous['names']) in RECEIPT_ROOTS, 'Prior Era DEV receipt required')
        d.require(Path(previous['client']).absolute() == client, 'Receipt belongs to another client')
        for p, h in previous['after'].items():
            d.safe_path(p)
            d.require(p.split('/')[0] in previous['names'] and re.fullmatch('[0-9a-f]{64}', h), 'Receipt escapes Era roots')
            known['files'].setdefault(p, []).append(h)
    for p, body in payload.items():
        d.safe_path(p)
        known['files'].setdefault(p, []).append(d.sha(body))
    desired, docs = dict(payload), []
    for p, body in m.managed(client / 'Interface/AddOns', NAMES).items():
        if p in desired and body != desired[p] and p.lower().endswith(('.md', '.txt')):
            del desired[p]
            docs.append(p)
    retired = support.retire_support(payload, m.managed(client / 'Interface/AddOns', NAMES), previous)
    preview = m.plan(client, desired, known, NAMES, retired)
    preview['retired'] = retired
    return desired, known, preview, docs


def verify_live_update(payload, preview, previous):
    """Explicit live updates replace known bytes only; discovery still requires a closed client."""
    d.require(previous is not None, 'Live updates require a prior installed Era receipt')
    before = preview['before']
    def runtime_paths(files):
        return {p for p in files if p.lower().endswith(('.lua', '.xml', '.toc'))}
    paths = runtime_paths(payload)
    d.require(paths == runtime_paths(before) == runtime_paths(previous['after']),
              'Live Era updates cannot add or remove runtime files; close the client')
    for path in paths:
        d.require(d.sha(before[path]) == previous['after'][path], 'Installed Era bytes differ from receipt: ' + path)
        if path.lower().endswith('.toc'):
            old_meta, old_runtime = d.toc_info(before[path])
            new_meta, new_runtime = d.toc_info(payload[path])
            old_meta.pop('Version', None); new_meta.pop('Version', None)
            d.require(old_meta == new_meta and old_runtime == new_runtime,
                      'Live Era updates cannot change loading metadata/order; close the client')


def install_target(args):
    """Called only by the central install CLI's explicit --target classic-era branch."""
    d.require(not args.initial_retrofit and not args.retire_file, 'No Era PROD retrofit or retirement')
    lock = read_lock(args.lock or LOCK)
    evidence = verify_api(args.client_root, lock)
    expected, _ = family_files(lock, args.sources_root)
    archive = args.artifacts / ('Apogee-' + lock['version'] + '-DEV.zip')
    payload = dual.validate(archive.read_bytes(), expected)
    previous = json.loads(args.previous_install.read_bytes()) if args.previous_install else None
    live_update = getattr(args, 'allow_running_era_update', False)
    d.require(not live_update or previous is not None, 'Live updates require a prior installed Era receipt')
    desired, known, preview, docs = prepare(args.client_root, payload, previous)
    if live_update:
        verify_live_update(payload, preview, previous)
    running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq WowClassic.exe', '/FO', 'CSV', '/NH'],
                             capture_output=True, text=True, check=True)
    client_running = 'wowclassic.exe' in running.stdout.lower()
    if args.inspect_only:
        return {'target': 'classic-era', 'writeCount': len(preview['writes']),
                'roots': sorted({p.split('/')[0] for p in payload}), 'managedRoots': list(NAMES),
                'preservedDocumentation': docs, 'clientRunning': client_running, 'retired': preview['retired'],
                'requiresClosedClientForInstall': not live_update, 'apiEvidence': evidence,
                'archiveSha256': d.sha(archive.read_bytes()), 'installed': False}
    d.require(not client_running or live_update, 'Close Classic Era or explicitly opt into a verified live update')
    result = m.apply(args.client_root, desired, known, args.backup, preview, NAMES, atomic_files=True, retired=preview['retired'])
    result.update(target='classic-era', family='DEV', publicationAllowed=False,
                  packageRoots=sorted({p.split('/')[0] for p in payload}),
                  supportLayout='embedded-master' if support.master_payload(payload) else 'standalone',
                  lockSha256=d.sha(d.canonical(lock)), apiEvidence=evidence,
                  archiveSha256=d.sha(archive.read_bytes()), preservedDocumentation=docs,
                  liveUpdate=live_update, clientRunningAtPreflight=client_running,
                  activation='Full game restart required for Apogee addon/loading changes; no settings imported' if preview['retired'] or any(p.endswith('.toc') and p not in preview['before'] for p in preview['writes']) or any((p.startswith('ApogeeUIDev/') or '/SharedUI/' in p) and p not in preview['before'] for p in preview['writes']) else 'User /reload after installation; no settings imported' if previous
                  else 'User opens Era and selects Apogee Era DEV; no settings imported')
    (args.backup / 'transaction.json').write_bytes(d.canonical(result))
    return {'status': result['status'], 'target': 'classic-era', 'writeCount': len(result['writes']),
            'receipt': str(args.backup / 'transaction.json'), 'activation': result['activation']}


def rollback_target(backup):
    """Explicit recovery after approval. No API freshness requirement to undo a failed install."""
    backup = m.ordinary(backup)
    receipt = json.loads(m.under(backup, 'transaction.json').read_bytes())
    client = m.ordinary(receipt['client'])
    d.require(client.name == CLIENT['directory'] and set(receipt['names']) in RECEIPT_ROOTS,
              'Only exact Era DEV receipts can be rolled back here')
    # A failed transaction may not yet have the post-install target annotation.
    d.require(receipt.get('target') in (None, 'classic-era'), 'Foreign target receipt refused')
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq WowClassic.exe', '/FO', 'CSV', '/NH'],
                            capture_output=True, text=True, check=True)
    d.require('wowclassic.exe' not in result.stdout.lower(), 'Close Classic Era before rollback')
    journal = m.rollback(backup)
    return {'status': journal['status'], 'target': 'classic-era', 'receipt': str(backup / 'transaction.json')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client-root', type=Path)
    parser.add_argument('--sources-root', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--rollback', type=Path, help='Explicit approved recovery of an Era transaction backup')
    parser.add_argument('--lock', type=Path, default=LOCK)
    args = parser.parse_args()
    if args.rollback:
        d.require(not any((args.client_root, args.sources_root, args.output)), 'Rollback cannot be combined with a build')
        print(json.dumps(rollback_target(args.rollback)))
        return
    d.require(all((args.client_root, args.sources_root, args.output)), 'Build requires client, sources and new output paths')
    lock = read_lock(args.lock)
    evidence = verify_api(args.client_root, lock)
    manifest = build(lock, args.sources_root, args.output, evidence)
    print(json.dumps({k: manifest[k] for k in ('archive', 'archiveSha256', 'apiEvidence', 'publicationAllowed')}))


if __name__ == '__main__':
    main()
