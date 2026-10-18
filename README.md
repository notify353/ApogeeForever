# Apogee Forever

Five focused addons for **World of Warcraft Forever 1.60.1**:

- **Heals:** party frames, click healing and buff reminders.
- **Keybinds:** configurable keyboard and mouse actions with combat HUDs.
- **Group Alert:** dungeon group discovery and recruitment alerts.
- **Essentials:** chat conveniences, UI fading and error controls.
- **Stats:** role-aware gear guidance with NEED during loot rolls and UPGRADE on other item tooltips.

Tank and the standalone Auction addon are retired from both package families.

Enable the modules you want under **Apogee Forever** in WoW's AddOns list.
Gameplay modules retain their own settings. Stats evaluates all supported roles outdoors and uses your assigned role or instance fallback in dungeons. Its character-window Gear filter applies only while that window is open. This edition supports Forever only.

Legacy profiles are not imported, and Dungeon Guide is not included.

Install using the [CurseForge listing](https://www.curseforge.com/wow/addons/apogee-party-health-bars)
or a packaged [GitHub release](https://github.com/notify353/ApogeeForever/releases).
For a manual installation, extract all six addon folders into Interface/AddOns.
GitHub source archives are not installable packages.

Contributor documentation: [build workflow](distribution/DUAL_WORKFLOW.md),
[release checklist](RELEASING.md), [client API reference](docs/WOW_INTERFACE_EXPORT.md).

For work across the five addons, use the sibling
[Apogee workspace](../workspace-apogee/README.md) and its
[current handoff](../workspace-apogee/memory/CURRENT.md). These are local sibling
links; the workspace has separate publication status. Distribution authority
remains in this repository.

Stats auction browsing: choose a role/playstyle, set the native equipment-slot
filter, enter Max gold, and click **Find best upgrade**. It starts the native
search, checks buyouts and selects the best affordable upgrade. **Cancel** stops
checking. You review the listing and click Buyout yourself. There is no dice
mode or duplicate slot selector. Role and budget reset each visit; auction
tooltips still show all qualifying roles.
