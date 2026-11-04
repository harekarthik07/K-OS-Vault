---
type: project_home
project: CPP V2 Geometry Optimisation
objective: "Redesign the Cell Pattern Plate (A1 → V2) to reduce weight while maintaining or improving stiffness, and still clear AIS-156 vibration."
status: active
started: 2026-10-30
domain_primary: Solid Mechanics
domain_secondary: []
current_phase: Phase 1
---

# CPP V2 Geometry Optimisation

> Redesign the **Cell Pattern Plate** (A1 → V2) to **reduce weight while maintaining or improving stiffness**, driven by manufacturing issues in the A1 pattern, and still clear **AIS-156** vibration qualification.

**Files on disk:** `D:\Hare Karthik\Mechanical\cell-pattern-plate-V2` — Ansys project `BBP0050-VIB-V2.wbpj`, report `Project logs\BBP0050-VIB-B.2.xlsx`.

## Sections
- [[03 Projects/CPP V2 Geometry Optimisation/Daily Log|Daily Log]]
- [[03 Projects/CPP V2 Geometry Optimisation/Questions|Questions]]
- Experiments/ — one note per solve or verification run
- Results/    — verified numbers and design verdicts
- Concepts/   — the four anchor docs + incubating knowledge
  - [[CPP_V2_Problem_Statement]] — objective, pass/fail gate, A1 vs V2 baseline
  - [[CPP_V2_Approach_and_TODO]] — method, software, theory, TODO
  - [[CPP_V2_Flowchart]] — the analysis and iteration loop
  - [[CPP_V2_Progress_Log]] — what was found and corrected, by date
- Resources/  — datasheets, AIS-156 references

---

## Roadmap

Phase status legend: ✅ done · 🟢 in progress · ⚪ queued/TBD

### 🟢 Phase 1 — Diagnose the V2 deflection increase (started 2026-10-30)
`#modal #harmonic-response #AIS-156`
**Objective:** Explain why V2 peak deflection is about 8.5× higher than A1 while stress is almost unchanged.
**Tasks:**
- [ ] Pull Frequency Response data at the V2 peak-deflection mount and identify the governing frequency
- [ ] Cross-check that frequency against the V2 mode shapes: local, global or participation-factor cause
- [ ] Confirm whether Directional Deformation axis (Y) matches the vertical excitation direction (Z), or re-pull using Total Deformation

### ⚪ Phase 2 — Targeted geometry fix
`#geometry #stiffness #mass-reduction`
**Objective:** Apply a targeted fix based on the diagnosis, not a blanket thickness increase.
**Tasks:**
- [ ] Apply the fix (local gusset or rib at the boss, rib re-orientation, or global retune)
- [ ] Re-solve the V2 iteration and re-compare stress, deflection and mass against A1

### ⚪ Phase 3 — Final report
`#report`
**Objective:** Record final verified numbers.
**Tasks:**
- [ ] Update `BBP0050-VIB-B.2.xlsx` with final verified numbers for all three designs

---

## Open Concepts (incubating)
```dataview
LIST FROM "03 Projects/CPP V2 Geometry Optimisation/Concepts"
WHERE status = "incubating"
```

## Background knowledge
Foundational explainers behind this study (in `04 Knowledge`):
- [[Modal_Analysis_Fundamentals]] — natural frequencies, mode shapes, participation factor
- [[Harmonic_Response_Fundamentals]] — forced response, sine sweep, the math with CPP numbers

## Atlas Connections
- [[Solid Mechanics]]
