---
type: concept
project: Raptee Vantage
status: core
tags: [gotchas]
---

# Landmines

> Things that bite people. Add to this the moment you get bitten.

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
before assuming live, and before deleting. ([[Questions]] Q1)

**Admin-gated routes** use `dependencies=[Depends(require_admin_token)]`.
Anything destructive or limit-changing must carry this.

---

## Verdict-specific landmines

**The 30-second cache.** `/api/bike-verdict-all` caches the whole grid for 30 s.
A verdict that "didn't update" is usually this, not a logic bug. Use the
single-bike endpoint `/api/bike-verdict/{n}` — it's uncached and honest.

**`failures[]` is truncated to 3** in the API response. The DB holds all of them.
Don't conclude a bike had exactly 3 failures from the API.

**`None` is not `False`.** In `bb_eol_eval._check()`, `None` means "not evaluated"
and does **not** fail the step. Treating it as a failure is a classic wrong-verdict bug.

**FAIL beats INCOMPLETE.** The roll-up checks `has_fail` *before* `complete`. A bike
with one FAIL and two missing stations is FAIL. Deliberate — see [[Verdict Engine]].

**`in_verdict` exclusion is a substring match** on the barcode. A legitimate barcode
containing "test" anywhere gets silently excluded. If a real pack vanishes from the
numbers, check this first. See [[in_verdict Gate]].

**Dyno golden bikes auto-pass.** If a test name contains a `GOLDEN_BIKES` token, the
dyno verdict returns PASS without running any check. Correct by design, surprising in
debugging. See [[Dyno]].

**Bike-number matching differs per suite.** Regex on filename (Dyno), registry lookup
(BB-EOL), zero-pad-or-not (VCH-EOL). A phantom INCOMPLETE is usually an identifier
mismatch, not a grading bug.

See [[Verdict Engine]] · [[Architecture]] · [[00 Home]]
