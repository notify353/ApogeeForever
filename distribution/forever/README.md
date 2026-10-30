# Live Forever authority

The isolated future candidate now targets reviewed Forever **1.60.1.70685**,
Interface 16001, product `wowf`, directory `_forever_`, executable `Wow.exe`.
The frozen v1.14.9 selection and its beta authority are unchanged.

`api-evidence.json` records the executable hash and 239 unique exported source
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

This checks both matching exports, child tests, generated Era DEV and Forever
PROD/DEV, loading safety, settings/binding preservation and historical rollback.
It never installs or publishes. The receipt records live authority separately
from native acceptance. See [candidate validation](../CANDIDATE_VALIDATION.md).

The live checker rejects a missing, stale or changed export, wrong executable,
wrong/inactive product, mismatched source pins and unsafe paths. It never falls
back to beta. The installation preflight recognizes the live executable, but
validation does not invoke an installer or authorize an installation.

## Source review, 2026-10-27

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
