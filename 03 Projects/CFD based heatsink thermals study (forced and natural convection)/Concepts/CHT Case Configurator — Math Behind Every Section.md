---
concept: CHT Case Configurator Math
project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: incubating
created: 2026-09-01
sources: ["[[Daily Log#2026-09-01]]"]
extracted_from: []
tags: [ETM, CFD, CHT, dimensionless-numbers, convection, tool-docs, second-brain]
related: ["[[CHT Case Configurator]]", "[[MC Heatsink CHT — Consolidated Setup]]", "[[MC_HS_ETM_I1]]"]
---

# CHT Configurator — The Math, Section by Section

> [!abstract] What this note is
> The theory under the [[CHT Case Configurator]] tool. Every section explained intuition-first, then the equation, then a worked example using the **default case**: T∞ = 36 °C, Tw = 110 °C, L = 0.05 m, U = 3 m/s. All intermediate arithmetic shown so future-me can re-derive or debug any number the tool prints.

---

## Quick Start — What to Type Where

> [!tip] The 60-second version
> Only **4 inputs matter**: T∞, Tw, L, U. Everything else is computed. Sections 1–4 tell you how to set up the CFD *before* running; Section 5 is the only thing you touch *after* running.

### Inputs (left panel)

| Field | What it is | Enter | Default case |
|---|---|---|---|
| Ambient T∞ | air temp entering the sink (°C) | measured / spec ambient | 36 |
| Wall Tw | hottest HS surface temp (°C) | from CFD, or an estimate pre-run | 110 |
| Characteristic length L | streamwise sink length or fin height (m) | CAD | 0.05 |
| Forced velocity U | fan air speed over fins (m/s); **0 = no fan** | fan spec / CFD | 3 |
| Geometry | labels the hardware (routes h-estimate correlation) | Radial spider fins | spider |
| Buoyancy orientation | assisting unless flow fights gravity | assisting | assist |
| Gravity | leave ON for any buoyancy | on | on |

### What each output section is for

| § | Section | When | Meaning |
|---|---|---|---|
| 1 | Convection regime | before | Forced / mixed / natural, from Ri. The headline call. |
| 2 | Governing numbers | before | The dimensionless evidence behind the regime. Computed, not entered. |
| 3 | Recommended Fluent setup | before | The actual settings to use, each with its reason. Your setup checklist. |
| 4 | Pre-run h estimate | before | Rough h from correlations — sanity check only, can't see the dead zone. |
| 5 | Post-CFD h extractor | **after** | Paste Fluent per-zone data → h per zone + Cauer R_conv. |

### Section 5 inputs (after the run)

Per HS zone, read from Fluent: **q″** wall heat flux (W/m²), **T_wall** (°C), **T_ref** (°C — ambient or local near-wall), **Area** (m²). Output → h per zone, area-weighted h̄, and R_conv = 1/(hA) for [[MC_HS_ETM_I1]].

### One-line flow

Sections 1–4 = *before* CFD (how to set it up) → run Fluent → Section 5 = *after* CFD (turn results into the 1D model).

---

## 0. The Property Engine (runs before everything)

### Film temperature — where properties are evaluated

> [!note] Intuition
> Air near a 110 °C wall isn't at 110 °C, and air far away isn't the only thing that matters either. The heat transfer happens *inside the boundary layer*, where the temperature is somewhere between wall and freestream. So we evaluate fluid properties at the **average of the two** — the film temperature. It's the single-temperature stand-in for "the air that's actually doing the convecting."

$$T_f = \frac{T_w + T_\infty}{2}$$

**Worked (default case):**
$$T_f = \frac{110 + 36}{2} = 73\ °C = 346.15\ \text{K}$$

Every property (ρ, cp, k, μ) is looked up at 73 °C, not at ambient or wall.

### Table interpolation

The tool holds an air table (−50 to 200 °C at 1 atm) and linearly interpolates between the two bracketing rows. For T_f = 73 °C it sits between the 60 °C and 80 °C rows, fraction f = (73−60)/(80−60) = 0.65:

| Prop        | @60 °C    | @80 °C   | @73 °C (f=0.65) |
| ----------- | --------- | -------- | --------------- |
| ρ (kg/m³)   | 1.059     | 0.9994   | **1.020**       |
| cp (J/kg·K) | 1007      | 1008     | **1007.7**      |
| k (W/m·K)   | 0.02808   | 0.02953  | **0.02902**     |
| μ (kg/m·s)  | 2.008e -5 | 2.096e-5 | **2.065e-5**    |

