---
tags: [battery-bms, ev-academy]
aliases: [C rate]
status: budding
domain: Battery & BMS
related: ["[[Cell and Pack Fundamentals]]", "[[Cell Heat Generation]]"]
sources: ["[[2026-11-04 Session 001]]"]
origin_project: EV Academy
created: 2026-11-04
---
# C-rate
## One-line idea
C-rate = current ÷ capacity: a size-independent measure of how hard a cell is working.
## Intuition first
13.9 A is brutal for a 2 Ah cell (7C) and easy for a 50 Ah cell (0.28C). Amps alone don't tell you stress; C-rate does.
## Governing relations
- C = I / Q [1/h, written "C"] · discharge time ≈ 1 / C [h]
- Use cell I with cell Q, or pack I with pack Q, never mixed; both give the same C.
## Worked example
100S4P, 20 kW: I_cell = 13.9 A, Q_cell = 5 Ah → 2.8C → ≈ 60/2.8 ≈ 21 min to empty. Pack check: 55.6 A / 20 Ah = 2.8C.
## Validity window & invalidation triggers
"Time = 1/C" is ideal; real capacity drops at high C and low temperature (Peukert-like effects).
## How we verify it
Cell datasheet C-rate limits vs predicted C-rate on the drive cycle; hot-spot cells see the highest effective C.
## Gotchas
- [[C-rate is a ratio, not amps]]
## Where used
- [[00 Home|EV Academy]] EV102
## References
- [Everything you'll want to know about C-Rating](https://www.youtube.com/watch?v=A5xRElEazSs)
- [Pack Lab](https://claude.ai/artifact/CCymsnCYCgY6uha3hkTLXg)
## Key identifiers
`C-rate` `Ah` `capacity` `discharge rate`
