---
type: daily_log
project: Raptee Vantage
---

# Daily Log — Raptee Vantage

Append newest at top. One `##` per day.
End of day: run `/eod` — triages into `Concepts/` (durable truth), `Experiments/`
(one investigation) or `Results/` (what shipped).

---

## 2026-08-31
**Did:**
- Restructured the vault to match the standard Project template (Concepts / Experiments / Results / Resources), mirroring `03 Projects/ETM For Heatsink and IGBT`
- Wrote the verdict engine deep-dive from the actual code, not from CLAUDE.md
- Split the six suites into `Concepts/Suites/` — Dyno, BB-EOL, VCH-EOL filled; Road, Cross-Compare, Bike Registry stubbed
- Defined the [[Workflow]] — four buckets, and which command drives each
- Built two skills: **`/note`** (capture one thing mid-work) and **`/eod`** (end-of-day triage). Ran `/eod` for the first time on this session.

**Learned:**
- Dyno verdict is *not* golden-version based like BB-EOL and VCH-EOL — it uses hardcoded envelope tables + a ±10% band around the golden-bike power mean. Different mechanism, same output shape. The band is **data-dependent** — it moves as golden runs are added. See [[Dyno]].
- `/api/bike-verdict-all` caches the whole grid for 30 s. A verdict that "didn't update" is usually this, not a logic bug — use `/api/bike-verdict/{n}`, which is uncached.
- BB-EOL step verdicts have four states, not two: PASS / FAIL / FLAG / SKIP. Only FAIL drives the pack verdict; FLAG means "activity missing from golden", a data gap rather than a defect. See [[BB-EOL]].
- The roll-up checks `has_fail` **before** `complete` — one FAIL plus two missing stations is FAIL, not INCOMPLETE. Deliberate: a known defect doesn't hide behind missing data.
- Tooling: `claude mcp list` reporting "✔ Connected" does **not** mean the running session can use the tools. Recorded in `Resources/README.md`.

**Next:**
- Fill [[Road]] and [[Cross-Compare]] when we next touch those suites
- Answer [[Questions]] Q1 (is `dyno_tests.db` dead?) before anyone deletes it

**Concepts touched:** [[Verdict Engine]] [[Golden Versions]] [[in_verdict Gate]] [[Dyno]] [[BB-EOL]] [[VCH-EOL]]
