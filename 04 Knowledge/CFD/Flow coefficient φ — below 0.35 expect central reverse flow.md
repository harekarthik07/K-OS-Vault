---
concept: Flow coefficient φ as a stall proximity gauge
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: promoted
promoted: 2026-09-02
created: 2026-09-02
aliases: ["φ = Q_op over Q_max — below 0.35 expect central reverse flow"]
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [cfd, fan-model, stall, reverse-flow]
---

# Flow coefficient φ — below 0.35 expect central reverse flow

> Filename note: written with "φ" rather than the raw `φ = Q_op/Q_max` because a `/` is illegal in Obsidian filenames. The alias carries the original phrasing.

## Working definition (project-specific)
Normalise the operating flow by the fan's free-delivery flow:

$$\varphi \;=\; \frac{Q_{op}}{Q_{max}}$$

φ says **where on its own curve** the fan is sitting, in one dimensionless number — comparable across fans and across designs.

| φ | Reading |
|---|---|
| > 0.5 | healthy |
| 0.35 – 0.5 | marginal |
| < 0.35 | choked / near-stall |

## Notes / derivations / snippets
- This case: `φ = 0.00846 / 0.02367 = 0.357` → marginal, right at the choked edge — consistent with the reverse flow observed.
- **Why low φ shows up as reverse flow near the hub first:** at low flow the blade incidence angle grows past the stall angle. The hub region has the lowest blade speed and the least momentum, so it separates first — the reverse-flow cells appear centrally and spread outward.
- Pair with the local slope test: `m = dΔp/dQ` at `Q_op`. `m < 0` stable; `m ≥ 0` means you're on the flat/rising left branch, which is dynamically unstable (surge).
- φ is a *design* verdict, not a *convergence* verdict — only trust it once [[Curve-match residual ε is a convergence gate for fan CHT]] passes.

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]]
- [[Fan operating point = fan PQ curve ∩ system curve K·Q²]] · [[Fan PQ Health Check & Reverse-Flow Diagnosis]]
