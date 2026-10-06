---
title: Long-Cycle Validation — Approach & TODO
project: MC_HS_LongCycle_Validation
type: approach-todo
status: active
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-01
tags: [thermal, validation, matlab, TODO]
related: "[[Problem_Statement]] [[Section4_Theory_LongCycle]] [[Progress_Log]] [[Flowchart]]"
---

# Approach & TODO

## Principle (ponytail)
One model, not two. The solver is already duration-agnostic (Q as [t Q] series). We change
only: how dt is chosen, how many points we draw, and which fit metrics we report.

## Phase gates (verify-before-advance)
| Phase | Deliverable | Gate | Status |
|---|---|---|---|
| 1 | `thermal_core` adaptive dt | dyno 4-min still Tj 93.5 (explicit dt override unchanged) | NEXT |
| 2 | app: dyno/long-cycle selector + decimation | WLTP loads, no slider lag | - |
| 3 | `cycle_fit`: RMSE + bias + lag | metrics print; lag sign convention correct | - |
| 4 | overlay measured vs model on long run | WLTP 48->57 degC tracked, lag read | - |

## Phase 1 detail (next turn)
```
dt = min( max(0.05, p.t_end/20000), 0.5 )   % only when p.dt not supplied
```
Explicit p.dt still wins, so test_core (p.dt=0.01) is untouched -> gate holds.

## Phase 2 detail
- Validation-mode dropdown: Dyno 4-min | Long cycle (label + decimation trigger)
- Display decimation: step = max(1, floor(N/4000)); cursor still indexes full R
- Reuses the existing Excel path in q_builder — no new loader

## Phase 3 detail
- `cycle_fit(t, Tmodel, Tmeas)` -> rmse, bias, lag, rho
- xcorr('coeff') with exist() guard + bounded-window fallback (+/-120 s)
- sign: lag>0 = measured leads = model sluggish = C too large

## Deferred / not now
- h(v) ram-air term (next project)
- Road-cycle validation (needs h(v))
- 100-run dyno h re-fit (separate task; tightens h_fan anchor)
