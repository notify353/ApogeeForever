"""No credentials, network, child clones or installed clients required."""
import copy
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import distribution as d
import era_distribution as era
import release_manifest as r
import publish_manifest as pub
import publish_distribution as legacy
import curseforge_preflight as cf


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.addCleanup(patch.stopall)
        patch.object(r,'ROOT',self.root/'releases').start()
        self.version='1.14.10'
        self.fixture('classic-era')

    def generated(self,target,lock,sources,version,family):
        suffix='Dev' if family=='DEV' else ''
        return {n+suffix+'/'+n+suffix+'.toc':('## Interface: '+r.TARGETS[target]['interface']+'\n## X-Apogee-Family: '+family+'\n').encode()
                for n in (d.MARKER,*d.ACTIVE_CHILDREN)}

    def fixture(self,target):
        folder=r.path(self.version).parent; folder.mkdir(parents=True,exist_ok=True)
        lock=era.read_lock() if target=='classic-era' else d.read_lock(d.ROOT/'distribution/future-launcher.lock.json')
        ep=era.CONFIG/'api-evidence.json' if target=='classic-era' else d.ROOT/'distribution/forever/api-evidence.json'
        evidence=json.loads(ep.read_bytes())
        self.manifest={'schema':1,'target':target,'version':self.version,'projectId':1608100,'releaseType':'release',
            'sourceLockSha256':d.sha(d.canonical(lock)),'apiEvidenceSha256':d.sha(d.canonical(evidence)),
            'notesSha256':d.sha(b'Player notes\n'),'curseforge':{k:r.TARGETS[target][k] for k in ('name','gameVersionTypeID')},
            'authorization':{'kind':'owner-approved-early-release','nativeAccepted':False,'basis':'Owner requests early release; full native acceptance pending.'},
            'packages':{f:d.sha(d.zip_bytes(self.generated(target,lock,None,self.version,f))) for f in ('PROD','DEV')}}
        (folder/'source.lock.json').write_bytes(d.canonical(lock));(folder/'api-evidence.json').write_bytes(d.canonical(evidence))
        (folder/'release-notes.md').write_bytes(b'Player notes\n'); self.save()

    def save(self): r.path(self.version).write_bytes(d.canonical(self.manifest))

    def stage(self):
        with patch.object(r,'files',side_effect=self.generated): return r.stage(self.version,None,self.root/'stage')

    def test_both_targets_and_exact_version_selection(self):
        rows=[{'id':101,'name':'1.15.9','gameVersionTypeID':67408},{'id':102,'name':'1.60.1','gameVersionTypeID':88568}]
        for target in r.TARGETS:
            self.fixture(target)
            self.assertEqual(r.load(self.version)[0]['target'],target)
            self.assertEqual(cf.select_version(rows,target)['name'],r.TARGETS[target]['name'])
            with self.assertRaises(ValueError): cf.select_version(rows+rows,target)
            wrong=[dict(x,gameVersionTypeID=1) for x in rows]
            with self.assertRaises(ValueError): cf.select_version(wrong,target)

    def test_no_duplicate_version_or_invalid_target(self):
        with self.assertRaisesRegex(ValueError,'already prepared'): r.prepare('classic-era',self.version,None,None,None,'basis')
        for version in ('../1.0.0','v1.0.0','1.0.0-era.1'):
            with self.assertRaises(ValueError): r.path(version)
        with self.assertRaises(ValueError): cf.select_version([], 'retail')

    def test_tampered_selection_authority_notes_and_authorization(self):
        original=copy.deepcopy(self.manifest)
        for key,value in [('target','forever'),('releaseType','beta'),('sourceLockSha256','0'*64),
                          ('apiEvidenceSha256','0'*64),('notesSha256','0'*64),
                          ('authorization',{'kind':'skip','nativeAccepted':True}),('curseforge',{})]:
            self.manifest=copy.deepcopy(original);self.manifest[key]=value;self.save()
            with self.subTest(key=key),self.assertRaises((ValueError,KeyError)):r.load(self.version)

    def test_wrong_package_hash_or_family_rejected(self):
        with patch.object(r,'files',side_effect=self.generated):
            self.assertEqual(set(r.packages(self.version,None)[1]),{'PROD','DEV'})
            self.manifest['packages']['PROD']='0'*64;self.save()
            with self.assertRaisesRegex(ValueError,'approved bytes'):r.packages(self.version,None)
        self.fixture('classic-era')
        with patch.object(r,'files',return_value={'ApogeeHealsDev/a.lua':b''}),self.assertRaisesRegex(ValueError,'roots'):
            r.packages(self.version,None)

    def test_cross_client_receipt_and_wrong_download_rejected(self):
        receipt=self.stage()
        for key,value in [('target','forever'),('filename','ApogeeForever-1.14.10.zip'),('sha256','0'*64),('manifestSha256','0'*64)]:
            bad=dict(receipt,**{key:value})
            with self.subTest(key=key),self.assertRaises(ValueError):pub.selection(bad)
        receipt.update(publicationState='awaiting-public-byte-verification',curseforgeFileId=1234005)
        (self.root/'stage/receipt.json').write_bytes(d.canonical(receipt))
        with patch.object(legacy,'actions_guard'),patch.object(pub.urllib.request,'build_opener') as network:
            with self.assertRaises(ValueError):pub.verify(self.root/'stage','https://example.com/file.zip')
            network.assert_not_called()

    def test_partial_remote_outcomes_are_journaled_and_never_retried(self):
        for failure in ('github','wrong-asset','curseforge'):
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as tmp:
                stage=Path(tmp)/'stage'
                with patch.object(r,'files',side_effect=self.generated):r.stage(self.version,None,stage)
                receipt=json.loads((stage/'receipt.json').read_bytes()); archive=(stage/receipt['filename']).read_bytes(); calls=[]
                def gh(*args):
                    calls.append(args[:2])
                    if failure=='github':raise TimeoutError('uncertain GitHub operation')
                    if args[:2]==('release','download'):
                        (Path(args[args.index('--dir')+1])/receipt['filename']).write_bytes(b'wrong' if failure=='wrong-asset' else archive)
                class Opener:
                    def open(self,request,timeout):
                        calls.append(request.get_method())
                        if request.get_method()=='POST':raise TimeoutError('uncertain CurseForge operation')
                        return io.BytesIO(json.dumps([{'id':101,'name':'1.15.9','gameVersionTypeID':67408}]).encode())
                with patch.object(legacy,'actions_guard'),patch.object(legacy,'gh',side_effect=gh),\
                     patch.object(pub.urllib.request,'build_opener',return_value=Opener()),\
                     patch.object(r,'files',side_effect=self.generated),patch.dict(os.environ,{'CF_API_KEY':'test-placeholder'}):
                    with self.assertRaises((TimeoutError,ValueError)):pub.upload(None,stage)
                    count=len(calls)
                    with self.assertRaises(ValueError):pub.upload(None,stage)
                    self.assertEqual(len(calls),count)
                state=json.loads((stage/'receipt.json').read_bytes())['publicationState']
                self.assertEqual(state,'curseforge-upload-attempted' if failure=='curseforge' else 'github-publication-attempted')
                if failure!='curseforge':self.assertNotIn('POST',calls)

    def test_successful_upload_and_public_byte_verification(self):
        receipt=self.stage();stage=self.root/'stage'
        archive=(stage/receipt['filename']).read_bytes(); requests=[]
        def gh(*args):
            if args[:2]==('release','download'):
                (Path(args[args.index('--dir')+1])/receipt['filename']).write_bytes(archive)
        class Opener:
            def open(self,request,timeout):
                if isinstance(request,str): return io.BytesIO(archive)
                requests.append(request)
                return io.BytesIO(json.dumps({'id':1234005} if request.get_method()=='POST' else
                    [{'id':101,'name':'1.15.9','gameVersionTypeID':67408}]).encode())
        with patch.object(legacy,'actions_guard'),patch.object(legacy,'gh',side_effect=gh),\
             patch.object(pub.urllib.request,'build_opener',return_value=Opener()),\
             patch.object(r,'files',side_effect=self.generated),patch.dict(os.environ,{'CF_API_KEY':'test-placeholder'}):
            result=pub.upload(None,stage)
            self.assertEqual(result['publicationState'],'awaiting-public-byte-verification')
            self.assertEqual(result['uploadVersion']['id'],101)
            result=pub.verify(stage,'https://edge.forgecdn.net/files/1234/5/'+receipt['filename'])
            self.assertEqual(result['publicationState'],'published-and-byte-verified')
        self.assertEqual([q.get_method() for q in requests],['GET','POST'])
        self.assertIn(b'"gameVersions": [101]',requests[-1].data)
        self.assertNotIn(b'88568',requests[-1].data)

    def test_changed_staged_bytes_and_local_upload_stop_before_network(self):
        receipt=self.stage();stage=self.root/'stage'
        with patch.dict(os.environ,{},clear=True),patch.object(pub.urllib.request,'build_opener') as network:
            with self.assertRaises(ValueError):pub.upload(None,stage)
            network.assert_not_called()
        (stage/receipt['filename']).write_bytes(b'wrong client archive')
        with patch.object(legacy,'actions_guard'),patch.object(r,'files',side_effect=self.generated),\
             patch.object(pub.urllib.request,'build_opener') as network:
            with self.assertRaisesRegex(ValueError,'Staged package changed'):pub.upload(None,stage)
            network.assert_not_called()


if __name__=='__main__':unittest.main(verbosity=2)
