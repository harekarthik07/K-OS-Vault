---
type: project_home
project: Raptee Vantage
status: active
started: 2026-08-26
domain_primary: Software / QC Systems
domain_secondary: [Manufacturing Test, Data Engineering]
---

# Raptee Vantage

> Production QC dashboard for Raptee electric motorcycles — ingests dyno, road and EOL test data, grades every unit against golden limits, and produces a PASS/FAIL verdict per bike. **Live system: these verdicts gate what ships.**

## Sections
- [[Daily Log]] — what we did / learned / next, one `##` per day
- [[Questions]] — open + answered
- [[Workflow]] — how Claude + this vault work together (read this first)
- Concepts/ — durable truth: architecture, verdict engine, per-suite logic
- Experiments/ — one note per investigation ("why did BIKE-07 fail?")
- Results/ — deploys, fixes shipped, outcomes
- Resources/ — links, docs, references

## Core concepts
- [[Architecture]] — six suites, six DBs, ports, PM2
- [[Verdict Engine]] — **the crown jewel**, how PASS/FAIL is actually computed
- [[Golden Versions]] — versioned limits, how activation works
- [[in_verdict Gate]] — which units count toward the headline numbers
- [[Landmines]] — things that bite people
- [[Conventions]] — how to touch this codebase safely

## Suites
| Suite | Note | DB | API |
|---|---|---|---|
| Dyno | [[Dyno]] | `raptee_dyno.db` | `/api/dyno/*` |
| Road | [[Road]] | `raptee_rides.db` | `/api/road/*` |
| BB-EOL | [[BB-EOL]] | `bb_eol.db` | `/api/bb_eol/*` |
| VCH-EOL | [[VCH-EOL]] | `raptee_eol.db` | `/api/eol/*`, `/api/vch-eol/*` |
| Cross-Compare | [[Cross-Compare]] | *(none — live join)* | `/api/cross-compare` |
| Bike Registry | [[Bike Registry]] | `bike_registry.json` | `/api/bike/*`, `/api/fleet` |

## Run it
| Task | Command |
|---|---|
| Dev | `launch_frontend.bat` |
| Prod deploy | `deploy.bat` → `pm2 reload ecosystem.config.js` |
| Backend only | `python -m uvicorn fastapi_server:app --port 8001 --host 0.0.0.0` |

Ports: backend `8001`, frontend `3000`.
**`vch-next-frontend/` (Next.js) is the live product.** `pages/` (Streamlit) is legacy.

## Open Questions
```dataview
LIST FROM "03 Projects/Raptee Vantage"
WHERE type = "questions"
```

## Atlas Connections
- [[Software Systems]]
- [[Manufacturing Test]]
