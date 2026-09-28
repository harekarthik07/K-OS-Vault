---
type: progress_log
project: CFD based heatsink thermals study (forced and natural convection)
status: active — Phase 1 in progress
created: 2026-09-28
related: ["[[Daily Log]]", "[[CFD_Problem_Statement]]", "[[00 Home]]"]
---

# CFD — Progress Log

> Chronological record of what was tried, what broke, the root cause, and the fix. Day-by-day detail lives in [[Daily Log]]; this note holds the milestone-level narrative and the `#learning` flags.

## Milestones
- **2026-09-02 — CHT baseline converged**, then hit a blocker: **reverse flow at the fan exit** on [[HS_I1-G1-K1]]. Root cause diagnosed via the PQ health check: tighter fins raised system `K`, shifting the operating point left toward stall. See [[Fan PQ Health Check & Reverse-Flow Diagnosis]].
- **2026-09-03 — Re-converged** with Hybrid Init + FMG, coupled + pseudo-transient, 1st→2nd order, backflow BCs set. Confirmed `K_new/K_old ≈ 3–4`.

## Learnings (feed to /weekly)
- #learning/gotcha — A **growing** reverse-flow face count is a physics/BC problem, not solver noise → [[Growing reverse-flow face count = physics-BC problem, not solver noise]]
- #learning/concept — Below `φ ≈ 0.35` expect central reverse flow → [[Flow coefficient φ — below 0.35 expect central reverse flow]]
- #learning/concept — Dead-zone `h` is a different regime, not a correction factor → [[Dead-zone h is a different regime, not a correction factor]]

## Open
- Re-run PQ health check (require `ε < 5 %`), match mesh `y+`, report per-zone `h`. Live tasks in [[00 Home]].

---
`CHT baseline` · `reverse-flow blocker` · `PQ health check` · `#learning`
