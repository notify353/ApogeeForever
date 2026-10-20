## Focus diagnostic removed - 2026-10-20

Owner chose native health alerts and requested removal of this task's tests.
Heals be8ee10 removes the Focus panel, runtime, TOC hooks and diagnostic spec;
other Heals features and diagnostics are unchanged. Central combined candidate
8f91a74 preserves concurrent dungeon settings 86889e7 and damage placement afae151.
Full child checks with matching Forever 70450 export and all 76 central tests
plus generated-family checks pass. Evidence under
C:/Temp/apogee-focus-health-20261020/: removal-child-checks.log,
removal-final-checks.log, removal-final-validation/, removal-verification.json.

DEV receipt: C:/Dev/WoW/local-install-backups/apogee-focus-removed-20261020/transaction.json.
Chained from apogee-damage-placement-20261020. Verified 115 installed files,
137 backups and 111 unchanged PROD files. Three Heals DEV writes (bootstrap,
TOC, settings); explicitly retired ApogeeHealsDev/Health/Diagnostics.lua to
verified retired-files backup. No private saves, native alert preferences,
other diagnostics, retained worktrees or historical evidence were removed.
First preview refused concurrent damage changes before any writes; final
combined candidate passed full checks and installed successfully. Owner reload
required; if stale UI persists after reload, restart manually. Native UI
acceptance pending. No push, main integration or publication performed.

## Incoming damage placement installed - 2026-10-20

Owner explicitly approved the placement fix. Combined candidate 1530154 retains
the concurrently installed dungeon-settings update from 86889e7; all 76 central
tests and generated checks passed again. Essentials 4ee0e2f places the row above
threat, at center Y=45. Atomic DEV install changed only Damage/Runtime.lua.
Receipt: C:/Dev/WoW/local-install-backups/apogee-damage-placement-20261020/transaction.json,
chained from apogee-dungeon-settings-20261020. Independently verified 116 installed
files, 137 backups and 111 unchanged PROD files. Evidence:
C:/Temp/apogee-incoming-damage-20261020/placement-install-verification.json.
Owner reload and visual placement acceptance pending; no discovery changes.
No private-save access, game operation, enable changes, push or publication.

## Incoming damage DEV installed - 2026-10-20

Owner explicitly approved DEV installation. Checked candidate fb1aada was
installed atomically via the central installer, chained from the roster-font
receipt. New receipt:
C:/Dev/WoW/local-install-backups/apogee-incoming-damage-20261020/transaction.json.
Independently verified 116 installed files, 136 backup files and all 111 PROD
files unchanged. Only Essentials DEV bootstrap, TOC and new Damage/Runtime.lua
changed. Evidence: C:/Temp/apogee-incoming-damage-20261020/install-verification.json.
Reload required; if the new module is not discovered, user restart may be needed.
No game operation, private-save access, enable changes, push or publication.
HUD appearance and full magic/periodic/environmental coverage await owner testing.

## Restricted Dungeons settings installed - 2026-10-20

Owner explicitly approved installation. Rechecked canonical d08c0eb and newest
indicator-order receipt; no concurrent change since final validation. Installed
checked candidate 330c8ab (handoff 802eae2), Group Alert 6e3085e, via the central
atomic DEV installer. Exactly four Group Alert DEV files changed: bootstrap,
TOC notes, Discovery/Dictionary.lua and Settings/View.lua. Verified all 116
installed files, 137 backup files and 111 unchanged PROD files.
Receipt: C:/Dev/WoW/local-install-backups/apogee-dungeon-settings-20261020/transaction.json.
Evidence: C:/Temp/apogee-dungeon-mappings-20261020/settings-install-preview.json,
settings-install-log.json and settings-install-verification.json. This supersedes
the prior pending-install status below. All 23 child suites and 76 central checks
were passed for these bytes. Concurrent Heals/Essentials changes are retained.

Next: owner /reload and visual acceptance of Dungeons wording toggles, including
shared per-dungeon choices and combat browsing. Restart only if reload does not
discover the TOC update. No game operation, private-save access, preference edits,
PROD install, push, main integration or publication. Retained backups/worktrees
remain available. Future installs must chain from this new receipt.

## Restricted Dungeons settings prepared - 2026-10-20

Implemented the approved toggle-only plan. Group Alert 6e3085e retains a complete
predefined catalog separately from enabled mappings, archives personal additions
without applying/deleting them, and confirms official names through native activity
discovery. Exclusions, native level data and collected/ignored history survive.
Settings show alphabetical dungeon/wording lists, per-dungeon shared checkboxes,
combat browsing with disabled changes, and native fonts. Editing tabs/actions,
Defaults and the native reset callback are removed.

Child test-local passes all 23 suites on matching Forever 1.60.1.70450 / 16001.
Central 330c8ab combines this change with latest canonical d08c0eb; all 76 tests
and generated PROD/DEV regressions pass. Concurrent incoming damage, combat-hidden
indicators and leader-left/role-right layout are retained. Evidence:
C:/Temp/apogee-dungeon-mappings-20261020/settings-child-checks.log,
settings-final-checks.log and settings-final-validation/packages.

Preview against newest installed receipt
C:/Dev/WoW/local-install-backups/apogee-indicator-order-20261020/transaction.json
changes exactly four ApogeeGroupAlertDev files: bootstrap, TOC notes,
Discovery/Dictionary.lua and Settings/View.lua. Preview/baseline and verification
helper: settings-install-preview.json, settings-prod-before.json,
verify-settings-install.py in the task folder. Planned backup:
C:/Dev/WoW/local-install-backups/apogee-dungeon-settings-20261020.

NOT INSTALLED. Immediate deployment approval is required by the owner's explicit
plan/workspace rules; earlier installation approvals do not cover this candidate.
Recheck newest candidate/receipt before installing with the central installer, then
verify installed bytes/backups and unchanged PROD via the helper's after mode.
User reload and visual acceptance are required; TOC notes changed, so restart only
if reload fails to discover the update. No private-save access, game operation,
push, main integration, publication or cleanup. Worktrees/backups preserved.

## Incoming damage candidate - 2026-10-20

Essentials ba80077 adds the combat-only Physical/Magic incoming damage row,
reset each fight. Unreadable or incomplete fights show dashes. The candidate
preserves installed party roles and reviewed roster-font Group Alert aef5998.
No installer has run for this candidate. Source tests pass; native magic,
periodic/environmental coverage and HUD placement remain pending. Installation
requires immediate owner approval under the current workspace agreement.
Task/evidence: C:/Temp/apogee-incoming-damage-20261020.
Use the latest installed receipt, currently
C:/Dev/WoW/local-install-backups/apogee-roster-font-20261020/transaction.json,
and recheck concurrent candidates before any installation.

## Multilingual roster font installed - 2026-10-20

Owner approved fix, checks and installation. Group Alert aef5998 preserves the
native multilingual font family with SetFontHeight. All 23 child suites and 75
central tests/generated checks pass, including synthetic Unicode roster tests.
Current Heals assigned-role changes are retained alongside prior features.
Only Group Alert DEV Core/UI.lua changed. Verified 115 installed files, 136
backup files and 111 unchanged PROD files. Receipt:
C:/Dev/WoW/local-install-backups/apogee-roster-font-20261020/transaction.json.
Evidence: C:/Temp/apogee-dungeon-mappings-20261020/font-final-validation,
font-final-checks.log and font-install-verification.json. User reload and visual
glyph acceptance pending. No discovery changes or publication.

## Reviewed dungeon mappings installed - 2026-10-20

Owner approved installation. Combined current ce7876b with the reviewed Group
Alert 6f2d5f8 pin, preserving Heals level typography, Focus diagnostic and crown.
All 75 central tests and generated checks pass. Evidence:
C:/Temp/apogee-dungeon-mappings-20261020/install-validation and install-checks.log.
The checked atomic DEV install changed only Group Alert Discovery/Dictionary.lua
and Matching/Dungeons.lua. Verified 115 installed files, 136 backups and 111
unchanged PROD files. Receipt:
C:/Dev/WoW/local-install-backups/apogee-dungeon-mappings-20261020/transaction.json.
Previous receipt: apogee-party-leader-20261020. No discovery changes; user reload
required. Native acceptance pending. Use this combined candidate and newest
receipt for subsequent DEV changes. No publication, push or main integration.
Historical validation-only artifacts below were not installed.

## Focus health feasibility DEV diagnostic - 2026-10-20

Heals c4957bd combines the silent Focus health diagnostic (33a29ca) with the
concurrently installed level-font fix af69c4e, retained as cherry-pick c4957bd.
No sound is implemented or bundled. Settings > Heals > Focus health checks opens
session-only Start/Stop/Reset controls. Separate combat/outside counters show
readability and observed 50% crossings. Restricted data never enters comparisons.

Full Heals checks with matching Forever 1.60.1.70450 export pass. All 74 central
checks and generated PROD/DEV regressions pass, including health diagnostics.
Evidence: C:/Temp/apogee-focus-health-20261020/validation and child-checks.log,
central-checks.log, install-preview.json, install-verification.json.
DEV receipt: C:/Dev/WoW/local-install-backups/apogee-focus-health-20261020/transaction.json,
chained from the level-truncation receipt. Independently verified 115 installed
files, 135 backups and 111 unchanged PROD files. Four Heals DEV files changed:
bootstrap, TOC, UI/Settings.lua and new Health/Diagnostics.lua. Private saves,
local documentation and enable preferences preserved by the central installer.

Reload required; if the new diagnostic is not discovered, owner may need to
restart. Owner solo/party combat readability and UI acceptance remain pending;
previous native acceptance does not cover these new runtime bytes. No game
operation, PROD install, push, main integration, publication or cleanup occurred.
Focus asset provenance is incomplete in the legacy attribution; no license claim
or asset redistribution is made by this diagnostic.

# One source, two distributions

## October 20 reviewed dungeon vocabulary candidate

Group Alert candidate pins 6f2d5f8fdaeb31f54d7a80ff73768de4b9563728.
Reviewed 200 saved DEV discovery phrases with explicit owner permission limited
to those records. No raw examples or private data are included in the changes.
Exact reviewed aliases resolve against known full dungeon names, preserving
native IDs, level data and personal exclusions. Ambiguous shorthand remains
unconfirmed. Gnomergon is a reviewed Gnomeregan spelling.

