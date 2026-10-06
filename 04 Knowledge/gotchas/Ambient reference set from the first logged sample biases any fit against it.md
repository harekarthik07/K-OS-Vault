---
concept: Ambient reference set from the first logged sample biases any fit against it
origin_project: ETM For Heatsink and IGBT
domain: Thermal Management
status: seedling
created: 2026-10-06
sources: ["[[HS_Transient_Physics_h_and_C]]", "[[EOD_2026-10-06]]"]
extracted_from: ["[[HS_Transient_Physics_h_and_C]]"]
tags: [thermal, convection, fitting, gotcha, ambient, sensor]
---

# Ambient reference set from the first logged sample biases any fit against it

## Working definition (project-specific)
A tool that defaults `T_amb` to the **first logged value of the thing being heated**
(here: the IGBT's own starting temperature) rather than a true air-temperature
measurement silently biases every downstream fit, and the bias has a knowable direction.

## Notes / derivations / snippets
- **Concrete case:** on a road run, `T_amb` was set to the first IGBT temperature sample
  (~48 °C) while the real air temperature was likely ~30–35 °C. A too-warm assumed ambient
  sinks less heat in the model (smaller ΔT to the reference), so the model runs warmer than
  it should for a given h — and the fit compensates by returning a **higher fitted h** to
  pull the model back down to match measured data.
- **Why the direction matters, not just the existence of the bias:** knowing the bias is
  high (not low, not unknown) means a corrected ambient reading would only ever **lower**
  the fitted value further — so if a decision ("design is safe," "h is adequate") depends
  on the fitted value being conservative, this particular bias makes the current number
  *optimistic*, not safe-side. Treat the current fit as an upper bound on h, not a best
  estimate, until ambient is logged properly.
- **The general pattern:** any time a "reference" or "ambient" value is auto-populated from
  the first sample of the *measured* channel rather than an independent measurement, check
  which direction that substitution pushes every quantity fitted against it, before trusting
  the fit on data where the substitution and the true value diverge significantly (e.g. a
  cold-start road run vs. a pre-soaked dyno bench where the two values nearly coincide).
- **Fix:** log real ambient air temperature as its own channel; this is a workaround, not a
  model error — the thermal model itself is correct once given the right ambient.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]]
- [[A single fitted parameter is a duty-weighted average of a time-varying process, not a true constant]]
