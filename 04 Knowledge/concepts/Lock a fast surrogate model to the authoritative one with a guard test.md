---
type: concept
concept: Lock a fast surrogate model to the authoritative one with a guard test
domain: CAE
status: budding
created: 2026-09-28
origin_project: ETM For Heatsink and IGBT
aliases: ["fast twin guard test", "surrogate model lock", "two copies of the physics"]
sources: ["[[EOD_2026-09-28_ETM_1D_Thermal_Tool]]"]
tags: [cae, verification, modelling, surrogate, method]
related: ["[[Cauer Model Calibration — fit what you cannot derive]]"]
---

# Lock a fast surrogate model to the authoritative one with a guard test

## One-line idea
When you build a **fast surrogate** of a slow authoritative model (for live UI, sweeps, optimisation), you now have **two copies of the physics** — keep them from silently diverging with an automated **guard test** that fails on any mismatch.

## Intuition first
The moment a second implementation exists, the two can drift: someone edits the physics on one side, the other quietly lies. A cheap, deterministic test comparing both on a known case is the only thing that keeps the surrogate trustworthy.

## Method
1. Pick an authoritative reference (validated, slow) — here `MC_HS_ETM_I2.slx`.
2. Build the fast twin (`thermal_core.m`, 2-node RK4) for speed the reference can't give.
3. Write a guard (`test_core.m`) comparing twin vs reference on a fixed case; set a tight tolerance.
4. **Re-run the guard after ANY physics change to either side.** Treat a failure as a stop.

## Worked example (ETM tool)
`thermal_core` reproduces the Simulink reference to **0.000 K** (RK4 vs closed-form) and the loss chain to **0.05 W** on run 44. Live sliders need microsecond evaluations — impossible in Simulink — so the twin is necessary; the guard is what makes it safe. This was the deliberate mitigation for the "don't fork the validation" guardrail.

## Validity window & invalidation triggers
- Applies to any surrogate: 1D reduced-order, ROM, response-surface, or reimplementation in a faster runtime.
- Breaks down if the guard case isn't representative — pick a case that exercises the shared physics.

## How we verify it
The guard test itself is the verification; CI-style, it must pass before the surrogate is used.

## Gotchas
- A single guard case can pass while an untested regime diverges — add cases as the surrogate's use widens.

## Where used
- [[EOD_2026-09-28_ETM_1D_Thermal_Tool]] · [[1D Thermal Design Tool — spec & flowchart]]

---
`fast twin` · `guard test` · `surrogate lock` · `two copies of the physics` · `< 0.01 K`
