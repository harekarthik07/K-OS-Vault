---
type: project_home
project: Small Top Busbar ETM
aliases: [small-top-busbar-etm]
objective: "Compare new (rect block) vs old (cylindrical boss) Small Top Busbar terminal on absolute max terminal temp at 120A, via Maxwell 3D → Icepak two-way coupling."
status: active
started: 2026-10-28
domain_primary: Thermal Management
domain_secondary: [Power Electronics]
current_phase: Phase 1
---

# Small Top Busbar ETM

> Is the new rectangular-block terminal at least as cool as the old cylindrical boss, same load, same ambient?

## Sections
- [[Busbar_Problem_Statement]] · [[Busbar_Progress_Log]] · [[Busbar_Flowchart]] · [[Busbar_Approach_and_TODO]] — the four-note set
- [[Daily Log]] — dated EODs
- [[Questions]] — open unknowns
- Experiments/ · Results/ · Concepts/ · Resources/ — created when first needed

---

## Roadmap

### 🟢 Phase 1 — New vs old max terminal temp (started 2026-10-28)
`#ansys #maxwell3d #icepak #busbar #etm`
**Objective:** Pass if new max terminal temp ≤ old, 120A, matched 27°C ambient.
**Status:** new design solved at 27°C; old design re-run at 27°C pending. Task list lives in [[Busbar_Approach_and_TODO]].

---

## Open Concepts (incubating)
```dataview
LIST FROM "03 Projects/Small Top Busbar ETM/Concepts"
WHERE status = "incubating"
```

## Related
- [[Busbar G-Bridge Thermal Fatigue/00 Home|Busbar G-Bridge Thermal Fatigue]] — separate study, this one is standalone.
