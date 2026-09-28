---
type: daily_log
project: ETM For Heatsink and IGBT
---

# Daily Log — ETM For Heatsink and IGBT

Append newest at top. One `##` per day.


## 2026-09-15
**Did:**
- Filed the validated ETM thermal-budget write-up (`MC_HS_ETM_I2.slx`) into Results: [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]. Every resistance derived from datasheet/CAD/correlation; single fitted parameter h = 29.59, validated against 11 dyno runs to ~2 K.
- Extracted 7 durable method concepts (calibration philosophy, eigenvalue τ, spreading resistance, h·A product, convection-dominance, debug ladder, ΔT/Q-steady-state-only) and wired them into the write-up + Phase 1 outcome.
- Closed Phase 1 as *validated* (not just theory-matching); loaded Phase 2 with the concrete Simulink-mask + (h,A) contour approach from the write-up's Part 2 plan.
**Learned:**
- Calibrating the right parameter is everything: fitting h gave a 4.9 % spread across 11 runs where fitting the derivable R_hs gave 35 %.
- Convection is 78 % of R_total — solid-conduction refinements move a 17 % term.
**Next:**
- Phase 2: mask Subsystem1 with geometry params, sweep L × thermal mass via FastRestart, present fins as an (h,A) contour.
**Concepts touched:** [[Cauer Model Calibration — fit what you cannot derive]] · [[Spreading resistance — heat enters over the source, not the whole base]] · [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]

---

## 2026-09-03

**Did:**
- Ported the ETM electro-thermal chain into Raptee Vantage as an interactive web module — see [[ETM ported into Vantage]] and [[Heat-Transfer Module — Build & Decisions]].
- Backend: `etm_loss.py` (SVPWM losses, reproduces the loss-doc §7 worked example), `heat_transfer_sim.py` (2-node Cauer + `Sweep_h.m`-style h-calibration). Self-checks pass.

**Decided:**
- Reverse-recovery loss uses the DOC form (`Prr = fsw·Err·(Vdc/Vref)/π`, no current scaling), not the ETM-note variant — user said reference the doc.
- No values hardcoded — every constant is a user input; known disputes exposed as UI choices.

**Next:**
- Feed real FS200R07PE4 hot-Tj constants + a bike-37 run; reconcile Rjc per-die/module and C_plate 490 vs 500.

**Concepts touched:** [[ETM ported into Vantage]] [[MC_HS_ETM_I1]]

## 2026-08-29

### 00:04
[[Thermal Resistance]] again to trigger the card

### CFD for MC - G1, K1, I1
The topology was shared without any struggle for G1 and I1. Due to error in fillets the K1 took about a day to figure out. Lesson learnt: clear the fillets and any geometry inconsistencies first then proceed with the shared topology.
