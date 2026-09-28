---
concept: Heat-Transfer Module (Vantage)
project: Raptee Vantage
domain: Thermal Management
status: incubating
created: 2026-09-03
sources: ["[[Daily Log#2026-09-03]]"]
related: ["[[MC_HS_ETM_I1]]", "[[ETM ported into Vantage]]", "[[CHT Case Configurator — Math Behind Every Section]]", "[[Inverter Analytical Thermal Loss Model (SVPWM)]]"]
tags: [vantage, heat-transfer, ETM, CFD, thermal, second-brain]
---

# Heat-Transfer Module — Build & Decisions

> [!abstract] What this is
> A new **standalone module** in Raptee Vantage (`/heat-transfer`, Next.js) that ports
> the heatsink/IGBT thermal work — the CFD CHT configurator, the 1D/2-node Cauer ETM,
> the SVPWM inverter-loss chain, and a fan PQ debugger — into an interactive web tool.
> It does **not** touch the production bike PASS/FAIL pipeline. This note is the running
> record of what's built and *why*, so the decisions survive the session.

## What it is
An engineering calculator + simulator, not a QC suite. Ungated like `/help`.

| Layer | Where | Does |
|---|---|---|
| Client (JS) | `vch-next-frontend/app/heat-transfer/lib/thermal.js` | Instant steady algebra — Re/Pr/Gr/Ra/Ri, regime, setup advisor, Nu→h, fan PQ verdict, post-CFD h extractor |
| Backend | `heat_transfer_backend/` | Only the *new* math: SVPWM losses, transient 2-node Cauer ODE, case persistence |
| API | `/api/heat-transfer/*` in `fastapi_server.py` | `etm`, `calibrate-h`, `simulate`, `cases` |

Backend files: `etm_loss.py` (SVPWM losses — reproduces the doc §7 worked example),
`heat_transfer_sim.py` (2-node Cauer + `calibrate_h`, the `Sweep_h.m` port),
`heat_transfer_db_manager.py` (`cases`, WAL + timeout=60). All have `__main__` self-checks that pass.

UI tabs: Regime · Governing Numbers · CFD Setup Advisor · Pre-run h · 1D ETM Model ·
Transient · **ETM (bike run)** · Post-CFD Extractor · Fan PQ Debugger. Next up: a
**Network Map** (interactive Simulink-style schematic) and a re-skin to the suite theme.

## The model chain (parity target = [[MC_HS_ETM_I1]])
Bike run `ID,IQ,Vdc` → `Ipk=√(ID²+IQ²)` → SVPWM losses ([[Inverter Analytical Thermal Loss Model (SVPWM)]])
→ heat `P` → 2-node Cauer (junction `C_plate` → `Rjc` → heatsink `C_hs` → `R_conv` → ambient)
→ `T_junction(t)` vs measured `IGBT_Temp`, deration verdict at **95 °C**. `R_conv = 1/(h·A)`,
`C = m·cp` (the `Reference.xlsx` Derived-Calcs formulae).

## Decisions (the "why")
- **Hybrid client/server, one formula per layer.** Cheap steady algebra stays client-side
  (instant); heavy/stateful math (transient ODE, persistence) is server-side. No formula
  is duplicated across languages.
- **No assumed values.** The engine hardcodes *formulae only*; every magnitude is a user
  input. Reference-sheet values load only on an explicit click. Driven by the fact that the
  reference sheets themselves carry live disputes (below).
- **Reverse-recovery loss follows the DOC** (`Prr = fsw·Err·(Vdc/Vref)/π`, no current
  scaling), not the ETM-project note's variant — user said reference the doc.
- **Input source = uploaded per-bike xlsx** (`Time, ID, IQ, IGBT_Temp, BMS_cumulative_totv`),
  NOT the dyno DB — dyno stores no current channels.

## Open items (surfaced in-UI, not resolved silently)
- **Rjc per-die vs per-module** — 6× swing on `T_junction` (ETM sheet Open Item #1).
- **C_plate 490 (calibrated) vs 500 (m_j·cp_j)** — reconcile before next fit.
- **Which P drives the node** — `P_switch`, `P_inv=6·P_switch`, or per-die.
- **Vdc source** — constant vs the per-sample `BMS_cumulative_totv` column.

## Ops notes
- Live `:8001` backend must **reload** to expose `/api/heat-transfer/*` (was verified on a
  throwaway `:8009` instance). Login gate blocks automated UI verification.
- Code currently lives in the **main working copy**, not the `heat-transfer-viz-module`
  worktree branch — reconcile before committing.

## Atlas
- [[ETM ported into Vantage]] · [[MC_HS_ETM_I1]] · [[CHT Case Configurator — Math Behind Every Section]]
- [[Thermal Management]] · [[Heat Transfer]]
