-- Select the native Era adapter by project identity; build/package labels never expire it.
do
    local name, ns = ...
    if type(ns) ~= "table" then return end
    ns.__ApogeeClient, ns.__ApogeeFamilyAdmission = nil, nil
    local ok, admitted = pcall(function()
        return type(issecretvalue) == "function" and not issecretvalue(WOW_PROJECT_ID)
            and not issecretvalue(WOW_PROJECT_CLASSIC)
            and WOW_PROJECT_CLASSIC == 2 and WOW_PROJECT_ID == WOW_PROJECT_CLASSIC
    end)
    if not ok or admitted ~= true then
        if type(print) == "function" then print("Apogee Era DEV inactive: native Era client APIs unavailable.") end
        return
    end
end
