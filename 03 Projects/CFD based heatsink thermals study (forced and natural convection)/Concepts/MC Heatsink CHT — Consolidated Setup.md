---
concept: MC Heatsink CHT Setup
project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: incubating
created: 2026-09-01
sources: ["[[Daily Log#2026-09-01]]"]
extracted_from: []
tags: [ETM, CFD, Fluent, CHT, MC_Heatsink, air-properties, solver-setup, forced-convection]
related: ["[[MC_HS_ETM_I1]]", "[[T30_1D_Heatsink_IGBT_Loss_Chain]]", "[[Fan_3D_Zone_Setup]]"]
verdict_status: validated-baseline
---

# MC Heatsink CHT — Consolidated Setup

> [!abstract] What this note is
> The single source of truth for my MC heatsink conjugate heat transfer (CHT) run in Fluent. Built on my **validated boussinesq baseline**, with the low-risk fidelity upgrades layered on top (Sutherland viscosity, corrected k, operating conditions, reference values, y+ based h workflow). Solver settings are the proven Courant-200 coupled config — NOT the pseudo-transient version that stalled.

---

## Problem Statement

CHT on the MC heatsink. Ambient = 36 °C (309.16 K), HS surface reaches ~110 °C. A fan provides forced convection over most fins, **but the dead zone under the IGBT (fan shadow) has near-zero forced flow** → natural convection contributes there → **mixed convection overall, forced-dominated**.

Goal: physically correct, dyno-validated **h [W/m²·K]** on the HS surfaces (per zone) to feed into the 1D Cauer model ([[MC_HS_ETM_I1]]) R_conv branches. This closes **Open Item #3** (CFD-derived area-weighted h for the fan dead zone).

---

## Final Material — air36 (Boussinesq)

> [!success] Validated config + cheap fidelity bump
> Boussinesq baseline (proven against dyno) with Sutherland μ added as a low-risk upgrade.

| Property | Setting | Value | Notes |
|---|---|---|---|
| Density | **boussinesq** | 1.145 kg/m³ | ρ @ ~36 °C ambient |
| Cp | constant | 1007 J/kg·K | varies <1% over range → constant fine |
| Thermal Conductivity | constant | 0.02627 W/m·K | k @ 36 °C (interpolated) |
| Viscosity | **sutherland** | (3-coeff) | upgraded from constant — stable, near-free |
| Thermal Expansion Coeff (β) | constant | 0.00323457 K⁻¹ | = 1/T_ref = 1/309.16 |

### β check
$$\beta = \frac{1}{T_{ref}} = \frac{1}{309.16} = 0.003235 \text{ K}^{-1} \checkmark$$

### Sutherland coefficients (air, Fluent defaults — don't change)
$$\mu(T) = \mu_{ref}\left(\frac{T}{T_{ref}}\right)^{3/2}\frac{T_{ref}+S}{T+S}$$

| Coeff | Value |
|---|---|
| μ_ref | 1.716e-05 kg/m·s |
| T_ref | 273.15 K |
| S (Sutherland const) | 110.56 K |

Verified vs air table: μ(309 K) = 1.884e-05 (table 1.887e-05), μ(383 K) = 2.22e-05 (table 2.24e-05) → <1% error across range. ✓

> [!note] Why Sutherland μ but constant k?
> μ drives the boundary layer / fan flow directly → worth the T-dependence. k constant at 36 °C value is fine and matches the validated baseline. Both vary ~20–24% but keeping k constant errs conservative. Don't overthink — leave k constant on the boussinesq baseline.

---

## Why Boussinesq (and NOT incompressible-ideal-gas) for this case

> [!important] Corrected understanding
> Boussinesq's buoyancy-term error **only matters where buoyancy matters**. This is a **fan-dominated** case → low Richardson number (Ri = Gr/Re² << 1) → buoyancy is a minor term in the momentum balance → Boussinesq error is negligible in the overall result.
>
> The large-ΔT worry (ΔT/T ≈ 0.24) is really about **property variation (k, μ)**, not the density linearization. And most of the bulk air stays near ambient — only the thin boundary layer at the HS surface is at 110 °C. So constant/boussinesq props are defensible, and they're **validated against dyno**.

**Validated-and-converged beats theoretically-pure-but-unconverged.**

### The ideal-gas experiment (what went wrong)
When I swapped to incompressible-ideal-gas + kinetic-theory + pseudo-transient all at once, I got persistent fan reverse flow and stuck continuity (~0.3 flat). Root cause was **mostly the solver change**, secondarily the ideal-gas + fan coupling:
- incompressible-ideal-gas → local ρ drops near hot HS (~0.92 vs 1.14) → the density-corrected 3D fan momentum source wobbles when hot air recirculates → reverse flow harder to settle.
- boussinesq keeps **bulk ρ constant** (only the buoyancy source term varies) → fan sees clean constant-density air → predictable, clears fast.

