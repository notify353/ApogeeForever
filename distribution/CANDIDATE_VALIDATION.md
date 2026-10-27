# Candidate validation

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

Use `--offline` on a host without matching Era authority. That mode still runs
synthetic generated-package checks but creates **no installable Era artifact**.
No offline result establishes API or native acceptance. Future Forever is always
offline here: its frozen release pins and installed beta stay untouched until a
fresh matching export and native acceptance are available. The existing hosted
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
