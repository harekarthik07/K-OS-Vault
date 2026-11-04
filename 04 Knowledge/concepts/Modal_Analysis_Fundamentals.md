---
tags: [Ideaverse, knowledge, modal-analysis, vibration, FEA, engineering-concepts]
aliases: [Modal Analysis, Eigenvalue Analysis, Natural Frequency Analysis]
date: 2026-10-31
type: knowledge-page
domain: Solid Mechanics
related: "[[CPP_V2_Problem_Statement]] [[CPP_V2_Approach_and_TODO]] [[Harmonic_Response_Fundamentals]]"
---

# Modal Analysis — Core Concepts

> [!info] Ideaverse knowledge page
> Reusable engineering concept, captured from [[CPP_V2_Approach_and_TODO|CPP V2]] work. Applies to any structural vibration problem, not just CPP — backlink from here whenever modal analysis comes up in other projects.

## A. What it actually is (intuition first)

Every structure has a "natural way it wants to shake" — push it and let go, it vibrates at specific frequencies in specific shapes, same way a guitar string always rings at the same pitch no matter how you pluck it. Modal analysis finds those frequencies and shapes. **No load is applied** — it's a pure property of the structure's stiffness and mass distribution, like finding a person's resting heart rate rather than how fast it beats after running.

## B. The physics behind it

For any structure discretized into mass/stiffness (FE model), the governing equation of free, undamped vibration is:

**[M]{ẍ} + [K]{x} = 0**

Assume harmonic motion x = φ·sin(ωt), substitute in:

**([K] − ω²[M]){φ} = 0**

This is an eigenvalue problem. Non-trivial solutions exist only at specific ω values — the **natural frequencies**. Each ω has a corresponding **{φ}** — the **mode shape** (relative deformation pattern, not absolute — mode shapes are normalized, magnitude is meaningless, only the *shape* matters).

**SDOF intuition (worked):** single mass-spring, k = 1000 N/m, m = 1 kg
- ωₙ = √(k/m) = √(1000/1) = 31.62 rad/s
- fₙ = ωₙ/2π = 31.62/6.283 = **5.03 Hz**

Stiffer → higher frequency. Heavier → lower frequency. That's the entire intuition behind every mode a structure has — ribs/thickness push frequencies up, added mass pulls them down.

## C. Why we run it (not just a box to check)

1. **Resonance screening** — compare natural frequencies against the operating/excitation band (e.g. the 7–200 Hz AIS-156 sweep). A mode inside the band is a candidate for large amplification.
2. **It's the engine behind Harmonic Response** — see [[Harmonic_Response_Fundamentals]]. Mode Superposition solves the forced response as a weighted sum of mode shapes, not by re-solving the full FE model at every frequency. Modal analysis is the prerequisite, not a separate check.
3. **Design guidance** — tells you *which* geometry feature to change to move a problem frequency, because the mode shape shows exactly where the structure is flexing.
4. **Cheap and load-independent** — run once, reuse for any load case (shaker test, road load, whatever) since frequencies/shapes don't depend on load magnitude.

## D. Participation Factor — the piece most people skip past

**The gap it fills:** a mode can sit right inside the excitation band and still barely respond — *if* that mode's shape doesn't align with the excitation direction. Participation factor tells you how much a mode actually couples with a given excitation direction.

**Formula:**

**Γᵢ = ({φᵢ}ᵀ [M] {D}) / ({φᵢ}ᵀ [M] {φᵢ})**

where {D} is the excitation direction vector (e.g. unit vector in Z for a vertical sine-sweep test).

**Effective mass** for mode i in that direction = Γᵢ² × modal mass. This is the number that actually matters — express it as **% of total structural mass** responding through that mode.

**Worked example (illustrative, 2-mode system, Z-excitation):**
Mode 1 shape φ₁ = {1.0, 0.8}, mode 2 shape φ₂ = {1.0, −2.5}, masses m = {2, 1} kg, excitation direction D = {1, 1} (uniform Z). The shapes are mass-orthogonal, as real modes must be: φ₁ᵀ[M]φ₂ = 1.0×2×1.0 + 0.8×1×(−2.5) = 0.

- Γ₁ = (1.0×2×1 + 0.8×1×1) / (1.0²×2 + 0.8²×1) = (2 + 0.8) / (2 + 0.64) = 2.8 / 2.64 = **1.06**
- Γ₂ = (1.0×2×1 + (−2.5)×1×1) / (1.0²×2 + 2.5²×1) = (2 − 2.5) / (2 + 6.25) = −0.5 / 8.25 = **−0.061**
- Effective mass₁ = Γ₁² × modal mass₁ = 1.06² × 2.64 = **2.97 kg** → 2.97/3 total = **99%** → mode 1 carries almost all the Z response
- Effective mass₂ = 0.061² × 8.25 = **0.03 kg** → 0.03/3 total = **1%** → relatively minor
- Check: 2.97 + 0.03 = 3 kg. Effective masses across all modes must add up to the total mass.

→ Even though both modes exist, mode 1 dominates the Z-direction response. That's the entire point of the participation summary.

## E. Reading the Participation Summary table (Ansys output)

Columns: Mode | Frequency | Participation Factor (X, Y, Z, ROTX, ROTY, ROTZ) | Ratio/Effective Mass | Cumulative Mass Fraction.

**How to use it:**
- A mode labeled pure "Rotation X" will have **near-zero participation in Z** (vertical excitation) — it can sit inside the excitation band and still be low-risk, because it barely couples with the applied shake.
- **Frequency-in-band alone is not a resonance verdict** — always cross-check against Z-participation before flagging a mode as dangerous.
- Cumulative effective mass should reach **~80–90%+** by the modes included — if it's not climbing, a dominant mode is missing or the frequency range cap is too low.
- This table is the standard root-cause diagnostic for "why did deflection change between two design iterations" — compare Z-participation of the governing mode across iterations, not just its frequency.

## Project application → [[CPP_V2_Problem_Statement]]

- Both A1 (145.99 Hz) and V2 (162.84 Hz) 1st modes fall inside the 7–200 Hz AIS-156 band — both designs are resonance-exposed by frequency alone.
- Both modes are labeled "Rotation Y" in the modal summary — participation summary not yet pulled; this is the next diagnostic step for the V2 deflection regression (see [[CPP_V2_Approach_and_TODO]] TODO).

## See also
- [[Harmonic_Response_Fundamentals]] — how modal results feed into forced response (mode superposition math, sweep theory)
- [[CPP_V2_Problem_Statement]]
- [[CPP_V2_Approach_and_TODO]]
