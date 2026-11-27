## Native loot quality formats - 2026-11-26

Reviewed current ColorManager.lua named |cnIQ tokens and override-aware RGB
palette, plus existing ItemDocumentation GetItemInfo/GetItemQualityColor.
Add the fresh ColorManager reference for Stats. Validate public data, keep
optional lookup failure neutral, and rerender late item data without loot scans.
Native appearance acceptance remains pending after the reported hex-only gap.

## Loot page scrolling - 2026-11-26

Reviewed matching 71139 SimpleScrollFrame and SimpleSlider API documentation
and HybridScrollFrame.lua value-change/offset wiring. Three fresh references
owned by Stats cover clipped child scrolling and native thumb behavior. Only
addon-owned frames and public calculated geometry; native acceptance pending.

## Loot frame styling - 2026-11-26

Reviewed GetFont/SetFont and text shadow methods in the matching71139 existing
Stats-owned SimpleFontString API reference. Reuse the pinned Heals font/palette
conventions locally; no runtime dependency or new native API reference. Quality
rails read existing validated item hyperlink colors. Native visual acceptance
remains separate from offline layout review.

## Loot player class presentation - 2026-11-26

Verified current Forever71139 authority and reviewed playerClass tokens in
LootHistoryDocumentation/Mainline LootHistory, SharedXML/ClassColors.lua native
colorStr setup and FrameXMLBase/Constants.lua localized class names. Record the
fresh ClassColors source and Stats ownership of existing class-color/constants
references. Optional class/color values are validated; old wins remain valid.
No unit inspection or roster guessing. Hover regions reuse current frame and
tooltip contracts. Native fonts/hover acceptance remains separate.

## Crowded loot font measurement - 2026-11-26

Reviewed GetUnboundedStringWidthForText in the matching71139 native font-string
documentation. Existing Stats-owned reference suffices; optional method checks,
guarded calls and public finite width validation preserve runtime availability.
No new API files, saved schemas or loot event contracts. Native fonts/layout
remain separate from offline synthetic geometry and behavior checks.

## Compact loot UI review - 2026-11-26

Verified current Forever71139/268-reference authority. Reviewed native button
SetFontString for plain Stats controls; add Stats ownership of the existing
SimpleButtonAPIDocumentation reference. Existing frame/font/texture APIs suffice.
History grouping is display-only; saved records and native loot contracts stay
unchanged. Native visual acceptance is separate from offline geometry checks.

## Loot test preview review — 2026-11-26

Verified current Forever71139 authority before work. Reviewed native
Blizzard_SharedXML/Shared/Tabs/RightSideTab.lua SetOwner/SetText/AddLine sample
presentation; record its fresh hash for Stats. Preview data and clock are purely
local; no native loot APIs are replaced or native events emitted. Existing button,
frame, combat-event and cleanup contracts are reused. Native acceptance is pending.

## Loot panel review — 2026-11-26

Matching Forever71139/16001 authority verified before work. Reviewed native
LootHistory structured encounter/drop updates, confirmed winner and all-pass
fields, roll-state enums, the FrameXML family selection and Camelot override.
The panel uses public validated records only; no chat parsing or roll actions.
Native InputUtil tooltip ownership and Interpolator timer cancellation support
cleanup. Add these references and Stats ownership of existing item/frame/font/
timer contracts to current live evidence only. Historical selections and Era
remain unchanged. Native loot timing/layout/reload acceptance remains pending.

## Reviewed Forever71139 export - 2026-11-25

Active wowf metadata and Wow.exe agree on1.60.1.71139/interface16001. All260
prior references postdate the executable and remain byte-identical to71037.
The current inventory adds DurationTextBindingSharedDocumentation and
DurationTextBindingObjectAPIDocumentation for the Battle Shout countdown.
Reviewed native AuraContainer helpful/player spell-ID filtering and duration
text/color handoff; these secure native displays own restricted aura state.
Only current live evidence/candidate and build-warning acknowledgments advance.
Historical manifests, locks, exports and Era stay unchanged. Native acceptance
of the new countdown remains pending.