Child test-local passes (22 specs); central validation passes all 75 Python
tests and generated PROD/DEV gameplay checks, including the pinned vocabulary
regression. Matching export: Forever 1.60.1.70450 / 16001.
Evidence: C:/Temp/apogee-dungeon-mappings-20261020/validation and central-checks.log.
Install preview changes two Group Alert DEV Lua files and the DEV marker TOC.
Quality follow-up: new aliases now defer to valid personal associations even
without prior removals. All 22 child specs and 75 central tests pass again,
including the expanded regression against both generated families. Evidence:
C:/Temp/apogee-dungeon-mappings-20261020/quality-validation and quality-checks.log.
The earlier install preview is superseded: concurrent Heals work was installed
under apogee-level-truncation-20261020. This isolated candidate retains its older
Heals baseline and is validation-only until reconciled with the latest checked
central candidate. Do not install either task artifact set directly.
Installation also awaits immediate owner approval under workspace instructions.
No PROD installation, saved-data edits, push, integration or publication.

## October 18 actual stat-gain explanations

Coordinated tooltip fix 0a6ebbb was reviewed and cherry-picked as Stats 5050906
onto the latest auction/Warrior layout branch. Upgrade reasons include only
positive relevant stat changes; equal Stamina with higher Armor shows Armor only.
Ranking is unchanged. Equipment-only auction availability remains included.

Child checks pass: 624 tooltip, 134 policy and 111 auction assertions. All 74
central tests and generated PROD/DEV validation pass. Evidence under
C:/Temp/apogee-auction-budget-20261017: reasons-validation, reasons-checks.log,
reasons-install-preview.json and reasons-install-verification.json. Receipt:
C:/Dev/WoW/local-install-backups/apogee-stats-reasons-20261018/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Core/Rules.lua changed; no discovery changes. User /reload and native
acceptance remain pending. No game operation, private-save access, preference
changes, push, main integration or publication. Retained worktrees are preserved.

## October 17 coordinated Warrior tank weapon layouts

Shield/weapon chat handed over 1c8ff48 (Weapon DPS first) and 96e86a4 (current
layout-aware comparison) for the same next candidate. Cherry-picked onto latest
auction work as ac1fd39 and 982f912; documentation conflicts retain both tasks'
changes. Stats 982f912 is the combined immutable pin. The intermediate weapon
candidate passed checks but was not installed while the layout follow-up finished.

Warrior tank melee weapons rank DPS, then Stamina and existing tie-breakers
within the currently equipped shield, two-handed or trained dual-wield layout.
Hand restrictions and no inferred empty off-hand/cross-layout recommendations
are preserved. Other classes and shield Armor-first priorities are unchanged.
Latest equipment-only auction filtering/category continuity remain included.

Combined child checks: 619 tooltip, 134 policy, 111 auction assertions. All 74
central tests and generated PROD/DEV checks pass. Evidence under
C:/Temp/apogee-auction-budget-20261017: layout-validation, layout-checks.log,
layout-pins.log, layout-install-preview.json, layout-install-verification.json.
Receipt: C:/Dev/WoW/local-install-backups/apogee-warrior-layout-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Core/Rules.lua changed; no discovery changes. Owner /reload and native
layout comparisons remain pending. No game operation, private-save access,
enable changes, push, main integration or publication occurred. Source worktree
C:/Temp/apogee-tank-shield-20261017/ApogeeStats and prior backups are retained.

## October 17 Armor/Weapons filtering availability

Stats e5202f3 limits filtering to native Armor/Weapons roots and descendants.
Other categories and All categories restore native results, dim/disable custom
controls and show category guidance. Remember dice preference, cap and role;
returning restores them and waits for a matching Search when enabled. Native
localized root names are used, not fixed indexes or English labels. Previous
category-continuity and tank-shield priority changes remain included.

Child checks: 602 tooltip, 123 policy, 111 auction assertions. All 74 central tests
and generated PROD/DEV checks pass. Evidence under
C:/Temp/apogee-auction-budget-20261017: equipment-validation, equipment-checks.log,
equipment-api-review.json, equipment-install-preview.json,
equipment-install-verification.json, equipment-pins.log. Receipt:
C:/Dev/WoW/local-install-backups/apogee-auction-equipment-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Auction/Browse.lua changed; no discovery changes. Owner /reload and native
layout/timing acceptance remain pending. No game operation, private-save access,
enable preference changes, push, main integration or publication occurred.

## October 17 category continuity and coordinated shield priorities

Stats f1a1958 keeps the filtered provider empty after category changes instead
of restoring native unfiltered rows under a lit dice. Gold/role remain set;
status/list prompt for Search. Old responses and edits cannot repopulate the
list until a new native search starts. Best stays disabled while waiting.

The shield-priority chat requested inclusion in this same DEV update. Reviewed
00a6dd0 from its retained codex/tank-shield-armor worktree and cherry-picked as
8a7b61a onto the auction branch. Resolved the changelog conflict by preserving
both entries; README changes merged. Warrior/Paladin tank shields rank Armor,
then Stamina, then existing defensive tie-breakers. Other roles/slots unchanged.
The combined immutable Stats pin is 8a7b61a; no main integration occurred.

Combined child checks pass: 602 tooltip, 123 policy, 100 auction assertions.
All 74 central tests plus generated PROD/DEV checks pass. Evidence under
C:/Temp/apogee-auction-budget-20261017: category-shield-validation,
category-shield-checks.log, category-shield-install-preview.json,
category-shield-install-verification.json, category-shield-pins.log.
Receipt: C:/Dev/WoW/local-install-backups/apogee-auction-category-shield-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Auction/Browse.lua and Core/Rules.lua changed; no discovery changes.
Owner /reload and native category/shield acceptance remain pending. No game
operation, private-save access, enable changes, push or publication occurred.

## October 17 dice / gold / role / best controls

Owner explicitly requested a left-side dice enable/disable switch, followed by
Max gold, default All roles with optional role narrowing, and disabled best until
a specific native slot is selected. Stats a4903f5 implements this, superseding
prior interaction decisions below. Best also requires one role/playstyle and
complete checks. Explicit inventory slot filters are required; broad or class/
subclass-only categories remain browseable. Purchases remain manual.

Child checks: 602 tooltip, 104 policy, 89 auction assertions. All 74 central tests
and generated PROD/DEV checks pass. Evidence in
C:/Temp/apogee-auction-budget-20261017: dice-validation, dice-checks.log,
dice-api-review.json, dice-install-preview.json, dice-install-verification.json,
dice-pins.log. Receipt:
C:/Dev/WoW/local-install-backups/apogee-auction-dice-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Auction/Browse.lua changed; no discovery changes. Owner /reload and native
layout/server timing acceptance remain pending. No game operation, private-save
access, enable preference changes, push, integration or publication occurred.

## October 17 browse-first auction correction

Owner approved all selected-role upgrades first, optional Max gold narrowing,
and Select best only on explicit click. Stats 9686772 supersedes the one-action
flow below. Compact Role / Max gold (Any) / Select best row; no dice. Native
Search owns candidates. Clearing the cap restores all role upgrades immediately.
Completed checks never open a winner. Purchases remain manual.

Child checks pass: 602 tooltip, 104 policy, 73 auction assertions. All 74 central
tests and generated PROD/DEV checks pass. Evidence in
C:/Temp/apogee-auction-budget-20261017: browse-validation, browse-checks.log,
browse-install-preview.json, browse-install-verification.json, browse-pins.log.
Receipt: C:/Dev/WoW/local-install-backups/apogee-auction-browse-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Two Stats
Auction Lua files changed; no discovery changes. Owner /reload and native layout,
server timing and manual-Buyout acceptance remain pending. No game operation,
private-save access, enable changes, push, integration or publication occurred.

## October 17 one-action auction upgrade search

Owner rejected the dice/Select best interaction. Stats e7fee67 removes the dice
and offers Find best upgrade after role and budget input. It starts a native
filtered search, checks listings and selects a fresh winner; Cancel stops work.
Native filters own slot selection and purchases remain manual. Supersedes the
role-first interaction below. No loader or identity-transform changes.

Child checks: 602 tooltip, 104 policy, 66 auction assertions. All 74 central tests
and generated-family checks pass. Evidence: C:/Temp/apogee-auction-budget-20261017/
find-validation, find-checks.log, find-api-review.json, find-install-verification.json.
DEV receipt: C:/Dev/WoW/local-install-backups/apogee-auction-find-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Auction/Browse.lua and Auction/Queue.lua changed; no discovery changes.
Owner /reload and native UI/server-timing acceptance remain pending. No game
operation, private-save access, enable changes, push, integration or publication.

## October 17 Stats role-first correction

Owner rejected the duplicate slot selector and requested role selection first.
Stats now requires an explicit role/playstyle before enabling dice or Max gold;
slot/category filtering belongs to the native auction UI. Mixed-slot results
cannot produce a best ranking, and native category changes cancel old checks
until a new native search runs. This supersedes the initial slot UI below.
Runtime acceptance remains pending. Stats source is 9474ea0 (full revision and
hashes in the lock). Child tests pass: 602 tooltip, 104 policy and 120 auction
assertions; all 74 central tests plus generated PROD/DEV checks pass. Evidence:
C:/Temp/apogee-auction-budget-20261017/role-first-final-validation and
role-first-final-checks.log.

Installed through the central checked DEV path. Receipt:
C:/Dev/WoW/local-install-backups/apogee-auction-role-first-20261017/transaction.json.
Verified 114 installed files, 135 backups and 111 unchanged PROD files. Only
Stats Auction/Browse.lua and Auction/Queue.lua changed; no discovery changes.
Owner reload and native verification are pending. No game operation, enable
changes, private-save access, push, main integration or publication occurred.

## October 17 Stats auction budget

Stats adds a visit-only per-item buyout cap, slot filter and Select best for one
role/playstyle. Actual item searches are throttled and bounded; incomplete work
never selects. The winning listing is refreshed before exact price/ID selection;
buying remains manual. No loader, saved-data or identity-transform changes.
The immutable revision and file hashes are in candidate.lock.json. Native
acceptance is invalidated; prior evidence is retained in history.

