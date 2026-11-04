---
tags: [battery-bms, ev-academy]
aliases: [I²R, pack voltage]
status: budding
domain: Battery & BMS
related: ["[[Cell and Pack Fundamentals]]", "[[Cell Heat Generation]]", "[[C-rate]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# I2R Losses and Pack Voltage
## One-line idea
Higher pack voltage cuts pack current and therefore I²R losses in cables, busbars, connectors, the MC and motor, but cell current and cell heat stay the same, because each cell delivers the same share of power at the same cell voltage.
## Intuition first
Wiring the cells differently only changes how currents and voltages combine at pack level. Each cell does the same work either way.
## Governing relations
- P = V·I → I_pack = P / V_pack [A]
- Loss = I²·R [W] → halve I, ¼ the loss
- I_cell = (P / N_cells) / V_cell [A]
## Worked example
Same 400 cells (3.6 V, 5 Ah, 20 mΩ), 20 kW:

| | 100S4P (360 V) | 50S8P (180 V) |
|---|---|---|
| Pack current | 55.6 A | 111.1 A |
| Cell current | 13.9 A | 13.9 A |
| Heat per cell | 3.86 W | 3.86 W |
| 10 mΩ cable loss | 31 W | 123 W |
## Validity window & invalidation triggers
Assumes identical cells and equal current sharing in parallel strings; poor busbar design or cell-to-cell IR spread breaks it.
## How we verify it
Pack thermal model: cell heat source set by I_cell; busbar/cable Joule heating set by I_pack. Validate with busbar thermocouples.
## Gotchas
- [[Pack voltage changes pack current, not cell current]]
## Where used
- [[00 Home|EV Academy]] EV102
## References
- [Pack Lab](https://claude.ai/artifact/W84v9ovW2BYMRPDE5mq9jT#pack-lab) — toggle 100S4P vs 50S8P
## Key identifiers
`I²R` `Joule heating` `HV architecture` `busbar` `series` `parallel`
