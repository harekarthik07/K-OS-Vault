---
tags: [power-electronics, ev-academy]
aliases: []
status: budding
domain: Power Electronics
related: ["[[Derating]]", "[[Regen Limits]]", "[[I2R Losses and Pack Voltage]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# EV Energy Flow
## One-line idea
Battery stores, BMS protects, motor controller turns DC into 3-phase AC and sets torque, motor makes rotation, VCU decides how much torque to ask for.
## Intuition first
```
Battery ─► BMS ─► Motor Controller ─► Motor ─► Chain/belt ─► Rear wheel
             ▲            ▲
             └──── VCU ───┘   (throttle, brake, mode, faults)
```
Every arrow carries power, and every arrow loses some of it as heat.
## Governing relations
- P = V·I [W]; η_system = η_cables · η_MC · η_motor · η_drive
## Worked example
20 kW at the pack, η_MC ≈ 0.97, η_motor ≈ 0.92 (illustrative) → ≈ 17.8 kW at the shaft, ≈ 2.2 kW lost as heat in MC + motor.
## Validity window & invalidation triggers
Holds for any battery-electric 2W/4W. Efficiencies vary strongly with speed and torque, so check the efficiency map, not one number.
## How we verify it
Every block is a heat source in a thermal model. Validate with logged pack current, phase current and component temperatures.
## Gotchas
- [[Overheating means derating, not just damage]]
## Where used
- [[00 Home|EV Academy]] EV101
## References
- Larminie & Lowry, *Electric Vehicle Technology Explained*
## Key identifiers
`VCU` `BMS` `MC` `MCU` `inverter` `PMSM` `HV bus`
