---
tags: [battery-bms, ev-academy]
aliases: [regen]
status: budding
domain: Battery & BMS
related: ["[[EV Energy Flow]]", "[[Battery Ageing and Temperature]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Regen Limits
## One-line idea
Regen is capped by how much charge current the battery can safely accept; a full or cold battery accepts little, so the brakes do more.
## Intuition first
A full water tank overflows if you keep pushing water in.
## Governing relations
- Regen torque ≤ f(BMS charge current limit, MC limit)
- Chain: BMS lowers allowed charge current → VCU reduces regen torque → mechanical brakes blend in
## Worked example
Near 100 % SOC an NMC cell sits near 4.2 V; any charge current pushes it over the limit → BMS allows ≈ 0 A → regen ≈ 0.
## Validity window & invalidation triggers
High SOC and low temperature both cut the limit. Exact values come from the cell datasheet and BMS calibration.
## How we verify it
Log SOC, cell temperature, BMS charge limit and regen torque on a downhill descent; check regen torque tracks the BMS limit.
## Gotchas
## Where used
- [[00 Home|EV Academy]] EV101, EV201
## References
## Key identifiers
`regen` `charge current limit` `lithium plating` `SOC` `brake blending`
