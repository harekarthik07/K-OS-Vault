# Architecture

Six backends. Each owns exactly one database. **Never cross the streams** —
a backend module reads/writes only its own DB.

| Suite | Backend module | Database | API prefix |
|---|---|---|---|
| Dyno | `dyno_backend/` | `dyno_backend/raptee_dyno.db` | `/api/dyno/*` |
| Road | `road_backend/` | `road_backend/raptee_rides.db` | `/api/road/*` |
| BB-EOL (battery box) | `bb_eol_backend/` | `bb_eol_backend/bb_eol.db` | `/api/bb_eol/*` |
| VCH-EOL (vehicle) | `eol_backend/` | `eol_backend/raptee_eol.db` | `/api/eol/*`, `/api/vch-eol/*` |
| Cross-compare | `cross_compare_backend/` | *(none — joins live)* | `/api/cross-compare` |
| Bike registry | `bike_backend/` | `bike_registry.json` | `/api/bike/*`, `/api/fleet` |

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

See [[Home]] · [[Verdict Pipeline]] · [[Landmines]]
