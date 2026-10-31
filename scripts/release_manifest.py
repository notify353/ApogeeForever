"""Immutable per-version release selection. No network, installation or publication."""
import argparse
import copy
import json
from pathlib import Path
import re

import distribution as d
import dual_distribution as dual
import era_distribution as era
import forever_client as forever

ROOT = d.ROOT / 'distribution/releases'
TARGETS = {
    'classic-era': {'label': 'Apogee Classic Era', 'filename': 'ApogeeClassicEra',
                    'name': '1.15.9', 'gameVersionTypeID': 67408, 'interface': '11509'},
    'forever': {'label': 'Apogee Forever', 'filename': 'ApogeeForever',
                'name': '1.60.1', 'gameVersionTypeID': 88568, 'interface': '16001'},
}


def stable(version):
    d.require(isinstance(version, str) and re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version), 'Stable version required')
    return version


def path(version):
    return ROOT / stable(version) / 'manifest.json'


def load(version):
    folder = path(version).parent
    manifest = json.loads(path(version).read_bytes())
    d.require(manifest.get('schema') == 1 and manifest.get('version') == version
              and manifest.get('target') in TARGETS and manifest.get('projectId') == 1608100
              and manifest.get('releaseType') == 'release', 'Invalid release selection')
    target = manifest['target']
    lock = (era.read_lock if target == 'classic-era' else d.read_lock)(folder/'source.lock.json')
    evidence = json.loads((folder/'api-evidence.json').read_bytes())
    d.require(d.sha(d.canonical(lock)) == manifest['sourceLockSha256'], 'Release source lock changed')
    d.require(d.sha(d.canonical(evidence)) == manifest['apiEvidenceSha256']
              == lock['apiEvidenceSha256' if target == 'classic-era' else 'liveApiEvidenceSha256'], 'Release API evidence changed')
    if target == 'classic-era':
        d.require(evidence.get('clientVersion') == lock['client']['reviewedBuild']
                  and evidence.get('product') == lock['client']['product']
                  and evidence.get('interface') == lock['client']['interface'], 'Era release authority identity mismatch')
    else:
        # The immutable selection has its own reviewed identity. read_lock above
        # enforces the historical allowlist; live installs still require LIVE_CLIENT.
        forever.verify_evidence(lock, folder/'api-evidence.json', expected_client=lock['client'])
    d.require(manifest.get('curseforge') == {k: TARGETS[target][k] for k in ('name','gameVersionTypeID')}, 'Wrong upload flavor')
    approval = manifest['authorization']
    d.require(approval.get('kind') == 'owner-approved-early-release' and approval.get('nativeAccepted') is False
              and isinstance(approval.get('basis'), str) and approval['basis'].strip(), 'Explicit truthful release authorization required')
    d.require(set(manifest['packages']) == {'PROD','DEV'} and all(re.fullmatch('[0-9a-f]{64}', v) for v in manifest['packages'].values()), 'Exact package hashes required')
    notes = (folder/'release-notes.md').read_text(encoding='utf-8')
    d.require(d.sha(notes.encode()) == manifest['notesSha256'], 'Release notes changed')
    return manifest, lock, notes


def files(target, lock, sources, version, family):
    lock = copy.deepcopy(lock); lock['version'] = stable(version)
    result = (era.family_files(lock, sources, family) if target == 'classic-era'
              else dual.family_files(lock, sources, family))[0]
    if family == 'PROD' and target == 'forever':
        result[d.MARKER+'/README.md'] = (d.ROOT/'distribution/forever/PUBLIC_README.md').read_bytes()
    return result


def packages(version, sources):
    manifest, lock, notes = load(version)
    target = manifest['target']; outputs = {}
    for family in ('PROD','DEV'):
        generated = files(target, lock, sources, version, family)
        suffix = 'Dev' if family == 'DEV' else ''
        roots = {d.MARKER+suffix, *(c['name']+suffix for c in lock['children'])}
        d.require({p.split('/')[0] for p in generated} == roots, 'Wrong release family roots')
        for root in roots:
            meta, _ = d.toc_info(generated[root+'/'+root+'.toc'])
            d.require(meta['Interface'] == TARGETS[target]['interface'] and meta['X-Apogee-Family'] == family, 'Wrong release client/family')
        archive = d.zip_bytes(generated); dual.validate(archive, generated)
        d.require(d.sha(archive) == manifest['packages'][family], 'Release package differs from approved bytes')
        outputs[family] = archive
    return manifest, outputs, notes


