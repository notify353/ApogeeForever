# Candidate validation

## Routine small changes

Use `scripts/validate_change.py` first for a narrow Forever Keybinds default
mapping change. The initial reviewed profile is `keybinds-defaults`; other gameplay
areas currently escalate to full validation. Do not guess a small profile or add
an ad hoc exhaustive input matrix. Extend the selector and its refusal tests when
another focused profile is justified.

The baseline must be a successful **full** `candidate-validation.json` from this
workflow version, including frozen regressions, live Forever evidence and
`distributionCommit`. A dirty distribution run or a focused receipt cannot serve
as that baseline. Keep the receipt outside Git. Selection compares the full pinned
source trees and distribution history, not just the changed file count.

```powershell
python -B scripts/validate_change.py --baseline C:/path/full/candidate-validation.json `
  --child C:/path/ApogeeKeybinds --plan
python -B scripts/validate_change.py --baseline C:/path/full/candidate-validation.json `
  --child C:/path/ApogeeKeybinds --sources-root C:/Dev/WoW `
  --client-root 'C:/Program Files (x86)/World of Warcraft/_forever_' `
  --artifact-root C:/path/new-focused-validation
```

Commit reviewed source/pin updates before running it. `--plan` is read-only and
prints the selected suites. Unsupported changes stop with a full-validation reason
before running tests or building packages. No automatic long full run is started.

This path runs five source suites (shared Warrior defaults, Vanguard, Intercept,
markers and the default toggle) and four generated DEV suites. New/changed regression
specs are included and deduplicated. The toggle's actual Settings control is covered
in source; unchanged shared Settings integration is inherited from the full baseline.
The seven repetitive per-spell Warrior suites are consolidated into one table.
The runner checks all child Lua syntax, current export freshness, exact pins,
generated-copy equality, both generated package contents and concurrent changes.
It requires no Era/unchanged-child test checkouts and creates no child source ZIP.
Unchanged Era, other children, generated PROD behavior and frozen migration suites
reuse the full baseline. This is validation reuse, not new native acceptance.

Any shared compiler/secure routing, default presentation helper, harness, loader,
package inventory, another child/support module, installer, transform, release or
client/API change requires the full path below. Missing/deleted tests, dirty source
or mismatched baseline evidence also stop the small path. Historical beta authority
is never substituted for current live authority.

Within Defaults.lua, the focused profile permits numeric mapping tables and
side-effect-free stance choices. Existing Vanguard knowledge is the only allowed
call in that selection block. New API calls, mutations, opt-in/marker dispatch or
changes to the shared compilation tail require full validation even in that file.

Success writes `focused-validation.json` (explicitly not full/release evidence)
and the checked packages under `future-forever-validated/`. Use the central installer
with the exact lock/artifacts and latest installation receipt. Inspect first, obtain
the required immediate installation approval, preserve the rollback backup and verify
installed bytes. These installation checks are unchanged. Test-only/tooling changes
with identical runtime do not need reinstallation.

Do not run standalone child full checks before either central path. Repeat a check
only after relevant changes, a failure, or a specific unresolved concern. Report
suite/behavior coverage; don't headline simulated key-press counts as test counts.

## Full validation

Current candidates explicitly select [capability-based runtime admission](RUNTIME_CAPABILITIES.md).
Generated behavior covers Era and Forever, each in PROD and DEV, including
legacy/mismatched/error metadata, missing actual APIs, shared-service startup,
family ownership and the combined Essentials quest-text/A-D defaults.

The merged-source candidate and unchanged release boundaries are recorded in
[release preparation](RELEASE_PREPARATION.md). Its two locks currently share
the five merged child revisions; use clean checkouts at those exact commits.

Run from the distribution worktree. This entry point checks **both** isolated
locks (`era/candidate.lock.json` and `future-launcher.lock.json`), not the frozen
release candidate. All five child test checkouts must be clean and exactly match
their lock commits. Shared support must match its owning Essentials revision.
Era-only work may advance its child pins independently. When pins differ, pass
`--future-child-worktrees` with clean checkouts at the unchanged future Forever
pins. Each target uses its own matching test sources, including generated tests;
the default shared checkout path still rejects mismatched pins. The validation
receipt records both target maps separately. Do not advance Forever merely to
make Era's test-source check pass.

For example, after creating one exact child checkout per subdirectory under
`C:/Temp/apogee-merged-child-checkouts`:

```powershell
python -B scripts/validate_candidates.py `
  --child-worktrees C:/Temp/apogee-merged-child-checkouts `
  --sources-root C:/Dev/WoW `
  --artifact-root C:/Temp/apogee-merged-validation-NEW
```

Stats' explicit loader-contract script and generated Era parser/startup/auction
tests are included, alongside future Forever Stats regressions. Historical
four-module Era upgrades and rollback remain covered after adding Stats.

This verifies fresh Era authority first, then parses child Lua, runs child Lua
and Python suites, independently validates Essentials' Forever/Era/support
inventories, checks explicitly source-only child archives, and tests generated
Era DEV and future Forever PROD/DEV packages. Startup fault injection runs on
generated shared UI, Essentials, Heals and Keybinds. Existing default-spell,
position-only reset, combat, family loading, rollback and historical archive
checks remain included. A receipt records tested commits, both lock hashes and
the Era evidence. No installation, publication or game operation occurs.

For the current live Forever client, use
`pwsh scripts/test-live-forever.ps1 -ChildWorktrees <path> -ArtifactRoot <new-path>`.
It supplies `--forever-client-root` to verify the live export before and after
the full run. The receipt then includes `futureForeverApiEvidence` and sets
`futureForeverOfflineOnly` to false; `nativeAccepted` remains false. The central
evidence covers all exact child pins without changing their historical beta
baselines. See [live Forever authority](forever/README.md).

Use `--offline` on a host without matching Era authority. That mode still runs
synthetic generated-package checks but creates **no installable Era artifact**.
No offline result establishes API or native acceptance. Without
`--forever-client-root`, future Forever remains offline. `--offline` skips only
Era's export check; explicitly supplying a Forever root still requires its live
authority. Frozen release pins and installed addons stay untouched. The existing hosted
release workflow validates the frozen candidate; it is not evidence for these
new candidate locks. A CI checkout may run this same offline command once all
exact private source/test revisions are available there.

`--skip-frozen-regression` is only for focused reruns after the unchanged frozen
suites have passed. The older `test-era.ps1` is Era-focused; use this entry point
for coordinated candidate changes. The existing release `test-local.ps1` remains
the frozen Forever release path.

Child `build-package.ps1` commands require `-SourceOnly`. Their archives are
incomplete development source bundles, not installable addons. Install only a
central checked family package. Heals and Stats have no standalone builder.

## Startup failure acceptance

Shared UI publishes readiness only after its required Settings owner succeeds.
Fatal startup remains failed until reload; it does not reset saved assignments
or preferences. Heals and Keybinds cancel owned polling/events/input claims and
hide partial UI. Presentation failures are contained separately from gameplay
startup and from cleanup. No new saved-data schema or migration is involved.

After the checked Era DEV installation, the owner should reload and confirm
normal startup, both editor toggles, individual editor closing, component
settings, combat behavior and position-only reset with existing binds. Native
acceptance, timing and taint cannot be established by these mocks. Do not inject
test failures into a live client or inspect/copy private saved data.
