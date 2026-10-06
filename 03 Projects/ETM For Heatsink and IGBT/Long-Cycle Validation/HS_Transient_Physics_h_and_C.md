---
title: HS Transient Physics — h, C, and What the Fits Mean
type: concept
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-06
project: MC_HS_LongCycle_Validation
tags: [thermal, concept, transient, capacitance, convection, h_eff, T30, learning]
related: "[[Section4_Theory_LongCycle]] [[T30_MC_ETM_Part1_Thermal_Budget]] [[EOD_2026-10-06]] [[mc-hs-thermal-tool]]"
---

# HS Transient Physics — h, C, and What the Fits Mean

> [!abstract] One line
> **C sets how FAST the temperature moves. h sets WHERE it settles.** C is fixed by
> mass; h changes with airflow. Fit h, validate C — never the other way round.

---

## 1. The tank model (exact, not a loose analogy)

```
          inflow  Q  (heat in, W)
               |
    +----------v----------+
    |~~~~~~~~~~~~~~~~~~~~~| <- water LEVEL  = temperature
    |                     |
    +----------+----------+
     <-- width = C -->         C = m x cp   (J/K)
               |
          outlet  1/R          R_conv = 1/(h x A)
```

| Tank | Thermal | Set by |
|---|---|---|
| width | capacitance C | mass x cp — **fixed** |
| water level | temperature T | the balance below |
| outlet size | 1/R (convection) | **h** — airflow |
| inflow | heat Q | load / throttle |

```
level rises until        inflow = outflow          (steady state)
final level              dT_ss = Q x R             <- set by h, NOT C
time to get there        tau  ~ R x C              <- set by C
```

- **C decides speed.** Wide tank rises/falls slowly; narrow tank is jumpy.
- **h decides height.** Big outlet keeps the level low.
- **The tank is never "partly used."** Width is always the full C. Only the *level* is
  partial — the outlet stops it climbing forever. With no outlet (h = 0) there is no
  "full"; temperature rises without limit.

Why a drive cycle teaches more than a dyno burst: the cycle pours unevenly (throttle
up/down), so the level rises **and falls**. Rise/fall *speed* exposes C; settling
*height* exposes h. A monotonic dyno ramp only ever showed the outlet.

---

## 2. Why h changes — real physics

Convection = air carrying heat off the fins. More air past the fins = bigger outlet.

```
h  proportional to  v^n ,   n ~ 0.5-0.8
```

| Regime | Typical h (W/m2K) |
|---|---|
| natural convection (still air) | ~5-15 |
| MC fan, forced | ~20-30 |
| fan + ram air (fast road) | higher, speed-dependent |

---

## 3. Bias sign — read this before interpreting any fit

```
bias = mean( T_meas - T_model )
```

| bias | meaning | h is | true h is |
|---|---|---|---|
| **> 0** | measured hotter -> model **over-cooled** | too **high** | **lower** |
| < 0 | measured cooler -> model under-cooled | too low | higher |

> [!warning] Correction — earlier reasoning was backwards
> On the fullpush-w-Fan run (bias +3.53 K at h = 29.59) the first interpretation was
> "cold bias -> h too low -> more airflow -> expect h > 29.59." **Wrong direction.**
> Positive bias = model over-cooled = true h **lower**. The fit returned **h = 22.39**,
> confirming the corrected reading.

---

## 4. Why C does NOT change with heat input

```
C = m x cp
m  = heatsink mass       -> fixed (CAD: 2.7576 kg sink node, 3.3224 kg total)
cp = specific heat (Al)  -> drifts only ~3-4 % over 20-150 degC
=> C_hs ~ 2402 J/K at 50 W or 500 W alike
```

Temperature changes with load. **Capacitance does not.**

### So why fit C at all?
Because it was never measured (no cooldown data). C is *derivable*, so a fit is a
**validation, not a measurement**:
- fit ~ CAD value -> mass model right, lump behaves as one node.
- fit far from CAD -> **something else is wrong** — not "C changed."

### The 1321 J/K lesson
Fitting C alone on the fan run returned **1321 J/K — physically impossible** (mass is
fixed). The fit had a level error caused by h, and the only knob it could turn was C.
A smaller C pushes peaks higher, which partly hides a level error. The tank didn't
shrink; the fitter pretended it did.

### Why h and C must not be fitted together on short windows
Both can reduce the same level error (raise/lower h, or shrink C to make peaks taller).
That degeneracy makes a joint fit ill-posed.

> [!note] Decision (supersedes "fit h and C together")
> **Lock C at the CAD value. Fit h only.** One error x one free parameter = unique,
> well-posed answer. C is then validated *indirectly* through the lag metric (sec 5).

---

## 5. How C gets validated without fitting it — lag

h shifts the **level**. C shifts the **timing**. No value of h can move *when* a peak
happens. So:

```
lag = 0   -> model rises/falls in step with measured -> C correct
lag != 0  -> timing error -> C (or loss model) wrong
```

**Result: lag = +0 s on every run tested** (fullpush-w-Fan, fan-off, road).
C = 2402 J/K is confirmed across all cooling conditions.

### Is the full C really participating on fast transients?
Worry: on fast transients, maybe only metal near the IGBT heats and the far side lags,
making effective C smaller. Evidence it doesn't:
- **Physics:** diffusion time across the 18 mm base = L^2/alpha ~ **5 s**; thermal
  changes happen over hundreds of seconds; **Bi = 0.004** -> whole casting ~ one
  temperature.
- **Data:** a partially-participating mass would make the full-C model sluggish ->
  measured would **lead** -> lag != 0. Observed lag = 0 every time.

---

## 6. h_eff — why road h can look LOW

The model has **one constant h**. A road run has **h(t)** — high when moving fast, low
when slow or stopped. The fit returns the single constant that best matches the whole
run: an **effective average**, weighted toward the longest / largest-error segments.

Road run example: hard push 0-1700 s, then a long decay to 6000 s (2/3 of the run). If
the tail is slow/idle, low airflow dominates and pulls h_eff down to 18.8 even if the
moving segment had much higher h.

**Test:** fit h separately on moving vs slow segments (segment fit, next phase).

> [!warning] T_amb confound — direction matters
> The app sets T_amb = **first IGBT temp** (IGBT start, not air). On the road run that
> is ~48 degC while real air is likely ~30-35 degC. A too-warm model "air" sinks less
> heat -> model runs warmer -> fit compensates with a **higher** h. So the fitted road h
> is, if anything, **biased high**. Correcting T_amb would lower it further, not raise
> it. For road work: **log real ambient air temperature separately.**

---

## 7. Summary table

| Question | Answer |
|---|---|
| What does C do? | Sets response speed (tau ~ RC) |
| What does h do? | Sets settling level (dT = QR) |
| Does C change with load? | No — m x cp fixed, cp drift ~3-4 % |
| Is C ever "partly used"? | No — width always full; only the level varies |
| Why fit C? | Validation only; disagreement flags another error |
| Fit h and C together? | No — degenerate. Lock C, fit h |
| How is C validated? | lag = 0 (h can't move timing) — 0 s on all runs |
| Is road h_eff an average? | Yes — one constant for a varying h(t) |
| bias > 0 means? | Model over-cooled -> true h lower |
