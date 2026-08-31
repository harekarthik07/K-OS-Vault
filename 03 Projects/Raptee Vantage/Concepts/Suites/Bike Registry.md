---
type: suite
project: Raptee Vantage
suite: Bike Registry
backend: bike_backend/
db: bike_registry.json
api_prefix: /api/bike/*, /api/fleet
frontend: vch-next-frontend/app/fleet/
status: stub
---

# Bike Registry

> The identity layer. Maps barcodes / VINs / test names to bike numbers. Stored as **JSON, not SQLite**.

Small but load-bearing: it's how [[BB-EOL]] turns a battery barcode into a bike
number (`_lookup_bike_no`), and therefore how pack results attach to a bike at all.

**If the registry is wrong, verdicts silently go missing** — the data exists, it
just doesn't attach to any bike, and the bike shows INCOMPLETE. When debugging a
phantom INCOMPLETE, check the registry before the grading logic.

Also provides bike **tier** (`_lookup_bike_no_with_tier`).

## To fill in
- [ ] `bike_registry.json` schema
- [ ] How entries are created — manual, on intake, or both?
- [ ] What "tier" means and where it's used
- [ ] What `/api/fleet` returns
- [ ] Behaviour when a barcode is unregistered

## Related
[[Architecture]] · [[BB-EOL]] · [[Cross-Compare]] · [[Verdict Engine]]
