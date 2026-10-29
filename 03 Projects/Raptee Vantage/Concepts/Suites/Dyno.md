---
type: suite
project: Raptee Vantage
suite: Dyno
backend: dyno_backend/
db: dyno_backend/raptee_dyno.db
api_prefix: /api/dyno/*
frontend: vch-next-frontend/app/dyno/
---

# Dyno

> Dynamometer rig testing. Thermal rise across four channels + power output, graded against envelope curves.

**The odd one out:** Dyno does **not** use [[Golden Versions]]. It grades against
hardcoded `envelope_*` tables in its own DB, plus a statistical band derived from
golden-bike runs. Same output shape, completely different mechanism.

---

## Data flow

```
dyno rig CSV → intake → dyno_summaries table
                             │
                    envelope_IGBT / _Motor / _HighCell / _AFE
                             │
                  _dyno_verdict_for_bike(bike_no)
                             │
                        PASS / FAIL
```

## Bike identification

Regex on `Test_Name` (e.g. `2025_10_22-07-BK`):
```python
r'-(\d+)-BK'        # primary
r'BK[_-]?(\d+)'     # fallback
```
A renamed or oddly-formatted dyno file simply won't match → the bike shows
INCOMPLETE with no dyno data. Check the filename before the logic.

## Golden bikes auto-pass ⚠️

```python
if any(g in test_name for g in GOLDEN_BIKES):
    return {"verdict": "PASS", "failures": []}
```

If the test name contains a `GOLDEN_BIKES` token, **every check is skipped** and
PASS is returned immediately. Reference units are known-good by definition. This
is correct — but it's surprising during debugging. Always check whether the bike
you're investigating is a golden bike.

## The two checks

### 1. Thermal rise vs envelope — four channels

Channels: `IGBT`, `Motor`, `HighCell`, `AFE`.
Evaluated at a **single time slice: `TIME_S = 120`** seconds.

```python
val_dt = row[f"{ch}_dT_{TIME_S}s"]  or  row[f"{ch}_dT_Max"]   # fallback
up_dt  = envelope[ch]["dT_Upper_20Pct"]  at  Time (s) == 120
if val_dt > up_dt:  FAIL
```

Notes:
- Missing envelope for a channel → that channel is **silently skipped**, not failed.
- Only the upper bound is checked. There is no lower thermal bound.
- Only t=120 s is checked, not the whole curve. ([[Questions]] Q4)

### 2. Power vs golden-bike mean

```python
g_powers = [ Power_Avg_120s of golden-bike rows where 19 ≤ p ≤ 20.5 ]
mgp      = mean(g_powers)  or  19.5 if none
if not (mgp * 0.90 ≤ bike_power ≤ mgp * 1.10):  FAIL
```

A **±10% band around the mean of golden-bike power**. The `19–20.5 kW` filter
keeps outlier golden runs from dragging the mean. `19.5` is the hardcoded
fallback when no golden runs qualify.

⚠️ This band is **data-dependent** — it moves as golden-bike runs are added. Two
identical bikes tested months apart can be graded against different bands.

## Verdict rule

```python
verdict = "FAIL" if failures else "PASS"
```
Any breach across either check → FAIL. `failures[]` truncated to 3 in the response.

##### Wrong Procedure (third outcome)

If a ΔT check fails **and** the run started too hot, the run is `WRONG_PROCEDURE`, not FAIL:

```
start_temp = HighCell_Raw_Max − HighCell_dT_Max      # T[0] from stored columns
golden            → PASS
all ΔT pass & power pass → PASS
ΔT fails & start_temp > start limit (default 38 °C) → WRONG_PROCEDURE
else              → FAIL
```

A wrong-procedure run is quarantined: it's left out of the pass rate and must be repeated. The start limit can be changed on the Overview (34–45 °C).

##### ⚠️ Four copies of the rule

The Dyno verdict is written out in **4 places**, and they don't all match:

| Where | Wrong-procedure check? |
|---|---|
| `fastapi_server.py` `run_qc_eval` (`/api/dyno/qc_eval`) | — |
| `fastapi_server.py` `_notify_dyno_verdicts` (Teams alerts) | yes |
| `fastapi_server.py` `_dyno_verdict_for_bike` (`/api/bike-verdict`) | **no** |
| `vch-next-frontend/app/dyno/verdict.js` (Overview) | yes |

So a bike whose latest run is WRONG_PROCEDURE on the Overview shows **FAIL** in `/api/bike-verdict` and Fleet. See [[Questions]] Q8.

## Overview page (since v1.7.3)

The Dyno **Overview** is the one QC page. The Trend QC Lab tab was merged into it on 2026-10-27; old `?tab=trend_qc_lab` links open the Overview.

**It counts bikes, not runs.** Each bike counts once with its **latest** test (newest `Test_Name`, same rule as `_dyno_verdict_for_bike`). Golden bikes and wrong-procedure runs are left out of the pass rate. The Run Verdict Log at the bottom still lists every run.

**Batch** = 10 bikes in a row by bike number (S1 = 1–10, S2 = 11–20 …). Test names whose bike number won't parse go to "Unassigned" and are only in the run log.

Six blocks, top to bottom:
1. **Status**: pass rate, passed/graded, failing, wrong procedure, top failing check, runs on record, verdict rule + start-limit selector
2. **Trend**: pass/fail per batch, or "by test date" (bikes placed on their latest test's date)
3. **Why bikes fail**: batch × check heatmap + bikes-failed-per-check bar
4. **Limit Watch**: batch average per check vs limit, sorted by headroom of the last 3 batches
5. **Batch vs Batch**: folded until opened
6. **Act on it**: runs to repeat + Run Verdict Log

Only the 5 checks that decide PASS/FAIL appear (4 ΔT + power). Code: `app/dyno/components/DynoOverview.js`, `DynoQcBlocks.js`, `app/dyno/trendSeries.js`. Record: [[2026-10-27 Dyno Overview merged v1.7.3]].
## No exclusion gate

Dyno has **no `in_verdict` equivalent**. There is no way to manually exclude a test/dummy run today. See [[Questions]] Q3.

The only automatic exclusions are on the Overview: wrong-procedure runs, golden bikes, and retests (only a bike's latest test counts). The backend `_dyno_verdict_for_bike` still has no wrong-procedure exclusion (Q8).

## Key files
- `dyno_backend/` — parsing, DB manager
- `fastapi_server.py:1749` `_extract_dyno_bike_no` (checked 2026-10-27)
- `fastapi_server.py:1756` `_dyno_verdict_for_bike` (checked 2026-10-27)
- `fastapi_server.py` `run_qc_eval`, `_notify_dyno_verdicts`: the other backend copies of the rule
- `vch-next-frontend/app/dyno/verdict.js` — frontend verdict (`computeDynoVerdicts`)
- `vch-next-frontend/app/dyno/trendSeries.js` — batch rollup, bike-number parser, headroom
- `vch-next-frontend/app/dyno/components/DynoOverview.js` + `DynoQcBlocks.js` — the Overview page

## Related
[[Verdict Engine]] · [[Architecture]] · [[Landmines]] · [[Cross-Compare]]
