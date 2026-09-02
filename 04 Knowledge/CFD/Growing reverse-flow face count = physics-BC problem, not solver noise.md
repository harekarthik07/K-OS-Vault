---
concept: Growing reverse-flow face count = physics-BC problem
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [cfd, convergence, reverse-flow, diagnostics]
---

# Growing reverse-flow face count = physics-BC problem, not solver noise

## Working definition (project-specific)
Fluent's `Reverse flow in N faces in <zone>` warning is only benign when **N is bounded and shrinking**. If N *grows* iteration over iteration (here 20 → 150+ on the fan exit, later spreading to the fan inlet), the solver is resolving a real recirculation the setup has created — not startup transients. More iterations will not clear it.

## Notes / derivations / snippets
- **Read the trend, not the presence.** Log N vs iteration. Falling/flat → ignore. Rising → stop the run.
- Spreading to a *second* boundary (exit → inlet) means the recirculation loop has closed on itself; the fan is pumping against a system it can't clear.
- Usual causes, in order of likelihood: system resistance too high for the fan (see [[Fan operating point = fan PQ curve ∩ system curve K·Q²]]), outlet placed inside a recirculating region, missing/incorrect backflow BCs, blocked discharge path.
- Corollary: residuals lie here. Continuity stalling at 6e-2 was a *symptom* of the reverse flow, not an independent problem — see [[Curve-match residual ε is a convergence gate for fan CHT]].

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]]
- [[Fan PQ Health Check & Reverse-Flow Diagnosis]]
