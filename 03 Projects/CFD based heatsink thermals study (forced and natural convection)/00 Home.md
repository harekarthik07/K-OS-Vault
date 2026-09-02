---
type: project_home
project: CFD based heatsink thermals study (forced and natural convection)
status: active
started: 2026-09-01
domain_primary: CFD
domain_secondary: [Thermal Management, Heat Transfer]
current_phase: Phase 1
---

# CFD based heatsink thermals study (forced and natural convection)

> CFD (Fluent) conjugate heat transfer study of the MC heatsink under mixed (forced + natural) convection, to extract dyno-validated zone-wise h for the [[MC_HS_ETM_I1]] Cauer network.

## Sections
- [[Daily Log]]
- [[Questions]]
- Experiments/ — one note per experiment
- Results/    — final outputs, plots, verdicts
- Concepts/   — incubating knowledge (harvested on Friday)
  - [[MC Heatsink CHT — Consolidated Setup]] — validated baseline (Boussinesq + Sutherland)
  - [[Fan 3D Zone Setup]] — 3D fan momentum-source setup
  - [[CHT Air Properties — Incompressible-Ideal-Gas (Superseded)]] — earlier attempt, reverted
  - [[CHT Case Configurator — Math Behind Every Section]] — theory backing the custom configurator tool
  - [[Fan PQ Health Check & Reverse-Flow Diagnosis]] — reverse-flow root cause + reusable PQ convergence gate
- Resources/  — links, papers, datasheets (promoted on close)

---

## Roadmap

### 🟢 Phase 1 — MC heatsink CHT baseline (in progress, started 2026-09-01)
`#fluent #CHT #boussinesq #y+`
**Objective:** Get the validated Boussinesq + Sutherland baseline (see [[MC Heatsink CHT — Consolidated Setup]]) to convergence and extract zone-wise h for the Cauer model.
**Tasks:**
- [x] Fix Reference Values (Temperature → 309.16 K, Reference Zone → fluid) ✅ 2026-09-02
- [x] Enter IGBT energy source (`750 [W] / Volume("igbt-die-zone")`) ✅ 2026-09-02
- [x] Load fan curve, verify rotational direction ✅ 2026-09-02
- [x] Std init + patch (fluid 309.16 K, IGBT 350 K, HS 320 K) ✅ 2026-09-02
- [x] Run to convergence — residuals + report-value plateau + energy balance <1 % ✅ 2026-09-02
- [x] **2026-09-02 blocker:** reverse flow at fan exit on [[HS_I1-G1-K1]] — see [[Fan PQ Health Check & Reverse-Flow Diagnosis]] ✅ 2026-09-02
  - [ ] Pull old-case operating point, confirm `K_new/K_old ≈ 3–4`
  - [ ] Re-converge: Hybrid Init + FMG, coupled + pseudo-transient, 1st→2nd order, backflow BCs set
  - [ ] Re-run PQ health check — require `ε < 5 %` before trusting any result
  - [ ] If still choked after convergence → escalate fin redesign to MC team
- [ ] Check actual mesh y+ on HS, set Yplus-for-HTC to match
- [ ] Report per-zone h — **under-hub vs impingement, kept separate** → feed [[MC_HS_ETM_I1]] R_conv (consider 3-node Cauer w/ dead-zone branch)
- [ ] Write up → `Results/YYYY-MM-DD Phase 1 …`

### ⚪ Phase 2 — Build CHT Case Configurator tool (queued, started 2026-09-01)
`#custom-tool #configurator #dimensionless-numbers #simulink-bridge`
**Objective:** Build a custom tool that takes case inputs (T∞, Tw, L, U, geometry), classifies the convection regime, recommends solver/physics setup, gives a pre-run h estimate, and post-CFD converts zone-wise h into copy-paste Cauer R_conv branches. Math backing: [[CHT Case Configurator — Math Behind Every Section]].
**Tasks:**
- [ ] Property engine — air table (−50…200 °C @ 1 atm), film-temp interp, derived ν/α/β
- [ ] Section 1 — Ri classifier + log-scale spectrum marker
- [ ] Section 2 — Re, Pr, Gr, Ra, Ri, ΔT/T∞, Ma readouts
- [ ] Section 3 — setup advisor (density / μ,k / viscous / pressure / radiation), solver block fixed
- [ ] Section 4 — pre-run h via Nu correlations (flat-plate forced, Churchill–Chu, Churchill–Bernstein, mixed)
- [ ] Section 5 — post-CFD h extractor (per-zone h, area-weighted, energy check, R_conv output)
- [ ] Validate against the default case (T∞ 36, Tw 110, L 0.05, U 3) — numbers match the worked examples in the math note
- [ ] Section 6 — automated fan PQ health check (ε gate, φ, slope, K) per [[Fan PQ Health Check & Reverse-Flow Diagnosis]]
- [ ] v0.2 hooks (see math note): fluid library, fin-array Nu, Simulink export format, Ra-based y+ target
- [ ] Write up → `Results/YYYY-MM-DD Phase 2 …`

### ⚪ Phase 3 — TBD
Define once Phase 1 h values and the configurator are in.

---

## Open Concepts (incubating)
```dataview
LIST FROM "03 Projects/CFD based heatsink thermals study (forced and natural convection)/Concepts"
WHERE status = "incubating"
```

## Atlas Connections
- [[CFD]]
- [[Thermal Management]]
- [[Heat Transfer]]
