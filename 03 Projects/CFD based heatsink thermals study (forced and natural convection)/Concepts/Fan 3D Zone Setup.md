---
concept: 3D Fan Zone Setup
project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: incubating
created: 2026-08-31
sources: ["[[Inbox/CHT Fluent Based Setup]]"]
extracted_from: []
tags: [CFD, Fluent, fan-model, MC_Heatsink]
related: ["[[MC Heatsink CHT — Consolidated Setup]]"]
---

![[Pasted image 20260831185112.png]]

# 3D Fan Zone Setup — Momentum Source Method

> [!note] Why 3D Fan Zone (vs pressure-jump BC)
> - Pressure-jump: 2D disk with ΔP(Q) — no swirl, no radial variation
> - 3D Fan Zone: volumetric momentum source distributed over fan disk thickness
>   - Captures **swirl** (tangential source) → wake mixing
>   - Captures **radial flow** (radial source) → proper distribution over fin field
>   - Uses **inflection point** to split axial/radial contribution
>   - Better fidelity for downstream heat transfer, especially at HS surface

## Geometry Inputs (from fan datasheet)

| Parameter | Value | Source |
|---|---|---|
| Hub Radius | 16.5 mm | Datasheet drawing |
| Tip Radius | 38.75 mm | Datasheet drawing |
| Thickness | 15 mm | Fan disk axial depth |
| Fan Origin | (0, −0.04628, 0.01298) m | Geometric center of fan disk, from CAD |
| Inflection Point | 0.83 (default) | Axial → radial transition radius (r/R_tip) |

## Operating Inputs

| Parameter | Value | Notes |
|---|---|---|
| Angular Velocity | 450.29 rad/s (≈4300 RPM) | Datasheet operating speed |
| Rotational Direction | positive/negative | Right-hand rule against fan-in-int normal |
| Fan Curve | Load .txt file (Q vs ΔP) | Polynomial fit order 2 usually adequate |
| Test Temperature | 298.16 K | Datasheet reference (density correction) |
| Max Flow Rate Limit | 0.0237 m³/s (~85 CFM) | Datasheet free-delivery value |

## Critical Setup Checks

1. **Fan Origin = geometric center of fan disk** (on rotation axis)
2. **Rotational Direction** — right-hand rule against fan-in-int normal
   - Wrong direction → flow reverses entirely
3. **Load fan curve** via "Read Fan Curve..." before running
   - Without it → zero pressure rise → zero flow
4. **fan-in-int and fan-out-int must be interior surfaces** (not walls)
5. **Fan disk fluid zone must be separate zone** from surrounding air enclosure

## Post-Run Validation

- [ ] Mass flow through fan ≈ 0.027 kg/s (Q × ρ)
- [ ] ΔP across fan matches fan curve at operating Q
- [ ] Tangential velocity component visible in wake (swirl proof)
- [ ] Flow direction from fan-in-int → fan-out-int (not reversed)

## Common Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Zero flow through fan | Fan curve not loaded | Read fan curve file |
| Flow in wrong direction | Rot direction wrong | Flip positive↔negative |
| Flow > max limit | Limit Flow Rate unchecked | Enable checkbox |
| No swirl in wake | Tangential Source not enabled | Enable if datasheet gives swirl profile |
| ΔP way off curve | Wrong Test Temperature | Set to datasheet ref (usually 298 K) |

## Detail Notes

### Fan Origin
Origin should be the **geometric center of the fan disk**, on the rotation axis. Y = −0.04628 puts it below world origin; Z = 0.01298 matches the reference pressure point used in Operating Conditions.

> [!warning] Verify
> - Open Discovery/CAD → locate fan disk center coordinates
> - Confirm rotation axis passes through this point
> - Rotation axis direction is inferred from the fan zone's normal — make sure fan-in-int face normal points along the intended rotation axis

### Rotational Direction — Right-Hand Rule
"Positive" = using right-hand rule about the axis normal defined by `fan-in-int` face orientation.

**Check:** curl fingers of right hand in direction of blade rotation → thumb should point in same direction as fan-in-int face normal (outward from inlet side).

If the fan physically spins clockwise viewed from the inlet side, and inlet normal points *toward* you → set to **negative**.
If it spins counter-clockwise viewed from inlet, normal points toward you → **positive** ✓

Getting this wrong = fan blows in wrong direction = entire flow field reverses.

### Fan Curve (Axial Source Term)
Method: fan curve, polynomial fit order 2.

> [!important] Load the fan curve
> Click **"Read Fan Curve..."** and load the P-Q data file from the datasheet:
> - File format: text file with two columns → Flow Rate [m³/s], Static Pressure Rise [Pa]
> - Should span from zero flow (max ΔP) to free delivery (zero ΔP)
> - Polynomial order 2 is fine for most fans; use order 3 if the curve has a strong knee
>
> Without loading the curve, fan produces zero pressure rise → no flow.

### Test Temperature = 298.16 K
Temperature at which the fan curve was measured (datasheet standard). Fluent corrects fan performance for actual operating density using this reference. Correct as-is.

### Inflection Point = 0.83
Non-dimensional radial location (0 = hub, 1 = tip) where flow transitions from mostly axial to significant radial component. Default 0.83 is typical for axial cooling fans; only change for mixed-flow fans (then 0.5–0.7).

### Quick sanity checks post-first-run
After 100 iterations, verify:

1. **Mass flow through fan** — should approach the operating point on the fan curve
   - Report → Surface Integrals → Mass Flow Rate on `fan-in-int`
   - Should be close to (but less than) 0.0237 m³/s × 1.145 kg/m³ ≈ 0.027 kg/s
2. **Pressure rise across fan** — matches fan curve at that flow rate
   - Report → Surface Integrals → Area-Weighted Avg Static Pressure on fan-in-int vs fan-out-int
   - ΔP should be on the fan curve at the operating Q
3. **Swirl component in wake** — tangential velocity should be visible downstream (this is what 3D Fan gives that pressure-jump doesn't)

## Atlas Connections
- [[CFD]]
