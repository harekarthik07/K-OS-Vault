---
type: result
project: ETM For Heatsink and IGBT
phase: Phase 1
title: "T30 MC ETM — Part 1: Thermal Budget & Parameter Derivation"
model: "[[MC_HS_ETM_I2]]"
component: "[[HS_I1-G1-K1]]"
status: closed
validated: 11 dyno runs (37–63), 356–492 W, ≤300 s
date: 2026-09-15
tags: [thermal, ETM, cauer, heatsink, IGBT, T30, calibration]
related:
  - "[[00 Home]]"
  - "[[Cauer Model Calibration — fit what you cannot derive]]"
  - "[[IGBT Electro-Thermal Loss Modelling]]"
  - "[[Heatsink Thermal RLC Network]]"
  - "[[Thermal Resistance model of Heatsink With IGBT]]"
  - "[[MC Heatsink CHT — Consolidated Setup]]"
---

# Part 1 — Thermal Budget & Parameter Derivation

> [!abstract] One-line summary
> A 1D two-node Cauer model of the T30 motor-controller heatsink, with **every resistance derived from datasheet, CAD, or correlation** and **exactly one calibrated parameter (h)**, validated against 11 dyno runs to ~2 K with no load-dependent residual.

---

## 0. Objective

Determine whether the T30 MC heatsink holds the IGBT below its **95 °C deration threshold** under the real duty: **4 minutes at peak output, 60 km/h speed-locked**.

**Why a 1D model at all:** to reduce — not eliminate — dependency on CFD. The 1D model screens the design space fast; CFD confirms specific candidates.

**Why transient, not steady state:** tests run 240 s against a dominant time constant of ~394 s. The system reaches under half its eventual temperature. A steady-state analysis would answer a question nobody asked. All dyno runs and the Fluent transient use the same 4-minute basis.

---

## 1. Final parameter table

| Block | Parameter | Value | Unit | Source | Status |
|---|---|---|---|---|---|
| `Rjc` | R | **0.02679** | K/W | Infineon FS200R07PE4, 6 IGBT ∥ 6 diode | derived |
| `Rcase-hs` | R | **0.00818** | K/W | Datasheet RthCH 0.009 × (1.0/1.1) | derived |
| `Rhs` | R | **0.03190** | K/W | L/(kA) 0.01313 + Yovanovich 0.01877 | derived |
| `Rconv,lat` | area | **0.232** | m² | CAD total external surface area | measured |
| `Rconv,lat` | h | **29.59** | W/m²K | 11-run calibration | **fitted** |
| `IGBT-Juntion Mass` | mass | **0.56264** | kg | CAD (ρ = 2700) | measured |
| `IGBT-Juntion Mass` | cp | **871** | J/kgK | A356 | material |
| `Chs` | mass | **2.75978** | kg | CAD (3.32242 − 0.56264) | measured |
| `Chs` | cp | **871** | J/kgK | A356 | material |
| `Temperature Source2/3` | T | `T_amb` | °C | per-run, auto from spreadsheet | measured |
| Model | StopTime | `t_end` | s | per-run, auto from spreadsheet | measured |

**Derived quantities:**

```
R_series (below NTC node) = 0.00818 + 0.03190           = 0.04008 K/W
R_conv                    = 1/(29.59 × 0.232)           = 0.14567 K/W
R_total (NTC → air)                                     = 0.18575 K/W

C_plate = 0.56264 × 871 =  490 J/K
C_hs    = 2.75978 × 871 = 2404 J/K

τ1 ≈ 19 s    τ2 ≈ 394 s
```

> [!important] Only one parameter is fitted
> `h = 29.59` is the sole calibrated value. Everything else comes from a datasheet, CAD measurement, or a published correlation. CFD independently gives area-weighted h = 34.3 — a 16 % agreement between two independent methods.

---

## 2. Model topology

```
        Q = P_inv (all inverter losses)
        ↓
   ┌──────────────┐  ← T_junction  (ESTIMATED, no sensor)
   └──────────────┘
        │ Rjc = 0.02679          junction → case
   ┌──────────────┐  ← T_sim      (predicts the CAN NTC)
   │ C = 490 J/K  │
   └──────────────┘
        │ Rcase-hs = 0.00818     case → heatsink (incl. TIM)
        │ Rhs      = 0.03190     conduction + spreading
   ┌──────────────┐  ← T_fin      (heatsink node)
   │ C = 2404 J/K │
   └──────────────┘
        │ Rconv = 1/(h·A)        heatsink → air
       T_amb
```

