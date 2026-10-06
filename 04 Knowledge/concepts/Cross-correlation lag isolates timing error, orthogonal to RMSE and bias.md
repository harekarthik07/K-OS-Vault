---
concept: Cross-correlation lag isolates timing error, orthogonal to RMSE and bias
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-10-01
sources: ["[[Section4_Theory_LongCycle]]"]
extracted_from: ["[[Section4_Theory_LongCycle]]"]
tags: [validation, cross-correlation, capacitance, method, thermal]
---

# Cross-correlation lag isolates timing error, orthogonal to RMSE and bias

## Working definition (project-specific)
Fitting a dynamic model against measured data with a single error number (RMSE) conflates
three physically distinct failure modes. Splitting the residual into **three orthogonal
metrics** — each sensitive to exactly one — lets a single validation run diagnose *which*
part of the model is wrong, not just *that* it's wrong.

```
magnitude error (too hot/cold in size)   -> RMSE
offset error    (constant shift)         -> bias
timing error    (lag/lead in time)       -> cross-correlation lag
```

## Notes / derivations / snippets
- Mean-removed cross-correlation at integer sample shift `m`:
  ```
  R(m)   = Σ_t [x(t)-x̄][y(t+m)-ȳ]                 x = model, y = measured
  ρ(m)   = R(m) / sqrt( Σ(x-x̄)² · Σ(y-ȳ)² )
  lag    = argmax_m ρ(m) · dt_data
  ```
- **Why it's orthogonal by construction:** mean-subtraction makes it blind to a constant
  offset (+5 °C everywhere doesn't move the lag); normalising (`'coeff'`) makes it blind to
  scale (doubling the signal doesn't move the lag either). What's left is purely the *shape
  alignment in time* — nothing else can leak into this number.
- **Interpretation table:**
  | ρ(m*) | lag | verdict |
  |---|---|---|
  | >0.95 | ~0 | model tracks correctly |
  | >0.95 | >0 | measured leads → model sluggish → capacitance too large |
  | >0.95 | <0 | model leads → capacitance too small |
  | <0.90 | any | shape itself is wrong → loss model or resistance, not capacitance |
- **Why a monotonic test can't separate these:** a single ramp that is "right shape but
  N seconds slow" just looks slightly cooler everywhere — indistinguishable from a small
  resistance error in an RMSE-only read. A signal that goes **up and down** (a drive cycle,
  a duty-cycle, any oscillatory input) makes a timing error show up as *peaks landing
  consistently after the measured peaks* — a signature cross-correlation reads cleanly,
  where RMSE alone cannot. The metric needs a non-monotonic signal to have something to bite.
- **Capacitance is otherwise hard to isolate:** a monotonic charge/discharge test identifies
  the *R·C product* far better than R and C individually (see
  [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]). A lag reading
  on a dynamic (cyclic) signal is often the first measurement that pins C on its own.

## Validated — 2026-10-06
Run on 3 real conditions (fan-on low speed, fan-off, road) with C locked at CAD value and
h as the only fitted parameter: **lag = +0 s on every run.** This confirms C independently
of the h fit — h can shift the settling level but cannot move *when* a peak happens, so a
zero lag across cooling conditions this different is strong evidence C is right rather than
coincidentally unmoved. See [[HS_Transient_Physics_h_and_C]] §5 and [[EOD_2026-10-06]].

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific — confirmed on 3 independent runs
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]
- [[Error shape diagnoses the cause — the thermal debug ladder]]
