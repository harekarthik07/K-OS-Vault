---
tags: [thermal-management, ev-academy]
aliases: []
status: budding
domain: Thermal Management
related: ["[[EV Energy Flow]]", "[[Cell Heat Generation]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Derating
## One-line idea
When a component gets too hot, its controller cuts power gradually to stay under the limit; the rider feels the bike get slower.
## Intuition first
A runner slows down before collapsing. The MC reads a sensor in the motor windings (NTC/PT1000) and lowers the torque limit as temperature rises.
## Governing relations
- Torque_limit = f(T_winding, T_MOSFET, T_cell) — typically a linear ramp from T_start to T_cutoff [°C]
- Heat in ≈ losses; T rises when heat in > heat removed
## Worked example
Illustrative: full torque below 120 °C winding, linear ramp to 0 at 150 °C → at 135 °C the bike delivers 50 % torque.
## Validity window & invalidation triggers
Thresholds are calibration values per bike and component; never assume them, so read the actual MC/BMS calibration.
## How we verify it
Motor/MC thermal model on a hard ride cycle → predict when T crosses T_start → compare with logged torque-limit flag.
## Gotchas
- [[Overheating means derating, not just damage]]
## Where used
- [[00 Home|EV Academy]] EV101, CAE2
## References
## Key identifiers
`derating` `torque limit` `NTC` `PT1000` `demagnetisation` `NdFeB`
