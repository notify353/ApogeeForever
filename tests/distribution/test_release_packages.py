"""Generated public Era contracts and unchanged candidate gameplay."""
import os
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import distribution as d
import dual_distribution as dual
import era_distribution as era
import release_manifest as r

SOURCES=Path(os.environ.get('APOGEE_SOURCES_ROOT','C:/Dev/WoW'))

class PackageTests(unittest.TestCase):
    def test_era_dev_unchanged_and_prod_source_bodies_exact(self):
        if os.environ.get('APOGEE_TEST_TARGET')=='forever': self.skipTest('Separate Era release')
        lock=era.read_lock();dev=era.family_files(lock,SOURCES)[0];prod=era.family_files(lock,SOURCES,'PROD')[0]
        self.assertEqual(d.sha(d.zip_bytes(dev)),'77a04ee84a7e6fd1ca9c5fed339ab1240ab67bb8a2bc145eefad64cd0c6f2c17')
        self.assertEqual({p.split('/')[0] for p in prod},{d.MARKER,*d.ACTIVE_CHILDREN})
        for child in lock['children']:
            name=child['name'];meta,runtime=d.toc_info(prod[name+'/'+name+'.toc'])
            self.assertEqual(meta['Interface'],'11509');self.assertEqual(meta['X-Apogee-Family'],'PROD')
            self.assertEqual(meta['Dependencies'],d.MARKER)
            source=d.source_tree(SOURCES/name,child['commit'])
            for p in runtime[1:]:self.assertEqual(prod[name+'/'+p],dual.prefix(name,'PROD')+source[p])
            for key,value in meta.items():
                if key.startswith('SavedVariables'):self.assertNotIn('Dev',value)
        meta,runtime=d.toc_info(prod[d.MARKER+'/'+d.MARKER+'.toc'])
        self.assertEqual(meta['SavedVariablesPerCharacter'],'ApogeeUIDB')
        self.assertEqual(meta['X-Curse-Project-ID'],'1608100')
        self.assertFalse(any(p.endswith('.toc') and '_Era' in p for p in prod))

    def test_each_prepared_manifest_reproduces_exact_packages(self):
        for path in sorted(r.ROOT.glob('*/manifest.json')):
            version=path.parent.name
            selected=os.environ.get('APOGEE_RELEASE_VERSION')
            if selected and version!=selected: continue
            with self.subTest(version=version):
                manifest,packages,_=r.packages(version,SOURCES)
                self.assertEqual(set(packages),{'PROD','DEV'})
                self.assertFalse(manifest['authorization']['nativeAccepted'])

if __name__=='__main__':unittest.main(verbosity=2)
