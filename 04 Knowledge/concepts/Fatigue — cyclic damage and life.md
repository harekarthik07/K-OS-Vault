---
type: concept
concept: Fatigue
domain: Solid Mechanics
status: seedling
created: 2026-09-24
aliases: ["fatigue", "fatigue life", "S-N curve", "strain-life", "high-cycle fatigue", "low-cycle fatigue"]
tags: [solid-mechanics, fatigue, S-N, strain-life, thermal-fatigue]
---

# Fatigue — cyclic damage and life

## What it is
**Fatigue is progressive, localised damage from *repeated* loading — failure at stresses well below the material's static strength.** A part that survives a single peak load can still crack after enough cycles at a fraction of that load. Damage accumulates in two stages: **crack initiation** (at a stress concentrator — a notch, rib, corner, or interface) then **crack propagation** until the remaining section fails.

The key point: a static stress check (von Mises < yield) can pass while the part is fatiguing to death. Fatigue is about the **range** and **number** of cycles, not the single worst instant.

## The two regimes
| Regime | Driven by | Described by | Typical life |
|---|---|---|---|
| **High-cycle (HCF)** | elastic stress amplitude | **S-N curve** (stress vs cycles) | > ~10⁴ cycles |
| **Low-cycle (LCF)** | plastic strain amplitude | **ε-N curve** (strain-life, Coffin-Manson for metals) | < ~10⁴ cycles |

**Thermal fatigue** (this project) is usually strain-controlled: a ΔT drives a fixed geometric strain via CTE mismatch each cycle, so the **strain range Δε** is the natural variable — see [[Material properties required for a fatigue study]].

## Concepts that matter
- **Stress/strain range** `Δσ`, `Δε` and **mean stress**: a tensile mean stress shortens life (Goodman/Gerber/SWT corrections).
- **Endurance limit:** *steels* show a stress below which life is ~infinite. **Polymers and aluminium do NOT** — their S-N curve keeps sloping down, so there is no "safe" stress, only a life at a given load. Critical for the ABS+PC G-Bridge.
- **Cumulative damage (Miner's rule):** `Σ nᵢ/Nᵢ = 1` at failure — how a spectrum of different cycles adds up.
- **Stress concentration** sets *where* it starts — thin webs, ribs, and dissimilar-material interfaces, not the bulk. Extract Δε there, not as an average.

## In this project
CTE mismatch between aluminium busbars and the ABS+PC housing cyclically strains the plastic every power cycle → strain-controlled thermal fatigue of a polymer. The metal-calibrated Coffin-Manson tool does **not** apply — see [[Temperature-dependent fatigue of polymers]] and [[Contact model must match how the part is made]].

## Related
- [[Temperature-dependent fatigue of polymers]] · [[Creep and stress relaxation]] · [[Material properties required for a fatigue study]]
- [[Solid Mechanics]] · [[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]]
