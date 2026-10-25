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

`api-evidence.json` fingerprints the reviewed executable and 46 freshly exported
files. Build and install verify product, executable hash, reference hashes and
export timestamps. Fresh selecting TOCs matter: the export also contains stale
files from other versions. Do not treat those as authority.

| Feature | Candidate treatment | Evidence / change |
| --- | --- | --- |
| Healing, buffs, fixed party recipients, protected clicks | Shared gameplay retained | Fresh Unit, UnitAura, Spell and secure sources; private name adapter uses Era's first UnitName return, never realm as surname |
| Spell drops and bindings | Small private adapters | Vanilla SpellBookFrame classic slots/tabs; preserve spell IDs and rank labels; no invented Forever override aliases; passive and pet spells excluded |
| Secure action execution | Retained and guarded | Fresh SecureTemplates and RestrictedAddOnEnvironment/SecureStateDriver execute in generated Keybinds tests; combat rebuilding deferred |
| Follow/Inspect/Talents strip | Entire strip omitted | Era InspectUI selection lacks native talent inspection; no shared behavior split |
| Chat recruitment / dungeon wording | Shared classifier and UI | ChatFrameUtil/filters and ChatInfo; separate activity namespace, explicit phrases retained |
| Official listings and activity discovery | Disabled | Era GroupFinder selection omits reviewed official-listing UI; no LFG_LIST registration or official API calls |
| Settings and conveniences | Shared with capability checks | Fresh Settings/Keybindings, Bindings_Vanilla and CVar settings sources; unsupported named CVars disable their own feature |
| Error suppression | Small Era policy | Fresh UIErrorsFrame; new types visible, explicit choices preserved; no Forever numeric-ID migration |
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

After approval and closing Era, omit `--inspect-only`. Updates require the last
Era `--previous-install <backup>/transaction.json` to recognize replaced bytes.
The installer admits four DEV children plus the inert marker, rebuilds expected
bytes from immutable pins, preserves edited documentation and unknown files,
refuses conflicting runtime edits or alternate loaders, backs up and verifies
writes, and stores an Era receipt. It never enables addons or reads/copies private
saves. Old archives are not recognized install sources.

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
drafts; error visibility and explicit suppression; optional settings; tooltip
errors; and absence of taint/blocked-action messages. Verify excluded features
stay unavailable. Never operate the game from Codex.

If a core feature needs substantial shared gameplay changes, stop for review.
Future Forever release work requires its own fresh authority and native
acceptance. Era results cannot substitute for either.
