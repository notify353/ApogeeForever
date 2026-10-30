"""Portable release checks must not silently weaken local export coverage."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'scripts'))
import distribution as d
import validate_release as runner


class RunnerTests(unittest.TestCase):
    def test_only_exact_reviewed_local_contract_is_separated(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/'tests').mkdir()
            local=root/'tests/native_spec.lua'; local.write_bytes(b'local export contract')
            portable=root/'tests/export_portable_spec.lua'; portable.write_bytes(b'mocked export contract')
            policy={'Child': {'tests/native_spec.lua': d.sha(local.read_bytes())}}
            with patch.object(runner,'LOCAL_EXPORT_CONTRACTS',policy):
                specs,local_only=runner.lua_specs(root,'Child')
                self.assertEqual(specs,[portable])
                self.assertEqual(local_only,['tests/native_spec.lua'])
                local.write_bytes(b'changed test')
                with self.assertRaisesRegex(ValueError,'Local export contract changed'):
                    runner.lua_specs(root,'Child')
                local.unlink()
                with self.assertRaisesRegex(ValueError,'Local export contract missing'):
                    runner.lua_specs(root,'Child')

    def test_other_children_keep_every_spec_including_stats(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); (root/'tests').mkdir()
            for name in ('ordinary_spec.lua','export_contract_spec.lua','test_era.lua'):
                (root/'tests'/name).write_text('-- test')
            specs,local_only=runner.lua_specs(root,'ApogeeStats')
            self.assertEqual({p.name for p in specs},{'ordinary_spec.lua','export_contract_spec.lua','test_era.lua'})
            self.assertEqual(local_only,[])

if __name__=='__main__': unittest.main(verbosity=2)
