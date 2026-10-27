# Era Group Finder correction - October 25, 2026

The Era.1/2 adapter disabled official listings and native activity discovery
unconditionally. The original review checked the base Vanilla GroupFinder TOC
but missed Vanilla UIParent's load-on-demand VanillaStyle selection. The owner
reported the native finder is present and requested support, suggesting the
archived addon as a reference. Archive code was read only; no runtime or saves
were restored.

## Implementation and authority

Era.3 pins GroupAlert `35abae5885c8e442ed1df76867dc8caa20e1f953`.
Only its private Era adapter changes runtime: remove the forced unavailable
GroupAPI, empty DiscoverActivities and disabled official event flag. The existing
shared guarded adapter, model and UI handle search, results and discovery.
No other child pin or shared gameplay file changes. Forever locks, family gate,
builder and installation remain frozen.

The fresh 1.15.9.70003 export confirms the VanillaStyle loader, seven-argument
search, dungeon category 2, available activities, suggested level ranges,
result/player structures, remaining-role counts and lifecycle events. Fourteen
additional selecting TOC/XML/Lua and generated contract references bring the
Era evidence to 61 files. The archived adapter's old language-filter dependency
and four-argument search are not imported.

## Verification

- The new Era test failed against Era.2's unconditional unavailable state and
  passed after the adapter correction.
- All 171 child Lua specs and parsing passed, including GroupAlert's documented
  Lua runner (24 specs). The standard Forever entry point still rejects Era.
- All 9 Era distribution tests passed: 76 generated admission scenarios, four
  generated adapters, installer isolation and interrupted-write recovery.
- Era source and generated tests exercise manual search and completion, partial,
  empty, failed and timed-out results; role/member/level filtering; identity
  rechecking before editable whisper drafts; combat hiding; restricted-data
  guards; missing capability fallback and continuing chat alerts. No login or
  update-triggered search and no automatic messages.
- The fresh exported LFGBrowse_DoSearch function executes under mocks and sends
  the same seven arguments as the generated Era adapter. This is not live WoW
  execution or a native timing/taint acceptance claim.
- All 77 existing central Forever offline tests passed. Rebuilt Forever PROD
  and DEV ZIPs match the previously frozen archives byte for byte.
- All 1,477 installed Forever addon files and eight frozen repository files
  match the pre-work snapshot. Installed Era.2's 113 files are unchanged.

Artifact: `Apogee-1.14.8-era.3-DEV.zip`, SHA-256
`20bb8d6f1649238a0f7518ad59718a76db54dc3b12345aa865f4dffb5116b36e`.

Machine-local evidence:
`C:/Temp/apogee-era-20261024/group-finder-20261025/validation.log`,
`validation/packages/`, `before.json`, `frozen-package-hashes.json`, and
`install-preview.json`.

## Installation and native acceptance

Preflight proposes six writes: five version TOCs and the GroupAlert Era adapter.
The central installer preserves three existing README files; updated package
guidance is in the ZIP and this report. Its receipt must chain from
`C:/Dev/WoW/local-install-backups/apogee-era-bugfix-20261024/transaction.json`.
No Era.3 installation occurred during these checks; the client was running.
Obtain final approval and a closed client under the Era workflow. Retain all
prior backups and create a new verified backup before writing.

User acceptance: select Tank or Healer and click View; compare native listings,
test empty results and refresh, role and My level filters, editable Tank/Heal
drafts, chat alerts and combat hiding. Runtime capability checks can still reject
native search when unavailable to the character. Never operate WoW from Codex.
