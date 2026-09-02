---
type: daily_log
project: CFD based heatsink thermals study (forced and natural convection)
---

# Daily Log — CFD based heatsink thermals study (forced and natural convection)

Append newest at top. One `##` per day.

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
