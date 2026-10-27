---
type: folder_readme
project: Vantage VE
---

# Results

What shipped and what it changed. Permanent record.

Naming: `YYYY-MM-DD <what shipped>`
e.g. `2026-10-20 Powertrain Phase 1 — curves live`

Template: `_templates/Project/Results/_results-template.md`

## Index
```dataview
TABLE date
FROM "03 Projects/Vantage VE/Results"
WHERE type = "results"
SORT date DESC
```
