-- Read actual generated metadata and exercise admission before any gameplay.
local root,family,target=assert(arg[1]),assert(arg[2]),assert(arg[3])
local suffix=family=='DEV' and 'Dev' or ''
local support='ApogeePartyHealthBars'..suffix
local serviceName='ApogeeUI'..suffix
local bases={'ApogeePartyHealthBars','ApogeeHeals','ApogeeKeybinds','ApogeeGroupAlert','ApogeeEssentials'}
bases[#bases+1]='ApogeeStats'
local scenarios=0
local originalPrint=print
for _,base in ipairs(bases) do
    local name=base..suffix
    for _,scenario in ipairs({'allowed','api','version','family','missing','dependency',
        'runtime-missing','runtime-api','runtime-not-ready','runtime-incomplete','disabled','master-metadata','not-loaded','child-contract','metadata-error','runtime-legacy','runtime-failed','client-version'}) do
        if base~='ApogeePartyHealthBars' or not scenario:match('^runtime') and scenario~='dependency' and scenario~='not-loaded' and scenario~='child-contract' then
            local metadata,paths={},{}
            for _,b in ipairs(bases) do
                local n=b..suffix; metadata[n]={}; paths[n]={}
                for line in io.lines(root..'/'..n..'/'..n..'.toc') do
                    local k,v=line:match('^## ([^:]+):%s*(.-)%s*$')
                    if k then metadata[n][k]=v
                    elseif line:match('%.lua$') then paths[n][#paths[n]+1]=line end
                end
            end
            if scenario=='master-metadata' then metadata[support]['X-Apogee-Master']=nil end
            if scenario=='api' then metadata[support]['X-Apogee-UI-API']='2' end
            if scenario=='version' then
                if name==support then metadata[support].Version=nil
                else metadata[support].Version='different-package' end
            end
            if scenario=='family' then metadata[support]['X-Apogee-Family']='OTHER' end
            if scenario=='missing' then metadata[support]=nil end
            if scenario=='dependency' then metadata[name].Dependencies='ApogeeUIOtherFamily' end
            if scenario=='child-contract' then metadata[name]['X-Apogee-Requires-Master']=nil end
            local service={apiVersion=1,ready=true}
            for _,method in ipairs({'RegisterComponent','RefreshComponent','UnregisterComponent','RegisterSettings','EnsureSettingsParent'}) do
                service[method]=function() end
            end
            if scenario=='runtime-api' then service.apiVersion=2 end
            if scenario=='runtime-legacy' then service.apiVersion=nil; service.ready=nil end
            if scenario=='runtime-failed' then service.failed=true end
            if scenario=='runtime-not-ready' then service.ready=false end
            if scenario=='runtime-incomplete' then service.RegisterComponent=nil end
            _G[serviceName]=scenario~='runtime-missing' and service or nil
            ApogeeDistributionFamilyLease=nil
            issecretvalue=function() return false end
            WOW_PROJECT_CLASSIC,WOW_PROJECT_ID=2,2
            GetBuildInfo=function() return scenario=='client-version' and '99.99.9' or '1.15.9' end
            UnitGUID=function() return 'Player-Fixture' end
            Enum={AddOnEnableState={None=0,Some=1,All=2}}
            C_AddOns={
                GetNumAddOns=function() return #bases end,
                GetAddOnName=function(i) local n=bases[i]..suffix; return scenario=='missing' and n==support and 'UnrelatedAddon' or n end,
                GetAddOnMetadata=function(n,k)
                    if scenario=='metadata-error' then error('Metadata must not control runtime') end
                    assert(k~='Dependencies','Dependencies use their dedicated native API')
                    return metadata[n] and metadata[n][k]
                end,
                GetAddOnDependencies=function(n) return metadata[n] and metadata[n].Dependencies end,
                GetAddOnEnableState=function(n) return n==support and scenario=='disabled' and 0 or 2 end,
                IsAddOnLoaded=function(n) return n==support and scenario~='not-loaded' end,
            }
            print=function() end
            local ns={}
            assert(loadfile(root..'/'..name..'/__Distribution/FamilyGate.lua'))(name,ns)
            local allowed={allowed=true,api=true,version=true,family=true,dependency=true,['runtime-api']=true,
                ['master-metadata']=true,['child-contract']=true,['metadata-error']=true,['runtime-legacy']=true,['client-version']=true}
            if allowed[scenario] then
                assert(ns.__ApogeeFamilyAdmission and ns.__ApogeeFamilyAdmission(name),name..' denied')
                if name==support and scenario=='allowed' then
                    -- Boot the generated service through its real gate, then
                    -- prove child admission follows dependency initialization.
                    local mock=dofile(assert(arg[4]))
                    local W=mock.New()
                    if target=='era' then WOW_PROJECT_ID=2 end
                    _G[serviceName]=nil
                    for _,p in ipairs(paths[name]) do
                        if not p:match('^__Distribution/') then assert(loadfile(root..'/'..name..'/'..p))(name,ns) end
                    end
                    assert(_G[serviceName]==ns and not ns.ready)
                    local child='ApogeeHeals'..suffix
                    local early={}
                    assert(loadfile(root..'/'..child..'/__Distribution/FamilyGate.lua'))(child,early)
                    assert(not early.__ApogeeFamilyAdmission,'Child admitted before support initialized')
                    W.Event('ADDON_LOADED',name)
                    assert(ns.ready and not ns.button,'Support startup must not create a launcher alone')
                    local after={}
                    assert(loadfile(root..'/'..child..'/__Distribution/FamilyGate.lua'))(child,after)
                    assert(after.__ApogeeFamilyAdmission and after.__ApogeeFamilyAdmission(child),
                        'Initialized generated support must admit its child')
                    -- A real late Settings exception must also deny every child chunk.
                    W=mock.New(); if target=='era' then WOW_PROJECT_ID=2 end
                    _G[serviceName]=nil
                    _G[family=='DEV' and 'ApogeeDevSettingsRegistry' or 'ApogeeSettingsRegistry']=nil
                    local broken={}
                    assert(loadfile(root..'/'..name..'/__Distribution/FamilyGate.lua'))(name,broken)
                    for _,p in ipairs(paths[name]) do
                        if not p:match('^__Distribution/') then assert(loadfile(root..'/'..name..'/'..p))(name,broken) end
                    end
                    Settings.RegisterAddOnCategory=function() error('injected Settings failure') end
                    W.Event('ADDON_LOADED',name)
                    assert(broken.failed and not broken.ready)
                    local denied={}
                    assert(loadfile(root..'/'..child..'/__Distribution/FamilyGate.lua'))(child,denied)
                    assert(not denied.__ApogeeFamilyAdmission,'Failed master admitted its child')
                    CreateFrame=function() error('Failed master allowed child side effects') end
                    for _,p in ipairs(paths[child]) do
                        if not p:match('^__Distribution/') then assert(loadfile(root..'/'..child..'/'..p))(child,denied) end
                    end
                elseif name~=support then
                    local state=C_AddOns.GetAddOnEnableState
                    C_AddOns.GetAddOnEnableState=function(n) return n==support and 0 or 2 end
                    assert(not ns.__ApogeeFamilyAdmission(name),'disabled master admitted later chunk')
                    C_AddOns.GetAddOnEnableState=state
                    service.apiVersion=2
                    assert(ns.__ApogeeFamilyAdmission(name),'revision labels never expire working methods')
                    service.RegisterSettings=nil
                    assert(not ns.__ApogeeFamilyAdmission(name),'later chunks must revalidate actual capabilities')
                end
            else
                assert(not ns.__ApogeeFamilyAdmission or not ns.__ApogeeFamilyAdmission(name),name..' admitted '..scenario)
                CreateFrame=function() error('Denied package created frame') end
                for _,p in ipairs(paths[name]) do
                    if not p:match('^__Distribution/') then assert(loadfile(root..'/'..name..'/'..p))(name,ns) end
                end
            end
            scenarios=scenarios+1
        end
    end
end
print=originalPrint
print('PASS generated launcher admission: '..scenarios..' '..target..' '..family..' scenarios')
