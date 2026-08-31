---
type: concept
project: Raptee Vantage
status: core
tags: [verdict, limits]
---

# Golden Versions

> The versioned limit sets that BB-EOL and VCH-EOL grade against. Change the active version and every verdict in that suite changes meaning.

APIs: `/api/bb_eol/golden/*` and `/api/vch_eol/golden/*`
(note the **underscore** form — see [[Landmines]] on route naming).

---

## Why versioned at all

QC limits evolve — a supplier changes, a design revision lands, a band was too
tight. But you cannot silently retune limits on a live system, because then
"BIKE-07 passed" means different things on different dates.

So limits live in **immutable versions**. You clone a version, edit the clone,
then **activate** it. Exactly one version is active per suite at a time. Old
results keep a `version_id` recording what they were graded against.

```
v1 (active) ──clone──► v2 (draft, editable) ──activate──► v2 active, v1 frozen
```

## The three operations

| Op | Effect |
|---|---|
| **clone** | copy the active version into a new editable draft |
| **edit** | change limits / bands / `eval_now` flags on a draft |
| **activate** | make this the version all new evaluations grade against |

Activation is the dangerous one. It is admin-gated
(`dependencies=[Depends(require_admin_token)]`) — as anything limit-changing
must be.

## What a golden version contains

For BB-EOL, `gold.get_golden_tree(version_id)` returns a tree of:
- **scripts** → **activities** → **limits**
- each limit: `param_key`, `op`, `low`, `high`, `unit`, `eval_now`
- plus a separate `capacity` section for the phase-total Ah bands

**`eval_now` is the per-parameter on/off switch.** A limit with `eval_now = 0` is
stored and visible but **not graded**. This is how a parameter gets staged before
it goes live, and how VCH-EOL's "deselected params" are implemented.

## The comparison operators

From `bb_eol_eval._check()` — all comparisons carry an epsilon `_EPS` so a value
sitting exactly on a boundary passes rather than failing on float noise:

| op | meaning |
|---|---|
| `range` | `low - ε ≤ v ≤ high + ε` |
| `gte` / `gt` | at or above / above `low` |
| `lte` / `lt` | at or below / below `high` |
| `point` | `abs(v - low) ≤ ε` — exact match |
| `skip` / `raw` | **not evaluated** — returns `None` |

`None` is not a failure. It means "no opinion" — the parameter is recorded but
does not vote. Confusing `None` with `False` is a classic source of wrong verdicts.

## Rules

- **Never activate a version to make failures go away.** See rule 2 in
  [[Verdict Engine]]. If a batch fails, the limits are probably right.
- Cloning is free and safe. Editing the active version directly is not the flow —
  clone, edit, activate.
- A result's stored `version_id` is the audit trail. Don't drop it.
- Dyno does **not** use this system — it grades against hardcoded `envelope_*`
  tables. See [[Dyno]].

## Related
- [[Verdict Engine]] · [[BB-EOL]] · [[VCH-EOL]] · [[in_verdict Gate]]
