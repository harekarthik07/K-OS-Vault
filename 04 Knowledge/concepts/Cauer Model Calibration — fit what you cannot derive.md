---
concept: Cauer Model Calibration — fit what you cannot derive
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-09-15
aliases: ["Cauer_Model_Calibration", "Fit what you cannot derive"]
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [thermal, cauer, calibration, method, etm]

> [!cite] Also applied
> 2026-09-28 — reused in the 1D design tool (fit `h`, not `Rhs`; 4.9 % vs 35 % spread): [[EOD_2026-09-28_ETM_1D_Thermal_Tool]]

---

# Cauer Model Calibration — fit what you cannot derive

## Working definition (project-specific)
A lumped thermal network has one honest calibration strategy: **derive every parameter you can** (datasheet, CAD, or a published correlation) and **fit only the one you genuinely cannot** — here the convective `h`. Calibrating a *derivable* resistance to hit the data launders a modelling error into a fitted number and destroys the model's predictive value.

> [!quote] Standing principle
> Fit what you cannot derive. Derive what you can. Never bend a derived parameter to absorb an offset you can explain.

## Notes / derivations / snippets
- **The evidence:** calibrating `R_hs` (fully derivable as `L/(kA) + spreading`) gave a **35 % spread** across 11 dyno runs. Calibrating `h` on the *same* data gave **4.9 %**. Same model, same runs — the difference is calibrating the right knob.
- A tight fitted-parameter spread across independent runs is the real validation signal, not RMSE alone. Wide spread = fitting the wrong thing.
- **Don't correct a documented, explainable bias by bending a derived R.** The +1.89 K offset is explainable (NTC sits partway up RthJC); pushing R_hs to absorb it would re-fit a derived number.
- Independent cross-check builds credibility the fit can't: CFD gave area-weighted h = 34.3 vs fitted 29.59 (16 %), in the physically correct direction (dyno had no ram air).
- Diagnostic companion: [[Error shape diagnoses the cause — the thermal debug ladder]].

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]]
- [[Heatsink Thermal RLC Network]] · [[Thermal Resistance model of Heatsink With IGBT]] · [[Error shape diagnoses the cause — the thermal debug ladder]]
