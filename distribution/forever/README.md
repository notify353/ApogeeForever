## Own HoT local DEV test; current API review deferred - 2026-11-07

Candidate 1.14.15-dev.1 adds only the Heals own-caster Renew/Rejuvenation strip.
Owner explicitly authorized DEV installation and skipping the export refresh.
Source and generated behavior checks use the existing export as historical
reference. Source pins advance; the reviewed70790 client, executable hash and
244 reference hashes remain historical and unchanged. Installed70862 is not
claimed reviewed. Use the explicit deferred-review DEV option with the latest
receipt; native acceptance is pending. No Era/release selection changes.

## Focus spell re-follow - 2026-11-05

The candidate extends only focus-assisted spell inputs with an optional follow
attempt before the native cast, outside combat, on the same user input. Existing
follow/casting/range and editor guards apply. No automatic event/timer movement,
new loader entry or saved-data migration. The owner selected one eligible input
attempt after reload when follow status is unknown. The same244 source reference
hashes cover the added contracts; PlayerScript/Unit ownership includes Keybinds.
Native follow/movement/cast acceptance remains pending. Previous friendly-focus
targeting was reported working by the owner; this does not accept the new behavior.

## Friendly focus assist - 2026-11-05

Current candidate adds guarded native friendly-focus targeting in Keybinds and
retains the prepared hidden-damage change. No source is installed or published by
these pins. The same 244 API references cover secure button remapping, native
state drivers, macro dispatch and spell classification. Native in-game acceptance
remains pending, including focus transitions, reticles, attacks and cast outcomes.

## Incoming damage visibility - 2026-11-05

The owner reports dashes throughout combat on 70790 and requested hiding the
empty display. The current Forever candidate uses Essentials 0ee3f1896308cb5667e29144218f8e00eb6e9bc1
to hide empty/incomplete encounters while retaining valid percentages. The
244 API reference hashes are unchanged; only the reviewed source pin advances.
Era and immutable releases stay unchanged. Native visibility review is pending.

# Live Forever authority

The isolated future candidate now targets reviewed Forever **1.60.1.70790**,
Interface 16001, product `wowf`, directory `_forever_`, executable `Wow.exe`.
The frozen v1.14.9 selection and its beta authority are unchanged.

`api-evidence.json` records the executable hash and 244 unique exported source
files covering distribution, all five pinned children and embedded shared UI.
The future lock binds its canonical hash and the exact merged child revisions.
These central checks cover the current client; the children's retained standalone
beta checkers are historical and do not establish live-client authority.

Run from the distribution checkout with clean child checkouts at the lock pins:

```powershell
pwsh -NoProfile -File scripts/test-live-forever.ps1 `
  -ChildWorktrees C:/Temp/apogee-merged-child-checkouts `
  -ArtifactRoot C:/Temp/apogee-live-validation-NEW
```

This checks both matching exports, child tests, generated Era and Forever
PROD/DEV, loading safety, settings/binding preservation and historical rollback.
It never installs or publishes. The receipt records live authority separately
from native acceptance. See [candidate validation](../CANDIDATE_VALIDATION.md).

The live checker rejects a missing, stale or changed export, wrong executable,
wrong/inactive product, mismatched source pins and unsafe paths. It never falls
back to beta. The installation preflight recognizes the live executable, but
validation does not invoke an installer or authorize an installation.

## Launch source review, 2026-11-04

Exported from the running 70790 client at character selection under explicit
owner authorization. Active wowf metadata, executable version/hash and fresh
export agree. Of 243 existing references, 233 are unchanged and ten changed.
Nine changed files have retained beta bodies matching their exact prior hashes:

- UnitDocumentation now marks UNIT_COMBAT amount as secret. Essentials already
  checks canaccessvalue before type, comparison or arithmetic, and displays
  unknown totals after restricted input. Existing secret-value regressions cover
  this behavior. Damage percentages may therefore be unavailable in combat.
- PaperDollInfo adds documentation that imbue enchants take priority; signatures
  are unchanged. Camelot NameUtil now retains a name when surname parsing fails.
