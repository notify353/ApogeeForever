# Classic Era archive comparison - October 25, 2026

Scope: inspect the installed Era.5 baseline for silent compatibility failures,
using the retained old Era addon as a reference and the fresh 1.15.9.70003 export
as authority. Four concrete display gaps were reproduced and corrected in
Era.6. This audit does not claim complete native acceptance or restore the old
addon's full feature set.

Archive: `C:/Dev/WoW/addon-archives/classic-era-apogee-2026-10-24` (275 files).
The archive is read-only reference material; none of its runtime or settings is
installed/imported. Fresh selecting TOCs are essential: the old Vanilla action
bar and Classic buff-frame TOCs remain on disk but predate the executable.

## Compatibility findings

| Area | Archived implementation / current evidence | Result |
| --- | --- | --- |
| Party and friendly-target debuff icons | APHB `PartyFrames/Auras.lua` reads public harmful aura records. Current Heals `PartyFrames/View.lua` requires the absent CustomAuraContainerTemplate. Fresh AuraUtil and TargetFrame confirm icon/dispelName records. | **Fixed:** private Era display, first eight icons, complete bounded scan, read-only out-of-combat tooltips, cleanup on replacement/death/preview/world changes. |
| Cleansing highlights | APHB `Reminders/CleanseData.lua` and `CleanseWatch.lua` use public dispel types and learned class spells. Current `Cleansing/Runtime.lua` creates secure actions but its glow requires the missing container. | **Fixed:** Era artwork reflects all scanned dispel types for learned player cleansing actions, including in combat. Secure spells/recipients stay fixed and shared. No pet action or old dynamic Cleanse Watch panel restored. |
| Combat fading: action-bar artwork | Archived Essentials `Fade/Runtime.lua` includes MainMenuBar. Fresh ActionBar Classic TOC selects MainMenuBar and MainActionBar as distinct roots. Current frame list includes only the latter. | **Fixed:** Era adds MainMenuBar to the ordinary fading/hover/restore list. |
| Combat fading: quest tracker | Shared tracker list names ObjectiveTrackerFrame; fresh UIPanels Classic TOC selects Vanilla/QuestLogFrame.xml defining QuestWatchFrame. Wrath WatchFrame is excluded. | **Fixed:** Era selects QuestWatchFrame; remains hidden during hover, preserves original alpha/visibility, handles late load and disable. |
| Warrior threat debuffs | Archived Tank `Core/Auras.lua`, `Threat/DebuffData.lua`; Era.5 already supplies public aura scanning for the current three warrior families. | Retained and retested: own Sunder ranks/stacks, Thunder Clap and Demoralizing Shout. Old all-class debuff catalogs are outside the current warrior-only baseline. |
| Healing, health/power and incoming heals | Old APHB `Core/UnitAPI.lua` / `PartyFrames/IncomingHeals.lua` use direct numeric values. Current native curves, status bars and heal prediction APIs occur in the fresh generated Unit contracts. | No concrete missing-contract defect found. Existing source/generated tests retained. Native incoming-heal coverage and cast timing still need user testing; declaration presence is not live acceptance. |
| Buffs, drinking and weapon upkeep | Archived APHB aura snapshots use public records; current Buffs/Drinking already use guarded public GetAuraDataByIndex scans. Fresh BuffFrame/AuraUtil provide matching field/tooltip contracts. | No additional concrete failure found. Existing out-of-combat reminder/learning policy retained; combat expiry inference is intentionally limited. |
| Keyboard, mouse, stances and spell drops | Archived Keybinds `Core/Client.lua` uses legacy tab/slot APIs. Current Era adapter already replaces modern spellbook paths and rejects pet/passive/unreadable cursor data. | No new adapter defect found. Source/generated Era tests exercise startup, ranks, cursor validation and actual exported secure code under mocks. Native input execution remains user-owned. |
| Chat and official Group Finder | Archived GroupAlert uses C_LFGList; the current Era.4 correction already retains the fresh Vanilla-style search/role/activity contracts. | Retained and retested. No auto-search, message sending or player-identity persistence introduced. Native availability/server results still require user testing. |
| Errors, camera, sound and login defaults | Archived Essentials supplies separate convenience features. Current Era.4 native-name suppression/default migration and CVar capability checks already address known client differences. | Retained and retested. No repeat choice reset, save import or enabled-state changes. Optional unsupported CVars remain individually unavailable. |
| Stats, loot/item advice, auction automation | Current Era lock deliberately excludes Stats; current tooltip/auction implementations require a separately reviewed redesign for Era. The five-folder archive is not an authority to re-enable those modern paths. | Still unavailable as documented in the initial Era design. No attempt to revive archived addons or weaken loading gates. |
| Other archive-only UI | Archived APHB README describes profiles, low-health sounds, HoT/shield displays, consumable HUD, automatic marking and the standalone Cleanse Watch panel. These are absent or substantially different in the current Forever baseline. | Feature gaps, not demonstrated failures of the installed Era implementation. Restoring them requires a separate scoped design review; no new profiles, automatic actions or pet cleansing added. |

