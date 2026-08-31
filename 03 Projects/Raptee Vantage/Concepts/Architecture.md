---
type: concept
project: Raptee Vantage
status: core
tags: [architecture]
---

# Architecture

Six backends. Each owns exactly one database. **Never cross the streams** —
a backend module reads/writes only its own DB.

| Suite | Backend module | Database | API prefix | Note |
|---|---|---|---|---|
| Dyno | `dyno_backend/` | `dyno_backend/raptee_dyno.db` | `/api/dyno/*` | [[Dyno]] |
| Road | `road_backend/` | `road_backend/raptee_rides.db` | `/api/road/*` | [[Road]] |
| BB-EOL (battery box) | `bb_eol_backend/` | `bb_eol_backend/bb_eol.db` | `/api/bb_eol/*` | [[BB-EOL]] |
| VCH-EOL (vehicle) | `eol_backend/` | `eol_backend/raptee_eol.db` | `/api/eol/*`, `/api/vch-eol/*` | [[VCH-EOL]] |
| Cross-compare | `cross_compare_backend/` | *(none — joins live)* | `/api/cross-compare` | [[Cross-Compare]] |
| Bike registry | `bike_backend/` | `bike_registry.json` | `/api/bike/*`, `/api/fleet` | [[Bike Registry]] |

## Root-level support DBs
| File | Owner | Purpose |
|---|---|---|
| `notifications.db` | `notification_log.py` | Every FAIL alert ever sent |
| `intake_log.db` | `intake_watcher.py` + API | Auto-ingest audit trail |
| `session_db.json` / `vch_users.json` | `auth_utils.py` | Sessions and users |

Config: `master_params.json` (parameter master list), `intake_config.json`
(watch folders + filename patterns).

`can_decoder_go/` — Go binary for decoding CAN logs, called out to, not imported.

## PM2 processes (`ecosystem.config.js`)
| Process | What |
|---|---|
| `Raptee-Backend` | FastAPI — `fastapi_server.py` |
| `Raptee-Frontend` | Next.js production server |
| `Raptee-Intake` | `intake_watcher.py` — auto-ingest daemon |

## Frontend
`vch-next-frontend/app/` routes: `admin` · `bb-eol` · `bike-report` ·
`cross-compare` · `dyno` · `fleet` · `fleet-eol` · `help` · `login` ·
`master` · `road`

`pages/` (Streamlit) is **legacy** — not the live UI, don't add features there.

See [[00 Home]] · [[Verdict Engine]] · [[Landmines]]