- Chat overrides add a Battle.net sub-icon; edit-box/util changes route title
  friends to character whispers. The actual fresh exported SendTellWithMessage
  and ExtractTellTarget pass the existing offline character-whisper contract:
  full spaced/hyphenated recipients, tank/heal drafts, no sending or BNet lookup.
- CombatLogProcessor caps traversal at the native message limit. Group Finder
  adjusts native row icon/level spacing; search/result contracts are unchanged.
- ActionBar TOC adds Camelot/ActionButtonUtilOverrides.lua, now included as the
  244th reference. It changes native unplaced-spell highlighting to the highest
  rank; no pinned Apogee runtime calls that override.

The prior matching Menu.lua body is unavailable. Current-contract review, rather
than a claimed full diff, verifies root AddMenuReleasedCallback and RemoveMenu:
the exact proxy is still passed before closing/removal, with an additional close
reason that the existing callback safely ignores.

No required gameplay adaptation was identified. All five source pins, Era and
historical selections remain unchanged. The owner explicitly requested skipping
in-game testing and publishing this launch compatibility release; new evidence
and release authorization retain nativeAccepted=false. Source review and mocks
do not establish native behavior, timing or taint acceptance.

## Source review, 2026-10-27

October 31 update: the owner refreshed the export after the 70707 update.
All 243 references postdate Wow.exe. Three of the prior 239 hashes changed:
SecretPredicates adds/tightens loss-of-control restrictions; Spell restricts
IsSpellCrowdControl secret arguments to untainted callers. Neither pinned Heals
nor Keybinds calls the affected APIs. Matching retained sources establish these
two diffs. Menu.lua has no retained matching previous body: current-contract
review confirms AddMenuReleasedCallback still receives the exact proxy before
Close/removal, preserving shared launcher's dismissal handling. No broader
old/new Menu diff or native acceptance is claimed.

Four newly reviewed sources bind instantQuestText to the native Camelot option
and establish the selected Mainline QuestFrame behavior through the TOCs.
The Era evidence separately includes its Classic and Vanilla quest-frame paths.
Both clients use "1" for immediate quest text. The existing public C_CVar
get/set contract remains unchanged. The two isolated candidates pin Essentials'
new login default; frozen beta and immutable release selections are unchanged.

The owner export postdates the installed executable. Comparing retained beta
source with matching recorded hashes identified five changed unique references:
UnitPopupSharedButtonMixins, Camelot Inspect and ClassTalents, Vanilla LFG parent,
and Blizzard_Menu/Menu.lua. Changes remove gamepad hints/focus handling or protect
menu resetters with securecallfunction; no incompatible Apogee-used contract was
identified. Native project identity remains WOW_PROJECT_CAMELOT (18). The earlier
240-reference inventory counted one generated-documentation TOC twice; this
inventory merges its ownership into one record.

All gameplay pins and generated package bytes are unchanged by this tooling
update. Era authority, lock and runtime remain separate and unchanged. On the
next client update, request a fresh owner export and review changed source before
changing evidence; hashes must not be refreshed merely to silence a failure.

## Remaining release gates

The 2026-10-29 owner-approved early-release policy in
[release selections](../releases/README.md) supersedes the earlier requirement
for complete native acceptance below for the exact prepared public package.
Fresh authority, automated tests and final tag approval still apply. The owner
export for70685 changes only the nameplate rarity-icon option among239 references.

Native owner testing of the exact candidate is still required, including secure
input, UI timing/taint and auction behavior. Name selection and source validation
cannot establish gameplay acceptance. Any test installation requires approval.
The release workflow still selects the frozen candidate. Final source selection,
version/preflight checks and immediate production-tag approval remain separate.

On this host, `test-local.ps1` stops at the historical beta metadata gate because
the current launcher metadata no longer supplies that reviewed beta build. This
is not a live-client validation result. The live runner passed the frozen package,
migration, publisher and rollback regression suites independently; it does not
claim a fresh beta installation check.
