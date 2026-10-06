---
title: Long-Cycle Validation — Flowchart
project: MC_HS_LongCycle_Validation
type: flowchart
status: active
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-01
tags: [thermal, validation, architecture]
related: "[[Problem_Statement]] [[Approach_and_TODO]]"
---

# Flowchart — long-cycle validation flow

```mermaid
flowchart TD
    MODE{Validation mode}
    MODE -->|Dyno 4-min| DY[run sheet, ~240 s, 480 samples]
    MODE -->|Long cycle| LC[WLTP sheet, ~3000 s, 6000 samples]

    DY & LC --> QB[q_builder 'excel'<br/>cols A-E, 2 Hz]
    QB --> LOSS[loss_from_idiq<br/>P_inv per row]
    LOSS --> QT["[t Q] series"]

    QT --> CORE[thermal_core<br/>adaptive dt = min max 0.05 tend/20000, 0.5]
    CORE --> TMOD[T_ntc model]
    SHEET[col E: T_meas] --> CMP
    TMOD --> CMP[cycle_fit]
    CMP --> M1[RMSE - magnitude]
    CMP --> M2[bias - offset]
    CMP --> M3[xcorr lag - timing -> C]

    TMOD & SHEET --> PLOT[overlay, decimated to 4000 pts]

    CORE -.gate.-> G[dyno 4-min still Tj 93.5]
```

## Three orthogonal metrics
- RMSE -> size error -> R / loss model
- bias -> constant offset
- lag  -> timing error -> capacitance C (first dynamic test of it)