Derived on the fly:
$$\nu = \frac{\mu}{\rho} = \frac{2.065\text{e-}5}{1.020} = 2.025\text{e-}5\ \text{m}^2/\text{s}$$
$$\alpha = \frac{k}{\rho c_p} = \frac{0.02902}{1.020 \times 1007.7} = 2.823\text{e-}5\ \text{m}^2/\text{s}$$
$$\beta = \frac{1}{T_{f,K}} = \frac{1}{346.15} = 2.889\text{e-}3\ \text{K}^{-1}$$

(β = 1/T is the ideal-gas thermal expansion coefficient — the same β you enter for Boussinesq, here evaluated at film temp.)

---

## Section 1 — Convection Regime

This is the hero. It answers one question: **is heat leaving by forced flow, by buoyancy, or both?** The whole downstream setup depends on the answer.

### The Richardson number — the classifier

> [!note] Intuition
> Two things can move hot air away from the heatsink: the **fan pushing it** (inertia) and **hot air rising on its own** (buoyancy). Richardson number is literally the ratio of those two. If the fan wins by a mile, buoyancy is a rounding error and you can be sloppy about the buoyancy model. If buoyancy wins, you'd better model it carefully. Ri tells you which world you're in.

$$Ri = \frac{Gr}{Re^2} = \frac{\text{buoyancy forces}}{\text{inertial forces}}$$

**Classification thresholds (what the spectrum bar encodes):**

| Ri | Regime | Meaning |
|---|---|---|
| Ri < 0.1 | **Forced-dominated** | Fan carries essentially all the heat |
| 0.1 ≤ Ri ≤ 10 | **Mixed** | Both matter; dead zone leans natural |
| Ri > 10 (or no fan) | **Natural-dominated** | Buoyancy sets the heat transfer |

**Worked (default case):**
$$Ri = \frac{Gr}{Re^2} = \frac{6.39\text{e}5}{(7409)^2} = \frac{6.39\text{e}5}{5.49\text{e}7} = 0.0116$$

0.0116 < 0.1 → **FORCED-DOMINATED**. The marker sits near the left (cyan) end of the spectrum. (Gr and Re computed in Section 2 below.)

### Why this single number drives everything

> [!important] The corrected Boussinesq insight
> Because Ri = 0.0116 << 1, buoyancy is a **minor term** in the momentum balance. That means the Boussinesq density linearisation — even though ΔT/T∞ = 0.24 is "too large" by the textbook rule — introduces negligible error, because the term it approximates barely contributes. **The validity of a buoyancy model scales with how much buoyancy matters.** This is why the validated Boussinesq baseline is correct for the MC heatsink despite the big ΔT.

### Marker position (how the bar is drawn)

The spectrum is logarithmic in Ri from 0.01 to 100. The marker's horizontal position:

$$\text{pct} = \frac{\log_{10}(Ri) - \log_{10}(0.01)}{\log_{10}(100) - \log_{10}(0.01)} \times 100\%$$

For Ri = 0.0116: pct = (log 0.0116 − log 0.01)/(log100 − log0.01) × 100 = (−1.936 + 2)/4 × 100 = **1.6%** → hard left, deep in forced territory.

---

## Section 2 — Governing Numbers

Each dimensionless group, intuition → formula → default-case value.

### Reynolds number — Re

> [!note] Intuition
> Ratio of "shoving" (inertia) to "stickiness" (viscosity). High Re → flow has momentum, tends turbulent, thin boundary layers. Low Re → viscosity dominates, laminar, thick sluggish layers.

$$Re = \frac{\rho U L}{\mu} = \frac{U L}{\nu}$$

**Worked:**
$$Re = \frac{1.020 \times 3 \times 0.05}{2.065\text{e-}5} = \frac{0.153}{2.065\text{e-}5} = 7.41\text{e}3$$

7410 is well below the flat-plate transition (5e5) → the *bulk* approach is laminar, though a real fan jet is locally turbulent (why the tool still recommends SST).

### Prandtl number — Pr

