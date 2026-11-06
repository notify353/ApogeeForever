# Apogee Forever 1.14.15

- Friendly focus assists offensive keybinds: attacks and harmful spells use your friendly focus's living enemy target. An invalid focus target blocks the action; clearing focus or focusing an enemy restores ordinary targeting.
- Before an eligible out-of-combat spell keypress, attempt to re-follow your friendly focus when needed. This never retries on a timer or triggers from spell completion, and ordinary non-focus inputs keep their existing behavior.
- Keep dead targets identifiable with their name and a DEAD label, and clear stale resource displays.
- Hide dungeon controls and alerts until level 10.
- Keep quest objectives visible during combat by default, including for existing installations. Enable Hide quest objectives in combat in Essentials if you prefer the previous behavior.
- Hide incoming damage percentages when the client does not provide usable data.
- Recognize the reviewed Forever build 70790 without the stale unverified-build startup warning.

For WoW Forever 1.60.1. Enable the top-level Apogee addon and the components you want. When switching from DEV, disable the DEV family, enable the public family, and reload; their settings remain separate.

Validated against the matching client API export with automated source and generated-package checks. Full native gameplay, timing/taint and CurseForge-client acceptance remain incomplete.