Child checks and all 74 central tests passed, including generated PROD/DEV
auction selection regressions. Final evidence:
C:/Temp/apogee-auction-budget-20261017/final-validation and final-central-checks.log.
The initial package notice-label mismatch was corrected before final validation.

Checked DEV receipt:
C:/Dev/WoW/local-install-backups/apogee-auction-budget-20261017/transaction.json.
Independently verified 114 installed files, 135 backup files and 111 unchanged
PROD files. Three Stats Lua files and the existing DEV version marker changed.
Differing documentation and private data remain preserved. Owner reload and
auction layout/timing/manual-Buyout acceptance are pending; the marker version
may need discovery on restart if reload does not refresh it. No push, main
integration, publication or game operation occurred. Task record:
C:/Temp/apogee-auction-budget-20261017/task-record.md.


## October 17 default-spell control placement correction

Owner requested moving the single checkbox into the Keybinds feature settings
group. Heals ba8cb53 and Keybinds 21922bf place it above the Keybinds rule toggles;
the parent overview and Heals page contain no duplicate control. Shared behavior,
off-initially preference and custom assignment locations remain unchanged.
Both child suites and full central validation pass (74 Python tests and generated
Lua checks, including 24 load orders in both families). Evidence:
C:/Temp/apogee-default-spells-20261017/move-validation and move-central-checks.log.

DEV receipt: C:/Dev/WoW/local-install-backups/apogee-default-spells-keybinds-20261017/transaction.json.
Only Heals/Keybinds UI/Settings.lua changed. Independently verified 114 installed
files, 135 backups and 111 unchanged PROD files. No discovery changes; user reload
required, then open Apogee DEV > Keybinds. Native acceptance remains pending.
No private-save access, game operation, push, integration or publication occurred.

## October 17 optional default spells

Heals 77b8b41 and Keybinds d211ef4 add one per-character **Enable default spells**
checkbox on the Apogee parent Settings page. New and existing characters without
an explicit choice start off. Only automatic spell fallbacks are gated; custom
spell/item/macro assignments and their locations, weapon attachments and highlights
are preserved across repeated toggles. The shared registry mirrors only this
timestamped preference into the two independent per-character stores. Either
addon can supply the control, including when another child created the parent.
PROD/DEV settings remain isolated. Combat locks the control. No new TOC entries,
saved globals, dependencies or identity transforms are introduced.

Both child suites and full central validation passed against matching Forever
1.60.1.70450 / 16001: 74 Python tests and generated Lua checks, including all 24
settings-owner load orders in both families, default-off, repeated on/off clicks,
custom locations, reload/character isolation and disabled-addon rejoin.
Evidence: C:/Temp/apogee-default-spells-20261017/validation and sibling check logs.

DEV receipt: C:/Dev/WoW/local-install-backups/apogee-default-spells-20261017/transaction.json,
chained from apogee-70450-20261017-r2. Independently verified 114 installed files,
135 backups and 111 unchanged PROD files. Seven gameplay Lua files and the existing
DEV marker version TOC changed. Differing documentation and private saved data
remain preserved. User reload required; the marker metadata may require discovery
on restart if the client does not refresh it. Native toggle acceptance is pending;
prior accepted evidence remains historical. No game operation, push, integration,
release or publication occurred. Task record: C:/Temp/apogee-default-spells-20261017/task-record.md.

## Development repository rename

The development repository and canonical checkout are named ApogeeForever:
`C:/Dev/WoW/ApogeeForever`, `notify353/ApogeeForever`. The installed
ApogeePartyHealthBars marker/TOC and historical migration identities remain
unchanged. Old path mentions in historical evidence describe their original
locations. No source repinning, gameplay change, addon installation or release
is implied by this development-only rename.

## October 12 Tank and standalone Auction retirement

The owner explicitly requested removal of Tank and Auction from this system
and Apogee. The current lock now contains five active children: Heals, Keybinds,
Group Alert, Essentials and Stats. Both PROD and DEV contain those five plus
their marker. Tank/Auction pins and active source requirements are removed. Historical
locks, migration safety recognition, source repositories and backups are retained.
Validation uses the current five-addon candidate and historical distribution
revisions; it no longer fetches or requires a retired sibling repository. Historical seven-child descriptions below are superseded by this scope.

The installer accepts the exact current six-root DEV inventory and preserves
omitted legacy folders rather than deleting them implicitly. Explicit owner
uninstallation uses `scripts/retire-unused-dev-addons.ps1` with the client root,
previous verified install receipt and a new backup directory outside the game.
It accepts only the two retired DEV roots, refuses unexpected runtime edits and
reparse points, checks every source/destination path, and moves whole folders to
a byte-verified recovery backup. Unknown documentation stays with that backup.
No saved variables, enabled-state preferences or source repositories are read,
changed or deleted. The owner restarts the game to refresh discovery and unload
already-loaded code; never operate the client from this task.

Full central validation passed at `C:/Temp/apogee-retire-validation-20261012`.
Retirement journal: `C:/Dev/WoW/local-install-backups/apogee-tank-auction-retired-20261012/retirement.json`.
Current DEV receipt: `C:/Dev/WoW/local-install-backups/apogee-five-addon-update-20261012/transaction.json`.
All 84 removed files are verified in the recovery backup, all 246 remaining
PROD/DEV files are byte-identical, and all 114 non-preserved package files match
the new DEV ZIP. None of the four canonical/DEV Tank/Auction roots remains in
AddOns. The installer performed no writes to the remaining addons. No game
operation, saved-data access, remote mutation or publication occurred.

## October 12 exclusive class-strip input

Heals pins `1a67fd51c864cba25959cf2d338d8e1165de1fc6`. The owner reports
the strip still healing on other classes and clarifies the strip location,
regardless of its class color, is exclusively for buff input. The secure row's
hit rectangle now excludes the rail and seam. The full-height overlay covers
that same width, disables click propagation, absorbs all button presses/releases,
and toggles only on left release through the existing combat guard. All nine
class fixtures cover input ownership independently of whether buff options exist.
No sibling, identity transform or buff catalog changes. Native physical-click
acceptance remains pending; mocks verify configuration rather than hit testing.

Full child and central checks passed at `C:/Temp/apogee-strip-input-validation-20261012`.
DEV receipt: `C:/Dev/WoW/local-install-backups/apogee-strip-input-1a67fd5-20261012/transaction.json`.
Independently verified 188 package files, 219 backups and 111 unchanged PROD
files. Heals Buffs/View.lua, PartyFrames/View.lua and UI/Style.lua changed;
no discovery changes. User reload and physical-click verification remain.

## October 11 buff recipient range

Heals pins `f27aff25008eeb6292a012074074ad4c32019ba3`. The owner clarified
that the remaining confusing icons were on out-of-range recipients. All buff
choices now use their own native spell-range check against the fixed recipient;
confirmed out-of-range choices disappear from automatic and expanded lists.
The existing one-second refresh restores them after movement. Self buffs remain
available; unknown/restricted range is not classified as out of range. Generated
class integration and dedicated range tests cover movement, recipient isolation,
manual expansion and combat. Sibling pins and transforms are unchanged.

Child and full central validation passed at `C:/Temp/apogee-buff-range-validation-20261011`.
DEV receipt: `C:/Dev/WoW/local-install-backups/apogee-buff-range-f27aff2-20261011/transaction.json`.
Independently verified 188 package files, 219 backups and 111 unchanged PROD
files. Only Heals Buffs/Runtime.lua changed; no discovery changes. User reload
and native movement verification remain. No game operation or publication.

## October 11 buff family name fallback

Heals pins `126d0b549e56321e4d66043904ed3bbea9dbbc96`. The owner reports that
the prior protection still fails and requests class-wide behavior. Fixed the
reproducible unlisted-rank gap: client-localized ordinary/group buff names now
provide family coverage as well as manual replacement protection. No hardcoded
English matching, guessed strength comparison, identity transforms or sibling
changes. Generated class and blessing regressions include unlisted aura IDs.
Native acceptance remains false; the actual reported case needs owner testing.

Full child and central checks passed at `C:/Temp/apogee-buff-names-validation-20261011`.
The new cross-class regression fails against the previous implementation. DEV
receipt: `C:/Dev/WoW/local-install-backups/apogee-buff-names-126d0b5-20261011/transaction.json`.
Independently verified 188 package files, 219 backups and 111 unchanged PROD
files. Four Heals runtime files changed; no discovery changes. User reload is
required. No game operation, PROD install or publication occurred.

## October 11 foreign-buff coverage correction

Heals pins `5781d06a3f014d7675a67969076b4483e2d253ff`. The owner reported a
"more powerful" blessing error. The early-refresh rule now applies only to
confirmed player-owned applications. Foreign or unknown-source buffs remain
coverage until removed and suppress matching recast choices during strip expansion.
Other blessing types remain available. This conservatively protects equal/weaker
foreign buffs too, since rank/ID does not prove strength after talent improvements.
Native own aura/aspect choices retain their separate stance authority.

The new regression covers self/party/target, higher and Greater blessings,
same-rank foreign applications, unknown source, removal recovery, own refresh
and gap-free icon layout in both generated families. Artifacts:
`C:/Temp/apogee-buff-foreign-coverage-validation-20261011-r2`. Existing runtime
acceptance is invalidated; historical accepted hashes and reports are preserved.
Publication remains blocked pending owner acceptance of this correction and
write-capable GitHub authentication. No sibling or identity transform changes.

Full child/central validation passed. The release-gate regression now separately
handles explicitly unaccepted candidates as well as changed accepted runtime.
DEV receipt: `C:/Dev/WoW/local-install-backups/apogee-buff-foreign-coverage-5781d06-20261011/transaction.json`.
All 188 package files and 219 backups independently verified; 111 PROD files
unchanged. Only Heals Buffs/Runtime.lua changed; no discovery changes. Reload and
verify the previously rejected blessing situation. No game operation or publication.

## October 11 quality review and release handoff

