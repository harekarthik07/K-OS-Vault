---
tags: [battery-bms, ev-academy]
aliases: [ageing, degradation]
status: budding
domain: Battery & BMS
related: ["[[Cell Heat Generation]]", "[[Regen Limits]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# Battery Ageing and Temperature
## One-line idea
Temperature, not current, is what ages a cell; poor cooling raises temperature for the same heat generated.
## Intuition first
T = heat generated − heat removed. Same 3.86 W/cell, worse cooling → hotter cell → faster ageing.
## Governing relations
- Rule of thumb: degradation rate ≈ ×2 per +10 °C (Arrhenius-like)
- Feedback: ageing → R↑ → I²R↑ → T↑ → faster ageing
## Worked example
Two packs, same 2.8C duty. Pack A holds cells at 30 °C, pack B at 40 °C → B ages roughly twice as fast.
## Validity window & invalidation triggers
×2/10 °C is a rough heuristic; real rates depend on chemistry, SOC and C-rate (plating dominates when cold).
## How we verify it
The two numbers that matter from a pack thermal sim: **Tmax** and **ΔT** across the pack. The hottest cell ages first and the weakest cell limits the pack.
## Gotchas
## Where used
- [[00 Home|EV Academy]] EV102, CAE1
## References
- [Heat vs Cold: What Really Kills EV Batteries?](https://www.youtube.com/watch?v=ZppdYZrnkIA)
- [Pack Lab](https://claude.ai/artifact/CCymsnCYCgY6uha3hkTLXg) — lower cooling, watch ageing rate
## Key identifiers
`SEI` `calendar ageing` `cycle ageing` `Tmax` `ΔT` `SOH`