## Reviewed Forever71037 export — 2026-11-20

Owner refreshed the current live export. Active wowf metadata and Wow.exe agree
on1.60.1.71037/interface16001. All258 reviewed API/source references postdate the
executable and remain byte-identical to70959. No API contract changes were found.
Update current release authority and reviewed-build notices only. Preserve frozen
70959 selections and every historical release. Native acceptance remains limited
to the owner's reported DEV.2 Gear removal and error-free bag clicks; warning-only
changes in other components are not new native gameplay acceptance.

## Stats scope and loot-settings review — 2026-11-20

Forever 70959/16001 verifies all 258 existing references. Reviewed native
MenuUtil.CreateContextMenu and the Settings canvas-subcategory implementation
guide against the export. Stats uses the existing ApogeeUI RegisterSettings
contract to expose only the session loot fallback, independently of tooltip
startup. The character selector and visibility hooks are removed. Ordinary
comparison defaults to all roles; explicit AH scopes and LOOT scope own their
policies. No new native API or loading-graph change. Source pin advances to
ef79cfecf55c6aa9dc0629b47b0ba2866054dd5e; historical evidence stays frozen.
Native visual/timing/taint acceptance remains pending.

## Stats callback recovery review — 2026-11-20

Live Forever 70959/16001 still verifies all 258 recorded references. Reviewed
ItemDocumentation GET_ITEM_INFO_RECEIVED and ITEM_DATA_LOAD_RESULT: both carry
itemID and non-null boolean success and may fire synchronously. Stats ignores
unrelated/failed results, batches relevant updates on its own frame, and ignores
completion reentry during rebuilding. Existing tooltip clear/hide, font restore,
and RebuildFromTooltipInfo methods are retained with failure cleanup. Auction
provider restoration remains conditional on ownership. No new API is introduced;
the current evidence source pin advances to the checked Stats fix. Historical
release evidence is unchanged. Native bag-click acceptance remains pending.

## Marker defaults and current authority - 2026-11-17

Reviewed live Forever1.60.1.70959 against the refreshed export. All248 prior
references are fresh;247 match70938. AddonList changes only the character-name
label to NameUtil.FormatUnitNameForDisplay; GUID enable selection is unchanged.
Added marker presentation reference evidence; existing SecureTemplates raidtarget
and RaidMarkers contracts support native user-input toggles without addon Lua
marker inspection. Current candidate pins marker defaults and reviewed-build
notices; historical locks and release manifests remain immutable. Native
acceptance remains pending.

# Forever interface authority

## Current live client: 1.60.1.70862 (2026-11-08)

The owner refreshed the export. Active wowf metadata and executable version agree;
all244 prior references postdate the executable and retain their70790 hashes.
Three newly recorded Heals references cover aura slots, duration-text options and
the native priority table, bringing the inventory to247. Timer/cleanse/native
tooltip/secure-action contracts remain compatible. See the live review record.
The new candidate uses verified export installation; prior deferred receipts and
immutable release authority remain historical. Native gameplay acceptance is separate.

## Previous live client: 1.60.1.70790 (2026-11-04)

The freshly exported launch client verifies 244 references and its executable.
Ten prior references changed; the newly selected Camelot action-button override
is included. See the [launch review](../distribution/forever/README.md).
Existing restricted-damage handling and native whisper/menu contracts remain
compatible. No gameplay source change was required. Native testing is explicitly
skipped at the owner's request and remains unclaimed.

## Previous live client: 1.60.1.70707 (2026-10-31)

The matching live export verifies 243 references against the current executable.
The reviewed contract changes and quest-text sources are recorded in
[live authority](../distribution/forever/README.md). The current Forever candidate
and its new release selection bind this evidence; historical selections retain
their original authority. Separate Forever native acceptance remains unrecorded.

