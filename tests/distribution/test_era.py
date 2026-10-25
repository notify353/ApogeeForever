"""Era packaging/installer boundaries plus real generated Lua adapter tests; offline acceptance only."""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import distribution as d
import dual_distribution as dual
import era_distribution as era
import migrate_distribution as m


class EraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = era.read_lock()
        if CLIENT_ROOT:
            era.verify_api(CLIENT_ROOT, cls.lock)
        cls.payload, cls.changes = era.family_files(cls.lock, SOURCES)

    def test_exact_isolated_payload_and_dev_storage(self):
        self.assertEqual({p.split('/')[0] for p in self.payload}, set(era.NAMES))
        for name in era.NAMES:
            meta, runtime = d.toc_info(self.payload[name + '/' + name + '.toc'])
            self.assertEqual(meta['Interface'], '11509')
            self.assertEqual(meta['X-Apogee-Client'], 'classic-era')
            self.assertFalse(any(k.startswith('X-Curse') for k in meta))
            if name == d.MARKER + 'Dev':
                self.assertEqual(runtime, [])
                self.assertFalse(any(k.startswith('SavedVariables') for k in meta))
            else:
                self.assertEqual(runtime[0], dual.GATE_PATH)
                self.assertEqual(runtime[-2:], ['Era/Adapter.lua', name + '.lua'])
                for key, value in meta.items():
                    if key.startswith('SavedVariables'):
                        self.assertIn(name, value)
                for path in runtime[1:]:
                    self.assertTrue(self.payload[name + '/' + path].startswith(dual.prefix(name, 'DEV')))
        self.assertEqual(dual.validate(d.zip_bytes(self.payload), self.payload), self.payload)

    def test_changed_source_or_unloaded_lua_rejected(self):
        lock = copy.deepcopy(self.lock)
        lock['children'][0]['files']['Era/Adapter.lua'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'pinned file mismatch'):
            era.family_files(lock, SOURCES)
        damaged = dict(self.payload)
        damaged['ApogeeStatsDev/unexpected.lua'] = b''
        with self.assertRaises(ValueError):
            dual.validate(d.zip_bytes(damaged), self.payload)

    def test_forever_lock_cannot_be_reinterpreted(self):
        with self.assertRaises((ValueError, KeyError)):
            era.read_lock(ROOT / 'distribution/candidate.lock.json')
        with self.assertRaises((ValueError, KeyError)):
            d.read_lock(era.LOCK)
        for field, value in [('reviewedBuild', '1.15.9.70004'), ('directory', '_classic_beta_')]:
            lock = copy.deepcopy(self.lock); lock['client'][field] = value
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'lock.json'; path.write_bytes(d.canonical(lock))
                with self.assertRaises(ValueError): era.read_lock(path)

    def client_fixture(self, folder):
        client = Path(folder) / '_classic_era_'
        (client / 'Interface/AddOns').mkdir(parents=True)
        return client

    def test_fresh_install_backup_receipt_and_preservation(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client_fixture(folder)
            m.put(client / 'Interface/AddOns', {'CodexWoWBridge/note.txt': b'keep',
                  'ApogeeHealsDev/README.md': b'personal note', 'ApogeeHealsDev/custom.txt': b'keep'})
            desired, known, preview, docs = era.prepare(client, self.payload)
            self.assertIn('ApogeeHealsDev/README.md', docs)
            backup = Path(folder) / 'backup'
            result = m.apply(client, desired, known, backup, preview, era.NAMES)
            self.assertEqual(result['status'], 'installed')
            self.assertEqual((client / 'Interface/AddOns/ApogeeHealsDev/README.md').read_bytes(), b'personal note')
            self.assertEqual((client / 'Interface/AddOns/CodexWoWBridge/note.txt').read_bytes(), b'keep')
            self.assertEqual((backup / 'addons-before/ApogeeHealsDev/custom.txt').read_bytes(), b'keep')
            with patch.object(era.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='INFO: none')):
                self.assertEqual(era.rollback_target(backup)['status'], 'rolled-back')
            self.assertFalse((client / 'Interface/AddOns/ApogeeHealsDev/ApogeeHealsDev.lua').exists())
            self.assertEqual((client / 'Interface/AddOns/ApogeeHealsDev/README.md').read_bytes(), b'personal note')
            self.assertTrue((backup / 'rollback-added-files/ApogeeHealsDev/ApogeeHealsDev.lua').is_file())

    def test_era_rollback_rejects_running_client_and_forever_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client_fixture(folder)
            backup = Path(folder) / 'backup'; backup.mkdir()
            receipt = {'client': str(client), 'names': list(era.NAMES), 'target': 'classic-era'}
            (backup / 'transaction.json').write_bytes(d.canonical(receipt))
            with patch.object(era.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='WowClassic.exe')):
                with self.assertRaisesRegex(ValueError, 'Close Classic Era'): era.rollback_target(backup)
            receipt['client'] = str(Path(folder) / '_classic_beta_')
            (backup / 'transaction.json').write_bytes(d.canonical(receipt))
            with self.assertRaisesRegex(ValueError, 'Only exact Era'): era.rollback_target(backup)

    def test_unexpected_runtime_loader_and_foreign_receipt_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client_fixture(folder)
            runtime = 'ApogeeHealsDev/ApogeeHealsDev.lua'
            m.put(client / 'Interface/AddOns', {runtime: b'user edit'})
            with self.assertRaisesRegex(ValueError, 'conflicting edit'):
                era.prepare(client, self.payload)
            previous = {'schema': 1, 'status': 'installed', 'target': 'forever', 'family': 'DEV',
                        'client': str(client), 'names': era.NAMES, 'after': {runtime: d.sha(b'user edit')}}
            with self.assertRaisesRegex(ValueError, 'Era DEV receipt'):
                era.prepare(client, self.payload, previous)
            previous['target'] = 'classic-era'; previous['client'] = str(Path(folder) / '_classic_beta_')
            with self.assertRaisesRegex(ValueError, 'another client'):
                era.prepare(client, self.payload, previous)
            previous['client'] = str(client)
            era.prepare(client, self.payload, previous)
            m.put(client / 'Interface/AddOns', {'ApogeeHealsDev/ApogeeHealsDev_Vanilla.toc': b'bad.lua'})
            with self.assertRaisesRegex(ValueError, 'Unexpected child loader'):
                era.prepare(client, self.payload, previous)

    def test_api_wrong_product_stale_export_changed_executable(self):
        with tempfile.TemporaryDirectory() as folder:
            client = self.client_fixture(folder)
            config = Path(folder) / 'config'; config.mkdir()
            (client.parent / '.build.info').write_text('Product!STRING:0|Version!STRING:0\nwow_classic_era|1.15.9.70003\n')
            exe = client / 'WowClassic.exe'; exe.write_bytes(b'reviewed executable')
            path = client / 'BlizzardInterfaceCode/Interface/AddOns/API.lua'
            path.parent.mkdir(parents=True); path.write_bytes(b'reviewed API')
            os.utime(exe, (100, 100)); os.utime(path, (200, 200))
            record = {'executableSha256': d.sha(exe.read_bytes()), 'files': [{'path': 'API.lua', 'sha256': d.sha(path.read_bytes())}]}
            (config / 'api-evidence.json').write_bytes(d.canonical(record))
            lock = copy.deepcopy(self.lock); lock['apiEvidenceSha256'] = d.sha(d.canonical(record))
            with patch.object(era, 'CONFIG', config):
                self.assertEqual(era.verify_api(client, lock)['referencesVerified'], 1)
                os.utime(path, (50, 50))
                with self.assertRaisesRegex(ValueError, 'Stale Era'): era.verify_api(client, lock)
                os.utime(path, (200, 200)); path.write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'reference changed'): era.verify_api(client, lock)
                exe.write_bytes(b'new executable')
                with self.assertRaisesRegex(ValueError, 'executable changed'): era.verify_api(client, lock)
                (client.parent / '.build.info').write_text('Product|Version\nwowf|1.60.1.70532\n')
                with self.assertRaisesRegex(ValueError, 'product build'): era.verify_api(client, lock)

    def test_generated_gates_and_each_adapter(self):
        with tempfile.TemporaryDirectory() as folder:
            m.put(folder, self.payload)
            subprocess.run([LUA, str(ROOT / 'tests/distribution/era_gate.lua'), folder], check=True)
            for name in era.MEMBERS:
                env = os.environ.copy(); env['APOGEE_ERA_RUNTIME_ROOT'] = str(Path(folder) / (name + 'Dev'))
                if CLIENT_ROOT:
                    env['APOGEE_ERA_EXPORT'] = str(CLIENT_ROOT / 'BlizzardInterfaceCode/Interface/AddOns')
                subprocess.run([LUA, 'tests/era_spec.lua'], cwd=CHILD_WORKTREES / name, env=env, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources-root', type=Path, default=Path('C:/Dev/WoW'))
    parser.add_argument('--child-worktrees', type=Path, required=True)
    parser.add_argument('--lua', default='lua')
    parser.add_argument('--client-root', type=Path)
    args, rest = parser.parse_known_args()
    SOURCES, CHILD_WORKTREES, LUA = args.sources_root, args.child_worktrees, args.lua
    CLIENT_ROOT = args.client_root
    unittest.main(argv=[sys.argv[0], *rest])
