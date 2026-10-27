---
type: folder_readme
project: Vantage VE
---

# Experiments

One note per **investigation**. Anything that starts with "why does X behave like Y?"
and ends with an answer belongs here.

Naming: `YYYY-MM-DD <short description>`
e.g. `2026-10-15 top-speed sensitivity to CD`

Template: `_templates/Project/Experiments/_experiment-template.md`
(`Ctrl+P` → *Templater: Create new note from template*)

**Outcome goes back into a Concept note** — an experiment that teaches something
durable must leave a trace in `Concepts/`, or it'll be re-run in six months.

## Index
```dataview
TABLE date, status
FROM "03 Projects/Vantage VE/Experiments"
WHERE type = "experiment"
SORT date DESC
```
