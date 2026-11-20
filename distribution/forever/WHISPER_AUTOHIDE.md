# Whisper arrival visibility and idle fade - 2026-11-19

DEV1.14.19-dev.11 starts the whisper window hidden, ignoring legacy saved
visibility for startup. A new eligible whisper shows it; the120-second deadline
resets on each eligible arrival. The final second fades parent alpha to zero,
then fully hides the frame and restores alpha for the next use. Excluded-class,
duplicate and unreadable messages do not wake or prolong it. Who updates, settings
and combat events render without resetting the deadline. Manual reopen provides
a new120-second reading period; closing hides until the next arrival/manual open.

Hidden windows expand and reset to the newest messages on arrival. While visible,
arrivals preserve scroll/collapse choices. The bounded100-message session log and
Who level/class/location remain available after fading. Full hide cancels pressed
actions, dragging and owned row/header tooltips, avoiding transparent mouse targets.
Combat still permits reading/show/hide but guards actions/dragging. No saved
deadline/player data, search, sound or existing alert-lifetime changes.

One pending C_Timer.After compares the latest deadline; arrivals do not allocate
additional pending callbacks. OnUpdate runs only during the final fade and is
removed when hidden or renewed. Matching Forever70959/16001 authority reviewed
UITimerDocumentation.After, SimpleFrame.SetAlpha and SimpleScriptRegion.SetScript;
central evidence now includes258 references, adding the timer contract.

Child aba7166b3e958a4c817dc98654cdc96b2d8791da is based on installed efbe547.
Central starts from installed priest DEV.8 afc1c8b, preserving Heals7d7bc23,
Keybinds54da9a3, Who/class filtering and other child/shared pins. Separate pending
healing DEV.9/.10 and release1.14.20 work is not silently included. Reconcile any
newer installed receipt before writes; version text alone is insufficient.

Source57 Lua files/35 specs and29-file exact source archive pass. Lifecycle
coverage includes first show, old saved visibility, renewal before/during fade,
exact hide boundary,1000-arrival timer bound, class filters, rejection/dedup,
Who/settings/combat non-renewal, manual close/open, stale callbacks, scroll/collapse,
interaction cleanup and session reset. Earlier suites now account for the idle
timer and explicitly reopen before testing retained expired location text.
The new lifecycle test also runs against generated PROD and DEV.

Synthetic source geometry/alpha snapshots show arrival,119.5s and hidden120s;
this is not native timing/font/taint/mouse acceptance. Owner should test those
in game, including a whisper arriving during fade and reopening cached messages.
Task evidence is under
`C:/Dev/WoW/local-task-archives/apogee-whisper-autohide-20261119`.
Historical child wrapper targets removed foreverBeta; coordinated validation
uses fresh live authority. Generic central unittest discovery finds0 tests;
the documented runner invokes explicit entry points instead.

No install, game operation, private-save inspection, enable changes, PROD write,
push, main integration, publication or cleanup is included. Immediate explicit
owner approval is required before a checked central DEV installation.

Full coordinated validation completed successfully, including generated PROD/DEV,
Era and frozen install/rollback suites. Fresh live authority258 references verified
before/after; receipt retains nativeAccepted:false. Official running-client
inspect-only and independent preview pass7 writes (Whispers/View.lua plus six
version TOCs),17 preserved docs, no discovery/loading-graph change or restart.
Actual clientRunning:true. Installed DEV.8 byte verification passes unchanged.
Checked DEV ZIP SHA256:
`cf121d89b0d1567699ce6fea528944335046efa49ea7e72468faed04f8296cc6`.