**Signal meanings — this matters:**

| Signal | Measured? | What it is |
|---|---|---|
| `T_mes` | ✅ yes | The real CAN NTC reading, from the run's spreadsheet |
| `T_sim` | ❌ no | Model's **prediction of that CAN reading**. Calibration target |
| `T_junction` | ❌ no | `T_sim + Q × RthJC`. Estimate, no validation data |
| `T_fin` | ❌ no | Heatsink node. Valid as a single lump because Bi = 0.004 |

---

## 3. Section-by-section derivation

### 3.1 Rjc — junction to case = 0.02679 K/W

Datasheet gives **per-device** values; the FS200R07PE4 is a six-pack with all 12 dice on one baseplate, so their paths are thermally **parallel** and conductances add:

```
6 IGBTs : 6 / 0.25 = 24.00 W/K
6 diodes: 6 / 0.45 = 13.33 W/K
                     ─────────
                     37.33 W/K   →  RthJC = 0.02679 K/W
```

> [!check] The method validates against a published number
> Applying the identical reduction to the case-to-heatsink values:
> `6/0.084 + 6/0.15 = 111.43 W/K → 0.00897`, and the datasheet's own module row says **0.009**. ✅
> Second check: the Foster network on the ZthJC curve sums to `0.015+0.0825+0.08+0.0725 = 0.25` = per-IGBT RthJC. ✅

**Assumption:** losses split between IGBTs and diodes in proportion to conductance. In a *motoring* inverter the IGBTs carry more, so IGBT-only would give `0.25/6 = 0.04167` (+56 %). **Use 0.04167 for any safety claim.**

**No capacitance on this node:** the datasheet Foster time constants are `[0.01, 0.02, 0.05, 0.1] s` — all under 0.1 s against a 240 s test. The chip equilibrates instantly at this timescale.

### 3.2 Rcase-hs — case to heatsink = 0.00818 K/W

Datasheet `RthCH = 0.009 K/W per module`, defined **with λ_paste = 1.0 W/mK already in place**. Raptee uses Fasto at **1.1 W/mK**:

```
R_ch = 0.009 × (1.0 / 1.1) = 0.00818 K/W
```

> [!warning] The TIM is inside RthCH — do not add it twice
> `RthCH` is not "case to paste". It is **case, through the paste, to the heatsink surface**. The old model had a separate `Rthp = 0.00999` in series with it, double-counting the same grease layer. The spec sheet had flagged this: *"Don't add separately if using RthCH."*
> Confirmed: no gap pad or insulator is used — paste only. So no extra layer is needed.

### 3.3 Rhs — heatsink conduction + spreading = 0.03190 K/W

**Term 1 — 1D conduction**

```
R_cond = L / (k · A_contact)
       = 0.018 / (150.624 × 0.00909815)
       = 0.013135 K/W
```

**Term 2 — spreading resistance** (Lee/Yovanovich, isoflux circular source on finite plate)

Heat enters over the IGBT footprint (0.0091 m²), not the whole base (0.0343 m²). The constriction is real and calculable.

```
A_base = 154.36 × 222.21 mm = 0.034300 m²      ← from CAD

1.  a = √(A_src/π)  = √(0.00909815/π) = 0.05381 m
    b = √(A_base/π) = √(0.034300/π)   = 0.10449 m

2.  ε = a/b = 0.5150          relative source size
    τ = t/b = 0.018/0.10449 = 0.1723

3.  Bi = h·b/k = 29.59 × 0.10449 / 150.624 = 0.02053

4.  λ  = π + 1/(ε√π) = 3.1416 + 1/(0.5150 × 1.7725) = 4.2371

5.  λτ = 0.7299  →  tanh(λτ) = 0.6230 ,  λ/Bi = 206.4
    φc = (0.6230 + 206.4) / (1 + 206.4 × 0.6230) = 1.5978

6.  (1−ε)^1.5 = 0.33774
    ψ = ½ × 0.33774 × 1.5978 = 0.2698

7.  k·a·√π = 150.624 × 0.05381 × 1.7725 = 14.3672
    R_sp = 0.2698 / 14.3672 = 0.01877 K/W
```

