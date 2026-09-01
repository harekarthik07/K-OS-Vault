For Air Prop Setup 
---
title: CHT Air Properties Setup — Boussinesq vs Incompressible-Ideal-Gas
tags: [ETM, CFD, Fluent, CHT, MC_Heatsink, air-properties]
project: T30_MC_ETM
related: [[MC_HS_ETM_I1]], [[T30_1D_Heatsink_IGBT_Loss_Chain]], [[Fluent_CHT_Setup]]
date: 2026-08-31
---

# Air Property Setup for MC Heatsink CHT (36 → 110 °C)

## Problem Statement

Running CHT on MC heatsink in Fluent. Ambient = 36 °C, HS surface hits ~110 °C. Fan provides forced convection over most fins, **but dead zone under IGBT (fan shadow) has near-zero forced flow** → natural convection kicks in there → **mixed convection regime overall**.

Question: which density model + property setup gives physically correct h in *both* forced and buoyancy-driven regions without blowing up accuracy?

---

## What We Decided

> [!success] Final Setup
> - **Density** → `incompressible-ideal-gas`
> - **Cp** → constant, 1007 J/kg·K
> - **Thermal conductivity (k)** → `kinetic-theory` (or piecewise-linear)
> - **Viscosity (μ)** → `sutherland`
> - **Molecular weight** → 28.966 kg/kmol (fixed for dry air)
> - **Operating Conditions** → gravity ON, operating density = ρ_ambient ≈ 1.143 kg/m³ @ 36 °C

## Why (Decision Chain)

1. **Rejected Boussinesq** because ΔT = 74 K → ΔT/T_ref ≈ 0.24, way above the 0.1 validity limit. Density varies ~21% over range → linear approx fails.
2. **Rejected full `ideal-gas`** — unnecessary for low-Mach, incompressible flow; brings acoustic timestep pain.
3. **Chose `incompressible-ideal-gas`** — captures full ρ(T) via `ρ = p_op·MW/(R·T)`, handles buoyancy in dead zone correctly, no acoustic cost.
4. **k as constant was wrong** — varies ~24% from 36→110 °C, directly affects h in low-Re dead zone. Switched to `kinetic-theory`.
5. **cp variation <1%** over range → constant is fine.
6. **μ needs Sutherland** — varies ~20%, affects boundary layer everywhere.

---

## Concept Breakdown

### 1. Incompressible-Ideal-Gas

> [!note] Intuition
> "Ideal gas density (varies with T) but pressure is *frozen* at operating pressure for the density calc." So density responds to temperature (buoyancy works) but not to pressure fluctuations (no sound waves, no acoustic timestep).

**Formula:**
$$\rho = \frac{p_{op} \cdot MW}{R \cdot T}$$

- `p_op` = operating pressure (101325 Pa), constant
- `T` = local temperature (varies)
- Density becomes purely a function of T

**When to use:**
- Low Mach (< 0.3) ✓
- Large ΔT where Boussinesq fails ✓
- Need buoyancy but don't want compressibility overhead ✓

**Contrast:**
| Model | ρ formula | Valid ΔT | Cost |
|---|---|---|---|
| Constant | ρ = const | — (no buoyancy) | cheapest |
| Boussinesq | ρ = ρ₀[1 − β(T−T₀)] | ΔT/T < 0.1 | cheap |
| Incompressible-ideal-gas | ρ = p_op·MW/RT | any (subsonic) | cheap |
| Ideal-gas | ρ = p·MW/RT | any | expensive (acoustic) |

---

### 2. Specific Heat (cp)

> [!note] Intuition
> "How much energy does 1 kg of this fluid need to warm up by 1 K." Sets how *sluggish* the fluid is thermally — high cp means slow to heat up, slow to cool down.

- Units: **J/(kg·K)**
- Enters energy equation directly: $\dot{q} = \dot{m} \cdot c_p \cdot \Delta T$
- For air: ~1007 J/kg·K, varies **<1%** from −50 to +200 °C → **constant is fine**
- Only worth making variable for very high ΔT (combustion, hypersonics) or non-ideal fluids

**In our case:** heat carried away by air stream = ṁ·cp·ΔT. cp determines how much airflow we need for a given heat removal.

---

### 3. Thermal Conductivity (k)

> [!note] Intuition
> "How well the fluid conducts heat through itself, molecule to molecule." In the boundary layer right next to the hot wall, heat crosses by *conduction through the fluid* before advection takes over → k directly sets the local h.

