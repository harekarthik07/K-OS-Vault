# Conventions

- **Never write to `.db` / `.db-wal` / `.db-shm` directly.** Go through the
  owning suite's DB manager (`*_db_manager.py`) or `db_bridge.py`.
- Adding a parameter touches multiple layers: eval logic, golden limits, DB
  schema, API route, Next.js display. Miss one → silent wrong verdict. Trace
  all five. (`/add-param` skill does this systematically.)
- FAIL alerts → Teams via `teams_notify.py`, configured centrally in the home
  Admin Zone, not per-suite. Every send logged in `notifications.db`.
- `# ====` banner comments separate route groups in `fastapi_server.py` —
  keep new routes inside the right banner.

## Working agreements
- Plan before touching `fastapi_server.py` or any verdict logic.
- Verify by running the real app against actual bike data, not just reading
  the diff.
- Ask rather than assume when a verdict looks wrong — the data is often
  correct and the expectation is what's off.

See [[Home]] · [[Verdict Pipeline]] · [[Landmines]] · [[Architecture]]
