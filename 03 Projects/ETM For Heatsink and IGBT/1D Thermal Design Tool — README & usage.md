---
type: readme
project: ETM For Heatsink and IGBT
status: active
created: 2026-09-28
tags: [thermal, matlab, app, readme, handover, etm]
related: ["[[00 Home]]", "[[1D Thermal Design Tool — spec & flowchart]]", "[[ETM_Problem_Statement]]", "[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[EOD_2026-09-28_ETM_1D_Thermal_Tool]]"]
---

# MC Heatsink 1D Thermal Tool

Predicts IGBT NTC / junction / heatsink temperature for the T30 motor-controller
heatsink under a given heat load. Built on the ETM validated against 11 dyno runs.

---

## 1. Sharing it

### What to send
Six files. They must all sit in **one folder**, and that folder must be on the
MATLAB path (or be the current folder).

```
thermal_core.m       physics  (two-node RK4 solver)
loss_from_idiq.m     P_inv from id/iq/Vdc  (mirrors the Simulink loss block)
q_builder.m          builds Q(t) from const / Excel / manual input
mc_thermal_app.m     the GUI
test_core.m          gate: core vs closed-form
test_app_gate.m      gate: app path vs core
```

Zip the folder and send it. No toolboxes beyond base MATLAB are required.
**MATLAB R2020b or newer** (uses `uigridlayout` + `Scrollable`).

### What NOT to send as "the model"
`MC_HS_ETM_I2.slx` is the *validation reference*, not the tool. Send it only if the
recipient needs to re-verify the physics.

### Excel-mode caveat
If they will use Excel mode, they also need the run spreadsheets, and the file path
is entered at runtime via the browse button — nothing is hardcoded.

---

## 2. Using it

```matlab
mc_thermal_app
```

### Left panel — inputs

| Section | What to set |
|---|---|
| **GEOMETRY** | `L base` (slider) = base plate thickness. `A_fin` = total external surface area. `A_contact` = IGBT footprint. `A_base` = base plan area (L×W of the plate) |
| **CONVECTION** | `h` = heat transfer coefficient. **This is the calibrated parameter** — 29.59 is the dyno-measured value (MC fan only, no ram air) |
| **MATERIAL** | Alloy dropdown auto-fills k / rho / cp. LM25 = current GDC part, ADC12 = PDC alternative |
| **MASS** | Three modes — see below |
| **POWER** | Three Q modes — see below |
| **ENVIRONMENT** | `T_amb`, `t_end` |

**Mass modes**
- `Split known` — enter `m_hs` and `m_igbt` separately (from CAD)
- `Total only` — enter total mass + a split fraction (default 0.17, CAD-derived).
  Derived m_hs / m_igbt display live as you drag the slider
- `Thermal direct` — enter C_hs and C_plate in J/K if you already have them

> Total mass sets the sink temperature. The split shifts the **junction** estimate
> by roughly ±1 K per 0.05 — small, but not nothing.

**Q modes**
- `Constant` — a flat wattage (e.g. 470 W)
- `Manual dq` — enter Id, Iq, Vdc; the tool computes P_inv via the loss model
- `Excel run` — browse a dyno run sheet; P_inv is computed per row from columns
  A(time) B(Vdc) C(id) D(iq). Range defaults to `A3:E588` — **row 3 is the first
  data row**; starting at row 1 or 2 picks up headers

### Right panel — output

Four plot panes, each with a **dropdown** to choose its signal:
`T_ntc · T_j · T_fin · dTj/dt · P_inv · Id · Iq · Vdc`

Two **cursors** (c1 gold, c2 cyan) driven by sliders. The readout table shows every
signal at each cursor plus the delta, and `ΔTj/Δt` — the average heating rate between
them, in °C/s. Bottom line shows Rhs / R_total / tau2 / Tj_peak.

### Buttons
- `Restore defaults` — back to the validated LM25 set
- `L sweep` — R_hs and Tj_peak vs base thickness, optimum marked
- `h-A map` — Tj_peak contour over the (h, A_fin) plane, current point starred

### Reading the limit lines
- **95 °C** on T_ntc = the NTC deration threshold the VCU acts on
- **150 °C** on T_j = `Tvj op`, the device limit

---

## 3. How the code works