```
Rhs = 0.013135 + 0.018770 = 0.03190 K/W
```

> [!note] The correlation is insensitive to h — no circularity
> Because `λ/Bi ≈ 206 ≫ 1`, both terms of φc are dominated by it and it nearly cancels: `φc → 1/tanh(λτ) = 1.6051` vs. computed 1.5978, a 0.5 % difference.
> Sweeping h from 10 → 150 moves R_sp by **1.6 %**. So using the calibrated h to compute a resistance that partly justifies the calibration is harmless here.
> `Bi ≪ 1` means the **adiabatic-edge limit** — the base spreads heat far faster than convection removes it, so R_sp is set by geometry and k alone. **A_base is the only sensitive input**, which is why measuring it from CAD mattered.

### 3.4 Rconv — heatsink to air = 0.14567 K/W

```
R_conv = 1 / (h · A_fin) = 1 / (29.59 × 0.232) = 0.14567 K/W
```

**CAD surface areas:**

| Surface | Area (mm²) | Area (m²) |
|---|---|---|
| Total external (TSA) | 231 955 | **0.2320** |
| Fins | 63 850 | 0.0639 |
| Bottom | 14 902 | 0.0149 |
| Fins + bottom | 78 752 | 0.0788 |
| Side / outer walls (remainder) | 153 203 | 0.1532 |

All of the 0.232 m² is **external** — no internal faces included.

**CFD cross-check (Fluent, MC cooling fan, 36 °C domain):**

```
hs-fins-wall  : h = 33.23 , A = 0.06272 m²  →  hA = 2.084 W/K
hs-bottom     : h = 39.03 , A = 0.01491 m²  →  hA = 0.582 W/K
                                  area-weighted h = 34.3 W/m²K
```

Fitted h = 29.59 vs CFD 34.3 → **16 % apart**, dyno lower. **Direction is correct**: the dyno had **no road-speed fan**, only the MC's own cooling fan, so real airflow was worse than CFD assumed.

> [!tip] Why the fins barely outperform the plain walls
> The CFD contour shows most fin-channel area sitting at **20–28 W/m²K** — the channels are flow-starved, with a clear dead zone at the central hub. Only rib junctions and leading edges reach 85–100.
> Implied h on the 0.1532 m² of plain outer wall is ~30, essentially equal to the fins. **That is a real finding about the design, not an inconsistency.**

### 3.5 Capacitances

```
C_plate = 0.56264 kg × 871 J/kgK =  490 J/K     IGBT-region heatsink material
C_hs    = 2.75978 kg × 871 J/kgK = 2404 J/K     rest of the sink
                                   ─────────
total mass                        3.32242 kg    ✅ matches CAD
```

**The two-node split is of one heatsink**, not sink-plus-separate-plate. `IGBT-Juntion Mass` is the 562.64 g of heatsink material directly under the IGBT — not the module's own baseplate.

Density check: `0.56264 / 208385 mm³ = 2700 kg/m³` ✅ · `3.32242 / 1235252 mm³ = 2690 kg/m³` ✅ — both consistent with A356.

**Lumped-capacitance validity:**

```
Bi = h·L/k = 29.59 × 0.018 / 150.624 = 0.0035  ≪ 0.1          ✅
diffusion time = L²/α = 0.018² / 6.45e-5 = 5 s  vs  τ2 = 394 s ✅ 78× separation
```

Heat crosses the base in 5 s; the sink takes ~394 s to heat up. Internally equilibrated at all times — lumping is justified.

---

## 4. The transient solution

### 4.1 Governing equations

Two nodes, energy balance at each (`θ = T − T_amb`):

```
C_p  · dθ₁/dt = Q − (θ₁ − θ₂)/R_s
C_hs · dθ₂/dt = (θ₁ − θ₂)/R_s − θ₂/R_c
```

### 4.2 State matrix and eigenvalues

```
A = [ −1/(R_s C_p)      1/(R_s C_p)          ]
    [  1/(R_s C_hs)   −(1/R_s + 1/R_c)/C_hs  ]

eig(A) = −0.0526 , −0.00254   →   τ1 ≈ 19 s , τ2 ≈ 394 s
```

