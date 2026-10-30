"""Validate isolated Era and future Forever candidates; never install or publish."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import distribution as d
import dual_distribution as dual
import era_distribution as era


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def verify_test_sources(locks, worktrees):
    pins = {}
    for lock in locks:
        children = {child['name']: child['commit'] for child in lock['children']}
        for support in lock.get('supportModules', []):
            d.require(children.get(support['sourceChild']) == support['commit'], 'Support/test source revision mismatch')
        for name, commit in children.items():
            d.require(name not in pins or pins[name] == commit, 'Candidate test revisions differ: ' + name)
            pins[name] = commit
    for name, commit in pins.items():
        root = worktrees/name
        d.require(git(root, 'rev-parse', 'HEAD') == commit, 'Wrong test source revision: ' + name)
        d.require(not git(root, 'status', '--porcelain'), 'Uncommitted test source: ' + name)
    return pins


def verify_candidate_sources(locks, era_root, future_root=None):
    d.require(len(locks) == 2, 'Expected Era and future Forever locks')
    return [verify_test_sources([lock], root) for lock, root in
            zip(locks, (era_root, future_root or era_root))]


def validate(args):
    locks = [era.read_lock(), d.read_lock(d.ROOT/'distribution/future-launcher.lock.json')]
    future_root = args.future_child_worktrees or args.child_worktrees
    roots = [args.child_worktrees, future_root]
    pins = verify_candidate_sources(locks, args.child_worktrees, future_root)
    d.require(not args.artifact_root.exists(), 'Use a new external artifact directory')
    # No inherited client exports or generated-runtime overrides may contaminate a run.
    env = {k: v for k, v in os.environ.items() if not k.startswith('APOGEE_')}
    env.update(APOGEE_CHILD_WORKTREES=str(args.child_worktrees), APOGEE_FUTURE_CHILD_WORKTREES=str(future_root),
               APOGEE_SOURCES_ROOT=str(args.sources_root))
    def run(command, cwd=d.ROOT):
        subprocess.run([str(x) for x in command], cwd=cwd, env=env, check=True)
    def python(*command): run([sys.executable, '-B', *command])
    evidence = None if args.offline else era.verify_api(args.client_root, locks[0])
    from forever_client import verify_live_export
    forever_evidence = verify_live_export(args.forever_client_root, locks[1]) if args.forever_client_root else None
    print('Era: ' + ('OFFLINE ONLY; no export or installable Era artifact' if args.offline else 'matching export verified'), flush=True)
    print('Future Forever: ' + ('matching live export verified; native acceptance still required' if forever_evidence
                               else 'OFFLINE ONLY; fresh export and native acceptance still required'), flush=True)
    args.artifact_root.mkdir(parents=True)
    tested = set()
    sources = [(name, commit, parent/name) for target, parent in zip(pins, roots) for name, commit in target.items()]
    for name, commit, root in sources:
        if (name, commit) in tested: continue
        tested.add((name, commit))
        for file in git(root, 'ls-files', '*.lua').splitlines(): run(['luac', '-p', file], root)
        specs = sorted((root/'tests').glob('*_spec.lua'))
        if name == 'ApogeeStats': specs += sorted((root/'tests').glob('test_*.lua'))
        for spec in specs: run(['lua', spec], root)
        if name == 'ApogeeStats': run([sys.executable, '-B', 'tests/check_baseline.py'], root)
        if any((root/'tests').rglob('test_*.py')):
            run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], root)
        # Standalone child builders are explicitly non-installable source checks.
        builder = root/'scripts/build-package.ps1'
        if builder.exists(): run(['pwsh', '-NoProfile', '-File', builder, '-SourceOnly'], root)
    python('tests/distribution/test_candidates.py', '-v')
    python('tests/distribution/test_live_forever.py', '-v')
    python('tests/distribution/test_release_manifest.py', '-v')
    python('tests/distribution/test_release_packages.py', '-v')
    command = ['tests/distribution/test_era.py', '--sources-root', args.sources_root,
               '--child-worktrees', args.child_worktrees, '-v']
    if not args.offline: command += ['--client-root', args.client_root]
    python(*command)
    python('tests/distribution/test_launcher.py', '-v')
    if not args.skip_frozen_regression:
        for test in ('test_repository', 'test_curseforge', 'test_publisher'):
            python('tests/distribution/' + test + '.py')
        for test in ('test_distribution', 'test_migration', 'test_dual'):
            python('tests/distribution/' + test + '.py', '--sources-root', args.sources_root,
                   '--artifacts', args.artifact_root/test)
    dual.build(locks[1], args.sources_root, args.artifact_root/('future-forever-validated' if forever_evidence else 'future-forever-offline'))
    if evidence: era.build(locks[0], args.sources_root, args.artifact_root/'packages', evidence)
    # Detect a checkout changed while the tests were running.
    verify_candidate_sources(locks, args.child_worktrees, future_root)
    d.require(locks == [era.read_lock(), d.read_lock(d.ROOT/'distribution/future-launcher.lock.json')],
              'Candidate locks changed during validation')
    if forever_evidence:
        d.require(verify_live_export(args.forever_client_root, locks[1]) == forever_evidence,
                  'Live Forever authority changed during validation')
    run(['git', 'diff', '--check'])
    receipt = {'testSources': dict(zip(('era', 'futureForever'), pins)), 'lockSha256': [d.sha(d.canonical(lock)) for lock in locks],
               'eraApiEvidence': evidence, 'futureForeverApiEvidence': forever_evidence,
               'futureForeverOfflineOnly': forever_evidence is None, 'nativeAccepted': False,
               'frozenRegressionRun': not args.skip_frozen_regression}
    (args.artifact_root/'candidate-validation.json').write_bytes(d.canonical(receipt))
    print(json.dumps(receipt, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--child-worktrees', type=Path, required=True)
    parser.add_argument('--future-child-worktrees', type=Path,
                        help='Exact future Forever test checkouts when its pins differ from Era; defaults to --child-worktrees')
    parser.add_argument('--sources-root', type=Path, default=Path('C:/Dev/WoW'))
    parser.add_argument('--artifact-root', type=Path, required=True)
    parser.add_argument('--client-root', type=Path, default=Path('C:/Program Files (x86)/World of Warcraft/_classic_era_'))
    parser.add_argument('--forever-client-root', type=Path,
                        help='Verify current live Forever authority before and after candidate checks; no installation')
    parser.add_argument('--offline', action='store_true', help='No export check and no installable Era artifact')
    parser.add_argument('--skip-frozen-regression', action='store_true', help='Focused rerun only after unchanged frozen suites passed')
    try: validate(parser.parse_args())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, 'Candidate validation stopped: ' + str(error) + '\n')


if __name__ == '__main__': main()
