-- Mixed-family admission from both actual generated package inventories.
local root=assert(arg[1])
if arg[2]=='era' then
    WOW_PROJECT_ID=2; WOW_PROJECT_CLASSIC=2
    GetBuildInfo=function() return '1.15.9','70576',nil,11509 end
end
local bases={'ApogeePartyHealthBars','ApogeeHeals','ApogeeKeybinds','ApogeeGroupAlert','ApogeeEssentials','ApogeeStats'}
local originalPrint=print
local cases={
    {'both-on',true,false,false},
    {'prod-master-off',false,false,true},
    {'prod-master-off-loaded',false,true,false},
    {'legacy-master-enabled',true,false,false},
    {'legacy-disabled',false,false,true},
    {'legacy-prod-enabled',false,false,false},
}
for _,case in ipairs(cases) do
    local metadata,names={},{}
    for _,family in ipairs({'PROD','DEV'}) do
        for _,base in ipairs(bases) do
            local name=base..(family=='DEV' and 'Dev' or '')
            names[#names+1]=name; metadata[name]={}
            for line in io.lines(root..'/'..family..'/'..name..'/'..name..'.toc') do
                local k,v=line:match('^## ([^:]+):%s*(.-)%s*$')
                if k then metadata[name][k]=v end
            end
        end
    end
    local legacy=case[1]:match('^legacy')
    if legacy then
        metadata.ApogeePartyHealthBars['X-Apogee-Master']=nil
        metadata.ApogeePartyHealthBars['X-Apogee-Distribution-Only']='1'
        for _,base in ipairs(bases) do metadata[base]['X-Apogee-Requires-Master']=nil; metadata[base].Dependencies=nil end
    end
    issecretvalue=function() return false end
    UnitGUID=function() return 'Player-Fixture' end
    Enum={AddOnEnableState={None=0,Some=1,All=2}}
    C_AddOns={
        GetNumAddOns=function() return #names end,
        GetAddOnName=function(i) return names[i] end,
        GetAddOnMetadata=function(n,k) return metadata[n] and metadata[n][k] end,
        GetAddOnDependencies=function(n) return metadata[n].Dependencies end,
        GetAddOnEnableState=function(n)
            if n:sub(-3)=='Dev' then return 2 end
            if n=='ApogeePartyHealthBars' then return case[2] and 2 or 0 end
            if legacy then return case[1]=='legacy-prod-enabled' and 2 or 0 end
            return 2 -- New PROD children deliberately remain checked while master is off.
        end,
        IsAddOnLoaded=function(n) return n=='ApogeePartyHealthBarsDev' or n=='ApogeePartyHealthBars' and case[3] end,
    }
    ApogeeUIDev={apiVersion=1,ready=true}
    for _,method in ipairs({'RegisterComponent','RefreshComponent','UnregisterComponent','RegisterSettings','EnsureSettingsParent'}) do
        ApogeeUIDev[method]=function() end
    end
    for _,base in ipairs(bases) do
        ApogeeDistributionFamilyLease=nil
        local name=base..'Dev'; local ns={}
        print=function() end
        assert(loadfile(root..'/DEV/'..name..'/__Distribution/FamilyGate.lua'))(name,ns)
        local admitted=ns.__ApogeeFamilyAdmission and ns.__ApogeeFamilyAdmission(name) or false
        assert(admitted==case[4],case[1]..': '..name)
    end
end
print=originalPrint
print('PASS master selection: checked children with master off, loaded family protection, legacy marker and frozen PROD safety')