Reviewed the complete Heals buff-strip/timer diff against the released baseline:
restricted-value guards, fixed recipient actions, combat and lifecycle handling,
timer boundaries, duplicate coverage, input geometry, polling and distribution
isolation. No blocking runtime defect was found. Added recipient-isolation and
no-catch-up/preview polling regressions in child commit
`940b6fb66ff16c753dbb59235b5c4c6d80a6721d`. This changes tests only; both generated
family file maps and archive hashes are identical to the accepted installed
timer-polish candidate. No reinstall is necessary.

The owner reports "perfect" for the installed result and requests review and
deployment preparation. Native acceptance now records that report and the exact
verified DEV runtime and generated PROD counterpart; unchanged sibling acceptance
is retained. It does not claim a comprehensive native test matrix or separate
PROD/CurseForge-client testing. Release notes are consolidated.

Full child checks with the matching export and full central checks passed.
Evidence: `C:/Temp/apogee-buff-quality-validation-20261011`. Offline publisher
payload acceptance passes for planned patch 1.14.5. No release version/tag has
been created. Both repositories are committed locally on their task branches;
push/main integration require explicit approval under the owner instructions.
After integration, use prepare-release.ps1 from synchronized main, integrate its
release PR and pass exact-final-main hosted checks before requesting production-tag
approval. Existing worktrees/backups are retained; no cleanup, game operation,
PROD installation, external message or publication occurred.

## October 11 buff timer presentation correction

Heals pins `d4ad2103e43619b59e32e1f78346a31756b4317d`. Buff timers use smaller
outlined numeric text, centered and inset inside the icon. Long durations use
compact minute/hour labels (56m, 2h); the final two minutes retain m:ss. This
addresses the owner's screenshot of a wide 56:18 label crossing the icon edge.
Reminder thresholds, strip controls and combat behavior are unchanged. Existing
generated expiry regressions cover compact formatting and text bounds. Artifacts:
`C:/Temp/apogee-buff-timer-polish-validation-20261011`. Native appearance requires
owner review after reload. Sibling pins and identity transforms are unchanged.

Child/full central checks passed. DEV receipt:
`C:/Dev/WoW/local-install-backups/apogee-buff-timer-polish-d4ad210-20261011/transaction.json`.
All 188 package files and 219 backups independently verified; 111 PROD files
unchanged. Only Heals Buffs/View.lua changed, with no discovery changes. Reload
to inspect the presentation. No game operation, PROD installation or publication.

## October 11 early buff reminders and timers

Heals pins `217ff5eea83147b0b39b261ad7cdeb9fb0ddb0e9`. Existing buff icons appear
for missing buffs or known remaining durations below 120 seconds. An m:ss label
shows remaining time on matching icons, including manually expanded choices.
Unknown/permanent timing retains coverage without a guessed timer. One shared
one-second update handles countdowns and threshold crossings outside combat;
preview/world suspension also disables its aura work. No panel or settings added.
Sibling pins, identities and loader inventories are unchanged. The new regression
runs against both generated families. Artifacts:
`C:/Temp/apogee-buff-expiry-strip-validation-20261011`. Native acceptance is pending.
The owner's lower-strip click report is also addressed: the toggle now belongs
to the full row, with explicit full-height geometry above the strip artwork,
instead of inheriting the health-only name layer's bounds. Every supported row
is covered by the revised strip regression in both generated families.

Child checks and full central validation passed. DEV installation receipt:
`C:/Dev/WoW/local-install-backups/apogee-buff-expiry-strip-217ff5e-20261011/transaction.json`,
chained from the inline-strip correction. All 188 package files, 155 Lua files
and 219 backup files were independently verified; all 111 PROD files are unchanged.
Only Heals Buffs/Catalog.lua, Runtime.lua and View.lua changed. No discovery
changes; user reload activates the update. Settings, private saves and differing
documentation are preserved. No game operation, PROD install or publication.

## October 11 inline buff-strip correction

The owner requested the existing left-side buff icons, without the additional
panel. Heals now pins `6bdc011` (full immutable commit in candidate.lock.json).
Clicking the strip toggles the existing blessing/upkeep/aura choices, including
already active buffs. Clicking again restores ordinary missing-buff reminders.
The panel and current-buff text list are removed. Combat and recipient changes
clear expansion; the existing secure icon controls and visibility remain in use.
All sibling pins and transforms are unchanged. This supersedes the panel below.
Validation artifacts: `C:/Temp/apogee-buff-strip-inline-validation-20261011`.

Child and full central checks passed, including the revised regression in both
generated families. DEV-only receipt:
`C:/Dev/WoW/local-install-backups/apogee-buff-strip-inline-6bdc011-20261011/transaction.json`.
All 188 package files, 155 Lua files and 219 backups were independently verified;
111 PROD files are unchanged. Only Heals Buffs/Runtime.lua and Buffs/View.lua
changed on disk; no discovery changes. Reload to activate. Native acceptance is
pending. No game operation, PROD installation, push, merge or publication occurred.

## October 11 class-strip buff picker DEV candidate

Heals pins `87f3a6142c97ed883c87bc977e5a4c76364c5c10`. Clicking the class-color
strip opens a recipient picker with current buffs and learned buff choices,
including already active blessings for recasting/replacement. It is available
only outside combat, closes on combat entry and target/group changes, and does
not reopen when combat ends. Current unknown/restricted aura data closes it.
Native secure buttons retain fixed recipients. No saved data, loader inventory
or identity transforms change; all six sibling pins remain unchanged.

The child regression is included in both generated family checks. Child checks
use the matching Forever export. Full distribution validation artifacts are at
`C:/Temp/apogee-buff-strip-validation-20261011`. Native appearance, casting and
taint acceptance require owner testing; prior native acceptance is not advanced.

Full child and central checks passed. DEV-only installation is recorded at
`C:/Dev/WoW/local-install-backups/apogee-buff-strip-87f3a61-20261011/transaction.json`,
chained from the minimap-consistency receipt. All 188 package files, 155 DEV Lua
files and 219 backups were independently verified; all 111 PROD files are unchanged.
Private saves, enable preferences and 31 differing documentation files are preserved.
Four Heals Lua files changed. The existing DEV marker TOC also advances to the
current distribution version; it is the only discovery change. Reload with DEV
enabled; if the updated TOC is not discovered, a user restart may be needed.
No game operation, PROD installation, push, merge or publication occurred.

The active local workflow is side-by-side PROD and DEV. Earlier prototype and
migration fixtures remain historical evidence. PROD 1.0.0 is published on
CurseForge and GitHub; DEV remains local. APHB is a zero-Lua distribution identity with no gameplay or saved
settings. The candidate now pins seven independent children; five are selected for PROD.

## Build and validate

### Hosted Auction

Auction is now a private hosted child under notify353, pinned by immutable commit
and file hashes alongside the other children. The candidate includes isolated ApogeeAuctionDev in DEV only. PROD has six roots
(five selected children and the marker); DEV has eight. ApogeeTank and
ApogeeAuction remain DEV-only. ApogeeStats is included in both families as an
inert baseline with no gameplay or saved data.
Historical source locks retain their original five-child inventories; local-only
Auction fixtures remain supported but cannot be promoted without a hosted pin.

Auction provides all nine classes and sixteen supported class/role combinations, a saved
per-character role selector, and confirmed Defaults. Clear upgrades show ROLL NEED;
known stat tradeoffs show POSSIBLE UPGRADE; unresolved data stays quiet.
The native auction browse list also provides session-only upgrade filters, a shared
role selector, bounded evaluation and manual pagination. Recommendations describe
personal value without group-competition vetoes. Its displayed-tooltip path preserves random
auction suffix stats. All generated runtime chunks are guarded, and canonical
Auction participates in the same PROD/DEV exclusion decision as the other addons.

Hosted validation and production require read access to the private Auction and Stats
repositories in DISTRIBUTION_READ_TOKEN. Adding the repository does not establish
that access. Runtime changes require renewed owner-reported native acceptance;
local validation does not authorize a release or claim in-game acceptance.

Run from the canonical checkout `C:/Dev/WoW/ApogeeForever`.
This document and its central scripts are the stable authority for all seven
child projects. Historical prototype worktrees are retained evidence, not an
installation dependency. Run `pwsh ./scripts/test-local.ps1` for full validation.

```powershell
python -B scripts/dual_distribution.py --sources-root C:/Dev/WoW --output C:/Temp/apogee-dual-UNIQUE
python -B tests/distribution/test_dual.py --sources-root C:/Dev/WoW --artifacts C:/Temp/apogee-tests-UNIQUE
python -B tests/distribution/test_migration.py --sources-root C:/Dev/WoW --artifacts C:/Temp/apogee-migration-tests-UNIQUE
```

`candidate.lock.json` pins immutable source commits and explicit file hashes.
Before future development builds, locally commit the reviewed child candidate on
its task branch, update only that child's pin/file inventory to reviewed Git
blobs, and run its checks plus aggregate checks. Never include sibling dirty
files implicitly. New identity tokens or loader mechanisms need an explicit audit.

The builder emits two deterministic ZIPs from the same pins. PROD retains exact
source gameplay bodies behind an admission prefix. DEV transforms audited
identifiers, saves, frames, popup/slash names, asset paths and labels. Manifests
list every identity edit and source/body hash. Comments, gameplay keys and Blizzard
names are not blindly renamed. The publicChildren selection in candidate.lock.json includes five PROD children;
DEV retains all seven pinned children. Public artifacts have six roots including
the marker; DEV has eight. Tank and Auction remain DEV-only, with their pins retained.
Family safety still recognizes older installed canonical Tank and Auction. Omitting a folder
from a ZIP does not prove CurseForge removes an older installed copy; that update
behavior needs client acceptance. Never delete PROD folders or saved data here.
Heals uses an independent default position beneath the default Keybinds Mouse grid.
Its factory-reset dialog is explicitly mapped to a separate DEV identity; the
confirmation and per-character storage remain within their own family.
The existing CurseForge project1608100 download owns PROD roots, never the eight DEV roots.
DEV TOCs contain no CurseForge project ID.
Each family marker bundles the existing green Apogee logo from the pinned
Keybinds source and points its IconTexture at that family-local asset. Native
group rows use the marker icon; this adds no runtime, saved data or child dependency.

## Install and recover

