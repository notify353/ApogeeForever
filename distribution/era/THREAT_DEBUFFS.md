# Era live threat debuffs - 2026-10-25

The owner reported missing live debuffs such as Sunder Armor. The pictured tank
threat demo uses scripted icons; the live shared renderer requires
CustomAuraContainerTemplate, which is absent from the fresh Era export. Era.4
did not provide a replacement, so live rows could not display those effects.

## Correction

Era.5 pins Heals `9a1fe7de6f2e6f3360f3b3fac0bc9500f02c5d1e`. Only its private
Era adapter changes runtime behavior. Other child pins, shared gameplay and
Forever's native renderer remain unchanged.

The adapter reads public C_UnitAuras.GetAuraDataByIndex records on existing
nameplate tokens using HARMFUL|INCLUDE_NAME_PLATE_ONLY. It recognizes all Era
ranks of player-owned Sunder Armor, Thunder Clap and Demoralizing Shout. Sunder
counts above one appear on the existing icon; confirmed effects with unreadable
counts show a question mark. Effects from other players or pets remain excluded,
matching the existing feature contract. This is not a general debuff tracker.

The existing 0.1-second refresh, fixed artwork and row lifecycle are reused.
Each scan is bounded to 64 auras plus a terminating probe. Failed, restricted or
incomplete snapshots clear icons; no partial result or stale stack is retained.
No frames, protected geometry, global API aliases or saved-setting migrations
are introduced. Demo mode remains synthetic. Party cleansing/aura widgets are
outside this correction.

## Evidence and checks

- Build 1.15.9.70003 / Interface 11509 and 67 fresh export references verified.
  New evidence includes the selecting FrameXMLUtil and UnitFrame Classic TOCs,
  AuraUtil common/Classic sources and Classic TargetFrame. Stale alternative
  TOCs are not used. Native AuraUtil field unpacking also executes under mocks.
- The new live Sunder regression failed before the adapter correction and
  passed afterward. Tests cover all Sunder ranks, own-caster filtering, stack
  updates, removal, failed/restricted/bounded reads, combat frame guards,
  nameplate reuse, demo transitions and disabled/world cleanup.
- All 171 child specs and Lua parses passed, along with nine Era distribution
  tests, 76 admission scenarios and four generated adapter tests. All 77 frozen
  Forever offline distribution tests passed. The runner's final whitespace
  check caught a documentation line ending; it was corrected and rechecked.
- Rebuilt frozen Forever PROD and DEV ZIPs are byte-identical to the previous
  frozen archives. All 1,477 installed Forever files and eight frozen repository
  files match the before-snapshot; all 113 installed Era.4 files were unchanged
  at preflight. No live Forever acceptance is claimed.

Artifact: `Apogee-1.14.8-era.5-DEV.zip`, SHA-256
`b3e3eb116b0e896a64d8649c6ab7663ce352e539d485b6d648b2c3c1e1493e8e`.

External evidence: `C:/Temp/apogee-era-20261024/threat-debuffs-20261025/`, including
task record, before-snapshot, Heals checks, aggregate validation log/packages,
preservation and frozen archive checks, and install preview.

## Installation and native acceptance

Central preflight reports a closed Era client and six writes: five version TOCs
and the Heals Era adapter. Seven existing README files are preserved. Chain from
the installed Era.4 receipt at
`C:/Dev/WoW/local-install-backups/apogee-era-errors-and-groups-20261025/transaction.json`.
Use a fresh external backup and explicit `--target classic-era`.

The user must confirm live Sunder stacks build/change/expire on enemy nameplates,
Thunder Clap and Demoralizing Shout appear, switching/removing enemies clears
old icons, and combat produces no Lua or blocked-action errors. Demo mode must
be off for this live check. Mocks do not establish native timing or taint safety.
No private saves, addon enable preferences or game controls are accessed.
