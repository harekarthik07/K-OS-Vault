---
tags: [gotcha, ev-academy]
domain: Battery & BMS
related: ["[[I2R Losses and Pack Voltage]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Pack voltage changes pack current, not cell current
**What I did:** said max pack current is unchanged between 100S4P and 50S8P; then said cell heat is equal "because of capacity".
**Why wrong:** pack current doubles at half the voltage (55.6 → 111.1 A). Cell heat is equal because power per cell (50 W) and cell voltage (3.6 V) are equal.
**Fix:** pack voltage → conductor losses. Power per cell → cell heat.
