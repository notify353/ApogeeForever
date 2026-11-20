# Whisper foreground correction - 2026-11-19

Owner screenshot shows the installed DEV.12 whisper panel below another UI.
Child24c22217434da2fb79ef9e5d0726c1001bdebce8 changes only the existing whisper
parent's creation-time SetFrameStrata from MEDIUM to DIALOG. Controls inherit its
layer; existing GameTooltip uses its native higher layer. No Raise loop, polling,
timer or click changes. Grouping, exclusions, metadata and idle fade are retained.

Matching live Forever70959/16001 authority258 refs verified. Existing
SimpleFrameAPIDocumentation.SetFrameStrata is reused. Matching SharedXML/UI.xsd
orders HIGH below DIALOG and TOOLTIP above it; DamageMeterSourceWindow.xml uses
HIGH. Actual overlap, native frame layering and mouse behavior require owner
acceptance; mocks do not simulate the WoW compositor.

DEV1.14.19-dev.13 starts from installed central5348420/child15f6ae5, preserving
the other installed DEV.12 child/shared pins. Source58 Lua/36 specs pass. Focused
coordinated validation uses --skip-frozen-regression, reusing the unchanged frozen
suite's successful full DEV.12 receipt in validation-groups/candidate-validation.json.
Fresh source/generated PROD/DEV/Era and matching authority checks run again in
validation-foreground; no claim of rerunning frozen suites or native acceptance.

Separate owner report: a quoted /who query prints level/class/location in chat
but the whisper log does not update. Current code handles WHO_LIST_UPDATE only.
Native SlashCommands uses SocialWhoOrigin.Chat; WhoList toggles SetWhoToUi with
visibility. The screenshot establishes the missing chat-result path, not which
native events/cached fields fired. Do not claim this candidate fixes Who.
Awaiting owner-provided /dump {WHO_LIST_FORMAT, WHO_LIST_GUILD_FORMAT} output:
these baked-in localization strings are absent from the matching source export.
Need exact template evidence before implementing a guarded localized chat parser.
No native panel opening, global Who routing mutation, automatic query or save
inspection is planned. LFGForever's source was read only for clues and reported
native panel taint; no code copied.

Task evidence: C:/Dev/WoW/local-task-archives/apogee-whisper-autohide-20261119.
This candidate is prepared only. Immediate explicit approval precedes installation;
no game operation, private saves, enabled-state change, PROD write, integration,
push, publication or cleanup is included. Latest installed receipt remains
local-install-backups/apogee-whisper-class-groups-20261119/transaction.json.

Focused coordinated validation passed, including source/generated PROD/DEV/Era,
source-only package checks and before/after live authority. Receipt explicitly
records frozenRegressionRun:false; full unchanged frozen evidence is retained
from DEV.12. Foreground preview and official inspect-only agree7 writes:
Whispers/View.lua plus6 version TOCs,17 preserved documents, no discovery change
or restart. Installed DEV.12 verified unchanged. No installation performed.
Checked DEV.13 ZIP SHA256:
`225bccaa87e27706ec1abc809fa7b9966debce1d07be81cc7da58c3996597f9e`.