---

## Density Model Reference

| Model | ρ formula | Valid ΔT | Cost | Use for my case? |
|---|---|---|---|---|
| Constant | ρ = const | no buoyancy | cheapest | ❌ no buoyancy |
| **Boussinesq** | ρ = ρ₀[1 − β(T−T₀)] | small (but see note) | cheap | ✅ **validated, fan-dominated** |
| Incompressible-ideal-gas | ρ = p_op·MW/RT | any subsonic | cheap | ⚠️ destabilizes fan coupling |
| Ideal-gas | ρ = p·MW/RT | any | expensive (acoustic) | ❌ overkill |

---

## Operating Conditions

| Parameter | Value | Notes |
|---|---|---|
| Operating Pressure | 101325 Pa | standard atm |
| Gravity | ON, (0, −9.81, 0) | +Y = up (bike upright) |
| Boussinesq Operating Temperature | 309.16 K | **used** (this IS the boussinesq T_ref) |
| Specified Operating Density | ✅ CHECKED | 1.145 kg/m³ |
| Reference Pressure Location | (0, 0.53345, 0.01298) m | top of enclosure, far from HS |

> [!note] Boussinesq Operating Temperature matters now
> Unlike the ideal-gas run (where it was ignored), with boussinesq density the Operating Temperature (309.16 K) **is** the reference temperature T₀ in ρ = ρ₀[1 − β(T−T₀)]. Must be set correctly = ambient.

### Why specify operating density
Buoyancy force = (ρ − ρ_op)·g. If ρ_op is auto-computed it drifts each iteration → oscillation. Locking to ambient ρ makes ambient cells buoyancy-neutral (correct) and hot cells rise.

### Reference pressure location rule
Point must be (1) inside fluid, (2) quiescent zone far from HS/fan/inlet, (3) typically a far corner or top. My point sits ~500 mm above the HS → well outside thermal/momentum influence. ✓ **Unit gotcha:** CAD shows mm, Fluent wants m → 533.45 mm = 0.53345 m.

---

## Reference Values (post-processing only)

> [!note] What these are
> Used ONLY for computing coefficients in reports (Cd, Cl, Cf, Nu, and h). They do **NOT** affect the solution. Separate from Operating Conditions.

| Field | Set to | Matters? |
|---|---|---|
| Temperature | **309.16 K** | ✅ used as T_ref when reporting h |
| Density | 1.145 | minor |
| Viscosity | 1.895e-05 | minor |
| Reference Zone | **fluid domain** (NOT solid) | ✅ critical |
| Yplus for HTC | **match actual mesh y+** | ✅ critical (check after first run) |
| Length, Area, Velocity | defaults | only for Nu/Re/Cd |

> [!warning] Two must-fix items
> 1. Temperature was defaulting to 288.16 → set to **309.16 K**.
> 2. Reference Zone often auto-picks a **solid** (e.g. `..._330w-domain-dom`) → reassign to the **fluid** enclosure zone or all flow/h reports break.

---

## h Extraction — y+ Based Surface HTC (my method)

$$h_{y+} = \frac{q''_{wall}}{T_{wall} - T_{y+}}$$

T_y+ = fluid temp at the specified y+ location, back-computed from the wall-function thermal law.

> [!success] Why y+ based h is right for ETM validation
> Reference temp = **local near-wall fluid**, not far-field ambient. Handles the dead zone correctly (accounts for hot recirculating air). Gives zone-appropriate h directly for the Cauer R_conv branches — no manual per-zone T_fluid extraction.

**Critical:** "Yplus for HTC" must match the actual mesh y+.
- Check: `Report → Surface Integrals → Area-Weighted Avg → Wall Yplus` on HS surfaces
- Then set Reference Values → Yplus for HTC to match (y+~1 resolved → 1; y+~30 wall function → 30; coarse → 100–300)

**Length does NOT affect h_y+** — only appears in Nu/Re. Only Temperature, Reference Zone, and Yplus-for-HTC matter for h.

### Theory anchor — where h comes from
At the wall, no-slip → heat crosses by pure conduction → Fourier = Newton's cooling:
$$h = \frac{-k_f (\partial T/\partial y)|_{y=0}}{T_w - T_{ref}}$$
Fluent computes ∂T/∂y at the wall from the resolved field → h directly. **This is why wall mesh resolution (y+) controls h accuracy.** For air Pr≈1 → δ ≈ δt → a mesh resolving the momentum BL also resolves the thermal BL.

