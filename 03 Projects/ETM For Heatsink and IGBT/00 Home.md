---
type: project_home
project: ETM For Heatsink and IGBT
objective: "Dyno-validated 1D electro-thermal (Cauer) model of the IGBT+heatsink, then a design tool over L and thermal mass."
status: active
domain_primary: Thermal Management
domain_secondary: [Power Electronics]
current_phase: Phase 3
---

# ETM For Heatsink and IGBT

> Electro-thermal model coupling IGBT loss calculation with heatsink thermal network.

## Sections
- [[ETM_Problem_Statement]] · [[ETM_Progress_Log]] · [[ETM_Flowchart]] · [[ETM_Approach_and_TODO]] — the four-note set
- [[Daily Log]] · `daily/` — dated EODs
- [[Questions]] — open unknowns
- Results/ — validated write-ups & phase reports
- Concepts/ — project staging (harvested to the Ideaverse on `/weekly`)
- Experiments/ · Resources/ — optional (runs, datasheets); leave empty if the log covers it
- Tool: [[1D Thermal Design Tool — spec & flowchart]] · [[1D Thermal Design Tool — README & usage]]

---

## Roadmap

### ✅ Phase 1 — Validated 1D Cauer model (2026-08 → 2026-09-15)
`#matlab #1D-cauer #cauer #calibration #dyno-validated`
**Objective:** Build the 1D IGBT → HS → ambient Cauer network, derive every parameter from datasheet/CAD/correlation, and validate against real dyno data.
**Outcome:** `MC_HS_ETM_I2.slx` validated against **11 dyno runs (356–492 W)** to ~2 K, with **one fitted parameter (h = 29.59)** — CFD independently gives 34.3 (16 %). Full budget + derivation: [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]. Early theory-match milestone: [[2026-09-01 Phase 1 — 1D Cauer model matches theory]].
**Concepts captured:** [[Cauer Model Calibration — fit what you cannot derive]] · [[Spreading resistance — heat enters over the source, not the whole base]] · [[Multi-node thermal time constants need eigenvalues, not per-branch RC]] · [[Convection dominates the thermal budget]] · [[Only the h·A product matters for convective resistance]] · [[Error shape diagnoses the cause — the thermal debug ladder]]

### ✅ Phase 2 — Design tool: L-sweep + h–A map (2026-09-28)
`#parametric-sweep #thermal-mass #baseplate-L #design-tool #matlab-app`
**Objective:** Characterise how junction temperature behaves over L and thermal mass, and ship a tool that screens heatsink/alloy/fin designs in 1D.
**Outcome (2026-09-28):** Built the interactive **1D thermal design tool** (`mc_thermal_app.m` on a gated `thermal_core` fast twin) — see [[1D Thermal Design Tool — spec & flowchart]] and [[EOD_2026-09-28_ETM_1D_Thermal_Tool]]. **L-sweep:** `R_hs` minimum at **17.9 mm** (part is 18 mm — already optimal). **h–A map** built (current point 29.59/0.232 → Tj 93.4 °C). **ADC12 vs LM25:** `Rhs +63 %`, time-to-95 °C 270 s → 198 s (fails hot-ambient duty without +16 % h). All six build gates passed (core RK4 = 0.000 K; P_inv match 0.05 W).
**Fin study delivered as an `(h, A)` lever map**, not a single predicted h — [[Only the h·A product matters for convective resistance]].
- [x] Geometry-parametric core with auto-recomputed R_cond/R_spread/R_ch on L change — [[Spreading resistance — heat enters over the source, not the whole base]]
- [x] L-sweep with optimum marked (17.9 mm)
- [x] (h, A) contour map
- [x] Knee identified (spreading vs conduction cross at the part's L)
- [x] Write-up → [[EOD_2026-09-28_ETM_1D_Thermal_Tool]]

> [!note]- Reasoned deviation from the Phase-1 guardrail
> Phase 1 said "build in Simulink; no parallel MATLAB reimplementation (would fork the validation)." A parallel core (`thermal_core`) **was** built — deliberately, because live sliders need microseconds — and the fork risk is mitigated by `test_core.m` locking the twin to `MC_HS_ETM_I2.slx` at **<0.01 K**. `h` kept as the one fitted number; +1.89 K bias uncorrected; transient-only ≤300 s.
> **Carried:** a dedicated T_j-vs-total-mass sweep figure (the app supports it; not yet saved as a plot).

### 🟢 Phase 3 — Decisions & handover (in progress, started 2026-09-28)
`#decision #alloy #handover`
**Objective:** Turn the tool's outputs into decisions and make the tool a clean handover.
**Tasks:**
- [x] Decide ADC12 viability given 198 s time-to-deration at hot ambient (cost/performance call, not modelling) 🔼 ✅ 2026-09-29
- [x] Add save/load of design configs to `.mat` ✅ 2026-09-29
- [x] Add the T_j-vs-total-mass sweep figure (carried from Phase 2) ✅ 2026-09-29
- [x] Standing re-verification: run `test_core` + `test_app_gate` after any physics edit ✅ 2026-09-29
- [x] Write up → `Results/YYYY-MM-DD Phase 3 …` ✅ 2026-09-29

---

## Open Concepts
```dataview
LIST FROM "03 Projects/ETM For Heatsink and IGBT/Concepts"
WHERE status = "incubating"
```

## Atlas Connections
- [[Thermal Management]]
- [[Power Electronics]]
- [[Heat Transfer]]
