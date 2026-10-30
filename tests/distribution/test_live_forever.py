"""Live client authority and installer destination tests; synthetic files only."""
import copy
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
import distribution as d
import forever_client as live
import migrate_distribution as migration


class LiveForeverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.client = self.root/'_forever_'
        self.client.mkdir()
        self.exe = self.client/'Wow.exe'; self.exe.write_bytes(b'reviewed live binary')
        os.utime(self.exe, (1000, 1000))
        self.reference = self.client/'BlizzardInterfaceCode/Interface/AddOns/Example/API.lua'
        self.reference.parent.mkdir(parents=True); self.reference.write_bytes(b'reviewed API')
        self.info = self.root/'.build.info'
        self.info.write_text('Product!STRING:0|Version!STRING:0|Active!DEC:1\nwowf|1.60.1.70685|1\nwow_classic_era|1.15.9.70576|1\n')
        self.lock = d.read_lock(ROOT/'distribution/future-launcher.lock.json')
        self.lock['client'] = copy.deepcopy(live.LIVE_CLIENT)
        self.record = {'schema': 1, 'client': copy.deepcopy(live.LIVE_CLIENT),
                       'executableSha256': d.sha(self.exe.read_bytes()),
                       'sourcePins': {c['name']: c['commit'] for c in self.lock['children']},
                       'files': [{'path': 'Example/API.lua', 'sha256': d.sha(self.reference.read_bytes())}]}
        self.evidence = self.root/'evidence.json'
        self.save_record()

    def save_record(self):
        self.evidence.write_bytes(d.canonical(self.record))
        self.lock['liveApiEvidenceSha256'] = d.sha(d.canonical(self.record))

    def verify(self):
        return live.verify_live_export(self.client, self.lock, self.evidence)

    def test_live_export_and_legacy_locks_are_separate(self):
        result = self.verify()
        self.assertEqual(result['build'], '1.60.1.70685')
        self.assertEqual(result['referencesVerified'], 1)
        self.assertEqual(d.read_lock(ROOT/'distribution/candidate.lock.json')['client']['reviewedBuild'], '1.60.1.70450')
        with self.assertRaises(ValueError):
            live.verify_live_export(self.client, d.read_lock(ROOT/'distribution/candidate.lock.json'), self.evidence)

    def test_committed_evidence_matches_candidate_and_all_child_pins(self):
        lock = d.read_lock(ROOT/'distribution/future-launcher.lock.json')
        record = live.verify_evidence(lock)
        self.assertEqual(set(record['sourcePins']), set(d.ACTIVE_CHILDREN))
        self.assertGreater(len(record['files']), 200)
        self.assertEqual(lock['supportModules'][0]['commit'], record['sourcePins']['ApogeeEssentials'])
        for path in ('Blizzard_ProjectConstants/Camelot/ProjectConstants.lua',
                     'Blizzard_Menu/Menu.lua', 'Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua'):
            self.assertIn(path, [r['path'] for r in record['files']])

    @unittest.skipUnless(shutil.which('pwsh'), 'PowerShell required')
    def test_default_live_wrapper_propagates_missing_client_failure(self):
        result = subprocess.run(['pwsh', '-NoProfile', '-File', str(ROOT/'scripts/check-wow-api-export.ps1'),
                                 '-WowRoot', str(self.root/'absent'), '-RequireInstalled'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no beta or offline fallback', result.stderr)

    def test_missing_stale_changed_and_wrong_executable_rejected(self):
        for defect in ('missing', 'stale', 'changed', 'wrong-exe'):
            with self.subTest(defect=defect):
                self.reference.write_bytes(b'reviewed API'); os.utime(self.reference, (2000, 2000))
                self.exe.write_bytes(b'reviewed live binary'); os.utime(self.exe, (1000, 1000))
                if defect == 'missing': self.reference.unlink()
                if defect == 'stale': os.utime(self.reference, (900, 900))
                if defect == 'changed': self.reference.write_bytes(b'changed API')
                if defect == 'wrong-exe': self.exe.write_bytes(b'unreviewed binary')
                with self.assertRaises(ValueError): self.verify()

    def test_wrong_duplicate_inactive_or_missing_product_rejected(self):
        for rows in ('wow_classic_beta|1.60.1.70685|1', 'wowf|1.60.1.70450|1',
                     'wowf|1.60.1.70685|0', 'wowf|1.60.1.70685|1\nwowf|1.60.1.70685|1', ''):
            with self.subTest(rows=rows):
                self.info.write_text('Product|Version|Active\n'+rows+'\n')
                with self.assertRaises(ValueError): self.verify()

    def test_no_client_directory_or_identity_fallback(self):
        for folder in ('_classic_beta_', '_classic_era_', '_retail_'):
            wrong = self.root/folder; wrong.mkdir()
            with self.subTest(folder=folder), self.assertRaises(ValueError):
                live.verify_live_export(wrong, self.lock, self.evidence)
        for key,value in [('product','wow_classic_beta'), ('directory','_classic_beta_'),
                          ('executable','WowB.exe'), ('reviewedBuild','1.60.1.70686')]:
            bad = copy.deepcopy(self.lock); bad['client'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                live.verify_live_export(self.client, bad, self.evidence)
            path = self.root/'bad.lock.json'; path.write_bytes(d.canonical(bad))
            with self.assertRaises(ValueError): d.read_lock(path)

    def test_evidence_tampering_source_pin_drift_and_unsafe_paths_rejected(self):
        original = copy.deepcopy(self.record)
        for defect in ('digest', 'source', 'traversal', 'duplicate'):
            self.record = copy.deepcopy(original); self.save_record()
            if defect == 'digest': self.record['executableSha256'] = '0'*64; self.evidence.write_bytes(d.canonical(self.record))
            if defect == 'source': self.record['sourcePins']['ApogeeStats'] = '0'*40; self.save_record()
            if defect == 'traversal': self.record['files'][0]['path'] = '../outside.lua'; self.save_record()
            if defect == 'duplicate': self.record['files'].append(copy.deepcopy(self.record['files'][0])); self.save_record()
            with self.subTest(defect=defect), self.assertRaises(ValueError): self.verify()

    def test_live_process_detection_and_export_gate_precede_any_write(self):
        process = subprocess.CompletedProcess([], 0, stdout='"Wow.exe","123"\n', stderr='')
        real_verify = live.verify_live_export
        with patch.object(live, 'verify_live_export', side_effect=lambda c,l: real_verify(c,l,self.evidence)), \
             patch.object(migration, 'os', SimpleNamespace(name='nt')), \
             patch.object(migration.subprocess, 'run', return_value=process) as tasklist:
            self.assertTrue(migration.real_client_preflight(self.client, self.lock, allow_running_dev=True))
            self.assertIn('IMAGENAME eq Wow.exe', tasklist.call_args.args[0])
            with self.assertRaisesRegex(ValueError, 'close it before migration'):
                migration.real_client_preflight(self.client, self.lock)
            tasklist.return_value = subprocess.CompletedProcess([], 0, stdout='"WowB.exe","123"\n', stderr='')
            self.assertFalse(migration.real_client_preflight(self.client, self.lock))
            count = tasklist.call_count
            self.reference.write_bytes(b'changed')
            with self.assertRaises(ValueError): migration.real_client_preflight(self.client, self.lock, allow_running_dev=True)
            self.assertEqual(tasklist.call_count, count)
        self.assertFalse((self.client/'Interface').exists())


if __name__ == '__main__': unittest.main()
