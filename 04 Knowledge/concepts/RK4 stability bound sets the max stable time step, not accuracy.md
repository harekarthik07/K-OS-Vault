---
concept: RK4 stability bound sets the max stable time step, not accuracy
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: seedling
created: 2026-10-01
sources: ["[[Section4_Theory_LongCycle]]"]
extracted_from: ["[[Section4_Theory_LongCycle]]"]
tags: [numerical-methods, rk4, stability, ode, thermal, method]
---

# RK4 stability bound sets the max stable time step, not accuracy

## Working definition (project-specific)
For an explicit integrator applied to a decaying linear system (`dy/dt = λy`, λ < 0), there
are **two independent ceilings on the time step**: a *stability* bound (does the numerical
solution blow up?) and an *accuracy* bound (does it resolve the real shape?). They are not
the same number, and the accuracy bound is usually the tighter one.

## Notes / derivations / snippets
- RK4's amplification factor per step: `G(z) = 1 + z + z²/2 + z³/6 + z⁴/24`, `z = λ·dt`.
  Need `|G(z)| < 1` to decay; on the negative real axis this breaks at **`z ≈ -2.78`**.
  (Forward Euler's equivalent bound is `z = -2.0` — RK4 buys headroom from its four stages.)
- Binding mode is the **fastest** eigenvalue, not the slowest:
  ```
  λ_fast = -1/τ_fast  →  dt_stable < 2.78 / |λ_fast|
  ```
  Example: τ1 = 19 s → dt_stable < 52.8 s. Looks generous — but:
- **Accuracy is stricter than stability here.** Resolving the *shape* of a τ1 = 19 s
  transient wants `dt < τ1/10 ≈ 1.9 s`, over 25× tighter than the stability ceiling.
  Numerically confirmed flat: dt = 0.05 / 0.15 / 0.50 s all agree to <1e-5 K at t = 240 s.
- **Takeaway:** don't size dt off the stability formula alone — it tells you where the
  solver breaks, not where it stops being trustworthy. Size off the fastest physical
  mode you need to resolve, then only *check* stability as a sanity floor.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[Heat Transfer]]
- [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]
