---
tags: [project, CAE-CFD, busbar, ETM]
date: 2026-10-29
related: "[[small-top-busbar-etm]]"
---

# Progress_Log — Small Top Busbar ETM

## 2026-10-21
- Standalone Small Top Busbar V1.0 run: Maxwell 3D → Icepak two-way coupling validated. 2-face excitation (60A each, I_DC=120A), converged Total Loss = 0.127W (Pass 3, Loss Error 0.076%).
- Diagnosed near-ambient ΔT (30.107–30.153°C) as physically correct for bulk conduction at this loss level, not a coupling bug — back-calc R ≈ 8.8µΩ matches cast-383 Al resistivity for the geometry.
- Confirmed EMLoss1 link live (Volume → SmallTopBusbarV10), 2-Way Coupling object active (3 coupling iters, 15 Icepak iters/coupling), material props (σ=1.333e7 S/m w/ PTC modifier, k=95.9 W/m·K) correct for cast 383.0 Al.
- Bolted joint to pattern plate identified as un-modeled contact resistance — flagged as likely real hotspot location, not yet addressed in this study.

## 2026-10-28
- Reframed as standalone ETM project (separate from [[busbar-thermal-fatigue]] G-Bridge work).
- Locked objective: compare new vs old busbar design on **absolute max terminal temp** (not ΔT) at 120A, 18-wirebond excitation (6.67A/bond, 8mm bond length).
- Geometry clarified: old = cylindrical boss terminal (Ø15mm, 2° draft, 15.2mm long, ~176.7mm²); new = rectangular block terminal (35.24×17mm, 15mm long, 599mm², ~3.4× old's cross-section).
- First-principles flag: larger new-design cross-section should mean *lower* resistance/current density → expect new design to run cooler, not hotter. Any contrary result needs root-cause before touching geometry.
- Both designs confirmed already modeled with per-wirebond excitation under matched BCs — no baseline rebuild needed.
- Hardware confirmed: CAE server = Ryzen 9 4000-series (= PC1 in [[ways-of-working]]).

## 2026-10-29
- New design solved: ambient = 27°C.
- **Open:** old design not yet (re-)run at matched 27°C ambient — comparison blocked until this lands.
- Obsidian starter notes generated (Problem_Statement, Progress_Log, Flowchart, Approach_and_TODO).
- Section 6 (End Result For) still open — pending confirmation of what this result feeds.

## Next session starts with
- Get old design's max terminal temp result at 27°C ambient, same load.
- Run the new-vs-old temp comparison; check against the area-ratio sanity expectation.
- Close Section 6.