> [!note] Intuition
> How fast momentum diffuses vs how fast heat diffuses in the fluid. Pr ≈ 1 for gases means the velocity boundary layer and thermal boundary layer are about the same thickness — so a mesh that resolves one resolves the other. (Liquids: Pr >> 1, thin thermal layer. Liquid metals: Pr << 1.)

$$Pr = \frac{\nu}{\alpha} = \frac{\mu c_p}{k}$$

**Worked:**
$$Pr = \frac{2.065\text{e-}5 \times 1007.7}{0.02902} = \frac{0.02081}{0.02902} = 0.717$$

Air is ~0.71 across the whole range — the δ ≈ δt property you rely on for inflation-layer sizing.

### Grashof number — Gr

> [!note] Intuition
> The buoyancy version of Reynolds. It's the ratio of the buoyant "lift" on hot fluid to the viscous drag holding it back. Big Gr → strong natural convection currents.

$$Gr = \frac{g\, \beta\, \Delta T\, L^3}{\nu^2}$$

**Worked:**
$$Gr = \frac{9.81 \times 2.889\text{e-}3 \times 74 \times (0.05)^3}{(2.025\text{e-}5)^2}$$

Numerator: 9.81 × 2.889e-3 = 0.02834; × 74 = 2.097; × 1.25e-4 = 2.621e-4
Denominator: (2.025e-5)² = 4.101e-10

$$Gr = \frac{2.621\text{e-}4}{4.101\text{e-}10} = 6.39\text{e}5$$

### Rayleigh number — Ra

> [!note] Intuition
> Ra = Gr·Pr. It's the master switch for natural convection: it decides whether buoyant flow even starts, and later whether the plume is laminar or turbulent (transition around Ra ≈ 1e9).

$$Ra = Gr \cdot Pr$$

**Worked:**
$$Ra = 6.39\text{e}5 \times 0.717 = 4.58\text{e}5$$

