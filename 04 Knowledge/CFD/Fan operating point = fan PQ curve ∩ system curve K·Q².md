---
concept: Fan operating point = PQ curve ∩ system curve
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [cfd, fan-model, pq-curve]
---

# Fan operating point = fan PQ curve ∩ system curve K·Q²

## Working definition (project-specific)
A fan does not deliver "its" flow rate. It delivers whatever flow satisfies **both** its own pressure-flow characteristic and the duct/heatsink's resistance. The operating point is the intersection:

$$\Delta p_{\text{fan}}(Q) \;=\; K\,Q^2$$

The fan curve is fixed by the hardware. **The system curve is set by the geometry you design** — so a fin redesign moves the operating point even with an identical fan.

## Notes / derivations / snippets
- From CFD: `Q_op = ṁ_fan / ρ_op`, `Δp_op = p_out − p_in` (area-weighted at the fan in/out interfaces).
- System resistance coefficient: `K = Δp_op / Q_op²`. Dimensionally it lumps every loss in the path — fin channels, bends, discharge blockage — into one number.
- **Design comparison is a K ratio.** `K_new / K_old` tells you what a geometry change actually cost, independent of fan choice. This case: straight/tight fins vs curved/open ⇒ expected ≈ 3–4×.
- Higher K rotates the system parabola upward ⇒ intersection slides **left** (less flow, more Δp) ⇒ toward stall. See [[Tighter fins raise system K → operating point shifts left toward stall]].

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]]
- [[Fan PQ Health Check & Reverse-Flow Diagnosis]] · [[Fan 3D Zone Setup]] · [[Fan_TRV_I1]]
