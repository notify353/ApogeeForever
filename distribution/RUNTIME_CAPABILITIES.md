# Runtime capability policy — 2026-10-31

Owner instruction: no addon feature on Classic Era or Forever, DEV or PROD,
may be inactive solely because client/build/interface text is outdated or
mismatched, or package status is legacy/unverified. This supersedes older
runtime version/metadata policies. It does not bypass native restrictions.

The current Era and future-launcher locks select `runtimePolicy: capabilities-v1`.
Only these selections use `runtime/FamilyGate.lua`, `runtime/MasterGate.lua` and
`runtime/EraClientGate.lua`. Earlier gates remain solely to reproduce immutable
historical artifacts. No installed packages or release manifests change here.

The reported Keybinds warning came from `API.Conflict`: it accepted loaded APHB
only when Distribution-Only and Distribution-Schema were both exactly `1`.
The embedded master intentionally runs shared UI and lacks Distribution-Only.
Era startup and secure binding claims therefore rejected a legitimate master.
That metadata inference is removed from Keybinds on both clients.

All five children accept shared UI by the methods they call. The UI provider
validates actual component/action fields rather than its numeric API label.
Forever's native project identity (or legacy project 1) selects its adapter;
Era uses native Classic project identity. Neither path expires on version text.
Heals target actions are independent: missing talent-inspection support does not
hide available Follow/Inspect actions. Their native range/combat checks remain.

Generated runtime admission never queries package metadata. It uses installed
addon identities, current-character enable/load state and native dependencies
to choose one family; an enabled or loaded PROD owner wins. A checked dependent
child with its master disabled cannot select PROD unless already loaded. A
disabled legacy installation alone cannot block DEV. An enabled legacy owner
can still compete and therefore selects PROD, regardless of its metadata.

Children need the enabled, loaded master and actual shared UI methods. Explicit
initialization failure or `ready=false` blocks use; older services without a
ready/version marker are accepted when their methods exist. New shared UI sets
ready=false before initializing. Family leases retain identity and family
checks, without requiring a numeric schema label. Malformed/secret ownership
state still fails safely; switching families requires reload.

Remaining restrictions are concrete: required APIs or data shapes, restricted
values, combat/protected actions, native client adapter identity, explicit
startup failure, incompatible saved-data schemas and actual family ownership.
Method presence cannot prove identical native semantics. In-game timing, taint,
secure actions and coexistence still require user testing.

Offline checks retain exact export/executable evidence, source/package hashes,
TOC/dependency validation, immutable pins, install receipts and rollback rules.
The game itself controls loading outdated TOCs; no game preference is changed.

Validation: `scripts/test-live-forever.ps1` with exact clean child worktrees runs
all five source suites, generated packages for Era/Forever × PROD/DEV, metadata
mutation/capability failure cases, shared Settings, family selection, Essentials
quest/A-D defaults and historical archive/migration/rollback regressions.
No installation, main integration, push or publication is authorized by this work.

## Validation evidence — 2026-10-31

The full live runner passed using clean child pins on
`codex/runtime-capabilities-20261031`: Essentials `7039bf1`, Heals `c421ae2`,
Keybinds `103cad3`, GroupAlert `ece5d6e`, Stats `6d7c59a`. Essentials includes
the prior instant quest text and A/D strafe defaults. Both candidate locks select
these exact immutable sources.

Machine-local receipt:
`C:/Temp/apogee-quest-text-20261031/capabilities-validation-r2/candidate-validation.json`.
Log: `C:/Temp/apogee-quest-text-20261031/capabilities-central-checks-r2.log`.
Era 70576 verified 99 references; Forever 70707 verified 243. All 184 child Lua
specs, generated behavior for all four variants (396 admission scenarios),
shared Settings, native-default coexistence, and frozen archive/migration/rollback
suites passed. Root Python discovery finds no tests; the documented runner
explicitly invokes the distribution suites. Native acceptance remains false.

The first run stopped at a synthetic historical standalone upgrade lock that
inherited the new embedded-only policy. That fixture now explicitly selects its
archived policy; immutable historical archive hashes still match. Both attempts
and all existing worktrees/backups are retained. No install or game operation occurred.
