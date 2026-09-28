---
concept: Thermal resistance ΔT/Q is a steady-state identity only
origin_project: ETM For Heatsink and IGBT
domain: Heat Transfer
status: budding
created: 2026-09-15
aliases: ["R = ΔT/Q holds only at steady state"]
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [heat-transfer, transient, thermal-resistance, method]
---

# R = ΔT over Q holds only at steady state

> Filename uses "over" because `/` is illegal in Obsidian filenames; the alias keeps the `R = ΔT/Q` form.

## Working definition (project-specific)
`R = ΔT / Q` is an **equilibrium identity** — only true once every capacitance in the path has stopped charging. Apply it to transient data that hasn't plateaued and you extract a resistance that is biased low, because part of the input power is still going into heat storage, not across the resistance.

## Notes / derivations / snippets
- **This case:** the plateau equation under-predicted the required resistance by ~30 %, because no run reaches steady state (240 s test vs tau2 = 394 s, only 46 % risen — see [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]).
- Practical consequence: **manual transient bracketing beat the steady-state formula.** Fit against the transient solution, or a fixed mid-transient window, not the endpoint.
- Rule of thumb: only trust `ΔT/Q` when run length ≫ the largest tau (roughly ≥ 4–5 tau). Below that you are reading an RC charging curve, not a resistance.
- This is *why* the model is transient-only and its validity envelope stops at ~300 s.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Heat Transfer]]`)
- [x] Sources cited

## Atlas Connections
- [[Heat Transfer]] · [[Thermal Management]]
- [[Multi-node thermal time constants need eigenvalues, not per-branch RC]] · [[Cauer Model Calibration — fit what you cannot derive]]
