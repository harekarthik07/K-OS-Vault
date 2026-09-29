---
type: experiment
project: ETM For Heatsink and IGBT
status: done
created: 2026-09-29
case: peak-power (constant 470 W, 4 min)
tool: mc_thermal_app.m (thermal_core)
related: ["[[00 Home]]", "[[EXP_4min_Dyno_Run44]]", "[[2026-09-29 Peak-power vs 4-min dyno — model application & conservatism]]", "[[1D Thermal Design Tool — spec & flowchart]]"]
---

# EXP — Peak power (constant 470 W, 4-minute duty)

> **Purpose:** the bounding worst-case screen — hold the full 470 W (top of the 356–492 W band) flat for the entire 240 s duty and read the peak temperatures. No ramp, no bus sag — the hardest thermal case the duty can present.

## Setup (inputs)
![[MC-ETM -Input -1.png]]
![[MC-ETM -Input -2-constant-power.png]]

| Input | Value | Source |
|---|---|---|
| Q mode | **Constant** | 470 W injected flat |
| Q | 470 W | top of the validated band (356–492 W) |
| Nominal op. point | Id 120 A, Iq 0 A, Vdc 270 V | manual-dq reference |
| Alloy | LM25 (k 150.6) | current GDC part |
| Geometry | L 18 mm, A_fin 0.232 m², A_contact 0.00910 m², A_base 0.0343 m² | CAD |
| h | 29.59 W/m²K | calibrated (only fitted parameter) |
| Mass | m_total 3.3224 kg, split 0.170 (m_hs 2.7576, m_igbt 0.5648) | CAD |
| Ambient / duration | 36 °C / 240 s | typical dyno |

## Loss cross-check (why 470 W is the right number)
At the nominal point Id 120 / Iq 0 / Vdc 270, `analytical_loss` gives:
`Ipk = √2·Irms = 120 A`, `Mcos = M·PF = 0.344`.
- IGBT: `Pcond_T = 29.2 W`, `Psw_T = 25.9 W` → `P_igbt = 55.1 W`
- Diode: `Pcond_D = 14.5 W`, `Psw_D = 7.2 W` → `P_diode = 21.8 W`
- `P_inv = 6·(55.1 + 21.8) = 460.9 W ≈ 470 W` (run-average). ✓ The constant-Q screen uses the rounded 470 W.

## Model output
![[MC-ETM -output-1-constant-power.png]]
![[MC-ETM -output-2-constant -power.png]]
![[MC-ETM -output-3-constant -power.png]]

| Quantity | @ 60 s | @ 240 s | Δ |
|---|---|---|---|
| T_j (°C) | 70.8 | **93.5** | +22.7 |
| T_ntc (°C) | 58.2 | **80.9** | +22.7 |
| T_fin (°C) | 42.7 | 64.0 | +21.3 |
| ΔT_j/Δt | — | — | 0.126 °C/s |

`Rhs / Rtot / τ2 / Tj_pk = 0.0319 / 0.1858 / 425 / 93.5` — matches the Expected-Output gate exactly.

## Reading it
- **T_ntc peak 80.9 °C** vs the 95 °C deration line → **14.1 °C margin.**
- **T_j peak 93.5 °C** vs the 150 °C `Tvj,op` limit → **56.5 °C margin.**
- Inverter loss is flat 470 W (bottom-right pane), so this is purely the sink's transient charge curve.
- Steady-state ceiling (if the duty never ended): `T_ntc,ss = 36 + 470·0.1858 = 123.3 °C` — **the part only survives because it is transient-limited** (τ2 ≈ 425 s ≫ 240 s).

**Verdict:** PASS with margin, and this is the conservative bound. Compare to the real duty in [[EXP_4min_Dyno_Run44]].

---
`peak power` · `constant 470 W` · `Tj_pk 93.5` · `T_ntc 80.9` · `transient-limited` · `conservative bound`
