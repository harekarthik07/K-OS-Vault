# _meta

Config and state for the vault. Read by `_tools/kos_capture_hub.py`, not by Obsidian.

| File | What it is |
|---|---|
| `domains.json` | The ONLY place to add/rename domain buckets and concept aliases. Edit, restart the hub, done. |
| `.env` | Your API key. **Gitignored.** Copy `.env.example` → `.env` and fill it in. |
| `concept-registry.md` | Auto-appended when a concept is promoted to `04 Knowledge/`. Don't edit by hand. |
| `concept-mentions.json` | Mention counter per concept — a card only spawns on the 2nd sighting. Tracked in git so counts follow you across machines. |
| `.active_project` | Which project the hub is capturing into. Gitignored (per-machine). |

Never put actual notes here.

## Adding a new domain

Add a key under `domains`, then create the matching folder in both
`04 Knowledge/` and `06 Resources/`. Folder names must match the key exactly.

## Killing duplicate concepts

If Harvest shows `Tj` and `Junction Temperature` as separate cards, add the
variant to `concept_aliases` under the canonical name, delete the stray card,
and future captures will collapse into one.
