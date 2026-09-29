---
type: progress_log
project: ETM For Heatsink and IGBT
status: active — Phase 2 in progress
created: 2026-09-28
related: ["[[Daily Log]]", "[[ETM_Problem_Statement]]", "[[00 Home]]"]
---

# ETM — Progress Log

> Chronological record of what was tried, what broke, the root cause, and the fix. Day-by-day detail lives in [[Daily Log]]; this note holds the milestone-level narrative and the `#learning` flags.

## Milestones
- **2026-09-28 — Phase 2 complete: 1D design tool shipped.** Built `mc_thermal_app.m` on a gated `thermal_core` fast twin (all 6 build gates passed; core RK4 = 0.000 K, P_inv match 0.05 W). L-sweep gives `R_hs` optimum **17.9 mm** (part already at 18 mm); h–A lever map built; ADC12 vs LM25 alloy trade quantified (`Rhs +63 %`, 270 s → 198 s to deration). Full day: [[EOD_2026-09-28_ETM_1D_Thermal_Tool]]; tool: [[1D Thermal Design Tool — spec & flowchart]].
- **2026-09-15 — Phase 1 validated.** `MC_HS_ETM_I2.slx` matches **11 dyno runs (356–492 W) to ~2 K** with **one fitted parameter `h = 29.59`** (CFD independently gives 34.3, 16 %). Full budget: [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]. Early theory-match: [[2026-09-01 Phase 1 — 1D Cauer model matches theory]].
- **2026-09-03 — Ported to Vantage.** Electro-thermal chain rebuilt as an interactive web module: [[ETM ported into Vantage]].

## Learnings (feed to /weekly)
- #learning/concept — For a 4-min duty the transient result is set by **total thermal mass**, not the node split (split ≈0.17 is low-sensitivity) → new
- #learning/concept — `R_hs(L)` has a real optimum where spreading benefit and conduction penalty cross (~17.9 mm); thicker base is not monotonically better → new
- #learning/method — Keep a **fast twin locked to the authoritative model with a guard test** (`thermal_core` ⟷ `MC_HS_ETM_I2.slx`, `test_core < 0.01 K`) so a parallel reimplementation can't silently fork the validation → new
- #learning/concept — Calibrating the *right* parameter is everything: fitting `h` gave a 4.9 % spread across 11 runs where fitting the derivable `R_hs` gave 35 % → [[Cauer Model Calibration — fit what you cannot derive]]
- #learning/concept — Convection is ~78 % of `R_total`; refining solid conduction only moves a 17 % term → [[Convection dominates the thermal budget]]

## Open
- Phase 2 sweep not yet run — see live tasks in [[00 Home]].

---
`Phase 1 validated` · `h = 29.59` · `11 dyno runs` · `#learning`
