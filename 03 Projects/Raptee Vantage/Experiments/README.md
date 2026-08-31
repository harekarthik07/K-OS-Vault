---
type: folder_readme
project: Raptee Vantage
---

# Experiments

One note per **investigation**. Anything that starts with "why did X do Y?" and
ends with an answer belongs here.

Naming: `YYYY-MM-DD <short description>`
e.g. `2026-08-30 BB-EOL all-fail investigation`

Template: `_templates/Project/Experiments/_experiment-template.md`
(`Ctrl+P` → *Templater: Create new note from template*)

For verdict investigations, the useful shape is the debugging order from
[[Verdict Engine]]:

1. Cache? (use `/api/bike-verdict/{n}`, not the grid)
2. Did the bike match? (identifier matching per suite)
3. Is the unit excluded? ([[in_verdict Gate]])
4. Which golden version is active? ([[Golden Versions]])
5. Which parameter actually breached?
6. Then read the suite eval code

**Outcome goes back into [[Landmines]] or the suite note** — an experiment that
teaches something durable must leave a trace in `Concepts/`, or it'll be
re-investigated in six months.

## Index
```dataview
TABLE date, status
FROM "03 Projects/Raptee Vantage/Experiments"
WHERE type = "experiment"
SORT date DESC
```
