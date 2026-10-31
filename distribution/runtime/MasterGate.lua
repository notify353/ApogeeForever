-- Current shared-service capability admission. Package/version labels are provenance only.
do
    local name, ns = ...
    local admitted = ns.__ApogeeFamilyAdmission
    if type(admitted) ~= "function" then return end
    local family = "@FAMILY@"
    local support = family == "DEV" and "ApogeePartyHealthBarsDev" or "ApogeePartyHealthBars"
    local service = family == "DEV" and "ApogeeUIDev" or "ApogeeUI"
    local function compatible()
        local function public(value) return not issecretvalue(value) end
        local character = UnitGUID("player")
        if not public(character) or type(character) ~= "string" or character == "" then return false end
        local state = C_AddOns.GetAddOnEnableState(support, character)
        if not public(state) or (state ~= 1 and state ~= 2) then return false end
        if name == support then return true end
        local loaded = C_AddOns.IsAddOnLoaded(support)
        if not public(loaded) or loaded ~= true then return false end
        local ui = rawget(_G, service)
        if not public(ui) or type(ui) ~= "table" or getmetatable(ui) ~= nil then return false end
        local ready, failed = rawget(ui, "ready"), rawget(ui, "failed")
        if not public(ready) or not public(failed) or ready == false or failed then return false end
        for _, method in ipairs({"RegisterComponent", "RefreshComponent", "UnregisterComponent",
            "RegisterSettings", "EnsureSettingsParent"}) do
            local fn = rawget(ui, method)
            if not public(fn) or type(fn) ~= "function" then return false end
        end
        return true
    end
    ns.__ApogeeFamilyAdmission = function(caller)
        if not admitted(caller) then return false end
        local ok, result = pcall(compatible)
        return ok and result == true
    end
    if not ns.__ApogeeFamilyAdmission(name) then
        ns.__ApogeeFamilyAdmission, ns.__ApogeeClient = nil, nil
        if type(print) == "function" then
            print("Apogee " .. family .. ": " .. name .. " inactive. Enable and initialize the shared master; required UI methods must be available.")
        end
    end
end
