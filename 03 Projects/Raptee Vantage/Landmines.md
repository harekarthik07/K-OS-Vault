# Landmines

**`fastapi_server.py` is 3,110 lines.** Every suite routes through it. A
locally-safe-looking change can break another suite. Read the relevant
section fully and plan before editing.

**Route naming is inconsistent.** VCH-EOL uses *both*:
- `/api/vch_eol/*` (underscore) → golden version management
- `/api/vch-eol/*` (hyphen) → QC analysis, summary, reports

Check which one you need. Don't "fix" one to match the other without
updating the frontend callers.

**Concurrent SQLite writers.** `intake_watcher.py` and FastAPI both write.
DBs run in WAL mode with `timeout=60`. Preserve both when opening
connections — dropping the timeout reintroduces `database is locked`.

**Restart cascades have happened in production.** `ecosystem.config.js`
carries `kill_timeout`, `restart_delay`, `max_restarts`, `min_uptime`
specifically to stop a 231-restart loop. Don't remove/shorten these.

**`dyno_tests.db` at repo root appears unreferenced.** Likely stale — verify
before assuming live, and before deleting.

**Admin-gated routes** use `dependencies=[Depends(require_admin_token)]`.
Anything destructive or limit-changing must carry this.

See [[Verdict Pipeline]] · [[Architecture]] · [[Home]]
