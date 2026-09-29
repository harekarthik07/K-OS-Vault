---
type: concept
concept: Base thickness has a thermal optimum (spreading gain vs conduction penalty)
domain: Heat Transfer
status: budding
created: 2026-09-28
origin_project: ETM For Heatsink and IGBT
aliases: ["optimal base thickness", "R_hs(L) minimum", "spreading vs conduction crossover"]
sources: ["[[EOD_2026-09-28_ETM_1D_Thermal_Tool]]"]
tags: [heat-transfer, spreading-resistance, heatsink-design, optimum]
related: ["[[Spreading resistance — heat enters over the source, not the whole base]]", "[[Only the h·A product matters for convective resistance]]"]
---

# Base thickness has a thermal optimum — spreading vs conduction

## One-line idea
Heatsink base resistance `R_hs(L)` is **not monotonic** in base thickness `L`: a thicker base spreads heat better (lower `R_spread`) but adds series conduction (higher `R_cond`), so there is a real **minimum** where the two curves cross.

## Intuition first
Thin base → heat can't fan out from the source footprint before hitting the fins → high spreading resistance. Thick base → heat spreads nicely but now has a long path straight down → conduction penalty. Somewhere between, the total is minimised.

## Governing relations
- `R_hs(L) = R_cond(L) + R_spread(L)`, `R_cond ∝ L/(k·A)` (rising), `R_spread` falling with L (Yovanovich spreading).
- Minimum where `dR_cond/dL = −dR_spread/dL`.

## Worked example (T30 MC heatsink, ETM tool)
L-sweep of the 1D core puts the `R_hs` minimum at **17.9 mm**; the actual part is **18 mm** — already optimal. Thicker base helps spreading, hurts conduction, and the two cross right where the part sits.

## Validity window & invalidation triggers
- Assumes source smaller than the base (spreading regime) and 1D series conduction to the fin base.
- Breaks if the source covers most of the base (no spreading term) or if `k(T)` varies strongly across L.

## How we verify it
Sweep L in the validated 1D core and confirm a single interior minimum; cross-check the optimum against the as-built dimension.

## Where used
- [[EOD_2026-09-28_ETM_1D_Thermal_Tool]] · [[1D Thermal Design Tool — spec & flowchart]] (L-sweep tab)

---
`R_hs(L)` · `optimal base thickness` · `spreading vs conduction` · `17.9 mm`
