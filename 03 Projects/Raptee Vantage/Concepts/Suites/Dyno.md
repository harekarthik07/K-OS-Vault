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

## No exclusion gate

Dyno has **no `in_verdict` equivalent**. Every dyno run counts. There is no way
to exclude a test/dummy run today. See [[Questions]] Q3.

## Key files
- `dyno_backend/` — parsing, DB manager
- `fastapi_server.py:2026` `_extract_dyno_bike_no`
- `fastapi_server.py:2033` `_dyno_verdict_for_bike`
- Frontend: `vch-next-frontend/app/dyno/`

## Related
[[Verdict Engine]] · [[Architecture]] · [[Landmines]] · [[Cross-Compare]]
