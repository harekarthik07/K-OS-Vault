---
title: Long-Cycle Adaptation — Section 4 Theory & Math
project: MC_HS_LongCycle_Validation
type: theory
section: 4
author: Hare Karthik (Vehicle Engineering)
date: 2026-10-01
tags: [thermal, ETM, RK4, cross-correlation, validation, T30, long-cycle]
related: "[[T30_MC_ETM_Part1_Thermal_Budget]] [[README_thermal_tool]] [[mc-hs-thermal-tool]]"
---

# Section 4 — Calc & Theory (Long-Cycle Adaptation)

Physics is unchanged from the validated ETM. This phase adds only two pieces of math:
an **adaptive solver step** (so long runs stay fast and accurate) and a
**transient-tracking metric** (so a drive cycle validates the capacitances, which a
monotonic dyno burst never could). Both are derived below.

---

## 4.1 — Adaptive time step

### 4.1.1 The solver: RK4 (Runge–Kutta, 4th order)

`thermal_core` integrates the two-node ODEs with RK4 — the same method already in use.
Each step samples the derivative four times and takes a weighted average:

```
k1 = f(y)
k2 = f(y + dt/2 * k1)
k3 = f(y + dt/2 * k2)
k4 = f(y + dt   * k3)
y_next = y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
```

"4th order" means local error per step ~ O(dt^5), global error ~ O(dt^4): halving dt
cuts error ~16x. This is why RK4 is extremely accurate at the steps we use.

### 4.1.2 Stability limit — where |lambda . dt| <= 2.78 comes from

Apply any integrator to the scalar test equation `dy/dt = lambda*y` (lambda < 0 = decay).
True solution `y = y0 * exp(lambda*t)` decays smoothly. RK4 gives, per step:

```
y_next = G(z) * y ,   z = lambda*dt
G(z) = 1 + z + z^2/2 + z^3/6 + z^4/24     (RK4's 4 stages for the linear case;
                                           the leading terms of exp(z))
```

For the numerical solution to decay like the real one, need |G(z)| < 1. On the negative
real axis the boundary is z ~ -2.78. Beyond it |G| > 1 and the solution GROWS each step
(blows up) even though the real system decays. So:

```
|lambda . dt| < 2.78    (RK4 real-axis stability)
```

The constant is RK4-specific (Forward Euler = 2.0). Binding mode = the fast one:

```
lambda1 = -1/tau1 = -1/19.0 = -0.0526  ->  dt_stable < 2.78/0.0526 = 52.8 s
lambda2 = -1/tau2 = -1/425  = -0.00235 (slow, not binding)
```

### 4.1.3 Accuracy limit — the real constraint

Stability allows 52.8 s, but resolving the SHAPE of the 19 s transient is far stricter:

```
dt < tau1 / 10 = 1.9 s     (standard "resolve the fastest mode" rule)
```

Numerically verified (RK4 vs closed-form, T_ntc at 240 s, LM25 defaults):

| dt (s) | T_ntc(240) | error |
|--------|-----------|-------|
| 0.05   | 80.8818   | <1e-5 K |
| 0.15   | 80.8818   | <1e-5 K |
| 0.50   | 80.8818   | ~1e-5 K |

At dt <= 0.5 the error is numerically invisible (4th order, linear system, tau1=19 s).
The 1/10 rule is conservative; we sit well inside it.

### 4.1.4 The three-way rule

```
dt = min( max(0.05, t_end/20000), 0.5 )
         |________|  |___________|   |__|
          accuracy    cost cap      data
           floor     (<=20k steps)  floor
```

- **0.05 floor** — accuracy already saturated; finer = wasted compute.
- **t_end/20000** — cost is linear in step count; 20k steps keeps a slider redraw
  sub-second. WLTP (3042 s) -> 0.152 s.
- **0.5 cap** — the 2 Hz data interval. If dt > 0.5 s the solver steps PAST input
  samples and silently skips load transients (aliasing). Engages only for
  t_end > 10,000 s (2.8 h).

