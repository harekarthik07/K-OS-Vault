---
type: suite
project: Raptee Vantage
suite: BB-EOL
backend: bb_eol_backend/
db: bb_eol_backend/bb_eol.db
api_prefix: /api/bb_eol/*
frontend: vch-next-frontend/app/bb-eol/
---

# BB-EOL — Battery Box End-of-Line

> Pack-level end-of-line testing. A pack runs a script of test steps; each step is graded against the active golden version; zero failing steps = PASS.

---

## Data flow

```
EOL station log → intake → test_sessions + test_steps
                                   │
                     evaluate_session(session_id, version_id)
                                   │
                   per-step: PASS / FAIL / FLAG / SKIP
                                   │
                        failing_steps count on the session
                                   │
                    is_counted(session)?  ──no──► excluded
                                   │ yes
                    _bb_eol_verdict_for_bike(bike_no)
```

## Bike identification

`_lookup_bike_no(battery_barcode)` — a **registry lookup**, not a filename regex.
Barcode → bike number via [[Bike Registry]]. An unregistered barcode means the
pack exists but attaches to no bike → phantom INCOMPLETE on the bike.

There is also `_lookup_bike_no_with_tier()` which additionally returns the bike tier.

## Step verdicts — four states, not two ⚠️

This is the most misunderstood part of BB-EOL. From `bb_eol_eval.evaluate_session()`:

| Verdict | When | Counts as failure? |
|---|---|---|
| **PASS** | all evaluated params in band | no |
| **FAIL** | any evaluated param out of band | **yes** |
| **FLAG** | activity not found in the golden version | **no** — needs review |
| **SKIP** | rest step / not in golden / capacity deferred / documented cutoff with no band / no usable reading | no |

**Only FAIL drives the pack verdict.** A FLAG means "we don't know what this step
was" — it's a data-quality signal for a human, not a defect. Treating FLAG as
FAIL would fail packs for a golden-version gap rather than a real fault.

### How a step gets classified

```
rest step, or not in golden      → SKIP  "rest / not in golden"
capacity Ah/Wh activity          → SKIP  "capacity Ah/Wh deferred"
activity not found in golden     → FLAG  "activity not found in golden"
in golden but no band defined    → SKIP  "documented cutoff, no band"
banded:
   no param produced a usable reading  → SKIP  "no usable reading"
   any evaluated param out of band     → FAIL  "param(s) out of band"
   otherwise                            → PASS
```

Inside a banded step, only limits with `eval_now = 1` are checked. A limit
returning `None` from `_check()` (op is `skip`/`raw`, or the bound is missing)
sets no opinion — it neither passes nor fails. See [[Golden Versions]] for the
operator table.

## Phase-total capacity (Ah)

Individual capacity activities are SKIPped during the step loop — but the
**integrated per-phase Ah** is graded separately against the editable Total-row
band (`tree["capacity"]`), producing `AhDischarge` / `AhCharge` results.

**A failing phase folds into the pack FAIL exactly like any out-of-band param.**
So "capacity is deferred" does not mean capacity is ungraded — it means it's
graded at phase level, not step level.

## Pack verdict rule

```python
verdict = "PASS" if failing_steps == 0 else "FAIL"
```

Dead simple by design. All the nuance lives in *what counts as a failing step*.

## Exclusion gate

`is_counted(session)` — the single definition. Excluded packs are visible in the
Test Repo but never drive a bike verdict, never appear in cross-compare, never
alert. Full details in [[in_verdict Gate]].

## Golden versions

BB-EOL is fully golden-versioned: `/api/bb_eol/golden/*` for clone / edit /
activate. `gold.get_golden_tree(version_id)` returns scripts → activities →
limits, plus the capacity bands. See [[Golden Versions]].

If there is **no active golden version**, `evaluate_session` returns
`{"ok": False, "msg": "no active golden version"}` — nothing is graded at all.

## Key files
- `bb_eol_backend/bb_eol_eval.py` — `evaluate_session()` (~266), `evaluate_all()` (~434), `_check()` (~240)
- `bb_eol_backend/bb_eol_db_manager.py` — `is_counted()` (~156), verdict-inclusion rules (~140)
- `fastapi_server.py:2108` — `_bb_eol_verdict_for_bike`
- Frontend: `vch-next-frontend/app/bb-eol/`

## Related
[[Verdict Engine]] · [[in_verdict Gate]] · [[Golden Versions]] · [[VCH-EOL]] · [[Cross-Compare]]
