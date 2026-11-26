"""Validate a narrow Forever change against an exact full baseline; never install."""
import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import distribution as d
import dual_distribution as dual
from forever_client import verify_live_export

CHILD = 'ApogeeKeybinds'
LOCK = 'distribution/future-launcher.lock.json'
EVIDENCE = 'distribution/forever/api-evidence.json'
ERA_LOCK = 'distribution/era/candidate.lock.json'
SPECS = ('warrior_defaults_spec.lua', 'vanguard_default_spec.lua',
         'intercept_default_spec.lua', 'marker_defaults_spec.lua')
SOURCE_ONLY = ('default_toggle_spec.lua',)
POLICY = ('Actions/Defaults.lua', 'common/Actions/Defaults.lua')
DIST_ALLOWED = {LOCK, EVIDENCE, 'CHANGELOG.md', 'distribution/DUAL_WORKFLOW.md'}


def require(value, reason):
    d.require(value, 'Full validation required: ' + reason)


def changed(before, after):
    return sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))


def pins(lock):
    return {c['name']: c['commit'] for c in lock['children']}


def select(dist_before, dist_after, child_before, child_after, receipt):
    """Pure policy; compare complete trees, not a caller-supplied changed-file list."""
    require(receipt.get('profile') == 'full' and receipt.get('frozenRegressionRun') is True,
            'baseline must be a full run, not another focused receipt')
    require(receipt.get('futureForeverOfflineOnly') is False,
            'baseline must verify the live Forever export')
    old, new = (json.loads(t[LOCK]) for t in (dist_before, dist_after))
    old_era = json.loads(dist_before[ERA_LOCK])
    require(receipt.get('lockSha256') == [d.sha(d.canonical(old_era)), d.sha(d.canonical(old))],
            'baseline receipt does not match its recorded distribution commit')
    require(receipt.get('testSources') == {'era': pins(old_era), 'futureForever': pins(old)},
            'baseline source pins do not match')
    old_evidence, new_evidence = (json.loads(t[EVIDENCE]) for t in (dist_before, dist_after))
    for lock, evidence in ((old, old_evidence), (new, new_evidence)):
        require(d.sha(d.canonical(evidence)) == lock.get('liveApiEvidenceSha256'), 'API evidence hash differs')
        require(evidence.get('sourcePins') == pins(lock), 'API evidence source pins differ')
    require(receipt.get('futureForeverApiEvidence', {}).get('evidenceSha256') == old['liveApiEvidenceSha256'],
            'baseline live evidence differs')
    require(not (set(changed(dist_before, dist_after)) - DIST_ALLOWED),
            'distribution tooling, loaders, transforms, releases, Era or other packaging changed')
    old_shape, new_shape = copy.deepcopy(old), copy.deepcopy(new)
    for shape in (old_shape, new_shape):
        shape.pop('version', None); shape.pop('liveApiEvidenceSha256', None)
        selected = next(c for c in shape['children'] if c['name'] == CHILD)
        selected.pop('commit'); selected.pop('files')
    require(old_shape == new_shape, 'another child, support module or package contract changed')
    old_api, new_api = copy.deepcopy(old_evidence), copy.deepcopy(new_evidence)
    old_api.pop('sourcePins'); new_api.pop('sourcePins')
    require(old_api == new_api, 'client/export authority changed')
    a, b = (next(c for c in lock['children'] if c['name'] == CHILD) for lock in (old, new))
    require(set(a['files']) == set(b['files']), 'package inventory changed')
    paths = changed(child_before, child_after)
    extra_specs = []
    for path in paths:
        require(path in child_after, 'source or test deletion: ' + path)
        if path in POLICY:
            marker = b'local warrior='
            require(marker in child_before.get(path, b'') and marker in child_after[path],
                    'default policy boundary changed')
            require(child_before[path].split(marker, 1)[0] == child_after[path].split(marker, 1)[0],
                    'shared default presentation/storage helpers changed')
        elif re.fullmatch(r'tests/[A-Za-z0-9_]+_spec\.lua', path):
            extra_specs.append(path.split('/')[-1])
        else:
            require(path in ('README.md', 'CHANGELOG.md') or (path.startswith('docs/') and path.endswith('.md')),
                    'unmapped source, harness or shared execution change: ' + path)
    require(child_after[POLICY[0]] == child_after[POLICY[1]], 'generated default copy differs')
    for path, digest in b['files'].items():
        require(path in child_after and d.sha(child_after[path]) == digest, 'candidate source hash differs: ' + path)
    source = sorted(set(SPECS + SOURCE_ONLY) | set(extra_specs))
    generated = sorted((set(SPECS) | set(extra_specs)) - set(SOURCE_ONLY))
    for spec in source:
        require('tests/' + spec in child_after, 'required regression missing: ' + spec)
    return {'profile': 'keybinds-defaults', 'changedSourceFiles': paths,
            'sourceSuites': source, 'generatedDevSuites': generated,
            'reusedCoverage': ['unchanged children', 'Era', 'generated PROD behavior', 'frozen packages and rollback']}


def git(root, *args):
    return d.git_bytes(root, *args).decode().strip()