## Previous live client: 1.60.1.70685 (2026-10-29)

The owner refreshed the export after the client advanced past70658 to70685.
Executable metadata and active wowf build agree; all239 references postdate it.
238 match the prior review. Nameplates.lua now always offers the rarity-icon
checkbox, removing the ShowRarityIconInfoDisplayOption conditional. The retained
older source matches the prior recorded hash; no Apogee-used API signature changed.
Separate live evidence and future candidate metadata advance; Era and frozen beta
remain unchanged. Current native gameplay acceptance is still not claimed.

## Previous live client: 1.60.1.70634 (2026-10-27)

`pwsh scripts/check-wow-api-export.ps1` now checks live product `wowf` in
`_forever_`, using `Wow.exe` and the isolated future candidate's exact source
pins and [live evidence](../distribution/forever/README.md). All 239 unique
references must match and postdate the reviewed executable. No missing-client
or beta fallback is allowed. Run `scripts/test-live-forever.ps1` for full
candidate validation. Native acceptance remains separate.

The frozen release and historical notes below retain beta authority. Use
`check-wow-api-export.ps1 -Client Beta` for that legacy baseline; `test-local.ps1`
selects it explicitly. `record-wow-api-export.ps1` remains a beta-only recorder.
Do not use it to refresh live evidence. Review live changes and update the
separate evidence and future lock together, without rewriting frozen history.

## Historical beta authority

Loading safety targets Forever16001, reviewed client1.60.1.70170. Export root:
`C:/Program Files (x86)/World of Warcraft/_classic_beta_/BlizzardInterfaceCode/Interface/AddOns`.
Its historical checker is `pwsh ./scripts/check-wow-api-export.ps1 -Client Beta`.

The October 1, 2026 owner export is newer than the installed 70170 executable.
Four recorded references are byte-identical to the 70124 baseline. The Unit
documentation hash changed; the current UnitGUID contract was reviewed directly:
one unit token, a nullable WOWGUID, and restricted identity/argument annotations.
FamilyGate already checks the player GUID for restricted, missing and malformed
values before use. AddOnList's matching GUID/enable-selection source is unchanged.
The prior complete Unit source was not retained here, so this records a current
contract review, not a claim that every Unit API is unchanged.

Auction's item metadata/stat, hyperlink/item-key tooltip and tooltip-line enum
contracts were also inspected in this export for its reader work. Missing returns
remain possible and restricted values require checking. No runtime guard, TOC,
Interface number, child source pin or transform changes are needed for this
authority refresh. Native gameplay acceptance on 70170 remains unverified.

The September 29, 2026 refresh was exported after the installed 70124 client
update. All five recorded loading-safety reference files are byte-identical to
the reviewed 70009 export. The current candidate build pin advances to 70124;
Interface 16001, child source pins, TOCs, transforms and runtime remain unchanged.
Historical source locks retain their original build. This source review does not
establish native gameplay acceptance on the updated client.

Recorded AddOns, AddOnConstants, FrameScript and Unit generated documentation
establish metadata/load/enable APIs, enums, secret inspection and UnitGUID.
Blizzard_AddOnList/AddonList.lua establishes current-character GUID selection,
Group metadata, group context controls and reload handling. Use this matching
local source before online references or memory.

After client updates, stop API work until the owner exports fresh source with
`exportInterfaceFiles code` in the developer console. Do not operate the game.
Review affected APIs/source, then run `pwsh ./scripts/record-wow-api-export.ps1
-ConfirmReviewed` and commit hashes with compatibility changes. Never refresh
hashes merely to suppress a stale check. Build/interface changes require explicit
code/lock/TOC review.

Without local WoW, validation checks baseline consistency only and reports the
installed-client authority check unavailable. This does not prove current API
review. Native startup timing remains a separate live acceptance requirement.


## Native Forever identity correction (October 1)

