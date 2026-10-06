---
concept: Capacitance sets transient speed, convection sets steady-state level — lock one before fitting the other
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-10-06
sources: ["[[HS_Transient_Physics_h_and_C]]", "[[EOD_2026-10-06]]"]
extracted_from: ["[[HS_Transient_Physics_h_and_C]]"]
tags: [thermal, capacitance, convection, rc-model, fitting, degeneracy, method]
---

# Capacitance sets transient speed, convection sets steady-state level — lock one before fitting the other

## Working definition (project-specific)
In a lumped RC thermal model, capacitance (C) and convective resistance (via h) govern
**two different things about the response** — but on a single error signal, both can move
the error in the same direction, making a joint fit degenerate.

```
dT_ss  = Q · R        <- settling LEVEL, set by h (R_conv = 1/(h·A))
tau    ~ R · C        <- TIME to get there, set by C
```

## Notes / derivations / snippets
- **Tank analogy:** C is the tank's *width* (fixed by mass — `C = m·cp`); h sets the
  *outlet size* (how fast it drains, i.e. the settling level under constant inflow). The
  tank is never "partly used" — width is always the full C; only the water *level* is
  partial, and the outlet is what stops it climbing forever.
- **Why a joint fit breaks:** a level (magnitude) error can be closed two ways — change
  the outlet (h) or shrink the tank (C) so the same inflow produces a taller level. Both
  reduce the same residual. One error, two free knobs = ill-posed, non-unique answer.
- **Concrete failure case:** fitting C alone on a real run returned **1321 J/K** against a
  CAD-true value of ~2402 J/K — physically impossible (mass doesn't shrink). The fit had a
  level error actually caused by a wrong h, and C was the only knob available, so the
  optimizer "hid" the h-error inside a fake capacitance.
- **The fix:** lock the parameter you can independently derive (C, from CAD mass + known
  cp) and fit only the one you can't (h, which depends on uncontrolled airflow). One error
  × one free parameter = a unique, well-posed answer — RMSE(h) becomes a single bowl.
- **Validating the locked parameter without fitting it:** see
  [[Cross-correlation lag isolates timing error, orthogonal to RMSE and bias]] — h can move
  the settling level but *cannot* move *when* a peak happens, so a lag reading of ~0 across
  runs confirms the locked C independently of the h fit.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[Multi-node thermal time constants need eigenvalues, not per-branch RC]]
- [[Cross-correlation lag isolates timing error, orthogonal to RMSE and bias]]
- [[Error shape diagnoses the cause — the thermal debug ladder]]
