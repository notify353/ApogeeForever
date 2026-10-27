# Era error defaults correction - October 25, 2026

The owner reported all errors still visible. Era.1/2 deliberately defaulted
every learned type to unchecked, so the enabled suppression switch had nothing
selected to suppress. A test using the fresh native Classic UIErrorsMixin
confirmed that checked types already suppress combat text and handler audio.

The owner explicitly approved combat defaults with useful feedback preserved
and a once-only reset of existing Era learned choices. No private saved files
were inspected, imported or edited. The reset occurs through addon initialization
when the user next loads the updated package.

## Change

Era.4 pins Essentials `4f0402a598b047174ee74b532b6e29729fda07f2` and retains
GroupAlert `35abae5885c8e442ed1df76867dc8caa20e1f953` from the pending
[Group Finder correction](GROUP_FINDER.md). Other child pins remain unchanged.

The private Era adapter uses GetGameMessageInfo to resolve native symbolic names
for routine cooldown, range, resource, target and casting-position errors.
Useful inventory, item, equipment, reagent, quest, interaction and interruption
errors are not suppressed by default; unknown/unreadable types remain visible.
No Forever numeric identities are reused. The shared runtime adds only a private
Era defaults callback; its Forever branch and saved migration remain unchanged.

The separate eraErrorDefaultsVersion=1 marker resets valid learned entries once.
It preserves message history, global/other preferences, subsequent checkbox
changes and future versions. Defaults uses the same policy. All suppression
remains combat-only and requires the main switch to be enabled.

## Checks and evidence

- Fresh product/executable and 62 Era references verified, including generated
  GameErrorDocumentation and selected Classic UIErrorsFrame source.
- New Era regression failed before the correction, passed afterward.
- All 29 Essentials specs and 47 tracked Lua parses passed. Full central runner
  passed all 171 child specs, nine Era distribution tests, 76 generated admission
  scenarios and four generated adapter tests.
- Generated tests run the fresh native error handler under mocks: combat-only
  text, voice and sound suppression; visible useful/unknown errors; unchanged
  info/system delivery and global-off behavior. They cover once-only reset,
  later choices, disabled-feature migration, new accounts, future versions,
  native names with different numeric IDs and unavailable/restricted mappings.
- All 77 existing central Forever offline tests passed; rebuilt frozen PROD
  and DEV archives are byte-identical to their original ZIPs. Live Forever
  validation is unavailable and is not claimed.
- Before installation, all 1,477 Forever addon files, eight frozen repository
  files and all 113 installed Era.2 files remain unchanged.

Artifact: `Apogee-1.14.8-era.4-DEV.zip`, SHA-256
`c49951a39cdfcdd74ca61a40bfed0ac861f0a6ffeb3a820820c81834720f2f38`.

Machine-local record/evidence:
`C:/Temp/apogee-era-20261024/error-defaults-20261025/`, including
`task-record.md`, `before.json`, `essentials-checks.log`, `validation.log`,
`validation/packages/`, `frozen-package-hashes.json` and `install-preview.json`.

## Installation and acceptance

Preflight proposes eight writes: five version TOCs, GroupAlert Era adapter,
Essentials Era adapter and Errors runtime. Five existing README files are
preserved by the central installer. Chain the update from the installed Era.2
receipt at
`C:/Dev/WoW/local-install-backups/apogee-era-bugfix-20261024/transaction.json`,
using a fresh external backup. The client was running at preflight; wait for
the user to close it before installation. No game operation or enabled-state
change is permitted.

Native user testing must confirm combat error text/audio, outside-combat and
useful error feedback, later checkbox choices across reload, and Group Finder
manual search/results/drafts. Offline tests do not establish native timing,
taint, server availability or complete coverage of every possible error name.

## Installed October 25

After the owner confirmed Classic Era was closed, central preflight rechecked
closed-client state, exact artifact and fresh API evidence, then installed eight
files. New verified backup/latest receipt:
`C:/Dev/WoW/local-install-backups/apogee-era-errors-and-groups-20261025/transaction.json`.
All 113 prior files were backed up. All 113 installed files verified: 108 payload
receipt entries plus five intentionally preserved README files. All 1,477
Forever addon files and eight frozen repository files match the before-snapshot.
See `closed-install-preview.json`, `install.stdout.json`, `install.stderr.txt`
and `install-verification.json` in the evidence directory. The earlier Era.1/2
backups and uninstalled Era.3 package are retained. Native acceptance and the
once-only settings reset await the user's next login; no game was operated.
