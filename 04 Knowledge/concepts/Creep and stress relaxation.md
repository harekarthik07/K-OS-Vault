---
type: concept
concept: Creep and stress relaxation
domain: Solid Mechanics
status: seedling
created: 2026-09-24
aliases: ["creep", "stress relaxation", "viscoelastic", "creep-fatigue"]
tags: [solid-mechanics, creep, stress-relaxation, viscoelastic, polymer, temperature]
---

# Creep and stress relaxation

## What they are
Two faces of the same time-dependent, temperature-activated behaviour:

- **Creep:** under a **constant load**, strain keeps growing with time. (Hold the stress → the part keeps deforming.)
- **Stress relaxation:** under a **constant strain**, stress decays with time. (Hold the deformation → the stress bleeds off.)

Both matter when a material is held at elevated temperature relative to its transition point — for metals above ≈ 0.3–0.4·T_melt, for **polymers near or above Tg** (and, to a degree, well below it, since polymers creep at modest temperatures).

## Why it matters for a thermal-fatigue study
A busbar holder is a **fixed-strain problem**: CTE mismatch imposes a geometric strain the plastic can't escape. That is exactly the **stress-relaxation** case — if the part sits hot under sustained CTE load, the peak stress it actually sees **relaxes below** what a purely elastic analysis predicts.

- This is often *favourable* (lower peak stress) — but it **cannot be assumed**; it changes the strain/stress the fatigue calc consumes.
- **Creep-fatigue interaction:** sustained hold at temperature (dwell) plus cycling is more damaging than either alone; relaxation during dwell resets the mean stress each cycle.

## The three creep stages (for reference)
1. **Primary** — decreasing rate (strain hardening dominates).
2. **Secondary** — steady minimum rate (the design-relevant regime).
3. **Tertiary** — accelerating to rupture (voids/necking).

## Modelling
- Needs a **viscoelastic** material model: creep compliance / relaxation modulus, usually fitted as a **Prony series**, plus temperature shift (WLF/Arrhenius).
- Decision rule for this project: only build viscoelastic data **once the transient peak temperature is known** and turns out near Tg or under sustained high-temperature load — do not pre-build it speculatively.

## Related
- [[Fatigue — cyclic damage and life]] · [[Temperature-dependent fatigue of polymers]] · [[Material properties required for a fatigue study]]
- [[Solid Mechanics]] · [[Thermal_Fatigue_Approach_and_TODO]]
