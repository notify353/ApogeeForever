"""Focused validation must cover narrow changes and reject broader or stale inputs."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import validate_change as v


class SelectionTests(unittest.TestCase):
    def setUp(self):
        policy = (b'helpers\nlocal warrior={}\nlocal defensiveWarrior={}\n'
                  b'    local spellId=defaults and defaults[slotId]\n'
                  b'    if state=="spell2458" then spellId=20252 end\n'
                  b'    local spell=spellId and K.API.Family(spellId)\ncompile defaults\n')
        self.child = {p: policy for p in v.POLICY}
        self.child.update({'tests/' + s: b'assert(true)\n' for s in v.SPECS + v.SOURCE_ONLY})
        self.child['Actions/Secure.lua'] = b'secure dispatcher\n'
        self.child['tests/mock.lua'] = b'harness\n'
        self.lock = {'version': '1-dev.1', 'client': {'build': 'reviewed'},
                     'children': [{'name': v.CHILD, 'commit': 'a'*40, 'toc': 'Keybinds.toc',
                                   'files': {v.POLICY[0]: v.d.sha(self.child[v.POLICY[0]])}},
                                  {'name': 'ApogeeHeals', 'commit': 'b'*40, 'files': {}}],
                     'supportModules': [{'commit': 'c'*40}]}
        self.api = {'sourcePins': v.pins(self.lock), 'files': [{'sha256': 'reviewed'}]}
        self.lock['liveApiEvidenceSha256'] = v.d.sha(v.d.canonical(self.api))
        self.era = {'children': [{'name': 'ApogeeKeybinds', 'commit': 'd'*40}]}
        self.dist = {v.LOCK: v.d.canonical(self.lock), v.EVIDENCE: v.d.canonical(self.api),
                     v.ERA_LOCK: v.d.canonical(self.era), 'scripts/distribution.py': b'tooling'}
        self.receipt = {'profile': 'full', 'frozenRegressionRun': True,
                        'futureForeverOfflineOnly': False,
                        'lockSha256': [v.d.sha(v.d.canonical(self.era)), v.d.sha(v.d.canonical(self.lock))],
                        'testSources': {'era': v.pins(self.era), 'futureForever': v.pins(self.lock)},
                        'futureForeverApiEvidence': {'evidenceSha256': self.lock['liveApiEvidenceSha256']}}

    def candidate(self, edits=None, lock_edit=None, api_edit=None, dist_edit=None):
        child = dict(self.child)
        for path, data in (edits or {}).items():
            if data is None: child.pop(path)
            else: child[path] = data
        lock = copy.deepcopy(self.lock)
        lock['version'] = '1-dev.2'; lock['children'][0]['commit'] = 'e'*40
        lock['children'][0]['files'] = {p: v.d.sha(child[p]) for p in self.lock['children'][0]['files'] if p in child}
        if lock_edit: lock_edit(lock)
        api = copy.deepcopy(self.api); api['sourcePins'] = v.pins(lock)
        if api_edit: api_edit(api)
        lock['liveApiEvidenceSha256'] = v.d.sha(v.d.canonical(api))
        dist = dict(self.dist, **{v.LOCK: v.d.canonical(lock), v.EVIDENCE: v.d.canonical(api)})
        if dist_edit: dist_edit(dist)
        return dist, child

    def choose(self, **kwargs):
        dist, child = self.candidate(**kwargs)
        return v.select(self.dist, dist, self.child, child, self.receipt)

    def test_default_change_selects_focused_source_and_dev_without_other_families(self):
        edited = self.child[v.POLICY[0]].replace(b'local warrior={}', b'local warrior={key3=2458}')
        plan = self.choose(edits={p: edited for p in v.POLICY})
        self.assertEqual(plan['profile'], 'keybinds-defaults')
        self.assertEqual(len(plan['sourceSuites']), 5)
        self.assertEqual(len(plan['generatedDevSuites']), 4)
        self.assertEqual(plan['changedSourceFiles'], list(v.POLICY))

    def test_new_regression_is_included_and_selected_suites_are_deduplicated(self):
        plan = self.choose(edits={'tests/new_default_spec.lua': b'new test',
                                 'tests/intercept_default_spec.lua': b'updated regression'})
        self.assertIn('new_default_spec.lua', plan['sourceSuites'])
        self.assertIn('new_default_spec.lua', plan['generatedDevSuites'])
        self.assertEqual(plan['sourceSuites'].count('intercept_default_spec.lua'), 1)

    def test_recheck_and_documentation_only_change_keep_the_small_profile(self):
        self.assertEqual(self.choose()['profile'], 'keybinds-defaults')
        self.choose(edits={'README.md': b'updated usage'})

    def test_shared_execution_harness_and_unmapped_changes_require_full(self):
        for path in ('Actions/Secure.lua', 'Actions/Compile.lua', 'Core/Client.lua',
                     'UI/Hud.lua', 'tests/mock.lua', 'scripts/test-local.ps1', 'ApogeeKeybinds.toc'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'Full validation required'):
                self.choose(edits={path: b'changed'})

    def test_test_deletion_and_generated_drift_require_full(self):
        for edits in ({'tests/intercept_default_spec.lua': None},
                      {v.POLICY[0]: b'helpers\nlocal warrior={new=true}'},
                      {p: b'changed helper\nlocal warrior={}' for p in v.POLICY}):
            with self.subTest(edits=edits), self.assertRaises(ValueError): self.choose(edits=edits)

    def test_other_child_support_client_and_inventory_changes_require_full(self):
        edits = [lambda x: x['children'][1].update(commit='f'*40),
                 lambda x: x['supportModules'][0].update(commit='f'*40),
                 lambda x: x['client'].update(build='new'),
                 lambda x: x['children'][0]['files'].update({'new.lua': 'hash'}),
                 lambda x: x['children'][0].update(toc='Other.toc')]
        for edit in edits:
            with self.subTest(edit=edit), self.assertRaises(ValueError): self.choose(lock_edit=edit)

    def test_export_change_requires_full_even_when_hash_is_rebound(self):
        with self.assertRaisesRegex(ValueError, 'authority changed'):
            self.choose(api_edit=lambda x: x['files'][0].update(sha256='new'))

    def test_mapping_file_cannot_hide_new_calls_or_shared_compiler_changes(self):
        original = self.child[v.POLICY[0]]
        for old, new in [(b'spellId=20252', b'spellId=NewAPI()'),
                         (b'spellId=20252', b'state=20252'),
                         (b'compile defaults', b'changed compiler'),
                         (b'spellId=20252', b'while true do end'),
                         (b'spellId=20252', b'spellId=K.API.LearnedSpell(999)')]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.choose(edits={p: original.replace(old, new) for p in v.POLICY})

    def test_existing_vanguard_query_and_new_stance_mapping_are_supported(self):
        original = self.child[v.POLICY[0]]
        choices = b'spellId=K.API.LearnedSpell(1310317) and 100 or 2457'
        self.choose(edits={p: original.replace(b'spellId=20252', choices) for p in v.POLICY})

    def test_distribution_tooling_era_and_release_changes_require_full(self):
        for path in ('scripts/distribution.py', 'scripts/install_dual_distribution.py',
                     'distribution/FamilyGate.lua', v.ERA_LOCK, 'distribution/releases/1/manifest.json'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.choose(dist_edit=lambda x: x.update({path: b'changed'}))

    def test_no_focused_offline_or_mismatched_baseline_can_anchor_a_run(self):
        for field, value in [('profile', 'keybinds-defaults'), ('profile', 'full-without-frozen'),
                             ('frozenRegressionRun', False), ('futureForeverOfflineOnly', True),
                             ('lockSha256', []), ('testSources', {}), ('futureForeverApiEvidence', {})]:
            with self.subTest(field=field, value=value):
                receipt = copy.deepcopy(self.receipt); receipt[field] = value
                dist, child = self.candidate()
                with self.assertRaises(ValueError): v.select(self.dist, dist, self.child, child, receipt)

    def test_package_hash_mismatch_and_missing_required_regression_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'source hash differs'):
            self.choose(lock_edit=lambda x: x['children'][0]['files'].update({v.POLICY[0]: 'wrong'}))
        before = dict(self.child); before.pop('tests/warrior_defaults_spec.lua')
        after = dict(before)
        with self.assertRaisesRegex(ValueError, 'regression missing'):
            v.select(self.dist, self.dist, before, after, self.receipt)

    def test_dirty_distribution_is_rejected_before_reading_baseline(self):
        from argparse import Namespace
        with patch.object(v, 'git', return_value=' M scripts/distribution.py'):
            with self.assertRaisesRegex(ValueError, 'worktree is dirty'):
                v.context(Namespace(baseline=Path('must-not-be-read')))


if __name__ == '__main__': unittest.main()
