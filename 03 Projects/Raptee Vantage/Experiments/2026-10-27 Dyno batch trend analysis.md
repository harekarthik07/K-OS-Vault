---
type: experiment
project: Raptee Vantage
date: 2026-10-27
status: done
---

# 2026-10-27 Dyno batch trend analysis

## Hypothesis
- Grouping bikes into batches of 10 by bike number shows which checks fail most, and whether any check is drifting, better than the run-by-run view.

## Setup
- Live `dyno_backend/raptee_dyno.db`, read-only: 124 tests in `dyno_summaries`, bike numbers 1–128.
- Verdict: the Overview rule (`app/dyno/verdict.js`): ΔT at 120 s vs envelope `dT_Upper_20Pct`, power vs golden mean ±10%, wrong procedure at start > 38 °C.
- Limits that day: IGBT 40.9 °C, Motor 59.4 °C, High Cell 13.9 °C, AFE 10.6 °C, power 17.67–21.60 kW.

## Procedure
1. Parsed bike numbers with the backend regex (`-(\d+)-BK`, then `BK[_-]?(\d+)`).
2. Kept each bike's latest test (newest `Test_Name`). Retested: bikes 4, 9, 16, 17, 22, 80.
3. Left out 6 golden bikes and wrong-procedure runs. 8 tests had unreadable numbers (`45_01`…`45_07`, `3.3`) and went to "Unassigned".
4. Grouped into 13 batches (S1 = 1–10 … S13 = 121–130). Per batch: pass count, per-check pass count, per-check mean.
5. Cross-checked with node asserts: every bike in exactly one batch, every PASS bike passes all 5 checks.

## Raw data / artifacts
| Batch | Pass | High Cell ok | AFE ok | Motor ok | Motor ΔT avg |
|---|---|---|---|---|---|
| S1 | 0/2 | 0/2 | 1/2 | 2/2 | 46.2 |
| S4 | 6/9 | 8/9 | 9/9 | 7/9 | 55.3 |
| S7 | 0/7 | 1/7 | 1/7 | 7/7 | 51.4 |
| S9 | 5/10 | 6/10 | 10/10 | 9/10 | 52.9 |
| S12 | 2/6 | 5/6 | 4/6 | 3/6 | 58.3 |
| S13 | 0/6 | 4/6 | 2/6 | 2/6 | **60.3** |

Totals over 102 graded bikes: **33 pass (32%)**. Bikes failed per check: High Cell 44 · AFE 31 · Motor 18 · Power 8 · IGBT 0.

## Observations
- **High Cell ΔT is the #1 fail cause** in almost every batch. Batch averages sit right at the 13.9 °C limit (last 3 batches 13.4 °C, headroom ~3%).
- **Motor ΔT is drifting up**: S1 46.2 → S13 60.3 °C. S13's average is over the 59.4 °C limit; headroom of the last 3 batches is ~4%.
- **AFE** headroom is only ~2%, with S7 and S13 mostly failing it.
- **IGBT never failed a bike.** Averages ~29 °C vs 40.9 °C limit (~29% headroom).
- Power fails rarely (8 bikes), mostly early batches.

## Verdict
- Batch view is worth having. It turned into the Overview's Trend / Why bikes fail / Limit Watch blocks ([[2026-10-27 Dyno Overview merged v1.7.3]]).
- The Motor drift is real in the data but its cause is unknown: [[Questions]] Q6. Limits were **not** touched.

## Concepts touched
[[Dyno]] [[Verdict Engine]] [[Landmines]]
