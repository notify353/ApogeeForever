# Whisper class exclusions - 2026-11-19

Group Alert's existing per-character Exclude classes checklist now also filters
its incoming whisper window. Positively known excluded class tokens hide matching
messages before the three-row viewport; unresolved classes remain visible. All
messages remain in the bounded, session-only 100-message log, so clearing an
exclusion restores retained messages. Ordinary WoW chat and recruitment alerts
are unaffected. Playstyles continue to apply only to official multiplayer groups.

Settings changes refresh the window immediately. Incoming public identity and
Who updates re-evaluate existing entries, without automatic queries or polling.
Scroll anchoring uses message identity so excluded arrivals do not shift the
message being read. Reply, Invite and location clicks recheck exclusions at
release, retaining the prior recipient, combat and permission safeguards.
Class controls and Clear exclusions keep their existing combat locks.

Child e7569fcebbce9ce5592ae9acc6f7e8c7931f0369 includes the four pending
[bug sweep fixes](WHISPER_SWEEP.md). DEV1.14.19-dev.6 preserves other child/shared
pins from installed DEV.3. Prepared priest DEV.4 remains separate and uninstalled;
any newer installed changes must be reconciled before installation.

Source checks pass:55 Lua files,33 specs and29-file source archive byte checks.
The new whisper_classes_spec.lua also runs against generated PROD and DEV.
Coverage includes all/none/multiple classes, unknown/restricted data, cached
restoration, independent resets, per-character persistence, combat locks, late
identity changes, click races, scrolled arrivals and bounded storage/frame count.
Filter changes add no searches, sounds or timer resets. Exact existing API
authority remains Forever1.60.1.70959/16001,255 references; no new API is used.

Source-derived settings geometry was rendered and inspected, including the
updated two-line class explanation. This is a synthetic layout check, not native
WoW acceptance. Owner in-game layout, interaction and timing checks remain pending.
Task evidence and the final checked package/installation preview live under
`C:/Dev/WoW/local-task-archives/apogee-whisper-classes-20261119`.

Installation requires fresh explicit owner approval under workspace AGENTS.md.
Preparation does not install, publish, push or integrate. Use the latest installed
receipt and a new verified rollback backup through the central DEV installer.
Do not operate WoW, inspect private saves, change enable preferences or write PROD.

Completed central coordinated validation passes generated PROD/DEV, Era and full
frozen regression suites; receipt retains nativeAccepted:false. The historical
child wrapper expects removed foreverBeta authority; coordinated validation uses
the matching live export. Generic central unittest discovery finds0 tests; the
documented runner invokes explicit test entry points instead.
Official running-client inspect-only and independent preview pass12 writes
(six existing Group Alert Lua paths plus six version TOCs),17 preserved documents,
no loading-graph changes and no restart requirement. Actual clientRunning:true;
installation would require the owner to reload. Installed DEV.3 is unchanged.
Checked DEV ZIP SHA256:
`8ffcdeccd90beeb2ba42625dc17f34a8eedf44d29b5697d60ccfcfc81e0db262`.
