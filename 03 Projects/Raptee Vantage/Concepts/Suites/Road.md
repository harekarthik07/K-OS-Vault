---
type: suite
project: Raptee Vantage
suite: Road
backend: road_backend/
db: road_backend/raptee_rides.db
api_prefix: /api/road/*
frontend: vch-next-frontend/app/road/
status: stub
---

# Road

> Road ride data ingest and analysis. **Stub — fill in when we next touch this suite.**

Does **not** contribute to the bike verdict roll-up. `/api/bike-verdict/{n}` uses
Dyno + BB-EOL + VCH-EOL only. Road is analysis/telemetry, not a QC gate.

## To fill in
- [ ] What the ride files look like and how they're parsed
- [ ] Role of `can_decoder_go/` in decoding CAN logs
- [ ] Schema of `raptee_rides.db`
- [ ] What the `/road` page actually shows
- [ ] Whether road data should ever feed a verdict

## Related
[[Architecture]] · [[Verdict Engine]] · [[00 Home]]
