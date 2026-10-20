import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import distribution as d
import dual_distribution as dual
import migrate_distribution as m
import install_dual_distribution as installer
import publish_distribution as publisher


class DualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = d.read_lock(dual.LOCK)
        cls.known = m.catalog(ROOT / 'distribution/migration-known.json')
        cls.prod, cls.prod_changes = dual.family_files(cls.lock, OPTIONS.sources_root, 'PROD')
        cls.dev, cls.dev_changes = dual.family_files(cls.lock, OPTIONS.sources_root, 'DEV')
        OPTIONS.artifacts.mkdir(parents=True, exist_ok=False); OPTIONS.owns_artifacts = True
        m.put(OPTIONS.artifacts / 'PROD', cls.prod); m.put(OPTIONS.artifacts / 'DEV', cls.dev)
        cls.counter = 0

    def fixture(self, files):
        type(self).counter += 1
        base = OPTIONS.artifacts / ('fixture-' + str(self.counter))
        client = base / '_classic_beta_'; (client / 'Interface/AddOns').mkdir(parents=True)
        m.put(client / 'Interface/AddOns', files)
        m.put(client, {'WTF/Account/Private/SavedVariables/ApogeeEssentials.lua': b'private prod settings',
                       'WTF/Account/Private/AddOns.txt': b'unchanged enablement',
                       'Interface/AddOns/Unrelated/keep.txt': b'unchanged unrelated'})
        return client, base / 'backup'

    def test_native_forever_identity_and_revision_tolerance(self):
        # Warning baselines follow the reviewed source pins, independently of install provenance.
        reviewed_children = {'ApogeeHeals': '70450', 'ApogeeGroupAlert': '70450', 'ApogeeEssentials': '70450'}
        reviewed_build = self.lock['client']['reviewedBuild'].rsplit('.', 1)[-1]
        for child in self.lock['children']:
            if child['name'] == 'ApogeeStats':
                continue  # Stats client identity is covered by its pinned generated-package suite.
            warning_build = reviewed_children.get(child['name'], reviewed_build if child['name'] == 'ApogeeKeybinds' else None)
            reviewed = warning_build is not None
            for family in (('PROD', 'DEV') if reviewed else ('DEV',)):
                name = child['name'] + ('Dev' if family == 'DEV' else '')
                subprocess.run(['lua', str(ROOT / 'tests/distribution/client_identity.lua'),
                                str(OPTIONS.artifacts / family / name), name] +
                               [warning_build or '', reviewed_build], check=True)

    def test_reviewed_dungeon_aliases_in_generated_families(self):
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeGroupAlert')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family in ('PROD', 'DEV'):
            name = child['name'] + ('Dev' if family == 'DEV' else '')
            harness = OPTIONS.artifacts / ('dungeon-vocabulary-' + family)
            (harness / 'tests').mkdir(parents=True)
            root = (OPTIONS.artifacts / family / name).resolve().as_posix()
            helper = source['tests/helpers.lua'].decode()
            helper = helper.replace('local A = {}', 'local A = {__ApogeeFamilyAdmission=function() return true end}')
            helper = helper.replace('loadfile(path)', 'loadfile(' + json.dumps(root + '/') + ' .. path)')
            helper = helper.replace("'ApogeeGroupAlert'", repr(name))
            (harness / 'tests/helpers.lua').write_text(helper)
            (harness / 'tests/reviewed_vocabulary_spec.lua').write_bytes(source['tests/reviewed_vocabulary_spec.lua'])
            subprocess.run(['lua', 'tests/reviewed_vocabulary_spec.lua'], cwd=harness, check=True)
            (harness / 'tests/mock.lua').write_bytes(source['tests/mock.lua'])
            font_spec = source['tests/roster_font_spec.lua'].decode()
            font_spec = font_spec.replace("loadfile('", "loadfile('" + root + "/")
            font_spec = font_spec.replace("'test'", repr(name))
            (harness / 'tests/roster_font_spec.lua').write_text(font_spec, encoding='utf-8')
            subprocess.run(['lua', 'tests/roster_font_spec.lua'], cwd=harness, check=True)
            # Exercise the real generated UI with the owning startup mock, bypassing
            # only the family lease (covered separately by loading-safety tests).
            toc_lines = source['ApogeeGroupAlert.toc'].decode().splitlines()
            fixture_toc = '\n'.join(root + '/' + (name + '.lua' if line == 'ApogeeGroupAlert.lua' else line)
                                    for line in toc_lines if line.endswith('.lua')) + '\n'
            (harness / 'ApogeeGroupAlert.toc').write_text(fixture_toc)
            ui_spec = source['tests/settings_background_spec.lua'].decode().replace(
                'local A={}', 'local A={__ApogeeFamilyAdmission=function() return true end}')
            ui_spec = ui_spec.replace(')("ApogeeGroupAlert",A)', ')(' + json.dumps(name) + ',A)')
            (harness / 'tests/settings_background_spec.lua').write_text(ui_spec)
            subprocess.run(['lua', 'tests/settings_background_spec.lua'], cwd=harness, check=True)
            for spec in ('discovery_spec.lua', 'reversible_phrases_spec.lua'):
                (harness / 'tests' / spec).write_bytes(source['tests/' + spec])
                subprocess.run(['lua', 'tests/' + spec], cwd=harness, check=True)


    def test_incoming_damage_in_generated_families(self):
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeEssentials')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family in ('PROD', 'DEV'):
            name = child['name'] + ('Dev' if family == 'DEV' else '')
            harness = OPTIONS.artifacts / ('incoming-damage-' + family)
            (harness / 'tests').mkdir(parents=True)
            for path in ('tests/mock.lua', 'tests/incoming_damage_spec.lua'):
                data = source[path]
                if path.endswith('incoming_damage_spec.lua'):
                    data = data.replace(b'"ApogeeEssentials", addon',
                                        ('"' + name + '", addon').encode())
                (harness / path).write_bytes(data)
            subprocess.run(['lua', 'tests/incoming_damage_spec.lua',
                            str((OPTIONS.artifacts / family / name).resolve()),
                            'ApogeeHealsDevAnchor' if family == 'DEV' else 'ApogeeHealsAnchor'],
                           cwd=harness, check=True)

    def test_essentials_error_defaults_in_generated_families(self):
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeEssentials')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family in ('PROD', 'DEV'):
            name = child['name'] + ('Dev' if family == 'DEV' else '')
            harness = OPTIONS.artifacts / ('error-defaults-' + family)
            (harness / 'tests').mkdir(parents=True)
            generated = OPTIONS.artifacts / family / name
            # Exercise unchanged generated chunks with admission supplied by the
            # fixture; complete family gate behavior has separate coverage.
            for path in source['ApogeeEssentials.toc'].decode().splitlines():
                if path.endswith('.lua'):
                    target = name + '.lua' if path == 'ApogeeEssentials.lua' else path
                    dest = harness / target
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes((generated / target).read_bytes())
            (harness / (name + '.toc')).write_bytes(
                source['ApogeeEssentials.toc'].replace(b'ApogeeEssentials', name.encode()))
            for path in ('tests/mock.lua', 'tests/combat_error_defaults_spec.lua', 'tests/defaults_spec.lua', 'tests/error_defaults_migration_spec.lua'):
                data = source[path].replace(b'ApogeeEssentials', name.encode())
                if family == 'DEV':
                    data = data.replace(b'APOGEE_ESSENTIALS_DEFAULTS', b'APOGEE_ESSENTIALS_DEV_DEFAULTS')
                if path.endswith('mock.lua'):
                    data = data.replace(b'local addon={}',
                        b'local addon={__ApogeeFamilyAdmission=function() return true end}')
                (harness / path).write_bytes(data)
            for spec in ('combat_error_defaults_spec.lua', 'defaults_spec.lua', 'error_defaults_migration_spec.lua'):
                subprocess.run(['lua', 'tests/' + spec], cwd=harness, check=True)

    def test_shared_settings_parent_in_generated_families(self):
        subprocess.run(['lua', str(ROOT / 'tests/distribution/shared_settings.lua'),
                        str(OPTIONS.artifacts)], check=True)
        for name in ('ApogeeHeals', 'ApogeeKeybinds', 'ApogeeGroupAlert', 'ApogeeEssentials', 'ApogeeAuction'):
            output, edits = dual.transform_lua(b'-- ApogeeSettingsRegistry\nApogeeSettingsRegistry = {}\n', name)
            self.assertEqual(output, b'-- ApogeeSettingsRegistry\nApogeeDevSettingsRegistry = {}\n')
            self.assertEqual(len(edits), 1)
        for name in ('ApogeeTank', 'ApogeeStats'):
            self.assertNotIn('ApogeeSettingsRegistry', dual.identity_map(name))

    def test_heals_target_buffs_require_friendly_players_in_both_families(self):
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeHeals')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family in ('PROD', 'DEV'):
            name = child['name'] + ('Dev' if family == 'DEV' else '')
            harness = OPTIONS.artifacts / ('heals-target-tests-' + family)
            (harness / 'tests').mkdir(parents=True)
            for path, data in source.items():
                if path.startswith('tests/') and path.endswith('.lua'):
                    target = harness / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
            runner = source['tests/generated_dev.lua'].decode()
            runner = runner.replace('local name = "ApogeeHealsDev"', 'local name = assert(arg[2])')
            runner = runner.replace('"APOGEE_HEALS_DEV_RESET_CHARACTER"',
                                    '(name == "ApogeeHealsDev" and "APOGEE_HEALS_DEV_RESET_CHARACTER" or "APOGEE_HEALS_RESET_CHARACTER")')
            start = runner.index('for _, path in ipairs({')
            end = runner.index('}) do', start) + len('}) do')
            runner = runner[:start] + 'for _, path in ipairs({"tests/bindings_spec.lua", "tests/target_bindings_spec.lua", "tests/range_spec.lua", "tests/bindings_spec.lua", "tests/target_bindings_spec.lua", "tests/range_spec.lua", "tests/target_support_spec.lua", "tests/class_integration_spec.lua", "tests/smart_buffs_spec.lua", "tests/blessing_guidance_spec.lua", "tests/minimap_spec.lua", "tests/buff_strip_spec.lua", "tests/buff_expiry_spec.lua", "tests/buff_foreign_coverage_spec.lua", "tests/buff_range_spec.lua", "tests/leader_spec.lua", "tests/roles_spec.lua", "tests/names_spec.lua", "tests/party_actions_spec.lua"}) do' + runner[end:]
            runner = runner.replace('    assert(loadstring(fixtureTest,', '    if name == "ApogeeHealsDev" then fixtureTest = fixtureTest:gsub("Apogee Heals", "Apogee Heals DEV") end\n    assert(loadstring(fixtureTest,')
            runner = runner.replace('print("PASS generated DEV buffs, tooltips, cleansing buttons, debuffs, drinking timers and spell-range scenarios")', 'print("PASS generated target buffs, class integration and minimap regressions: " .. name)')
            (harness / 'target-generated.lua').write_text(runner)
            subprocess.run(['lua', 'target-generated.lua', str(OPTIONS.artifacts / family / name), name],
                           cwd=harness, check=True)

    def test_keybinds_spell_shift_and_ready_highlight_in_both_families(self):
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeKeybinds')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family in ('PROD', 'DEV'):
            name = child['name'] + ('Dev' if family == 'DEV' else '')
            harness = OPTIONS.artifacts / ('keybinds-spell-tests-' + family)
            (harness / 'tests').mkdir(parents=True)
            for support in ('mock.lua', 'beta_native.lua', 'macro_model.lua'):
                (harness / 'tests' / support).write_bytes(source['tests/' + support])
            env = dict(os.environ, APOGEE_KEYBINDS_RUNTIME_ROOT=str((OPTIONS.artifacts / family / name).resolve()),
                       APOGEE_KEYBINDS_RUNTIME_NAME=name)
            for spec in ('default_toggle_spec.lua', 'spell_override_spec.lua', 'spell_rank_replacement_spec.lua', 'shift_keyboard_spec.lua', 'ready_highlight_spec.lua', 'self_buff_reminder_spec.lua', 'paladin_defaults_spec.lua', 'settings_spec.lua', 'gcd_spec.lua', 'cooldowns_spec.lua', 'defensive_extra_defaults_spec.lua', 'defensive_mouse_defaults_spec.lua', 'minimap_spec.lua', 'minimap_geometry_spec.lua'):
                data = source['tests/' + spec]
                if family == 'DEV':
                    if spec == 'minimap_geometry_spec.lua':
                        # This fixture defaults its runtime name explicitly; production runtime maps stay unchanged.
                        data = data.replace(b'"ApogeeKeybinds"', b'"ApogeeKeybindsDev"')
                    data, _ = dual.transform_lua(data, child['name'])
                (harness / 'tests' / spec).write_bytes(data)
                subprocess.run(['lua', 'tests/' + spec], cwd=harness, env=env, check=True)

    def test_receipted_retirement_and_rollback_preserve_unknown_files(self):
        path = 'ApogeeEssentialsDev/Thanks/Retired.lua'
        extra = 'ApogeeEssentialsDev/Thanks/User.lua'
        files = dict(self.dev); files[path] = b'-- retired module'; files[extra] = b'-- user file'
        client, backup = self.fixture(files)
        previous = {'schema': 1, 'status': 'installed', 'client': str(client), 'after': {path: d.sha(files[path])}}
        result = installer.install(client, self.dev, self.known, backup, previous=previous, retire_files=[path])
        self.assertFalse((client / 'Interface/AddOns' / path).exists())
        self.assertEqual((backup / 'retired-files' / path).read_bytes(), files[path])
        self.assertEqual((client / 'Interface/AddOns' / extra).read_bytes(), files[extra])
        self.assertEqual(result['retired'], previous['after'])
        m.rollback(backup)
        self.assertEqual((client / 'Interface/AddOns' / path).read_bytes(), files[path])

    def test_interrupted_retirement_recovers_from_verified_backup(self):
        paths = ['ApogeeEssentialsDev/Thanks/One.lua', 'ApogeeEssentialsDev/Thanks/Two.lua']
        files = dict(self.dev)
        for p in paths: files[p] = b'-- retired'
        client, backup = self.fixture(files)
        previous = {'schema': 1, 'status': 'installed', 'client': str(client),
                    'after': {p: d.sha(files[p]) for p in paths}}
        replace = m.os.replace
        def fail_second(source, target):
            if str(source).endswith('Two.lua'): raise OSError('injected sharing violation')
            return replace(source, target)
        with patch.object(m.os, 'replace', side_effect=fail_second), self.assertRaises(OSError):
            installer.install(client, self.dev, self.known, backup, previous=previous, retire_files=paths)
        self.assertEqual(json.loads((backup / 'transaction.json').read_text())['status'],
                         'incomplete-recover-with-rollback')
        m.rollback(backup)
        for p in paths: self.assertEqual((client / 'Interface/AddOns' / p).read_bytes(), files[p])

    def test_retirement_refuses_modified_or_packaged_files_and_rollback_conflict(self):
        path = 'ApogeeEssentialsDev/Thanks/Retired.lua'
        files = dict(self.dev); files[path] = b'-- original'
        client, backup = self.fixture(files)
        previous = {'schema': 1, 'status': 'installed', 'client': str(client), 'after': {path: d.sha(files[path])}}
        target = client / 'Interface/AddOns' / path
        target.write_bytes(b'-- user change')
        with self.assertRaises(ValueError):
            installer.install(client, self.dev, self.known, backup, previous=previous, retire_files=[path])
        self.assertFalse(backup.exists())
        target.write_bytes(files[path])
        with self.assertRaises(ValueError):
            installer.install(client, files, self.known, backup, previous=previous, retire_files=[path])
        self.assertFalse(backup.exists())
        installer.install(client, self.dev, self.known, backup, previous=previous, retire_files=[path])
        target.write_bytes(b'-- new user file')
        with self.assertRaises(ValueError): m.rollback(backup)
        self.assertEqual(target.read_bytes(), b'-- new user file')

    def test_public_and_dev_selection_omit_retired_children(self):
        self.assertNotIn('ApogeeTank', d.public_children(self.lock))
        self.assertFalse(any(p.startswith('ApogeeTank/') for p in self.prod))
        self.assertNotIn('ApogeeTankDev/ApogeeTankDev.toc', self.dev)
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            for p, b in files.items():
                if p.endswith('.toc'):
                    meta, runtime = d.toc_info(b)
                    self.assertFalse(any(k in meta for k in ('Dependencies', 'RequiredDeps', 'OptionalDeps', 'LoadWith')))
                    self.assertTrue(all(p.rsplit('/', 1)[0] + '/' + f in files for f in runtime))
        # Simulated acceptance tests publisher mechanics only, never live acceptance.
        accepted = {'accepted': True, 'runtimeFiles': {
            f: {p: d.sha(b) for p, b in files.items() if p.endswith('.lua')}
            for f, files in (('PROD', self.prod), ('DEV', self.dev))}}
        evidence = OPTIONS.artifacts / 'simulated-native-acceptance.json'
        evidence.write_bytes(d.canonical(accepted))
        with patch.object(publisher, 'ACCEPTANCE', evidence):
            self.assertEqual(publisher.payload(OPTIONS.sources_root, self.lock['version']), d.zip_bytes(self.prod))

    def test_stats_guidance_in_both_families_is_guarded(self):
        self.assertIn('ApogeeStats', d.public_children(self.lock))
        child = next(c for c in self.lock['children'] if c['name'] == 'ApogeeStats')
        source = d.source_tree(OPTIONS.sources_root / child['name'], child['commit'])
        for family, files, changes in (('PROD', self.prod, self.prod_changes),
                                       ('DEV', self.dev, self.dev_changes)):
            name = 'ApogeeStats' + ('Dev' if family == 'DEV' else '')
            meta, runtime = d.toc_info(files[name + '/' + name + '.toc'])
            self.assertEqual(runtime, [dual.GATE_PATH, 'Core/Rules.lua', 'Core/Items.lua', name + '.lua', 'Auction/Queue.lua', 'Auction/Browse.lua'])
            self.assertEqual(meta['Title'], 'Apogee Stats' + (' DEV' if family == 'DEV' else ''))
            self.assertFalse(any(k.startswith('SavedVariables') for k in meta))
            path = name + '/' + name + '.lua'
            self.assertEqual(files[path], dual.prefix(name, family) + source['ApogeeStats.lua'])
            self.assertEqual(changes[path]['identityEdits'], [])
            for relative in ('Core/Rules.lua', 'Core/Items.lua', 'Auction/Queue.lua', 'Auction/Browse.lua'):
                self.assertEqual(files[name + '/' + relative], dual.prefix(name, family) + source[relative])
            test_path = OPTIONS.artifacts / ('stats-guidance-' + family + '.lua')
            test_path.write_bytes(source['tests/test_tooltip.lua'])
            subprocess.run(['lua', str(test_path), str(OPTIONS.artifacts / family / name), name], check=True)
            test_path = OPTIONS.artifacts / ('stats-auction-' + family + '.lua')
            test_path.write_bytes(source['tests/test_auction.lua'])
            subprocess.run(['lua', str(test_path), str(OPTIONS.artifacts / family / name), name], check=True)
            test_path = OPTIONS.artifacts / ('stats-policy-' + family + '.lua')
            test_path.write_bytes(source['tests/test_stat_policy.lua'])
            subprocess.run(['lua', str(test_path), str(OPTIONS.artifacts / family / name), name], check=True)
        bad = copy.deepcopy(self.lock)
        next(c for c in bad['children'] if c['name'] == 'ApogeeStats')['files']['ApogeeStats.lua'] = '0' * 64
        for family in ('PROD', 'DEV'):
            with self.assertRaisesRegex(ValueError, 'pinned file mismatch'):
                dual.family_files(bad, OPTIONS.sources_root, family)

    def test_stats_dev_install_and_rollback_preserve_existing_family(self):
        old = {p: b for p, b in self.dev.items() if not p.startswith('ApogeeStatsDev/')}
        client, backup = self.fixture(old)
        result = installer.install(client, self.dev, self.known, backup)
        self.assertIn('ApogeeStatsDev', result['names'])
        self.assertEqual(m.tree(client / 'Interface/AddOns/ApogeeStatsDev'),
                         {p.split('/', 1)[1]: b for p, b in self.dev.items() if p.startswith('ApogeeStatsDev/')})
        self.assertIn('ApogeeStatsDev/ApogeeStatsDev.toc', result['activation']['discoveryChanges'])
        m.rollback(backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns', m.DEV_NAMES + m.LOCAL_DEV_NAMES), old)

    def test_retired_children_are_absent_from_current_sources_and_packages(self):
        self.assertEqual(d.hosted_children(self.lock), d.ACTIVE_CHILDREN)
        for name in ('ApogeeTank', 'ApogeeAuction'):
            for files in (self.prod, self.dev):
                self.assertFalse(any(p.split('/')[0] in (name, name + 'Dev') for p in files))
        # Exclusion does not silently delete an installed old addon or its unknown files.
        retired = {'ApogeeTankDev/keep.txt': b'owner file', 'ApogeeAuctionDev/keep.txt': b'owner file'}
        client, backup = self.fixture(dict(self.dev, **retired))
        installer.install(client, self.dev, self.known, backup)
        for p, data in retired.items():
            self.assertEqual((client / 'Interface/AddOns' / p).read_bytes(), data)
        for name in ('ApogeeTank', 'ApogeeAuction'):
            bad = copy.deepcopy(self.lock); bad['publicChildren'].append(name)
            with self.assertRaises(ValueError): d.public_children(bad)

    def test_explicit_retirement_moves_only_reviewed_dev_roots(self):
        files = {name + '/' + path: data
                 for name in ('ApogeeTankDev', 'ApogeeAuctionDev')
                 for path, data in (('Core.lua', b'-- reviewed runtime'), ('notes.txt', b'owner notes'))}
        for altered in (False, True):
            client, backup = self.fixture(files)
            receipt = backup.parent / 'previous.json'
            receipt.write_bytes(d.canonical({'schema': 1, 'status': 'installed',
                                            'client': str(client), 'after': m.hashes(files)}))
            if altered:
                (client / 'Interface/AddOns/ApogeeTankDev/Core.lua').write_bytes(b'-- owner edit')
            before = m.tree(client)
            result = subprocess.run(['pwsh', '-NoProfile', '-File',
                                     str(ROOT / 'scripts/retire-unused-dev-addons.ps1'),
                                     '-ClientRoot', str(client), '-PreviousInstall', str(receipt),
                                     '-Backup', str(backup)], capture_output=True, text=True)
            if altered:
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(backup.exists())
                self.assertEqual(m.tree(client), before)
            else:
                self.assertEqual(result.returncode, 0, result.stderr)
                for path, data in files.items():
                    self.assertFalse((client / 'Interface/AddOns' / path).exists())
                    self.assertEqual((backup / path).read_bytes(), data)
                remaining = {p: b for p, b in before.items()
                             if not any(p.startswith('Interface/AddOns/' + n + '/')
                                        for n in ('ApogeeTankDev', 'ApogeeAuctionDev'))}
                self.assertEqual(m.tree(client), remaining)
                self.assertEqual(json.loads((backup / 'retirement.json').read_text())['status'], 'retired')

    def test_production_gameplay_bodies_are_identical_to_pins(self):
        source = d.collect(self.lock, OPTIONS.sources_root, 'local-candidate')
        for path, change in self.prod_changes.items():
            prefix = dual.prefix(path.split('/')[0], 'PROD')
            self.assertEqual(self.prod[path], prefix + source[change['source']])
            self.assertEqual(change['identityEdits'], [])

    def test_group_and_heals_icons_bundle_same_brand_asset(self):
        logo = 'Media/Textures/ApogeeLogo.png'
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            suffix = 'Dev' if family == 'DEV' else ''
            expected = files['ApogeeKeybinds' + suffix + '/' + logo]
            for base in (d.MARKER, 'ApogeeHeals', 'ApogeeStats'):
                name = base + suffix
                meta, runtime = d.toc_info(files[name + '/' + name + '.toc'])
                self.assertEqual(meta['IconTexture'], 'Interface/AddOns/' + name + '/' + logo)
                self.assertEqual(files[name + '/' + logo], expected)
                if base == d.MARKER:
                    self.assertEqual(runtime, [])
                    self.assertFalse(any(k.startswith('SavedVariables') for k in meta))

    def test_exact_roots_tocs_guards_separate_saves_and_no_dev_project_ids(self):
        saves = {}
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            names = tuple(n + ('Dev' if family == 'DEV' else '') for n in (d.MARKER, *dual.family_children(self.lock, family)))
            self.assertEqual(set(p.split('/')[0] for p in files), set(names))
            saves[family] = set()
            for name in names:
                meta, runtime = d.toc_info(files[name + '/' + name + '.toc'])
                self.assertEqual(meta['Group'], names[0])
                self.assertEqual(meta['Category'], 'Apogee Forever' if family == 'PROD' else 'Apogee Dev')
                if name.startswith(d.MARKER):
                    self.assertEqual(meta['Title'], 'Apogee Forever' if family == 'PROD' else 'Apogee Dev')
                    self.assertEqual(runtime, []); continue
                self.assertEqual(runtime[0], dual.GATE_PATH)
                self.assertEqual(len(runtime), len(set(runtime)))
                for p in runtime[1:]:
                    self.assertTrue(files[name + '/' + p].startswith(dual.prefix(name, family)))
                for key, value in meta.items():
                    if key.startswith('SavedVariables'): saves[family].update(value.replace(',', ' ').split())
                if family == 'DEV': self.assertFalse(any(k.startswith('X-Curse') for k in meta))
        self.assertTrue(saves['PROD']); self.assertTrue(saves['DEV'])
        self.assertFalse(saves['PROD'] & saves['DEV'])

    def test_release_requires_native_accepted_runtime(self):
        accepted = json.loads(publisher.ACCEPTANCE.read_text())
        actual = {family: {p: d.sha(b) for p, b in files.items() if p.endswith('.lua')}
                  for family, files in (('PROD', self.prod), ('DEV', self.dev))}
        if accepted.get('accepted') is not True:
            with self.assertRaisesRegex(ValueError, 'Native owner acceptance required'):
                publisher.payload(OPTIONS.sources_root, '1.0.0')
        elif actual == accepted['runtimeFiles']:
            self.assertTrue(publisher.payload(OPTIONS.sources_root, '1.0.0').startswith(b'PK'))
        else:
            with self.assertRaisesRegex(ValueError, 'Runtime changed since native acceptance'):
                publisher.payload(OPTIONS.sources_root, '1.0.0')

    def test_running_client_allowed_only_for_dev_preflight(self):
        client, _ = self.fixture(self.dev)
        (client.parent / '.build.info').write_text('Product|Version\nwow_classic_beta|' + self.lock['client']['reviewedBuild'])
        process = subprocess.CompletedProcess([], 0, stdout='"WowB.exe","123"', stderr='')
        # Keep pathlib on the real host platform while simulating the installer OS check.
        with patch.object(m, 'os', SimpleNamespace(name='nt')), patch.object(m.subprocess, 'run', return_value=process):
            self.assertTrue(m.real_client_preflight(client, self.lock, allow_running_dev=True))
            with self.assertRaisesRegex(ValueError, 'close it before migration'):
                m.real_client_preflight(client, self.lock)
            bad = copy.deepcopy(self.lock); bad['client']['reviewedBuild'] = 'wrong'
            with self.assertRaisesRegex(ValueError, 'build changed'):
                m.real_client_preflight(client, bad, allow_running_dev=True)

    def test_atomic_dev_failure_retains_original_and_verified_backup(self):
        client, backup = self.fixture(self.dev)
        updated = dict(self.dev)
        path = 'ApogeeHealsDev/' + dual.GATE_PATH
        updated[path] += b'\n-- next version\n'
        previous = {'schema': 1, 'status': 'installed', 'client': str(client), 'after': m.hashes(self.dev)}
        with patch.object(m.os, 'replace', side_effect=OSError('fixture sharing violation')):
            with self.assertRaisesRegex(OSError, 'sharing violation'):
                installer.install(client, updated, self.known, backup, previous=previous)
        self.assertEqual((client / 'Interface/AddOns' / path).read_bytes(), self.dev[path])
        self.assertEqual(m.tree(backup / 'addons-before'), self.dev)
        self.assertEqual(json.loads((backup / 'transaction.json').read_bytes())['status'], 'incomplete-recover-with-rollback')
        with self.assertRaisesRegex(ValueError, 'DEV-only'):
            m.apply(client, self.prod, self.known, backup.parent / 'forbidden', atomic_dev=True)

    def test_activation_distinguishes_existing_runtime_and_discovery(self):
        self.assertFalse(installer.activation({'before': {'a.lua': b'old'}, 'writes': {'a.lua': b'new'}})['restartRequired'])
        result = installer.activation({'before': {}, 'writes': {'a.lua': b'new', 'a.toc': b'metadata'}})
        self.assertEqual(result['discoveryChanges'], ['a.lua', 'a.toc'])
        self.assertEqual(result['action'], 'user-reload-after-install')

    def test_dev_install_still_refuses_concurrent_protected_changes(self):
        client, backup = self.fixture(self.dev)
        with patch.object(m, 'protected', side_effect=[{}, {'WTF/fixture': [1, 2]}]):
            with self.assertRaisesRegex(ValueError, 'Preferences changed during backup'):
                installer.install(client, self.dev, self.known, backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns', m.DEV_NAMES + m.LOCAL_DEV_NAMES), self.dev)

    def test_public_package_has_player_guide_and_required_notices(self):
        source = d.collect(self.lock, OPTIONS.sources_root, 'local-candidate')
        for child in self.lock['children']:
            if child['name'] not in d.public_children(self.lock): continue
            for p in child['files']:
                path = child['name'] + '/' + p
                if p in ('LICENSE', 'NOTICE.md', 'THIRD_PARTY_NOTICES.md'):
                    self.assertEqual(self.prod[path], source[path])
                elif p.endswith('.md') or p.startswith('docs/'):
                    self.assertNotIn(path, self.prod)
        guide = self.prod[d.MARKER + '/README.md'].decode()
        self.assertIn('Forever 1.60.1', guide)
        self.assertNotIn('PROD', guide)

    def test_every_actual_runtime_chunk_is_denied_without_gameplay_effects(self):
        result = subprocess.run(['lua', str(ROOT / 'tests/distribution/family_matrix.lua'), str(OPTIONS.artifacts)],
                                capture_output=True, text=True)
        (OPTIONS.artifacts / 'family-matrix.log').write_text(result.stdout + result.stderr)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reproducibility_and_corruption(self):
        first = dual.build(self.lock, OPTIONS.sources_root, OPTIONS.artifacts / 'build-a')
        second = dual.build(self.lock, OPTIONS.sources_root, OPTIONS.artifacts / 'build-b')
        self.assertEqual(first, second)
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            self.assertEqual(dual.validate(d.zip_bytes(files), files), files)
            altered = dict(files); p = next(iter(altered)); altered[p] += b'altered'
            with self.assertRaises(ValueError): dual.validate(d.zip_bytes(altered), files)

    def test_one_time_retrofit_and_dev_coexistence_preserve_saves_and_unknown_docs(self):
        historical = d.read_lock()
        # Exercise unguarded historical active children without retired source clones.
        historical['children'] = [c for c in historical['children'] if c['name'] in d.ACTIVE_CHILDREN]
        baseline = d.collect(historical, OPTIONS.sources_root, 'children-only')
        baseline['ApogeeKeybinds/README.md'] = b'user edited documentation'
        baseline['ApogeeTank/unknown.lua'] = b'user source unreferenced'
        client, backup = self.fixture(baseline)
        active_names = tuple(sorted({p.split('/')[0] for p in dict(self.prod, **self.dev)}))
        protected = m.protected(client, active_names)
        legacy_lock = copy.deepcopy(self.lock); legacy_lock.pop('publicChildren', None)
        retrofit_prod, _ = dual.family_files(legacy_lock, OPTIONS.sources_root, 'PROD')
        result = installer.install(client, dict(retrofit_prod, **self.dev), self.known, backup, True)
        self.assertEqual((client / 'Interface/AddOns/ApogeeKeybinds/README.md').read_bytes(), baseline['ApogeeKeybinds/README.md'])
        self.assertEqual(m.protected(client, tuple(result['names'])), protected)
        for p, b in dict(self.prod, **self.dev).items():
            if p not in result['preservedDocumentation']:
                self.assertEqual((client / 'Interface/AddOns' / p).read_bytes(), b)
        m.rollback(backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns'), baseline)

    def test_dev_update_never_touches_production_and_rolls_back(self):
        baseline = dict(self.prod, **self.dev)
        client, backup = self.fixture(baseline)
        original = m.managed(client / 'Interface/AddOns')
        result = installer.install(client, self.dev, self.known, backup)
        self.assertEqual(result['writes'], {})
        self.assertEqual(m.managed(client / 'Interface/AddOns'), original)
        m.rollback(backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns'), original)

    def test_conflicting_dev_runtime_prevents_all_writes(self):
        baseline = dict(self.dev)
        baseline['ApogeeHealsDev/Core/Access.lua'] += b'-- local unexpected change'
        client, backup = self.fixture(baseline)
        before = m.tree(client)
        with self.assertRaises(ValueError): installer.install(client, self.dev, self.known, backup)
        self.assertEqual(m.tree(client), before); self.assertFalse(backup.exists())

    def test_reviewed_dev_update_uses_receipt_and_preserves_rollback_chain(self):
        client, first_backup = self.fixture(self.prod)
        first = installer.install(client, self.dev, self.known, first_backup)
        updated = dict(self.dev)
        path = 'ApogeeHealsDev/' + dual.GATE_PATH
        updated[path] += b'\n-- fixture next reviewed version\n'
        second_backup = first_backup.parent / 'backup-update'
        result = installer.install(client, updated, self.known, second_backup, previous=first)
        self.assertEqual(len(result['writes']), 1)
        self.assertEqual(m.managed(client / 'Interface/AddOns'), self.prod)
        m.rollback(second_backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns', m.DEV_NAMES + m.LOCAL_DEV_NAMES), self.dev)
        m.rollback(first_backup)
        self.assertEqual(m.managed(client / 'Interface/AddOns', tuple(n + 'Dev' for n in m.NAMES)), {})

    def test_lexical_transform_preserves_comments_and_gameplay_literals(self):
        source = b'-- ApogeeTankUIDB\nlocal x="1"; local y="Interface/Icons/Spell"\nApogeeTankUIDB={}\n'
        output, edits = dual.transform_lua(source, 'ApogeeTank')
        self.assertTrue(output.startswith(b'-- ApogeeTankUIDB'))
        self.assertIn(b'ApogeeTankDevUIDB={}', output)
        self.assertIn(b'local x="1"', output)
        with self.assertRaises(ValueError): dual.transform_lua(b'ApogeeTankUnknown={}', 'ApogeeTank')

    def test_dungeons_settings_label_has_exact_dev_mapping(self):
        source = b'-- Apogee Dungeons\nlocal title="Apogee Dungeons"; local text="Keep Apogee Dungeons unchanged"\n'
        output, edits = dual.transform_lua(source, 'ApogeeGroupAlert')
        self.assertEqual(output, b'-- Apogee Dungeons\nlocal title="Apogee Dungeons DEV"; local text="Keep Apogee Dungeons unchanged"\n')
        self.assertEqual(len(edits), 1)
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            name = 'ApogeeGroupAlert' + ('Dev' if family == 'DEV' else '')
            label = 'Apogee Dungeons' + (' DEV' if family == 'DEV' else '')
            settings = files[name + '/Settings/View.lua'].decode()
            self.assertIn('"' + label + '"', settings)

    def test_heals_default_is_independent_and_reset_dialog_is_family_local(self):
        canonical = 'APOGEE_HEALS_RESET_CHARACTER'
        development = 'APOGEE_HEALS_DEV_RESET_CHARACTER'
        for family, files in (('PROD', self.prod), ('DEV', self.dev)):
            suffix = 'Dev' if family == 'DEV' else ''
            settings = files['ApogeeHeals' + suffix + '/UI/Settings.lua'].decode()
            expected = development if suffix else canonical
            forbidden = canonical if suffix else development
            tokens = [token.strip(chr(34) + chr(39)) for kind, token in dual.lua_tokens(settings)
                      if kind in ('identifier', 'string')]
            self.assertIn(expected, tokens)
            self.assertNotIn(forbidden, tokens)
            editor = files['ApogeeHeals' + suffix + '/UI/BindingEditor.lua'].decode()
            self.assertNotIn('ApogeeKeybinds', editor)
            meta, _ = d.toc_info(files['ApogeeHeals' + suffix + '/ApogeeHeals' + suffix + '.toc'])
            self.assertNotIn('Dependencies', meta)
            self.assertNotIn('RequiredDeps', meta)
        source = ('-- ' + canonical + '\nStaticPopup_Show("' + canonical + '")\n').encode()
        output, edits = dual.transform_lua(source, 'ApogeeHeals')
        self.assertEqual(output, ('-- ' + canonical + '\nStaticPopup_Show("' + development + '")\n').encode())
        self.assertEqual(len(edits), 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources-root', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    OPTIONS = parser.parse_args(); OPTIONS.owns_artifacts = False
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DualTests))
    if OPTIONS.owns_artifacts:
        (OPTIONS.artifacts / 'summary.json').write_bytes(d.canonical({
            'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
            'nativeClientTested': False, 'curseforgeAppTested': False}))
    sys.exit(not result.wasSuccessful())