Only the central installer writes local DEV folders. Future child changes must
not copy canonical sources over production. Normal local installs are DEV-only.
Requested source changes include checked DEV installation under standing owner
authorization; do not ask for another routine DEV install confirmation.

The owner requires canonical PROD folders to come only from the CurseForge app.
The initial staged PROD candidate has been moved out of AddOns into the verified
handover backup at `C:/Dev/WoW/local-install-backups/apogee-curseforge-handover-20260924`.
Its transaction.json preserves all original files for explicitly authorized recovery.
Do not reinstall local PROD ZIPs, repeat the initial retrofit, or restore the
candidate automatically. User-managed CurseForge installation is the next step.
All six DEV roots and private settings remain unchanged by the handover.

```powershell
python -B scripts/install_dual_distribution.py --client-root 'C:/Program Files (x86)/World of Warcraft/_classic_beta_' --sources-root C:/Dev/WoW --artifacts C:/Temp/apogee-dual-UNIQUE --backup C:/Dev/WoW/local-install-backups/apogee-UNIQUE --previous-install C:/Dev/WoW/local-install-backups/PREVIOUS/transaction.json
```

Omit `--previous-install` only for fresh DEV installs or exact matching files.
`--inspect-only` validates without writes. For explicitly approved obsolete DEV
Lua files, repeat `--retire-file <exact-Dev-root/path.lua>`. Retirement requires
that each file is absent from the new package and matches the previous installed
receipt exactly. After the full verified backup and new writes, the central
installer moves only those files to `retired-files` inside the backup. Unknown
files are preserved. Rollback restores retired files from the verified original
backup and refuses a conflicting new user file at any retired path. Existing output/backup directories are
refused. `--initial-retrofit` remains historical migration tooling and must not be
used under the owner's current CurseForge-managed PROD policy.

The installer regenerates expected bytes and verifies the actual aggregate ZIPs.
It rejects unexpected runtime/asset overwrites, links/junctions and alternate
child TOCs. Differing documentation remains intact and is recorded in the receipt;
executable files and required assets match the package exactly. All scoped addon
files are backed up and byte-verified before writes. Unknown non-loader files
remain untouched. It does not open, import, copy or modify private SavedVariables;
only WTF/unrelated-addon filesystem metadata is observed for concurrent changes.
Enabled preferences remain untouched. The reviewed Forever build must match.
Routine DEV installation permits WoW to remain running and replaces each changed
file atomically after the verified backup. Do not reload, log out or switch addon
groups during the short installation transaction; the package as a whole is not
an atomic switch. Concurrent protected-state changes still stop validation and
retain the receipt/backup. Sharing violations fail without truncating the target;
failed staging files are retained for diagnosis. Legacy migration, retrofit and
rollback continue to require a closed client. The installer never operates WoW.

After a successful DEV install, the user reloads the UI. Existing Lua edits take
effect on reload. Receipts separately list new files and changed TOCs as discovery
changes: the local exported UI does not establish the native filesystem rescan
contract for Forever. Verify those changes after reload; if not discovered, the
user may need to restart. This activation uncertainty does not require closing
WoW before writing the DEV package. Never claim native acceptance from installation.

```powershell
python -B scripts/migrate_distribution.py rollback --backup C:/Dev/WoW/local-install-backups/apogee-UNIQUE
```

Rollback checks backup hashes, refuses newly edited candidate files, restores
overwritten bytes and moves added files outside AddOns into `rollback-added-files`
inside the backup. It deletes nothing. This is recovery, not the normal mode switch.

## Switch in WoW

For the current character, right-click **Apogee Forever** in AddOns and select
**Disable Group**, then right-click **Apogee Dev** and select **Enable Group**.
Reverse those choices for production.
Apply changes and reload the UI. Do not switch by manually calling LoadAddOn,
especially in combat. Merely toggling the marker checkbox does not toggle children.

The current Blizzard addon-list implementation supplies these group controls;
APHB adds no runtime/UI. Group metadata introduces no dependencies. Children remain
standalone, independently disableable and optional. One download still has
multiple addon entries, grouped by family.

Any enabled/loaded canonical child at the first decision selects PROD; mixed
selection leaves all DEV inactive. The session family stays fixed until reload.
Every Lua chunk checks admission; an opposite guarded family loaded later cannot
initialize gameplay. Missing API/GUID, restricted values, malformed metadata and
invalid shared state fail closed. DEV refuses any installed canonical child
without schema-1 safety metadata, even disabled, and reports inactivity.
It also rejects an installed legacy/malformed production APHB marker, preventing
an older single-addon release from silently coexisting with DEV gameplay.
An older CurseForge release overwriting the retrofit therefore blocks DEV until
a compatible PROD release is installed. Never silently repair PROD on a DEV install.

DEV saves start separately with defaults. There is no automatic import/read of
production settings; switching back uses the unchanged PROD stores. The lease is
not saved. Marker metadata is exactly X-Apogee-Distribution-Only=1 and
X-Apogee-Distribution-Schema=1. Keybinds still rejects legacy/malformed APHB.

## Evidence and limits

Current export 1.60.1.70170 documents C_AddOns.GetAddOnEnableState(name, character),
GetAddOnMetadata, GetNumAddOns, GetAddOnName and IsAddOnLoaded.
Blizzard_AddOnList/AddonList.lua uses UnitGUID("player") for current-character
selection, Group metadata for grouping, right-click SetEnabledAll for groups,
and ReloadUI after ordinary enable changes. AddOnConstantsDocumentation.lua
defines None=0, Some=1, All=2. The gate creates no frames, bindings or stores.

Mocked tests do not prove actual GUID availability before addon loading, native
loader timing, taint, secure input or in-game acceptance. Live checks must cover
login, both group switches/reloads, separate settings, both enabled selecting
PROD, inactive diagnostics and combat/input behavior. No game session is automated.

Actual CurseForge app testing requires an approved available compatible release.
Local ZIP installation is not that test; private/held uploads are not assumed
accessible. Its FAQ says Modified/Working Copy addons skip auto-updates, so check
production app status for release testing. DEV stays installed separately.
Native acceptance for the staged gameplay is recorded in native-acceptance.json.
Release1.0.0 was approved for exact Forever1.60.1 (upload ID17053/type88568), and
Actions verified identical downloaded CurseForge/GitHub ZIP bytes. See RELEASING.md
for the active publication workflow and required gates for future versions.
The staged PROD candidate is backed up outside AddOns. First CurseForge app
installation and later update/removal ownership tests remain
separate acceptance checks; published-byte verification does not establish them.

## October 1 complete DEV candidate

The all-class Auction candidate includes uniform class modules, conditional talent
stat handling, conflicting tooltip baseline rejection and connected group/browse
regressions. The default-off Heals threat stack remains pinned. All other child
pins are unchanged; their additional local merge commits have identical packaged
content. Retained child worktrees contain no uncommitted or unintegrated feature
changes relative to their canonical source branches. Native acceptance is pending.

Runtime patch-number differences do not expire features. Addons retain their
Forever interface/capability checks and family exclusion; missing required APIs
can prevent startup. The exact reviewed-build requirement belongs to export and
installation provenance, not a runtime patch-number kill switch. An observed
in-game shutdown still needs its actual message/context to identify its cause.


## Native Forever identity correction (October 1)

The owner's screenshot is a real Keybinds startup rejection, not a status label.
The fresh native export assigns WOW_PROJECT_ID = WOW_PROJECT_CAMELOT (18), while
five child adapters required project 1. Earlier patch-only tests held that stale
identity constant and missed the defect. The reviewed ProjectConstants base,
Camelot override and selecting TOC are now included in the authority hashes.

All six children now accept native Forever identity and/or their legacy Forever
identification without an exact-interface expiry. Native identity accepts older
and future version/interface metadata; mandatory API checks, other-family
rejection and DEV/PROD admission remain. Six child suites and generated client
regressions cover the native identity, interface revisions and missing APIs.
The new source regressions fail against all five old project-1 adapters.
Export/install provenance remains pinned; runtime version numbers do not expire
features. Native acceptance of the corrected package still requires owner testing.

## Stats replaces Auction in the production candidate

Stats is pinned to its hosted private baseline commit with five explicit file
hashes. Its one source chunk unconditionally returns. Both generated identities
receive the existing admission prefix and family metadata; no lexical identity
edits or saved-variable mappings are needed. The bundled logo uses family-local
TOC paths. The family inventory recognizes
canonical Stats alongside retained Tank and Auction identities.

PROD selects Heals, Keybinds, Group Alert, Essentials and Stats. DEV additionally
includes Tank and Auction. Workflow source checkouts include private Stats;
DISTRIBUTION_READ_TOKEN must have read access in both build environments before
hosted validation. Local CLI access does not prove that environment-token access.
The recorded token expiry also requires owner review before hosted builds.

This is package configuration, not a production release. Existing canonical
Auction folders are never removed by local tools. CurseForge update/removal
behavior and renewed native acceptance remain required before release.

## Stats gameplay promotion

Stats now pins the owner-accepted role-aware tooltip implementation. Its three
private-namespace chunks are gated; unnamed UI frames and session-only role state
introduce no saved-variable or lexical identity mappings. The central generated
suite runs the pinned child's Lua regressions against both families. Native role
assignments override fallback selection; damage weapons compare DPS first, caster
weapons stay stat-first, and tank shield layouts are protected.

## October 4 Stats equipment audit acceptance

The owner reports testing the installed Stats audit corrections and explicitly
approves GitHub integration and CurseForge deployment. The candidate pins merged
Stats commit `aecb5fbf9f08b857ffec5fbabe059c5703f3413b`. Its throughput-first
caster/healer policy, tank Defense and separate block stats, uncertain alias
handling, required weapon DPS and skill-change refresh are covered by the child
regressions against both generated families. All 155 installed DEV Lua hashes
match the candidate and receipt at
`C:/Dev/WoW/local-install-backups/apogee-stats-policy-18c7f80-20261004/transaction.json`.
The acceptance record retains unchanged sibling coverage. Generated PROD is the
counterpart of the accepted sources; separate PROD and CurseForge-client testing
are not claimed.

## October 4 Keybinds learned-rank recovery DEV candidate

