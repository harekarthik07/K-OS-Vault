---
type: folder_readme
project: Raptee Vantage
---

# Results

What actually shipped, and what it changed. The permanent record.

Naming: `YYYY-MM-DD <what shipped>`
e.g. `2026-08-31 in_verdict bulk toggle shipped`

Template: `_templates/Project/Results/_results-template.md`

Worth recording here:
- Deploys (`deploy.bat` → `pm2 reload`) and what went out
- Verdict-logic changes — **always**, with before/after numbers on real bike data
- Golden version activations (which version, why, what re-graded)
- Anything that changed a headline QC number

**A verdict-logic change with no Results note is a change nobody can audit.**
See [[Conventions]].

## Index
```dataview
TABLE date
FROM "03 Projects/Raptee Vantage/Results"
WHERE type = "result"
SORT date DESC
```
