---
type: project_home
project: ETM For Heatsink and IGBT
status: active
domain_primary: Thermal Management
domain_secondary: [Power Electronics]
current_phase: Phase 2
---

# ETM For Heatsink and IGBT

> Electro-thermal model coupling IGBT loss calculation with heatsink thermal network.

## Sections
- [[Daily Log]]
- [[Questions]]
- Experiments/
- Results/
- Concepts/ — 5 concepts currently incubating (see below)
- Resources/

---

## Roadmap

### ✅ Phase 1 — 1D Cauer baseline (2026-08 → 2026-09-01)
`#matlab #1D-cauer #baseline`
**Objective:** Build the 1D IGBT → HS → ambient Cauer network in MATLAB and verify it matches theory.
**Outcome:** Model behaves per theory. See [[2026-09-01 Phase 1 — 1D Cauer model matches theory]].

### 🟢 Phase 2 — Parametric sweep: thermal mass & L (in progress, started 2026-09-01)
`#parametric-sweep #thermal-mass #baseplate-L #T_junction`
**Objective:** For different thermal mass and different L (thickness under IGBT), run the 1D model and characterise how IGBT junction temperature behaves.
**Tasks:**
- [ ] Define sweep matrix — L values (min/mid/max) × thermal-mass values (min/mid/max)
- [ ] Add sweep loop to MATLAB model (existing Phase 1 model as inner function)
- [ ] Run sweep — capture steady-state T_j and transient τ per point
- [ ] Plot T_j vs L (fixed thermal mass) and T_j vs thermal mass (fixed L)
- [ ] Identify the knee: at what L / thermal mass does T_j stop improving meaningfully?
- [ ] Write up conclusion → `Results/YYYY-MM-DD Phase 2 …`

### ⚪ Phase 3 — TBD
Define once Phase 2 conclusions are in.

---

## Open Concepts
```dataview
LIST FROM "03 Projects/ETM For Heatsink and IGBT/Concepts"
WHERE status = "incubating"
```

## Atlas Connections
- [[Thermal Management]]
- [[Power Electronics]]
- [[Heat Transfer]]
