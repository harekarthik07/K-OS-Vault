# Raptee Vantage — Project Brain

Production QC dashboard for Raptee electric motorcycles. Ingests dyno, road,
and EOL test data, evaluates every unit against golden limits, produces a
**PASS/FAIL verdict per bike**. This is a live production system — QC
verdicts here gate what ships.

## Map
- [[Architecture]] — suites, backends, DBs, ports
- [[Verdict Pipeline]] — the crown jewel, hard rules
- [[Landmines]] — things that bite people
- [[Conventions]] — how to touch this codebase safely

## Run it
| Task | Command |
|---|---|
| Dev | `launch_frontend.bat` |
| Prod deploy | `deploy.bat` → `pm2 reload ecosystem.config.js` |
| Backend only | `python -m uvicorn fastapi_server:app --port 8001 --host 0.0.0.0` |

Ports: backend `8001`, frontend `3000`.

**`vch-next-frontend/` (Next.js) is the live product.** `pages/` (Streamlit)
is legacy — don't add features there.
