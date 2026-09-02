---
concept: Raising system K shifts the operating point toward stall
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: Thermal Management
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [thermal, heatsink, fin-design, pq-curve, stall]
---

# Tighter fins raise system K → operating point shifts left toward stall

## Working definition (project-specific)
The system curve `Δp = K·Q²` is a parabola through the origin. Raising **K** steepens it, so its intersection with the (falling) fan curve slides **left and up**: less flow, higher back-pressure. Push far enough left and you cross into the choked/stall corner — where the fan starts recirculating internally instead of pumping.

**A fin redesign is a fan operating-point change.** Same fan, same RPM, same clearance — different flow.

## Notes / derivations / snippets
- This case: fin change alone moved K by an expected **3–4×**, landing φ at 0.357 — the choked edge (see [[Flow coefficient φ — below 0.35 expect central reverse flow]]).
- Because Δp scales with Q², a 3–4× K rise does **not** cost 3–4× flow — the fan curve's own slope absorbs part of it. The steeper the fan curve near the operating point, the more flow you keep. Flat-curve fans are the vulnerable ones.
- **Practical rule:** any geometry change in the flow path must be re-checked against the fan curve before it's accepted on thermal grounds. Extra fin area that pushes φ below 0.35 is a net loss.
- Confirmation method: pull `Q, Δp` from both the old and new converged cases, plot both points on the one datasheet curve, and report `K_new/K_old`.

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[CFD]]
- [[Fan operating point = fan PQ curve ∩ system curve K·Q²]] · [[Impinging fan + straight tight fins = high cross-flow resistance]]
