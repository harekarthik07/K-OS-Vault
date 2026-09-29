---
concept: Only the h·A product sets convective resistance
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-09-15
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [thermal, convection, heatsink, fin-design, design-tool]

> [!cite] Also applied
> 2026-09-28 — fin study delivered as an `(h, A)` lever map in the design tool: [[EOD_2026-09-28_ETM_1D_Thermal_Tool]]

---

# Only the h·A product matters for convective resistance

## Working definition (project-specific)
Convective resistance is `R_conv = 1/(h·A)`. It depends only on the **product** `h·A`, never on either factor alone. A fin redesign that **doubles area but halves h** (flow-starving the new channels) is a lateral move — the thermal result is identical.

## Notes / derivations / snippets
- **Design consequence:** more fin area is not automatically better. Tighter/taller fins add A but can collapse local h by starving channels of flow — net h·A flat or worse. (CFD sibling: [[Impinging fan + straight tight fins = high cross-flow resistance]].)
- **Honest way to present a design study:** an **(h, A) contour map** of R_conv, not a single predicted h. The 1D model cannot compute h for a new geometry, so plotting the product is more truthful than pretending to predict one number.
- **Identifiability:** because only the product is observable, a mid-transient dyno fit constrains `R·C`, not h and A separately — h's credibility comes from CFD, not the fit. See [[Cauer Model Calibration — fit what you cannot derive]].
- This case: R_conv = 1/(29.59 × 0.232) = 0.1457 K/W = 78 % of R_total ([[Convection dominates the thermal budget]]).

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]] · [[CFD]]
- [[Convection dominates the thermal budget]] · [[Impinging fan + straight tight fins = high cross-flow resistance]]
