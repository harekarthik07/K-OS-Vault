---
type: project_home
project: Vantage VE
status: active
started: 2026-10-10
objective: Engineering-tools platform (Vantage VE) — Powertrain tool + subject-wise Calculator Library, cloned from the Thermal tool
domain_primary: Motor Control
domain_secondary: [Vibrations, Solid Mechanics, Heat Transfer, CFD]
current_phase: Phase 1
---

# Vantage VE

> Second platform (split from production Vantage) for engineering / design / R&D tools. This project tracks the **Powertrain tool** and the subject-wise **Calculator Library** — both cloned from the existing Thermal tool's structure.

## Sections
- [[Daily Log]] — what we did / learned / next
- [[Questions]] — open + answered
- [[Workflow]] — how Claude + this vault work together
- Concepts/ — durable design: [[Powertrain Tool]], [[Calculator Library]]
- Experiments/ — one note per investigation
- Results/ — what shipped
- Resources/ — datasheets, references

## Core concepts
- [[Powertrain Tool]] — Phase 1 performance curves → Phase 2 NVH gear-health
- [[Calculator Library]] — one registry-driven calculator shell, many subjects

## The platform (shared with Thermal tool)
Lives in its own repo: `D:\Hare Karthik\Dashboard\Streamlit\Raptee-Vantage-VE`
(sibling of the main Vantage repo). One app, many tools. Shared JWT auth, deploy,
theme. Frontend Next.js **port 3200**, backend FastAPI **port 8003** (loopback).
Add a tool = new `# ==== X TOOL ====` banner + `sys.path` to its engine.
Interpreter is **`py -3.14`** (not PATH `python`). See memory `project_vantage_ve`.

Full brainstorm lives in the repo: `PLANNING_powertrain_and_calc_library.md`.

---

## Roadmap

Phase status legend: ✅ done · 🟢 in progress · ⚪ queued/TBD

### 🟢 Phase 1 — Powertrain: performance & curves (started 2026-10-10)
`#powertrain #motor-control`
**Objective:** turn a dyno torque/RPM log + bike spec sheet into torque curve, power curve, wheel tractive effort, and road-load → top speed. Formulae hardcoded, every number user-supplied.
**Tasks:**
- [x] Clone Thermal tool structure (engine package + server banner + page.js)
- [x] Build engine `powertrain_engine/powertrain.py` + passing self-check
- [x] Wire `/api/powertrain/analyze`; manifest `ready:True` (backend verified)
- [x] Build frontend `app/powertrain/page.js` (inputs → formula → plots)
- [x] Shipped to `/powertrain` (2026-10-14)
- [ ] Dyno-log CSV/XLSX upload + read from Dyno DB (paste works today)
- [ ] Collect one real bike spec sheet + sample dyno log to validate

### ✅ Platform work (2026-10-14 → 10-27)
`#platform #security`
- [x] Road Suite moved into VE (backend + `/road`)
- [x] Admin Console (users, sessions, audit, system)
- [x] Own `ve-session` cookie; default-deny API; login lockout
- [x] Home console, light/dark contrast sweep, T30 model 23× smaller
- [x] Deploy hardening (pm2, build-abort)
- [ ] HTTPS via a public raptee.com cert (self-CA attempt reverted)

### ⚪ Phase 2 — Calculator Library shell + seed calcs
`#calculators #engineering-mechanics`
**Objective:** lift Phase-1 pattern into a registry-driven shell; seed 5 calcs (cantilever UDL + UVL, Reynolds, shaft diameter, one heat-transfer case).
**Tasks:**
- [ ] Extract calculator shell (registry row = one calc)
- [ ] "Show working steps" toggle (engineer ↔ student view)
- [ ] Seed 5 calculators with units + validity-range warnings

### ⚪ Phase 3 — Powertrain: NVH gear-health
`#nvh #vibrations`
**Objective:** vibration/acoustic log → RMS, crest factor, gear-mesh freq, order tracking → PASS/FAIL. Reuses golden-limit + Teams machinery.
**Tasks:**
- [ ] Confirm vibration/acoustic log format
- [ ] Define golden limits per metric

---

## Open Questions
```dataview
LIST FROM "03 Projects/Vantage VE"
WHERE type = "questions"
```

## Atlas Connections
- [[Motor Control]]
- [[Vibrations]]
- [[Solid Mechanics]]
- [[Raptee Vantage]]
