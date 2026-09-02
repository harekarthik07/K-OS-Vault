---
type: project_home
project: <% tp.file.folder() %>
status: active            # active | paused | completed | archived
started: <% tp.date.now("YYYY-MM-DD") %>
domain_primary:           # main domain, must match _meta/domains.yaml
domain_secondary: []
current_phase: Phase 1
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

---

## Roadmap

Phase status legend: ✅ done · 🟢 in progress · ⚪ queued/TBD

### ⚪ Phase 1 — <name> (started YYYY-MM-DD)
`#tag1 #tag2`
**Objective:** *(one-line goal of this phase)*
**Tasks:**
- [ ]

*(when a phase completes: change ⚪/🟢 → ✅, add end date, and replace the Tasks block with a one-line link to `Results/YYYY-MM-DD Phase N — …`)*

---

## Open Concepts (incubating)
```dataview
LIST FROM "<% tp.file.folder(true) %>/Concepts"
WHERE status = "incubating"
```

## Atlas Connections
- [[<domain MOC>]]
