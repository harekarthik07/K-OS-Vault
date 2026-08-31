---
type: concept
project: Raptee Vantage
status: core
tags: [verdict, qc, crown-jewel]
---

# Verdict Engine

> How a bike gets its PASS / FAIL. This is the most important thing in the system — every other feature exists to feed or display this.

Source of truth: `fastapi_server.py` lines ~2022–2285, banner `🏆 BIKE VERDICT`.

---

## The mental model

A bike is tested by **three independent stations**. Each station gives its own
verdict. The bike's overall verdict is a **roll-up of the three**.

```
       Dyno rig            Battery-box EOL          Vehicle EOL
          │                       │                      │
   _dyno_verdict_for_bike  _bb_eol_verdict_for_bike  _vch_eol_verdict_for_bike
          │                       │                      │
          └───────────────┬───────┴──────────────────────┘
                          ▼
              /api/bike-verdict/{bike_no}     ← one bike, full detail
              /api/bike-verdict-all           ← every bike, grid view
```

Each helper returns the **same shape**, which is what makes the roll-up trivial:

```python
{"status": "complete" | "missing" | "error",
 "verdict": "PASS" | "FAIL" | None,
 "test_date": "...", "failures": [...], "link": "/dyno"}
```

`verdict: None` means *this station has no data for this bike* — not a failure.
That distinction is the whole reason `INCOMPLETE` exists as an outcome.

---

## The roll-up truth table

```python
has_fail = any(v == "FAIL" for v in verdicts)
complete = all(v is not None for v in verdicts)
has_any  = any(v is not None for v in verdicts)

overall = ("FAIL"       if has_fail
      else "PASS"       if complete
      else "INCOMPLETE" if has_any
      else "NO DATA")
```

| Dyno | BB-EOL | VCH-EOL | Overall | Why |
|---|---|---|---|---|
| PASS | PASS | PASS | **PASS** | all three in, all clean |
| PASS | FAIL | PASS | **FAIL** | one fail is enough |
| FAIL | — | — | **FAIL** | fail wins even with data missing |
| PASS | PASS | — | **INCOMPLETE** | clean so far, not fully tested |
| — | — | — | **NO DATA** | bike unknown to all three |

**Read the order carefully: `FAIL` is checked before `complete`.** A bike with
one FAIL and two missing stations is FAIL, not INCOMPLETE. That is deliberate —
a known defect doesn't get to hide behind missing data.

There is also a `score` field, `"{pass_count}/3"`. It is **display only**.
Never make a decision on it — 2/3 with one FAIL is still a FAIL.

---

## Hard rules — do not violate

1. **Any FAIL → overall FAIL.** No averaging, no "mostly passed", no best-of-N.
   One failing parameter fails the unit.
2. **Never loosen a limit or band to make something pass.** An all-FAIL batch can
   be completely legitimate. Test datasets deliberately contain good *and* bad
   units. If results look wrong, the bug is in the logic or the data — not the
   limits. Fix the cause, never the threshold. See [[Landmines]].
3. **`in_verdict` is the gate.** Excluded units never drive a bike verdict.
   Respect it *everywhere* a roll-up happens. See [[in_verdict Gate]].
4. **VCH-EOL exclusions are intentional.** Admin-deselected params and the three
   acceleration params are left out by design. See [[VCH-EOL]].
5. **Test/dummy files are blocked at intake**, not filtered later. If junk reaches
   the DB, the intake filter is what to fix — not the verdict code.

---

## The three station engines are NOT the same

This is the single most misunderstood thing about the system. They produce the
same output shape but work completely differently inside:

| | Dyno | BB-EOL | VCH-EOL |
|---|---|---|---|
| Grading source | hardcoded `envelope_*` tables | **active golden version** | **active golden version** |
| Unit of evaluation | 4 channels @ t=120 s | every test step | every parameter row |
| Verdict rule | any breach → FAIL | `failing_steps == 0` → PASS | parsed `final_result` |
| Exclusion gate | *none* | `is_counted()` | `counted_only=True` |
| Auto-pass path | golden bikes bypass all checks | none | none |

So "how does the verdict work" has **three different answers**. Always ask which
suite before answering. Details in [[Dyno]], [[BB-EOL]], [[VCH-EOL]].

---

## Caching — a real gotcha

`/api/bike-verdict-all` has a **30-second server-side TTL cache**
(`_bike_verdict_cache`, `_BIKE_VERDICT_TTL`). It is busted on any upload,
reprocess, or dispatch action.

**If a verdict "didn't update", suspect this cache first**, before suspecting
the logic. Wait 30 s or trigger a bust, then re-check.

`/api/bike-verdict/{bike_no}` is **not** cached — it recomputes live. When
debugging a specific bike, always use the single-bike endpoint; it tells the truth.

---

## Bike-number matching is fuzzy, per suite

Each suite identifies "which bike is this?" differently. Mismatches here show up
as phantom `INCOMPLETE` verdicts — the data exists, it just didn't match.

| Suite | How the bike number is found |
|---|---|
| Dyno | regex on `Test_Name`: `-(\d+)-BK` or `BK[_-]?(\d+)` |
| BB-EOL | `_lookup_bike_no(battery_barcode)` — registry lookup, barcode → bike |
| VCH-EOL | tries `BIKE-07` **then** `BIKE-7` (zero-padded and not) |

**Debugging an INCOMPLETE that shouldn't be:** check the identifier match before
checking the grading logic. A renamed dyno file or an unregistered barcode is the
usual culprit, not the engine.

---

## "Most recent wins"

Every helper takes `matched[0]` / `reports[0]` after a DESC ordering. Only the
**latest** test at each station counts. A bike that failed then was reworked and
passed shows PASS — history is kept in the DB but does not affect the verdict.

---

## Where to look when a verdict is wrong

Walk it in this order — it's cheapest to most expensive:

1. **Is it the cache?** Use `/api/bike-verdict/{n}` instead of the grid.
2. **Did the bike match?** Check identifier matching above.
3. **Is the unit excluded?** Check [[in_verdict Gate]].
4. **Which golden version is active?** See [[Golden Versions]].
5. **Which parameter actually breached?** Read `failures[]` — note it's **truncated
   to 3** in the API response; the DB holds all of them.
6. Only then read the suite's eval code.

Record each real investigation as a note in `Experiments/`.

## Related
- [[Golden Versions]] · [[in_verdict Gate]] · [[Architecture]] · [[Landmines]]
- Suites: [[Dyno]] · [[BB-EOL]] · [[VCH-EOL]]
