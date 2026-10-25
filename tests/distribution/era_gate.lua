-- Execute real packaged chunks for denied client/family cases, without gameplay mocks.
local root = assert(arg[1])
local savedPrint, secret = print, {}
local scenarios = 0
for _, base in ipairs({"ApogeeHeals", "ApogeeKeybinds", "ApogeeGroupAlert", "ApogeeEssentials", "ApogeeUI"}) do
    local name = base .. "Dev"
    for _, option in ipairs({"allowed", "forever", "retail", "wrong-version", "missing-build", "secret-build",
        "missing-secret", "secret-project", "wrong-target", "secret-target", "metadata-error", "no-guid",
        "prod-enabled", "prod-loaded", "legacy-prod", "bad-state", "bad-enum", "bad-lease", "other-lease"}) do
        ApogeeDistributionFamilyLease = nil
        WOW_PROJECT_CLASSIC, WOW_PROJECT_ID = 2, 2
        if option == "forever" then WOW_PROJECT_ID = 19 end
        if option == "retail" then WOW_PROJECT_ID = 1 end
        if option == "secret-project" then WOW_PROJECT_ID = secret end
        issecretvalue = function(v) return v == secret end
        GetBuildInfo = function() return option == "secret-build" and secret or option == "wrong-version" and "1.60.1" or "1.15.9" end
        if option == "missing-build" then GetBuildInfo = nil end
        if option == "missing-secret" then issecretvalue = nil end
        UnitGUID = function() if option ~= "no-guid" then return "Player-Fixture" end end
        Enum = {AddOnEnableState={None=0, Some=1, All=option == "bad-enum" and 9 or 2}}
        local prod = option == "prod-enabled" or option == "prod-loaded" or option == "legacy-prod" or option == "bad-state"
        C_AddOns = {
            GetNumAddOns=function() return prod and 2 or 1 end,
            GetAddOnName=function(i) return i == 1 and name or "ApogeeHeals" end,
            GetAddOnMetadata=function(addon, key)
                if option == "metadata-error" then error("private text") end
                if key == "X-Apogee-Client" then
                    return option == "secret-target" and secret or option == "wrong-target" and "forever" or "classic-era"
                end
                if addon == "ApogeeHeals" and option == "legacy-prod" then return nil end
                if key == "X-Apogee-Family-Schema" then return "1" end
                if key == "X-Apogee-Family" then return addon == name and "DEV" or "PROD" end
            end,
            GetAddOnEnableState=function(_, guid)
                assert(guid == "Player-Fixture")
                return option == "bad-state" and secret or option == "prod-enabled" and 2 or 0
            end,
            IsAddOnLoaded=function() return option == "prod-loaded" end,
        }
        if option == "bad-lease" then ApogeeDistributionFamilyLease = {schema=2,family="DEV"} end
        if option == "other-lease" then ApogeeDistributionFamilyLease = {schema=1,family="PROD"} end
        print = function(message) assert(not message:find("private text")) end
        local function forbidden() error("Denied package performed gameplay") end
        CreateFrame, SetBinding, SaveBindings, SetOverrideBindingClick = forbidden, forbidden, forbidden, forbidden
        local ns = {__ApogeeClient="stale",__ApogeeFamilyAdmission=function() return true end}
        local before = {}; for k,v in pairs(_G) do before[k]=v end
        local folder = root .. "/" .. name .. "/"
        assert(loadfile(folder .. "__Distribution/FamilyGate.lua"))(name, ns)
        if option == "allowed" then
            assert(ns.__ApogeeClient == "classic-era" and ns.__ApogeeFamilyAdmission(name))
            assert(not ns.__ApogeeFamilyAdmission(base))
            -- A replaced lease also denies already admitted chunks.
            ApogeeDistributionFamilyLease = {schema=1,family="DEV"}
            assert(not ns.__ApogeeFamilyAdmission(name))
            ns.__ApogeeClient, ns.__ApogeeFamilyAdmission = nil, nil
        else
            assert(next(ns) == nil, "Denied gate left an admission")
        end
        for line in io.lines(folder .. name .. ".toc") do
            if line:match("%.lua$") and not line:match("^__Distribution/") then
                assert(loadfile(folder .. line))(name, ns)
            end
        end
        assert(next(ns) == nil, "Denied runtime mutated namespace")
        for k,v in pairs(_G) do
            if k ~= "ApogeeDistributionFamilyLease" then assert(before[k] == v, "Denied runtime changed " .. k) end
        end
        scenarios = scenarios + 1
    end
end
print = savedPrint
print("PASS Era generated client/family gates: " .. scenarios .. " scenarios")
