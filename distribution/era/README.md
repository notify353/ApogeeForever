## Current capability policy - 2026-10-31

The current candidate uses Era 1.15.9.70576 authority and includes all five
components. Follow and Inspect now use their individual native requirements;
missing talent inspection no longer hides them. Essentials applies instant
quest text and A/D strafing at login/reload. See the current
[runtime policy](../RUNTIME_CAPABILITIES.md) and [release selections](../releases/README.md).
The earlier candidate assessments below describe their original limitations.

## Era.20 Stats candidate

Stats now joins the five-component Era package. English tooltip reading and a
separate paged auction backend retain shared evaluation and Forever behavior.
See [Stats design and acceptance](STATS.md). Installing the added folder requires
Era closed and a full restart; settings and enabled preferences are preserved.
The historical assessment below records why earlier candidates excluded Stats.

## Era.8 shared launcher candidate

Era.8 adds required Apogee UI shared support and one green minimap launcher.
Source/API/persistence/installation details and native checklist: LAUNCHER.md.
New support requires closed-client installation and full restart. The separate
future-launcher.lock.json prepares Forever source without changing frozen pins
or its installed beta. No publication or native acceptance is implied.

# Isolated Classic Era candidate

The owner approved isolated Era development on October 24, 2026, keeping the
last verified Forever beta unchanged. The beta ended; unavailable live Forever
validation is not a prerequisite for this separate target. The Forever checker
remains strict and is not bypassed or rewritten.

`candidate.lock.json` here is the only Era source selection: unpublished,
DEV-only, Classic Era 1.15.9.70003 / Interface 11509. The ordinary
`distribution/candidate.lock.json`, release lock, Forever family gate and default
build output remain frozen. Gameplay stays in the existing child repositories;
each `_Era.toc` loads a private adapter immediately before startup. No global API
replacement, archived addon or settings import is involved.

## Scope and authority

`api-evidence.json` fingerprints the reviewed executable and selected freshly exported
files. Build and install verify product, executable hash, reference hashes and
export timestamps. Fresh selecting TOCs matter: the export also contains stale
files from other versions. Do not treat those as authority.

| Feature | Candidate treatment | Evidence / change |
| --- | --- | --- |
| Healing, buffs, fixed party recipients, protected clicks | Shared gameplay retained | Fresh Unit, UnitAura, Spell and secure sources; private name adapter uses Era's first UnitName return, never realm as surname |
| Party debuffs and cleansing artwork | Era.6 private reader | Eight fixed debuff icons and learned player-spell highlights from public aura records; shared secure actions unchanged. See [archive sweep](ARCHIVE_SWEEP.md). |
| Spell drops and bindings | Small private adapters | Vanilla SpellBookFrame classic slots/tabs; preserve spell IDs and rank labels; no invented Forever override aliases; passive and pet spells excluded |
| Secure action execution | Retained and guarded | Fresh SecureTemplates and RestrictedAddOnEnvironment/SecureStateDriver execute in generated Keybinds tests; combat rebuilding deferred |
| Follow/Inspect/Talents strip | Entire strip omitted | Era InspectUI selection lacks native talent inspection; no shared behavior split |
| Chat recruitment / dungeon wording | Shared classifier and UI | ChatFrameUtil/filters and ChatInfo; separate activity namespace, explicit phrases retained |
| Tank threat-stack warrior debuffs | Era.5 private renderer | Fresh public aura records; player-owned Sunder/Thunder Clap/Demoralizing Shout, bounded scans and fixed preallocated icons. Forever native containers unchanged. |
| Official listings and activity discovery | Enabled from Era.3 through the shared guarded adapter | Fresh Vanilla UIParent loads VanillaStyle on demand; seven-argument search, activity/player records and remaining-role counts match shared contracts. Initial TOC-only assessment was incomplete. |
| Settings and conveniences | Shared with capability checks | Fresh Settings/Keybindings, Bindings_Vanilla and CVar settings sources; unsupported named CVars disable their own feature |
| Combat UI fading | Era.6 private frame selection | Includes fresh MainMenuBar artwork and selects QuestWatchFrame; shared hover/restore behavior retained. |
| Error suppression | Era.7 checked errors suppressed in and out of combat | Fresh UIErrorsFrame and GetGameMessageInfo; routine errors start checked, useful/unknown types visible. Existing choices and Era.4's once-only reset marker preserved; no new reset or Forever migration. See [scope correction](ERROR_SCOPE.md). |
| Stats and item/loot tooltip evaluation | Excluded; redesign review needed | Era tooltip selection uses OnTooltipSetItem; modern hyperlink/item-key readers absent from fresh generated contracts |
| Auction filtering/buyout selection | Excluded; redesign review needed | Modern AuctionHouseUI TOC permits cata/mists; Era uses separate AuctionUI |
| Loading / family safety | Era preamble plus unchanged family gate | Fresh project constants, AddOns enum, UnitGUID and current AddOnList; wrong client or ambiguous selection admits no gameplay |

