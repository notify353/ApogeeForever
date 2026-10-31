# Shared launcher - Era / future Forever

The [2026-10-31 capability policy](../RUNTIME_CAPABILITIES.md) supersedes numeric
API, registry-schema and package-version runtime gates described below. Current
candidates validate the fields/methods actually used. Saved-data schema
protection and actual family ownership remain in force.

Current Era.11 architecture: [internal UI and master switch](MASTER.md).
It supersedes the standalone UI and runtime-free marker described in the
historical sections below; current click/drag behavior remains unchanged.
Era.12 removes the minimap hover tooltip at the owner's request. The editor
border, click menu, dragging and saved position remain unchanged.

## Combined controls

Left-click toggles available editors together: open all if any is closed,
otherwise close all. One available editor toggles alone; none is a no-op.
Right-click lists available Heals, Keybinds, Dungeons and Essentials settings
directly, followed by Reset minimap position. No editor menu entries, submenu
or overview shortcut. Stats has no settings entry. Right-drag and saved position
remain unchanged. Existing controls may still close either editor independently.

API 1 adds optional boolean primary to actions, requiring a checked predicate.
The service snapshots one target state, revalidates before each callback, and
skips failed/unreadable predicates or unavailable actions. Callbacks remain
component-owned; failures do not prevent the other editor from responding.
Tooltip and border track changes from existing controls. No settings migration.

## Second audit: Settings and dependency startup

Generated Era DEV and future Forever PROD/DEV now run the complete component
Settings fixture against the actual shared UI owner, including all 24 settings
load orders, each owner alone, missing APIs, malformed registries, repeated
registration, default-spell synchronization, combat lock and saved-choice reload.
The existing frozen-package fixture remains covered in its original mode.
Admission tests also load the generated service through its real gate and
dispatch ADDON_LOADED, checking that dependent components are blocked before
initialization and admitted afterward. Support alone creates no launcher.
These tests pass without another gameplay or packaging change. Era.9 remains
the installed runtime; its receipt is
C:/Dev/WoW/local-install-backups/apogee-launcher-sweep-20261025/transaction.json.
Native testing and fresh Forever validation remain pending.

## Era.9 audit follow-up

Native Menu.lua releases pooled frames after AddMenuReleasedCallback. The service
now clears its exact root reference there (not on unrelated submenu releases),
preventing later combat/launcher cleanup from closing a reused menu frame.
New generated admission checks enforce matching support API, version and family,
the exact dependency, and a successfully initialized service before child chunks.
Dependencies use C_AddOns.GetAddOnDependencies (the variadic string result in
fresh AddOnsDocumentation.lua), not a guessed GetAddOnMetadata key. Future
Forever must verify this contract again against its fresh export before use.
Only support-enabled candidates receive this extra guard; frozen packages remain
byte-identical. Tests reproduce both defects before the fixes and run against Era
DEV and isolated future Forever PROD/DEV. Native acceptance remains user-owned.

One Apogee UI support addon owns the green 32-unit minimap button, native context
menu, Settings parent and per-character schema-1 angle (default 220 degrees).
Source is pinned from Essentials Shared/ApogeeUI, separately packaged. Each
component requires matching support; Essentials itself may be disabled.
Heals and Keybinds no longer create minimap frames. Components register only
after successful supported startup. Editors remain independent and callbacks
revalidate availability. Keybinds unregisters on deactivation; Essentials removes
registration on rollback. Stats registers only on supported initialized Forever.

Current controls are described above; Era.8 originally used a left-click action
menu and right-click overview. Right-drag still saves position and suppresses release clicks.
Combat/world suspension cancels owned menus and dragging; no protected gameplay
mutations are added. Existing default-spell synchronization remains in components
and joins the shared parent's schema-1 registry. No saved settings are imported.

Client adapter evidence: Era 1.15.9.70003, 83 fresh references including menu TOC,
Menu/MenuUtil/MenuTemplates and Vanilla variants. Native menu proxy Close affects
only our owned menu. Forever source is identical but current native authority is
unavailable; future-launcher.lock.json is offline-only and does not replace the
frozen candidate/release locks or beta installation. Includes prepared pre-combat
Forever suppression behavior; no new error-default migration.

Packaging validates explicit support source owner/subdirectory/commit/file hashes,
API 1, exact loaders and every child's dependency. DEV resource/frame/global/save
identities are audited separately. Every support chunk receives the client/family
gate. Marker stays runtime-free. Historical no-support packages remain unchanged.
Install/rollback accept only known inventories, support verified legacy Era receipts,
and retain unknown files/docs/private-save metadata protections. Live-update opt-in
rejects this discovery change. First support installation requires client closed
and a full restart, not a reload. No enable preferences are changed automatically.

Verification: source suites; actual generated support in Era DEV and future
Forever PROD/DEV, 325 component subsets/load orders each; real generated editor
adapters; Stats startup registration; callback failure/stale callbacks, malformed
API/source, future save schema, combat, drag, position/reload and editor independence.
Existing generated Era adapters, denial-before-effects and frozen Forever suites
remain required. Frozen Forever archives must match prior hashes exactly.

Native acceptance (owner performs): restart Era, enable desired components plus
Apogee UI shared support; verify exactly one green button with both components,
each alone, and Essentials or Group Alert alone. Check flat menu order, grouped
editor toggling from every mixed state, external close reflected in tooltip/border, settings destinations,
right-drag then reload persistence, reset, combat dismissal and no release click.
Do not claim native acceptance from mocks. Do not operate WoW or read private saves.


## Verified Era.8 installation - 2026-10-25

Full final runner passed: 172 child specs, 11 Era distribution tests, 95 generated
admission scenarios, four generated Era adapter tests, five launcher/package
checks (325 subsets/load orders in each of three generated targets), and all 77
frozen Forever offline tests. Stats passes 628 tooltip/134 stat-policy/111 auction
checks; future generated PROD/DEV also check Stats registration. Frozen rebuilt
Forever ZIPs remain byte-identical. No live acceptance is claimed.

User's implementation instruction includes the agreed closed-client installation.
Preflight first saw Era running, later independently confirmed it closed. Central
installer rechecked closure and installed without operating the game or changing
addon enable preferences. Receipt/rollback:
C:/Dev/WoW/local-install-backups/apogee-shared-launcher-20261025/transaction.json
28 writes, 114 files backed up, all 122 installed files independently verified
(115 receipt payload and seven preserved README files). All 1477 Forever addon
files and eight frozen repository files unchanged. No private-save contents read.
Artifact: C:/Temp/apogee-launcher-20261025/validation-final/packages/Apogee-1.14.8-era.8-DEV.zip
SHA256 fa2f03d6cdefb99804af0e8f4676b93ec8e3d7f5d0d52c6af94ebe6043296387.

Source pins and offline future candidate are retained on codex/shared-launcher in
six independent worktrees under C:/Temp/apogee-launcher-20261025. No push, main
integration, release or publication. Earlier Era and Forever worktrees preserved.
Next: owner full restart of Era and native checklist above. Future Forever needs
fresh authority and normal validation before pin integration/installation.
