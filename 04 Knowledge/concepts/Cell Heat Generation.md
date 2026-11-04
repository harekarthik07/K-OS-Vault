---
tags: [thermal-management, ev-academy]
aliases: [Bernardi, battery heat]
status: budding
domain: Thermal Management
related: ["[[Battery Ageing and Temperature]]", "[[I2R Losses and Pack Voltage]]", "[[Derating]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Cell Heat Generation
## One-line idea
Cell heat = irreversible Joule heat (I²R, dominant at high current) + reversible entropic heat; together the Bernardi equation behind Ansys battery models.
## Intuition first
Internal resistance turns current into heat like a resistor; the chemistry adds or absorbs a smaller amount depending on direction.
## Governing relations
- Q = I²R + I·T·(dU/dT) [W] (Bernardi, simplified)
- Comfort window 15–35 °C; > 45 °C ageing accelerates; < 0 °C charging risky
## Worked example
100S4P, 20 mΩ cells, 20 kW peak: I_pack = 20000/360 = 55.6 A → I_cell = 13.9 A → Q_cell = 13.9² × 0.020 = **3.86 W** → pack ≈ **1.54 kW** during hard acceleration.
## Validity window & invalidation triggers
R depends on temperature, SOC and age; a single R value only holds near the test condition. Entropic term matters at low C-rate.
## How we verify it
Q_cell is the volumetric heat source in the pack model. Fluent MSMD sub-models: NTGK, ECM, Newman P2D. Correlate with cell-tab thermocouples on a pulse test.
## Gotchas
- [[Round late when squaring]]
## Where used
- [[00 Home|EV Academy]] EV102, CAE1
## References
- [Battery Thermal Modeling](https://www.youtube.com/watch?v=HWaZU8lm7_o)
- [Pack Lab](https://claude.ai/artifact/W84v9ovW2BYMRPDE5mq9jT#pack-lab)
- Ansys Fluent Battery Module User Guide
## Key identifiers
`Bernardi` `Joule heat` `entropic heat` `MSMD` `NTGK` `ECM` `P2D`
