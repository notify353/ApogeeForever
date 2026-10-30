# Client-specific public releases

Each version directory is a fixed release selection: manifest, source-lock
snapshot, matching API-evidence snapshot and player release notes. The manifest
binds both generated family archives, notes, source and evidence with SHA256.
Only PROD is uploaded. Existing DEV locks, installs and saves remain independent.
Never overwrite a prepared/published version; revise unmerged preparation only
through review, or use the next unused version after publication.

The owner approved early normal Releases for both clients on 2026-10-29. Era may
publish first. This supersedes the previous restriction against publishing Era
and the requirement for complete Forever native acceptance for these exact early
releases. Authorization is recorded against exact packages without marking them
native-tested. Final production-tag approval is still required.

The release matrix runs independent `release-<version>` checks for versions in
pending.json on main, or one prepared version via workflow dispatch. Each job
checks exact child/test revisions, generated client behavior, archive hashes and
the exact CurseForge version. No missing export or failed version lookup falls
back to a different client. Hosted checks verify recorded authority; fresh local
client verification occurs during preparation. Native testing is separate.

The portable release runner explicitly separates three hash-pinned local-export
contracts (Keybinds exported API, Dungeons whisper parser and Essentials native
error handler). They execute the owner's retained Blizzard beta source, which is
not available on GitHub runners and is never redistributed. They still run in the
complete local candidate validation. Hosted output labels them LOCAL EXPORT ONLY,
not passed or native-accepted. A missing or changed test stops classification for
review. Every other child spec and all generated-package suites remain hosted.

From a clean synchronized main checkout, use `scripts/prepare-release.ps1` with
Version, Target (`classic-era` or `forever`), SourcesRoot, ClientRoot,
ChildWorktrees, Notes and Basis. The basis records the owner's real authorization;
it must never be generated as a substitute for consent. Add the version to the
pending queue in the preparation PR. For an existing coordinated tooling branch,
`release_manifest.py prepare` provides the same explicit preparation without
creating a second branch. `validate_release.py` is the exact-source test/staging
entry point. These commands never install or publish.

After review/main integration, `publish-release.ps1` requires successful test,
aggregate and the selected release-<version> check on exact final main, immediate
owner approval and ConfirmProduction. It creates one immutable vX.Y.Z tag. The
existing production Actions environment rebuilds that selection and uploads
identical PROD bytes to GitHub and CurseForge project1608100. Each client has
its own version/tag, ZIP, metadata and receipt; no all-clients ZIP is produced.

Publication journals the first GitHub mutation and the CurseForge POST before
performing them. Any uncertain outcome blocks automatic replay. Preserve the
Actions receipt and inspect remote file IDs, assets and hashes before deciding
manual recovery. Never rerun a failed tag job blindly. A staged receipt is not
proof of upload or approval. After CurseForge approves the file, use the existing
verify-release workflow on that tag with its upload run and exact CDN link to
compare both public downloads. No completed publication is claimed until verified.

The historical native-accepted publisher and frozen v1.14.9 lock remain available
for historical checks. They do not authorize relabeling frozen bytes as a new
unselected release. Later releases need their own manifest or the documented
native-accepted preparation path.
