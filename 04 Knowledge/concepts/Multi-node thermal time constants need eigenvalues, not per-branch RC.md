---
concept: Multi-node thermal time constants need eigenvalues
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-09-15
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [thermal, transient, cauer, eigenvalues, method]
---

# Multi-node thermal time constants need eigenvalues, not per-branch RC

## Working definition (project-specific)
In a multi-node RC (Cauer) network the system time constants are **the eigenvalues of the state matrix**, not the individual `R·C` products of each branch. The per-branch estimate is systematically wrong because upstream capacitance also discharges through the downstream resistance.

## Notes / derivations / snippets
- Two-node state matrix (`theta = T - T_amb`):
  ```
  A = [ -1/(R_s C_p)      1/(R_s C_p)          ]
      [  1/(R_s C_hs)   -(1/R_s + 1/R_c)/C_hs  ]
  tau = -1 / eig(A)
  ```
- **This case:** naive `tau2 = C_hs · R_conv = 2404 × 0.1457 = 350 s`. Correct eigenvalue: **394 s**. The junction's 490 J/K also drains through the same convection path, which the per-branch product ignores.
- Sanity estimate that *does* work as a mental model: `(C_p + C_hs)·R_c = 2894 × 0.1457 = 422 s` — same order, right intuition.
- Test-design consequence: with tau2 = 394 s a 240 s run reaches only `1 - e^(-240/394) = 46 %` of the eventual rise. Fitting steady-state `R = ΔT/Q` to such data is invalid — see [[R = ΔT over Q holds only at steady state]].

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]]
- [[Heatsink Thermal RLC Network]] · [[R = ΔT over Q holds only at steady state]]
