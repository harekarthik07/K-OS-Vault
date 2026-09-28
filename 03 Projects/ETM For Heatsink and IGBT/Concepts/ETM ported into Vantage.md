---
concept: ETM ported into Vantage
project: ETM For Heatsink and IGBT
domain: Thermal Management
status: incubating
created: 2026-09-03
sources: ["[[Daily Log#2026-09-03]]"]
related: ["[[MC_HS_ETM_I1]]", "[[Heat-Transfer Module — Build & Decisions]]", "[[IGBT Electro-Thermal Loss Modelling]]"]
tags: [ETM, vantage, port, thermal, second-brain]
---

# ETM ported into Vantage

> [!abstract] TL;DR
> The Simulink electro-thermal model [[MC_HS_ETM_I1]] now has an **interactive web port**
> inside Raptee Vantage. Same chain — SVPWM inverter losses → 2-node Cauer thermal network
> → junction temperature vs measured, deration at 95 °C. The Vantage note is the live
> implementation record: [[Heat-Transfer Module — Build & Decisions]].

## What carried over
- **Loss stage** — [[IGBT Electro-Thermal Loss Modelling]] formulae, implemented server-side
  in `heat_transfer_backend/etm_loss.py`. Verified against the `Inverter_Loss_Calculation_Documentation`
  §7 worked example (Pcond,T 251.9 W, Ppos 300.4 W).
- **Thermal stage** — the `.slx` 2-node Cauer (junction `C_plate` → `Rjc` → heatsink `C_hs`
  → `R_conv` → ambient), with `C = m·cp` and `R_conv = 1/(h·A)` taken from `Reference.xlsx`
  Derived Calcs. Solved as a small ODE (scipy) — no Simscape engine needed.
- **Calibration** — the `Sweep_h.m` RMSE h-fit against a measured `IGBT_Temp` trace.

## What's different from the Simulink model
- Input comes from an **uploaded per-bike xlsx**, not `FromSpreadsheet` blocks (and not the
  dyno DB — it has no current channels).
- **No values are hardcoded** — every constant is a user input; the reference sheet values
  load only on explicit request. The known disputes (Rjc per-die vs per-module, C_plate
  490 vs 500) are exposed as user choices, tracked in [[Heat-Transfer Module — Build & Decisions]].

## Still open (same as the model's)
Rjc per-die vs per-module (6× on Tj) · C_plate 490 vs 500 · which P drives the node ·
Vdc constant vs per-sample. See [[MC_HS_ETM_I1]] open items.

## Atlas
- [[MC_HS_ETM_I1]] · [[Heat-Transfer Module — Build & Decisions]] · [[Heat Transfer]]