def prepare(target, version, sources, client, notes_path, basis):
    stable(version); d.require(target in TARGETS, 'Unknown release target')
    d.require(not path(version).parent.exists(), 'Release version already prepared; never overwrite')
    lock = era.read_lock() if target == 'classic-era' else d.read_lock(d.ROOT/'distribution/future-launcher.lock.json')
    evidence_path = era.CONFIG/'api-evidence.json' if target == 'classic-era' else forever.EVIDENCE
    authority = era.verify_api(client, lock) if target == 'classic-era' else forever.verify_live_export(client, lock)
    notes = Path(notes_path).read_text(encoding='utf-8')
    d.require(notes.strip() and basis.strip(), 'Player notes and authorization basis required')
    archives = {family: d.zip_bytes(files(target, lock, sources, version, family)) for family in ('PROD','DEV')}
    manifest = {'schema': 1, 'version': version, 'target': target, 'projectId': 1608100, 'releaseType': 'release',
                'sourceLockSha256': d.sha(d.canonical(lock)), 'apiEvidenceSha256': authority['evidenceSha256'],
                'curseforge': {k: TARGETS[target][k] for k in ('name','gameVersionTypeID')},
                'packages': {f:d.sha(b) for f,b in archives.items()}, 'notesSha256':d.sha(notes.encode()),
                'authorization': {'kind':'owner-approved-early-release','nativeAccepted':False,'basis':basis}}
    folder = path(version).parent; folder.mkdir(parents=True, exist_ok=False)
    (folder/'source.lock.json').write_bytes(d.canonical(lock))
    (folder/'api-evidence.json').write_bytes(evidence_path.read_bytes())
    (folder/'release-notes.md').write_text(notes, encoding='utf-8', newline='\n')
    path(version).write_bytes(d.canonical(manifest))
    packages(version, sources)
    return manifest


def stage(version, sources, output):
    manifest, archives, notes = packages(version, sources)
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    filename = TARGETS[manifest['target']]['filename']+'-'+version+'.zip'
    (output/filename).write_bytes(archives['PROD'])
    (output/(filename+'.sha256')).write_text(manifest['packages']['PROD']+'  '+filename+'\n')
    (output/'release-notes.md').write_text(notes, encoding='utf-8', newline='\n')
    receipt = {'schema':2,'version':version,'target':manifest['target'],'projectId':1608100,'filename':filename,
               'sha256':manifest['packages']['PROD'],'manifestSha256':d.sha(d.canonical(manifest)),
               'publicationState':'staged','nativeAccepted':False,'curseforgeClientTested':False}
    (output/'receipt.json').write_bytes(d.canonical(receipt))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('prepare','pins','check'))
    parser.add_argument('--version', required=True)
    parser.add_argument('--target', choices=tuple(TARGETS))
    parser.add_argument('--sources-root', type=Path)
    parser.add_argument('--client-root', type=Path)
    parser.add_argument('--notes', type=Path)
    parser.add_argument('--basis')
    args = parser.parse_args()
    if args.operation == 'prepare':
        d.require(all((args.target,args.sources_root,args.client_root,args.notes,args.basis)), 'Preparation arguments required')
        print(json.dumps(prepare(args.target,args.version,args.sources_root,args.client_root,args.notes,args.basis)))
    elif args.operation == 'pins':
        lock = load(args.version)[1] if path(args.version).exists() else d.read_lock(dual.LOCK)
        for child in lock['children']: print(child['name']+'='+child['commit'])
    else:
        manifest, _, _ = packages(args.version,args.sources_root)
        print(json.dumps({'version':args.version,'target':manifest['target'],'packages':manifest['packages']}))


if __name__ == '__main__': main()
