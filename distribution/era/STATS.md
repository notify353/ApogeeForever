# Era Stats candidate

## Era.24 reliability audit — 2026-10-27

The owner's Kang tooltip showed two anonymous Weapon DPS lines. The old shared
renderer replaced role names with atlases that did not display in Era. Era now
provides plain role/playstyle text and groups identical reasons. A screenshot
fixture reproduces the exact visible Kang text; filtered-row tooltips explicitly
use the selected role while ordinary item/loot scope remains unchanged.

Additional reproduced failures: duplicate result events restarted evaluation;
late item data did not recover pending rows; recycled rows retained old hover
content; scrolling between mouse press/release could select a different row;
model cleanup could abort event cleanup. Fixes keep the current-page-only design,
bound data-driven retries, make startup idempotent, and protect independent cleanup.
Final fault injection also reproduced partial UPGRADE text after a rendering
exception. The Era renderer now restores native content and becomes inert until
reload, reporting once while leaving the rest of Stats active.

The test harness now admits only explicit native methods rather than inventing
no-op APIs. Tests retain/reuse tooltip font strings, deliver native refreshes on
both sides of addon events, clamp native scrolling and verify final-row selection.
Future Forever remains pinned separately; full package/archive equality must be
verified. Synthetic checks do not prove native visual acceptance or absence of
all defects. Owner acceptance must cover the screenshot, hovered scrolling,
role changes, current-page navigation, late data and native purchase handoff.

## Era.23 simplification — 2026-10-27

Owner requested a simple Era-only role upgrade filter and explicitly selected
current-page-only operation. Native Search, sorting and Next/Previous remain.
The dice opens a role/playstyle filter for that page; unknown comparisons are
omitted and counted. Clicking an upgrade turns filtering off and returns to the
native list with the verified current row selected for manual purchase.

Removed Max gold, Select best, automatic multi-page scanning, query ownership
tracking and selection re-querying. Stats issues no auction queries or purchases.
Era/AuctionScan.lua retains its loading path but contains only bounded page
evaluation. Search/page/filter changes, hidden Browse, combat and world changes
invalidate pending results. Existing tooltip fixes and shared scoring remain.

Era's pin advances independently. The future Forever lock, generated package
contents and installed beta remain unchanged. The candidate validator supports
separate exact test checkouts via --future-child-worktrees, avoiding a forced
Forever pin change just to validate an Era update. Tests verify no automatic
queries, native paging/selection, listing changes, role changes, bounded missing
data and cleanup failures. Native UI acceptance is still required.

## Era.22 tooltip correction — 2026-10-27

The owner reported flicker and showed recommendation lines outside the tooltip
border. The Era adapter queued rendering on a separate frame after native tooltip
sizing, without recalculating bounds. Depending on frame update order, native
periodic rebuilds could also erase the recommendation for one drawn frame.
The adapter now flushes pending work in the tooltip's OnUpdate hook, after its
native script, and calls Show to recalculate bounds when lines were appended.
Nested setters still settle before rendering; clearing/hiding cancels pending
work. The matching Classic GameTooltip XML and Lua in the 94-file authority
confirm its native OnUpdate rebuild sequence. Forever runtime is unchanged.
Generated regressions cover native rebuild timing and sizing; native visual
acceptance still requires the owner to hover real inventory and loot items.

## Era.21 correction — 2026-10-27

The missing auction dice was reproduced: Era.20 required GetAuctionSortColumn,
which is local to Blizzard's auction source and unavailable to addons. Era.21
uses public GetAuctionSort("list", 1). Tests no longer invent the private global;
both already-loaded and load-on-demand auction startup are exercised. Search
click ownership now survives mouse-down/release across frames and clears when
the press is abandoned. No tooltip/scoring or Forever runtime behavior changes.

Owner refreshed the 1.15.9.70576 export. All 94 selected API files are identical
to the reviewed 70003 sources and postdate the new executable. The Era package
authority advances to the new exact build/hash; historical locks remain readable
but cannot install against a different client. Frozen Forever pins stay unchanged.

## Initial Era.20 implementation

Era.20 adds ApogeeStatsDev to the embedded-master package. Inventory version 2
requires exactly the five existing gameplay children; absent/version-1 inventory
retains the exact historical four. Old receipts and rollback archives remain
valid. New Stats installation changes discovery and requires Era closed and a
full restart. No saved-data migration or enable-preference changes are allowed.

The 1.15.9.70003 evidence includes fresh selecting Classic AuctionUI/GameTooltip
and Vanilla TalentUI TOCs plus their implementations and item/tooltip contracts.
Era uses the Classic auction list, 50 rows per page, QueryAuctionItems throttled by
CanSendAuctionQuery, AUCTION_ITEM_LIST_UPDATE and fresh native row selection.
Modern C_AuctionHouse and C_TooltipInfo getters are not substituted into Era.
The scanner uses a hidden GameTooltip and explicitly supported English patterns.

Stats owns the private Era adapters; the comparison algorithm and ranking remain
shared. Era feral weapons do not score raw weapon DPS; rating labels and automatic
Hunter melee inference are omitted. Unknown passive stat text blocks comparison.
Procs, use effects, set bonuses and caps remain outside the baseline policy.
See the child's Era/README.md for user behavior and native acceptance.

Generated tests exercise the actual Era chunks, loader denial, scanner/parser,
Gear/tooltip startup, nested loot setters, paging, throttling, cancellation,
price/suffix changes, role/budget changes during selection, native UI ownership
and cleanup. Both future Forever families retain their existing Stats suites.
The aggregate validator also explicitly runs Stats' Python loader contract.

Offline fixtures do not certify native timing, tooltip coverage, taint or auction
layout. Owner acceptance must include real loot, inventory/merchant links,
multi-page searches, changed listings and manual native purchase controls.
All new packages remain unpublished DEV candidates; the installed Forever beta,
release pins and historical archives are unchanged.