Keybinds pins reviewed commit `9123fe23d092769c3cf466859eb20e1fd5a852e9`.
Saved spell assignments whose former rank is no longer learned recover through
the current active spell family, including talent overrides. Exact learned ranks
remain explicit choices. The child regression and existing talent-override spec
pass against both generated families, including key/HUD routing, saved-choice
preservation, exclusions and combat-deferred refresh. All sibling pins, runtime
transforms and loader contracts are unchanged.

Full local distribution validation passed against the matching Forever
1.60.1.70205 export. DEV-only installation is recorded at
`C:/Dev/WoW/local-install-backups/apogee-keybinds-rank-9123fe2-20261004/transaction.json`;
the verified backup retains every previously managed DEV file. All 188 installed
package-file hashes and all 155 generated DEV Lua hashes match. The 111 existing
PROD addon files are byte-identical before and after installation. Private saves,
enable preferences and differing local documentation remain untouched.

Only Keybinds DEV `Actions/Identity.lua` and the distribution DEV marker's version
TOC changed. The owner subsequently reports "that fixed it" for the installed
level-25 Vanguard Charge fix. This accepts the reported Charge failure only;
broader new gameplay checks, PROD testing and CurseForge-client testing are not
claimed. `native-acceptance.json` updates the changed Keybinds Lua hash in each
generated family and preserves prior acceptance for all unchanged runtime.

The owner authorizes GitHub push and merge so this fix is included in the next
deployment. The reviewed source pin remains the exact installed candidate.
This request does not authorize a release, deployment, tag or further local
installation. The ordinary release-preparation and final-commit hosted gates
still apply before any separately authorized publication.

## October 4 reviewed-build warning correction

The central DEV candidate now pins Heals
`f81fa69ddbd60beb04495fab7f1266bad6e4f6df`, Keybinds
`c15d46d652c676b6208031150c65b719ec391eba`, and Group Alert
`f1781c9dd3f88b5512205bd5cce1f5e74f503c6a`. Each changes its stale warning
comparison to the reviewed Forever build 1.60.1.70205. The matching local export
and all three child suites pass. Group Alert's source export record was refreshed
after contract review; the child pins retain the reviewed documentation and
regressions. Existing package inventories, sibling pins, identity transforms,
loaders and capability guards remain unchanged.

The generated client regression first failed against all six prior PROD/DEV
client adapters. Both generated families now verify quiet startup on the build
recorded in the central lock, warnings for the next build, cross-family rejection,
revision tolerance and required-API failures. Full central validation passed.
The owner subsequently confirmed after DEV reload: "Yes, all three stopped and
everything works". Native acceptance advances only the three changed client
adapters; prior accepted Charge behavior and unchanged sibling runtime retain
their acceptance. All 155 installed DEV Lua hashes were verified again against
the candidate and receipt. Separate PROD and CurseForge-client testing are not
claimed.

DEV-only installation is recorded at
`C:/Dev/WoW/local-install-backups/apogee-reviewed-build-70205-20261004/transaction.json`.
Only the three DEV `Core/Client.lua` files changed. All 188 installed package
files, 155 generated DEV Lua files and 219 backed-up files were byte-verified;
111 PROD files remained unchanged. Private saves, addon enable preferences and
31 differing local documentation files were preserved. There are no TOC or file
discovery changes. No game operation or PROD installation was performed.

The owner requests CurseForge deployment and authorizes the necessary GitHub
integration and preparation of release 1.14.2. Exact source pins remain unchanged
from the installed candidate. The release contains Charge rank recovery and the
three reviewed-build warning corrections. Publication still requires successful
hosted test, aggregate and exact-version preflight checks on the final preparation
commit, review of its exact package and notes, and immediate production-tag
approval. Version preparation does not trigger another local installation.

## October 5 Keybinds Shift keyboard DEV candidate

Keybinds pins reviewed commit `41b476ace10a965a24d65685e18d7a54169b852a`.
Its 15 keyboard slots claim priority Shift aliases to the same secure action,
including existing native Shift bindings. The 30 saved slots remain unchanged;
mouse-button and wheel modifier actions retain their independent assignments.
The generated PROD and DEV suites run the pinned Shift regression alongside
spell-rank and talent-override checks, covering combat deferral, layout changes,
manual/default actions, macro modifiers, mouse isolation and override rollback.
Sibling pins, admission guards, identity transforms and loader schemas are unchanged.

Full central validation passed against the matching Forever 1.60.1.70205 export.
DEV-only installation is recorded at
`C:/Dev/WoW/local-install-backups/apogee-keybinds-shift-41b476a-20261005/transaction.json`;
packages and aggregate evidence are under
`C:/Temp/apogee-keybinds-shift-validation-20261005`.
All 188 installed package files, 155 generated DEV Lua files and 219 backed-up
files were byte-verified; all 111 canonical PROD files remained unchanged.
Private saves, enable preferences and 31 differing documentation files were preserved.
Only Keybinds DEV `Actions/Secure.lua` and the DEV marker version TOC changed.

The user must reload with the complete DEV family enabled and verify Shift+1,
other keyboard aliases and unchanged mouse/wheel modifier actions. The changed
marker TOC is a discovery change; if reload does not discover it, a user restart
may be needed. No game operation, PROD installation or publication was performed.
Native acceptance remains pending; the prior acceptance record is not advanced.

The owner subsequently confirms after reload that the Shift change is all working
correctly. All 155 installed DEV runtime hashes were reverified against this
receipt and candidate. Native acceptance advances only Keybinds
`Actions/Secure.lua` in each generated family and retains all unchanged coverage.
The owner authorizes GitHub integration so the exact pinned source is consumed
by the next CurseForge deployment; no new release or publication is requested.
Separate PROD and CurseForge-client testing are not claimed.

## October 5 Keybinds ready-highlight DEV candidate

Keybinds pins reviewed commit `379c36ded8d0f499f46f053b0baf9e70f2148885`.
The per-spell right-click option Highlight when ready enables a pulsing green
border and glow when cooldown, resources and applicable range checks confirm
readiness. Missing or restricted data stays quiet. Hidden spell art and the
queued-action indicator retain precedence. The generated PROD and DEV suites
run the pinned ready-highlight regression alongside Shift, learned-rank and
talent-override checks. Sibling pins, transforms and loader metadata are unchanged.

Full central validation passed against the matching Forever 1.60.1.70205 export.
Artifacts and verification are at
`C:/Temp/apogee-keybinds-ready-validation-20261005`. DEV-only installation used
the latest Heals revert receipt and is recorded at
`C:/Dev/WoW/local-install-backups/apogee-keybinds-ready-379c36d-20261005/transaction.json`.
All 188 installed package files, 155 DEV Lua files and 219 backed-up files were
byte-verified; all 111 canonical PROD files remained unchanged. Private saves,
enable preferences and 31 differing local documentation files were preserved.
Only Keybinds DEV Actions/Defaults.lua, UI/Cooldowns.lua, UI/Hud.lua and
UI/Widgets.lua changed. There are no TOC or file discovery changes.

Reload with the complete DEV family enabled, then enable Highlight when ready
from a spell icon's right-click menu. Verify the effect appears when ready and
disappears on cooldown, insufficient resources and out-of-range targets. Check
persistence and combat behavior in the client. Native acceptance remains pending;
the prior acceptance record is unchanged. No game operation, PROD installation,
push, integration or publication was performed.

## October 5 Keybinds self-buff reminder DEV candidate

Keybinds advances to reviewed commit `dbe93d829daa1b80395751a2d1127a67f12e2a2f`.
The explicit Self-buff reminder (out of combat) right-click mode highlights only
when the player's buff is confirmed missing and readiness/resource checks pass.
It performs no combat aura queries and fails closed on unavailable or restricted
observations. Name-based aura lookup recognizes different ranks of the same buff.
Ordinary Highlight when ready behavior and existing HUD visibility are retained.
The new pinned regression passes against both generated families, covering
resources, cooldown, present/missing ranks, combat, restricted data, persistence,
default slots and ordinary-mode independence. Sibling pins are unchanged.

Full central validation passed against Forever 1.60.1.70205. Evidence is under
`C:/Temp/apogee-keybinds-self-buff-validation-20261005`; the DEV-only transaction
is `C:/Dev/WoW/local-install-backups/apogee-keybinds-self-buff-dbe93d8-20261005/transaction.json`.
It chains from the previous ready-highlight receipt. All 188 package files,
155 DEV Lua files and 219 backed-up files were byte-verified; 111 PROD files
remain unchanged. Private saves, enable preferences and 31 differing local
documentation files are preserved. Four Keybinds DEV Lua files changed:
Actions/Defaults.lua, Core/Client.lua, UI/Cooldowns.lua and UI/Hud.lua. There are
no loader or discovery changes.

Reload with the complete DEV family enabled and select the self-buff reminder
mode on the desired spell. Native checks remain pending for buff application,
expiration, combat suppression, resource gating and persisted selection. Existing
HUD hiding settings still apply. Native acceptance was not advanced; no game
operation, PROD installation, push, integration or publication was performed.

The owner subsequently reports "it all works" after testing the ready highlight
and self-buff reminder, and authorizes GitHub integration for future CurseForge
consumption. All 155 installed DEV Lua hashes were reverified against the receipt
and candidate. Native acceptance advances only the five changed Keybinds runtime
files across the two generated families; sibling acceptance remains unchanged.
The preceding Heals change and exact revert have no net candidate/runtime diff
and receive no new acceptance here. Separate PROD/CurseForge-client testing is
not claimed. No release, version bump, tag or publication is authorized by this
integration request.

The owner subsequently confirms all current work is functioning in game and
requests CurseForge deployment. Release 1.14.3 includes the accepted Shift
keyboard fix, ready highlight and explicit out-of-combat self-buff reminder.
Heals canonical main has the same tree as its existing pin; the recent rejected
Boosted Rest experiment was exactly reverted and is not included. Source pins
and accepted runtime bytes remain unchanged. Version preparation uses the
documented helper; final-main test, aggregate and exact Forever version gates
precede the single production-tag publication path.

## October 10 Keybinds default-spell DEV candidate

