---
type: concept
concept: Total thermal mass sets the short-duty transient, not the node split
domain: Heat Transfer
status: budding
created: 2026-09-28
origin_project: ETM For Heatsink and IGBT
aliases: ["total C dominates transient", "node split low sensitivity"]
sources: ["[[EOD_2026-09-28_ETM_1D_Thermal_Tool]]"]
tags: [heat-transfer, transient, thermal-mass, lumped-capacitance]
related: ["[[R = ΔT over Q holds only at steady state]]", "[[Multi-node thermal time constants need eigenvalues, not per-branch RC]]"]
---

# Total thermal mass sets the short-duty transient, not the node split

## One-line idea
For a short duty that never reaches steady state, the temperature rise is governed by the **total** heat capacity `C_total = Σ mᵢcpᵢ`; **how** that capacity is split between nodes barely moves the result.

## Intuition first
Over a few minutes the part is still charging up — heat is going into storage, not flowing out to ambient. Storage is set by total `C`. The internal split only changes how fast heat *redistributes between nodes*, a second-order effect on the node you read as long as the whole assembly is well-connected internally.

## Governing relations
- Lumped charge: `C_total · dT̄/dt ≈ Q(t)` while `t ≪ τ_out`.
- Node split changes the fast internal time constant, not the slow bulk rise.

## Worked example (T30 MC heatsink, ETM tool)
4-min (240 s) duty. Sweeping the IGBT/HS mass split around **0.17** (range 0.10–0.30) barely moves `Tj_peak`, while changing **total** mass moves it directly. Hence the tool's mass panel exposes `m_total` + a low-sensitivity split slider with a live derived readout.

## Validity window & invalidation triggers
- Holds when `t_duty ≪ τ_to_ambient` (transient-dominated) **and** internal inter-node resistance is small vs the storage effect.
- Breaks near steady state, or if a node is thermally isolated (then its local C matters).

## How we verify it
Sweep the split at fixed total C in the 1D core; confirm `Tj_peak` spread is negligible vs the total-C sweep.

## Where used
- [[EOD_2026-09-28_ETM_1D_Thermal_Tool]] · [[1D Thermal Design Tool — spec & flowchart]] (mass-panel design)

---
`total C` · `short-duty transient` · `node split low-sensitivity` · `lumped capacitance`
