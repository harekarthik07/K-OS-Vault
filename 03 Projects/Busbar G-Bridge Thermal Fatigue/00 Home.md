---
type: project_home
project: Busbar G-Bridge Thermal Fatigue
objective: "Thermal-fatigue life of the G-Bridge ABS+PC housing under the electrical duty, via Maxwell 3D → Icepak → Mechanical."
status: active
started: 2026-09-01
domain_primary: Solid Mechanics
domain_secondary: [Thermal Management, Heat Transfer, CFD]
current_phase: Phase 5
---

# Busbar G-Bridge Thermal Fatigue

> Thermal-fatigue life of the **G-Bridge plastic housing** (`NVA5P1MCP0090_A_GBridge`) and its busbars, by chaining **Maxwell 3D → Icepak → Mechanical** so EM loss drives temperature and temperature drives cyclic CTE-mismatch strain. Separate assembly and chain from the [[ETM For Heatsink and IGBT/00 Home|IGBT/heatsink ETM work]].

## Sections
- [[Daily Log]]
- [[Questions]]
- Experiments/ — one note per solve/verification run
- Results/    — verified fields, stress/strain verdicts, fatigue estimates
- Concepts/   — the four anchor docs + incubating knowledge
  - [[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]] — physics chain, assembly, scope boundary
  - [[IcepakThermalBridge_Progress_Log]] — why the native link failed, how the ACT bridge was built
  - [[IcepakThermalBridge_Flowchart]] — how the tool works (batch AEDT, per-body import)
  - [[Thermal_Fatigue_Approach_and_TODO]] — the forward plan (transient, structural, fatigue)
- Resources/  — datasheets (ABS+PC grade, cast 383.0), moulding spec

---

## Roadmap

Phase status legend: ✅ done · 🟢 in progress · ⚪ queued/TBD

### ✅ Phase 1 — Maxwell 3D EM loss (done)
`#maxwell #ac-conduction #dc-conduction #joule-loss`
**Objective:** Solve the electromagnetic loss that drives the whole chain.
**Tasks:**
- [x] Maxwell 3D AC + DC conduction loss solve (Joule / ohmic)
- [x] Confirm busbar material — **cast 383.0 aluminium** confirmed 2026-09-24 (not copper) ✅

### ✅ Phase 2 — Icepak thermal solve (done)
`#icepak #cht #steady-state #temperature-field`
**Objective:** Turn the loss field into a temperature field across all 6 solids.
**Tasks:**
- [x] Icepak steady-state CHT solve — 30.5–52.5 °C across all 6 solids
- [x] Produce the cold and hot thermal states used by the two-state structural step (Phase 4)

### ✅ Phase 3 — Icepak → Mechanical transfer tool (done)
`#act-extension #imported-body-temperature #batch-aedt`
**Objective:** Get the Icepak field reliably onto Mechanical bodies, via the custom `IcepakThermalBridge` ACT tool (native Workbench link would not populate).
**Tasks:**
- [x] Build `IcepakThermalBridge` — batch headless AEDT export (no COM/gRPC live-session dependency)
- [x] Object-mesh field export (no bounding-box air contamination) + point decimation
- [x] Per-body idempotent import — one `ImportedLoadGroup` each, safe re-runs
- [x] Named Selection → body name → GeoBody ID scoping fallback
- [x] Single-body (`G_Bridge`) verified against the Icepak contour
- [x] Re-verified end-to-end (batch mode) for all 6 bodies — `AC_Busbar_A/B/C`, `DC_Busbar_A/B`, `G_Bridge`
- [ ] Set `expect_min_c` / `expect_max_c` in Settings so future runs self-validate
- [ ] (tool backlog) add m/mm sanity assert to the import step — warn on 1000× coord-vs-unit mismatch

### ✅ Phase 4 — Structural cold↔hot + strain extraction (done 2026-09-26)
`#static-structural #two-load-step #mesh-convergence #strain-range`
**Objective:** Solve the cold↔hot two-state structural problem, prove the hotspot is converged (not a singularity), and extract the fatigue input.
**Outcome (Case 1, DC 120 A / AC 200 A, mesh-converged):** G_Bridge peak stress **45 MPa** at the boss fillet (converged 37.8→46.0→45.1, <2 %); peak elastic **Δε = 0.0208 (2.08 %)** per cycle. Thermal strain 3.62e-3; total deformation 0.122 mm; busbar 129 MPa dismissed as a singularity. Full log: [[EOD_2026-09-26_GBridge_Phase4_Closure]].
**Tasks:**
- [x] Two load steps set up — Step 1 zero-strain reference, Step 2 hot instant (Step 2 strain = the range directly)
- [x] Mesh convergence confirmed on the G_Bridge boss-fillet hotspot; busbar singularity dismissed
- [x] Extract Δε at the hotspot — 0.0208 (Case 1)
- [x] Validity caveat logged: 45 MPa ≈ ABS+PC yield & 2.08 % at/past elastic limit → linear-elastic kept for the first (conservative) pass; upgrade to elastic-plastic only if life comes out alarmingly short

### 🟢 Phase 5 — Thermoplastic fatigue life (active, blocked on ABS+PC grade)
`#polymer-fatigue #strain-life #low-cycle #comparative`
**Objective:** Turn Δε into a defensible fatigue conclusion. This is **low-cycle fatigue** (hundreds–thousands of cycles at 2 % amplitude), not high-cycle.
**Fatigue input (from Phase 4):** Δε = **0.0208** per power cycle at the G_Bridge boss fillet.
**Tasks:**
- [ ] **Identify the ABS+PC grade** of the G_Bridge (Bayblend / Cycoloy / other) — blocks everything below
- [ ] Path A — supplier / CAMPUS / Material Data Center ε–N curve at temperature → **absolute life** at Δε = 0.0208 (custom post, **not** the metal-only Coffin-Manson Fatigue Tool)
- [ ] Path B — no grade data → run **Case 2 (50 A)** and give a **comparative** Case 1 vs Case 2 conclusion (honest, no invented number)
- [ ] Path C — generic polymer model → order-of-magnitude life only, flagged as such
- [ ] Write up → `Results/YYYY-MM-DD Phase 5 …`

## Open Concepts (incubating)
```dataview
LIST FROM "03 Projects/Busbar G-Bridge Thermal Fatigue/Concepts"
WHERE status = "incubating"
```

## Background knowledge
Foundational explainers behind this study (in `04 Knowledge`):
- [[Fatigue — cyclic damage and life]] — what fatigue is, S-N vs strain-life
- [[Temperature-dependent fatigue of polymers]] — why room-temp curves lie, Tg
- [[Creep and stress relaxation]] — the fixed-strain relaxation case
- [[Material properties required for a fatigue study]] — every input and why
- [[Electro-Thermal Modelling (ETM) and the multiphysics hybrid approach]] — what ETM is, one-way vs two-way coupling

## Atlas Connections
- [[Solid Mechanics]]
- [[Thermal Management]]
- [[Heat Transfer]]
- [[CFD]]
