---
title: Long-Cycle Validation — Progress Log
project: MC_HS_LongCycle_Validation
type: progress-log
status: active
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-01
tags: [thermal, validation, progress]
related: "[[Problem_Statement]] [[Approach_and_TODO]]"
---

# Progress Log

## 2026-10-01 — Kickoff, Sections 1-6
- Attribution corrected: this project is Hare Karthik's (Vehicle Engineering), not Sarath.
- `/start` run. Scope: dyno/long-cycle data selector for IGBT-temp validation. h constant.
- Confirmed data format from WLTP file: 2 Hz, cols A-E = Time/Vdc/ID/IQ/IGBT_Temp,
  sheet 3, 6084 samples, 50.7 min. No loader change needed.
- WLTP run characterised: P_inv avg 27 W / peak 188 W, IGBT 48->57 degC — low-load cycle,
  tests dynamics (capacitance), not thermal stress.
- Section 4 theory written in full: RK4 stability (|lambda.dt|<2.78), adaptive-dt three-way
  rule, cross-correlation lag metric, orthogonality of RMSE/bias/lag.

### Next session starts with
- Phase 1: adaptive dt in thermal_core. Gate: dyno 4-min still Tj 93.5.

### For Claude Code
- New files live beside the v1.0 tool set. thermal_core edit is additive (dt selection only).
- Re-run test_core after the edit — explicit p.dt=0.01 path must be untouched.

## 2026-10-01 — Concepts harvested to Ideaverse (pre-implementation)
Four atomic concepts pulled from Section 4 theory + the approach doc, filed to
`04 Knowledge/concepts/` as `seedling` (status matures once Phase 1-4 implementation lands):
- [[RK4 stability bound sets the max stable time step, not accuracy]]
- [[Adaptive time-step — balance an accuracy floor, a cost cap, and a data floor]]
- [[Cross-correlation lag isolates timing error, orthogonal to RMSE and bias]]
- [[A duration-agnostic solver scales via step selection, not by forking the model]]

## 2026-10-06 — h-only fit delivered, C validated across cooling conditions
- Redesigned from a joint (h,C) fit to **h-only** (C locked at CAD 2402 J/K) after a joint
  fit returned a non-physical C = 1321 J/K — the two parameters are degenerate on a single
  level error.
- Delivered `fit_h_cycle.m` + app "Fit h to cycle" button; ran on 4 conditions.
- **C = 2402 J/K confirmed on every run via lag = +0 s.** h spans ~14-30 W/m2K across
  cooling states (fan-off floor ~14 is the deration-critical case).
- Concept note: [[HS_Transient_Physics_h_and_C]]. Full write-up: [[EOD_2026-10-06]].
- Concepts harvested to Ideaverse (3 new + 1 gotcha + 1 existing upgraded seedling -> budding):
  - [[Capacitance sets transient speed, convection sets steady-state level — lock one before fitting the other]]
  - [[Fit-residual bias sign tells you which direction a locked parameter is wrong]]
  - [[A single fitted parameter is a duty-weighted average of a time-varying process, not a true constant]]
  - [[Ambient reference set from the first logged sample biases any fit against it]] (gotcha)
  - [[Cross-correlation lag isolates timing error, orthogonal to RMSE and bias]] — now `budding`, validated on 3 runs

### Next session starts with
- Segment fit: h(t) piecewise on moving vs idle segments of the road run.
