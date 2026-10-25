# Era candidate validation - October 24, 2026

Status: offline candidate ready for review. No installation, publication, push or main integration. Native acceptance pending.

## Immutable sources

| Module | Era commit |
| --- | --- |
| ApogeeHeals | `0858cb7e0a226c6a9426d16580a114b85de0dc98` |
| ApogeeKeybinds | `fad2b247f51f730f456cfd2a6aea0706c8ffc086` |
| ApogeeGroupAlert | `400326b4baf3549a47d88d2ca640e12251d8563a` |
| ApogeeEssentials | `dd852eb49b0216934c517f97f764b2dfa3bcbb76` |

Every source worktree is on `codex/classic-era`, based on the exact latest installed Forever DEV revision. Stats is unchanged and excluded from Era.

## Checks

- 171 child Lua spec files passed; Lua 5.1 parsing passed for all tracked child Lua.
- Heals and Keybinds documented local runners passed (Keybinds uses its supported `-SkipExport` for frozen offline regression). Group Alert Lua runner and Essentials parse/spec checks passed.
- Nine Heals historical-export contract specs also passed against retained beta source. These are offline regressions, not current Forever authority.
- 8 Era distribution/installer tests passed, including 76 generated client/family scenarios and all four generated DEV adapter tests.
- Fresh Era SecureTemplates and SecureStateDriver executed under mocks: direct spell action, macro routing, combat action and deferred rebuilding passed. This cannot establish native taint or timing.
- All 77 existing central offline tests passed across repository, CurseForge validation, publisher, distribution, migration and dual-family suites.
- 46 Era export references verified fresh and unchanged against the reviewed executable/product 1.15.9.70003.
- Existing Forever PROD and DEV ZIPs rebuild byte-for-byte identically. Forever candidate/release source locks, family gate and builder hashes unchanged.
- All 116 frozen installed DEV receipt files and 128 frozen source files reverified. No installed addon files changed.
- Final read-only Era preview: 113 files, four DEV modules plus marker; no existing Apogee folders to replace. Era was closed at final preview. No backup/install transaction created.

## Artifact

`Apogee-1.14.8-era.1-DEV.zip` SHA-256:

`db9d35cb09b25d444aa6b2cec87c16234149c8fa5b07902df66d23c11ea6b1b1`

Machine-local artifact: `C:/Temp/apogee-era-20261024/final-validation/packages/`.
Evidence: `era-final-checks.log`, `child-test-results.json`, `central-offline-checks.log`, `central-offline-results.json`, `heals-frozen-export-contracts.log`, `frozen-verification.json`, and `install-preview.json` in the task directory.

The complete generated file manifest and source transforms are in `ERA-DEV-manifest.json` beside the ZIP. The prior assessment evidence remains in `C:/Temp/apogee-era-assessment-20261024/`.

## Limitations and next action

Live Forever validation is unavailable after beta and was not claimed. Its safeguards remain strict. Era excludes Stats/tooltips/auction evaluation, official group listings and the Heals target-action strip. Error defaults are conservative and optional unsupported CVars are unavailable.

Review the candidate and obtain explicit approval for first Era deployment. Recheck that Era is closed, use the central explicit Era installer, retain its backup/receipt and verify installed bytes. The user selects the family and performs the native acceptance checklist in README.md. Do not operate the game, import archived saves or modify the frozen Forever installation.
