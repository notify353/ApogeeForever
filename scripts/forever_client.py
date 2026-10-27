"""Explicit live Forever authority; no game operation, installation or fallback."""
import argparse
import json
from pathlib import Path
from distribution import LIVE_CLIENT

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT/'distribution/forever/api-evidence.json'


def verify_evidence(lock, evidence_path=EVIDENCE):
    import distribution as d
    d.require(lock['client'] == LIVE_CLIENT, 'Unreviewed live Forever client identity')
    record = json.loads(Path(evidence_path).read_bytes())
    d.require(d.sha(d.canonical(record)) == lock.get('liveApiEvidenceSha256'), 'Live Forever evidence differs from lock')
    d.require(record.get('schema') == 1 and record.get('client') == LIVE_CLIENT, 'Wrong live Forever evidence identity')
    d.require(record.get('sourcePins') == {c['name']: c['commit'] for c in lock['children']}, 'Live evidence source pins differ')
    d.require(isinstance(record.get('files'), list) and record['files'], 'Missing live API inventory')
    seen = set()
    for item in record['files']:
        path = d.safe_path(item['path'])
        d.require(path.casefold() not in seen, 'Duplicate live API reference')
        seen.add(path.casefold())
    return record


def verify_live_export(client_root, lock, evidence_path=EVIDENCE):
    import distribution as d
    import migrate_distribution as m
    record = verify_evidence(lock, evidence_path)
    client = m.ordinary(client_root)
    d.require(client.name == LIVE_CLIENT['directory'], 'Only the reviewed live Forever directory is allowed')
    lines = m.under(client.parent, '.build.info').read_text(encoding='utf-8-sig').splitlines()
    d.require(bool(lines), 'Missing live Forever build metadata')
    keys = [k.split('!')[0] for k in lines[0].split('|')]
    d.require('Product' in keys and 'Version' in keys, 'Unknown live Forever build metadata')
    rows = [dict(zip(keys, line.split('|'))) for line in lines[1:] if line]
    selected = [r for r in rows if r.get('Product') == LIVE_CLIENT['product']]
    d.require(len(selected) == 1 and selected[0].get('Version') == LIVE_CLIENT['reviewedBuild']
              and selected[0].get('Active', '1') == '1', 'Live Forever build changed/missing/inactive; fresh review required')
    exe = m.under(client, LIVE_CLIENT['executable'])
    d.require(exe.is_file() and d.sha(exe.read_bytes()) == record['executableSha256'], 'Live Forever executable differs from reviewed export')
    export = m.under(client, 'BlizzardInterfaceCode/Interface/AddOns')
    for item in record['files']:
        path = m.under(export, item['path'])
        d.require(path.is_file(), 'Missing live Forever API reference: ' + item['path'])
        d.require(path.stat().st_mtime_ns >= exe.stat().st_mtime_ns, 'Stale live Forever export: ' + item['path'])
        d.require(d.sha(path.read_bytes()) == item['sha256'], 'Live Forever API reference changed: ' + item['path'])
    return {'build': LIVE_CLIENT['reviewedBuild'], 'product': LIVE_CLIENT['product'],
            'directory': LIVE_CLIENT['directory'], 'referencesVerified': len(record['files']),
            'evidenceSha256': lock['liveApiEvidenceSha256']}


def main():
    import distribution as d
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client-root', type=Path, required=True)
    parser.add_argument('--lock', type=Path, default=ROOT/'distribution/future-launcher.lock.json')
    args = parser.parse_args()
    try:
        print(json.dumps(verify_live_export(args.client_root, d.read_lock(args.lock)), indent=2))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, 'Live Forever authority stopped: ' + str(error) + '\n')


if __name__ == '__main__': main()