> [!warning] Time constants are NOT the individual RC products
> A natural but wrong estimate is `τ2 = C_hs × R_conv = 2404 × 0.1457 = 350 s`. That ignores that the junction's 490 J/K **also discharges through the same convection path**.
> The correct value comes from the eigenvalues: **394 s**.
> Quick sanity estimate: `(C_p + C_hs) × R_c = 2894 × 0.1457 = 422 s` — same order, right mental model.

### 4.3 Physical meaning

| | Value | What it is |
|---|---|---|
| τ1 | ~19 s | Local heatsink metal under the IGBT equilibrating with the bulk |
| τ2 | ~394 s | Bulk sink dumping heat to the airstream — **dominates everything past a minute** |

At 240 s: `1 − e^(−240/394) = 46 %` risen. **The 4-minute test sees under half the eventual temperature.**

---

## 5. Validation results

`h = 29.59`, all 11 runs, fit window 150–200 s:

| idx | Run | Q (W) | gap (K) | wants h |
|---|---|---|---|---|
| 1 | 37 | 468 | +1.32 | 29.03 |
| 2 | 38 | 492 | +1.59 | 28.95 |
| 3 | 39 | 428 | +2.44 | 28.48 |
| 4 | 40 | 470 | +0.24 | 29.49 |
| 5 | 41 | 356 | +1.77 | 28.61 |
| 6 | 42 | 374 | +2.83 | 28.13 |
| 7 | 43 | 477 | +1.27 | 29.06 |
| 8 | 44 | 464 | +2.74 | 28.44 |
| 9 | 45 | 476 | +2.75 | 28.46 |
| 10 | 47 | 481 | +1.24 | 29.08 |
| 11 | 63 | 363 | +2.58 | 28.21 |

```
h spread : 28.13 – 29.49   (4.9 %)
RMSE     : 2.05 K
bias     : +1.89 K
```

> [!success] What "good" looks like here
> **h spread of 4.9 % across 11 runs** is the headline. The earlier version — which calibrated `Rhs` instead — spread **35 %** (0.0220–0.0314) on the same data. Same model, same runs; the difference is calibrating the right parameter.
> **Residual vs load shows no trend**: 356 W and 492 W sit in the same band. Nothing load-dependent is hiding inside h.

### 5.1 The residual bias is documented, not corrected

The +1.89 K is a **near-constant offset with no load dependence**, and it has a credible physical explanation:

The module NTC sits on the **DCB substrate**, electrically isolated, **partway up RthJC** — not at the baseplate. The model compares `T_sim` (the case node) against `T_mes` (a sensor a little higher up the chain), so `T_mes` legitimately reads hotter. Infineon publishes no junction-to-NTC resistance, so this cannot be quantified from the datasheet.

**Deliberately not corrected.** Pushing `Rhs` to ~0.036 would close it, but that converts a *derived* number back into a *fitted* one — exactly the mistake the restructure was undoing.

> [!quote] Standing principle
> Fit what you cannot derive. Derive what you can. Never bend a derived parameter to absorb an offset you can explain.

**The model is therefore ~2 K conservative against the CAN reading.** That is the safe direction.

---

## 6. Key takeaways

> [!important] The seven that matter
>
> **1. Convection is 78 % of the thermal budget.** `R_conv = 0.1457` of `R_total = 0.1858`. All the effort spent on `Rhs` moved a 17 % term. Real margin only ever comes from airflow.
>
> **2. Fit what you cannot derive.** `Rhs` is fully derivable (L/(kA) + Yovanovich). `h` is not, for this geometry. Calibrating `Rhs` gave a 35 % spread; calibrating `h` gave 4.9 % on identical data.
>
> **3. `R = ΔT/Q` only holds at steady state.** None of these runs reach it. The plateau equation under-predicted the required resistance by ~30 %, which is why manual bracketing beat the formula.
>
> **4. R and C are not independently identified by this data.** The fit constrains the **R·C product**. At the 150–200 s window, changing h by 3 % moves `T_sim` by **0.1 K** — h is nearly unidentifiable here. Its credibility comes from CFD, not from the fit.
>
> **5. Multi-node time constants require eigenvalues.** Per-branch `RC` under-predicts, because upstream capacitance also discharges through the downstream path.
>
> **6. Error shape diagnoses the cause.** Magnitude-wrong → resistance. Shape-wrong (tail, crossover) → capacitance. Widening with temperature → loss model. Constant offset appearing before the sink charges → series path, not convection.
>
> **7. The base thickness is already optimal.** Thicker base improves spreading but worsens conduction. Sweeping L: minimum `Rhs` at **18.1 mm**; the part is **18 mm**. (5 mm → 0.0611, 12 mm → 0.0346, **18 mm → 0.0319**, 30 mm → 0.0359, 50 mm → 0.0487.)

