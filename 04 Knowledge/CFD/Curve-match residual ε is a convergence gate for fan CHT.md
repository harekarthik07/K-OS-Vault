---
concept: Curve-match residual ε as a convergence gate
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [cfd, convergence, fan-model, vv]
---

# Curve-match residual ε is a convergence gate for fan CHT

## Working definition (project-specific)
Residuals tell you the equations are balanced. They do **not** tell you the fan BC is being honoured. ε does:

$$\varepsilon \;=\; \frac{\left|\Delta p_{op} - \Delta p_{curve}(Q_{op})\right|}{\Delta p_{curve}(Q_{op})}$$

where `Δp_curve` is the datasheet PQ curve linearly interpolated at the CFD's own `Q_op`. A converged fan case must sit **on its own curve**.

| ε | Verdict |
|---|---|
| < 5 % | fan BC honoured ✓ |
| 5 – 10 % | suspect |
| > 10 % | not converged / reverse-flow contaminated — **do not use the results** |

## Notes / derivations / snippets
- Interpolation between bracketing datasheet points:
  `Δp_curve = Δp₁ + (Q_op − Q₁)/(Q₂ − Q₁)·(Δp₂ − Δp₁)`
- This case: `Δp_curve(0.00846) = 38.83 Pa`, `Δp_op = 32.11 Pa` ⇒ `ε = 17.3 %` → gate failed. The case *looked* like it was converging (continuity dropping) but the fan was delivering 17 % less rise than physically possible.
- **Ordering matters:** run the ε gate *first*. Only if it passes do φ and the slope test mean anything as design verdicts.
- Complement with report-value monitors (IGBT baseplate T, fan ṁ, base heat flux) flat to < 0.5 % over 50 iterations — a physical-quantity plateau beats a residual floor.
- Automate as Section 6 of the [[CHT Case Configurator — Math Behind Every Section|configurator tool]].

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]]
- [[Fan PQ Health Check & Reverse-Flow Diagnosis]] · [[Growing reverse-flow face count = physics-BC problem, not solver noise]]
