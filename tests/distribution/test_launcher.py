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
                master=d.MARKER+('Dev' if family=='DEV' else '')
                env=os.environ.copy(); env.update(APOGEE_UI_ROOT=str(Path(folder)/master/'SharedUI'),APOGEE_UI_NAME=name,APOGEE_UI_ADDON=master,APOGEE_COMPONENTS_ROOT=folder)
                subprocess.run(['lua','tests/launcher_spec.lua'],cwd=CHILDREN/'ApogeeEssentials',env=env,check=True)
                essentials='ApogeeEssentials'+('Dev' if family=='DEV' else '')
                env.update(APOGEE_ESSENTIALS_RUNTIME_ROOT=str(Path(folder)/essentials),
                           APOGEE_ESSENTIALS_RUNTIME_NAME=essentials, APOGEE_ESSENTIALS_TEST_ERA='1' if target=='era' else '0')
                subprocess.run(['lua','tests/startup_refresh_spec.lua'],cwd=CHILDREN/'ApogeeEssentials',env=env,check=True)
                for component in ('ApogeeHeals','ApogeeKeybinds'):
                    subprocess.run(['lua',str(ROOT/'tests/distribution/position_reset.lua'),folder,family,target,component],
                                   cwd=CHILDREN/component,env=env,check=True)
                subprocess.run(['lua',str(ROOT/'tests/distribution/launcher_gate.lua'),folder,family,target,
                                str(CHILDREN/'ApogeeEssentials/tests/launcher_mock.lua')],check=True)
                heals='ApogeeHeals'+('Dev' if family=='DEV' else '')
                env.update(APOGEE_HEALS_RUNTIME_ROOT=str(Path(folder)/heals),
                           APOGEE_HEALS_RUNTIME_NAME=heals, APOGEE_HEALS_TEST_ERA='1' if target=='era' else '0')
                subprocess.run(['lua','tests/healing_defaults_spec.lua'],cwd=CHILDREN/'ApogeeHeals',env=env,check=True)
                subprocess.run(['lua','tests/startup_failure_spec.lua'],cwd=CHILDREN/'ApogeeHeals',env=env,check=True)
                keybinds='ApogeeKeybinds'+('Dev' if family=='DEV' else '')
                env.update(APOGEE_KEYBINDS_RUNTIME_ROOT=str(Path(folder)/keybinds),
                           APOGEE_KEYBINDS_RUNTIME_NAME=keybinds, APOGEE_KEYBINDS_TEST_SIMULATED='1',
                           APOGEE_KEYBINDS_TEST_ERA='1' if target=='era' else '0')
                subprocess.run(['lua','tests/startup_failure_spec.lua'],cwd=CHILDREN/'ApogeeKeybinds',env=env,check=True)
                if target=='forever-offline':
                    keybinds='ApogeeKeybinds'+('Dev' if family=='DEV' else '')
                    env.update(APOGEE_KEYBINDS_RUNTIME_ROOT=str(Path(folder)/keybinds),
                               APOGEE_KEYBINDS_RUNTIME_NAME=keybinds, APOGEE_KEYBINDS_TEST_SIMULATED='1')
                    subprocess.run(['lua','tests/explosives_spec.lua'],cwd=CHILDREN/'ApogeeKeybinds',env=env,check=True)
                    stats='ApogeeStats'+('Dev' if family=='DEV' else '')
                    subprocess.run(['lua','tests/test_tooltip.lua',str(Path(folder)/stats),stats],cwd=CHILDREN/'ApogeeStats',check=True)
                for child in self.era['children'] if target=='era' else self.future['children']:
                    n=child['name']+('Dev' if family=='DEV' else '')
                    meta,runtime=d.toc_info(files[n+'/'+n+'.toc'])
                    self.assertEqual(meta['Dependencies'],master)
                    self.assertEqual(meta['X-Apogee-UI-API'],'1')
                    for old in ('ApogeeHealsMinimapButton','ApogeeKeybindsMinimapButton'):
                        self.assertFalse(any(old.encode() in files[n+'/'+p] for p in runtime))
                meta,_=d.toc_info(files[master+'/'+master+'.toc'])
                self.assertEqual(meta['SavedVariablesPerCharacter'],name+'DB')

    def test_support_source_api_and_dependencies_fail_closed(self):
        for field,value in [('commit','0'*40),('sourceChild','ApogeeHeals'),('subdirectory','../outside'),('apiVersion',2),('placement','hidden')]:
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

    def test_generated_settings_with_real_shared_owner(self):
        for target in ('era','forever-offline'):
            with self.subTest(target=target),tempfile.TemporaryDirectory() as folder:
                if target=='era':
                    m.put(Path(folder)/'DEV',self.payload)
                else:
                    for family in ('PROD','DEV'):
                        m.put(Path(folder)/family,dual.family_files(self.future,SOURCES,family)[0])
                command=['lua',str(ROOT/'tests/distribution/shared_settings.lua'),folder,'launcher']
                if target=='era': command.append('DEV')
                subprocess.run(command,check=True)
                if target=='forever-offline':
                    subprocess.run(['lua',str(ROOT/'tests/distribution/master_selection.lua'),folder],check=True)

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
            self.assertTrue(any(p.endswith('.toc') for p in preview['writes']))
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

    def test_standalone_upgrade_and_rollback_both_targets(self):
        for target, lock in [('era',self.era), ('forever',self.future)]:
            old=copy.deepcopy(lock); old['supportModules'][0].pop('placement')
            build=lambda selected: era.family_files(selected,SOURCES)[0] if target=='era' else dual.family_files(selected,SOURCES,'DEV')[0]
            payload, prior=build(lock),build(old)
            self.assertIn('ApogeeUIDev/ApogeeUIDev.toc',prior)
            self.assertFalse(any(p.startswith('ApogeeUIDev/') for p in payload))
            with self.subTest(target=target), tempfile.TemporaryDirectory() as folder:
                root=Path(folder); client=root/('_classic_era_' if target=='era' else 'client')
                m.put(client/'Interface/AddOns',prior)
                # Harmless unrecognized files must survive migration and rollback.
                note='ApogeeUIDev/my-notes.txt'
                m.put(client/'Interface/AddOns',{note:b'owner note'})
                receipt={'schema':1,'status':'installed','target':'classic-era','family':'DEV',
                         'client':str(client),'names':list({p.split('/')[0] for p in prior}), 'after':m.hashes(prior)}
                if target=='era':
                    desired,known,preview,_=era.prepare(client,payload,receipt)
                    names=era.NAMES
                    with self.assertRaises(ValueError): era.verify_live_update(payload,preview,receipt)
                else:
                    desired,known,names,preview,_=installer.prepare(client,payload,{'schema':1,'files':{},'legacyTocHashes':[]},previous=receipt)
                    self.assertTrue(installer.activation(preview)['restartRequired'])
                retired=preview['retired']
                self.assertEqual(set(retired),{p for p in prior if p.startswith('ApogeeUIDev/') and p.endswith(('.lua','.toc'))})
                result=m.apply(client,desired,known,root/'backup',preview,names,atomic_files=True,retired=retired)
                self.assertEqual(result['status'],'installed')
                self.assertTrue(all(not (client/'Interface/AddOns'/p).exists() for p in retired))
                self.assertEqual(m.tree(root/'backup/retired-files'),{p:prior[p] for p in retired})
                self.assertEqual((client/'Interface/AddOns'/note).read_bytes(),b'owner note')
                # Subsequent updates no longer see a stale runtime or addon entry.
                result.update(target='classic-era',family='DEV')
                if target=='era':
                    _,_,next_preview,_=era.prepare(client,payload,result)
                    era.verify_live_update(payload,next_preview,result)
                    self.assertFalse(next_preview['retired'])
                self.assertEqual(m.rollback(root/'backup')['status'],'rolled-back')
                self.assertEqual(m.managed(client/'Interface/AddOns',names),dict(prior,**{note:b'owner note'}))
                # Modified or unreceipted runtime cannot be retired.
                p='ApogeeUIDev/Client.lua'; (client/'Interface/AddOns'/p).write_bytes(b'owner edit')
                with self.assertRaises(ValueError):
                    support.retire_support(payload,m.managed(client/'Interface/AddOns',names),receipt)

    def test_frozen_forever_archives_byte_identical(self):
        lock=d.read_lock(ROOT/'distribution/candidate.lock.json')
        expected={'PROD':'34a6f788db78068effa231576bd03eb674daaf2db9d486fdce6502b72b7f8a2c',
                  'DEV':'1d78e89a95d563fc2d41e7394745fff3b4333a3dbf5caa0644096f048a243234'}
        for family,digest in expected.items():
            files,_=dual.family_files(lock,SOURCES,family)
            self.assertEqual(d.sha(d.zip_bytes(files)),digest)

    def test_historical_era10_archive_byte_identical(self):
        lock=json.loads(subprocess.check_output(['git','show',
            'e62a0d785a8d9a1150923a80116a9586557ce916:distribution/era/candidate.lock.json'],cwd=ROOT))
        files,_=era.family_files(lock,SOURCES)
        self.assertEqual(d.sha(d.zip_bytes(files)),
            '2eec2a6b43fdd774020ea16e32e8eccb4c6e070722b975919453720bf9b858dc')

if __name__=='__main__': unittest.main()
