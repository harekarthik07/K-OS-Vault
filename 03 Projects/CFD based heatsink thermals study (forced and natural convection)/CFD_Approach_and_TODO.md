---
type: approach_todo
project: CFD based heatsink thermals study (forced and natural convection)
status: active
created: 2026-09-28
related: ["[[00 Home]]", "[[CFD_Problem_Statement]]"]
---

# CFD — Approach & TODO

> Live task checkboxes (the source of truth) stay in [[00 Home]] under each phase. This note holds the **method and theory** for upcoming work.

## Phase 1 — finish the baseline (method)
1. **Re-run the fan PQ health check** — require `ε < 5 %` before trusting any result ([[Curve-match residual ε is a convergence gate for fan CHT]]). If still choked after convergence, escalate fin redesign to the MC team.
2. **Match mesh `y+`** on the HS and set Yplus-for-HTC to match.
3. **Report per-zone `h`** — under-hub vs impingement kept **separate** ([[Dead-zone h is a different regime, not a correction factor]]) → feed [[MC_HS_ETM_I1]] `R_conv`; consider a 3-node Cauer with a dead-zone branch.

## Phase 2 — CHT case configurator (method)
Property engine → Ri classifier → Re/Pr/Gr/Ra/Ri readouts → setup advisor → pre-run `h` via Nu correlations → post-CFD per-zone `h` extractor → automated PQ health check. Math backing: [[CHT Case Configurator — Math Behind Every Section]].

## Phase 3 — TBD
Define once Phase 1 `h` values and the configurator are in.

---
`PQ gate` · `y+ match` · `zone-wise h` · `configurator`
