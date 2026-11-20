# Group Alert bug sweep - 2026-11-19

Reviewed installed DEV1.14.19-dev.3 and its owning Group Alertd31e9e8. Four
defects reproduced with failing tests before changes:

1. Reply, Invite and location callbacks read the current pooled row at mouse
   release. A new incoming message or scroll between press/release could act
   on a different sender. Bind to the entry at press and cancel on replacement,
   collapse or close. Fresh deliberate clicks still work; action-time combat,
   data-access, party-permission and invite-debounce checks remain.
2. Reused or hidden rows could retain the preceding sender/message/location
   tooltip. Clear owned tooltips during refresh/reuse/close, preserving tooltips
   belonging to other UI. Expiring Who metadata cannot leave a stale zone tooltip.
3. Changed dungeon level ranges with unchanged names skipped chat reclassification
   on listing updates. Track actual range revisions and invalidate cached chat
   eligibility when ranges change. Unchanged ranges keep the fast path; no search,
   sound or lifetime reset is introduced.
4. A public localized class name was discarded when its optional class token was
   absent or restricted. FriendList.WhoInfo.filename is nullable. Keep readable
   labels independently; use known tokens for color only, without guessing.

Prepared child156bcc6fb7bd93389283e4d1bd8709a24ce573b2 and DEV1.14.19-dev.5.
Only Group Alert gameplay changes; other child/shared pins match installed DEV.3.
Concurrent priest DEV.4 is a separate uninstalled candidate and is not included.
An installation must reconcile any subsequently installed changes before writes.
Historical locks/releases and installed files are untouched by this preparation.

New regression suite whisper_sweep_spec.lua runs on source and generated PROD/DEV.
Source54 Lua files/32 specs and29-file source archive pass; targeted failing logs
are retained in external task storage. Central coordinated validation, fresh
Forever70959 authority255 references and installation preview are recorded there:
`C:/Dev/WoW/local-task-archives/apogee-whisper-sweep-20261119`.
The existing APIs, identity transforms, runtime paths, TOCs and saved fields are
unchanged. No layout redesign; only interaction/metadata invalidation changes.
Native timing, tooltip rendering and click behavior still need owner acceptance.
These findings do not establish the cause of the reported whole-client glitch.

Normal checked running-client DEV installation is eligible only after its fresh
inspect-only checks pass and immediate explicit owner approval. Use the latest
installed whisper receipt; retain a new verified rollback backup. No automatic
installation, private-save access, game operation, PROD write, push or publication.

Completed validation:54 Lua parses/32 Group Alert specs,29-file source archive,
generated PROD/DEV regressions, Era and full frozen distribution suites pass.
Fresh Forever255/Era99 references verified; candidate receipt retains
nativeAccepted:false. The historical child wrapper stops at its removed
foreverBeta gate; coordinated validation supplies the actual live authority.
Generic central unittest discovery finds no tests; the documented runner invokes
its explicit test entry points. Read-only installer preflight passes the checked
live-update path:10 writes (four existing Group Alert Lua paths and six TOCs),
17 preserved documents, no discovery changes or restart requirement. No writes
performed. DEV ZIP SHA256:
`1b259349527ba3514b01c447c43b92efe6ec9235d9feac6a6b62c13b66485efb`.