Keybinds pins reviewed commit `e911a536890a9b0d59223191b943721046e2dced`.
Priest and Paladin empty slots no longer receive automatic spell assignments;
Warrior defaults and saved assignments remain. Keybinds also refreshes its
reviewed-build warning baseline to 70338. Sibling source pins, runtime, transforms
and admission schema remain unchanged. Heals and Group Alert retain their pinned
70205 warning baselines; generated tests independently verify their acceptance of
the current 70338 installer build without suppressing those warnings.

All eight central loading-safety export hashes are unchanged in the owner's fresh
1.60.1.70338 export. Exact current installation provenance advances to this build;
historical locks are preserved. Full central validation passed, including the
Priest/Paladin regression against both generated identities. Evidence and packages
are under `C:/Temp/apogee-keybinds-defaults-validation-20261010`.

DEV-only installation chains from the latest self-buff receipt and is recorded at
`C:/Dev/WoW/local-install-backups/apogee-keybinds-defaults-e911a53-20261010/transaction.json`.
All 188 installed package files, 155 generated DEV Lua files and 219 backed-up files
were independently byte-verified. All 111 canonical PROD files remain unchanged;
private saves, enable preferences and 31 differing local documentation files are
preserved. Only Keybinds DEV Actions/Defaults.lua, Core/Client.lua and the DEV marker
version TOC changed. No game operation, PROD installation or publication occurred.

Reload with the complete DEV family enabled and verify Priest/Paladin empty slots,
manual saved assignments and unchanged Warrior defaults. The marker TOC is a
discovery change; if reload does not discover it, a user restart may be needed.
Native acceptance remains pending and its record is unchanged.

## October 10 shared Settings parent DEV candidate

Five independent settings owners share a native parent: Apogee in PROD and
Apogee DEV in DEV. Loaded settings pages appear as Auction, Dungeons (Group Alert),
Essentials, Heals and Keybinds. Auction remains DEV-only under the existing public
selection. Tank and Stats have no settings page and their pins are unchanged.
The marker remains zero-runtime. There are no new loader chunks or saved variables.

Reviewed immutable pins are Heals `5ba1d9716e9ba92e344670cee36313de2b01ea66`,
Keybinds `fab87a527b1408732dae386475651871badd94f6`, Group Alert
`eb306ea6a3c4c5c9c82d0975e47d8cff9ff69d51`, Essentials
`5f9393c4b3120001dde5c1f7d12c5845d1af49e3`, and Auction
`64aaa9cb7c706cbb4d2eb8ec82df77bd3494e4ed`. Each uses the existing settings module
and the session-only schema-1 ApogeeSettingsRegistry. The exact lexical mapping
isolates it as ApogeeDevSettingsRegistry in those five owners only. Native category
IDs stay on each child's existing open/settings path. Malformed shared state is
preserved and rejected; absent subcategory APIs retain standalone compatibility.

Full central validation passed, including generated settings regressions covering
120 load orders per family, sole loaded owners, repeated creation, malformed
registries, child IDs, Auction setting ownership, compatibility fallback, denied
chunks and family isolation. The same regression fails against the prior packages.
Matching 70338 Settings sources are recorded in the central export authority.
Heals, Group Alert and Essentials also advance their reviewed warning baselines.

Artifacts are at `C:/Temp/apogee-shared-settings-validation-20261010`. The DEV-only
installation chains from the preceding Keybinds defaults receipt and is recorded
at `C:/Dev/WoW/local-install-backups/apogee-shared-settings-20261010/transaction.json`.
All 188 installed package files, 155 DEV Lua files and 219 backup files were
independently byte-verified; all 111 PROD files remain unchanged. Private saves,
enable preferences and 31 differing local documentation files are preserved.
Eight existing Lua files and Heals' export record changed. There are no new files
or TOC discovery changes. No game operation, PROD installation or publication occurred.

Start or reload with the complete DEV family enabled and inspect Settings > AddOns >
Apogee DEV. Verify the expected loaded child pages, their controls and direct-open
paths. Native appearance, defaults behavior and taint acceptance remain pending;
the prior native-acceptance record is unchanged. No push or merge is authorized
for this new candidate.

## October 10 compact Keybinds settings correction

Keybinds advances to reviewed pin `9b6ca9f47a0b79c4ae22807e7692b1b947891fa2`.
The compact settings controls now attach directly to the canvas, removing the
unnecessary far-right scrollbar while preserving the shared parent, settings,
layout and Defaults button. All six sibling pins are unchanged.

Full central validation passed, including the updated settings regression on
both generated families and the existing shared-parent/load-order suite. Evidence
is under `C:/Temp/apogee-keybinds-settings-scrollbar-validation-20261010`.
The DEV-only receipt is
`C:/Dev/WoW/local-install-backups/apogee-keybinds-settings-scrollbar-9b6ca9f-20261010/transaction.json`,
chained from the preceding shared-settings installation.

Only ApogeeKeybindsDev/UI/Settings.lua changed. All 188 installed package files,
155 DEV Lua files and 219 backups were independently verified; all 111 canonical
PROD files remain unchanged. Private saves, enable preferences and 31 differing
local documentation files are preserved. There are no discovery changes. Reload
and verify the Keybinds settings page in game; native acceptance remains pending.
No game operation, PROD installation, push, merge or publication was performed.

## October 10 settings typography consistency

The five settings owners use native large gold titles, small white labels,
muted small help text and gray unavailable labels. The shared parent has the
same dark backdrop as its children. Dungeons uses matching native tabs with a
gold selected underline and gold section/list selection text. Its displayed
header is Apogee Dungeons; the exact DEV string mapping appends DEV. Technical
Group Alert addon, saved-variable and slash identities remain unchanged.
The changed Core/UI ListButton helper is settings-only; HUD helpers retain their
existing styling. Essentials' learned-list help/status text is muted consistently.

Reviewed pins are Keybinds `12790011110c0b95737366d0f683daaa83948e47`, Heals
`b14f4afbd361a25198a9142dabcf764d51879fc1`, Group Alert
`afc55343c2931f70f9f86a2d2831ec6e8070409a`, Essentials
`8fd1d9a196003f5981692bc392e069ec53388c2b`, and Auction
`040b608b51bacb4f50653ee01de9bd4bc562a117`. Tank, Stats and public selection
are unchanged. The fresh native FontStyles.xml is included in API authority.

Full central validation passed. Generated tests verify parent/title/help styles,
disabled label colors, native Dungeons tabs and list colors across 120 load orders
per family, together with existing isolation, settings and gameplay regressions.
The exact Dungeons label transform preserves comments and unrelated prose.
Evidence is at `C:/Temp/apogee-settings-typography-validation-20261010`.

DEV-only installation chains from the scrollbar correction receipt and is recorded
at `C:/Dev/WoW/local-install-backups/apogee-settings-typography-20261010/transaction.json`.
All 188 installed package files, 155 DEV Lua files and 219 backups were independently
verified; all 111 PROD files remain unchanged. Private saves, enable preferences
and 31 differing local documentation files are preserved. Seven existing Lua files
changed, with no new files or TOC discovery changes. Reload and inspect settings
appearance, tab switching and unavailable controls in game. Native acceptance is
pending. No game operation, PROD install, push, merge or publication was performed.

## October 11 self-buff reminder combat carry

Keybinds pins `c7b30575d3c6bc83e95032b18bd7e5d314f1ebc4`. A confirmed missing
out-of-combat self buff can retain its reminder through combat, subject to
readiness and visibility. A readable successful player cast of the matching known
spell family acknowledges that reminder until combat ends. Failed, interrupted,
unrelated, pet and restricted observations do not acknowledge it. Unknown or
present pre-combat state stays quiet. No combat aura queries are introduced.
All six sibling source pins, loader identities and transforms remain unchanged.

Full local central validation passed, including the updated pinned self-buff
regression in both generated families and prior settings/gameplay checks.
Evidence is under `C:/Temp/apogee-self-buff-combat-validation-20261011`.
DEV-only installation chains from the typography receipt and is recorded at
`C:/Dev/WoW/local-install-backups/apogee-self-buff-combat-c7b3057-20261011/transaction.json`.
All 188 installed package files, 155 DEV Lua files and 219 backup files were
independently verified. All 111 PROD files remain unchanged; private saves,
enable preferences and 31 differing local documentation files are preserved.
Only the Keybinds DEV bootstrap and UI/Hud.lua changed, with no discovery changes.

Reload with the complete DEV family enabled and verify combat carry and readable
successful-cast dismissal in game. Restricted cast data cannot acknowledge the
reminder; native behavior remains pending and acceptance was not advanced.
No game operation, PROD installation, push, merge or publication was performed.

## October 11 ignore GCD in Keybinds visuals

Keybinds pins `0917183c620b8eb5ee1a6aec88f81678aa564d16`. Spell dimming, hiding,
countdowns and readiness/self-buff cues ignore the global cooldown while retaining
individual cooldown and charge behavior. Public event-only isOnGCD classification
is captured for learned/base spell IDs; native duration objects request ignoreGCD.
Unknown and restricted observations retain conservative handling. No new loader or
identity is introduced; all six sibling pins and transforms remain unchanged.

Full central validation passed, including new gcd_spec.lua and updated
cooldowns_spec.lua against both generated families. Coverage includes restricted
timing, real cooldowns, charges, hiding, readiness/self buffs and cache resets.
Artifacts are under `C:/Temp/apogee-keybinds-gcd-validation-20261011`.
DEV-only installation chains from the combat self-buff receipt and is recorded at
`C:/Dev/WoW/local-install-backups/apogee-keybinds-gcd-0917183-20261011/transaction.json`.

All 188 installed package files, 155 DEV Lua files and 219 backups were independently
verified; all 111 canonical PROD files remain unchanged. Private saves, enable
preferences and 31 differing local documentation files are preserved. Only Keybinds
DEV bootstrap and UI/Cooldowns.lua changed; there are no discovery changes.
Reload and verify ordinary GCDs no longer dim/hide/count down or suppress readiness,
while real spell cooldowns remain visible. Native acceptance is pending.
No game operation, PROD installation, push, merge or publication was performed.

## October 11 additional Defensive Warrior defaults