### Data flow
```
inputs (GUI)
   │
   ├─ mass mode ──► resolveMass()  ──► m_hs, m_igbt, cp
   ├─ Q mode ─────► resolveQ()     ──► scalar W  or  [t Q] series
   │                   └─ 'excel'  ──► q_builder ──► loss_from_idiq
   │                   └─ 'manual' ──► loss_from_idiq
   │
   └──────────────► thermal_core(p) ──► R struct
                                          │
                                          ├─ drawPane(1..4)  plots
                                          └─ moveCursors()   readout table
```

### `thermal_core.m` — the physics
Takes a param struct, returns a result struct. Five steps:

1. **Conduction** `R_cond = L/(k·A_contact)`
2. **Spreading** — Lee/Yovanovich isoflux circular-source correlation. Converts the
   rectangular geometry to equivalent radii (`a`, `b`), computes ε, τ, Bi, λ, φc, ψ,
   then `R_sp = ψ/(k·a·√π)`
3. **Interface** `R_ch = RthCH_datasheet × (1.0/λ_TIM)` — the datasheet value assumes
   1.0 W/mK paste; this scales it to the actual TIM
4. **Convection** `R_conv = 1/(h·A_fin)`
5. **Solve** — two coupled ODEs (energy balance at each node) integrated by
   fixed-step RK4. Time constants come from the eigenvalues of the state matrix,
   **not** from per-branch RC products

```
C_p  · dθ₁/dt = Q − (θ₁−θ₂)/R_series
C_hs · dθ₂/dt = (θ₁−θ₂)/R_series − θ₂/R_conv
```

`T_junction = T_ntc_node + Q·RthJC` — added afterwards, no capacitance, because the
datasheet Foster time constants are all ≤0.1 s (instant at this timescale).

### `loss_from_idiq.m` — the loss model
Mirrors the Simulink chain exactly: `PhaseCurrents` (id,iq → peak current) then
`analytical_loss` (FS200R07PE4 conduction + switching, per device × 6 IGBT + 6 diode).
Constants M=0.86, PF=0.40, fsw=10 kHz match the model's blocks.

### `q_builder.m` — load builder
Returns `[t Q]` in every mode so `thermal_core` has one code path. Strips non-finite
rows, sorts and de-duplicates time (interp1 requires unique, finite, sorted x).

### `mc_thermal_app.m` — the GUI
- `S` = state struct (every input value). `S0` = defaults for restore
- `W` = widget handles
- Every widget callback writes into `S`, then calls `refresh()`
- `refresh()` packs `S` into a param struct, calls `thermal_core`, stores the result
  in `W.R`, then redraws
- **Cursor moves do not re-solve** — `moveCursors()` just indexes into `W.R`, which
  is why dragging is instant

---

## 4. Trust boundaries — read before quoting numbers

| Signal | Measured? | Notes |
|---|---|---|
| `T_ntc` | model prediction of the **CAN NTC**, calibrated to it | ~2 K conservative (model reads low) |
| `T_j` | **estimated**, never measured | two biases, opposite directions — see below |
| `T_fin` | model only | single-lump sink (valid: Bi ≈ 0.004) |

**T_j caveats**
- Reads **high**: the NTC sits on the DCB, already partway up RthJC, so adding the
  full 0.02679 double-counts part of the rise
- Reads **low** at high load: 0.02679 assumes IGBT/diode losses split by conductance.
  IGBT-only would be 0.04167 (+56 %). **Use 0.04167 for any safety claim**

**Validity envelope** — 356–492 W, ≤300 s, 34–41 °C ambient, dyno airflow
(MC fan, no ram air). Outside this the tool still runs but is not validated.
`h` is **not predictive for a redesigned fin geometry** — that needs CFD or test.

---

## 5. Verifying an install

```matlab
test_core        % expect: GATE PASSED, RK4 = closed-form
test_app_gate    % expect: GATE PASSED, T_ntc ≈ 80.88
mc_thermal_app   % defaults → Rhs 0.0319 / Rtot 0.1858 / tau2 425 / Tj_pk 93.5
```

If those three agree, the install is faithful to the validated model.

> **Standing rule:** the physics exists in two places (Simulink + `thermal_core`).
> Re-run `test_core` after any change to either side. See [[Lock a fast surrogate model to the authoritative one with a guard test]].
