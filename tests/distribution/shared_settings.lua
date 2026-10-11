-- Generated modules, mocked native UI. Does not establish live Settings/taint acceptance.
local root = assert(arg[1])
local owners = {
    {"ApogeeHeals", "UI/Settings.lua", "Heals"},
    {"ApogeeKeybinds", "UI/Settings.lua", "Keybinds"},
    {"ApogeeGroupAlert", "Settings/View.lua", "Dungeons"},
    {"ApogeeEssentials", "Core/Settings.lua", "Essentials"},
    {"ApogeeAuction", "RoleSettings.lua", "Auction"},
}
local function noop() end
local frames, categories, roots, serial
local function widget()
    local object = {scripts={}}
    return setmetatable(object, {__index=function(self, key)
        if key == "SetScript" then return function(_, event, callback) self.scripts[event]=callback end end
        if key == "CreateTexture" or key == "CreateFontString" then return widget end
        if key == "GetWidth" or key == "GetHeight" then return function() return 600 end end
        return noop
    end})
end
local function reset()
    ApogeeSettingsRegistry=nil; ApogeeDevSettingsRegistry=nil
    ApogeeAuctionDB=nil; ApogeeAuctionDevDB=nil
    frames, categories, roots, serial = {}, {}, {}, 0
    StaticPopupDialogs={}; GameTooltip=widget()
    CreateFrame=function() local frame=widget(); frames[#frames+1]=frame; return frame end
    InCombatLockdown=function() return false end
    issecretvalue=function() return false end
    canaccessvalue=function() return true end
    canaccesstable=function() return true end
    UnitClass=function() return "Warrior", "WARRIOR" end
    local function category(frame, name, parent)
        serial=serial+1
        local c={id=serial, name=name, parent=parent, frame=frame, children={}}
        function c:GetID() return self.id end
        function c:GetName() return self.name end
        function c:GetParentCategory() return self.parent end
        if parent then parent.children[#parent.children+1]=c end
        categories[#categories+1]=c
        return c
    end
    Settings={VarType={String="string"},
        RegisterCanvasLayoutCategory=function(frame,name) return category(frame,name) end,
        RegisterCanvasLayoutSubcategory=function(parent,frame,name) return category(frame,name,parent) end,
        RegisterAddOnCategory=function(c)
            assert(c and c.GetID, "Native category required")
            c.registered=true
            if not c.parent then roots[#roots+1]=c end
        end,
        GetCategory=function(id) for _,c in ipairs(categories) do if c.id==id then return c end end end,
        OpenToCategory=function(id) assert(Settings.GetCategory(id),"Open must target registered numeric ID") end,
        RegisterAddOnSetting=function(c,_,key,db,_,_,default)
            c.settingCount=(c.settingCount or 0)+1
            local s={}
            if db[key]==nil then db[key]=default end
            function s:GetValue() return db[key] end
            function s:SetValue(value) db[key]=value end
            function s:SetValueToDefault() db[key]=default end
            function s:SetValueChangedCallback(callback) self.callback=callback end
            return s
        end,
    }
end
local function load(owner, family, denied)
    local name=owner[1]..(family=="DEV" and "Dev" or "")
    local ui={Text=widget, Button=widget, Label=widget, ListButton=widget,
        Scroll=function() return widget(),widget() end}
    local A={ready=true,active=true,db={rules={}},UI=ui,Text={},Rules={list={}},
        API={Combat=function() return false end},Hud={HideTooltip=noop},
        Style={Text=widget},Minimap={Refresh=noop},Cleansing={},Threat={},ThreatDiagnostics={},
        Errors={BuildErrorSettings=noop,RefreshErrors=noop},IsFeatureAvailable=function() return true end,
        __ApogeeFamilyAdmission=function(caller) assert(caller==name); return not denied end}
    local start=#frames
    assert(loadfile(root.."/"..family.."/"..name.."/"..owner[2]))(name,A)
    if denied then assert(#frames==start); return end
    if owner[1]=="ApogeeHeals" then A.Settings.Create()
    elseif owner[1]=="ApogeeKeybinds" then A.Settings.Build()
    elseif owner[1]=="ApogeeGroupAlert" then A.testView=A.SettingsView.New({}, {})
    elseif owner[1]=="ApogeeEssentials" then A.BuildSettings()
    else
        local event=frames[start+1]
        event.scripts.OnEvent(event,"ADDON_LOADED",name)
    end
    local registry=family=="DEV" and ApogeeDevSettingsRegistry or ApogeeSettingsRegistry
    if type(registry)=="table" and type(registry.children)=="table" then
        local child=registry.children[owner[3]]
        if child then
            assert(child.registered and child.parent==registry.category)
            if A.Settings then assert(A.Settings.category==child) end
            if A.testView then assert(A.testView.category==child) end
            if owner[1]=="ApogeeAuction" then assert(child.settingCount>0) end
        end
    end
    return A
end
local function verify(family, count)
    local label=family=="DEV" and "Apogee DEV" or "Apogee"
    local registry=family=="DEV" and ApogeeDevSettingsRegistry or ApogeeSettingsRegistry
    assert(type(registry)=="table" and registry.schema==1)
    local parent=assert(registry.category)
    assert(parent.name==label and not parent.parent)
    assert(#parent.children==count, "Only loaded Settings owners appear")
    local seen={}
    for _,child in ipairs(parent.children) do
        assert(not seen[child.name],"Duplicate subcategory"); seen[child.name]=true
        assert(not child.name:find("Apogee") and not child.name:find("DEV"),"Single-word child labels required")
    end
    return seen
end
local permutations=0
local function order(list, depth)
    if depth>#owners then
        for _,family in ipairs({"PROD","DEV"}) do
            reset()
            for _,index in ipairs(list) do
                -- Auction is intentionally absent from the selected PROD family.
                if family=="DEV" or index~=5 then load(owners[index],family) end
            end
            local seen=verify(family,family=="DEV" and 5 or 4)
            assert(#roots==1 and seen.Dungeons and seen.Keybinds and seen.Heals and seen.Essentials)
            if family=="DEV" then assert(seen.Auction and ApogeeSettingsRegistry==nil)
            else assert(not seen.Auction and ApogeeDevSettingsRegistry==nil) end
        end
        permutations=permutations+1; return
    end
    for i=depth,#owners do list[depth],list[i]=list[i],list[depth]; order(list,depth+1); list[depth],list[i]=list[i],list[depth] end
end
order({1,2,3,4,5},1)
for _,family in ipairs({"PROD","DEV"}) do
    for index,owner in ipairs(owners) do
        if family=="DEV" or index~=5 then
            reset(); load(owner,family); assert(verify(family,1)[owner[3]] and #roots==1)
            load(owner,family); assert(verify(family,1)[owner[3]] and #roots==1)
            if owner[1]=="ApogeeKeybinds" then
                local addon=load(owner,family); assert(addon.Settings.Open())
            end
            for _,bad in ipairs({true, {schema=2}, {schema=1,category={},children={}}}) do
                reset()
                local key=family=="DEV" and "ApogeeDevSettingsRegistry" or "ApogeeSettingsRegistry"
                _G[key]=bad; load(owner,family)
                assert(_G[key]==bad and #categories==0 and #roots==0,"Malformed registry must stay untouched")
            end
            reset(); Settings.RegisterCanvasLayoutSubcategory=nil
            load(owner,family)
            assert(#roots==1 and #categories==1 and not categories[1].parent)
            assert(ApogeeSettingsRegistry==nil and ApogeeDevSettingsRegistry==nil)
            reset(); load(owner,family,true); assert(#categories==0 and #roots==0)
        end
    end
end
reset()
for index,owner in ipairs(owners) do
    if index~=5 then load(owner,"PROD") end
    load(owner,"DEV")
end
assert(#roots==2 and ApogeeSettingsRegistry.category~=ApogeeDevSettingsRegistry.category)
verify("PROD",4); verify("DEV",5)
print("PASS shared Settings: "..permutations.." load orders, sole owners, denied chunks and isolated family parents")
