---
tags: [project, CAE-CFD, busbar, ETM]
date: 2026-10-29
related: "[[small-top-busbar-etm]]"
---

# Approach_and_TODO — Small Top Busbar ETM

## Approach
1. Model both old (cylindrical boss) and new (rect block) busbar terminal designs with identical 18-wirebond excitation (6.67A each) and BCs.
2. Solve each via Maxwell 3D → Icepak two-way coupling (steady-state).
3. Compare **absolute max terminal temp** — old is the baseline, not a separate spec.
4. If new fails (temp > old), root-cause first — don't default to "change length" since lengths are already near-matched (15 vs 15.2mm). Likely levers: cross-section shape, fillet radius at corners, contact/transition mesh.
5. Re-solve on whichever lever is implicated, iterate until new ≤ old.

## TODO
- [ ] Re-run old design at 27°C ambient (currently mismatched — earlier runs used 30°C)
- [ ] Pull old design max terminal temp result
- [ ] Direct comparison: new vs old max terminal temp
- [ ] Cross-check against area-ratio sanity expectation (new should run cooler given ~3.4× cross-section)
- [ ] If new underperforms: inspect mesh quality at rectangular terminal corners
- [ ] Close Section 6 (End Result For) — confirm what this result feeds downstream
- [ ] Decide: standalone bolted-joint contact resistance (flagged 2026-10-21, not yet modeled) — in scope for this study or deferred?
