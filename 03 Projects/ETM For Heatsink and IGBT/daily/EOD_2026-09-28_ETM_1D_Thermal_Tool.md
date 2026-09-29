---
type: eod
project: ETM For Heatsink and IGBT
date: 2026-09-28
objective: Close Part 1, then build the interactive 1D thermal design tool for the T30 MC heatsink
phase: Phase 2 — design tool (L-sweep + h–A map)
tags: [eod, thermal, matlab, app, T30, heatsink, etm]
related: ["[[00 Home]]", "[[ETM_Progress_Log]]", "[[1D Thermal Design Tool — spec & flowchart]]", "[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
---

# EOD — 2026-09-28 · ETM 1D Thermal Design Tool

## What we set out to do
Close out Part 1 (thermal budget + parameter derivation), then build the **1D thermal design tool** so heatsink / alloy / fin changes can be screened without running CFD every iteration.

## What we actually did
- **Part 1 closed** — full write-up (objective, parameter table, section-by-section derivation, transient solution, validation across 11 runs, validity envelope). See [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]].
- **ADC12 alloy comparison** — computed `Rhs` for the PDC alloy (k=92) as a design alternative.
- **Tool built, phase by phase with gates** — see the spec: [[1D Thermal Design Tool — spec & flowchart]].
  - `thermal_core.m` — two-node RK4 fast twin of the Simulink physics
  - `loss_from_idiq.m` — PhaseCurrents + analytical_loss chain, verbatim
  - `q_builder.m` — const / excel / manual Q modes, all returning `[t Q]`
  - `mc_thermal_app.m` — interactive uifigure app
  - `test_core.m`, `test_app_gate.m` — the guards
- **App features:** geometry sliders+boxes, alloy dropdown (LM25/ADC12/custom), 3-mode mass panel (split / total+split / thermal-direct) with live derived readout, 3 Q modes, SDI-style 2×2 linked plots with swappable signal dropdowns, two draggable cursors with a delta table and ΔTj/Δt rate, restore-defaults, **L-sweep** and **h–A map** windows.

## Results & numbers
**Gates — all passed:**
| Gate | Result |
|---|---|
| `thermal_core` RK4 vs closed-form | **0.000 K** |
| `loss_from_idiq` vs model P_inv (run 44) | **0.05 W** (463.8 vs 463.8) |
| App vs core (defaults) | Tj_peak **93.5**, Rhs **0.0319**, τ2 **425**, Rtot **0.1858** |
| Excel mode end-to-end (run 44) | loads; Tj_peak **91.6** on real P_inv profile |

**ADC12 (k=92) vs LM25 (k=150.6):** `Rhs 0.05216 vs 0.03191 (+63 %)`. Tj @240 s (492 W / 36 °C): **90.8 vs 83.0 °C**. Time to NTC 95 °C (492 W / 45 °C) drops **270 s → 198 s** — ADC12 fails the 4-min duty at hot ambient without an airflow offset (needs h 29.6 → ~34.4, +16 %).

**L-sweep:** `R_hs` minimum at **17.9 mm**; part is 18 mm — already optimal (spreading vs conduction cross right where the part sits). Matches the Phase-1 estimate (≈18.1 mm).

**h–A map (Tj peak, L=18 mm, 240 s):** corners `h10/A0.08 → 99.6`, `h70/A0.08 → 94.6`, `h10/A0.50 → 95.2`, `h70/A0.50 → 79.5`; current point `(29.59, 0.232) → 93.4`.

## Decisions made and why
- **Fit what you cannot derive.** Calibration knob moved from `Rhs` (derivable) to `h` (not derivable for this casting) — spread across 11 runs went **35 % → 4.9 %**.
- **+1.89 K bias left uncorrected** — near-constant offset (NTC on the DCB above the case node); bending `Rhs` to close it would re-fit a derived number. Model is ~2 K conservative.
- **Steady-state dropped** — 4-min tests, transient basis; extrapolating past 300 s with a never-measured C is indefensible.
- **App uses `thermal_core`, not Simulink** — live sliders need microseconds. Cost: two copies of the physics; `test_core.m` is the guard, re-run after ANY physics change to either side.
- **Sweeps as separate figure windows** (after a uitab container issue); **dTj/dt smoothed to 5 s** (raw derivative of noisy P_inv is meaningless).

## Learnings & theory
- #learning/concept — Fitting the right (non-derivable) parameter beats fitting a derivable one: `h` gave 4.9 % vs 35 % for `Rhs` on identical data → [[Cauer Model Calibration — fit what you cannot derive]]
- #learning/concept — For this 4-min duty the transient result is set by **total thermal mass**, not the node split (split ≈0.17 is low-sensitivity) → new
- #learning/concept — `R_hs(L)` has a real optimum where **spreading benefit** and **conduction penalty** cross (~17.9 mm here); thicker base is not monotonically better → new
- #learning/method — Keep a **fast twin locked to the authoritative model with a guard test** (`thermal_core` ⟷ `MC_HS_ETM_I2.slx`, `test_core < 0.01 K`) so a parallel reimplementation can't silently fork the validation → new
- #learning/concept — Fin design is a lever **map** `(h, A)`, not a single predicted `h`; 1D cannot predict `h` for new geometry (CFD/test only) → [[Only the h·A product matters for convective resistance]]

## Blocked & open
| # | Item | Impact |
|---|---|---|
| 1 | No cooldown data in any run | C never independently measured (CAD-derived only) |
| 2 | Junction-to-NTC resistance unpublished | +1.89 K bias cannot be quantified |
| 3 | h not predictive for new fin geometry | CFD still needed per design; 1D screens only |
| 4 | Loss split IGBT vs diode unmeasured | RthJC 0.02679–0.04167 (use latter for safety) |
| 5 | Run 43 starts ~50 s late | trigger offset, not blocking |
| 6 | Test-bench validation | future acceptance criterion, deferred |

