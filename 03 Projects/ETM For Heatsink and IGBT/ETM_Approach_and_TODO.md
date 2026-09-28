---
type: approach_todo
project: ETM For Heatsink and IGBT
status: active
created: 2026-09-28
related: ["[[00 Home]]", "[[ETM_Problem_Statement]]"]
---

# ETM — Approach & TODO

> Live task checkboxes (the source of truth) stay in [[00 Home]] under each phase. This note holds the **method and theory** for upcoming phases.

## Phase 2 — parametric sweep (method)
1. **Mask `Subsystem1`** with geometry params (L, A_contact, A_base, k, masses, h, A_fin). Mask init recomputes `R_cond`, `R_spread`, `R_ch` so changing `L` auto-recomputes spreading — see [[Spreading resistance — heat enters over the source, not the whole base]].
2. **Sweep matrix:** L {min, mid, max} × thermal-mass {min, mid, max}, run via `FastRestart`, capture steady `T_j` and transient `τ` per point.
3. **Present fins as an `(h, A)` contour of `R_conv`**, not a single predicted `h` — [[Only the h·A product matters for convective resistance]].
4. **Find the knee:** at what L / thermal mass does `T_j` stop improving? (L optimum ≈ 18.1 mm already.)

## Guardrails (from the validated write-up)
- Build Phase 2 **on the validated Simulink model** — no parallel MATLAB reimplementation.
- Keep `h` as the one fitted number; never bend a derived R to close the +1.89 K bias.
- Transient-only, valid ≤ ~300 s — no steady-state extrapolation.

## Phase 3 — TBD
Define once Phase 2 conclusions are in.

---
`Phase 2 method` · `Simulink mask` · `(h,A) contour` · `guardrails`
