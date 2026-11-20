# Explicit Who lookup and player level - 2026-11-19

DEV1.14.19-dev.7 adds Who below Reply and Invite without changing the320x294
whisper window. Who prepares an editable quoted /who command; the owner presses
Enter. Matching public WHO_LIST_UPDATE results refresh level, class and location
on retained messages from that exact full-name sender. Unknown levels are omitted;
valid positive integer levels remain session-only and update when fresh results
arrive. Location retains its five-minute expiry. No log identity is saved.

The addon does not invoke restricted SendWho or open protected native panels.
Who is unavailable in combat, restricted contexts, when the native Who panel is
not loaded or the game rule disables it. ADDON_LOADED refreshes controls when
Blizzard_FriendsFrame becomes available. Click release still checks the original
entry, current class exclusions and current lookup availability. No query polling,
automatic searches, extra alerts, sounds or lifetime resets are introduced.

Owning child efbe547c753a2e5b2cae57aa7831aa0742b50676 includes class exclusions
and the four pending whisper bug-sweep fixes. While this feature was underway,
Vanguard DEV.6 was installed in another task. This package deliberately retains
its Keybinds54da9a3e299f57ffdde8ac119408e769b1eb35ea and matching257-reference
API evidence, plus its generated PROD/DEV regression. Other pins are unchanged.
It must chain from the latest installed receipt, not the earlier whisper receipt:
`C:/Dev/WoW/local-install-backups/apogee-vanguard-default-20261119/transaction.json`.
Separate uninstalled priest changes are not included. Version text alone cannot
identify earlier distinct DEV.6 candidates; source hashes and receipts are required.

Source56 Lua files/34 specs and29-file exact source archive checks pass. The new
whisper_who_spec runs on source and generated PROD/DEV: layout, editable lookup,
exact-name public metadata, independent sanitization, invalid/restricted/missing
levels, session inheritance, reload clearing, combat, late native-panel loading,
class changes and press/release recipient races. Reviewed live70959/16001
FriendListDocumentation.WhoInfo.level, native SlashCommands and AddOnsDocumentation
against the matching export; no additional API files beyond installed evidence.

Synthetic source geometry/font renders cover normal, combat, localized and
collapsed states. They demonstrate intended placement, not native fonts, secure
execution or server response timing. Owner in-game acceptance remains pending:
load Who once if needed, click Who/Enter, verify level/class/location updates,
no-result/throttle handling, combat and newly excluded classes. No response means
no fabricated metadata; previously known level/class remain until updated/reload.

Task evidence under
`C:/Dev/WoW/local-task-archives/apogee-whisper-classes-20261119`:
WHO_TASK.md, who-child-checks.log, who-central-checks.log, validation-who,
who-layout.png, who-localized.png and WHO_INSTALL_PREVIEW.md.
Historical child test-local still targets removed foreverBeta; the documented
coordinated runner uses fresh live authority. Generic central unittest discovery
finds0 tests; explicit central test entry points provide actual validation.
No installation, PROD write, push, main integration or publication is included.
Immediate explicit installation approval remains required by workspace AGENTS.

Full coordinated checks completed successfully: generated Who and Vanguard
PROD/DEV, Era and frozen distribution/install/rollback regressions. Exact live
authority verified257 references before/after; nativeAccepted remains false.
Official running-client inspect-only and independent preview pass12 writes
(six Group Alert Lua files plus six version TOCs),17 preserved documents,
no discovery/loading-graph changes and no restart requirement. Actual client
was running at preview; owner reload activates an approved installation.
Installed Vanguard bytes remain unchanged. Checked DEV ZIP SHA256:
`50ebcae2eca5b7b025997cba36c3f7a2d46bece3c857caf7521209b8395e6a9b`.
