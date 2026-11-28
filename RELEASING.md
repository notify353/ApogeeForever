# Prepared selection - 2026-11-27

Forever **1.14.24** selects the party-bar improvements installed as DEV1.14.23-dev.7. The owner explicitly requested check-in, merge and CurseForge deployment. All release DEV Lua/XML runtime files match that installed package. The initial priest strip was reported working; subsequent refinements have automated validation, with nativeAccepted:false. See [immutable selection](distribution/releases/1.14.24/manifest.json). Require successful test, aggregate and release-1.14.24 checks on exact final main before the authorized production tag.

# Prepared selection - 2026-11-27

Forever **1.14.23** selects the accepted DEV1.14.22-dev.38 gameplay: auction-house-only upgrades, Loot history/presentation, Group Finder polish, self-buff countdowns and Warrior Intercept. The owner requested CurseForge deployment after confirming the reload looks good. See [immutable selection](distribution/releases/1.14.23/manifest.json) and [scoped DEV acceptance](distribution/releases/1.14.23/dev-acceptance.json). All generated DEV Lua/XML runtime files match the accepted archive. Require test, aggregate and release-1.14.23 on exact final main before the authorized production tag. Comprehensive native/taint and separate PROD/CurseForge-client acceptance remain unclaimed.

# Prepared selection - 2026-11-22

Forever **1.14.22** includes the compact, class-grouped and resizable Whisper UI,
manual location pin, native sender levels and the Penance healing-binding fix.
The owner accepted Whisper DEV.5 and Penance DEV.6 after reload, then requested
CurseForge deployment of all changes. See the [immutable selection](distribution/releases/1.14.22/manifest.json)
and [scoped DEV acceptance](distribution/releases/1.14.22/dev-acceptance.json).
All generated DEV Lua/XML runtime files match installed DEV1.14.21-dev.6.
Require test, aggregate and release-1.14.22 checks on exact final main, then
immediate production-tag approval. Comprehensive native/taint, separate PROD
and CurseForge-client acceptance remain unclaimed. Earlier notes are historical.

# Prepared selection - 2026-11-20

Forever **1.14.21** includes the Stats runtime tested in DEV1.14.20-dev.2 plus
reviewed-build notice updates for71037. The owner confirmed Gear removal and
error-free bag clicks after reload, then requested CurseForge deployment.
See [selection](distribution/releases/1.14.21/manifest.json) and
[scoped acceptance and exact runtime differences](distribution/releases/1.14.21/dev-acceptance.json).
Require test, aggregate and release-1.14.21 checks on exact final main, then
immediate production-tag approval. Separate PROD/CurseForge-client acceptance
and comprehensive native coverage remain unclaimed. Earlier notes are historical.

# Prepared selection - 2026-11-19

Forever **1.14.20** selects the complete owner-tested DEV.15 gameplay, including healing recovery, priest Dispel Magic, Vanguard Charge, Dungeons filters and whisper grouping/fade/Who fixes. See [selection](distribution/releases/1.14.20/manifest.json) and [owner DEV acceptance](distribution/releases/1.14.20/dev-acceptance.json).

The owner requests integration and readiness for CurseForge deployment. Final production-tag approval remains separate. Require successful test, aggregate and release-1.14.20 checks on exact final main before publication. Separate PROD and CurseForge-client testing are not claimed.

Earlier preparation notes below remain historical.

# Apogee Forever releases

Current prepared selection: **Forever 1.14.18**, reviewed against build **70862**.
Its immutable manifest and player notes are in [1.14.18](distribution/releases/1.14.18/manifest.json).
The owner explicitly approved CurseForge deployment and its required release steps
on 2026-11-08 after two resurrection bug sweeps. This selection matches installed
DEV1.14.17-dev.5 gameplay. Source/generated DEV checks pass; regular resurrection
and range have in-game acceptance, while Druid combat/taint acceptance is pending.
The manifest retains nativeAccepted:false. Exact final-main hosted checks remain
required before the approved production tag. Published1.14.17 and all earlier
prepared selections remain immutable.

Published 2026-10-31: Era **1.14.12** and Forever **1.14.13**. The
[publication record](distribution/releases/PUBLISHED_2026-10-31.md) links both
releases and successful public-byte verification. The earlier
[review](distribution/releases/REVIEW_2026-10-31.md) retains its preparation-time
status. The final-main checks and tag approval below apply to future releases.

