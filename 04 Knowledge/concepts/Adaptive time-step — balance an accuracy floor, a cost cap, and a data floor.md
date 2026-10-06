---
concept: Adaptive time-step — balance an accuracy floor, a cost cap, and a data floor
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: seedling
created: 2026-10-01
sources: ["[[Section4_Theory_LongCycle]]", "[[Approach_and_TODO]]"]
extracted_from: ["[[Section4_Theory_LongCycle]]"]
tags: [numerical-methods, adaptive-step, ode, simulation-cost, method]
---

# Adaptive time-step — balance an accuracy floor, a cost cap, and a data floor

## Working definition (project-specific)
A single fixed time step is wrong at both ends of a duration range: too fine wastes compute
on long runs, too coarse skips load transients on short/finely-sampled ones. A **three-way
min/max rule** picks dt automatically from problem size, with each term defending a
different failure mode:

```
dt = min( max(0.05, t_end/20000), 0.5 )
          |________|  |___________|   |__|
           accuracy     cost cap      data
            floor      (N steps)     floor
```

## Notes / derivations / snippets
- **Accuracy floor (0.05 s):** below the point where finer stepping stops changing the
  answer (see [[RK4 stability bound sets the max stable time step, not accuracy]]). Going
  finer than this is wasted compute, not more truth.
- **Cost cap (`t_end/20000`):** step count is what a UI/slider redraw actually pays for.
  Capping total steps (here ~20k) keeps interactive runs sub-second regardless of t_end.
  A 4-min dyno run and a 50-min WLTP run both resolve to a step count, not a step size.
- **Data floor (0.5 s):** if dt exceeds the input sample spacing, the solver can step
  *past* a loaded data point between evaluations — the real signal didn't teleport between
  samples, but a solver with too-coarse dt would effectively assume it did (aliasing).
  This only engages for very long runs (here, t_end > 10,000 s / 2.8 h).
- When dt lands *finer* than the input sampling (the common case), the loss/heat-input
  series must be **interpolated up** between samples for the stage evaluations an RK-type
  method needs (t, t+dt/2, t+dt) — linear interpolation is the physically honest choice;
  a zero-order hold injects fake step edges that a shape-based metric would misread as a
  fast transient.
- **Generalizes beyond this project:** any duration-agnostic solver over a variable-length
  episodic input (sensor logs, control traces, drive cycles) wants this same three-term
  shape — one term for the physics, one for the budget, one for the data itself.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[RK4 stability bound sets the max stable time step, not accuracy]]
- [[A duration-agnostic solver scales via step selection, not by forking the model]]
