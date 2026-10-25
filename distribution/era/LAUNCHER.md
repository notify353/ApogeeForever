# Shared launcher - Era.8 / future Forever

One Apogee UI support addon owns the green 32-unit minimap button, native context
menu, Settings parent and per-character schema-1 angle (default 220 degrees).
Source is pinned from Essentials Shared/ApogeeUI, separately packaged. Each
component requires matching support; Essentials itself may be disabled.
Heals and Keybinds no longer create minimap frames. Components register only
after successful supported startup. Editors remain independent and callbacks
revalidate availability. Keybinds unregisters on deactivation; Essentials removes
registration on rollback. Stats registers only on supported initialized Forever.

Left-click: Healing bindings and Keybind editing checks (when available),
component Settings submenu, Apogee settings and Reset minimap position.
Right-click: common overview. Right-drag: move/save, suppress release click.
Combat/world suspension cancels owned menus and dragging; no protected gameplay
mutations are added. Existing default-spell synchronization remains in components
and joins the shared parent's schema-1 registry. No saved settings are imported.

Client adapter evidence: Era 1.15.9.70003, 83 fresh references including menu TOC,
Menu/MenuUtil/MenuTemplates and Vanilla variants. Native menu proxy Close affects
only our owned menu. Forever source is identical but current native authority is
unavailable; future-launcher.lock.json is offline-only and does not replace the
frozen candidate/release locks or beta installation. Includes prepared pre-combat
Forever suppression behavior; no new error-default migration.

Packaging validates explicit support source owner/subdirectory/commit/file hashes,
API 1, exact loaders and every child's dependency. DEV resource/frame/global/save
identities are audited separately. Every support chunk receives the client/family
gate. Marker stays runtime-free. Historical no-support packages remain unchanged.
Install/rollback accept only known inventories, support verified legacy Era receipts,
and retain unknown files/docs/private-save metadata protections. Live-update opt-in
rejects this discovery change. First support installation requires client closed
and a full restart, not a reload. No enable preferences are changed automatically.

Verification: source suites; actual generated support in Era DEV and future
Forever PROD/DEV, 325 component subsets/load orders each; real generated editor
adapters; Stats startup registration; callback failure/stale callbacks, malformed
API/source, future save schema, combat, drag, position/reload and editor independence.
Existing generated Era adapters, denial-before-effects and frozen Forever suites
remain required. Frozen Forever archives must match prior hashes exactly.

Native acceptance (owner performs): restart Era, enable desired components plus
Apogee UI shared support; verify exactly one green button with both components,
each alone, and Essentials or Group Alert alone. Check menu order, both editors
open simultaneously, external close reflected in checks, settings destinations,
right-drag then reload persistence, reset, combat dismissal and no release click.
Do not claim native acceptance from mocks. Do not operate WoW or read private saves.
