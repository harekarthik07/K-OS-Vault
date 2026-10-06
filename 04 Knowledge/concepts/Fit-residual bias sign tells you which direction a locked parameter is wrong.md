---
concept: Fit-residual bias sign tells you which direction a locked parameter is wrong
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: budding
created: 2026-10-06
sources: ["[[HS_Transient_Physics_h_and_C]]", "[[EOD_2026-10-06]]"]
extracted_from: ["[[HS_Transient_Physics_h_and_C]]"]
tags: [thermal, convection, fitting, bias, method, debugging]
---

# Fit-residual bias sign tells you which direction a locked parameter is wrong

## Working definition (project-specific)
When a model systematically reads hot or cold vs measured data, the **sign** of that
offset directly tells you which way the responsible parameter needs to move — but it is
easy to get the direction backwards on first pass.

```
bias = mean( T_measured − T_model )

bias > 0  ->  measured hotter  ->  model OVER-cooled  ->  resistance too LOW  ->  h too HIGH
bias < 0  ->  measured cooler  ->  model UNDER-cooled  ->  resistance too HIGH -> h too LOW
```

## Notes / derivations / snippets
- **The trap:** a positive bias (model reading cold relative to measured) intuitively
  suggests "the model needs more heat retention, so airflow must be *weaker* than
  assumed → expect a *lower* fitted h." The actual relationship runs the other way:
  positive bias means the model is **removing too much heat**, i.e. its convective
  resistance is too *low*, i.e. its assumed h was too *high*. The fitted/corrected h comes
  out *lower* than the naive guess, confirming the corrected (not the intuitive) direction.
- **How to avoid the trap:** write the full causal chain before interpreting any single
  fitted run — `bias sign -> which direction the model's heat REMOVAL is wrong -> which
  direction the resistance is wrong -> which direction the fitted parameter should move` —
  and check it against at least one data point where you already independently know the
  expected direction, before trusting the fit on cases you don't.
- **Generalizes beyond h:** any single-knob fit against a residual bias has this same
  two-step inversion risk (offset sign → physical-quantity direction → fitted-parameter
  direction). Worth writing the chain out explicitly every time rather than trusting the
  first intuitive read, especially when the knob and the residual have an inverse
  relationship (as resistance and heat removal do here).

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[Capacitance sets transient speed, convection sets steady-state level — lock one before fitting the other]]
- [[Error shape diagnoses the cause — the thermal debug ladder]]
