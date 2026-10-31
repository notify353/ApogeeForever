# Era.11 and future Forever: internal UI and master switch

Current runtime admission follows the owner-approved
[capability policy](../RUNTIME_CAPABILITIES.md), dated 2026-10-31. Package/version
labels cannot disable compatible services. Historical archives remain frozen.

Owner decisions, October 25, 2026: keep independent gameplay checkboxes, remove
the separate shared-support entry, and reset only minimap position on upgrade.
This explicitly supersedes the metadata-only marker requirement for these
new candidate packages. Frozen no-support and historical standalone builds
retain their original loading contracts and exact archive bytes.

The Essentials Shared/ApogeeUI source is embedded in ApogeePartyHealthBars[Dev].
The support lock entry has placement=master and retains its owner commit,
subdirectory, API and file hashes. The root TOC owns its three SharedUI chunks,
family gate and per-character ApogeeUI[Dev]DB. Public UI service/frame identities
stay separate by family. The root owns its artwork and responds to its actual
ADDON_LOADED event. It has no gameplay dependency, so disabling Essentials does
not disable the launcher. With no active components there is no minimap button.

The builder transforms each reviewed source dependency on ApogeeUI to the
matching family master and records X-Apogee-Requires-Master=1. Every runtime
chunk checks actual family admission, required methods and enabled master. Children
also require native loaded status and an initialized service. Missing, disabled,
wrong-family or failed/incomplete services cannot start gameplay. Mixed package
versions with working methods are allowed. The additive
master gate does not replace or modify frozen FamilyGate.lua. New checked PROD
children cannot select PROD when its master is off; already-loaded PROD and
legacy children retain the existing family exclusion behavior. No global game
API replacements, enable preference writes or gameplay edits are introduced.

Fresh Era 1.15.9.70003 authority verifies 83 references. Native AddOnList uses
Group as presentation metadata; ordinary entry checkboxes only select that
addon. Native GetAddOnDependencies exposes required dependencies separately
from metadata. The new master relies on those established APIs and guarded
current-character enable/loaded state. Future Forever has offline coverage only;
fresh matching export and native acceptance remain prerequisites to installing it.

Upgrade uses the central installer with a closed client and full restart.
The prior installed receipt must recognize every old ApogeeUIDev Lua/XML/TOC
byte; alternate loaders or user edits stop preflight without writes. The
installer backs up all managed files, then moves exact known old runtime files
into the external transaction's retired-files directory. Remaining notes/assets
are preserved and inert without a TOC. The rollback journal restores the old
loader and all retired runtime and quarantines newly added files. Unknown files
and private saves are never imported, purged or relocated. The new save owner
starts the minimap at 220; component settings remain with their original owners.
Later updates of this same loading graph may use the existing checked live path.

Required checks: full test-era.ps1, generated Era/future PROD/DEV launcher and
Settings tests, master-off/failed-start/missing-method denial, mixed-family and
legacy selection, standalone upgrade and rollback fixtures, unknown-file
preservation, live structural-update refusal, frozen archive identity.

User acceptance after restart: no Apogee UI row; master off => no components
after reload; master on => selected components work. Test Heals/Keybinds together,
each alone, and Essentials or Dungeons alone. Confirm one green icon, grouped
editor toggle, flat settings menu, drag/release, combat handling, default position
and persistence on the next reload. Native results must be recorded separately.