For the WLTP run all three give **dt = 0.152 s** — finer than the data, so P_inv is
linearly interpolated UP between samples (RK4 needs Q at t, t+dt/2, t+dt). That is the
physically honest choice: the real current ramped between samples, it did not teleport.
A zero-order hold would inject fake step-edges that the derivative metric would then
misread as fast transients.

---

## 4.2 — Transient-tracking metric (cross-correlation lag)

### 4.2.1 Why RMSE alone is blind to timing

A model perfectly right in shape but 10 s slow, on a MONOTONIC dyno ramp, just looks a
bit cooler — indistinguishable from a small resistance error. RMSE collapses everything
to one number and cannot separate "wrong size" from "wrong timing."

A drive cycle goes UP and DOWN. A timing error now shows as the model's peaks landing
consistently after the measured peaks — a signature cross-correlation isolates cleanly.

### 4.2.2 The math

Mean-removed discrete cross-correlation vs integer sample shift m:

```
R(m) = sum_t [ x(t) - xbar ] * [ y(t+m) - ybar ]      x = T_model, y = T_meas
```

Normalise to a correlation coefficient (peak interpretable as "how well shapes match"):

```
rho(m) = R(m) / sqrt( sum(x-xbar)^2 * sum(y-ybar)^2 )
lag    = argmax_m rho(m) * dt_data   [seconds]
```

### 4.2.3 Interpretation

| rho(m*) | lag | verdict |
|---------|-----|---------|
| >0.95   | ~0  | C correct, model tracks |
| >0.95   | >0  | measured leads model -> model sluggish -> C too large |
| >0.95   | <0  | model leads -> C too small |
| <0.90   | any | shape wrong -> loss model or R, not C |

Worked example: m* = +14 samples at 0.5 s -> lag = +7 s, rho = 0.98. Shapes match
(0.98); model trails by 7 s -> thermal mass responding slightly slow -> C a few %
high. Since C was never measured from cooldown, this metric is how we finally pin it.

### 4.2.4 Orthogonality — why three metrics, not one

Orthogonal = independent, non-interfering: change one without touching the others.
Three error types, each seen by exactly ONE metric:

```
magnitude error (too hot/cold in size)   -> RMSE
offset error    (constant shift)         -> bias
timing error    (lag/lead in time)       -> cross-correlation lag
```

Cross-correlation is orthogonal to the other two BY CONSTRUCTION:
- **ignores offset** — means subtracted, so +5 degC everywhere doesn't move the lag.
- **ignores magnitude** — normalised ('coeff'), so scaling x2 doesn't move the lag.

So lag reports PURELY timing. That un-mixing is the whole point:

```
high RMSE, lag~0  -> size problem   -> look at R or loss model
low  RMSE, lag!=0 -> timing problem -> look at C (capacitance)
```

The dyno burst is the non-orthogonal counterexample: a monotonic ramp blends timing and
size into one blur, which is exactly why a C error there looked identical to an R error.
The drive cycle, read with these three orthogonal metrics, separates them.

### 4.2.5 Implementation note
`xcorr(y, x, 'coeff')` (Signal Processing Toolbox) gives rho(m) directly. Guard with
`exist('xcorr','file')`; fallback is a plain loop over a bounded shift window (+/-120 s
is ample for a tau2=425 s system) so the tool never hard-depends on a toolbox.

---

## 4.3 — What is NOT in this phase
No h(v). h stays constant at the dyno value (29.59). Section 4 adds no new physics —
only a safe adaptive solver step and an orthogonal diagnostic metric. Differential-h
(ram air) is the next project.

> [!note] Data caveat
> The WLTP run is low-load (P_inv avg 27 W, peak 188 W; IGBT 48->57 degC). The lag
> metric works best on sharper transients; it will still read a lag here, but a more
> aggressive cycle exercises it harder. Also: this run is DYNO (no ram air), so constant
> h is correct for it — a genuine road cycle would show the h bias until differential-h
> lands.
