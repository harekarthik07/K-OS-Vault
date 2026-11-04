---
tags: [gotcha, ev-academy]
domain: Thermal Management
related: ["[[Cell Heat Generation]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Round late when squaring
**What I did:** rounded 13.89 A to 13.8 A before squaring → 1.52 kW instead of 1.54 kW.
**Why wrong:** squaring roughly doubles the relative rounding error, and it then gets multiplied by the cell count.
**Fix:** carry full precision until the final answer.
