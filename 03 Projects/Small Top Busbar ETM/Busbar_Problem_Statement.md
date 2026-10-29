---
tags: [project, CAE-CFD, busbar, ETM]
date: 2026-10-29
objective: "Characterize Ohmic heat generation in Small Top Busbar V1.0 vs older design under 120A load; determine thermal adequacy"
phase: "Section 5 complete (new design solved) — old design pending re-run at matched ambient; Section 6 open"
related: "[[small-top-busbar-etm]] [[busbar-thermal-fatigue]] [[engineering-workflow]]"
---

# Problem_Statement — Small Top Busbar ETM

**Objective:** Characterize Ohmic heat generation in the Small Top Busbar V1.0 geometry under 120A input (18 wirebonds × 6.67A each, 8mm std bond length) via Maxwell 3D → Icepak two-way coupling. Compare **absolute max terminal temperature** (not ΔT) against the old design to determine if the new geometry is thermally adequate.

**Scope note:** Standalone study — separate from [[busbar-thermal-fatigue]] (G-Bridge) work.

## Geometry comparison

| | Old | New |
|---|---|---|
| Terminal shape | Cylindrical boss | Rectangular block |
| Length | 15.2 mm | 15 mm |
| Cross-section | Ø15mm, 2° draft (~176.7 mm²) | 35.24×17mm (599 mm²) |
| Area ratio | — | ~3.4× old |

**First-principles expectation:** larger cross-section → lower current density/resistance at terminal → new design should run cooler. If sim shows otherwise, root-cause before changing geometry (mesh at rectangular corners, contact/transition region, current crowding) — don't jump to "change length" since lengths are already matched.

## Pass/fail criterion

New design max terminal temp ≤ old design max terminal temp, same load, same ambient.

**⚠️ Open flag:** New design solved at 27°C ambient. Earlier screenshots of this model showed 30°C stationary-wall temp used elsewhere in the session — confirm old design is (re-)run at the same 27°C ambient as new before the comparison is valid. Mismatched ambient invalidates a direct comparison.

## Methodology

Both old and new designs modeled with identical per-wirebond excitation (18×6.67A) and boundary conditions, two-way coupled Maxwell↔Icepak. Max terminal (sink) temperature compared directly — old is baseline. If new underperforms, optimization proceeds on terminal cross-section/geometry (lengths already matched, so length is not the lever).

## Software & Environment

- ANSYS 2025 R2 — Maxwell 3D (DC conduction, 18-bond excitation) two-way coupled to Icepak (steady-state thermal)
- Geometry: SOLIDWORKS 2026 → Parasolid import
- Material: Aluminium alloy, cast 383.0 (σ = 1.333×10⁷ S/m, PTC thermal modifier 1/(1+0.0039·(T−20)), k = 95.9 W/m·K)
- Hardware: CAE server, Ryzen 9 4000-series (= PC1 per [[ways-of-working]])

## Calc & Theory

- Governing physics: DC Joule heating, P = I²R per conduction path; steady-state conduction-convection coupling
- Key derived check: cross-sectional area ratio (new:old ≈ 3.4:1) as independent sanity check against simulated max-temp ratio
- Material resistivity is temperature-dependent (PTC) — two-way coupling required, confirmed working (validated earlier in standalone busbar run: 0.127W total loss at 120A, consistent with cast-383 resistivity and geometry)

## End Result & How It's Studied

- Primary output: max terminal temp, old vs new, single-point comparison at 120A
- Secondary output: total ohmic loss (W) per design, cross-checked against area reasoning
- Study method: direct side-by-side Field Overlay comparison (Ohmic-Loss, Temperature), same color scale, same current, same ambient

## End Result For

*(Open — Section 6 not yet confirmed. Candidates: feeds [[busbar-thermal-fatigue]] G-Bridge integration / separate design freeze-sign-off / standalone geometry validation before CAD release.)*