## Implementation and protections

Heals pin: `e7e179ca2ee069e6973d7c1505f754cafb267638`.
`Era/PartyAuras.lua` is private and selected only by the Era TOC, before the
existing Era adapter/startup tail. It creates fixed artwork out of combat and
uses shared coalesced refreshes. It never derives secure actions from aura data
or changes protected layout in combat. The first eight debuffs are displayed;
all 64 permitted records are considered for cleansing, followed by a termination
probe. Restricted, failed or truncated reads clear artwork. Mouse motion enables
tooltips without intercepting clicks. Existing native-container behavior remains
available if a future separately reviewed Era provides it.

Essentials pin: `24eb82ccb120f4c01000438e23c6a12b606cbdd1`.
Two optional private frame-list settings select Era roots. The shared fade code
still uses its original lists when these settings are absent; no global aliases,
new preferences or behavior changes to the frozen Forever package.

Keybinds and GroupAlert source pins remain unchanged. Forever release/candidate
locks, gate, default builder and installed beta remain frozen. No push, main
integration, publication, game operation or private-save access occurred.

## Verification

- Verified client/executable and 78 selected fresh export references, including
  ActionBar/UIPanels selection, aura fields and native mouse-motion API.
- New party/cleanse regression failed on Era.5, then passed after the correction.
  Tests cover all five cleansing classes and warriors, exact secure recipients,
  combat construction guards, types beyond displayed slots, unknown/failed/capped
  scans, current tooltips, party removal, target changes, preview and world cleanup.
- New Era fading regression failed before the correction, then passed. It checks
  main-menu fade, hover, actual selected tracker, original-alpha restoration,
  hidden/late tracker handling, disable and unrelated-tracker isolation.
- Heals: 89 Lua parses / 56 specs; Essentials: 47 parses / 29 specs. Full central
  runner passed all 171 child specs, nine Era tests, 76 admission scenarios and
  four generated adapter tests, including the new helper in generated Heals.
- All 77 frozen Forever offline distribution tests passed. Rebuilt PROD and DEV
  ZIP hashes match frozen originals. Before installation, 1,477 Forever addon
  files, eight frozen repository files, 275 archived files and 113 Era.5 files
  were unchanged. Archive/source API-name scans were investigation leads only;
  unsupported-name hits were manually checked against existing private adapters
  and fresh native callers rather than treated as proof of a defect.
- Initial packaging correctly rejected placing another module after Era/Adapter.
  The load order was corrected; no distribution safeguard was weakened. The
  failed build log is retained alongside the successful full rerun.

Artifact: `Apogee-1.14.8-era.6-DEV.zip`, SHA-256
`313cc404fca46f8b65129288eb73c4ec4127cd48eb6a52bdb597e2e1f7947642`.

Evidence: `C:/Temp/apogee-era-20261024/archive-sweep-20261025/`, including before
hashes, task record, child logs, `validation-r2.log`, `validation-r2/packages`,
API-name investigation leads, preservation results and installation preview.

## Install and user acceptance

Preflight reports Era closed, eight writes, seven preserved README files and
the expected five DEV roots. Chain from the installed Era.5 receipt
`C:/Dev/WoW/local-install-backups/apogee-era-threat-debuffs-20261025/transaction.json`
using the central explicit Era target and a new external backup.

User checks: party/friendly-target harmful icons; cleanse highlights only for
types your learned spell removes; unchanged click recipient in combat; removal,
death, target change and reload cleanup; main-menu fade/hover; quest tracker
hiding/restoration. Also smoke-test healing/incoming heals, cast display, buffs,
bindings, Sunder, Group Finder and suppression. Offline tests do not establish
native timing, taint safety or complete feature parity with the archived addon.

## Verified installation

Era.6 installed October 25 after central preflight rechecked that the client was
closed. Latest receipt and rollback backup:
`C:/Dev/WoW/local-install-backups/apogee-era-archive-sweep-20261025/transaction.json`.
All eight writes verified. All 113 previous files were backed up; all 114
installed files match the new candidate plus preserved documentation (107 payload
receipt entries and seven README files). All 1,477 Forever addon files, eight
frozen repository files and 275 archived files remain unchanged. See the external
`install-verification.json` and install stdout/stderr. User acceptance is pending.
