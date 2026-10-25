"""Generated launcher contract, source pins, family isolation and Era upgrade safety."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import distribution as d
import dual_distribution as dual
import era_distribution as era
import migrate_distribution as m
import support_distribution as support
import install_dual_distribution as installer
import publish_distribution as publisher

SOURCES=Path(os.environ.get('APOGEE_SOURCES_ROOT','C:/Dev/WoW'))
CHILDREN=Path(os.environ.get('APOGEE_CHILD_WORKTREES',str(ROOT.parent)))
class LauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.era=era.read_lock()
        cls.future=d.read_lock(ROOT/'distribution/future-launcher.lock.json')
        cls.payload=era.family_files(cls.era,SOURCES)[0]

    def test_generated_behavior_all_targets(self):
        for target,family,files in [('era','DEV',self.payload)]+[
            ('forever-offline',family,dual.family_files(self.future,SOURCES,family)[0]) for family in ('PROD','DEV')]:
            with self.subTest(target=target,family=family),tempfile.TemporaryDirectory() as folder:
                m.put(folder,files)
                name='ApogeeUI'+('Dev' if family=='DEV' else '')
                env=os.environ.copy(); env.update(APOGEE_UI_ROOT=str(Path(folder)/name),APOGEE_UI_NAME=name,APOGEE_COMPONENTS_ROOT=folder)
                subprocess.run(['lua','tests/launcher_spec.lua'],cwd=CHILDREN/'ApogeeEssentials',env=env,check=True)
                if target=='forever-offline':
                    stats='ApogeeStats'+('Dev' if family=='DEV' else '')
                    subprocess.run(['lua','tests/test_tooltip.lua',str(Path(folder)/stats),stats],cwd=CHILDREN/'ApogeeStats',check=True)
                for child in self.era['children'] if target=='era' else self.future['children']:
                    n=child['name']+('Dev' if family=='DEV' else '')
                    meta,runtime=d.toc_info(files[n+'/'+n+'.toc'])
                    self.assertEqual(meta['Dependencies'],name)
                    self.assertEqual(meta['X-Apogee-UI-API'],'1')
                    for old in ('ApogeeHealsMinimapButton','ApogeeKeybindsMinimapButton'):
                        self.assertFalse(any(old.encode() in files[n+'/'+p] for p in runtime))
                meta,_=d.toc_info(files[name+'/'+name+'.toc'])
                self.assertEqual(meta['SavedVariablesPerCharacter'],name+'DB')

    def test_support_source_api_and_dependencies_fail_closed(self):
        for field,value in [('commit','0'*40),('sourceChild','ApogeeHeals'),('subdirectory','../outside'),('apiVersion',2)]:
            lock=copy.deepcopy(self.era); lock['supportModules'][0][field]=value
            with self.assertRaises(ValueError): era.family_files(lock,SOURCES)
        for mutate in ('missing','mixed','corrupt'):
            lock=copy.deepcopy(self.era)
            if mutate=='missing': lock.pop('supportModules')
            elif mutate=='mixed': lock['children'][0]['uiApi']=2
            else: lock['supportModules'][0]['files']['Client.lua']='0'*64
            with self.assertRaises(ValueError): era.family_files(lock,SOURCES)
        child=copy.deepcopy(self.future['children'][0]); tree=d.source_tree(SOURCES/child['name'],child['commit'])
        files={p:tree[p] for p in child['files']}
        files[child['toc']]=files[child['toc']].replace(b'Dependencies: ApogeeUI',b'Dependencies: ApogeeUIDev')
        with self.assertRaises(ValueError): d.child_contract(child,files)

    def test_upgrade_from_era7_receipt_requires_closed_install(self):
        with tempfile.TemporaryDirectory() as folder:
            client=Path(folder)/'_classic_era_'; client.mkdir()
            # Model the exact legacy root/TOC shape with receipt-verified bytes.
            # Historical frozen packages are tested independently below.
            previous_files={p:body for p,body in self.payload.items() if not p.startswith('ApogeeUIDev/')}
            for path,body in list(previous_files.items()):
                if path.endswith('.toc'):
                    previous_files[path]=b'\n'.join(line for line in body.split(b'\n')
                        if not line.startswith((b'## Dependencies:',b'## X-Apogee-UI-API:')))
            m.put(client/'Interface/AddOns',previous_files)
            receipt={'schema':1,'status':'installed','target':'classic-era','family':'DEV','client':str(client),
                     'names':era.LEGACY_NAMES,'after':m.hashes(previous_files)}
            desired,known,preview,docs=era.prepare(client,self.payload,receipt)
            self.assertTrue(any(p.startswith('ApogeeUIDev/') for p in preview['writes']))
            with self.assertRaises(ValueError): era.verify_live_update(self.payload,preview,receipt)
            # No live writes occurred in preflight, and rollback remains available.
            self.assertEqual(m.hashes(m.managed(client/'Interface/AddOns',era.LEGACY_NAMES)),receipt['after'])

    def test_future_installer_and_publisher_support_inventory(self):
        # Filesystem and acceptance fixtures only: never touches a live installation.
        payload=dual.family_files(self.future,SOURCES,'DEV')[0]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); client=root/'client'; (client/'Interface/AddOns').mkdir(parents=True)
            known={'schema':1,'files':{},'legacyTocHashes':[]}
            result=installer.install(client,payload,known,root/'backup')
            self.assertEqual(result['status'],'installed')
            self.assertTrue(result['activation']['restartRequired'])
            self.assertEqual(m.rollback(root/'backup')['status'],'rolled-back')
            version='1.14.99'
            accepted={'accepted':True,'runtimeFiles':{}}
            for family in ('PROD','DEV'):
                lock=copy.deepcopy(self.future); lock['version']=version
                files=dual.family_files(lock,SOURCES,family)[0]
                accepted['runtimeFiles'][family]={p:d.sha(b) for p,b in files.items() if p.endswith('.lua')}
            acceptance=root/'acceptance.json'; acceptance.write_text(json.dumps(accepted))
            with patch.object(dual,'LOCK',ROOT/'distribution/future-launcher.lock.json'),patch.object(publisher,'ACCEPTANCE',acceptance):
                archive=publisher.payload(SOURCES,version)
                self.assertTrue(archive)

    def test_frozen_forever_archives_byte_identical(self):
        lock=d.read_lock(ROOT/'distribution/candidate.lock.json')
        expected={'PROD':'34a6f788db78068effa231576bd03eb674daaf2db9d486fdce6502b72b7f8a2c',
                  'DEV':'1d78e89a95d563fc2d41e7394745fff3b4333a3dbf5caa0644096f048a243234'}
        for family,digest in expected.items():
            files,_=dual.family_files(lock,SOURCES,family)
            self.assertEqual(d.sha(d.zip_bytes(files)),digest)

if __name__=='__main__': unittest.main()
