"""Exact release sources and generated target checks; no install or upload."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import distribution as d
import era_distribution as era
import release_manifest as r
from validate_candidates import verify_test_sources, git


# These exact contracts execute Blizzard code from the owner's local beta export.
# They remain in validate_candidates.py's complete local run. Never replace that
# authority with mocks or copy the proprietary export into a hosted checkout.
LOCAL_EXPORT_CONTRACTS = {
    'ApogeeKeybinds': {'tests/export_contract_spec.lua': 'c344972a4f119fbfc715bf948060a56284bc5c52614f09c8279f23e74a47d7c6'},
    'ApogeeGroupAlert': {'tests/export_whisper_spec.lua': 'c0b7550818af18757b068a620691c395ca7667d5a4cbe349d8031bbed9d0221b'},
    'ApogeeEssentials': {'tests/blizzard_errors_spec.lua': 'a48b138e895d191b69538596f4417edf810ec7d0a07d00171c342071aefbac16'},
}


def lua_specs(root, name):
    specs=sorted((root/'tests').glob('*_spec.lua'))
    if name=='ApogeeStats': specs+=sorted((root/'tests').glob('test_*.lua'))
    local_only=LOCAL_EXPORT_CONTRACTS.get(name,{})
    for path,digest in local_only.items():
        spec=root/path
        d.require(spec in specs, 'Local export contract missing; review test inventory: '+name+'/'+path)
        d.require(d.sha(spec.read_bytes())==digest, 'Local export contract changed; review classification: '+name+'/'+path)
    return [p for p in specs if p.relative_to(root).as_posix() not in local_only],sorted(local_only)


def validate(version, sources, children, output):
    manifest, lock, _ = r.load(version)
    candidate = era.read_lock() if manifest['target']=='classic-era' else d.read_lock(d.ROOT/'distribution/future-launcher.lock.json')
    d.require(lock == candidate, 'Release test candidate differs from snapshot')
    verify_test_sources([lock], children)
    d.require(not output.exists(), 'Use a new release validation directory')
    env={k:v for k,v in os.environ.items() if not k.startswith('APOGEE_')}
    env.update(APOGEE_SOURCES_ROOT=str(sources),APOGEE_CHILD_WORKTREES=str(children),
               APOGEE_FUTURE_CHILD_WORKTREES=str(children),APOGEE_TEST_TARGET=manifest['target'],
               APOGEE_RELEASE_VERSION=version)
    def run(args,cwd=d.ROOT): subprocess.run([str(x) for x in args],cwd=cwd,env=env,check=True)
    for child in lock['children']:
        root=children/child['name']
        for file in git(root,'ls-files','*.lua').splitlines(): run(['luac','-p',file],root)
        specs,local_only=lua_specs(root,child['name'])
        for path in local_only:
            print('LOCAL EXPORT ONLY (not a hosted pass): '+child['name']+'/'+path,flush=True)
        for spec in specs: run(['lua',spec],root)
        if child['name']=='ApogeeStats': run([sys.executable,'-B','tests/check_baseline.py'],root)
        if any((root/'tests').rglob('test_*.py')): run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],root)
    for test in ('test_repository','test_curseforge','test_publisher','test_release_manifest','test_release_runner','test_release_packages'):
        run([sys.executable,'-B','tests/distribution/'+test+'.py'])
    run([sys.executable,'-B','tests/distribution/test_launcher.py','LauncherTests.test_generated_behavior_all_targets',
         'LauncherTests.test_generated_settings_with_real_shared_owner','-v'])
    if manifest['target']=='classic-era':
        run([sys.executable,'-B','tests/distribution/test_era.py','--sources-root',sources,'--child-worktrees',children])
    # Source pins and package hashes are rechecked after all generated tests.
    verify_test_sources([lock],children)
    return r.stage(version,sources,output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',required=True)
    parser.add_argument('--sources-root',type=Path,required=True)
    parser.add_argument('--child-worktrees',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    validate(args.version,args.sources_root,args.child_worktrees,args.output)
