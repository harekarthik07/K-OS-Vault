---
type: concept
project: Raptee Vantage
status: core
tags: [verdict, qc]
---

# in_verdict Gate

> The flag that decides whether a tested unit counts toward the headline QC numbers. Visible in the repo either way — but excluded units don't vote.

Defined in `bb_eol_backend/bb_eol_db_manager.py` (~line 140).

---

## The problem it solves

Not every pack that gets tested is a real production unit. Engineers run test
packs, dummy packs, 16s1p rigs, repeats. If those counted, the QC success rate
would be garbage. But you also can't just delete them — they're real test records.

So: **keep the record, drop the vote.**

```
in_verdict = 1  →  counts toward verdict / success rate   (default)
in_verdict = 0  →  visible in Test Repo, excluded from headline numbers
```

## The single source of truth

```python
def is_counted(session):
    """THE single definition of "does this pack count toward the QC verdict?"."""
    if session is None: return False
    v = session.get("in_verdict")
    return True if v is None else bool(v)
```

**Every aggregate must go through `is_counted()`** — QC stats, cross-compare,
fleet summary, Teams alerts. That's the whole point: one toggle in the Test Repo
reflects everywhere. If you write a new roll-up and skip this call, you've
introduced a silent inconsistency.

Legacy rows with `in_verdict = NULL` default to **counted**. Fail-safe direction:
an unknown pack counts rather than silently vanishing.

## Three ways a unit gets excluded

| Path | `verdict_reason` | Set by |
|---|---|---|
| **auto name rule** | `test-pack:<token>` | barcode matches an exclude pattern |
| **manual toggle** | `manual` | an engineer's decision in the UI |
| **bulk cleanup** | `legacy` | mass action on old / irregular packs |

**Human reasons are sticky.** `apply_verdict_name_rule()` re-runs the auto rule
across all sessions, but it only touches rows whose reason is empty or
`test-pack:*`. It will never override a `manual` or `legacy` decision. This
matters: an engineer's judgement outranks a substring match, permanently.

## The auto exclude patterns

```python
DEFAULT_VERDICT_EXCLUDE_PATTERNS = [
    "test", "dummy", "sample", "trial", "16s1p", "3.2 pack",
]
```

Case-insensitive **substring** match on the barcode. Configurable at runtime via
`set_verdict_exclude_patterns()`, stored in the `bb_eol_config` table — the
defaults are only a fallback.

⚠️ Substring matching is blunt. A legitimate barcode containing "test" anywhere
gets silently excluded. If a real pack goes missing from the numbers, check this
first.

## In SQL

Aggregates filter with:
```sql
WHERE IFNULL(in_verdict, 1) = 1
```
The `IFNULL` is what implements "legacy rows default to counted". Don't drop it.

## VCH-EOL equivalent

VCH-EOL ported the same idea. Its accessor is a keyword argument instead of a
helper function:

```python
vd_engine.get_vd_reports(bike_id=..., counted_only=True)
```

Same semantics: excluded reports never drive a bike verdict, and never appear in
the cross-compare grid. Both `_vch_eol_verdict_for_bike` and
`/api/bike-verdict-all` pass `counted_only=True`.

**Dyno has no equivalent.** There is no way to exclude a dyno run from the
verdict today. See [[Questions]] Q3.

## Alerting

`in_verdict` also gates Teams notifications — an excluded pack failing must not
page anyone. Callers of the alert path check the flag before sending. See
[[Architecture]] for the notification wiring.

## Related
- [[Verdict Engine]] · [[BB-EOL]] · [[VCH-EOL]] · [[Golden Versions]]
