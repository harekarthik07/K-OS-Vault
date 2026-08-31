---
type: suite
project: Raptee Vantage
suite: Cross-Compare
backend: cross_compare_backend/
db: none (live in-memory join)
api_prefix: /api/cross-compare
frontend: vch-next-frontend/app/cross-compare/
status: stub
---

# Cross-Compare

> Joins Dyno × BB-EOL data per bike. **Owns no database** — the join happens live, in memory, via [[Bike Registry]].

The DBs stay separate on purpose ("never cross the streams" — [[Architecture]]).
Cross-compare is the one place data from two suites meets, and it does so at
request time rather than by writing a joined table.

## Exclusion propagates here ⚠️

Excluded units are dropped from cross-compare too:
- BB-EOL: rows skipped where `is_counted(session)` is false
- VCH-EOL: `get_vd_reports(counted_only=True)`

So a pack that vanished from cross-compare may simply be excluded, not missing.
See [[in_verdict Gate]].

## To fill in
- [ ] Exact join keys and fallback behaviour
- [ ] Which parameters are compared and how they're paired
- [ ] What the `/cross-compare` page renders
- [ ] Performance characteristics of the live join at fleet scale

## Related
[[Architecture]] · [[Dyno]] · [[BB-EOL]] · [[Bike Registry]] · [[in_verdict Gate]]
