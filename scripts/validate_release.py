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
        specs=sorted((root/'tests').glob('*_spec.lua'))
        if child['name']=='ApogeeStats': specs+=sorted((root/'tests').glob('test_*.lua'))
        for spec in specs: run(['lua',spec],root)
        if child['name']=='ApogeeStats': run([sys.executable,'-B','tests/check_baseline.py'],root)
        if any((root/'tests').rglob('test_*.py')): run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],root)
    for test in ('test_repository','test_curseforge','test_publisher','test_release_manifest','test_release_packages'):
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
