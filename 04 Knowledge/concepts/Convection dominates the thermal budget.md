---
concept: Convection dominates the heatsink thermal budget
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-09-15
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [thermal, convection, heatsink, design-priority]
---

# Convection dominates the thermal budget

## Working definition (project-specific)
In an air-cooled heatsink the convective resistance to air usually swamps every solid-conduction term. Spend design effort where the resistance actually is — the airflow — not on polishing conduction terms that move a small fraction of the total.

## Notes / derivations / snippets
- **This case:** `R_conv = 0.1457` of `R_total = 0.1858` → **78 %**. All the effort deriving `R_hs` (spreading, conduction) refined a **17 %** term.
- Corollary: real thermal margin comes from more/better airflow (fan, ram air, channel design), not thicker metal or better TIM — those are already small.
- Diagnostic use: if a lumped model is magnitude-wrong, suspect the dominant term first (h / convection) before chasing small ones. Feeds [[Error shape diagnoses the cause — the thermal debug ladder]].
- Sizing sanity: budget every resistance from theory, sum, see which single term owns the majority — optimise that one.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]]
- [[Only the h·A product matters for convective resistance]] · [[Spreading resistance — heat enters over the source, not the whole base]]
