---
tags: [gotcha, ev-academy]
domain: Battery & BMS
related: ["[[C-rate]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# C-rate is a ratio, not amps
**What I did:** wrote "13.9/5 = 2.78 A".
**Why wrong:** current ÷ capacity cancels the amps; the result is in "C" (2.78C).
**Fix:** keep units on every line of a calculation.
