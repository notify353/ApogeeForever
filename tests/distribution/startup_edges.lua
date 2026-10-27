-- Generated runtime, synthetic state: earlier failures and deferred startup.
local folder,family,target,component=unpack(arg)
local name=component..(family=='DEV' and 'Dev' or '')
local heals=component=='ApogeeHeals'
local function copy(value)
    if type(value)~='table' then return value end
    local result={}; for k,v in pairs(value) do result[k]=copy(v) end; return result
end
local function equal(a,b)
    assert(type(a)==type(b),'saved value type changed')
    if type(a)~='table' then assert(a==b,'saved value changed'); return end
    for k,v in pairs(a) do equal(v,b[k]) end
    for k in pairs(b) do assert(a[k]~=nil,'saved field added during cleanup') end
end
for _,deferred in ipairs({false,true}) do
    for _,scenario in ipairs({'healthy','early','partial','queued','cleanup'}) do
        local m
        if heals then
            m=dofile('tests/mock.lua').New()
            C_Spell.GetSpellInfo=function(id) return {name='Heal '..id,iconID=123,spellID=id} end
            C_Spell.IsSpellHelpful=function() return true end
            C_Spell.IsSpellHarmful=function() return false end
            C_Spell.IsSpellPassive=function() return false end
            C_SpellBook={IsSpellKnown=function() return true end,IsSpellInSpellBook=function() return true end}
            Enum.SpellBookSpellBank={Player=0}
        else
            m=dofile('tests/mock.lua'); m.Spell(100,'Charge','Rank 1')
        end
        if target=='era' then
            WOW_PROJECT_ID=2; WOW_PROJECT_CLASSIC=2
            GetBuildInfo=function() return '1.15.9','70003','',11509 end
            GetNumSpellTabs=function() return 1 end
            GetSpellTabInfo=function() return 'Spells',0,0,1 end
            GetSpellBookItemInfo=function() return 'SPELL',100 end
            GetSpellBookItemName=function() return 'Charge','Rank 1' end
            IsPassiveSpell=function() return false end
        end
        ApogeeUIDev=ApogeeUI
        -- Match the real family's registry global while retaining the native-UI double.
        local ensure=ApogeeUI.EnsureSettingsParent
        ApogeeUI.EnsureSettingsParent=function(...)
            local registry=ensure(...)
            if family=='DEV' then ApogeeDevSettingsRegistry=registry end
            return registry
        end
        local a={__ApogeeClient=target=='era' and 'classic-era' or nil,
            __ApogeeFamilyAdmission=function(n) return n==name end}
        for line in io.lines(folder..'/'..name..'/'..name..'.toc') do
            if line:match('%.lua$') and not line:match('^__Distribution/') then
                assert(loadfile(folder..'/'..name..'/'..line))(name,a)
            end
        end
        local fire=heals and m.Event or m.Fire
        if heals then m.addon=a else m.K=a end
        _G[name..'DB']=heals and {bindings={['1']=2050},defaultSpells={enabled=false,time=1,serial=0}}
            or {layouts={base={key1={kind='spell',id=100}}},configurationMode=true}
        _G[name..'DB'].auditSentinel={text='keep',value=false,nested={1,2,3}}
        local snapshot,registry,neighbor
        local function fail()
            if scenario=='queued' then
                if heals then a.Runtime.Request()
                else
                    a.API.pendingItems[999]=true
                    fire('GET_ITEM_INFO_RECEIVED',999)
                end
                assert(#m.timers>0,'fixture failed to queue deferred work')
            end
            snapshot=copy(a.db)
            registry=ApogeeUI.EnsureSettingsParent()
            if registry and registry.defaultSpells then
                neighbor={getDB=function() return {defaultSpells={enabled=false,time=1,serial=0}} end,refresh=function() end}
                registry.defaultSpells.consumers.neighbor=neighbor
            end
            if scenario=='cleanup' then
                a.Minimap.Unregister=function() error('injected unregister failure') end
                if heals then a.Buffs.Stop=function() error('injected buff cleanup failure') end
                else a.Hud.CloseMenu=function() error('injected menu cleanup failure') end end
            end
            error('injected '..scenario..' startup failure')
        end
        if scenario~='healthy' then
            local owner,key
            if scenario=='early' then owner,key=heals and a.View or a.Hud,heals and 'Create' or 'Build'
            elseif scenario=='partial' then owner,key=heals and a.Cleansing or a.UI,heals and 'Create' or 'ActionIcon'
            elseif scenario=='queued' then owner,key=heals and a.Runtime or a.Secure,heals and 'Start' or 'Claim'
            else owner,key=heals and a.ThreatDiagnostics or a.Secure,heals and 'Start' or 'Claim' end
            local original=owner[key]; local calls=0
            owner[key]=function(...)
                calls=calls+1
                if scenario=='early' then fail() end
                local result=original(...)
                if scenario~='partial' or calls==3 then fail() end
                return result
            end
        end
        m.combat=deferred
        assert(pcall(fire,'ADDON_LOADED',name)); if not heals then assert(pcall(fire,'PLAYER_LOGIN')) end
        if deferred then
            assert(a.startupState=='pending' and not (heals and a.started or a.active))
            m.combat=false; assert(pcall(fire,'PLAYER_REGEN_ENABLED'))
        end
        if scenario=='healthy' then
            assert(a.startupState=='active' and (heals and a.started or a.active),'healthy startup regressed')
            m.Flush(); snapshot=copy(a.db)
            local p=assert(ApogeeUI.components[heals and 'heals' or 'keybinds'])
            p.actions[1].run(); p.actions[1].run()
            equal(snapshot,a.db)
        else
            assert(a.startupState=='failed' and not (heals and a.started or a.active),'partial startup stayed active')
            if registry and registry.defaultSpells then
                assert(not registry.defaultSpells.consumers[name],'failed component retained shared callback')
                assert(registry.defaultSpells.consumers.neighbor==neighbor,'cleanup removed another consumer')
            end
            local frames=#m.frames
            m.Flush(); fire('PLAYER_REGEN_ENABLED'); fire('PLAYER_ENTERING_WORLD'); fire('PLAYER_LOGIN')
            assert(#m.frames==frames and a.startupState=='failed','failed startup retried')
            equal(snapshot,a.db)
            assert(not ApogeeUI.components[heals and 'heals' or 'keybinds'])
            if heals then
                if a.View.root then assert(not a.View.root:IsShown()) end
                for _,f in pairs({a.Runtime.driver,a.Threat.frame,a.ThreatDiagnostics.frame,a.Buffs.timerDriver}) do
                    assert(not f.scripts.OnUpdate and next(f.events)==nil)
                end
            else
                assert(next(m.overrides)==nil and next(a.frame.events)==nil and not a.frame.scripts.OnUpdate)
                for _,g in ipairs(a.Inputs.groups) do if g.frame then assert(not g.frame:IsShown()) end end
                for _,b in pairs(a.Hud.buttons) do if b.remove then assert(not b.remove:IsShown()) end end
            end
        end
    end
end
print('PASS generated startup edges: '..name..' '..target..', early/partial/queued/cleanup, combat deferral and saved-data isolation')