### 6.1 Debug ladder — reusable

1. **Budget every resistance from theory first.** Sum them. That is the prior.
2. **Fit.** Within ~15 % of theory → material/geometry uncertainty. Accept and document.
3. **Fitted is 2×+ theory** → a term is missing entirely (spreading, contact, fin efficiency). Find it, don't fit it.
4. **Fitted varies with load** → not a resistance problem. Loss model or h.
5. **Residual is shape-wrong, not magnitude-wrong** → capacitance, not resistance.

---

## 7. Errors found and corrected

| # | Error | Resolution |
|---|---|---|
| 1 | `Rhs = 0.0173` in the model file, untraceable | Replaced with derived 0.03190 |
| 2 | `Rhs = 0.00584` on spec sheet | Stale — not reproducible from current L/k/A. Rejected |
| 3 | Block named `Rjc` actually held RthCH | Renamed `Rcase-hs`; true RthJC added |
| 4 | `Rthp = 0.00999` double-counted the TIM | Removed — already inside RthCH |
| 5 | `T_amb` hardcoded, wrong per run | Auto-read from each run's spreadsheet via InitFcn |
| 6 | Run 63 diverged to 800 °C | StopTime was past the data end. Now `t_end` per run |
| 7 | `A_base` unknown, guessed at 0.024 m² | CAD: 0.0343 m². R_sp 0.01209 → 0.01877 |
| 8 | Masses not CAD-traceable | 0.56264 + 2.75978 = 3.32242 kg ✅ |
| 9 | Both scope outputs named `T_sim` | Renamed `T_junction` / `T_sim` |
| 10 | Calibrating `Rhs` instead of `h` | Restructured — spread 35 % → 4.9 % |

---

## 8. Validity envelope

> [!danger] Do not use outside this
> **Valid for:** CAN NTC temperature prediction · 356–492 W · ≤300 s · 34–41 °C ambient · dyno airflow (MC fan, **no ram air**).
>
> **Not validated for:**
> - **Anything past ~300 s.** τ2 ≈ 394 s, no run reaches steady state. Any steady-state figure is extrapolation resting on a CAD-derived C that was never measured — **no cooldown data exists**.
> - **Real riding.** Calibrated without ram air, so conservative on the road. Safe as a bound, wrong for accuracy work.
> - **`T_junction` as a real temperature.** Estimated, never measured, two known biases pushing opposite ways (see below).
> - **New fin geometries.** h is not predictive for a redesigned sink — that needs CFD.

### 8.1 T_junction health warning

```
T_junction = T_sim + Q × 0.02679
```

| Bias | Direction | Cause |
|---|---|---|
| Reads **high** | over-estimate | NTC already sits partway up RthJC; adding the full value double-counts |
| Reads **low** at high load | under-estimate | 0.02679 assumes conductance-proportional loss split. IGBT-only = 0.04167 (+56 %) |

They partly cancel, by an unknown amount. **Use 0.04167 for any safety claim.** The limit is `Tvj op = 150 °C` — **not** the 95 °C line, which is the *NTC deration* threshold.

---

## 9. Open items

| # | Item | Impact |
|---|---|---|
| 1 | No cooldown data anywhere in the dataset | C never independently measured. `Q = 0` decay is the only clean way |
| 2 | Junction-to-NTC resistance unpublished | The +1.89 K bias cannot be quantified or corrected |
| 3 | h not predictive for new fin designs | Blocks pure-1D design iteration; needs a CFD h-map |
| 4 | Run 43 (idx 7) starts ~50 s late | Trigger offset? Not blocking |
| 5 | Loss split IGBT vs diode not measured | Sets RthJC between 0.02679 and 0.04167 |
| 6 | CFD used 20 W/m²K wall BC on non-fin surfaces | Fitted data implies ~30. CFD may be conservative there |