Keybinds pins `0e81416cadc693a8963f0e087dcb1b85c003746a`. Defensive Warrior
empty slots gain learned-spell defaults: 5 Intimidating Shout (5246), R Disarm
(676), T Forever Victory Rush (402927), X Last Stand (12975), C Shield Wall (871),
and Ctrl+Mouse4 Concussion Blow (12809). Saved assignments retain priority.
Z, other stances/classes, six sibling pins and runtime transforms are unchanged.

Full central validation passed, including defensive_extra_defaults_spec.lua
against both generated families: learned-only gating, saved macro priority,
combat stance transitions and class isolation. Evidence is under
`C:/Temp/apogee-defensive-defaults-validation-20261011`.
The DEV-only install chains from the GCD receipt and is recorded at
`C:/Dev/WoW/local-install-backups/apogee-defensive-defaults-0e81416-20261011/transaction.json`.

Only Keybinds DEV Actions/Defaults.lua changed. All 188 package files, 155 DEV Lua
files and 219 backups were independently verified; 111 PROD files remain unchanged.
Private saves, enable preferences and 31 differing local documentation files are
preserved. No discovery changes occurred. Reload and test learned spells on empty
Defensive slots in game; native acceptance remains pending. No game operation,
PROD installation, push, merge or publication was performed.

## October 11 friendly-player target buff suggestions

Heals pins `74f238c7fa902c6155ef2b1514807fdfa9642433`. Target-buff scanning now
requires public UnitIsPlayer true alongside the existing friendly/assist predicate.
NPCs, pets, hostile/dead and unknown/restricted player status produce no target-buff
suggestions. Party/self buffs, target health and cleansing retain their behavior.
All six sibling pins, identity transforms and loader inventories are unchanged.

Full central validation passed, including the pinned target_support_spec.lua and
class_integration_spec.lua against both generated families. The existing child
runtime loader is adapted to the selected family for these regressions. Artifacts
are under `C:/Temp/apogee-heals-target-players-validation-20261011`.
DEV-only installation chains from the Defensive defaults receipt and is recorded
at `C:/Dev/WoW/local-install-backups/apogee-heals-target-players-74f238c-20261011/transaction.json`.

Only ApogeeHealsDev/Buffs/Runtime.lua changed. All 188 package files, 155 DEV Lua
files and 219 backups were independently verified; all 111 PROD files remain
unchanged. Private saves, enable preferences and 31 differing local documentation
files are preserved. There are no discovery changes. Start/reload and verify target
buff suggestions on friendly players versus NPCs/pets in game. Native acceptance
remains pending. No game operation, PROD install, push, merge or publication occurred.

## October 11 Heals and Keybinds minimap consistency

Keybinds pins `4cfbea4775ae25d7dc583e3a0efeaf6a7fa9b4b7` and Heals pins
`6c0b712a602f699c5e0e96a493cda7e19dd7d7c7`. Their minimap tooltips share anchor,
colors and three action lines. Right-click opens each child's settings; right-button
drag moves either minimap button with click suppression after dragging. Keybinds
mouse-up cleanup preserves the session-only movement contract and combat lock.
Other five child pins, family transforms and public selection are unchanged.

Full central validation passed, including both pinned minimap specs and Keybinds
geometry against PROD and DEV. The geometry fixture's explicit default addon name
is adapted only inside the DEV test harness; runtime identity maps are unchanged.
Heals tooltip assertions use the generated family display label. Evidence is at
`C:/Temp/apogee-minimap-consistency-validation-20261011-r2`.

DEV-only installation chains from the target-player buff receipt and is recorded
at `C:/Dev/WoW/local-install-backups/apogee-minimap-consistency-20261011/transaction.json`.
Only Heals DEV UI/Minimap.lua and Keybinds DEV UI/Minimap.lua changed. All 188 package
files, 155 DEV Lua files and 219 backups were independently verified; all 111 PROD
files remain unchanged. Private saves, enable preferences and 31 differing local
documentation files are preserved. No discovery changes occurred. Reload and verify
both tooltips, right-click settings and right-button drag in game. Native acceptance
is pending. No game operation, PROD install, push, merge or publication occurred.

## October 11 owner acceptance and release request

The owner explicitly confirms "Yes, tested and working" for the latest installed
DEV changes, including settings pages, combat reminders/GCD behavior, defaults,
target buffs and both minimap buttons, and requests all work merged and deployed
to CurseForge. All 155 current DEV Lua files were reverified against the latest
minimap receipt and candidate. Native acceptance now records these exact runtime
hashes and the generated PROD counterpart. Separate PROD and CurseForge-client
testing are not claimed. Historical follow-up evidence remains intact.

Release 1.14.4 is the next patch after the published 1.14.3. Child and central
integration, final-main hosted test/aggregate/version checks, exact package review
and immediate production-tag approval precede publication. No additional local
installation is implied by version preparation.

## October 13 Battle Shout in all stances

Keybinds pins `bfff13ae530417da0f5a85bf82ca131e3dfbfc6b`. Empty Warrior F
slots default to the highest learned Battle Shout in every stance. Saved
assignments and per-stance weapon attachments retain priority and isolation.
Child test-all and full central test-local passed against Forever 1.60.1.70338 /
16001, including the stance regression against generated PROD and DEV families.
Evidence: `C:/Temp/apogee-battle-shout-20261013/validation`.

DEV-only receipt: `C:/Dev/WoW/local-install-backups/apogee-battle-shout-20261013/transaction.json`,
chained from the five-addon-update October 12 receipt. Independently verified
114 installed package files, 135 backup files and 111 unchanged PROD files.
Only Keybinds DEV Actions/Defaults.lua and the DEV marker TOC changed. Differing
documentation and private saves remain preserved. User reload is required;
marker TOC discovery may require a restart if reload does not discover it.
Native acceptance is pending and historical evidence is retained. No game
operation, push, main integration, release or PROD installation occurred.

## October 13 Battle Shout reminder default

Keybinds pins child commit `68d418d` (full immutable revision in candidate.lock.json).
Battle Shout defaults to self-buff reminder for automatic and manual assignments,
all stances and learned ranks. Explicit false and ordinary ready-highlight modes
win; historical absent choices adopt the new default because old off choices
were stored as nil. Spell classification occurs during action compilation, not
HUD refresh. Child test-all and full central test-local passed with matching
Forever 1.60.1.70338 / 16001 export, including generated PROD/DEV reminder tests.
Evidence: C:/Temp/apogee-battle-shout-20261013/reminder-validation.

DEV receipt: C:/Dev/WoW/local-install-backups/apogee-shout-reminder-20261013/transaction.json,
chained from apogee-battle-shout-20261013. Independently verified 114 package files,
135 backups and 111 unchanged PROD files. Three Keybinds DEV Lua files changed:
Actions/Defaults.lua, Actions/Identity.lua and UI/Hud.lua. No discovery changes.
User reload and native acceptance remain pending. No private-save access, game
operation, push, main integration or release occurred.

## October 13 Up Arrow Auto Run

Essentials pins `304448a` (full immutable revision in candidate.lock.json).
Login/reload assigns UP to native TOGGLEAUTORUN with existing context checks,
combat deferral and conditional rollback. Other Auto Run shortcuts and later
session edits remain. The read-only defaults reference includes the shortcut.
Verified Bindings_Camelot.xml in the matching Forever 1.60.1.70338 / 16001 export.
Full child test-local and central test-local passed. Evidence:
C:/Temp/apogee-autorun-20261013/validation and child-checks.log.

DEV receipt: C:/Dev/WoW/local-install-backups/apogee-autorun-20261013/transaction.json,
chained from apogee-shout-reminder-20261013. Independently verified 114 package
files, 135 backups and 111 unchanged PROD files. Only Essentials DEV
Core/LoginDefaults.lua and Core/Settings.lua changed; no discovery changes.
User reload and native input acceptance remain pending. No game operation,
private-save access, push, main integration or release occurred.

## October 17 Forever 70450 review and release preparation

The owner exported the updated client and confirmed the previously installed
Battle Shout all-stance/reminder and Up Arrow Auto Run behavior works. Matching
Forever 1.60.1.70450 / 16001 exports were reviewed before updating provenance.
Current-contract review found no required gameplay adapter changes. Only four
Core/Client.lua reviewed-build warnings change at runtime relative to the last
installed candidate. Reviewed source pins: Heals de4c53f, Keybinds 644fefb,
Group Alert f289b6a, Essentials 6901e39; Stats stays at its existing immutable pin.
Full revisions/hashes live only in candidate.lock.json.

All five child suites passed, including Heals actual exported-source contracts,
plus 18 workspace tests and full central validation (74 Python tests and generated
Lua checks). Evidence: C:/Temp/apogee-api-20261017/validation and sibling check logs.
The central exact build allowlist now includes 70450 and rejects neighboring
unreviewed builds. Generated warning checks cover both families for all four
warning-bearing children. Export review hashes are recorded in the owning repos;
additional local inventory is C:/Temp/apogee-api-20261017/export-review.json.

DEV install receipt: C:/Dev/WoW/local-install-backups/apogee-70450-20261017-r2/transaction.json.
The first attempt stopped at prepared status because protected metadata changed
during backup; addon bytes were independently confirmed unchanged before retry.
Both backups are retained. Successful retry independently verified 114 installed
package files, 135 backups and 111 unchanged PROD files. Four client modules and
Heals export metadata changed, with no discovery changes. Private save contents
and enabled preferences were never opened or modified. User reload/startup
acceptance for these exact updated bytes is pending separately from earlier
feature acceptance.

Latest remote release is v1.14.5; proposed next patch is 1.14.6. Native acceptance,
approved child/central integration, prepare-release.ps1 from synchronized main,
exact-final-main hosted test/aggregate/version checks, and explicit production-tag
approval still gate publication. Required secret entries exist (source-read
entries updated October 2); their current expiry/access are not established by
metadata. No push, main integration, tag, release or publication was performed.

October 17 acceptance follow-up: owner reloaded the refreshed DEV candidate and
confirmed everything works. Exact installed Lua bytes were independently reverified;
native-acceptance.json now records current DEV and generated PROD runtime hashes.
Offline publisher payload validation passes for proposed 1.14.6. Historical evidence
is retained. Push/integration, final-main hosted checks and tag approval remain pending.
