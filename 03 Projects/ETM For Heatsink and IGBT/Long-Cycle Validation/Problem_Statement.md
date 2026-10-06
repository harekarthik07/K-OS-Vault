---
title: Long-Cycle Validation — Problem Statement
project: MC_HS_LongCycle_Validation
type: problem-statement
status: active
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-01
tags: [thermal, ETM, validation, long-cycle, WLTP, T30]
related: "[[Section4_Theory_LongCycle]] [[T30_MC_ETM_Part1_Thermal_Budget]] [[README_thermal_tool]] [[mc-hs-thermal-tool]]"
---

# Problem Statement — Long-Timestamp Data Adaptation

## 1. Objective
Add a data-source selector (`Dyno 4-min` / `Long cycle`) to the MC thermal tool so the
IGBT-temp model can be validated against EITHER a 4-min dyno stress test OR a long
drive-cycle log (WLTP / office / road) — same model, same five-column format, no fork.

## 2. What this phase validates
That the model tracks measured IGBT temp **dynamically** as heat input varies with
throttle. A drive cycle never reaches steady state, so this tests the thermal
**capacitances** (tau1, tau2) — which the monotonic dyno bursts could not isolate.

## 3. What this phase is NOT
- Not a second model. `thermal_core` already takes Q(t) as a series; long data is just a
  longer series into the same solver.
- Not the h(v) / ram-air work. h stays constant at the dyno value (29.59). Differential-h
  is the next project.

## 4. Acceptance gate ("done")
1. Dyno 4-min mode still returns Tj_peak 93.5 after the adaptive-dt change (gate).
2. WLTP sheet loads, model overlays measured IGBT temp, no slider lag on ~6000 samples.
3. Three orthogonal metrics reported: RMSE, bias, cross-correlation lag.
- **Future:** road-cycle validation (needs differential-h first).

## 5. Format (confirmed)
All exports are 2 Hz. Columns A=Time, B=Vdc, C=ID, D=IQ, E=IGBT_Temp. Identical to the
dyno sheets — no loader change. WLTP reference file: 31_08_2026_#0045_Adhi-WLTP,
sheet 3, 6084 samples, 50.7 min.

## 6. Honest flags
- WLTP run is LOW-load (P_inv avg 27 W, peak 188 W; IGBT 48->57 degC). It tests dynamics,
  not thermal stress. Should fit well — at low load it is capacitance-driven and h barely
  matters.
- Still DYNO (no ram air), so constant h is correct for it. A genuine ROAD cycle will show
  the h bias (model runs hot) until differential-h lands — expected, not a bug.
- C was never measured from cooldown; the lag metric is the first dynamic test of it.
