---
tags: [battery-bms, ev-academy]
aliases: [cell basics, pack configuration, S/P]
status: budding
domain: Battery & BMS
related: ["[[C-rate]]", "[[I2R Losses and Pack Voltage]]", "[[Cell Heat Generation]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Cell and Pack Fundamentals
## One-line idea
Series adds voltage, parallel adds capacity; pack energy depends only on total cell count.
## Intuition first
Series = stacking batteries end-to-end (more push). Parallel = side-by-side (more fuel).

| Property | Meaning | Example |
|---|---|---|
| Chemistry | NMC: energy-dense, heat-sensitive · LFP: safer, longer life, heavier | 2W mostly NMC |
| Form factor | Cylindrical (18650, 21700), pouch, prismatic | 21700 |
| Nominal voltage | Average discharge voltage | ~3.6 V NMC |
| Capacity | Charge held | 5 Ah |
| Energy | V × Ah | 18 Wh |
| Internal resistance | Main heat source | 15–25 mΩ |
## Governing relations
- V_pack = N_s · V_cell · Q_pack = N_p · Q_cell · E_pack = V_pack · Q_pack [Wh]
## Worked example
100S4P with 3.6 V, 5 Ah cells → 360 V · 20 Ah · 7.2 kWh · 400 cells.
## Validity window & invalidation triggers
Nominal values only. Voltage swings ~3.0–4.2 V/cell with SOC; capacity fades with age.
## How we verify it
Pack geometry and S/P layout define the cell array in the thermal model.
## Gotchas
## Where used
- [[00 Home|EV Academy]] EV102
## References
- Andrea, *Battery Management Systems for Large Lithium-Ion Battery Packs*
## Key identifiers
`NMC` `LFP` `21700` `nS mP` `nominal voltage` `Wh`
