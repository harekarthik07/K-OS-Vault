---
tags: [K-OS, command, SOP]
command: /eod
status: standing
---
# `/eod` — compile the day

**Goal:** turn today's work into one dated, honest log that feeds tomorrow and the weekly harvest.

## Procedure (Claude)
1. Create `03 Projects/<Project>/daily/EOD_<YYYY-MM-DD>_<Project>_<phase>.md` from **Daily_EOD_Template**.
2. Fill: what we set out to do → what we did → **Results & numbers** (every row tagged verified / assumed / needs-checking) → decisions & why → **Learnings & theory** → blocked & open → next session → for Claude Code → vault links.
3. **Learnings & theory** is the raw feed for `/weekly` — one line each, tagged:
   - `#learning/concept — <insight> → [[page]]` (or `→ new`)
   - `#learning/gotcha — <failure turned into a rule> → new`
   - `#learning/method — <a check that worked> → [[page]]`
4. Update the project's `00 Home` roadmap: tick completed tasks, flip a phase `⚪→🟢→✅`, add the outcome line when a phase closes.
5. Add a short pointer entry in the project `Daily Log.md`.

## Honesty rule
No polished claims. If a number is assumed or needs checking, say so in its row.
