---
concept: Hub-shadow dead-zone h is its own regime
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: Heat Transfer
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [heat-transfer, cht, cauer, impingement, etm]
---

# Dead-zone h is a different regime, not a correction factor

## Working definition (project-specific)
Under an axial fan hub there is no through-flow — the hub shadow is a genuine **stagnation zone** with low velocity and correspondingly low `h`. At tight clearance (here H/D = 0.14) it is physically real, not a meshing or convergence artefact. It must not be "corrected away" or blended into a single surface-average `h`.

Extract `h` **zone-wise**:

| Zone | Radius | Regime |
|---|---|---|
| under-hub | `r < r_hub` | stagnation, low `h` |
| impingement | `r_hub < r < r_tip` | jet impingement, high `h` |

## Notes / derivations / snippets
- These two zones differ by regime, not by a few percent — an area-weighted average sits in a range neither zone actually occupies.
- **Why it biases the Cauer model:** the IGBT die is not uniformly distributed over the base. A single averaged `h` implicitly assumes it is, so a die sitting in the hub shadow gets an optimistically low junction temperature.
- Fix: a **3-node Cauer with a parallel dead-zone branch** — one `R_conv = 1/(h·A)` per zone in parallel, rather than one lumped branch. Open item on [[MC_HS_ETM_I1]].
- Sanity check on the extraction: `Σ h_i·A_i·ΔT_i` must close against the CFD base heat flux to < 1 %.

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Heat Transfer]]`)
- [x] Sources cited

## Atlas Connections
- [[Heat Transfer]] · [[Thermal Management]]
- [[MC_HS_ETM_I1]] · [[Fan PQ Health Check & Reverse-Flow Diagnosis]] · [[MC Heatsink CHT — Consolidated Setup]]
