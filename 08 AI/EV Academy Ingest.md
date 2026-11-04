# EV Academy — ingest rules for Claude Code

Karthik's mentor sessions run in Claude chat and end with an `=== EV-ACADEMY HANDOFF ===` block (format: `03 Projects/EV Academy/Resources/Study Protocol.md`). When he pastes one and says **ingest**:

1. **`=== FILE: <path> ===`** → create the note at that vault path, content as-is.
   - Concept already exists in `04 Knowledge/concepts/`: don't overwrite. Merge new material into the matching sections, add the new session to `sources`, and raise `status` only (seedling → budding → evergreen), never lower it.
   - Gotcha already exists: append a `## Seen again YYYY-MM-DD` line.
2. **`=== DAILY LOG ===`** → add under `## YYYY-MM-DD` in `03 Projects/EV Academy/Daily Log.md` (create the heading if missing).
3. **`=== QUESTIONS ===`** → append to `## Open` in `03 Projects/EV Academy/Questions.md`.
4. **`=== PROGRESS ===`** → add a row per line to the table in `03 Projects/EV Academy/Results/Progress.md`; put partial/failed lessons under "Open revisits"; update Stats.
5. Check every `domain:` matches `_meta/domains.json` exactly, and every `[[wikilink]]` resolves. Report mismatches; don't create stubs.
6. Reply: files created, files updated, problems found.

Never write to `00 Home/`, `_meta/`, `_tools/`. Never delete, rename or move notes. No MOC edits: domain maps are dataview-driven.
