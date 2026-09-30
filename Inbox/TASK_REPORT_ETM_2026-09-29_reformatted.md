## Task Report — Electro-Thermal Model of Heatsink &amp; IGBT

**Owner:** Hare Karthik S &nbsp;·&nbsp; **Project:** MC-Thermals &nbsp;·&nbsp; **Date:** 2026-09-29 &nbsp;·&nbsp; **Status:** Done

---

### 1. Objective

Build a dyno-validated 1D electro-thermal (Cauer) model of the IGBT + heatsink that predicts junction/NTC temperature from the electrical duty — matched to 11 dyno runs (356–492 W) to ~2 K with a single fitted parameter `h = 29.59`. This report freezes how the model is built so it can be handed over and re-derived, and delivers a fast 1D design tool for screening heatsink/alloy/fin changes without running CFD each iteration.

---

### 2. Methodology

*Input → transform → output, verified phase by phase*

1. Electrical duty (Id, Iq, Vdc per dyno run) → PhaseCurrents (dq → Irms) → `analytical_loss` (SVPWM conduction + switching, per FS200R07PE4) → inverter loss P_inv.
2. P_inv → controlled heat-flow source into a Simscape Cauer thermal network (Rjc | Rcase-hs | Rhs | Rconv,lat, with junction and heatsink thermal masses) → T_ntc, T_j, T_fin.
3. Derive every resistance from datasheet / CAD / Yovanovich spreading; leave ONE knob (h) and calibrate it against 11 dyno runs (fit window 150–200 s).
4. Build a fast 1D twin (`thermal_core.m`, 2-node RK4) of the Simulink physics; lock it to the authoritative model with a guard test (`test_core.m` < 0.01 K) so the twin cannot silently fork.
5. Wrap the twin in an interactive app (`mc_thermal_app.m`): geometry/mass/convection inputs, three Q modes (constant / manual dq / Excel run), live plots, L-sweep and (h,A) map studies.
6. Validate against measured CAN NTC on a real run (run 44) and characterise the design margin (peak-power bound vs actual duty).

---

### 3. Software &amp; Environment

- MATLAB / Simulink R2020b+ with Simscape (uses `uigridlayout`, `Scrollable`).
- Authoritative model: `MC_HS_ETM_I2.slx` (Simscape, slow, validation reference).
- Code (base MATLAB, no extra toolboxes): `thermal_core.m`, `loss_from_idiq.m`, `q_builder.m`, `mc_thermal_app.m`, `test_core.m`, `test_app_gate.m`.
- Inputs: `T30_MC_HS_Thermal_Inputs.xlsx` (validated parameter set — single source of truth); dyno run sheets e.g. `Data/44.xlsx` (Time, Vdc, ID, IQ, IGBT_Temp).
- Hardware modelled: T30 motor controller, Infineon FS200R07PE4 IGBT module (6 IGBT + 6 diode), LM25 gravity-die-cast aluminium heatsink; ADC12 (PDC) considered as an alternative.
- Repo / files: `D:\Hare Karthik\Electrical\MC\MC_ETM_Model\` (Prj-Workflow, Data, Resources).

---

### 4. Calc &amp; Theory

#### 4a. Loss model — SVPWM analytical (source: `analytical_loss.m`)

Intermediate scalars:

```
I_pk  =  √2 · I_rms                  (peak phase current, dq → Irms)
Mcos  =  M · PF                      (M = 0.86, PF = 0.40)
```

Conduction losses (per device):

```
P_cond,T  =  VCE0 · I_pk · ( 1/(2π) + Mcos/8 )  +  rC · I_pk² · ( 1/8 + Mcos/(3π) )
P_cond,D  =  VF0  · I_pk · ( 1/(2π) − Mcos/8 )  +  rD · I_pk² · ( 1/8 − Mcos/(3π) )
```

Switching losses (per device):

```
P_sw,T  =  (fsw/π) · (Eon + Eoff) · (Vdc/Vref) · (I_pk/Iref)
P_sw,D  =  (fsw/π) ·  Erec        · (Vdc/Vref) · (I_pk/Iref)
```

Total inverter loss (6 IGBT + 6 diode):

```
P_inv  =  6·(P_cond,T + P_sw,T)  +  6·(P_cond,D + P_sw,D)
```

Device coefficients — Infineon FS200R07PE4 @ T_j = 150 °C:

| Symbol | Description                   | Value       | Unit             |
| ------ | ----------------------------- | ----------- | ---------------- |
| VCE0   | IGBT threshold voltage        | 0.70        | V                |
| rC     | IGBT slope resistance         | 5.25 × 10⁻³ | Ω                |
| VF0    | Diode threshold voltage       | 0.70        | V                |
| rD     | Diode slope resistance        | 3.75 × 10⁻³ | Ω                |
| Eon    | Turn-on switching energy      | 4.05 × 10⁻³ | J (at Vref/Iref) |
| Eoff   | Turn-off switching energy     | 11.0 × 10⁻³ | J                |
| Erec   | Diode reverse recovery energy | 4.20 × 10⁻³ | J                |
| Vref   | Datasheet voltage reference   | 300         | V                |
| Iref   | Datasheet current reference   | 200         | A                |
| fsw    | Switching frequency           | 10,000      | Hz               |
	
#### 4b. Thermal network — 2-node Cauer (θ = T − T_amb, ambient reference)

State equations:

```
C_j  · dθ₁/dt  =  Q  −  (θ₁ − θ₂) / R_series
C_hs · dθ₂/dt  =       (θ₁ − θ₂) / R_series  −  θ₂ / R_conv
```

Junction temperature (Foster R_JC, τ_JC ≤ 0.1 s → treated as pure resistance):

```
T_j  =  T_NTC_node  +  Q · R_JC

