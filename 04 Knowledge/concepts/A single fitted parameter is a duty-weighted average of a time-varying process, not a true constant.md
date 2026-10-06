---
concept: A single fitted parameter is a duty-weighted average of a time-varying process, not a true constant
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: seedling
created: 2026-10-06
sources: ["[[HS_Transient_Physics_h_and_C]]", "[[EOD_2026-10-06]]"]
extracted_from: ["[[HS_Transient_Physics_h_and_C]]"]
tags: [thermal, convection, fitting, h_eff, method]
---

# A single fitted parameter is a duty-weighted average of a time-varying process, not a true constant

## Working definition (project-specific)
A model with one constant parameter (h), fit against a run where the true physical
quantity actually varies in time (h(t): high moving, low idling), returns an **effective
average** — weighted toward whichever segments dominate the run's duration or error, not a
single physical value that ever existed on its own.

## Notes / derivations / snippets
- **Concrete case:** a road run's fitted h_eff = 18.8 W/m²K looked low compared to the
  fan-forced bench value (29.59). The run was a hard push for ~1700 s followed by a long
  slow/idle tail to 6000 s (2/3 of the run) — the low-airflow tail dominated the fit,
  pulling h_eff down even though the moving segment likely had much higher instantaneous h.
- **The failure mode this prevents:** reading h_eff = 18.8 as "road airflow is weak" would
  be a category error — it conflates a *duty-cycle-weighted average* with a *physical
  constant*. The correct read is "this run's time-weighted average h is 18.8"; the
  underlying h(t) was never constant.
- **The fix is a segment fit, not a single global fit:** split the run at the condition
  boundaries (moving vs idle, fan on vs off) and fit h independently on each segment. Only
  then does "h_eff" become "h(condition)" — a lookup table instead of one misleading number.
- **Generalizes beyond this project:** any single-parameter fit against a run with mixed
  operating regimes (duty cycles, intermittent loads, multi-phase processes) returns a
  weighted average dominated by whichever regime has the longest duration or largest
  residual — not evidence that the underlying process was constant. Always check whether
  the input actually varied in time before trusting a "constant" fit result as physical.

## Maturity checklist (before promoting to evergreen)
- [ ] Definition is generalizable, not project-specific (segment-fit confirmation pending —
      next phase of this project)
- [ ] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[Capacitance sets transient speed, convection sets steady-state level — lock one before fitting the other]]
