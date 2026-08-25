# Verdict Pipeline — the crown jewel

Assembled in `fastapi_server.py` from three per-suite helpers, rolled up:

```
_dyno_verdict_for_bike(bike_no)     ─┐
_bb_eol_verdict_for_bike(bike_no)   ─┼─→  /api/bike-verdict/{bike_no}
_vch_eol_verdict_for_bike(bike_no)  ─┘    /api/bike-verdict-all
```

Each suite compares measured values against an **active golden version**.
Golden limits are versioned, cloneable, activated one at a time — see
`/api/bb_eol/golden/*` and `/api/vch_eol/golden/*`.

## Hard rules — do not violate

1. **Any FAIL → overall FAIL.** No averaging, no "mostly passed", no best-of-N.
2. **Never loosen limits or bands to make something pass.** An all-FAIL batch
   can be legitimate. Test datasets deliberately mix good and bad units. If
   results look wrong, the bug is in the logic or data — fix the cause, never
   the threshold.
3. **`in_verdict` is the gate.** BB-EOL packs carry an `in_verdict` flag
   (auto/manual/bulk) controlling whether they count toward overall verdict.
   Respect it everywhere a rollup happens.
4. **VCH-EOL exclusions:** deselected parameters + the three acceleration
   parameters are left out of the verdict by design. Intentional.
5. **Test/dummy files are blocked at intake**, not filtered later. If junk
   reaches the DB, fix the intake filter.

See [[Architecture]] · [[Landmines]] · [[Home]]
