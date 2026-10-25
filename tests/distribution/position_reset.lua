-- Execute generated launcher -> actual component callback -> actual reset routine.
-- Synthetic saved data only. Rendering is covered by launcher_spec.lua separately.
local folder,family,target,component=unpack(arg)
local suffix=family=='DEV' and 'Dev' or ''
local name=component..suffix
local era=target=='era'
local m,a
if component=='ApogeeHeals' then
    m=dofile('tests/mock.lua').New()
    C_Spell.GetSpellInfo=function(id) return {name='Heal '..id,iconID=123,spellID=id} end
    C_Spell.IsSpellHelpful=function() return true end
    C_Spell.IsSpellHarmful=function() return false end
    C_Spell.IsSpellPassive=function() return false end
    C_SpellBook={IsSpellKnown=function() return true end,IsSpellInSpellBook=function() return true end}
    Enum.SpellBookSpellBank={Player=0}
else
    m=dofile('tests/mock.lua')
    m.Spell(100,'Charge','Rank 1'); m.Spell(1715,'Hamstring','Rank 1')
end
if era then
    WOW_PROJECT_ID=2; WOW_PROJECT_CLASSIC=2
    GetBuildInfo=function() return '1.15.9','70003','',11509 end
    GetNumSpellTabs=function() return 1 end
    GetSpellTabInfo=function() return 'Spells',0,0,1 end
    GetSpellBookItemInfo=function() return 'SPELL',100 end
    GetSpellBookItemName=function() return 'Charge','Rank 1' end
    IsPassiveSpell=function() return false end
end
ApogeeUIDev=ApogeeUI
a={__ApogeeClient=era and 'classic-era' or nil,__ApogeeFamilyAdmission=function(n) return n==name end}
local prefix=folder..'/'..name..'/'
for line in io.lines(prefix..name..'.toc') do
    if line:match('%.lua$') and not line:match('^__Distribution/') then assert(loadfile(prefix..line))(name,a) end
end
if component=='ApogeeHeals' then
    m.addon=a; m.Event('ADDON_LOADED',name); m.Flush(); assert(a.started)
else
    m.K=a; m.Fire('ADDON_LOADED',name); m.Fire('PLAYER_LOGIN'); assert(a.active,a.reason)
end

-- Replace the dependency double with the generated dispatch/registration/menu code.
-- Keep the Settings registrar double; no Settings creation occurs during a reset.
local U=ApogeeUI
ApogeeUI=nil; ApogeeUIDev=nil
U.Client={Supported=function() return true end,CloseMenu=function() end}
U.__ApogeeFamilyAdmission=function() return true end
local master='ApogeePartyHealthBars'..suffix
assert(loadfile(folder..'/'..master..'/SharedUI/ApogeeUI'..suffix..'.lua'))(master,U)
U.RefreshComponent=function() end -- Headless test: actual menu/reset paths stay intact.
U.ready=true; U.save={schema=1,angle=91,unknown={keep=true}}; U.angle=91
if component=='ApogeeHeals' then a.Minimap.Create() else a.Minimap.Build() end
local actions={}
local menu={AddMenuReleasedCallback=function() end,CreateTitle=function() end,CreateDivider=function() end,
    CreateButton=function(_,label,run) actions[label]=run end}
U.BuildMenu(nil,menu)
local reset=assert(actions['Reset UI positions'])
local minimapOnly=assert(actions['Reset minimap position'])

local function copy(v)
    if type(v)~='table' then return v end
    local result={}; for k,x in pairs(v) do result[k]=copy(x) end; return result
end
local function equal(a,b,path)
    assert(type(a)==type(b),'Type changed: '..path)
    if type(a)~='table' then assert(a==b,'Value changed: '..path); return end
    for k,v in pairs(a) do equal(v,b[k],path..'.'..tostring(k)) end
    for k in pairs(b) do assert(a[k]~=nil,'Field added: '..path..'.'..tostring(k)) end
end
local placement=component=='ApogeeHeals' and {position=true,editorPosition=true,threatPosition=true} or {positions=true}
local function settings()
    local result={}; for k,v in pairs(a.db) do if not placement[k] then result[k]=copy(v) end end
    return result
