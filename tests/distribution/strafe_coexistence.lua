-- Actual generated Essentials startup and Keybinds Claim, in both orders.
local keybindsRoot, keybindsName = assert(arg[1]), assert(arg[2])
local essentialsName = assert(os.getenv("APOGEE_ESSENTIALS_RUNTIME_NAME"))
for _, keybindsFirst in ipairs({false,true}) do
    local W=dofile("tests/mock.lua"); W.Install(); _G[essentialsName.."DB"]={}
    W.bindings.A="TURNLEFT"; W.bindings.D="TURNRIGHT"
    W.bindings.Q="STRAFELEFT"; W.bindings.E="STRAFERIGHT"
    local K={__ApogeeFamilyAdmission=function(name) return name==keybindsName end}
    assert(loadfile(keybindsRoot.."/Core/Inputs.lua"))(keybindsName,K)
    assert(loadfile(keybindsRoot.."/Actions/Secure.lua"))(keybindsName,K)
    K.active=true; K.API={Combat=function() return W.combat end,Conflict=function() return false end}
    K.Message=function(message) error(message) end
    K.Secure.owner={}
    for _, slot in ipairs(K.Inputs.all) do
        local id=slot.id
        K.Secure.buttons[id]={GetName=function() return "TestButton"..id end}
    end
    local overrides={}
    ClearOverrideBindings=function(owner) assert(owner==K.Secure.owner); overrides={} end
    SetOverrideBindingClick=function(owner,priority,key,button,click)
        assert(owner==K.Secure.owner and priority and click=="LeftButton")
        assert(key~="A" and key~="D", "Keybinds must not shadow Essentials movement keys")
        overrides[key]=button
    end
    local A=W.Load()
    if keybindsFirst then assert(K.Secure.Claim()) end
    W.Event("PLAYER_LOGIN")
    if not keybindsFirst then assert(K.Secure.Claim()) end
    assert(A.active and W.bindings.A=="STRAFELEFT" and W.bindings.D=="STRAFERIGHT")
    assert(W.bindings.Q=="STRAFELEFT" and W.bindings.E=="STRAFERIGHT", "Native Q/E remain untouched")
    assert(overrides.Q and overrides.E and overrides["SHIFT-Q"] and overrides["SHIFT-E"])
    W.bindings.A="USEREDIT"
    assert(K.Secure.Claim()); A.Apply(); W.Event("UPDATE_BINDINGS")
    assert(W.bindings.A=="USEREDIT" and W.bindings.D=="STRAFERIGHT")
    K.Secure.Release()
    assert(next(overrides)==nil and W.bindings.A=="USEREDIT" and W.bindings.D=="STRAFERIGHT")
end
print("PASS generated Essentials A/D defaults coexist with actual Keybinds claims in both startup orders")