## Current dual-client early releases (2026-10-29)

Follow [client-specific release selections](distribution/releases/README.md)
for Era1.14.10 and Forever1.14.11. Both are normal Releases under project1608100,
with separate archives/version metadata. Era is independently releasable.
The owner explicitly accepted limited live Forever testing; manifests retain
`nativeAccepted: false` and bind that decision to exact packages. This policy
does not waive client evidence, source/package checks, upload verification or
immediate final production-tag approval. Installed addons remain unchanged.

The workflow reads each tagged version's manifest and exact source pins. Main
must pass its selected `release-<version>` check, including authenticated version
preflight. Existing aggregate checks continue covering the frozen release.
The historical native-accepted flow below remains for its archived selections.

GitHub Actions is the sole publisher for CurseForge project1608100 and the
notify353/ApogeeForever repository. It publishes only the selected canonical
Forever addon folders (currently five public children plus the marker; Tank and standalone Auction are retired; Stats is included). The same verified ZIP goes to both services.

## Access and validation

The distribution-validation environment is restricted to main. It requires
DISTRIBUTION_READ_TOKEN access to four private child repositories (including Stats) and CF_API_KEY
for read-only version preflight. Public child checkouts use the job token. Pull
requests run self-contained tests without these environment credentials.
Production retains its v*.*.* tag-only policy and holds the same scoped source
read token plus its existing CF upload credential. Never log secret values.

On October 17, 2026, read-only GitHub inspection confirmed source-read secret
entries in both environments were updated October 2, superseding the historical
October 1 expiry note. Secret metadata does not reveal current expiry or prove
access. Require successful aggregate/version checks on the exact final main
commit. If renewal is needed, obtain owner approval and retain the reviewed
read-only private-repository scope, including Stats. Never print credentials.

Enable APOGEE_DISTRIBUTION_SOURCES_READY only after the required secrets exist.
Run Distribution validation and CurseForge version preflight on main. Both must
pass for the exact release-preparation commit before tagging. The preflight
requires one exact 1.60.1 result with Forever version type88568; the type is not
an upload-version ID and there is no fallback.

Native acceptance is tracked separately for each installed DEV candidate.
`distribution/native-acceptance.json` pins its tested Lua bytes and the generated
PROD counterpart from the same reviewed sources; this does not claim separate
PROD or CurseForge-client testing.
Runtime changes invalidate acceptance; documentation/version changes do not.
The local staged installation was not a CurseForge download.

## Prepare and publish

From clean, synchronized main run:

```powershell
pwsh ./scripts/prepare-release.ps1 -Version X.Y.Z
```

The helper creates a release branch, updates version/changelog metadata, runs
local validation and commits only the preparation files. Integrate through a PR
and wait for test, aggregate and version checks on the final main commit.
Review the exact version, package and player-facing notes. Obtain explicit
production-tag approval under the owner's current instructions, then run:

```powershell
pwsh ./scripts/publish-release.ps1 -Version X.Y.Z -ConfirmProduction
```

Never create tags ad hoc or move/reuse a published tag. The helper requires a
clean synchronized main, matching version and successful hosted checks.

Actions regenerates and validates the accepted package, resolves the exact
Forever upload ID again, creates a GitHub draft, uploads and downloads its ZIP to verify its hash,
publishes GitHub, and then sends the same bytes to CurseForge once. Its retained apogee-publication artifact records
an attempt before the CF POST and records the returned file ID afterward.
An uncertain response must be investigated; never blindly rerun an upload.

After CurseForge approval, obtain the file's actual download link. Dispatch
Verify Apogee Forever publication on the same production tag with the successful
upload run ID and that link. It validates the source run, matches both remote
hashes and records completed verification. GitHub is already public. Monitor both Actions workflows
and the CurseForge file status before declaring publication complete.

## Client acceptance and public copy

The first actual CurseForge-client installation check follows the first approved
available Forever upload. Preserve Dev folders, private settings and unknown
files with a verified rollback plan. A local ZIP installation is not that check;
record first installation separately from later update/removal tests.

Publish only the current release section, not cumulative historical changelogs.
Keep notes focused on features, fixes, supported clients and necessary upgrade
steps. Packages include the short player guide and required licenses/notices;
engineering reports and child development changelogs are excluded.
