---
type: daily_log
project: CFD based heatsink thermals study (forced and natural convection)
---

# Daily Log — CFD based heatsink thermals study (forced and natural convection)

Append newest at top. One `##` per day.

---

## 2026-09-02
**Did:**
- Diagnosed persistent reverse flow at the fan exit on the new heatsink [[HS_I1-G1-K1]] (150+ faces and growing, continuity stalled ~6e-2). Ruled out hub blockage, H/D and the fan zone — all unchanged. Root cause: fin redesign (curved/open → straight/tight + central pin cluster) raised system K ~3–4×.
- Defined a reusable **fan PQ health check** (Q_op, Δp_op, curve interpolation, ε gate, φ, slope, K) → [[Fan PQ Health Check & Reverse-Flow Diagnosis]].
**Learned:**
- A *growing* reverse-flow face count is a physics/BC problem, not solver noise — more iterations won't fix it.
- ε = |Δp_op − Δp_curve|/Δp_curve is a better convergence gate than residuals for fan cases. This case: ε = 17.3 % → results untrustworthy. φ = 0.357 → already at the choked edge.
- The hub-shadow dead zone at H/D = 0.14 is real physics, not an artefact — it needs its own h, not an averaged one. Possible 3-node Cauer with a parallel dead-zone branch.
**Next:**
- Pull the old-case operating point to confirm K_new/K_old ≈ 3–4, then converge (Hybrid+FMG, coupled + pseudo-transient) to ε < 5 % before extracting any h.
**Concepts touched:** [[Fan PQ Health Check & Reverse-Flow Diagnosis]]

---

## 2026-09-01
**Did:**
- Consolidated the MC heatsink CHT setup into a single validated-baseline note (Concepts/MC Heatsink CHT — Consolidated Setup.md): Boussinesq density + Sutherland viscosity, operating conditions, reference values, y+ based h extraction method, and the proven Courant-200 coupled solver config.
**Learned:**
- Boussinesq's buoyancy-linearization error only matters where buoyancy matters — this case is fan-dominated (low Ri), so the error is negligible despite the large ΔT.
- The earlier ideal-gas + pseudo-transient attempt stalled mainly from the solver change (explicit pseudo-time with a conservative timescale), not primarily from the density model.
- Rule going forward: change ONE thing at a time — physics OR solver, never both — when testing a new model.
**Next:**
- Merge in the older "CHT Fluent Based Setup" note (sitting in Inbox on the other PC, not yet synced to this vault) once available.
- Run to convergence, check actual mesh y+, set Yplus-for-HTC, extract per-zone h, feed into Cauer R_conv branches.
**Concepts touched:** [[MC Heatsink CHT — Consolidated Setup]]

### later 2026-09-01
**Did:**
- Filed the CHT Case Configurator math reference (theory under a planned custom tool): [[CHT Case Configurator — Math Behind Every Section]]. Covers property engine (film-temp interp), Section 1 Ri classifier, Section 2 dimensionless-number panel, Section 3 setup advisor thresholds, Section 4 pre-run Nu→h correlations, Section 5 post-CFD zone h → Cauer R_conv bridge, all worked against the default case (T∞ 36, Tw 110, L 0.05, U 3).
- Added Phase 2 to the project roadmap for the tool build.
**Learned:**
- The "corrected Boussinesq insight" formalised: buoyancy-model validity scales with how much buoyancy actually matters (i.e. with Ri), not just with ΔT/T. That's why Boussinesq is fine here even at ΔT/T = 0.24.
**Next:**
- Finish Phase 1 CFD run first (h values needed as the tool's post-run validation case).
**Concepts touched:** [[CHT Case Configurator — Math Behind Every Section]]
