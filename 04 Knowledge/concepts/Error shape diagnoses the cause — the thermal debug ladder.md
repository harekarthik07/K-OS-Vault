---
concept: Error shape diagnoses the cause — thermal debug ladder
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-09-15
aliases: ["Thermal debug ladder", "Error shape diagnoses the cause"]
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [thermal, debugging, method, calibration, etm]
---

# Error shape diagnoses the cause — the thermal debug ladder

## Working definition (project-specific)
The **shape** of a model-vs-measurement residual tells you *which* parameter class is wrong, before you touch anything. Read the error, then fix the indicated class — don't fit blindly.

| Residual signature | Culprit |
|---|---|
| Magnitude wrong, shape right | a **resistance** |
| Shape wrong (tail, crossover), magnitude right | a **capacitance** |
| Widens with temperature / load | the **loss model** or h |
| Constant offset appearing *before* the sink charges | a **series path** term, not convection |

## Notes / derivations / snippets
- **Reusable debug ladder:**
  1. Budget every resistance from theory first, sum them — that is your prior.
  2. Fit. Within ~15 % of theory → material/geometry uncertainty; accept and document.
  3. Fitted is 2×+ theory → a **term is missing entirely** (spreading, contact, fin efficiency). Find it, don't fit it.
  4. Fitted varies with load → not a resistance problem — loss model or h.
  5. Residual shape-wrong not magnitude-wrong → capacitance, not resistance.
- **This case:** the +1.89 K residual was a near-constant, load-independent offset appearing early → a series-path explanation (NTC partway up RthJC), *not* a convection error. Documented, not corrected — see [[Cauer Model Calibration — fit what you cannot derive]].
- Pairs with [[Convection dominates the thermal budget]] (check the big term first) and [[R = ΔT over Q holds only at steady state]] (don't misread a charging curve as a resistance error).

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]] · [[Power Electronics]]
- [[Cauer Model Calibration — fit what you cannot derive]] · [[Convection dominates the thermal budget]]
