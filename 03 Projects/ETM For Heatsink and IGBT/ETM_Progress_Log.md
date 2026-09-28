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
- **2026-09-15 — Phase 1 validated.** `MC_HS_ETM_I2.slx` matches **11 dyno runs (356–492 W) to ~2 K** with **one fitted parameter `h = 29.59`** (CFD independently gives 34.3, 16 %). Full budget: [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]. Early theory-match: [[2026-09-01 Phase 1 — 1D Cauer model matches theory]].
- **2026-09-03 — Ported to Vantage.** Electro-thermal chain rebuilt as an interactive web module: [[ETM ported into Vantage]].

## Learnings (feed to /weekly)
- #learning/concept — Calibrating the *right* parameter is everything: fitting `h` gave a 4.9 % spread across 11 runs where fitting the derivable `R_hs` gave 35 % → [[Cauer Model Calibration — fit what you cannot derive]]
- #learning/concept — Convection is ~78 % of `R_total`; refining solid conduction only moves a 17 % term → [[Convection dominates the thermal budget]]

## Open
- Phase 2 sweep not yet run — see live tasks in [[00 Home]].

---
`Phase 1 validated` · `h = 29.59` · `11 dyno runs` · `#learning`