> [!note] Why CFD instead of a Nu correlation
> Nu = C·Re^m·Pr^n needs a known geometry + clean flow. The fan dead zone (recirculation, confined fin channels, non-uniform approach) has no valid C,m,n. CFD resolves the real local ∂T/∂y everywhere → true local h. That's the whole justification for doing this.

---

## 3D Fan Zone (summary — see [[Fan 3D Zone Setup]])

Values from fan datasheet. Captures swirl + radial variation (vs a flat pressure-jump).

| Parameter | Value |
|---|---|
| Hub Radius | 0.0165 m |
| Tip Radius | 0.03875 m |
| Thickness | 0.015 m |
| Fan Origin | (0, −0.04628, 0.01298) m — disk center |
| Inflection Point | 0.83 |
| Angular Velocity | 450.29 rad/s (~4300 RPM) |
| Test Temperature | 298.16 K (datasheet ref) |
| Max Flow Limit | 0.023668 m³/s |

> [!warning] Fan gotchas (caused my reverse-flow scare)
> - **Load the fan curve** (Read Fan Curve) — Q vs ΔP_rise, positive. Without it → zero flow.
> - **Rotational direction** — right-hand rule vs fan-in-int normal. Wrong → flow reverses.
> - Reverse flow <10 faces early = normal; >50 persisting = real problem.
> - Small early reverse flow is expected — on the validated solver it clears by ~10–15 iters.

---

## Solver Setup (VALIDATED — the proven config)

> [!success] This is the working recipe. Do NOT turn on explicit pseudo-transient.

### General
- Pressure-Based, **Steady**, Absolute velocity
- Gravity ON (0, −9.81, 0)

### Models
- Energy: ON
- Viscous: **k-ω SST** (handles mixed convection + auto y+ blending). **NOT laminar** — the fan jet + fin channels are turbulent.
- Radiation: OFF

### Solution Methods
| Setting | Value |
|---|---|
| Scheme | **Coupled** |
| Pressure | **PRESTO!** |
| Gradient | Least Squares Cell Based |
| Momentum / k / ω / Energy | **Second Order Upwind** |
| **Pseudo Time Method** | **OFF** |
| Warped-Face Gradient Correction | ON |

### Solution Controls
| Control | Value |
|---|---|
| **Flow Courant Number** | **200** |
| Explicit RF — Momentum | 0.5 |
| Explicit RF — Pressure | 0.5 |
| URF — Density / Body Forces / Turb Visc / Energy | 1 |
| URF — k / ω | 0.8 |

> [!important] Why "Pseudo Time OFF" is correct here
> Coupled scheme + **Flow Courant 200 IS the (implicit) time advancement** — it's already pseudo-transient in effect, and aggressive. Turning ON the *explicit* Pseudo Time Method with a conservative timescale (0.5) slows advancement dramatically → at iter 100 the flow still hasn't developed → fan reverse flow won't clear → continuity stuck flat. That's what stalled the experimental run. Courant 200 develops the flow fast → reverse flow clears ~15 iters.

---

## Initialization + Patching

1. **Standard Initialization**, Compute from an inlet/wall, Temperature = **309.16 K**
2. Initialize
3. **Patch** (Solution → Initialization → Patch):
   - Fluid zones (enclosure + fan-vol): T = **309.16 K**
   - IGBT die solid: T = **350 K**
   - HS solid + baseplate: T = **320 K**
   - (thermal paste ~335 K)

> [!warning] Why patching is mandatory
> The IGBT source dumps its power into a tiny die volume. Without a realistic starting field:
> - **Thermal shock** — die T jumps hundreds of K in iter 1 → energy residual spikes → limiter fires → divergence.
> - **Wrong gradient direction** — HS starting at ambient while "cooled" by ambient air confuses the solver (reverse heat flow early).
> - **Wasted iters** — starting IGBT at 300 K when steady is ~380 K = hundreds of iters just heating up.
>
> Estimate: `T_patch ≈ T_amb + P_loss × R_thermal_guess`. IGBT: 309 + 750×0.05 ≈ 350. HS: 309 + 750×0.015 ≈ 320. ±20 K is fine.
>
> Verify with a Temperature contour **before** iterating — should show hot IGBT / warm HS / cool air, not uniform 300 K.

---

## Cell Zone Conditions (heat source)