where:
  R_series  =  R_JC + R_CH + R_hs     (junction-to-fin series path)
  R_conv    =  1 / (h · A_fin)
```

#### 4c. Validated parameter set

Sole authoritative source: `T30_MC_HS_Thermal_Inputs.xlsx`

**Geometry**

| Parameter        | Symbol    | Value          | Unit |
| ---------------- | --------- | -------------- | ---- |
| HS Thk           | L         | 18             | mm   |
| Contact area     | A_contact | 9.09815 × 10⁻³ | m²   |
| Base plate area  | A_base    | 0.0343         | m²   |
| Fin surface area | A_fin     | 0.232          | m²   |

**Convection**

|Parameter|Symbol|Value|Unit|Note|
|---|---|---|---|---|
|Convection coefficient|h|29.59|W/(m²·K)|Fitted; CFD area-weighted = 34.3 (+16 %)|

**Material — LM25 (GDC, baseline) vs ADC12 (PDC, candidate)**

|Property|Symbol|LM25|ADC12|Unit|
|---|---|---|---|---|
|Thermal conductivity|k|150.624|92|W/(m·K)|
|Density|ρ|2690|2740|kg/m³|
|Specific heat|cp|871|963|J/(kg·K)|

**Mass &amp; thermal capacitance**

|Parameter|Symbol|Value|Unit|
|---|---|---|---|
|IGBT module mass|m_igbt|0.56264|kg|
|Heatsink mass|m_hs|2.75978|kg|
|Total mass|m_total|3.32242|kg|
|Junction capacitance|C_j|490|J/K|
|Heatsink capacitance|C_hs|2404|J/K|

**Device / interface resistances**

|Parameter|Symbol|Value|Unit|Note|
|---|---|---|---|---|
|Junction-to-case (datasheet)|R_JC|0.02679|K/W|Use 0.04167 K/W for safety claims|
|Case-to-heatsink (datasheet)|R_CH|0.009|K/W||
|TIM thermal conductivity|λ_TIM|1.1|W/(m·K)||
|TIM resistance (from λ, geometry)|R_ch|0.00818|K/W||

**Thermal resistance budget**

|Resistance|Symbol|Value|Unit|Derivation|
|---|---|---|---|---|
|Fin conduction|R_cond|0.01313|K/W|L / (k · A_base)|
|Spreading|R_spread|0.01878|K/W|Yovanovich correlation|
|Total fin|R_hs|0.03191|K/W|R_cond + R_spread|
|Convection|R_conv|0.14567|K/W|1 / (h · A_fin)|
|**Total (HS to amb)**|R_total|**0.18576**|K/W|R_hs + R_conv|

**System time constant**

| Parameter         | Symbol | Value | Unit | Method                         |
| ----------------- | ------ | ----- | ---- | ------------------------------ |
| Dominant τ        | τ₂     | ≈ 425 | s    | Eigenvalue of [A] state matrix |
| C·R approximation | —      | 421.5 | s    | (C_j + C_hs) · R_total         |

> [!important] Validity limits
> Transient only — steady state at 470 W → T_NTC = 123 °C, never reached in 4 min because τ₂ ≫ 240 s. *h* is not predictive for a new fin geometry (CFD/test required per redesign). T_j is estimated, not measured; use R_JC = 0.04167 K/W for safety claims. Validated vs CAN NTC: **RMSE 0.82 K, bias +0.05 K** over 240 s (run 44).

---

### 5. End Result &amp; How It's Studied

**Delivered**
- Validated Simulink model `MC_HS_ETM_I2.slx` and a fast 1D twin + interactive design tool.
- Design studies: L-sweep (R_hs optimum 17.9 mm — part already optimal); (h,A) lever map; LM25 vs ADC12 alloy comparison.

**Verification gates — all passed**

|Gate|Result|
|---|---|
|`thermal_core` RK4 vs closed-form|0.000 K|
|`loss_from_idiq` vs model P_inv (run 44)|0.05 W (463.8 vs 463.8)|
|App vs core (defaults) — Tj_pk / Rhs / τ2 / Rtot|93.5 °C / 0.0319 / 425 / 0.1858|
|Measured validation (run 44 vs CAN NTC)|**RMSE 0.82 K, bias +0.05 K** (measured NTC peak 80.0 °C)|

**Worked design margin**

| Quantity                  | Peak screen (470 W const.) | Actual duty (run 44)      |
| ------------------------- | -------------------------- | ------------------------- |
| T_j peak                  | **93.5 °C**                | 91.5 °C                   |
| T_ntc peak (model)        | 80.9 °C                    | 79.3 °C @ 240 s           |
| T_ntc peak (measured CAN) | —                          | **80.0 °C**               |
| Validation                | Bounding screen            | RMSE 0.82 K, bias +0.05 K |
| NTC margin to 95 °C       | 14.1 K                     | 15.0 K                    |
| Junction margin to 150 °C | 56.5 K                     | 58.5 K                    |
| Verdict                   | PASS                       | PASS + validated          |

> [!success] Conservatism finding
> The constant-470 W screen is conservative by ~2 K vs the real duty — from the raw run-44 file the actual P_inv averages ~432 W (peak ~498 W), because of the soft-start ramp and bus sag (261 → 232 V). Use the 470 W constant screen as the design bound. Both cases confirm transient-limited operation: τ₂ ≈ 425 s ≫ 240 s run time.

**ADC12 trade:** R_hs +63 %; time-to-95 °C at 492 W/45 °C drops 270 → 198 s (derates inside the test); needs h 29.59 → 34.4 (+16 % airflow) to neutralise the alloy change.

---

### 6. End Result For

- **MC thermal / hardware team:** fast 1D screening tool for heatsink, alloy and fin decisions before CFD.
- **Alloy decision (LM25 vs ADC12 / GDC vs PDC):** quantified thermal penalty for the costing call.
- **Design verification:** a validated, hand-over-able model with a stated measured error (< 1 K RMSE).
- **Future consumers:** test-bench correlation, and reuse of the loss + Cauer method on other MC parts.

---

### Phase Log

*One phase at a time, verify before advance*

|#|Phase|Gate (pass criteria)|Result|Pass?|Date|
|---|---|---|---|---|---|
|1|Validated 1D Cauer model|Match 11 dyno runs to ~2 K with a single fitted h|h = 29.59; ≤ 2 K over 356–492 W; run-44 RMSE 0.82 K, bias +0.05 K|PASS|2026-09-15|
|2|Design tool (L-sweep + h–A map)|Core RK4 < 0.01 K, app = core, P_inv match < 1 W|0.000 K; 0.05 W; L-opt 17.9 mm; (h,A) map built|PASS|2026-09-28|
|3|Decisions &amp; handover|Validated report + alloy trade documented|This report; ADC12 quantified; docs filed|IN PROGRESS|2026-09-29|

### Issues / Blockers

- No cooldown data in any run → C never independently measured (CAD-derived only).
- Junction-to-NTC resistance unpublished → the +1.89 K NTC offset cannot be quantified.
- h is not predictive for a new fin geometry → CFD/test still required per redesign; 1D screens only.
- IGBT vs diode loss split unmeasured → RthJC between 0.02679 and 0.04167 (use 0.04167 for safety).

### Next Step

- Decide ADC12 viability given the 198 s time-to-deration at hot ambient (cost/performance call).
- Add save/load of design configs (.mat) and a T_j-vs-total-mass sweep figure.
- Test-bench correlation as the future acceptance criterion.

### Links

**K-OS:** [[ETM For Heatsink and IGBT/00 Home]] · [[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]] · [[1D Thermal Design Tool — spec & flowchart]] · [[EXP_PeakPower_Constant_470W]] · [[EXP_4min_Dyno_Run44]] · [[2026-09-29 Peak-power vs 4-min dyno — model application & conservatism]]

**Repo/files:** `D:\Hare Karthik\Electrical\MC\MC_ETM_Model\` (MC_HS_ETM_I2.slx, thermal_core.m, loss_from_idiq.m, q_builder.m, mc_thermal_app.m, test_core.m, test_app_gate.m)

**Data:** `Resources\T30_MC_HS_Thermal_Inputs.xlsx` · `Data\44.xlsx`

---

### Appendix — Figures

Loss model (Simulink):
![[MC_ETM_Loss_Model.png]]

Thermal network (Simscape Cauer):
![[MC_ETM_Thermal_Network.png]]

1D design tool (delivered app):
![[MC_ETM_1D_Tool_GUI.png]]

Validation — run 44, model vs measured CAN NTC (RMSE 0.82 K, bias +0.05 K):
![[MC-ETM -output-4-4min-peak-power-actual-test-dyno.png.jpg]]
