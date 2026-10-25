"""Pinned UI support module, owned by Essentials; no UI behavior lives here."""
from pathlib import Path
import distribution as d

def descriptor(lock):
    return d.support_descriptor(lock)


def source(lock, sources_root):
    module = descriptor(lock)
    if not module: return None, {}
    tree = d.source_tree(Path(sources_root) / module['sourceChild'], module['commit'])
    files = {}
    for path, digest in module['files'].items():
        d.safe_path(path)
        full = module['subdirectory'] + '/' + path
        d.require(full in tree and d.sha(tree[full]) == digest, 'Support pinned file mismatch: ' + path)
        files[path] = tree[full]
    meta, runtime = d.toc_info(files[module['toc']])
    d.require(meta.get('Interface') == ('11509' if lock.get('target') == 'classic-era' else '16001'), 'Support client mismatch')
    d.require(meta.get('X-Apogee-UI-API') == '1' and meta.get('SavedVariablesPerCharacter') == 'ApogeeUIDB', 'Support identity drift')
    d.require(not any(k in meta for k in ('Dependencies','RequiredDeps','OptionalDeps','LoadWith')), 'Support cannot depend on gameplay')
    d.require(runtime == ['Client.lua','Settings.lua','ApogeeUI.lua'], 'Unreviewed support load order')
    d.require({p for p in files if p.endswith(('.lua','.xml'))} == set(runtime), 'Unlisted support runtime')
    d.require({p for p in files if p.endswith('.toc')} == {module['toc']}, 'Alternate support TOC')
    d.require('LICENSE' in files and 'Media/Textures/ApogeeLogo.png' in files, 'Missing support assets')
    return module,files

def gate_bytes(lock, base):
    if not descriptor(lock): return base
    old = b'"ApogeeAuction", "ApogeeStats"}'
    d.require(base.count(old) == 1, 'Unexpected gate member list')
    return base.replace(old,b'"ApogeeAuction", "ApogeeStats", "ApogeeUI"}')

def add_files(lock, sources_root, family, output, changes, gate, dual):
    module, files = source(lock,sources_root)
    if not module: return
    old='ApogeeUI'; name=old+('Dev' if family=='DEV' else '')
    meta,runtime=d.toc_info(files[module['toc']])
    meta.update({'Title':'Apogee UI'+(' DEV' if family=='DEV' else '')+' (shared support)',
                 'Version':lock['version'],'Group':d.MARKER+('Dev' if family=='DEV' else ''),
                 'X-Apogee-Family':family,'X-Apogee-Family-Schema':'1'})
    if lock.get('target') == 'classic-era': meta['X-Apogee-Client']='classic-era'
    if family=='DEV':
        meta['SavedVariablesPerCharacter']='ApogeeUIDevDB'
        meta['IconTexture']=meta['IconTexture'].replace('ApogeeUI/','ApogeeUIDev/')
    renamed={p:name+'.lua' if p==old+'.lua' else p for p in runtime}
    output[name+'/'+name+'.toc']=(''.join('## '+k+': '+v+'\n' for k,v in meta.items())+'\n'+dual.GATE_PATH+'\n'+''.join(renamed[p]+'\n' for p in runtime)).encode()
    output[name+'/'+dual.GATE_PATH]=gate.replace(b'@NAME@',name.encode()).replace(b'@FAMILY@',family.encode())
    for path,data in files.items():
        if path==module['toc']: continue
        target=name+'/'+renamed.get(path,path)
        if path in runtime:
            body,audit=dual.transform_lua(data,old) if family=='DEV' else (data,[])
            output[target]=dual.prefix(name,family)+body
            changes[target]={'source':'ApogeeEssentials/'+module['subdirectory']+'/'+path,'sourceSha256':d.sha(data),'identityEdits':audit}
        else: output[target]=data
