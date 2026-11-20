# Who chat result refresh and foreground - 2026-11-19

DEV1.14.19-dev.14 fixes the unhandled chat-result path while retaining the
foreground correction from the uninstalled DEV.13 candidate. Installed DEV.12
only refreshed on WHO_LIST_UPDATE. A manually submitted quoted /who can return
its answer as CHAT_MSG_SYSTEM. The new handler consumes only public system text
matching the client's exact native Who format; no automatic query, native-panel
opening or global Who routing change. Existing list-result handling remains.

The owner supplied these matching-client /dump values in the November19 screenshot
codex-clipboard-6c312772-1426-48b1-86d3-b3de4dc61188.png:

```text
WHO_LIST_FORMAT = |Hplayer:%s|h[%s]|h: Level %d %s %s - %s
WHO_LIST_GUILD_FORMAT = |Hplayer:%s|h[%s]|h: Level %d %s %s <%s> - %s
```

Runtime reads the localized globals, not these hardcoded English examples.
Two cached anchored patterns validate placeholder types/counts and escape literal
pattern characters, supporting positional substitutions and literal percent signs.
Player-link target, display, level, race, class, optional guild and area retain
their argument identities. Only the exact full link target matches retained
senders; display labels cannot redirect metadata to another player or realm.
Native localized male/female class names resolve the class suffix even when race
or class has spaces. Unknown classes preserve prior public identity. Public input
is bounded to2048 bytes and messages to100 session entries. Restricted text or
missing/malformed formats fail safely. No arbitrary text enters recruitment
discovery or SavedVariables. Existing metadata render, class filters/grouping,
pressed-recipient guards and location expiry apply without renewing the idle fade.

Child2354e8c39ac9dbe1a4cd1a4f020349ea4dff82bb includes runtime fix dfe0e27
and synthetic player fixtures, building on foreground24c2221 and
installed15f6ae5; central starts42c4cb5. Preserve installed Heals7d7bc23,
Keybinds54da9a3 and other shared/child pins. Pending healing/release work remains
separate; reconcile any later installed receipt before writing. The latest known
receipt is local-install-backups/apogee-whisper-class-groups-20261119/transaction.json.

Matching live Forever70959/16001 authority258 refs verified; existing ChatInfo
CHAT_MSG_SYSTEM and Constants localized class tables cover this handler. Owner
dump supplies the baked-in format authority absent from the exported source.
The regression fails against installed DEV.12 at the missing chat-only refresh,
then passes against current source.59 Lua files/37 specs and29-file exact source
archive pass. Regression covers guild/no-guild, spaces, localized/positional
formats, literal pattern characters, secret/malformed/missing data, exact targets,
class grouping/filtering, action races, combat, location expiry, idle deadline,
hidden-window non-renewal, bounded timers/frames and no implicit actions.
1000 unrelated system events take about0.03s synthetic CPU with no added frames
or timers; this is not an in-game performance measurement.

Focused coordinated source/generated PROD/DEV/Era checks use validation-who-chat-final
and --skip-frozen-regression. Unchanged frozen suites reuse their successful full
DEV.12 evidence in validation-groups/candidate-validation.json; do not claim they
were rerun. Current native acceptance remains false. Owner must test a real
chat-printed Who response and overlap with the damage meter after installation.

Task evidence lives under
C:/Dev/WoW/local-task-archives/apogee-whisper-autohide-20261119.
No installation, WoW operation, private saves, enabled-state changes, PROD writes,
integration, push, publication or cleanup included. Immediate explicit approval
is required before the checked central DEV installation.

Final focused coordinated validation passed. Source/generated PROD/DEV/Era and
before/after live258-reference authority are checked; nativeAccepted:false and
frozenRegressionRun:false are explicit. Official running-client inspect-only and
independent preview agree9 writes: Group Alert entry point, Whispers/Client.lua,
Whispers/View.lua and6 version TOCs.17 documents preserved; installed DEV.12
verified unchanged. No new loading paths/discovery changes or restart required.
The first interrupted validation-who-chat run was replaced by the completed
validation-who-chat-final run after changing test fixtures to synthetic names;
runtime bytes did not change. Checked DEV.14 ZIP SHA256:
`b1df3146ce5ee1af3c931ae387fc73050658b9df92bec0f6265bbc3b82bcdb98`.