| Zone | Material | Source |
|---|---|---|
| Fluid enclosure | air36 | — |
| Fluid fan-vol | air36 | 3D Fan Zone |
| Solid HS / baseplate | LM25 Al (k=150, cp=871, ρ=2670) | — |
| Solid IGBT die | Si / datasheet | **Energy source = P_loss/V_die [W/m³]** |
| Thermal paste (Fasto) | k = 1.1 | — |

> [!tip] Fluent expression for the source (unit tag mandatory)
> `750 [W] / Volume("igbt-die-zone")` — the `[W]` tag is required for unit consistency.

---

## Monitors (set BEFORE running)

- T_IGBT — volume-weighted avg on die
- T_HS_base — area-weighted avg on fin-root surface
- h_HS (y+ based) — area avg on all HS wetted surfaces
- h_dead_zone vs h_active_zone — split by named selections
- Mass flow through fan-in-int
- Energy imbalance — all zones (should → 0)

Enable **autosave** (every 100 iters, keep last 3) before Calculate.

---

## Convergence Criteria

| Residual | Target |
|---|---|
| Continuity, velocities, k, ω | 1e-4 |
| **Energy** | **1e-6** |

Real check = **report values plateau** (T_IGBT Δ < 0.1 K over 50 iters) **AND energy imbalance < 1% of input power**. Residuals alone aren't sufficient.

> [!note] Diagnostic signature
> Continuity flat-high + energy already low (1e-8) + everything else low = **flow field not developing** (fan / BC / timescale), NOT a thermal problem. Fix the flow side, don't touch the thermal setup.

---

## Concept Appendix

### Boussinesq approximation
Treats density as constant everywhere **except** in the gravity/buoyancy term, where it varies linearly: ρ = ρ₀[1 − β(T−T₀)]. Cheap, stable, ideal when buoyancy is a secondary effect (low Ri). β = 1/T_ref for an ideal gas.

### Richardson number (Ri = Gr/Re²)
Ratio of buoyancy to inertial forces. Ri << 1 → forced-dominated (my case). Ri >> 1 → natural-dominated. Ri ~ 1 → true mixed. Low Ri is *why* boussinesq's buoyancy-term error is negligible here.

### Sutherland's law
Kinetic-theory-based μ(T). T^(3/2) from the Maxwell-Boltzmann speed distribution; the (T_ref+S)/(T+S) factor corrects for molecular attraction. Valid for air 100–1900 K. Preferred over piecewise-linear: physical, extrapolates safely, near-free.

### Cp, k, μ, MW (one-liners)
- **Cp** [J/kg·K] — energy to warm 1 kg by 1 K; sets airflow needed for heat removal (ṁ·cp·ΔT). Air ~1007, ~constant.
- **k** [W/m·K] — fluid's own conduction; sets h via the wall gradient and Nu = hL/k. Dominates h at low Re (dead zone).
- **μ** [kg/m·s] — resistance to shear; sets boundary-layer thickness and Re = ρUL/μ.
- **MW** [kg/kmol] — 28.966 for dry air; T-independent; only relevant to ideal-gas / kinetic-theory (not this boussinesq run).

---

## Method Principle (hard-learned)

> [!important] Change ONE thing at a time — physics OR solver, never both
> I broke this by swapping density model **and** solver together → couldn't tell which caused the stall. To test a new physics model: keep the proven solver, swap only the model, and compare fairly (both converged). A "purer" model that won't converge is worse than a simpler validated one.

---

## Action Checklist

- [x] Material: boussinesq 1.145, β 0.00323457, Cp 1007, k 0.02627, μ sutherland
- [x] Operating: gravity ON, Op Temp 309.16, specified ρ_op 1.145, ref-P loc (0, 0.53345, 0.01298)
- [x] Solver: Coupled + PRESTO! + 2nd order, Pseudo-time OFF, Courant 200, k-ω SST
- [ ] Reference Values: Temperature → 309.16, Reference Zone → fluid
- [ ] IGBT energy source entered (P_loss/V_die with [W] tag)
- [ ] Fan curve loaded; rotational direction verified
- [ ] Std init 309.16 → patch IGBT 350 / HS 320
- [ ] Monitors + autosave set
- [ ] Run 100 → confirm reverse flow clears ~15 iters → continue to convergence
- [ ] Post-convergence: check actual y+ → set Yplus-for-HTC → report h per zone → feed Cauer R_conv
- [ ] Verify energy balance Σq″_out ≈ P_IGBT_in

## Promotion checklist (before flipping status: promoted)
- [ ] Definition is generalizable, not project-specific
- [ ] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[CFD]]`, `[[Heat Transfer]]`)
- [ ] Sources cited

## Atlas Connections
- [[CFD]]
- [[Heat Transfer]]
- [[Thermal Management]]
