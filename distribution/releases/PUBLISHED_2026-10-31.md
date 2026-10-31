# Era 1.14.12 and Forever 1.14.13 published

The owner explicitly approved pushing/integrating all seven reviewed repositories
and publishing both versions once checks passed. Both are now normal public
Releases on GitHub and CurseForge project1608100. Publication and verification
used the existing guarded Actions workflows; no upload was retried.

| Client | GitHub release | CurseForge file | Upload run | Public-byte verification |
| --- | --- | --- | --- | --- |
| Classic Era 1.15.9 | [1.14.12](https://github.com/notify353/ApogeeForever/releases/tag/v1.14.12) | [9385342](https://www.curseforge.com/wow/addons/apogee-party-health-bars/files/9385342) | [Succeeded](https://github.com/notify353/ApogeeForever/actions/runs/41216690184) | [Succeeded](https://github.com/notify353/ApogeeForever/actions/runs/41216944817) |
| Forever 1.60.1 | [1.14.13](https://github.com/notify353/ApogeeForever/releases/tag/v1.14.13) | [9385370](https://www.curseforge.com/wow/addons/apogee-party-health-bars/files/9385370) | [Succeeded](https://github.com/notify353/ApogeeForever/actions/runs/41216837236) | [Succeeded](https://github.com/notify353/ApogeeForever/actions/runs/41216966801) |

Both immutable tags point to release commit
626640e01679c012ca6e77e720e8141347191d9b, integrated through
[distribution PR192](https://github.com/notify353/ApogeeForever/pull/192).
Its tree equals reviewed preparation d33b335. Before tagging, test and aggregate
checks and both [release-specific checks](https://github.com/notify353/ApogeeForever/actions/runs/41216539505)
passed on that exact commit. [Normal main validation](https://github.com/notify353/ApogeeForever/actions/runs/41216706447)
passed again between tags, preserving the release helper's latest-check guard.

Authenticated publication resolved Era upload version16630/type67408 and Forever
17053/type88568. GitHub releases are neither draft nor prerelease; their notes,
asset names and digests match the immutable selections. Both verification
receipts report published-and-byte-verified with the following public hashes:

- ApogeeClassicEra-1.14.12.zip:
  fcade6dbc8e227af8d3c161609fdcdb90bc9b8ae271d9b1e8962c5de97dddfb3.
- ApogeeForever-1.14.13.zip:
  594f2032e733679ff5851d80b913ca8d2e286b1ffa705035eced091caa9f0913.

Direct public downloads also returned HTTP200 and those exact hashes:
[Era](https://mediafilez.forgecdn.net/files/9385/342/ApogeeClassicEra-1.14.12.zip)
and [Forever](https://mediafilez.forgecdn.net/files/9385/370/ApogeeForever-1.14.13.zip).
This establishes public file availability, not merely upload submission.

The five exact gameplay pins remain reachable on their merged child main
branches; workspace integration preserves its newer remote history. Final
coordination records contain the seven PRs and retained local evidence.

No installed DEV/PROD folder, enable preference or private save was changed.
User-reported native acceptance remains scoped to Era DEV. Separate Forever
native and actual CurseForge-client installation testing remain unrecorded;
the original nativeAccepted=false and curseforgeClientTested=false values were
not rewritten. Worktrees, initial/final archives and rollback backups remain.
