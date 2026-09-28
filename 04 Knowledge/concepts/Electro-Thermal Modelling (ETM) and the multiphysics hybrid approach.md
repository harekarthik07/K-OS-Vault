---
type: concept
concept: Electro-Thermal Modelling (ETM)
domain: Power Electronics
status: seedling
created: 2026-09-24
aliases: ["ETM", "electro-thermal model", "electro-thermal multiphysics", "multiphysics hybrid", "co-simulation coupling"]
tags: [power-electronics, thermal, multiphysics, coupling, etm, cae]
---

# Electro-Thermal Modelling (ETM) and the multiphysics hybrid approach

## What ETM is
**ETM = Electro-Thermal Model(ling): coupling where electrical loss generates heat, and the resulting temperature feeds back into the electrical behaviour.** In power electronics the loop is:

```
current + switching  →  device losses (conduction + switching / I²R + AC)  →  temperature rise
        ↑                                                                          │
        └──────────  loss depends on T (Vce(T), Rds(T), resistivity(T))  ◀────────┘
```

Losses raise junction/component temperature; temperature changes the loss (hotter silicon/copper is more resistive), so the two are genuinely **coupled**, not sequential. The classic ETM deliverable is a junction-temperature prediction under a real duty — e.g. the IGBT work in [[IGBT Electro-Thermal Loss Modelling]] and the [[ETM For Heatsink and IGBT/00 Home|heatsink ETM project]].

## Why "hybrid" — two senses in this vault

### 1. Reduced-order + high-fidelity (the IGBT/heatsink ETM)
A fast **1D lumped model** (Cauer RC network) is **calibrated/validated against high-fidelity CFD and dyno data**. The 1D model screens the design space in seconds; CFD supplies the one thing 1D can't compute (the convective `h` map) and confirms specific candidates. "Hybrid" = cheap model where it's enough, expensive model where it's needed.
See [[Cauer Model Calibration — fit what you cannot derive]] and [[Only the h·A product matters for convective resistance]].

### 2. Chained multiphysics solvers (the busbar / G-Bridge study)
Different physics, each solved in the tool best suited to it, output of one becoming the load of the next — a **one-way (sequential) coupled chain**:

```
Maxwell 3D (AC+DC conduction)  →  Joule / ohmic loss field
        ▼
Icepak (conjugate heat transfer)  →  temperature field
        ▼
Mechanical (Static Structural)  →  CTE-mismatch stress / strain
        ▼
Fatigue post-processing  →  cyclic strain range → life
```
See [[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]].

## One-way vs two-way coupling — the key modelling choice
- **One-way (sequential):** upstream → downstream only. Valid when the downstream result **doesn't materially change** the upstream physics (structural deformation barely changes the EM loss or thermal field). Cheap, and what the busbar chain uses.
- **Two-way (co-simulation):** solvers iterate until mutually consistent. Needed when feedback is strong — the main one in ETM is **loss depending on temperature**; if that matters, iterate the Maxwell↔Icepak step, or bake a `loss(T)` relation in.
- Practical rule: start one-way, add feedback only where a sensitivity check shows it moves the answer.

## Why not one monolithic multiphysics solve
A single solver doing EM + CHT + structural + fatigue is expensive, fragile, and locks you into one mesh/tool. Chaining lets each domain use its best solver and its own appropriate mesh; reduced-order models screen fast before the expensive solves. The cost is **handoff plumbing** — mapping a field from one solver's mesh onto another's — which is exactly why the [[IcepakThermalBridge_Progress_Log|IcepakThermalBridge]] tool had to exist.

## Related
- [[IGBT Electro-Thermal Loss Modelling]] · [[ETM For Heatsink and IGBT/00 Home|Heatsink ETM project]] · [[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]]
- [[Power Electronics]] · [[Thermal Management]] · [[Solid Mechanics]]
