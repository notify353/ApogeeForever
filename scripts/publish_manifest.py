"""Manifest-based publication, using the existing guarded Actions transport."""
import json
import os
from pathlib import Path
import tempfile
import urllib.request
from urllib.parse import urlsplit
import uuid

import distribution as d
import release_manifest as r
import curseforge_preflight as cf


def selection(receipt):
    manifest, lock, notes = r.load(receipt['version'])
    target = manifest['target']
    d.require(receipt.get('schema') == 2 and receipt.get('projectId') == 1608100
              and receipt.get('target') == target
              and receipt.get('filename') == r.TARGETS[target]['filename']+'-'+receipt['version']+'.zip'
              and receipt.get('sha256') == manifest['packages']['PROD']
              and receipt.get('manifestSha256') == d.sha(d.canonical(manifest)), 'Release receipt/selection mismatch')
    return manifest, notes


def upload(sources, output):
    import publish_distribution as p
    output = Path(output); receipt_path = output/'receipt.json'
    receipt = json.loads(receipt_path.read_bytes()); version = receipt['version']
    p.actions_guard(version)
    manifest, notes = selection(receipt)
    d.require(receipt['publicationState'] == 'staged', 'Prior publication attempt exists; inspect services before recovery')
    _, packages, _ = r.packages(version, sources)
    archive = (output/receipt['filename']).read_bytes()
    d.require(archive == packages['PROD'], 'Staged package changed')
    d.require((output/'release-notes.md').read_text(encoding='utf-8') == notes, 'Staged notes changed')
    token = os.environ.get('CF_API_KEY'); d.require(token, 'CurseForge credential unavailable')
    opener = urllib.request.build_opener(cf.NoRedirect)
    request = urllib.request.Request(cf.URL, headers={'X-Api-Token':token,'Accept':'application/json'})
    with opener.open(request,timeout=30) as response:
        row = cf.select_version(json.load(response), manifest['target'])
    meta = {'displayName':r.TARGETS[manifest['target']]['label']+' '+version,
            'releaseType':'release','gameVersions':[row['id']],'changelogType':'markdown','changelog':notes}
    # Journal before the first remote write, including uncertain GitHub outcomes.
    receipt.update(publicationState='github-publication-attempted',uploadVersion=row)
    receipt_path.write_bytes(d.canonical(receipt))
    p.gh('release','create','v'+version,'--verify-tag','--draft','--title',meta['displayName'],
         '--notes-file',str(output/'release-notes.md'))
    p.gh('release','upload','v'+version,str(output/receipt['filename']),str(output/(receipt['filename']+'.sha256')))
    with tempfile.TemporaryDirectory() as folder:
        p.gh('release','download','v'+version,'--pattern',receipt['filename'],'--dir',folder)
        d.require(d.sha((Path(folder)/receipt['filename']).read_bytes())==receipt['sha256'],'GitHub package checksum differs')
    p.gh('release','edit','v'+version,'--draft=false')
    receipt.update(githubPublished=True,publicationState='curseforge-upload-attempted')
    receipt_path.write_bytes(d.canonical(receipt))
    boundary='apogee-'+uuid.uuid4().hex
    request=urllib.request.Request('https://wow.curseforge.com/api/projects/1608100/upload-file',
        data=p.multipart(meta,receipt['filename'],archive,boundary),method='POST',
        headers={'X-Api-Token':token,'Content-Type':'multipart/form-data; boundary='+boundary})
    with opener.open(request,timeout=120) as response: result=json.load(response)
    file_id=result.get('id')
    d.require(type(file_id) is int and file_id>0,'Uncertain upload response; investigate before retrying')
    receipt.update(publicationState='awaiting-public-byte-verification',curseforgeFileId=file_id)
    receipt_path.write_bytes(d.canonical(receipt))
    return receipt


def verify(output, download_url):
    import publish_distribution as p
    output=Path(output); receipt_path=output/'receipt.json'
    receipt=json.loads(receipt_path.read_bytes()); p.actions_guard(receipt['version'])
    selection(receipt)
    d.require(receipt['publicationState']=='awaiting-public-byte-verification','Confirmed upload receipt required')
    url=urlsplit(download_url); parts=url.path.split('/')
    d.require(url.scheme=='https' and url.hostname in ('edge.forgecdn.net','mediafilez.forgecdn.net')
              and not url.username and not url.password and not url.query and not url.fragment
              and len(parts)==5 and parts[1]=='files' and parts[-1]==receipt['filename']
              and parts[2].isdigit() and parts[3].isdigit()
              and int(parts[2])*1000+int(parts[3])==receipt['curseforgeFileId'],'Use the exact approved file download link')
    with urllib.request.build_opener(cf.NoRedirect).open(download_url,timeout=60) as response:
        body=response.read(16*1024*1024)
    d.require(d.sha(body)==receipt['sha256'],'CurseForge package checksum differs')
    with tempfile.TemporaryDirectory() as folder:
        p.gh('release','download','v'+receipt['version'],'--pattern',receipt['filename'],'--dir',folder)
        d.require(d.sha((Path(folder)/receipt['filename']).read_bytes())==receipt['sha256'],'GitHub package checksum differs')
    receipt.update(publicationState='published-and-byte-verified',curseforgeDownloadUrl=download_url)
    receipt_path.write_bytes(d.canonical(receipt))
    return receipt