- Units: **W/(m·K)**
- Enters Fourier's law: $q'' = -k \frac{dT}{dy}$
- **Nusselt link:** $h = \frac{Nu \cdot k}{L}$ → **k appears directly in h**
- For air: varies **~24%** from 36 → 110 °C (0.0263 → 0.0325)

> [!warning] Why k matters most in the dead zone
> In the fan-shadow region, Re is tiny, Nu is small (natural conv dominated). h is *dominated* by k, not by velocity. Getting k wrong = getting h wrong = wrong T_junction prediction.

**Options in Fluent:**
- `constant` → OK only if ΔT small (<20 K)
- `piecewise-linear` → manual table (2-3 points enough)
- `kinetic-theory` → derived from MW + Lennard-Jones params, physically correct, **preferred**
- `sutherland` → also available for k

### Lennard-Jones Parameters (Auto-Required for kinetic-theory)

When k or μ is set to `kinetic-theory` in Fluent, two extra fields appear:

**L-J Characteristic Length (σ)** — effective molecular diameter [Å]
**L-J Energy Parameter (ε/k_B)** — potential well depth as temperature [K]

**For air (default Fluent values, correct):**
- σ = **3.711 Å**
- ε/k_B = **78.6 K**

**Physical basis — Lennard-Jones 12-6 potential:**
$$\phi(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$$

- r⁻¹² term → strong repulsion at short range (electron cloud overlap)
- r⁻⁶ term → weak attraction at moderate range (van der Waals)
- σ = zero-crossing distance
- ε = well depth (attraction strength)

**How Fluent uses them:**
Chapman-Enskog kinetic theory relates σ, ε, MW to transport properties:
$$k(T), \mu(T) = f(T, MW, \sigma, \varepsilon/k_B)$$

Result: physically-derived k(T) and μ(T) with correct temperature dependence — no need for empirical fits.

**When to change these:**
- Different gas (CO₂, H₂O vapor, etc.) → look up L-J params from tables
- For pure air/N₂ dominated systems → **defaults are correct, don't touch**

**Standard reference values:**

| Gas       | σ (Å) | ε/k_B (K) |
| --------- | ----- | --------- |
| Air/N₂    | 3.711 | 78.6      |
| O₂        | 3.467 | 106.7     |
| CO₂       | 3.941 | 195.2     |
| H₂O vapor | 2.641 | 809.1     |
### Sutherland's Law — Viscosity vs Temperature

**Formula (three-coefficient form):**
$$\mu(T) = \mu_{ref} \cdot \left(\frac{T}{T_{ref}}\right)^{3/2} \cdot \frac{T_{ref} + S}{T + S}$$

**Intuition:**
Derived from kinetic theory of gases with an intermolecular attraction correction. The T^(3/2) term comes from Maxwell-Boltzmann velocity distribution (hotter → faster molecules → more momentum transfer → higher μ). The (T_ref + S)/(T + S) term corrects for the fact that at low T, molecules "stick" briefly during collisions (Sutherland's molecular attraction model), reducing effective collision frequency.

**Physical meaning of S (Sutherland Constant):**
- Represents the characteristic temperature at which intermolecular attraction becomes negligible
- Higher S → stronger molecular attraction → viscosity more T-sensitive
- For air: S = 110.56 K

**Standard Sutherland Constants:**

| Gas | μ_ref (kg/m·s) | T_ref (K) | S (K) |
|---|---|---|---|
| **Air** | **1.716e-05** | **273.15** | **110.56** |
| N₂ | 1.663e-05 | 273 | 107 |
| O₂ | 1.919e-05 | 273 | 139 |
| CO₂ | 1.370e-05 | 273 | 222 |
| H₂ (steam) | 1.120e-05 | 350 | 1064 |

**Validity range for air:** 100 K to 1900 K → covers everything from cryogenic to combustion. Our 309–383 K range is well within validity.

**Verification against tabulated data:**

| T (°C) | T (K) | Sutherland μ | Table μ | Error |
|---|---|---|---|---|
| 36 | 309 | 1.884e-05 | 1.887e-05 | <1% |
| 110 | 383 | 2.22e-05 | 2.24e-05 | <1% |

**Why prefer Sutherland over piecewise-linear:**
- Physically-based (kinetic theory), not just curve fit
- 3 constants cover entire subsonic range → simpler than tables
- Extrapolates safely outside fitted range
- Nearly free computationally
- Fluent defaults are correct for air → zero setup effort

**When Sutherland breaks down:**
- Very high T (>2000 K) where dissociation happens
- Very high pressure where ideal gas assumption fails
- Non-ideal fluids (liquid, dense supercritical)

For our CHT (36–110 °C, 1 atm, air) → Sutherland is textbook-perfect.
---

### 4. Viscosity (μ)

> [!note] Intuition
> "Resistance of the fluid to shear — how much it 'sticks' to itself." Sets boundary layer thickness → controls where heat has to conduct through before advection takes over.

- Units: **kg/(m·s)** or Pa·s
- Two variants:
  - Dynamic viscosity μ [kg/m·s]
  - Kinematic viscosity ν = μ/ρ [m²/s]
- Enters: Re = ρUL/μ, and boundary layer equations
- For air: varies **~20%** from 36 → 110 °C (1.87e-5 → 2.24e-5)

**Sutherland's Law (what Fluent uses):**
$$\mu(T) = \mu_{ref} \cdot \left(\frac{T}{T_{ref}}\right)^{3/2} \cdot \frac{T_{ref} + S}{T + S}$$

- Physically-based (kinetic theory of gases)
- For air: S = 110.4 K, μ_ref = 1.716e-5 @ T_ref = 273.15 K (Fluent defaults)
- **Always use Sutherland for air over any non-trivial ΔT** — nearly free, big accuracy gain

---

### 5. Molecular Weight (MW)

> [!note] Intuition
> "Mass of one mole of the gas mixture." For air, it's the weighted average of N₂ (78%), O₂ (21%), Ar (1%) → ~28.97 g/mol.

- Units: **kg/kmol**
- Air: **28.966** (standard, don't change)
- **Where it's used:**
  1. Ideal gas law → ρ = p·MW/(R·T)
  2. Kinetic theory conductivity → uses MW to derive k(T)
  3. Species transport (if enabled)
- **Temperature-independent** — it's a composition property, not a state property
- Only changes if you're doing combustion, humidity, or gas mixing

---

---

## Operating Conditions (Final Setup)

### Values Entered

| Parameter | Value | Notes |
|---|---|---|
| Operating Pressure | 101325 Pa | Standard atm |
| Gravity | ON | Y = −9.81 m/s² (bike upright, +Y = up) |
| Specified Operating Density | ✅ CHECKED | Critical for variable-ρ + gravity |
| Operating Density | 1.145 kg/m³ | ρ_air @ ~35–36 °C ambient |
| Reference Pressure Location | (0, 0.53345, 0.01298) m | Top of enclosure, far from HS |
| Boussinesq Operating Temp | 309.16 K (ignored) | Not used — we're on incompressible-ideal-gas |

### Reference Pressure Location — How to Pick

> [!note] Rule
> Pick a point that is:
> 1. **Inside the fluid domain** (never inside a solid)
> 2. In a **quiescent/ambient zone** — far from heatsink, fan, inlet, outlet
> 3. Typically near a **far corner** or **top of enclosure** (for buoyancy-driven cases, top is natural since hot air rises → ambient stays at top far-field... wait, actually for our case top is fine because it's far from HS influence)

**Why it matters:**
- Fluent sets gauge pressure = 0 at this point → anchors the entire pressure field
- If placed inside a solid → invalid, solution errors
- If placed in high-velocity zone → pressure reference oscillates → residuals misbehave
- If placed too close to HS → thermal/buoyant plume shifts the reference → convergence issues

**My case:**
- Enclosure spans large volume above HS
- Point (0, 533.45 mm, 12.98 mm) sits at top-center of enclosure
- HS is at bottom → point is ~500 mm away → well outside thermal/momentum influence zone ✓

### Unit Gotcha

> [!warning] mm → m conversion
> Fluent Operating Conditions panel uses **meters**.
> ANSYS Discovery/SpaceClaim shows coords in **mm** by default.
> Always convert: 533.45 mm → **0.53345 m**

### Orientation Sanity Check

- Model +Y axis = physically upward (bike upright)
- Gravity vector: Y = −9.81 → gravity pulls in −Y direction ✓
- Buoyancy: hot air (ρ < ρ_op) experiences net force in +Y → rises ✓
- Consistent, no sign flips needed
---

## Reference Values (Post-Processing Only)

> [!note] What Reference Values are (and aren't)
> - **Used for:** computing non-dimensional coefficients in reports — Cd, Cl, Cf, Cp, Nu, and **h from wall heat flux**
> - **NOT used for:** the actual solution. Solver ignores these during iteration.
> - **Separate from:** Operating Conditions (which DO affect solution via ρ_op, gravity, etc.)

### Critical settings for our CHT

| Field | Value | Why |
|---|---|---|
| Temperature | **309.16 K (36 °C)** | Ambient — used as T_ref when Fluent computes h = q″/(T_wall − T_ref) |
| Density | 1.145 kg/m³ | Matches operating density |
| Viscosity | 1.88e-05 kg/m·s | μ @ 36 °C |
| Reference Zone | **Fluid domain zone** (NOT solid) | Solid zone gives meaningless flow coefficients |
| Length | HS characteristic length | For Re, Nu (only if reporting those) |
| Area | HS frontal area | For Cd (only if reporting drag) |

### Gotcha
Default Reference Zone often auto-picks a solid — **manually reassign to fluid enclosure zone** or all flow reports break.

### For our ETM work — minimum required
Since we mainly report T_IGBT and wall heat flux (W/m²), only these matter:
- Temperature = 309.16 K → correct h reporting
- Reference Zone = fluid → clean flow coefficients if we ever need them

### Characteristic Length — Two Different Contexts

> [!warning] Don't confuse these
> The "length" you enter in Fluent Reference Values ≠ the conduction length in your 1D model.

**1D thermal model (MC_HS_ETM_I1):**
- L_cond (IGBT base → fin root) = **18 mm** = 0.018 m
- Used in: R_cond = L/(k·A) for baseplate conduction resistance
- Material: LM25 Al, k ≈ 150 W/m·K
- This connects IGBT case node → fin-root node in Cauer network

**CFD Reference Values (Fluent):**
- Length = **fin height** (or hydraulic diameter of channel between fins)
- Used ONLY for Nu, Re coefficient reports
- Doesn't affect solution
- If not reporting Nu → leave default, doesn't matter

### Reporting h from Fluent — Watch the Reference Temp

**Surface HTC formula in Fluent:**
$$h = \frac{q''_{wall}}{T_{wall} - T_{ref}}$$

- T_ref comes from **Reference Values → Temperature** (NOT Operating Conditions)
- Length in Ref Values → **not used** for h, only for Nu/Re
- So for h reporting, only Temp and Reference Zone matter

**Gotcha for our ETM validation:**
- Fluent h uses **far-field ambient** (309.16 K) as reference
- In fan dead zone, local air near fin is much hotter (recirculation)
- → Fluent's h *underestimates* the true local heat transfer capability
  (because ΔT is inflated using cold ambient instead of warm local film)

**Correct approach for feeding h into 1D Cauer model:**
1. Split HS surface into zones (fan-active vs dead zone)
2. Per zone: report area-averaged q″ AND area-averaged near-wall T_fluid (via custom surface at y+~30)
3. Compute h_zone = q″_zone / (T_wall_zone − T_fluid_near_wall_zone)
4. Feed h_zone × A_zone into parallel R_conv branches in Simulink

This resolves **Open Item #3** from ETM model: "CFD-derived area-weighted h for the fan dead zone."


### Y+ Based Surface Heat Transfer Coefficient (My Preferred Method)

**Formula:**
$$h_{y+} = \frac{q''_{wall}}{T_{wall} - T_{y+}}$$

Where T_y+ is the fluid temperature at y+ = (Yplus for HTC value), back-computed from wall function thermal law.

> [!success] Why y+ based h is right for my ETM validation
> - Reference temp = **local near-wall fluid** (not far-field ambient)
> - Handles fan dead zone correctly (accounts for recirculating hot air)
> - Directly gives zone-appropriate h for feeding into 1D Cauer R_conv
> - **Resolves Open Item #3** without manual T_fluid extraction per zone

**Critical setting: Yplus for HTC**
- Not "300 by default" — MUST match your actual mesh y+
- Check via: Report → Surface Integrals → Area-Weighted Avg → Wall Yplus on HS
- Then update Reference Values → Yplus for HTC to match

| Actual mesh y+ | Set Yplus for HTC to |
|---|---|
| 1–5 (resolved) | 1 |
| 30–60 (wall function) | 30 |
| 100–300 (coarse WF) | 100 or 300 |

**What still doesn't affect h_y+:**
- Length, Area, Velocity, Density, μ in Ref Values → all irrelevant
- Only "Yplus for HTC" and Reference Zone matter

---

## Complete Setup Checklist (Before Initialize)

- [x] Density: incompressible-ideal-gas
- [x] Cp: constant 1007 J/kg·K
- [x] k: kinetic-theory (varies with T)
- [x] μ: sutherland
- [x] MW: 28.966 kg/kmol
- [x] Operating Pressure: 101325 Pa
- [x] Gravity: ON, (0, −9.81, 0) m/s²
- [x] Specified Operating Density: ✅ 1.145 kg/m³
- [x] Reference Pressure Location: (0, 0.53345, 0.01298) m
- [ ] Boundary conditions set (inlet, outlet, wall heat flux/temp)
- [ ] Initialize: patch T = 309.16 K everywhere in fluid
- [ ] URFs: energy 0.9 → 1.0 ramp over first 100 iters
- [ ] Monitor: T at IGBT base, mass imbalance, energy imbalance
- [ ] Convergence targets: residuals < 1e-4 (energy < 1e-6)

---
![[Pasted image 20260831185112.png]]
## Quick Reference — Why Each Choice

| Choice                     | Why                                             | Alternative Rejected Because                                     |
| -------------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| incompressible-ideal-gas   | Handles 21% ρ variation over 36→110 °C          | Boussinesq fails (ΔT/T > 0.1); full ideal-gas adds acoustic cost |
| kinetic-theory k           | k varies 24% → dominates h in dead zone         | Constant k → wrong T_junction                                    |
| sutherland μ               | μ varies 20%, affects BL everywhere             | Constant μ → wrong Re, wrong h                                   |
| Specified ρ_op             | Locks buoyancy reference → clean convergence    | Auto ρ_op → drifts, oscillates                                   |
| Ref pressure at top corner | Quiescent, far from HS → stable pressure anchor | (0,0,0) default → often inside solid or bad zone                 |
## Related Concepts to Explore Later

- [[Richardson_Number]] — Ri = Gr/Re² for classifying forced vs mixed vs natural conv
- [[Grashof_Number]] — buoyancy vs viscous forces
- [[Boussinesq_Approximation]] — when it's valid, derivation
- [[Sutherland_Law_Derivation]] — kinetic theory basis
- [[Fluent_Operating_Conditions]] — operating density, ref pressure, gravity setup
- [[Boundary_Layer_h_vs_k]] — why k dominates h at low Re
- [[Kinetic_Theory_Transport_Properties]] — how Fluent derives k, μ from MW

---

## Action Log

- [x] Switch density: constant → incompressible-ideal-gas
- [x] Switch μ: constant → sutherland
- [x] Switch k: constant → kinetic-theory
- [x] Confirm MW = 28.966
- [x] Confirm cp = 1007 (constant OK)
- [x] Set operating density = 1.143 @ 36 °C in Operating Conditions ✅ 2026-08-31
- [x] Enable gravity, set g-vector per model orientation ✅ 2026-08-31
- [ ] Patch initial T = 309 K (36 °C) everywhere before solving
- [ ] Ramp energy URF 0.9 → 1.0 over first 100 iters to avoid buoyancy divergence


# 3d Fan Zone Setup 

### 3D Fan Zone Setup — Momentum Source Method

> [!note] Why 3D Fan Zone (vs pressure-jump BC)
> - Pressure-jump: 2D disk with ΔP(Q) — no swirl, no radial variation
> - 3D Fan Zone: volumetric momentum source distributed over fan disk thickness
>   - Captures **swirl** (tangential source) → wake mixing
>   - Captures **radial flow** (radial source) → proper distribution over fin field
>   - Uses **inflection point** to split axial/radial contribution
>   - Better fidelity for downstream heat transfer, especially at HS surface

### Geometry Inputs (from fan datasheet)

| Parameter | Value | Source |
|---|---|---|
| Hub Radius | 16.5 mm | Datasheet drawing |
| Tip Radius | 38.75 mm | Datasheet drawing |
| Thickness | 15 mm | Fan disk axial depth |
| Fan Origin | (X, Y_center, Z) | From CAD → geometric center of fan disk |
| Inflection Point | 0.83 (default) | Axial → radial transition radius (r/R_tip) |

### Operating Inputs

| Parameter | Value | Notes |
|---|---|---|
| Angular Velocity | 450.29 rad/s (≈4300 RPM) | Datasheet operating speed |
| Rotational Direction | positive/negative | Right-hand rule against fan-in-int normal |
| Fan Curve | Load .txt file (Q vs ΔP) | Polynomial fit order 2 usually adequate |
| Test Temperature | 298.16 K | Datasheet reference (density correction) |
| Max Flow Rate Limit | 0.0237 m³/s (~85 CFM) | Datasheet free-delivery value |

### Critical Setup Checks

1. **Fan Origin = geometric center of fan disk** (on rotation axis)
2. **Rotational Direction** — right-hand rule against fan-in-int normal
   - Wrong direction → flow reverses entirely
3. **Load fan curve** via "Read Fan Curve..." before running
   - Without it → zero pressure rise → zero flow
4. **fan-in-int and fan-out-int must be interior surfaces** (not walls)
5. **Fan disk fluid zone must be separate zone** from surrounding air enclosure

### Post-Run Validation

- [ ] Mass flow through fan ≈ 0.027 kg/s (Q × ρ)
- [ ] ΔP across fan matches fan curve at operating Q
- [ ] Tangential velocity component visible in wake (swirl proof)
- [ ] Flow direction from fan-in-int → fan-out-int (not reversed)

### Common Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Zero flow through fan | Fan curve not loaded | Read fan curve file |
| Flow in wrong direction | Rot direction wrong | Flip positive↔negative |
| Flow > max limit | Limit Flow Rate unchecked | Enable checkbox |
| No swirl in wake | Tangential Source not enabled | Enable if datasheet gives swirl profile |
| ΔP way off curve | Wrong Test Temperature | Set to datasheet ref (usually 298 K) |

#### 1. Fan Origin

Origin should be the **geometric center of the fan disk**, on the rotation axis. Your Y = −0.04628 puts it below world origin, Z = 0.01298 matches your reference pressure point earlier.

> [!warning] Verify
> 
> - Open Discovery/CAD → locate fan disk center coordinates
> - Confirm rotation axis passes through this point
> - Rotation axis direction is inferred from the fan zone's normal — make sure fan-in-int face normal points along your intended rotation axis

#### 2. Rotational Direction — Right-Hand Rule

"Positive" = using right-hand rule about the axis normal defined by `fan-in-int` face orientation.

**Check:** curl fingers of right hand in direction of blade rotation → thumb should point in same direction as fan-in-int face normal (outward from inlet side).

If your fan physically spins clockwise when viewed from the inlet side, and inlet normal points _toward_ you → set to **negative**.

If it spins counter-clockwise viewed from inlet, normal points toward you → **positive** ✓

Getting this wrong = fan blows in wrong direction = your entire flow field reverses.

#### 3. Fan Curve (Axial Source Term)

You've set **Method: fan curve** with polynomial fit order 2. Good — but you need to:

> [!important] Have you loaded the fan curve yet?  
> Click **"Read Fan Curve..."** and load the P-Q data file from datasheet:
> 
> - File format: text file with two columns → Flow Rate [m³/s], Static Pressure Rise [Pa]
> - Should span from zero flow (max ΔP) to free delivery (zero ΔP)
> - Polynomial order 2 is fine for most fans; use order 3 if curve has strong knee
> 
> Without loading the curve, fan produces zero pressure rise → no flow.

#### 4. Test Temperature = 298.16 K

This is the temperature at which the fan curve was measured (datasheet standard). **Correct as-is at 298.16 K (25 °C)** — Fluent corrects fan performance for actual operating density using this reference.

#### 5. Inflection Point = 0.83

This is the **non-dimensional radial location** (0 = hub, 1 = tip) where flow transitions from mostly axial to significant radial component. Default 0.83 is typical for axial cooling fans. Only change if your fan is a mixed-flow type (then 0.5–0.7).

### Quick sanity checks post-first-run

After 100 iterations, verify:

1. **Mass flow through fan** — should approach your operating point on the fan curve
    - Report → Surface Integrals → Mass Flow Rate on `fan-in-int`
    - Should be close to (but less than) 0.0237 m³/s × 1.145 kg/m³ ≈ 0.027 kg/s
2. **Pressure rise across fan** — matches fan curve at that flow rate
    - Report → Surface Integrals → Area-Weighted Avg Static Pressure on fan-in-int vs fan-out-int
    - ΔP should be on the fan curve at your operating Q
3. **Swirl component in wake** — you should see tangential velocity downstream (this is what 3D Fan gives you that pressure-jump doesn't)
