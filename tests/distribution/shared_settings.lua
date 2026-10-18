-- Generated modules, mocked native UI. Does not establish live Settings/taint acceptance.
local root = assert(arg[1])
local owners = {
    {"ApogeeHeals", "UI/Settings.lua", "Heals"},
    {"ApogeeKeybinds", "UI/Settings.lua", "Keybinds"},
    {"ApogeeGroupAlert", "Settings/View.lua", "Dungeons"},
    {"ApogeeEssentials", "Core/Settings.lua", "Essentials"},
}
local function noop() end
local frames, categories, roots, serial
local function widget(parent, kind, font)
    local object = {scripts={},children={},parent=parent,kind=kind,font=font}
    if parent then parent.children[#parent.children+1]=object end
    return setmetatable(object, {__index=function(self, key)
        if key == "SetScript" then return function(_, event, callback) self.scripts[event]=callback end end
        if key == "CreateTexture" then return function() return widget(self,"Texture") end end
        if key == "CreateFontString" then return function(_,_,_,template) return widget(self,"FontString",template) end end
        if key == "SetText" then return function(_,text) self.text=text end end
        if key == "SetTextColor" or key == "SetColorTexture" then return function(_,...) self.color={...} end end
        if key == "SetNormalFontObject" then return function(_,font) self.normalFont=font end end
        if key == "SetHighlightFontObject" then return function(_,font) self.highlightFont=font end end
        if key == "SetSize" then return function(_,w,h) self.width=w;self.height=h end end
        if key == "SetShown" then return function(_,shown) self.shown=shown end end
        if key == "SetChecked" then return function(_,checked) self.checked=checked end end
        if key == "GetChecked" then return function() return self.checked end end
        if key == "SetEnabled" then return function(_,enabled) self.enabled=enabled end end
        if key == "GetWidth" or key == "GetHeight" then return function() return 600 end end
        return noop
    end})
end
local function find(frame, predicate)
    for _,child in ipairs(frame.children) do
        if predicate(child) then return child end
        local nested=find(child,predicate); if nested then return nested end
    end
end
local function color(object,r,g,b)
    assert(type(object.color)=="table" and object.color[1]==r and object.color[2]==g and object.color[3]==b)
end
local function typography(frame,title)
    local heading=assert(find(frame,function(c) return c.kind=="FontString" and c.text==title end),"Missing title: "..title)
    assert(heading.font=="GameFontNormalLarge",title.." must use native large title")
end
local function reset()
    ApogeeSettingsRegistry=nil; ApogeeDevSettingsRegistry=nil
    ApogeeAuctionDB=nil; ApogeeAuctionDevDB=nil
    frames, categories, roots, serial = {}, {}, {}, 0
    StaticPopupDialogs={}; GameTooltip=widget()
    CreateFrame=function(kind,_,parent,template) local frame=widget(parent,kind);frame.template=template; frames[#frames+1]=frame; return frame end
    InCombatLockdown=function() return false end
    GetServerTime=function() return 100 end
    SettingsPanel={GetLayout=function(_,c) return {GetFrame=function() return c.frame end} end}
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
local function load(owner, family, denied, saved)
    local name=owner[1]..(family=="DEV" and "Dev" or "")
    local function text(parent,value,font)
        local label=parent:CreateFontString(nil,"OVERLAY",font or "GameFontHighlightSmall")
        label:SetText(value); return label
    end
    local ui={Text=text, Button=function(parent,value) local b=widget(parent,"Button"); b:SetText(value); return b end,
        Label=function(parent,value,_,_,_,font) return text(parent,value,font) end,
        ListButton=function(parent) return widget(parent,"Button") end,
        Scroll=function(parent) return widget(parent,"ScrollFrame"),widget(parent,"Frame") end}
    local A={ready=true,active=true,db={rules={}},UI=ui,Text={},Rules={list={}},
        API={Combat=function() return false end},Hud={HideTooltip=noop},
        Style={Text=function(parent) local label=text(parent,"","GameFontNormal"); label:SetTextColor(1,1,1); return label end},Minimap={Refresh=noop},Cleansing={},Threat={},ThreatDiagnostics={},
        Errors={BuildErrorSettings=noop,RefreshErrors=noop},IsFeatureAvailable=function() return true end,
        __ApogeeFamilyAdmission=function(caller) assert(caller==name); return not denied end}
    if saved then A.db=saved; A.db.rules=A.db.rules or {} end
    A.refreshes=0
    A.Rebuild=function() A.refreshes=A.refreshes+1 end
    A.Bindings={Apply=A.Rebuild}
    local start=#frames
    if owner[1]=="ApogeeGroupAlert" then
        assert(loadfile(root.."/"..family.."/"..name.."/Core/UI.lua"))(name,A)
    end
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
            local title="Apogee "..owner[3]..(family=="DEV" and " DEV" or "")
            typography(child.frame,title)
            if owner[1]=="ApogeeHeals" then
                assert(A.Settings.threat.label.font=="GameFontHighlightSmall")
                color(A.Settings.cleanseStatus,0.8,0.8,0.8)
                InCombatLockdown=function() return true end; A.Settings.Refresh()
                color(A.Settings.threat.label,0.5,0.5,0.5)
                InCombatLockdown=function() return false end; A.Settings.Refresh()
                color(A.Settings.threat.label,1,1,1)
            elseif owner[1]=="ApogeeKeybinds" then
                A.active=false; A.Settings.Refresh(); color(A.Settings.hideUnusable.label,0.5,0.5,0.5)
                A.active=true; A.Settings.Refresh(); color(A.Settings.hideUnusable.label,1,1,1)
            elseif owner[1]=="ApogeeAuction" then
                local label=assert(find(child.frame,function(c) return c.kind=="FontString" and c.text=="Evaluate gear for" end))
                assert(label.font=="GameFontHighlightSmall")
            elseif owner[1]=="ApogeeGroupAlert" then
                local tabs=0
                for _,button in ipairs(child.frame.children) do
                    if button.kind=="Button" and rawget(button,"Present") then
                        tabs=tabs+1; assert(button.template=="UIPanelButtonTemplate")
                        local marker=assert(find(button,function(c) return c.kind=="Texture" and c.height==2 end))
                        color(marker,1,0.82,0)
                        button:Present("Tab",true); assert(button.normalFont=="GameFontNormalSmall" and marker.shown)
                        button:Present("Tab",false); assert(button.normalFont=="GameFontHighlightSmall" and not marker.shown)
                    end
                end
                assert(tabs==3,"Dungeons owns three native settings tabs")
                local headings=0
                for _,label in ipairs(child.frame.children) do if label.kind=="FontString" and label.font=="GameFontNormal" then headings=headings+1 end end
                assert(headings==2,"Dungeons column headings use native gold font")
                local row=A.UI.ListButton(widget(),0,0,200)
                row:Present("Example",true,false,"Shared")
                local selected=assert(find(row,function(c) return c.kind=="FontString" and c.text=="Example" end))
                color(selected,1,0.82,0)
                color(assert(find(row,function(c) return c.kind=="FontString" and c.text=="Shared" end)),0.8,0.8,0.8)
                color(assert(find(row,function(c) return c.kind=="Texture" and c.width==3 end)),1,0.82,0)
                row:Present("Example",false,false);color(selected,1,1,1)
            end
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
    typography(parent.frame,label)
    local help=assert(find(parent.frame,function(c) return c.kind=="FontString" and c.text=="Select an enabled addon's settings from the list on the left." end))
    assert(help.font=="GameFontHighlightSmall");color(help,0.8,0.8,0.8)
    local background=assert(find(parent.frame,function(c) return c.kind=="Texture" end))
    color(background,0.035,0.035,0.045);assert(background.color[4]==0.96)
    assert(#parent.children==count, "Only loaded Settings owners appear")
    if registry.children.Heals or registry.children.Keybinds then
        local check=assert(registry.defaultSpells.check,"Parent control must exist in every load order")
        assert(check.parent==parent.frame and check.label.text=="Enable default spells")
        local toggles=0
        for _,c in ipairs(parent.frame.children) do
            if c.kind=="CheckButton" then toggles=toggles+1 end
        end
        assert(toggles==1,"Exactly one shared default-spells toggle")
    end
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
                load(owners[index],family)
            end
            local seen=verify(family,4)
            assert(#roots==1 and seen.Dungeons and seen.Keybinds and seen.Heals and seen.Essentials)
            if family=="DEV" then assert(not seen.Auction and ApogeeSettingsRegistry==nil)
            else assert(not seen.Auction and ApogeeDevSettingsRegistry==nil) end
        end
        permutations=permutations+1; return
    end
    for i=depth,#owners do list[depth],list[i]=list[i],list[depth]; order(list,depth+1); list[depth],list[i]=list[i],list[depth] end
end
order({1,2,3,4},1)
for _,family in ipairs({"PROD","DEV"}) do
    for index,owner in ipairs(owners) do
        do
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
    load(owner,"PROD")
    load(owner,"DEV")
end
assert(#roots==2 and ApogeeSettingsRegistry.category~=ApogeeDevSettingsRegistry.category)
verify("PROD",4); verify("DEV",4)
print("PASS shared Settings: "..permutations.." load orders, typography, tabs/list colors, sole owners, denied chunks and isolated family parents")

for _,family in ipairs({"PROD","DEV"}) do
    for _,first in ipairs({1,2}) do
        reset()
        local other=first==1 and 2 or 1
        local custom={spell="custom",slot="shift-2"}
        local a=load(owners[first],family,false,{bindings=custom,layouts=custom})
        local b=load(owners[other],family,false,{bindings=custom,layouts=custom})
        local registry=family=="DEV" and ApogeeDevSettingsRegistry or ApogeeSettingsRegistry
        local policy=registry.defaultSpells
        assert(not policy.check:GetChecked() and not a.db.defaultSpells.enabled and not b.db.defaultSpells.enabled)
        for i=1,3 do
            for _,enabled in ipairs({true,false}) do
                policy.check:SetChecked(enabled); policy.check.scripts.OnClick(policy.check)
                assert(a.db.defaultSpells.enabled==enabled and b.db.defaultSpells.enabled==enabled)
                assert(a.db.bindings==custom and b.db.layouts==custom and custom.slot=="shift-2")
            end
        end
        assert(a.refreshes==6 and b.refreshes==6)
        InCombatLockdown=function() return true end
        policy.check.scripts.OnEvent(); assert(not policy.check.enabled)
        policy.check:SetChecked(true); policy.check.scripts.OnClick(policy.check)
        assert(not policy.check:GetChecked() and a.refreshes==6 and b.refreshes==6)
        InCombatLockdown=function() return false end
        policy.check.scripts.OnEvent(); assert(policy.check.enabled)
        assert(policy:Set(true))
        local stale=a.db.defaultSpells
        -- Toggle the remaining addon while the other is disabled, then rejoin it.
        reset(); local solo=load(owners[other],family,false,b.db)
        registry=family=="DEV" and ApogeeDevSettingsRegistry or ApogeeSettingsRegistry
        GetServerTime=function() return 200 end
        assert(registry.defaultSpells:Set(false))
        local newer=solo.db
        for _,newFirst in ipairs({true,false}) do
            reset()
            local fresh,old
            if newFirst then
                fresh=load(owners[other],family,false,newer)
                old=load(owners[first],family,false,{defaultSpells=stale})
            else
                old=load(owners[first],family,false,{defaultSpells=stale})
                fresh=load(owners[other],family,false,newer)
            end
            assert(not fresh.db.defaultSpells.enabled and not old.db.defaultSpells.enabled,"Latest explicit choice wins in either order")
        end
    end
end
reset()
local prod=load(owners[1],"PROD")
local dev=load(owners[2],"DEV")
ApogeeSettingsRegistry.defaultSpells:Set(true)
assert(prod.db.defaultSpells.enabled and not dev.db.defaultSpells.enabled,"Families never share the preference")
print("PASS shared defaults: off initially, single control, both consumers, combat lock, reload/disabled rejoin and family isolation")