---

## 10. MATLAB / Simulink infrastructure

**Model InitFcn** — per-run ambient and stop time, driven by `RUN_SEL`:

```matlab
mdl  = 'MC_HS_ETM_I2';
runs = [37 38 39 40 41 42 43 44 45 47 63];   % switch port order

idx = str2double(get_param([mdl '/RUN_SEL'],'Value'));
b   = find_system([mdl '/Inputs'],'regexp','on', ...
      'BlockType','FromSpreadsheet','Name',['^' num2str(runs(idx)) '_']);

f  = get_param(b{1},'FileName');
sh = get_param(b{1},'SheetName');
rg = get_param(b{1},'Range');

rows  = regexp(rg,'\d+','match');            % {'3','588'} from 'A3:E588'
T_amb = readmatrix(f,'Sheet',sh,'Range',sprintf('E%s:E%s',rows{1},rows{1}));
t_end = readmatrix(f,'Sheet',sh,'Range',sprintf('A%s:A%s',rows{2},rows{2}));

hws = get_param(mdl,'ModelWorkspace');
hws.assignin('T_amb', T_amb);
hws.assignin('t_end', t_end);

fprintf('Run %d | T_amb = %.2f degC | t_end = %.1f s\n', runs(idx), T_amb, t_end);
```

StopTime box = `t_end`. Column A = time, E = IGBT_Temp.

**`fit_h.m`** sweeps runs and reports the h each one wants:

```
R_conv_new = R_conv_old + gap/Q
h_new      = 1/(R_conv_new × A_fin)
```

> [!warning] Sign convention
> A **positive** gap (measured hotter than sim) needs **more** resistance → **lower** h. Inverted from the older `Rhs` version.

**Never auto-write the calibration.** Each run would overwrite the last and h would chase whichever run ran most recently. It is one constant across all runs — run the sweep, read the spread, set it by hand.

---

## 11. Next — Part 2

Turn the validated model into a **design tool**, built in Simulink (not a parallel MATLAB implementation — that would fork the validation).

| # | Objective | Feasible in 1D? |
|---|---|---|
| 1 | Effective base length L and required thermal mass | ✅ fully — optimum already found at 18.1 mm |
| 2 | How changing fin area and h helps or hurts | ◐ as an (h, A) contour map; h per geometry needs CFD |
| 3 | Fixed geometry response for a given heat input | ✅ fully, within the 4-min envelope |
| 4 | Interactive parameter window → Tj, T_IGBT, T_fin | ✅ via a masked subsystem |

**Approach:** mask `Subsystem1` with *geometry* parameters (L, A_contact, A_base, k, masses, h, A_fin). Mask initialization computes R_cond, R_spread, R_ch from them, so changing L in the dialog recomputes spreading automatically. Sweeps via `FastRestart`. App Designer only if live sliders become necessary.

> [!note] Since `R_conv = 1/(h·A)`, only the **product** matters
> A fin redesign that doubles area but halves h gains nothing. The contour map makes that immediately visible — and is more honest than predicting a single h the 1D model cannot compute.


---

## 12. Concepts captured

Durable, project-independent principles this work established — extracted as atomic notes (harvested to `04 Knowledge` on close):

- [[Cauer Model Calibration — fit what you cannot derive]] — one fitted parameter (h); everything else derived. Spread 35 % → 4.9 % by calibrating the *right* knob.
- [[Multi-node thermal time constants need eigenvalues, not per-branch RC]] — τ2 = 394 s from eig(A), not 350 s from C·R.
- [[Spreading resistance — heat enters over the source, not the whole base]] — Lee/Yovanovich constriction, and why A_base is the only sensitive input.
- [[Only the h·A product matters for convective resistance]] — a fin redesign that doubles A but halves h gains nothing.
- [[Convection dominates the thermal budget]] — R_conv is 78 % of R_total; effort on R_hs moved a 17 % term.
- [[Error shape diagnoses the cause — the thermal debug ladder]] — magnitude→R, shape→C, load-dependent→loss/h.

> [!quote] Standing principle
> Fit what you cannot derive. Derive what you can. Never bend a derived parameter to absorb an offset you can explain.