The owner's screenshot is a real Keybinds startup rejection, not a status label.
The fresh native export assigns WOW_PROJECT_ID = WOW_PROJECT_CAMELOT (18), while
five child adapters required project 1. Earlier patch-only tests held that stale
identity constant and missed the defect. The reviewed ProjectConstants base,
Camelot override and selecting TOC are now included in the authority hashes.

All six children now accept native Forever identity and/or their legacy Forever
identification without an exact-interface expiry. Native identity accepts older
and future version/interface metadata; mandatory API checks, other-family
rejection and DEV/PROD admission remain. Six child suites and generated client
regressions cover the native identity, interface revisions and missing APIs.
The new source regressions fail against all five old project-1 adapters.
Export/install provenance remains pinned; runtime version numbers do not expire
features. Native acceptance of the corrected package still requires owner testing.

## October 2 client refresh

Owner refreshed the export after updating to 1.60.1.70205. All eight recorded
loading-safety source hashes match the prior review exactly, and the fresh
files postdate the executable. Interface remains 16001. Reviewed Heals threat
and nameplate contracts; matching-source tests pass. Advance only the current
candidate build pin; historical locks and sibling runtime pins stay unchanged.

## October 10 client refresh

The owner refreshed the export after updating to 1.60.1.70338. All eight recorded
loading-safety source hashes remain byte-identical to the prior review, and each
fresh exported file postdates the installed executable. Interface remains 16001.
Only current installation provenance advances; historical locks and sibling pins
are retained. Generated adapter tests distinguish each pinned warning baseline
from current-build capability acceptance. Native acceptance remains pending.

## October 10 shared Settings category review

The matching 70338 Settings wrapper, inbound adapter, SettingsPanel, CategoryList
and Category mixin were reviewed and added to the authority hashes. Categories
receive numeric IDs. Despite its parameter name, Settings.GetCategory uses ID
comparison, not display-name lookup. RegisterCanvasLayoutSubcategory creates a
native child attached to its parent; registering the child refreshes the category
list without another top-level entry. A session-only, family-local registry shares
the parent between independent loaded addons. The DEV lexical map explicitly
isolates ApogeeSettingsRegistry as ApogeeDevSettingsRegistry in the five Settings
owners. This is not a saved-variable or marker runtime identity.

## October 10 settings typography review

The matching Shared/FontStyles.xml confirms the native normal large/small title
and heading templates, and white highlight-small labels. It is recorded in the
authority hashes. Settings-only help/disabled colors are explicit overrides;
no shared HUD font objects are changed. Apogee Dungeons is an exact audited
Group Alert settings label with an isolated DEV display spelling.

## Forever 70450 review - 2026-10-17

Reviewed the fresh installed Forever 1.60.1.70450 export; interface remains 16001.
Recorded sources postdate WowB.exe. Changed Unit/aura contracts retain nullable
and restricted returns; existing guarded adapters and native display sinks remain
required. UNIT_SPELLCAST_SUCCEEDED keeps unit/cast/spell payloads and adds an
optional trailing castBarID, which existing handlers do not consume. Settings
canvas registration still delegates to SettingsInbound. Native UP/TOGGLEAUTORUN,
OPENALLBAGS and sound binding actions retain their reviewed behavior. Mouse focus,
frame alpha/hit rectangles, minimap roots and native CVar names remain compatible.
No gameplay adapter change was identified in the reviewed contracts. Warning and
export baselines advance; native acceptance on the new client is separate.
Historical source bodies are not retained, so changed hashes establish a need for
current-contract review, not a complete old/new source diff. Detailed local hash
inventory: C:/Temp/apogee-api-20261017/export-review.json.

## Optional default spells (2026-10-17)

