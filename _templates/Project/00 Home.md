---
type: project_home
project: <% tp.file.folder() %>
status: active            # active | paused | completed | archived
started: <% tp.date.now("YYYY-MM-DD") %>
domain_primary:           # main domain, must match _meta/domains.yaml
domain_secondary: []
---

# <% tp.file.folder() %>

> One-sentence goal of this project.

## Sections
- [[Daily Log]]
- [[Questions]]
- Experiments/ — one note per experiment
- Results/    — final outputs, plots, verdicts
- Concepts/   — incubating knowledge (harvested on Friday)
- Resources/  — links, papers, datasheets (promoted on close)

## Open Concepts (incubating)
```dataview
LIST FROM "<% tp.file.folder(true) %>/Concepts"
WHERE status = "incubating"
```

## Atlas Connections
- [[<domain MOC>]]
