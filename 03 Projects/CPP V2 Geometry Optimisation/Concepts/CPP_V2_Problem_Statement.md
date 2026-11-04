---
tags: [CPP, AIS-156, vibration, modal, harmonic-response, V2]
date: 2026-10-30
objective: "CPP geometry optimisation — V2 from A1 baseline"
phase: "Section 1 — Objective"
related: "[[CPP_V2_Approach_and_TODO]] [[CPP_V2_Progress_Log]] [[CPP_V2_Flowchart]]"
---

# Cell Pattern Plate (CPP) — V2 Geometry Optimisation — Problem Statement

## 1. Objective

> [!tldr] Objective
> Redesign the Cell Pattern Plate (A1 → V2) to **reduce weight while improving/maintaining stiffness**, driven by manufacturing issues in the original pattern. Must continue to clear AIS-156 vibration qualification.

- **Driver:** entire cell pattern redesigned in V2 to avoid manufacturing-based issues in the A1 pattern (per rev history).
- **Objective function:** maximise stiffness-per-gram and stress margin — not raw stress reduction alone. Mass is currently unchanged (0.711 kg) between A1 and V2, so weight reduction is still pending in the geometry iteration.
- **Pass/fail gate:** AIS-156 sine sweep — 7–200 Hz logarithmic sweep, 15 min/cycle, 12 cycles vertical — survive without resonance-induced crack, and stress must stay within yield (65 MPa) and endurance (32.5 MPa) limits of Covestro 3040 PC FR ABS.

## Baseline finding (A1 vs V2, as solved)

| Design | Max Stress | Yield margin | Endurance margin | Max Deflection |
|---|---|---|---|---|
| A1 (baseline) | 13.635 MPa | 4.77× | 2.38× | 0.0814 mm |
| V2 (new) | 13.664 MPa | 4.76× | 2.38× | 0.6940 mm |

> [!warning] Open problem
> Stress is essentially unchanged (+0.2%) between A1 and V2, but **V2's peak deflection is ~8.5× higher**. Same failure location on both (mount/boss area, likely untouched by the redesign). This is a stiffness regression, not a strength regression — margins still pass, but it needs explaining and fixing before V2 is finalised. See [[CPP_V2_Approach_and_TODO]] for diagnosis plan.
