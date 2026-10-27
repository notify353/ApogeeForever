# Era errors before combat - October 25, 2026

The owner clarified that the unwanted errors occur **before combat**. Era.4-6
deliberately relay every error outside combat because the shared suppression
condition requires InCombatLockdown. On a clean account, a first cooldown error
is already learned with suppression checked, but that condition still allows
Blizzard's text/audio handler to run. This is the scope mismatch reported here,
not an initialization failure or a requirement to encounter the error twice.

Earlier speculation about GetGameMessageInfo returning unexpected names was not
confirmed. Fresh native VoiceUtils uses its first return as a global string key,
consistent with the existing symbolic-name policy. No speculative classifier or
native-ID changes are included.

## Correction

Era.7 pins Essentials `bae7a1c159bbe12154fc90d7b5e72d7426142729`.
The private Era adapter sets suppressErrorsOutsideCombat. The shared error relay
honors that optional policy when deciding whether to drop an already checked
error; absent the flag, Forever retains its existing combat-only behavior.
Both the main settings label and learned-error hint describe Era's actual scope.

The enabled feature takes ownership of UI_ERROR_MESSAGE from UIErrorsFrame,
learns the error ID/message, applies its initial default, and drops checked errors
before they reach the captured native text/audio handler. Unchecked errors are
relayed once. UI_INFO_MESSAGE and system messages remain Blizzard-owned. Disabling
the feature restores the prior event registration. These mechanics are unchanged.

Useful inventory, equipment, reagent, quest, interaction, interruption and unknown
types retain their existing visible defaults. Explicit checkbox choices and the
main switch are preserved; eraErrorDefaultsVersion remains 1. No additional reset,
settings import, private-save inspection or global API replacement is involved.
All other child pins and all frozen Forever pins remain unchanged.

## Evidence and verification

The new source/generated regression starts with **no SavedVariables**, runs full
login, and sends a first pre-combat cooldown error. It failed on Era.6 and passes
with this correction. It also exercises first combat errors, text/voice/sound,
useful/unknown messages, explicit unchecks in both states, saved-choice reload,
global disable/re-enable, Defaults and the actual Era label/hint. The generated
test runs the fresh Classic UIErrorsMixin under mocks, not just a synthetic sink.

Essentials checks: 48 tracked/new Lua parses and 29 specs passed. Matching client
1.15.9.70003 / 11509 and all 78 selected export references verified. Full central
Era/frozen results and preservation evidence are retained in the directory below;
native user acceptance remains separate.

Full central validation passed: all 171 child specs, nine Era tests, 76 admission
scenarios, four generated adapters and all 77 frozen Forever offline tests.
Both rebuilt Forever ZIPs are byte-identical; all 1,477 Forever addon files,
eight frozen repository files, 275 archived files and 114 Era.6 installed files
remain unchanged before installation.

Artifact: `Apogee-1.14.8-era.7-DEV.zip`, SHA-256
`2e1027d55c1dfbfff4ef0860bd80eb5c36556d89b57751c984dcd859a33fd217`.

Evidence/task record: `C:/Temp/apogee-era-20261024/error-scope-20261025/`.
Includes before hashes, child/aggregate logs, generated packages, preflight and
preservation results. No push, main integration or publication is authorized.

## Installation and acceptance

Initial preflight found Era running and proposed nine writes (four Essentials
runtime files and five version TOCs), preserving seven README files. A closed
client was required by the original Era installer. Chain from the installed Era.6
receipt at
`C:/Dev/WoW/local-install-backups/apogee-era-archive-sweep-20261025/transaction.json`.

User acceptance: with the main switch on, a checked cooldown/range error should
stay hidden before combat as well as during combat; inventory and unchecked
messages should remain visible. Toggling the main switch off must restore them.
No game controls or addon enable preferences are operated by the agent.

The owner subsequently explicitly rejected the closed-client requirement and
authorized installation while Era runs. The central CLI now supports
`--allow-running-era-update` for a verified existing Era DEV receipt only, with
unchanged runtime paths and TOC metadata/order except Version. Normal defaults,
first installations, discovery changes and rollback still require closure.
Atomic replacement and all source/API/artifact/backup checks are retained. The
opt-in is rejected for the default Forever target. No running process is operated.

After this installer change the complete central runner passed again: 171 child
specs, now 11 Era tests (including live-update/refusal and CLI isolation tests),
76 admission scenarios, four generated adapters and 77 frozen Forever tests.
Era.7 and both frozen Forever ZIPs are byte-identical to the preceding validation.
Evidence: `validation-live.log` and `live-install-preview.json`.

## Installed with Era running

Under the owner's explicit live-install instruction, Era.7 installed successfully
with `liveUpdate=true` and `clientRunningAtPreflight=true`. Latest receipt/backup:
`C:/Dev/WoW/local-install-backups/apogee-era-error-scope-20261025/transaction.json`.
Nine writes verified; all 114 previous files backed up and all 114 installed files
verified (107 payload receipt entries plus seven preserved README files). All
1,477 Forever addon files, eight frozen repository files and 275 archive files
remain unchanged. See `install-verification.json`. The user must `/reload` to load
the new code; the agent did not operate the game. Native acceptance is pending.
