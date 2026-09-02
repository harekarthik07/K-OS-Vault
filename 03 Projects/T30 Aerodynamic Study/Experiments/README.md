---
type: folder_readme
project: T30 Aerodynamic Study
---

# Experiments

One note per run/investigation.

Naming: `YYYY-MM-DD <short description>`

Template: `_templates/Project/Experiments/_experiment-template.md`
(`Ctrl+P` → *Templater: Create new note from template*)

## Index
```dataview
TABLE date, status
FROM "03 Projects/T30 Aerodynamic Study/Experiments"
WHERE type = "experiment"
SORT date DESC
```
