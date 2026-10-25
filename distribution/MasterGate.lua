-- Appended only to packages declaring the embedded master contract.
do
    local name, ns = ...
    local admitted = ns.__ApogeeFamilyAdmission
    if type(admitted) ~= "function" then return end
    local family = "@FAMILY@"
    local support = family == "DEV" and "ApogeePartyHealthBarsDev" or "ApogeePartyHealthBars"
    local service = family == "DEV" and "ApogeeUIDev" or "ApogeeUI"
    local function compatible()
        local function exact(value, expected)
            return not issecretvalue(value) and value == expected
        end
        local function metadata(addon, key) return C_AddOns.GetAddOnMetadata(addon,key) end
        local version = metadata(name,"Version")
        if issecretvalue(version) or type(version) ~= "string" or version == ""
            or not exact(metadata(support,"Version"),version)
            or not exact(metadata(name,"X-Apogee-UI-API"),"1")
            or not exact(metadata(support,"X-Apogee-UI-API"),"1")
            or not exact(metadata(support,"X-Apogee-Family"),family)
            or not exact(metadata(support,"X-Apogee-Family-Schema"),"1") then return false end
        local character = UnitGUID("player")
        if issecretvalue(character) or type(character) ~= "string" or character == "" then return false end
        local state = C_AddOns.GetAddOnEnableState(support,character)
        if issecretvalue(state) or (state ~= 1 and state ~= 2)
            or not exact(metadata(support,"X-Apogee-Master"),"1") then return false end
        if name == support then return true end
        if not exact(metadata(name,"X-Apogee-Requires-Master"),"1")
            or not exact(C_AddOns.IsAddOnLoaded(support),true) then return false end
        if type(C_AddOns.GetAddOnDependencies) ~= "function" then return false end
        local dependency, extra = C_AddOns.GetAddOnDependencies(name)
        if not exact(dependency,support) or not exact(extra,nil) then return false end
        -- WoW loads required dependencies first, but a dependency's Lua may
        -- have failed. Admit gameplay only after the matching service is ready.
        local ui = rawget(_G,service)
        if issecretvalue(ui) or type(ui) ~= "table" or getmetatable(ui) ~= nil
            or not exact(rawget(ui,"apiVersion"),1) or not exact(rawget(ui,"ready"),true) then return false end
        for _,method in ipairs({"RegisterComponent","RefreshComponent","UnregisterComponent",
            "RegisterSettings","EnsureSettingsParent"}) do
            local fn = rawget(ui,method)
            if issecretvalue(fn) or type(fn) ~= "function" then return false end
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
            print("Apogee " .. family .. ": " .. name .. " inactive. Enable the matching Apogee master addon and restart.")
        end
    end
end