## Next session starts with
- Run `test_core` + `test_app_gate` as the standing re-verification.
- Try the **L-sweep** and **h–A map** buttons; confirm L optimum ~17.9 mm and current point ~93.4 °C.
- Decide whether ADC12 is viable given the 198 s time-to-deration at hot ambient (cost/performance call, not modelling).
- Optional: save/load design configs to `.mat`.

## For Claude Code
MATLAB files (all on the path, alongside `MC_HS_ETM_I2.slx`): `thermal_core.m`, `loss_from_idiq.m`, `q_builder.m`, `mc_thermal_app.m`, `test_core.m`, `test_app_gate.m`. `thermal_core` is the single physics implementation for the app — any edit → re-run `test_core`. Validated set: `Rjc 0.02679 / Rcase-hs 0.00818 / Rhs 0.03190 / h_conv 29.59 / A_fin 0.232 / m_igbt 0.56264 / m_hs 2.75978 / cp 871`.
> Source of this EOD: `D:\Hare Karthik\Electrical\MC\MC_ETM_Model\Prj-Workflow\` (external working copy).

## Model & code reference (as-built, yesterday)
> Drop these three screenshots into `Attachments/` with the exact names below — the embeds resolve by name.

### Loss model — Simulink (`MC_HS_ETM_I2.slx`)
![[MC_ETM_Loss_Model.png]]
RUN_SEL = 8 snapshot (light load): `P_inv 5.716 W = 6·(P_igbt 0.6791 + P_diode 0.2735)`. Chain: `RUN_SEL → Run Select → IGBT-REF (id,iq,Vdc) → PhaseCurrents → analytical_loss (M=0.86, PF=0.40, fsw=10 kHz)`.

### Thermal network — Simscape
![[MC_ETM_Thermal_Network.png]]
Cauer ladder `Rjc | Rcase-hs | Rhs | Rconv,lat` with junction and heatsink masses. `T_junction = T_sim + Q·RthJC`, `RthJC = 0.02679` (use `0.04167` for safety claims). Limit `Tvj,op = 150 °C`.

### 1D design tool — delivered app
![[MC_ETM_1D_Tool_GUI.png]]
Defaults (LM25, 470 W const, 36 °C) @ 240 s: `T_ntc 80.9`, `T_j 93.5`, `T_fin 64.0`. Bottom readout `Rhs/Rtot/τ2/Tj_pk = 0.0319 / 0.1858 / 425 / 93.5`. Mass: `m_total 3.3224 kg`, split 0.170 → `m_hs 2.7576`, `m_igbt 0.5648`.

### Code — `analytical_loss.m`
```matlab
function [Pcond_T, Psw_T, Pcond_D, Psw_D, P_igbt, P_diode, P_inv] ...
        = analytical_loss(Irms, Vdc, M, PF, fsw)
%#codegen
% Analytical two-level VSI loss for FS200R07PE4, per switch position.
% Inputs:  Irms [A RMS], Vdc [V], M (0..1.15), PF cos(phi), fsw [Hz]
% Outputs: per-device losses [W] and inverter total.

% ===== device coefficients (FS200R07PE4, datasheet rev 2.1) =====
VCE0 = 0.70;    rC = 5.25e-3;     % IGBT : Vsat 1.75V @200A,150C
VF0  = 0.70;    rD = 3.75e-3;     % Diode: VF   1.45V @200A,150C
Eon  = 4.05e-3;  Eoff = 11.0e-3;  % IGBT switching @ 300V,200A,150C
Erec = 4.20e-3;                   % Diode recovery @ 150C
Vref = 300;   Iref = 200;         % datasheet test point
Kv   = 1.0;   Ki   = 1.0;         % voltage / current scaling exponents

% ===== derived =====
Ipk  = sqrt(2) * Irms;            % peak phase current
Mcos = M * PF;

% ===== conduction (per switch, standard SPWM duty distribution) =====
Pcond_T = VCE0*Ipk*(1/(2*pi) + Mcos/8) + rC*Ipk^2*(1/8 + Mcos/(3*pi));
Pcond_D = VF0 *Ipk*(1/(2*pi) - Mcos/8) + rD*Ipk^2*(1/8 - Mcos/(3*pi));

% ===== switching (per switch) =====
Vr = (Vdc/Vref)^Kv;
Ir = (Ipk/Iref)^Ki;
Psw_T = (fsw/pi) * (Eon + Eoff) * Ir * Vr;
Psw_D = (fsw/pi) *  Erec        * Ir * Vr;

% ===== aggregates =====
P_igbt  = Pcond_T + Psw_T;        % one IGBT
P_diode = Pcond_D + Psw_D;        % one diode
P_inv   = 6 * (P_igbt + P_diode); % whole inverter (6 IGBT + 6 diode)
end
```

### Code — `PhaseCurrents.m`
```matlab
function [Irms, Ipeak, Iavg] = PhaseCurrents(Id, Iq)
% AC phase current characteristics from d-q currents (amplitude-invariant).
    Ipeak = sqrt(Id.^2 + Iq.^2);   % peak phase current
    Irms  = Ipeak / sqrt(2);       % RMS
    Iavg  = (2 / pi) * Ipeak;      % average rectified
end
```

## Vault links
[[00 Home]] · [[ETM_Progress_Log]] · [[1D Thermal Design Tool — spec & flowchart]] · [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]] · [[Cauer Model Calibration — fit what you cannot derive]] · [[Only the h·A product matters for convective resistance]]

---
`EOD` · `1D thermal tool` · `L-opt 17.9mm` · `h–A map` · `ADC12 vs LM25` · `all gates passed`
