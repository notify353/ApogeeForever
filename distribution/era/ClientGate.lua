-- Era-only admission preamble. The unchanged family gate follows this block.
do
    local name, ns = ...
    if type(ns) ~= "table" then return end
    ns.__ApogeeClient, ns.__ApogeeFamilyAdmission = nil, nil
    local ok, admitted = pcall(function()
        if type(issecretvalue) ~= "function" or type(GetBuildInfo) ~= "function" then return false end
        local version = GetBuildInfo()
        if issecretvalue(version) or issecretvalue(WOW_PROJECT_ID)
            or issecretvalue(WOW_PROJECT_CLASSIC) then return false end
        if WOW_PROJECT_CLASSIC ~= 2 or WOW_PROJECT_ID ~= 2
            or type(version) ~= "string" or not version:match("^1%.15%.") then return false end
        if type(C_AddOns) ~= "table" or type(C_AddOns.GetAddOnMetadata) ~= "function" then return false end
        local target = C_AddOns.GetAddOnMetadata(name, "X-Apogee-Client")
        return not issecretvalue(target) and target == "classic-era"
    end)
    if not ok or admitted ~= true then
        if type(print) == "function" then print("Apogee Era DEV inactive: incompatible client or package.") end
        return
    end
end
