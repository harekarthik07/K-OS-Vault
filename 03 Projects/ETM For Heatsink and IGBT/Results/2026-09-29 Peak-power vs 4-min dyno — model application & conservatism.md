---
type: result
project: ETM For Heatsink and IGBT
status: done
created: 2026-09-29
objective: Compare the constant-470 W peak screen against the actual dyno run-44 duty, and state which to use for screening.
related: ["[[00 Home]]", "[[EXP_PeakPower_Constant_470W]]", "[[EXP_4min_Dyno_Run44]]", "[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[R = ΔT over Q holds only at steady state]]", "[[Total thermal mass sets the short-duty transient, not the node split]]"]
tags: [result, etm, validation, peak-power, dyno, conservatism]
---

# Result — Peak-power vs 4-min dyno: model application & conservatism

> Two worked cases on the validated LM25 model (h = 29.59), 36 °C ambient, 240 s: **(1)** a flat 470 W peak screen and **(2)** the actual dyno run-44 profile. Question answered: *which case do we screen designs against, and how conservative is it?*

## Shared network (validated set)
`R_cond 0.01313 · R_spread 0.01878 · R_hs 0.03191 · R_ch 0.00818 · R_conv 0.14567 · R_total 0.18576 K/W`, `τ2 ≈ 425 s`. Same for both cases — only the **heat input** differs.

## Head-to-head
| | Case 1 — peak (constant 470 W) | Case 2 — actual run 44 |
|---|---|---|
| Drive | flat 470 W | real Id/Iq/Vdc, `P_inv` per row (ramps 0→~470, Vdc 261→232) |
| **T_j peak** | **93.5 °C** | **91.5 °C** |
| T_ntc peak (model) | 80.9 °C | 79.3 °C @240 s |
| T_ntc peak (measured CAN) | — | **80.0 °C** |
| Validation | (bounding, not a run) | **RMSE 0.82 K, bias +0.05 K** |
| NTC margin to 95 °C | 14.1 °C | 15.0 °C |
| Junction margin to 150 °C | 56.5 °C | 58.5 °C |
| Verdict | PASS | PASS + validated |

## The finding
- **The constant-470 W screen is conservative by ~1.9 °C** on junction (93.5 vs 91.6) versus the real duty. The gap is physical: from the raw run-44 file the **actual P_inv averages ~432 W** (peak ~498 W), not a flat 470 W, because of the **soft-start ramp** (P_inv climbs over ~15 s) and the **bus sag** (261.2 → 231.6 V lowers switching loss mid-run). Less integrated energy → cooler peak.
- **Screen designs against the constant-peak case.** It is the honest upper bound, needs no run sheet, and over-predicts by a known ~2 °C — a safe direction.
- Both cases confirm the design is **transient-limited**: the steady-state ceiling at 470 W is `36 + 470·0.18576 = 123.3 °C` NTC (far past the 95 °C line); the part survives only because `τ2 ≈ 425 s ≫ 240 s` — see [[R = ΔT over Q holds only at steady state]].

## Honest flags
- **Run 44 T_ntc is now validated against measured CAN data: RMSE 0.82 K, bias +0.05 K** — the model tracks the measured curve (crosses it: +0.9 K early, −0.7 K late), it is not a constant offset. This supersedes the generic "~2 K conservative" statement for this run.
- **T_j remains estimated** (no junction sensor) — use RthJC 0.04167 for any safety claim, limit 150 °C. The peak case (constant 470 W) is the design screen; the validated run-44 duty is ~2 K milder.

**Next:** if a still-tighter bound is wanted, screen at 492 W (band max) rather than 470 W — that is the true worst case in the validated envelope.

---
`peak vs actual` · `93.5 vs 91.6` · `+1.9 C conservative` · `screen at constant peak` · `transient-limited`
