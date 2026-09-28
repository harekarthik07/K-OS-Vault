---
type: project_home
project: ETM For Heatsink and IGBT
objective: "Dyno-validated 1D electro-thermal (Cauer) model of the IGBT+heatsink, then a design tool over L and thermal mass."
status: active
domain_primary: Thermal Management
domain_secondary: [Power Electronics]
current_phase: Phase 2
---

# ETM For Heatsink and IGBT

> Electro-thermal model coupling IGBT loss calculation with heatsink thermal network.

## Sections
- [[Daily Log]]
- [[Questions]]
- Experiments/
- Results/
- Concepts/ — 5 concepts currently incubating (see below)
- Resources/

---

## Roadmap

### ✅ Phase 1 — Validated 1D Cauer model (2026-08 → 2026-09-15)
`#matlab #1D-cauer #cauer #calibration #dyno-validated`
**Objective:** Build the 1D IGBT → HS → ambient Cauer network, derive every parameter from datasheet/CAD/correlation, and validate against real dyno data.
**Outcome:** `MC_HS_ETM_I2.slx` validated against **11 dyno runs (356–492 W)** to ~2 K, with **one fitted parameter (h = 29.59)** — CFD independently gives 34.3 (16 %). Full budget + derivation: [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]. Early theory-match milestone: [[2026-09-01 Phase 1 — 1D Cauer model matches theory]].
**Concepts captured:** [[Cauer Model Calibration — fit what you cannot derive]] · [[Spreading resistance — heat enters over the source, not the whole base]] · [[Multi-node thermal time constants need eigenvalues, not per-branch RC]] · [[Convection dominates the thermal budget]] · [[Only the h·A product matters for convective resistance]] · [[Error shape diagnoses the cause — the thermal debug ladder]]

### 🟢 Phase 2 — Parametric sweep: thermal mass & L (in progress, started 2026-09-01)
`#parametric-sweep #thermal-mass #baseplate-L #T_junction`
**Objective:** For different thermal mass and different L (thickness under IGBT), run the 1D model and characterise how IGBT junction temperature behaves.
**Tasks:**
- [ ] Mask `Subsystem1` with **geometry** params (L, A_contact, A_base, k, masses, h, A_fin); mask init recomputes R_cond, R_spread, R_ch — so changing L auto-recomputes spreading (per [[Spreading resistance — heat enters over the source, not the whole base]])
- [ ] Define sweep matrix — L values (min/mid/max) × thermal-mass values (min/mid/max)
- [ ] Run sweep via `FastRestart` — capture steady-state T_j and transient τ per point
- [ ] Plot T_j vs L (fixed thermal mass) and T_j vs thermal mass (fixed L)
- [ ] Present fin study as an **(h, A) contour map of R_conv**, not a single predicted h (per [[Only the h·A product matters for convective resistance]])
- [ ] Identify the knee: at what L / thermal mass does T_j stop improving? (L optimum already ≈ 18.1 mm)
- [ ] Write up conclusion → `Results/YYYY-MM-DD Phase 2 …`

> [!warning] Guardrails from Phase 1 (see the validated write-up)
> Build Phase 2 **in Simulink on the validated model** — a parallel MATLAB reimplementation would fork the validation. Keep `h` as the one fitted number; never bend a derived R to close the +1.89 K bias. Model is transient-only, valid ≤ ~300 s — no steady-state extrapolation.

### ⚪ Phase 3 — TBD
Define once Phase 2 conclusions are in.

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
