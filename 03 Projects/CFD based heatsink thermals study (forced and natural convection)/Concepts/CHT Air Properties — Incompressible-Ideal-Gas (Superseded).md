---
concept: CHT Air Properties — Incompressible-Ideal-Gas Attempt
project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: incubating
created: 2026-08-31
sources: ["[[Inbox/CHT Fluent Based Setup]]"]
extracted_from: []
tags: [ETM, CFD, Fluent, CHT, MC_Heatsink, air-properties]
related: ["[[MC Heatsink CHT — Consolidated Setup]]"]
---

# CHT Air Properties — Incompressible-Ideal-Gas (Superseded)

> [!warning] Superseded 2026-09-01
> This was the setup decided on 2026-08-31, before the run stalled (fan reverse flow, continuity stuck ~0.3). The active baseline is now **Boussinesq + Sutherland μ**, see [[MC Heatsink CHT — Consolidated Setup]]. Kept here because the reasoning for rejecting Boussinesq (ΔT/T ≈ 0.24 > 0.1 rule-of-thumb) turned out to be an incomplete picture — the *bulk* buoyancy error is negligible in a fan-dominated (low Ri) flow even at this ΔT. Property variation (k, μ) was the real large-ΔT risk, and that's handled by keeping Sutherland μ regardless of density model.

## Problem Statement (as understood then)

CHT on MC heatsink in Fluent. Ambient = 36 °C, HS surface hits ~110 °C. Fan provides forced convection over most fins, but the dead zone under the IGBT (fan shadow) has near-zero forced flow → natural convection kicks in there → mixed convection regime overall.

Question: which density model + property setup gives physically correct h in *both* forced and buoyancy-driven regions without blowing up accuracy?

## What Was Decided (2026-08-31, later reverted)

- **Density** → `incompressible-ideal-gas`
- **Cp** → constant, 1007 J/kg·K
- **Thermal conductivity (k)** → `kinetic-theory` (or piecewise-linear)
- **Viscosity (μ)** → `sutherland`
- **Molecular weight** → 28.966 kg/kmol (fixed for dry air)
- **Operating Conditions** → gravity ON, operating density = ρ_ambient ≈ 1.143 kg/m³ @ 36 °C

## Decision Chain (as reasoned then)

1. **Rejected Boussinesq** because ΔT = 74 K → ΔT/T_ref ≈ 0.24, above the 0.1 validity rule-of-thumb. Density varies ~21% over range → linear approx assumed to fail.
2. **Rejected full `ideal-gas`** — unnecessary for low-Mach, incompressible flow; brings acoustic timestep pain.
3. **Chose `incompressible-ideal-gas`** — captures full ρ(T) via `ρ = p_op·MW/(R·T)`, handles buoyancy in dead zone correctly, no acoustic cost.
4. **k as constant was judged wrong** — varies ~24% from 36→110 °C, directly affects h in low-Re dead zone. Switched to `kinetic-theory`.
5. cp variation <1% over range → constant is fine (this part still holds).
6. μ needs Sutherland — varies ~20%, affects boundary layer everywhere (this part still holds).

## Why This Was Reverted

Running incompressible-ideal-gas + kinetic-theory + explicit pseudo-transient together caused persistent fan reverse flow and continuity stuck flat (~0.3). Root cause was mostly the **solver change** (explicit Pseudo Time Method with a conservative timescale, not Courant-200 coupled), compounded by incompressible-ideal-gas making local ρ near the hot HS drop (~0.92 vs 1.14), which made the density-corrected 3D fan momentum source wobble under recirculating hot air.

Lesson (see [[MC Heatsink CHT — Consolidated Setup]] → Method Principle): change ONE thing at a time — physics OR solver, never both. This attempt changed three things simultaneously (density model, k model, solver), so the failure couldn't be attributed.

## Reusable Reference Material

The property-model theory below is still valid background even though the density model choice changed.

### Incompressible-Ideal-Gas

> [!note] Intuition
> Ideal gas density (varies with T) but pressure is frozen at operating pressure for the density calc. So density responds to temperature (buoyancy works) but not to pressure fluctuations (no sound waves, no acoustic timestep).

$$\rho = \frac{p_{op} \cdot MW}{R \cdot T}$$

| Model | ρ formula | Valid ΔT | Cost |
|---|---|---|---|
| Constant | ρ = const | — (no buoyancy) | cheapest |
| Boussinesq | ρ = ρ₀[1 − β(T−T₀)] | ΔT/T < 0.1 (rule of thumb; negligible error at low Ri even beyond this) | cheap |
| Incompressible-ideal-gas | ρ = p_op·MW/RT | any (subsonic) | cheap |
| Ideal-gas | ρ = p·MW/RT | any | expensive (acoustic) |

### Lennard-Jones Parameters (kinetic-theory k/μ)

When k or μ is set to `kinetic-theory` in Fluent, two extra fields appear:
- **L-J Characteristic Length (σ)** — effective molecular diameter [Å]
- **L-J Energy Parameter (ε/k_B)** — potential well depth as temperature [K]

For air (Fluent defaults, correct): σ = 3.711 Å, ε/k_B = 78.6 K.

$$\phi(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$$

Chapman-Enskog kinetic theory relates σ, ε, MW to transport properties: k(T), μ(T) = f(T, MW, σ, ε/k_B) — physically-derived, no empirical fit needed.

| Gas | σ (Å) | ε/k_B (K) |
|---|---|---|
| Air/N₂ | 3.711 | 78.6 |
| O₂ | 3.467 | 106.7 |
| CO₂ | 3.941 | 195.2 |
| H₂O vapor | 2.641 | 809.1 |

Change these only for a different gas; for air/N₂-dominated systems, defaults are correct.

### Molecular Weight (MW)
Mass of one mole of the gas mixture. Air = weighted average of N₂ (78%), O₂ (21%), Ar (1%) ≈ 28.966 kg/kmol. Temperature-independent — a composition property. Only changes for combustion, humidity, or gas mixing.

### Reference Pressure Location — General Rule
Pick a point that is:
1. Inside the fluid domain (never inside a solid)
2. In a quiescent/ambient zone — far from heatsink, fan, inlet, outlet
3. Typically a far corner or top of enclosure

Fluent sets gauge pressure = 0 at this point → anchors the entire pressure field. Wrong placement (inside a solid, high-velocity zone, or too close to the HS) causes convergence issues.

## Atlas Connections
- [[CFD]]
- [[Heat Transfer]]
