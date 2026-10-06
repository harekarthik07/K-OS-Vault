---
concept: A duration-agnostic solver scales via step selection, not by forking the model
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: seedling
created: 2026-10-01
sources: ["[[Approach_and_TODO]]", "[[Problem_Statement]]"]
extracted_from: ["[[Approach_and_TODO]]"]
tags: [architecture, solver-design, validation, method]
---

# A duration-agnostic solver scales via step selection, not by forking the model

## Working definition (project-specific)
When a validated model needs to handle a new regime (here: a 50-minute drive cycle on top
of an already-validated 4-minute dyno burst), the instinct to build a second, specialised
path should be resisted if the existing solver is already general enough to take the new
case as *just more of the same input*.

## Notes / derivations / snippets
- The thermal solver already accepted heat input as an arbitrary `[t, Q]` series — a long
  drive cycle is not a new kind of input, it's a longer one. The only things that actually
  need to change for the new regime are: how the step size is chosen (see
  [[Adaptive time-step — balance an accuracy floor, a cost cap, and a data floor]]), how many
  points get drawn on screen, and which fit metrics get reported.
- **Why not fork:** a parallel implementation for "long mode" would drift from the one that
  was actually validated against dyno data — the validation gate would no longer cover the
  code path actually used for drive-cycle work. Compare
  [[Lock a fast surrogate model to the authoritative one with a guard test]], which solves a
  related problem (a second, faster model) by gating it against the first rather than
  trusting it independently — same instinct, applied to two different kinds of "a second
  version appeared."
- **Guard-rail discipline this implies:** any change made to support the new regime must be
  provably additive to the existing one — re-run the *old* regime's gate test after the
  change and require it to be unchanged (here: dyno 4-min must still read Tj_peak = 93.5 °C
  after the adaptive-dt edit). The gate is the thing that proves "duration-agnostic" is true
  and not just asserted.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] At least one equation or diagram (this one is architectural, not mathematical)
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[Lock a fast surrogate model to the authoritative one with a guard test]]
- [[Adaptive time-step — balance an accuracy floor, a cost cap, and a data floor]]
