---
type: suite
project: Raptee Vantage
suite: VCH-EOL
backend: eol_backend/
db: eol_backend/raptee_eol.db
api_prefix: /api/eol/*, /api/vch-eol/*, /api/vch_eol/*
frontend: vch-next-frontend/app/fleet-eol/
---

# VCH-EOL — Vehicle End-of-Line

> Whole-vehicle end-of-line testing. Parameters graded against the active golden version, with a deliberate set of exclusions.

⚠️ **Route naming trap.** This suite uses *both* forms:
- `/api/vch_eol/*` (**underscore**) → golden version management
- `/api/vch-eol/*` (**hyphen**) → QC analysis, summary, reports

Don't "fix" one to match the other without updating the frontend callers. See [[Landmines]].

---

## Data flow

```
vehicle EOL report → intake → vehicle_eol_results
                                     │
                     params graded vs active golden version
                       (minus deselected, minus accel params)
                                     │
                            final_result column
                                     │
                    get_vd_reports(counted_only=True)
                                     │
                    _vch_eol_verdict_for_bike(bike_no)
```

## Bike identification

Tries **two formats**, zero-padded first:
```python
for fmt in [f"BIKE-{bk_int:02d}", f"BIKE-{bk_int}"]:   # "BIKE-07", then "BIKE-7"
```
First match wins. This is why an inconsistently-formatted `bike_id` still resolves.

## Result parsing

The raw report carries `OK` / `NOT OK`, mapped to the system's vocabulary:

```python
final_result = "PASS"    if final_raw == "OK"
          else "FAIL"    if final_raw == "NOT OK"
          else "PENDING"
```

`PENDING` is the default when no recognisable result is found. It is **not** a
pass and **not** a fail — it flows up as a real verdict value, so a PENDING
report makes the bike's roll-up non-PASS without making it FAIL.

`failures` is a **semicolon-separated string** in the DB, split and truncated to
3 for the API response. The full list stays in the DB.

## The exclusions — intentional, do not "fix" ⚠️

Two separate mechanisms leave parameters out of the verdict:

### 1. Admin-deselected params (`eval_now = 0`)

Set per golden version. `get_deselected_params()` returns the list. These are
staged/known-noisy parameters an admin has switched off. They still display —
they just don't vote.

### 2. The three acceleration params — hardcoded

```python
_ACCEL_SKIP_PARAMS = ("distance travelled", "max tractive power", "regen")
```

Case-insensitive **substring** match on the param name. Always excluded,
regardless of golden version. Not configurable.

The report API surfaces both sets so the UI can show *why* something isn't graded:
```python
data["accel_skip_params"] = list(_ACCEL_SKIP_PARAMS)
```

**These exclusions are by design.** A parameter showing a value but no verdict is
correct behaviour, not a bug.

## Exclusion gate

Same idea as BB-EOL's `in_verdict`, exposed as a keyword argument instead of a
helper:

```python
vd_engine.get_vd_reports(bike_id=..., counted_only=True)
```

Both `_vch_eol_verdict_for_bike` and `/api/bike-verdict-all` pass
`counted_only=True`. See [[in_verdict Gate]].

## Supersession

Reports carry a `superseded_by` column — a re-test supersedes an earlier report.
Combined with "most recent wins" in the roll-up, a reworked bike reflects its
latest state.

## Recompute

`final_result` can be recomputed and rewritten:
```sql
UPDATE vehicle_eol_results SET final_result = ?, failures = ? WHERE id = ?
```
This is how activating a new golden version re-grades existing reports. It is
admin-gated — as anything limit-changing must be.

## Key files
- `eol_backend/vehicle_dyno_manager.py` — parsing (~285), `_ACCEL_SKIP_PARAMS` (~482), `get_deselected_params` (~958), `get_vd_reports` (~1391)
- `fastapi_server.py:2141` — `_vch_eol_verdict_for_bike`
- Frontend: `vch-next-frontend/app/fleet-eol/`

## Related
[[Verdict Engine]] · [[in_verdict Gate]] · [[Golden Versions]] · [[BB-EOL]] · [[Landmines]]
