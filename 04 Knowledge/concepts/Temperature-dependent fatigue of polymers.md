---
type: concept
concept: Temperature-dependent fatigue
domain: Solid Mechanics
status: seedling
created: 2026-09-24
aliases: ["temperature-dependent fatigue", "polymer fatigue", "fatigue at temperature", "hysteretic heating"]
tags: [solid-mechanics, fatigue, polymer, temperature, Tg, abs-pc]
---

# Temperature-dependent fatigue of polymers

## What it is
Fatigue resistance is **not a fixed material property — it falls as temperature rises.** A room-temperature S-N curve over-predicts life at operating temperature. For polymers the effect is large and starts well below any obvious limit, because stiffness and strength themselves drop with temperature.

## Why polymers are especially temperature-sensitive
- **Modulus and strength decline continuously with T**, then drop sharply approaching the **glass transition `Tg`** (≈ 110–125 °C for typical ABS+PC blends). Above Tg the material is rubbery and the whole elastic analysis is invalid.
- **Rate / frequency dependence:** polymers are viscoelastic, so faster cycling behaves stiffer, slower cycling softer — S-N data must match the loading rate.
- **Hysteretic self-heating:** each cycle dissipates energy inside the polymer; at higher frequencies this **raises the part's own temperature**, which lowers strength, which increases dissipation — a runaway that metals don't show.
- **No endurance limit:** the curve keeps sloping — there is no safe stress, only a life.

## Practical consequences
- Use **S-N / Δε–N data at the relevant operating temperature**, not the datasheet room-temperature curve.
- Establish the **actual peak temperature** first (needs the transient duty cycle), then compare to Tg:
  - **well below Tg** → linear-elastic with constant properties is defensible;
  - **near/above Tg** → temperature-dependent E, CTE and a viscoelastic/creep model are required — see [[Creep and stress relaxation]].
- In this project the steady-state range is **30.5–52.5 °C** (well below Tg), so a first-pass linear check is acceptable — but this must be re-checked once the transient peak is known.

## Related
- [[Fatigue — cyclic damage and life]] · [[Creep and stress relaxation]] · [[Material properties required for a fatigue study]]
- [[Solid Mechanics]] · [[Thermal_Fatigue_Approach_and_TODO]]
