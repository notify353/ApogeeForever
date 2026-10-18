# Forever interface authority

Loading safety targets Forever16001, reviewed client1.60.1.70170. Export root:
`C:/Program Files (x86)/World of Warcraft/_classic_beta_/BlizzardInterfaceCode/Interface/AddOns`.
Run `pwsh ./scripts/check-wow-api-export.ps1` before API work.

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
