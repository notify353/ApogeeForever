# Era Stats candidate

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