def context(args):
    root = d.ROOT
    require(not git(root, 'status', '--porcelain'), 'distribution worktree is dirty; commit reviewed changes first')
    receipt = json.loads(args.baseline.read_bytes())
    base = receipt.get('distributionCommit', '')
    require(bool(re.fullmatch('[0-9a-f]{40}', base)), 'baseline lacks immutable distribution provenance')
    head = git(root, 'rev-parse', 'HEAD')
    require(git(root, 'merge-base', base, head) == base, 'baseline is not an ancestor of the candidate')
    before, after = d.source_tree(root, base), d.source_tree(root, head)
    require(set(git(root, 'diff', '--name-only', '--no-renames', base, head).splitlines()) == set(changed(before, after)),
            'distribution archive does not represent every changed tracked path')
    old, new = (json.loads(t[LOCK]) for t in (before, after))
    old_pin, new_pin = pins(old)[CHILD], pins(new)[CHILD]
    require(git(args.child, 'rev-parse', 'HEAD') == new_pin, 'wrong changed-child checkout')
    require(not git(args.child, 'status', '--porcelain'), 'changed-child worktree is dirty')
    require(git(args.child, 'merge-base', old_pin, new_pin) == old_pin, 'child baseline is not an ancestor')
    old_tree, new_tree = d.source_tree(args.child, old_pin), d.source_tree(args.child, new_pin)
    require(set(git(args.child, 'diff', '--name-only', '--no-renames', old_pin, new_pin).splitlines()) == set(changed(old_tree, new_tree)),
            'child archive does not represent every changed tracked path')
    plan = select(before, after, old_tree, new_tree, receipt)
    return plan, new, head, new_pin


def validate(args):
    baseline_sha = d.sha(args.baseline.read_bytes())
    plan, lock, head, pin = context(args)
    print(json.dumps(plan, indent=2), flush=True)
    if args.plan: return
    require(args.artifact_root is not None and not args.artifact_root.exists(), 'use a new artifact directory')
    require(args.client_root is not None, 'focused installation artifacts require live Forever authority')
    evidence = verify_live_export(args.client_root, lock)
    env = {k: v for k, v in os.environ.items() if not k.startswith('APOGEE_')}
    # beta_native.lua concatenates paths; retain the trailing slash.
    env['APOGEE_KEYBINDS_EXPORT_ROOT'] = (args.client_root/'BlizzardInterfaceCode/Interface/AddOns').as_posix() + '/'
    def run(command, cwd=args.child, selected_env=env):
        subprocess.run([str(x) for x in command], cwd=cwd, env=selected_env, check=True)
    for tool in ('lua', 'luac'):
        result = subprocess.run([tool, '-v'], text=True, capture_output=True, check=True)
        require('Lua 5.1' in result.stdout + result.stderr, 'Lua 5.1 is required')
    args.artifact_root.mkdir(parents=True)
    # Syntax is cheap: check all tracked child Lua, but execute only the selected suites.
    for path in git(args.child, 'ls-files', '*.lua').splitlines(): run(['luac', '-p', path])
    for spec in plan['sourceSuites']: run(['lua', 'tests/' + spec])
    packages = args.artifact_root/'future-forever-validated'
    hashes = dual.build(lock, args.sources_root, packages)
    dev, _ = dual.family_files(lock, args.sources_root, 'DEV')
    runtime = args.artifact_root/'generated-dev'
    for path, content in dev.items():
        target = runtime/d.safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(content)
    generated_env = dict(env, APOGEE_KEYBINDS_RUNTIME_ROOT=str(runtime/(CHILD + 'Dev')),
                         APOGEE_KEYBINDS_RUNTIME_NAME=CHILD + 'Dev')
    for spec in plan['generatedDevSuites']: run(['lua', 'tests/' + spec], selected_env=generated_env)
    # Catch concurrent source, metadata or executable/export changes before issuing a receipt.
    require(context(args) == (plan, lock, head, pin), 'candidate changed during validation')
    require(d.sha(args.baseline.read_bytes()) == baseline_sha, 'baseline receipt changed during validation')
    require(verify_live_export(args.client_root, lock) == evidence, 'live authority changed during validation')
    run(['git', 'diff', '--check'], cwd=d.ROOT)
    result = dict(plan, schema=1, distributionCommit=head, sourcePin=pin,
                  baselineReceiptSha256=baseline_sha,
                  baselineDistributionCommit=json.loads(args.baseline.read_bytes())['distributionCommit'],
                  lockSha256=d.sha(d.canonical(lock)), packageSha256=hashes,
                  futureForeverApiEvidence=evidence, nativeAccepted=False,
                  publicationAllowed=False, fullValidation=False)
    (args.artifact_root/'focused-validation.json').write_bytes(d.canonical(result))
    print('PASS focused validation: %d source suites + %d generated DEV suites; full baseline reused, no install.' %
          (len(plan['sourceSuites']), len(plan['generatedDevSuites'])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True, help='Prior full candidate-validation.json')
    parser.add_argument('--child', type=Path, required=True, help='Clean Keybinds checkout at the candidate pin')
    parser.add_argument('--sources-root', type=Path, default=Path('C:/Dev/WoW'))
    parser.add_argument('--artifact-root', type=Path)
    parser.add_argument('--client-root', type=Path)
    parser.add_argument('--plan', action='store_true', help='Read-only selection; no tests, builds or installation')
    try: validate(parser.parse_args())
    except (ValueError, OSError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        parser.exit(1, 'Focused validation stopped: ' + str(error) + '\nUse the full validate_candidates.py workflow for changes outside this profile.\n')


if __name__ == '__main__': main()
