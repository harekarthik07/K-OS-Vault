---
type: daily_log
project: Raptee Vantage
---

# Daily Log — Raptee Vantage

Append newest at top. One `##` per day.
End of day: run `/eod` — triages into `Concepts/` (durable truth), `Experiments/`
(one investigation) or `Results/` (what shipped).

---

## 2026-09-03
**Did:**
- Built the **Heat-Transfer module** (`/heat-transfer`) — CHT configurator, 1D/ETM sim, fan PQ debugger, case persistence. New `heat_transfer_backend/` + `/api/heat-transfer/*`. Full record: [[Heat-Transfer Module — Build & Decisions]].
- Ported the Simulink [[MC_HS_ETM_I1]] electro-thermal chain: SVPWM losses → 2-node Cauer → junction temp vs measured, deration at 95 °C. See [[ETM ported into Vantage]].
- Backend self-checks pass; endpoints verified on a throwaway `:8009` instance.

**Decided:**
- **Hybrid, one formula per layer** — cheap steady algebra client-side (instant), heavy/stateful math (transient ODE, persistence) server-side; nothing duplicated.
- **No assumed values** — engine hardcodes formulae only; every magnitude is a user input; reference-sheet values load only on explicit click.
- Module is standalone — does **not** touch the bike PASS/FAIL [[Verdict Engine]].

**Learned:**
- Dyno DB stores **no motor-current channels** — the ETM is driven by an uploaded per-bike xlsx (`Time, ID, IQ, IGBT_Temp, BMS_cumulative_totv`), not a DB pull.
- The reference sheets carry live disputes (Rjc per-die vs per-module = 6× on Tj; C_plate 490 vs 500) — surfaced as UI choices, not resolved silently.

**Next:**
- Interactive Network Map tab + re-skin `/heat-transfer` to the suite theme (sidebar/header/accent).
- Reload `:8001` to expose the routes; reconcile main-copy vs the `heat-transfer-viz-module` worktree.

**Concepts touched:** [[Heat-Transfer Module — Build & Decisions]] [[ETM ported into Vantage]]

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