Reviewed current 70450 SettingsPanel:GetLayout and SettingsCanvasLayoutMixin:GetFrame
to add the control to a parent created by any loaded settings owner. Reviewed
SystemTime GetServerTime, a non-null numeric timestamp, for reconciling explicit
per-character choices when an independently disabled consumer returns. Layout
and SystemTime source hashes are now recorded. Existing registry identity mapping
is sufficient; no new global, SavedVariables name, TOC or gameplay transform.

## October 17 Stats auction budget review

Verified the installed Forever 1.60.1.70450 / 16001 export with the required
checker. Reviewed AuctionHouseDocumentation item-key/detail-result contracts,
SendSearchQuery, full-result/pagination APIs and item-result event payloads.
Reviewed native BrowseResultsFrame, Frame SelectBrowseResult/QueryItem,
SearchBar GetLevelFilterRange, ItemBuyFrame and ItemList selection methods.
Browse minPrice is not treated as a buyout; item-search buyoutAmount is nullable.
Separate owned results and native level bounds are preserved. Selecting an item
opens its view; SetSelectedEntryByCondition invokes native selection, not purchase.
Runtime carries no transaction calls. Source review does not establish native
layout, server timing or taint acceptance.

### Role-first/native slot correction

Reviewed matching CategoriesList SetSelectedCategory/GetCategoryFilterData and
BrowseResultsFrame OnCategorySelected/OnBrowseSearchStarted. Native category
selection changes UI/filter state before a new browse search; cancel old checks
immediately and require that new search before selection. Stats never sets a
native category or duplicates its slot selector. Reviewed EditBox SetEnabled
for locking Max gold until the explicit role choice. Native acceptance remains
pending; all prior evidence stays historical.

### One-action upgrade search

Reviewed Forever 70450 SearchBar:StartSearch and Frame:SendBrowseQuery. The
native entry point retains search text, level range, checked filters and category.
BrowseSearchStarted is synchronous; a declined native search cannot reuse old
results. Item selection remains the previously reviewed native selection path.
No transaction call is added. Owner layout/timing acceptance remains pending.

### Browse-first explicit selection

Reverified installed Forever 70450 / 16001 and reviewed BrowseResultsFrame
OnBrowseSearchStarted/OnCategorySelected. Native Search owns the browse query;
role filtering processes its results without calling SearchBar:StartSearch.
Optional cap changes restart listing checks, never navigation. The reviewed
SelectBrowseResult path is reachable only from the Select best click handler.
No new API dependency or transaction call. Native acceptance remains pending.

### Explicit toggle, all-role scope and native slot gate

Reverified installed Forever 70450 / 16001. Reviewed CategoriesList
GetCategoryFilterData/GetCategoryData, shared AuctionCategoryMixin:AddFilter,
Camelot armor category construction and AuctionHouseFilter inventoryType.
Only an explicit single inventory slot enables best; Chest/Robe normalize to
one slot. Missing/restricted/multiple slot filters fail closed. Categories with
only class/subclass filters remain browseable without best selection. All roles
uses existing Stats contexts; ranking requires one role/playstyle. No native
filter mutation, transaction API or new identity transform is introduced.

### Category-change filtering continuity

Reverified Forever 70450 / 16001. Reviewed CategoriesList:SetSelectedCategory
and BrowseResultsFrame OnCategorySelected/OnBrowseSearchStarted/UpdateBrowseResults.
A category change modifies native filter/header state without guaranteeing a new
search. Keep the filtered provider installed with empty rows until native Search;
ignore old result snapshots while waiting. No new API or native filter mutation.

### Armor/Weapons availability

Reverified Forever 70450 / 16001. Reviewed CategoriesList:GetSelectedCategory,
shared AuctionFrame_CreateCategory and Camelot category roots. Resolve the root
through AuctionCategories and compare its native localized name with the Armor/
Weapons constants; descendants inherit root availability. No fixed indexes or
English-label matching. Missing/restricted root data disables custom filtering.
Remember the dice preference separately from category availability. No new native
mutation or transaction API. Shield Armor-first policy remains included.
