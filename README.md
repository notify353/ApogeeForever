# Apogee Forever

## Current runtime policy — 2026-10-31

Owner policy supersedes earlier runtime version and package-verification gates:
on Classic Era and Forever, in DEV and PROD, never disable an addon or feature
solely because client/build/interface text, package versions, advertised API/schema
revisions or legacy/unverified metadata differ. Select the native client adapter
and check actual methods and data contracts. Preserve combat/protected-action,
restricted-value, failed-initialization, incompatible saved-data and actual
DEV/PROD ownership safeguards. Do not infer binding ownership from APHB metadata.
Exact exports, immutable source pins and installer/release validation remain
offline development/distribution requirements, not runtime expiry rules.
Current policy implementation is coordinated by ApogeeForever's
`distribution/RUNTIME_CAPABILITIES.md`; historical release bytes remain frozen.

Client-specific public releases for Forever and Classic Era are being prepared
under this existing project. See [release selections](distribution/releases/README.md)
and each version's player notes for support and testing status. The release files
use separate client metadata; choose the file for your WoW instance. Preparation
does not mean the new files have already been published.

An isolated, unpublished [Classic Era DEV candidate](distribution/era/README.md)
is available on the Era development branch. Its pins, API evidence and installer
target are separate; the Forever beta baseline below remains frozen.

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
Current unreleased Forever candidate: [live validation](distribution/forever/README.md).

For work across the five addons, use the sibling
[Apogee workspace](../workspace-apogee/README.md) and its
[current handoff](../workspace-apogee/memory/CURRENT.md). These are local sibling
links; the workspace has separate publication status. Distribution authority
remains in this repository.

Stats auction browsing: click the left-side dice to enable upgrade filtering.
Then optionally narrow by Max gold and role (All roles by default). Dice off
restores normal native results. Select best requires a specific native equipment
slot, one role/playstyle, and complete checks; the status explains missing choices.
Click it to select a freshly verified buyout. Buying remains manual. Each visit
starts off with no gold cap and All roles; native filter preferences are preserved.

Filtering is available only in Armor and Weapons and their subcategories.
Elsewhere, normal results appear with dimmed/disabled controls and guidance.
Returning restores the dice preference, gold and role; the filtered list waits
for a matching native Search.

Stats ranks Warrior and Paladin tank shields by Armor, then Stamina, followed by
existing defensive tie-breakers. Warrior tank weapons prioritize Weapon DPS, then
Stamina and existing tie-breakers within the current shield, two-handed or trained
dual-wield setup. Hand restrictions are preserved; cross-layout switches are not
recommended. Other equipment and role priorities are unchanged.
