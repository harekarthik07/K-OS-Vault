---
tags: [CAE, thermal, structural, fatigue, ansys, icepak, mechanical, maxwell, busbar, G-Bridge]
aliases: [G-Bridge Fatigue, Busbar Thermal Fatigue, NVA5P1MCP0090_A_GBridge, IcepakThermalBridge]
status: active
created: 2026-09
project: Busbar G-Bridge Thermal Fatigue
related:
  - "[[IcepakThermalBridge_Progress_Log]]"
  - "[[IcepakThermalBridge_Flowchart]]"
  - "[[Thermal_Fatigue_Approach_and_TODO]]"
---

# Busbar / G-Bridge Thermal Fatigue — Problem Statement

> [!abstract] One-line objective
> Determine the thermal fatigue life of the **G-Bridge plastic housing** (`NVA5P1MCP0090_A_GBridge`) and its busbar assembly under a real electrical duty cycle, by chaining **Maxwell 3D → Icepak → Mechanical** so that electromagnetic loss drives temperature, and temperature drives cyclic strain.

## Why this exists

The G-Bridge is the plastic component that carries and locates the six busbars (5× cast-aluminium AC/DC busbars + the housing itself, ABS+PC, flame retardant grade) in the motor controller / power distribution assembly. Under electrical load the busbars generate **Joule (I²R) and ohmic loss**, heat the surrounding plastic, and — because aluminium and ABS+PC have very different coefficients of thermal expansion (CTE) — the mismatch in thermal growth loads the housing at the busbar interface every time the vehicle power cycles. Repeated cycling is a classic driver of **thermomechanical fatigue** in the plastic, independent of any single peak-temperature stress check.

This is a companion effort to the T30 motor-controller heatsink thermal work (see the companion [[ETM For Heatsink and IGBT/00 Home|T30 MC heatsink ETM work]]) but is a **separate physical assembly and a separate analysis chain** — no shared geometry or model with the IGBT/heatsink ETM work.

## Physics chain (what has to happen, conceptually)

```
Electrical current input (AC + DC busbars)
        │
        ▼
Maxwell 3D  ── AC conduction + DC conduction solve
        │        → Joule loss (AC skin/proximity effect)
        │        → Ohmic loss (I²R, DC)
        ▼
Icepak  ── conjugate heat transfer (CHT) solve
        │        → steady-state (later: transient) temperature field
        │          across all 6 solids (5 busbars + G-Bridge housing)
        ▼
Mechanical (Static Structural)
        │        → Imported Body Temperature load
        │        → CTE-mismatch stress / strain / deformation
        ▼
(Not yet built) Fatigue post-processing
                 → cyclic strain range at busbar–plastic interface
                 → thermoplastic fatigue life estimate
```

## Toolchain

- **Ansys Electronics Desktop (AEDT) 2025 R2** — Maxwell 3D (AC Conduction, DC Conduction setups) and Icepak (Electronics Thermal) in one project.
- **Ansys Workbench 2025 R2** — Static Structural, geometry shared from the Icepak design.
- **Custom ACT extension: `IcepakThermalBridge`** (Python/IronPython, WinForms UI) — bridges Icepak → Mechanical because the native Workbench system-coupling link (`Icepak Solution → Static Structural Setup`) would not populate. See [[IcepakThermalBridge_Progress_Log]] for why, and [[IcepakThermalBridge_Flowchart]] for how the replacement works.

## Assembly definition

| Body | Material | Role |
|---|---|---|
| `AC_Busbar_A/B/C` | Aluminium alloy, cast 383.0 | AC power conduction |
| `DC_Busbar_A/B` | Aluminium alloy, cast 383.0 | DC power conduction |
| `G_Bridge` (`NVA5P1MCP0090_A_GBridge`) | Plastic, ABS+PC (flame retardant) | Structural housing / busbar locator — **the fatigue-critical part** |

> [!success] Material confirmed (2026-09-24)
> Busbars are **cast 383.0 aluminium alloy** (~96 W/m·K), a die-casting alloy — **not** copper. Confirmed by Karthik. The Icepak thermal field and every downstream number (stress, strain, fatigue life) use the correct conductivity; no material-driven error to carry. (For context: had it been copper at ~380 W/m·K the field would have been overpredicted.)

## Scope boundary — what this problem statement covers

- ✅ Maxwell loss solve → Icepak temperature field → Mechanical thermal stress (steady-state), including the tooling to make the Icepak→Mechanical handoff reliable.
- ⛔ **Not yet in scope, deliberately deferred:** transient cycling, load-step definition in Static Structural, reference/stress-free temperature, contact definition (bonded vs frictional at the busbar–plastic interface), temperature-dependent material properties (E, CTE vs T), and the actual thermoplastic fatigue-life calculation. All of these are captured as forward work in [[Thermal_Fatigue_Approach_and_TODO]] so they aren't lost, but they are **not being worked yet** — current focus is getting the steady-state Icepak → Mechanical temperature transfer fully verified and repeatable.

## Key identifiers (for search / backlinks)

`G-Bridge` · `NVA5P1MCP0090_A_GBridge` · `IcepakThermalBridge` · `busbar thermal fatigue` · `AC_Busbar_A/B/C` · `DC_Busbar_A/B` · `Maxwell 3D` · `AC Conduction` · `DC Conduction` · `Icepak` · `Imported Body Temperature` · `CTE mismatch` · `ABS+PC flame retardant`
