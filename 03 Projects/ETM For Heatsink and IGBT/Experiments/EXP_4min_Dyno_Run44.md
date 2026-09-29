---
type: experiment
project: ETM For Heatsink and IGBT
status: done
created: 2026-09-29
case: actual 4-min thermal test (dyno run 44) — validated, RMSE 0.82 K
tool: mc_thermal_app.m (thermal_core, Excel-run mode)
related: ["[[00 Home]]", "[[EXP_PeakPower_Constant_470W]]", "[[2026-09-29 Peak-power vs 4-min dyno — model application & conservatism]]", "[[1D Thermal Design Tool — README & usage]]"]
---

# EXP — Actual 4-minute thermal test (dyno run 44)

> **Purpose:** drive the model with the **real dyno run-44 time series** (measured Id, Iq, Vdc per sample) instead of a flat wattage, so `P_inv` is computed per-row and the temperature curve reflects the actual duty — soft-start ramp and DC-bus sag included.

## Setup (inputs)
![[MC-ETM -Input -2-4min-peak-power-actual-test-dyno.png]]

| Input | Value |
|---|---|
| Q mode | **Excel run** — `44.xlsx`, sheet `44`, range `A3:E588` (row 3 = first data row) |
| Per-row inputs | A = time, B = Vdc, C = Id, D = Iq → `loss_from_idiq` → per-row `P_inv` |
| Alloy / geometry / h / mass | LM25 validated set (same as [[EXP_PeakPower_Constant_470W]]) |
| Ambient / duration | 36 °C / 240 s |

## Measured drive (from `Data/44.xlsx`, columns Time · Vdc · ID · IQ · IGBT_Temp)
![[MC-ETM -output-2-4min-peak-power-actual-test-dyno.png]]
Recomputed from the raw file (546 rows, 0–272.5 s; tool windowed to 240 s):

| Signal | Profile |
|---|---|
| **Iq** | 0 → **85 A** peak after the ~15 s soft-start ramp |
| **Id** | steps to **−107 A** (field weakening) |
| **Irms** | up to **93.5 A** (steady) |
| **Vdc** | **261.2 → 231.6 V** sag, recovers to **245.9 V** by the end (battery droop then relaxation) |
| **P_inv** (loss model, per row) | **mean ≈ 432 W**, peak **≈ 498 W** — *not* a flat 470; the 470 W label is nominal |
| **IGBT_Temp (measured NTC)** | **34 °C → 81 °C** peak |

> [!important] The real duty averages ~432 W, below the 470 W constant screen
> That ~38 W deficit (plus the soft-start ramp and the bus sag) is exactly why the actual run peaks cooler than the constant-470 W case — see the conservatism verdict.

## Model vs measured (validation)
![[MC-ETM -output-4-4min-peak-power-actual-test-dyno.png.jpg]]
The overlay plots the model NTC (blue) against the **measured CAN NTC** (magenta) for the full run:

> [!success] Agreement: **RMSE 0.82 K, bias +0.05 K** — essentially unbiased over 240 s.

| Quantity | @ 60 s | @ 240 s | Δ |
|---|---|---|---|
| T_j (°C) | 69.6 | 91.5 | +21.9 |
| T_ntc — model (°C) | 56.9 | 79.3 | +22.5 |
| **T_meas — CAN NTC (°C)** | **56.0** | **80.0** | +24.0 |
| T_fin (°C) | 41.4 | 63.0 | +21.6 |
| ΔT_j/Δt | — | — | 0.122 °C/s |

**Residual (model − measured):** +0.9 K @ 60 s, −0.7 K @ 240 s → the model crosses the data, not offset from it (bias +0.05 K). `Rhs / Rtot / τ2 = 0.0319 / 0.1858 / 425`; peak T_j 91.5 °C, measured NTC peak **80.0 °C**.

## Reading it
- Same network (Rtot 0.1858) as the peak case — only the **drive** differs.
- Because the real profile **ramps from zero** (soft start) and the **bus sags**, the integrated heating is a touch lower than a flat 470 W → **Tj_pk 91.6 °C vs 93.5 °C** for the constant case.
- Still well under 95 °C NTC and 150 °C junction limits.

> [!success] This is a real validation, not just an application
> The measured CAN NTC trace is overlaid: **RMSE 0.82 K, bias +0.05 K** across the 4-minute run. The model reads +0.9 K high early and −0.7 K low at the end — it tracks the curve rather than sitting offset. Run 44 is one of the 11 calibration runs; this is its per-run residual.

**Verdict:** PASS; realistic duty is milder than the constant-power bound. Comparison: [[2026-09-29 Peak-power vs 4-min dyno — model application & conservatism]].

---
`run 44` · `excel profile` · `Vdc sag 261->232` · `Tj_pk 91.6` · `soft-start ramp` · `realistic duty`
