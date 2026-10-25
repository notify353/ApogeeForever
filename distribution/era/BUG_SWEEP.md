# Classic Era bug sweep - October 24, 2026

Scope: the installed Era.1 candidate's private adapters, shared entry points,
generated loading guards, packaging and install/recovery paths. Forever's last
verified sources, pins and installed beta are frozen. No game operation or saved
data inspection. This is source review and offline testing, not native acceptance.

## Confirmed and corrected

1. **Era Keybinds explicit cursor IDs bypassed validation.**
   The shared `Identity.Cursor` used the fourth cursor return directly and only
   called the Era `CursorSpell` adapter when that return was missing. An explicit
   ID therefore skipped the player-bank and restricted-value checks. A fixture
   with a pet-bank cursor plus a known explicit ID reproduced the bypass; a
   restricted-ID fixture also tests the actual editor entry point. The private
   Era adapter now validates all cursor fields before resolving a spell. Valid
   explicit IDs and legacy player slots remain supported. The original Forever
   resolver is unchanged.

2. **Interrupted Era file writes could prevent verified rollback.**
   Era used the migration helper's direct-write path. A partial destination write
   would match neither the prior nor intended hash, so rollback would refuse it
   as an unexpected modification. Era now explicitly selects atomic file
   replacement while retaining its closed-client check. Existing Forever default
   behavior and live DEV family restrictions are unchanged. The regression
   injects failure on the third replacement after two successful writes, then
   verifies rollback restores all prior package bytes. Temporary failed staging
   files remain available for diagnosis and cannot be loaded as addon code.

Both regressions failed before their fixes. Other reviewed boundaries include
Heals fixed recipients/name formatting, Group Alert's disabled official APIs,
Essentials error defaults/CVar availability, family admission before gameplay,
foreign receipts, alternate loaders, edited documentation and fresh API checks.
No additional confirmed defect was identified in those reviewed paths.

## Verification and delivery

Candidate `1.14.8-era.2` pins Keybinds' Era-only fix. No other child source pin
changes. The new cursor API reference is fresh and recorded, taking Era authority
to 47 files. The existing beta authority requirements remain unchanged.

Validation uses `scripts/test-era.ps1`, including all 171 child Lua specs, nine
Era distribution tests, 76 generated family/client scenarios, fresh exported
secure code under mocks, and the existing 77 central offline tests. Full log:
`C:/Temp/apogee-era-20261024/bug-sweep-validation.log`.

Package and audit manifest:
`C:/Temp/apogee-era-20261024/bug-sweep-validation/packages/`.

This sweep prepares local fixes; it does not replace the installed Era.1 package.
Its receipt remains
`C:/Dev/WoW/local-install-backups/apogee-era-20261024/transaction.json`.
Native startup, secure-action timing and taint acceptance still require the user.
No push, main integration or publication.