4.58e5 << 1e9 → any natural convection here would be laminar (but we're forced-dominated anyway).

### Richardson number — Ri

Covered in Section 1. $Ri = Gr/Re^2 = 0.0116$.

### Temperature ratio — ΔT/T∞

> [!note] Intuition
> The Boussinesq validity gauge. Boussinesq assumes density varies little; this ratio measures how hard that assumption is being pushed. Textbook cutoff ~0.1 — but see the Section 1 caveat: it only bites when buoyancy matters.

$$\frac{\Delta T}{T_\infty} = \frac{T_w - T_\infty}{T_{\infty,K}}$$

**Worked:**
$$\frac{74}{309.15} = 0.239$$

Above 0.1 → the tool flags property variation (Sutherland μ), but keeps Boussinesq because Ri is tiny.

### Mach number — Ma

> [!note] Intuition
> Speed relative to the speed of sound. Ma < 0.3 → incompressible, no acoustics to worry about. For fan-cooled air it's always tiny.

$$Ma = \frac{U}{a} \approx \frac{U}{343}$$

**Worked:** 3/343 = **0.0087** → firmly incompressible, justifies the pressure-based / incompressible density models.

---

## Section 3 — Setup Advisor (threshold logic)

Each recommendation fires off a specific number crossing a specific threshold. Here's the decision tree the tool encodes.

### Density model

```
if Ri < 0.1            → Boussinesq         (buoyancy minor, linearisation error negligible)
elif ΔT/T∞ < 0.1       → Boussinesq         (density variation genuinely small)
else                   → Boussinesq(validated) OR incompressible-ideal-gas
                          + warning: ideal-gas couples to fan source, can destabilise
```

Default case → Ri 0.0116 < 0.1 → **Boussinesq**, clean.

### Viscosity / conductivity

```
if ΔT/T∞ > 0.1  → Sutherland μ  (μ varies ~ΔT/T∞ × 80%; near-free, physical)
                → k constant @ T_f (defensible) or kinetic-theory
else            → all constant @ T_f
```

Default → 0.239 > 0.1 → **Sutherland μ**, constant k. (The exact hybrid on your validated run.)

### Viscous model

```
if U>0 and Re ≥ 1e5   → k-ω SST (turbulent, auto y+)
elif U>0              → k-ω SST (fan jet locally turbulent even if bulk Re low)
else (natural)        → Laminar if Ra<1e9, else k-ω SST
```

Default → fan present → **k-ω SST**. (Never Laminar for a fan-cooled heatsink, even though bulk Re=7410 looks laminar — the flat-plate tutorial's Laminar choice does *not* transfer.)

### Pressure scheme

```
if Ra>1e8 or U>0  → PRESTO! (or Body-Force-Weighted)
else              → Body-Force-Weighted
```

Default → fan swirl → **PRESTO!** (your validated choice).

### Solver (the hard-learned rule — fixed, not conditional)

> [!important] Always: Coupled · Flow Courant ≈ 200 · Pseudo-time OFF
> Coupled + Courant 200 already *is* an implicit time advance and develops the flow fast, so fan reverse-flow clears in ~15 iters. Turning on the explicit Pseudo Time Method with a conservative timescale slows advancement → flow never develops → continuity stalls flat. This is baked in as a constant recommendation because it cost a wrecked run to learn.

### Radiation

```
if Tw>200°C or (no fan and natural)  → consider S2S/DO
else                                 → off (<5% of total with forced air)
```

Default → Tw 110 °C + forced → **off**.

---

## Section 4 — Pre-run h Estimate

Turns the regime + numbers into a ballpark heat transfer coefficient, via Nusselt correlations, then h = Nu·k/L. **Cross-check only** — no correlation captures the dead-zone recirculation.

### The bridge: Nusselt → h

> [!note] Intuition
> Nu is the non-dimensional heat transfer coefficient — the ratio of convective to pure-conductive heat transfer across the fluid layer. Once you have Nu from a correlation, you scale it back to a physical h using the fluid conductivity and the length.

$$Nu = \frac{hL}{k} \quad\Rightarrow\quad h = \frac{Nu \cdot k}{L}$$

### Forced — flat plate (default case path)

Laminar average (Re < 5e5):
$$Nu = 0.664\, Re^{1/2}\, Pr^{1/3}$$

Turbulent average (Re ≥ 5e5): $Nu = 0.037\,Re^{0.8}Pr^{1/3}$

**Worked (default, laminar):**
$$Nu = 0.664 \times \sqrt{7410} \times 0.717^{1/3} = 0.664 \times 86.08 \times 0.895 = 51.2$$
$$h = \frac{51.2 \times 0.02902}{0.05} = \frac{1.486}{0.05} = 29.7\ \text{W/m}^2\text{·K}$$

So ~30 W/m²·K — a sensible forced-air ballpark. (Your CFD y+-based h per zone will differ, especially the dead zone — that's expected and is the point.)

### Natural — Churchill–Chu vertical plate (Ra ≤ 1e9)

$$Nu = 0.68 + \frac{0.670\, Ra^{1/4}}{\left[1 + (0.492/Pr)^{9/16}\right]^{4/9}}$$

### Cylinder in crossflow — Churchill–Bernstein

$$Nu = 0.3 + \frac{0.62\,Re^{1/2}Pr^{1/3}}{\left[1+(0.4/Pr)^{2/3}\right]^{1/4}}\left[1+\left(\frac{Re}{282000}\right)^{5/8}\right]^{4/5}$$

### Mixed — Churchill combination

> [!note] Intuition
> When both modes matter, you don't just add the h's. You combine the Nusselt numbers in cubes (an empirical blend that captures how the two boundary layers interact). Plus sign when buoyancy assists the flow, minus when it opposes.

$$Nu_{mixed} = \left(Nu_{forced}^3 \pm Nu_{natural}^3\right)^{1/3}$$

- **+** assisting (buoyancy and forced flow same direction → enhances)
- **−** opposing (buoyancy fights forced flow → reduces)

> [!warning] Why this is a ballpark, not truth
> These correlations assume clean geometry and undisturbed approach flow. The fan dead-zone recirculation, fin-channel confinement, and non-uniform approach velocity are exactly what they can't represent. Use this for order-of-magnitude sanity ("is my CFD h in the right ballpark?"), never as a target. The real per-zone h comes from the y+-based surface HTC on the solved field.

---

## Section 5 — Post-CFD h Extractor

The bridge from converged CFD back to the 1D Cauer model. Closes **Open Item #3**.

### Per-zone h from wall data

> [!note] Intuition
> Newton's law of cooling, inverted. You measured (in CFD) how much heat leaves each patch of surface (q″) and the temperature difference driving it (T_wall − T_ref). Divide → the local heat transfer coefficient for that zone.

$$h_{zone} = \frac{q''}{T_{wall} - T_{ref}}$$

**Worked (example zones):**

| Zone | q″ (W/m²) | Tw (°C) | Tref (°C) | ΔT | h = q″/ΔT | A (m²) |
|---|---|---|---|---|---|---|
| fan_active | 4200 | 88 | 52 | 36 | **116.7** | 0.0180 |
| dead_zone | 1500 | 104 | 71 | 33 | **45.5** | 0.0060 |
| side_fins | 2600 | 95 | 58 | 37 | **70.3** | 0.0090 |

Note the dead zone's h (45.5) is less than half the fan-active zone (116.7) — the whole reason for resolving zones separately. A single lumped h would smear this out and mispredict the local IGBT-adjacent temperature.

> [!important] T_ref choice matters
> If you feed **local near-wall fluid temp** (from the y+-based method) as T_ref, h is the true local coefficient. If you feed **far-field ambient**, h is referenced to ambient and will read lower in the dead zone (bigger ΔT denominator). Be consistent with what your Cauer R_conv expects.

### Area-weighted average

> [!note] Intuition
> To collapse many zones into one number, you can't just average the h's — a tiny hot patch shouldn't count as much as a big one. Weight each h by its area.

$$\bar{h} = \frac{\sum h_i A_i}{\sum A_i}$$

**Worked:**
$$\sum h_i A_i = 116.7(0.018) + 45.5(0.006) + 70.3(0.009) = 2.101 + 0.273 + 0.632 = 3.006$$
$$\sum A_i = 0.018 + 0.006 + 0.009 = 0.033\ \text{m}^2$$
$$\bar{h} = \frac{3.006}{0.033} = 91.1\ \text{W/m}^2\text{·K}$$

### Total heat rate (energy-balance check)

$$Q = \sum q''_i A_i = 4200(0.018) + 1500(0.006) + 2600(0.009) = 75.6 + 9.0 + 23.4 = 108\ \text{W}$$

Compare this against P_IGBT you injected — if they don't match within ~1%, the run isn't energy-converged.

### Convective resistance → Cauer branch

> [!note] Intuition
> Your Simulink Cauer model speaks in thermal resistances [K/W], not h. Convert each zone's h·A into a resistance — that's the R_conv branch from that surface node to the ambient node.

$$R_{conv,zone} = \frac{1}{h\, A}$$

**Worked (fan_active):**
$$R_{conv} = \frac{1}{116.7 \times 0.018} = \frac{1}{2.101} = 0.476\ \text{K/W}$$

Lumped (single branch):
$$R_{conv,total} = \frac{1}{\bar{h}\,A_{total}} = \frac{1}{91.1 \times 0.033} = \frac{1}{3.006} = 0.333\ \text{K/W}$$

The tool prints these as a copy-paste block ready for [[MC_HS_ETM_I1]].

---

## Quick Cross-Reference — Number → Decision

| Number | Threshold | Drives |
|---|---|---|
| Ri = Gr/Re² | 0.1 / 10 | Regime + density model |
| ΔT/T∞ | 0.1 | Property variation (Sutherland, kinetic-theory) |
| Re | 5e5 (plate) | Laminar vs turbulent Nu; viscous model |
| Ra = Gr·Pr | 1e9 | Natural-convection turbulence; pressure scheme (1e8) |
| Pr | ≈1 for air | δ ≈ δt → mesh/inflation sizing |
| Ma | 0.3 | Incompressible assumption |

## Method Principle (carried from the wrecked run)

> [!important] Change ONE thing at a time
> The tool separates *physics* recommendations (density, properties, viscous model) from the *solver* recommendation (Coupled/Courant/pseudo-time) precisely because mixing both at once made a stalled run undiagnosable. When testing a new physics model, hold the proven solver fixed and swap only the model — compare fairly, both converged.

---

## To extend later (v0.2 hooks)

- **Fluid library** — replace the single air table with a fluid selector (water, glycol, oil) for liquid cold plates; every downstream number already reads from the property object.
- **Fin-array Nu** — add a proper interrupted-fin / pin-fin correlation instead of the flat-plate proxy.
- **Simulink export** — format the R_conv block to match the exact R-network node naming in [[MC_HS_ETM_I1]].
- **Ra-based mesh y+ target** — suggest first-cell height from the regime so the y+-for-HTC is right on the first run.

## Atlas Connections
- [[CFD]]
- [[Heat Transfer]]