end
local function attributes()
    local result={}
    local frames=m.frames
    if component=='ApogeeHeals' then
        -- Buff/cleanse suggestions are live views, not user healing assignments.
        frames={unpack(a.View.rows)}
        frames[#frames+1]=a.View.target; frames[#frames+1]=a.View.targetTarget
    end
    for i,frame in ipairs(frames) do
        result[i]={}
        for k,v in pairs(frame.attributes or {}) do
            if type(v)~='table' then result[i][k]=v end
        end
    end
    return result
end
local foreign={binds={spell=9876},preferences={enabled=false}}
local foreignName=component..(family=='DEV' and '' or 'Dev')..'DB'
_G[foreignName]=foreign
local foreignBefore=copy(foreign)
a.db.auditSentinel={nested={enabled=false,value='preserve unknown preferences'}}
if component=='ApogeeHeals' then
    a.db.bindings={['1']=2050,['2']={kind='item',id=1251},['shift-1']=2052}
    a.db.buffs={{id=1243,enabled=false,party=true}}
    a.db.smartBuffs={stamina='manual',armor='off'}
    a.db.threatEnabled=true
    a.db.defaultSpells={enabled=false,time=456,serial=7}
    a.Bindings.Apply()
else
    assert(a.Hud.SetConfiguration(true))
    assert(a.Store.Put('base','key1',{kind='spell',id=100,weaponSet=2}))
    assert(a.Store.Put('base','down',{kind='item',id=10507}))
    a.db.layouts.custom={key2={kind='macro',name='My macro',scope='account'}}
    a.db.weaponSets[2]={[16]=123,[17]=456}
    a.db.rules.melee=false; a.db.rules.explosives=false
    a.db.hideUnusableInCombat=true; a.db.alwaysHideSpells=true
    a.db.defaultSpells={enabled=false,time=456,serial=7}
    a.Rebuild()
end
for _,open in ipairs({false,true}) do
    for _,drag in ipairs({false,true}) do
        if component=='ApogeeHeals' then
            if open then a.BindingEditor.Open() else a.BindingEditor.Close() end
            a.db.position={x=123,y=456}; a.db.editorPosition={x=321,y=654}; a.db.threatPosition={x=98,y=76}
            a.View.ApplyPosition(); a.BindingEditor.customPosition=nil; a.BindingEditor.Place()
            if drag then
                a.View.SetUnlocked(true); a.View.handle.scripts.OnDragStart()
                if open then a.BindingEditor.handle.scripts.OnDragStart() end
            end
        else
            a.Hud.SetConfiguration(open)
            for _,g in ipairs(a.Inputs.groups) do
                a.db.positions[g.id]={x=123,y=456}; a.Hud.Place(g)
                if drag and open then g.handle.scripts.OnDragStart() end
            end
            a.db.positions.weapons={x=321,y=654}; a.WeaponPanel.Place()
            if drag and open then a.WeaponPanel.moving=true end
        end
        local db=a.db; local before=settings(); local secure=attributes()
        local original=copy(db)
        minimapOnly(); equal(original,db,'minimap-only')
        m.combat=true; reset(); equal(original,db,'combat'); m.combat=false
        U.inWorld=false; reset(); equal(original,db,'world-transition'); U.inWorld=true
        reset()
        assert(a.db==db and _G[name..'DB']==db,'Saved database replaced')
        equal(before,settings(),'non-position saved settings'); equal(secure,attributes(),'secure bindings')
        assert(_G[foreignName]==foreign); equal(foreignBefore,foreign,'other family')
        assert(U.angle==220 and U.save.unknown.keep)
        if component=='ApogeeHeals' then
            equal(a.Storage.DefaultPosition(),a.db.position,'party position')
            assert(a.db.editorPosition==nil and a.db.threatPosition==nil)
            assert((a.BindingEditor.frame and a.BindingEditor.frame:IsShown() or false)==open
                and not a.BindingEditor.moving and not a.View.dragging)
            if a.View.handle.scripts.OnDragStop then a.View.handle.scripts.OnDragStop() end
            if a.BindingEditor.handle and a.BindingEditor.handle.scripts.OnDragStop then a.BindingEditor.handle.scripts.OnDragStop() end
        else
            assert(next(a.db.positions)==nil and a.db.configurationMode==open and not a.WeaponPanel.moving)
            for _,g in ipairs(a.Inputs.groups) do
                assert(not g.moving and g.frame.point[4]==g.x and g.frame.point[5]==g.y)
                g.handle.scripts.OnDragStop()
            end
            assert(a.WeaponPanel.frame.point[4]==a.Inputs.weaponsPosition.x)
        end
        local after=copy(db); reset(); equal(after,db,'repeated reset/drag release')
        equal(before,settings(),'settings after drag release')
    end
end
print('PASS generated '..target..' '..name..': complete settings/bindings preservation, menu dispatch, repeated reset, drag release, combat, world and family isolation')