Contract presence and mocked execution do not establish native availability,
timing, taint or gameplay acceptance. Optional capabilities still fail closed.

## Build and verify

From this owning distribution worktree, with clean child worktrees at the Era
lock commits and the owner's matching fresh export:

```powershell
pwsh -NoProfile -File scripts/test-era.ps1 `
  -ChildWorktrees C:/Temp/apogee-era-20261024 `
  -ArtifactRoot C:/Temp/apogee-era-validation-NEW
```

This parses child Lua, runs existing and Era specs, tests generated DEV code,
actual exported secure source under mocks, denial before side effects, exact
roots/identities, corrupt archives, stale/wrong authority, conflicting edits,
receipt scope, backup and reversible rollback. It also runs the existing Forever
offline distribution suites; it does not claim live Forever validation passed.
`-SkipFrozenRegression` is for a focused rerun after those unchanged suites passed.

## Installation and rollback

Initial Era installation requires explicit owner approval and a closed Era
client. Forever's standing installation authorization is not extended to this
new client. The central installer defaults to Forever; Era is explicit. Preview
is read-only and works while Era runs:

```powershell
python -B scripts/install_dual_distribution.py --target classic-era `
  --client-root 'C:/Program Files (x86)/World of Warcraft/_classic_era_' `
  --sources-root C:/Dev/WoW --artifacts <verified-packages-directory> `
  --backup <NEW-external-backup-directory> --inspect-only
```

After approval, omit `--inspect-only`. Updates require the last
Era `--previous-install <backup>/transaction.json` to recognize replaced bytes.
The installer admits four DEV children plus the inert marker, rebuilds expected
bytes from immutable pins, preserves edited documentation and unknown files,
refuses conflicting runtime edits or alternate loaders, backs up and verifies
writes, and stores an Era receipt. It never enables addons or reads/copies private
saves. Old archives are not recognized install sources.

Owner override (October 25): routine reviewed updates may run while Era is open
with explicit `--allow-running-era-update`. This requires a valid previous Era
receipt, exact installed runtime bytes, identical runtime file paths and unchanged
TOC metadata/load order (except Version). Initial installs, discovery changes and
rollback still require a closed client. The default remains closed-client unless
the explicit live-update option is supplied; the option cannot target Forever.

Era writes use atomic complete-file replacement, so an interrupted write leaves
either the old or new file bytes for verified rollback. A running client retains
its loaded code until the user reloads. After a completed live update use `/reload`;
the installer never operates the game, changes enable preferences or copies saves.

For explicitly approved recovery, close Era, then run:

```powershell
python -B scripts/era_distribution.py --rollback <transaction-backup-directory>
```

Rollback checks exact Era roots, unchanged installed bytes and verified backup.
Added files are retained outside AddOns rather than deleted. A fresh API export
is not required to undo a failed installation. Retain source worktrees, artifacts,
archives and backups until the owner chooses otherwise.

## Native acceptance required

User testing must cover first login/reload with only the Era DEV family chosen;
separate settings persistence/defaults; party changes and combat; friendly click
healing and buff reminders on fixed recipients; learned ranks, keyboard/mouse/
stance actions and combat edit deferral; chat matching and editable whisper
drafts; manual official search, completed/failed/empty results, role and level
filters, combat hiding, listing updates and whisper drafts; error visibility and explicit suppression; optional settings; tooltip
errors; and absence of taint/blocked-action messages. Verify excluded features
stay unavailable. Never operate the game from Codex.

If a core feature needs substantial shared gameplay changes, stop for review.
Future Forever release work requires its own fresh authority and native
acceptance. Era results cannot substitute for either.
