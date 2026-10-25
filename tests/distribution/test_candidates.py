"""Candidate validation must use test sources from both immutable locks."""
import copy
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'scripts'))
import validate_candidates as candidates


class CandidateTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('pwsh'), 'PowerShell required')
    def test_child_builders_refuse_installable_output(self):
        root = Path(os.environ.get('APOGEE_CHILD_WORKTREES', str(Path(__file__).resolve().parents[3])))
        for child in ('ApogeeEssentials', 'ApogeeKeybinds', 'ApogeeGroupAlert'):
            with self.subTest(child=child), tempfile.TemporaryDirectory() as directory:
                folder = Path(directory); script = folder/'build-package.ps1'
                shutil.copyfile(root/child/'scripts/build-package.ps1', script)
                result = subprocess.run(['pwsh', '-NoProfile', '-File', str(script)],
                                        capture_output=True, text=True, encoding='utf-8', errors='replace')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('central checked distribution workflow', result.stderr)
                self.assertEqual([p.name for p in folder.iterdir()], ['build-package.ps1'])

    def test_all_children_and_support_are_pinned(self):
        lock = {'children': [{'name': 'ApogeeHeals', 'commit': 'a'*40},
                             {'name': 'ApogeeEssentials', 'commit': 'b'*40}],
                'supportModules': [{'sourceChild': 'ApogeeEssentials', 'commit': 'b'*40}]}
        future = copy.deepcopy(lock)
        future['children'].append({'name': 'ApogeeStats', 'commit': 'c'*40})
        def git(root, *args):
            if args == ('status', '--porcelain'): return ''
            return {'ApogeeHeals': 'a', 'ApogeeEssentials': 'b', 'ApogeeStats': 'c'}[root.name]*40
        with patch.object(candidates, 'git', side_effect=git):
            self.assertEqual(len(candidates.verify_test_sources([lock, future], Path('worktrees'))), 3)
            for defect in ('support', 'different-pin', 'wrong-head', 'dirty', 'missing'):
                bad = copy.deepcopy(future)
                if defect == 'support': bad['supportModules'][0]['commit'] = 'd'*40
                if defect == 'different-pin': bad['children'][0]['commit'] = 'd'*40
                def broken(root, *args):
                    if root.name == 'ApogeeStats':
                        if defect == 'missing': raise OSError('missing test checkout')
                        if defect == 'dirty' and args[0] == 'status': return ' M tests/spec.lua'
                        if defect == 'wrong-head' and args[0] == 'rev-parse': return 'd'*40
                    return git(root, *args)
                with self.subTest(defect=defect), patch.object(candidates, 'git', side_effect=broken):
                    with self.assertRaises((ValueError, OSError)):
                        candidates.verify_test_sources([lock, bad], Path('worktrees'))


if __name__ == '__main__': unittest.main()
