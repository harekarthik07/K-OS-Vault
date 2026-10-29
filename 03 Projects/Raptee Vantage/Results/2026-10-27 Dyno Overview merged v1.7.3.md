---
type: result
project: Raptee Vantage
date: 2026-10-27
---

# 2026-10-27 Dyno Overview merged v1.7.3

## What we built / measured
Four releases in one day, frontend only (`npm run release` → `pm2 restart Raptee-Frontend`). No backend or limit change.

| Version | Commit | What shipped |
|---|---|---|
| v1.7.0 | `26ae0d7` | New Dyno **Trend QC Lab** tab: 10-bike series, bars, heatmap, trend, series compare |
| v1.7.1 | `9f3676f` | Cut to 3 tools (Batch Scorecard, Limit Watch, Batch vs Batch); "series" renamed "batch"; only the 5 PASS/FAIL checks |
| v1.7.2 | `b3b8d5f` | Charts back (pass/fail bars, heatmap, A-vs-B bars) |
| v1.7.3 | `ba1f263` | "How to read this" panels; **Trend QC Lab merged into Overview**; tab removed |

The Overview's per-test verdict code moved unchanged into `app/dyno/verdict.js` so every block uses one copy. Design pages: plan (three tools) and merge proposal, both private artifacts on claude.ai.

## Numbers
**Verdict rule: unchanged.** No bike changed PASS/FAIL. What changed is **how the headline counts**:

| | Before (Overview, ≤ v1.7.2) | After (v1.7.3) |
|---|---|---|
| Counts | every run | every bike, latest test |
| Golden bikes | counted as PASS | left out |
| Retests | counted each time | latest only |
| **Pass rate** | **34.4%** (42 / 122 valid runs) | **32%** (33 / 102 bikes) |
| Wrong procedure | 2 runs | 2 bikes |

Fails per check, runs → bikes: High Cell 52 → 44 · AFE 39 → 31 · Motor 19 → 18 · Power 10 → 8 · IGBT 0 → 0.

Start-limit check on real data: at 34 °C, 29 runs become wrong procedure and the status reads 33/77.

Removed from the Overview as duplicates: 6 stat cards, verdict donut, Element Performance, ΔT Failure Occurrence, Failure Evolution History (now the Trend block's "by test date" view).

**Not verified:** nobody has looked at the merged Overview logged in on :3000. Checks were a real-data server render, a production build, and :3000 health 200.

## Charts / images
- See [[2026-10-27 Dyno batch trend analysis]] for the batch numbers.

## Ties back to
- Experiment: [[2026-10-27 Dyno batch trend analysis]]
- Concept: [[Dyno]] (Overview page section)
- Open: [[Questions]] Q6–Q8
