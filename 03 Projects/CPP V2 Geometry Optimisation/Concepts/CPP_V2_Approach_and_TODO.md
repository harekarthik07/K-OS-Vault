---
tags: [CPP, AIS-156, vibration, modal, harmonic-response, V2]
date: 2026-10-30
objective: "CPP geometry optimisation — V2 from A1 baseline"
phase: "Section 2-4 — Methodology, Software & Environment, Calc & Theory"
related: "[[CPP_V2_Problem_Statement]] [[CPP_V2_Progress_Log]] [[CPP_V2_Flowchart]]"
---

# CPP V2 — Approach & TODO

## 2. Methodology

> [!note] Pipeline
> Modal (constrained) → Harmonic Response (mode superposition) → compare A1 vs V2 → diagnose deflection delta via mode-shape correlation → iterate geometry locally.

1. **Modal analysis** — Fixed Support (mount faces) + Frictionless Support (physical stopper-to-plate contact at mounting points, linearised — real contact is one-directional/separable, this is a known simplification). Max Modes = 20, undamped, Direct solver.
2. **Harmonic Response** — Mode Superposition, log frequency spacing 7–200 Hz, Cluster Number 3, 2% modal damping (ζ = 0.02) applied identically to both designs. No "Base Excitation" option used — instead, base held at Fixed Support (zero motion) + inertial acceleration load applied to all bodies (D'Alembert equivalence). Valid for stress and relative-deformation results; deformation output is relative to the fixed base, not absolute.
3. **Load profile** — per AIS-156 table: 7–18 Hz flat at 10000 mm/s² (~1.02g), 25–200 Hz flat at 20000 mm/s² (~2.04g), vertical (Z) axis. Entered as per spec table (confirmed, no ramp segment needed).
4. **Comparison basis** — same BCs, same mesh density/quality, same damping, same load profile across A1 / V2 / 9.1.2, so FRF overlay is apples-to-apples.
5. **Diagnosis of V2 deflection regression** — pull Frequency Response plot at the peak-deflection mount, find the governing frequency, cross-check against modal mode shape at/near that frequency: local boss/rib flex vs global plate mode vs resonance-proximity/participation-factor shift.

## 3. Software & Environment

- **Solver:** ANSYS Workbench 2026 R1 — Modal + Harmonic Response (Mode Superposition).
- **Geometry cleanup:** ANSYS Discovery (regular geo cleanup).
- **Material:** Covestro 3040 PC FR ABS — E = 2700 MPa, Yield = 65 MPa, Endurance = 32.5 MPa, Mass (both designs) = 0.711 kg.
- **Mesh:** ~967,120 elements / 1,607,043 nodes (both A1 and V2, same density for fair comparison).
- **Source report:** `BBP0050-VIB-B.2.xlsx` (Project logs folder) — contains Modal summary + Harmonic mount-wise stress/deflection tables for A1, V2, and interim iteration 9.1.2.

## 4. Calc & Theory

- **Base-excitation equivalence:** holding the base at Fixed Support (zero motion) and applying the required base acceleration as a body-force/inertial load on the whole structure reproduces the harmonic response relative to a moving base, by Newtonian frame equivalence — valid because stress/strain depend only on relative deformation, not on which frame displacement is measured in.
- **Margin calcs:**
  - Yield margin = Sy / σ_max
  - Endurance margin = Se / σ_max
- **Resonance risk:** both A1 (145.99 Hz) and V2 (162.84 Hz) 1st modes fall inside the 7–200 Hz excitation band — both designs are resonance-exposed, not just V2.
- **9.1.2 (interim) flag:** peak stress 33.082 MPa → endurance margin 0.98× — **fails** endurance limit. Not currently the lead candidate; noted for reference only.

## TODO

- [ ] Pull Frequency Response data at the V2 peak-deflection mount — identify governing frequency.
- [ ] Cross-check that frequency against V2's modal mode shapes — classify local vs global vs participation-factor cause.
- [ ] Confirm Directional Deformation axis (Y) actually corresponds to the vertical excitation direction (Z) in this model's local CS, or re-pull using Total Deformation.
- [ ] Based on diagnosis, apply targeted geometry fix (local gusset/rib at boss, rib re-orientation, or global retune) — not a blanket thickness increase.
- [ ] Re-solve V2 iteration, re-compare stress + deflection + mass against A1.
- [ ] Update `BBP0050-VIB-B.2.xlsx` report with final verified numbers for all three designs.
