---
concept: Fan PQ Health Check & Reverse-Flow Diagnosis
project: CFD based heatsink thermals study (forced and natural convection)
domain: CFD
status: incubating
created: 2026-09-02
sources: ["[[Daily Log#2026-09-02]]"]
title: Fan PQ Health Check & Reverse-Flow Diagnosis
model: "[[MC_HS_ETM_I1]]"
heatsink: "[[HS-I1]]"
component: "[[HS_I1-G1-K1]]"
tool: ANSYS Fluent 2025 R2
type: debugging-log
tags:
  - cfd
  - cht
  - fan-model
  - convergence
  - reverse-flow
  - pq-curve
  - vv
  - etm
---
# Fan PQ Health Check & Reverse-Flow Diagnosis

> [!abstract] TL;DR
> New heatsink [[HS_I1-G1-K1]] threw persistent **reverse flow** at the fan exit (150+ faces, growing) and continuity stalled ~6e-2. Fan, clearance (H/D) and 3D fan zone were **unchanged** from the old case — only the **fin design changed** (curved/open → straight/tight). The tighter fins raised system resistance ~3–4×, pushing the fan operating point into the **choked / near-stall corner** (φ ≈ 0.36). Fix path: converge properly (pseudo-transient + coupled), re-run the **PQ health check**, then extract zone-wise `h`.

---

## 1. Symptom
- Continuity residual stuck ~0.2 → slowly falling to 6e-2 by iter 67, not reaching 1e-3.
- `Reverse flow in N faces in fan (cell zone ID: 32030) exit` — N grew **20 → 150+**.
- Reverse flow later appeared at fan **inlet** too (recirculation loop closing on itself).
- Growing (not transient) face count ⇒ **structural**, not solver noise.

> [!warning] Key tell
> A *growing* reverse-flow face count = physics/BC problem. It will **not** self-heal with more iterations.

---

## 2. What we ruled out
| Hypothesis | Check | Result |
|---|---|---|
| Fan is a disc (hub not blocked) | Mesh slice — hub is green/solid | ❌ ruled out, already an **annulus** |
| H/D too tight | H=11 mm, D=80 mm → H/D=0.14 | ⚠️ tight & unforgiving, but **same as old case** → not the trigger |
| Fan zone / RPM changed | Same 3D fan zone | ❌ unchanged |
| **Fin geometry changed** | Old = curved/open radial fins; New = straight/tight parallel fins + central pin cluster | ✅ **ROOT CAUSE** |

> [!note] The insight
> Impinging-fan flow wants to leave **radially in all 360°**. Curved/open fins allowed that. Straight tight fins force flow into **2 channel directions only**; cross-flow slams into fin walls → big pressure loss. Central 12-tooth pin cluster sits in the hub shadow and blocks discharge. ⇒ system curve `K` jumped hard.

---

## 3. Operating point measured (new case, un-converged)
```
ṁ_fan   = 0.0097256 kg/s      (fan-out-int)
p_in    = -5.0174 Pa          (fan-in-int, area-weighted)
p_out   = 27.0937 Pa          (fan-out-int, area-weighted)
Q_op    = ṁ/ρ = 0.0097256 / 1.15 ≈ 0.00846 m³/s
Δp_op   = p_out − p_in = 27.09 − (−5.02) = 32.11 Pa
```

### Fan datasheet PQ curve ([[Fan_TRV_I1]])
| Q (m³/s) | Δp (Pa) |
|---|---|
| 0        | 61.88 |
| 0.004719 | 48.54 |
| 0.009439 | 36.28 |
| 0.014158 | 27.46 |
| 0.018878 | 14.71 |
| 0.023668 | 0     |

---

## 4. The reusable PQ health-check procedure

> [!tip] This is the upgrade for the [[CHT Case Configurator — Math Behind Every Section|CHT_Tool]] — run it as an automated post-step on every fan CHT case.

### Inputs
- `ṁ_fan`, `ρ_op`, `p_in`, `p_out` from CFD surface integrals
- Datasheet PQ points

### Steps
1. **Operating point**
   `Q_op = ṁ_fan / ρ_op` ; `Δp_op = p_out − p_in`
2. **Interpolate curve at Q_op**
   `Δp_curve = Δp₁ + (Q_op−Q₁)/(Q₂−Q₁)·(Δp₂−Δp₁)`
3. **Curve-match residual (convergence gate)**
   `ε = |Δp_op − Δp_curve| / Δp_curve`
   - `< 5%` → fan BC honoured ✓
   - `> 10%` → not converged / reverse-flow contaminated → **stop, don't trust results**
4. **Flow coefficient (position on curve)**
   `φ = Q_op / Q_max`
   - `>0.5` healthy · `0.35–0.5` marginal · `<0.35` choked/near-stall
5. **Local slope (stall test)**
   `m = dΔp/dQ` at Q_op → `m<0` stable, `m≥0` stall
6. **System resistance coefficient**
   `K = Δp_op / Q_op²` → compare designs via `K_new/K_old`
7. **Verdict**
   ```
   IF   ε > 10%            → NOT CONVERGED
   ELIF φ < 0.35 OR m ≥ 0  → CHOKED / STALLED
   ELIF φ < 0.5            → MARGINAL
   ELSE                    → HEALTHY
   ```

### Applied to this case
```
Δp_curve(0.00846) = 38.83 Pa
ε = |32.11 − 38.83|/38.83 = 17.3%   → GATE FAILED (not converged)
φ = 0.00846/0.02367       = 0.357   → MARGINAL, edge of choked
```

> [!danger] Verdict
> **Cannot judge the fan yet — ε = 17% means the case is not converged.** But φ = 0.36 already flags a choked system. Converge first, then re-judge.

---

## 5. Fix sequence (do in order)
- [ ] **Confirm** by comparing to OLD converged case: pull `Q_old`, `Δp_old`, plot both points on one curve. Expect `K_new/K_old ≈ 3–4`.
- [ ] **Converge properly**
  - Hybrid Init + FMG (5–10 sweeps)
  - **Coupled** pressure-velocity + **Pseudo-Transient** (Conservative length scale, timescale factor 1 → 0.5 if unstable)
  - 1st-order upwind for first ~100 iters → switch to 2nd-order
  - Outlet backflow: dir "normal to boundary", turb intensity 5%, length 0.07·D_h, T=ambient
- [ ] **Re-run PQ health check** → require `ε < 5%` before trusting anything
- [ ] **Monitors** (truer than residuals): IGBT baseplate T, fan ṁ, base heat flux → flat <0.5%/50 iters
- [ ] If still choked after convergence → it's a **real design problem**, escalate to MC team (fin redesign vs accept low-flow thermals)

---

## 6. Consequences for [[MC_HS_ETM_I1]] (the ETM/Cauer link)

> [!important] Dead-zone h is a *different regime*, not a correction factor
> With H/D=0.14 the hub-shadow **stagnation zone is physically real** — low velocity, low `h`. Don't try to erase it. Extract `h` **zone-wise**:
> - under-hub zone: `r < r_hub`
> - impingement zone: `r_hub < r < r_tip`
>
> These are very different `h` values. Averaging them into one number is what biases the 2-node Cauer model. → candidate for a **3-node Cauer with a parallel dead-zone branch** (open item #3).

---

## 7. Principles captured
*Promoted to `04 Knowledge` on 2026-09-02 — these now live under [[CFD]] / [[Thermal Management]] / [[Heat Transfer]].*

- [[Growing reverse-flow face count = physics-BC problem, not solver noise]]
- [[Fan operating point = fan PQ curve ∩ system curve K·Q²]]
- [[Flow coefficient φ — below 0.35 expect central reverse flow]]
- [[Curve-match residual ε is a convergence gate for fan CHT]]
- [[Impinging fan + straight tight fins = high cross-flow resistance]]
- [[Tighter fins raise system K → operating point shifts left toward stall]]
- [[Dead-zone h is a different regime, not a correction factor]]

## 8. Open items
1. Pull old-case operating point, confirm `K_new/K_old`.
2. Reach ε < 5% via pseudo-transient + coupled.
3. Zone-wise `h` (under-hub vs impingement) for Cauer.
4. Decide: accept new-fin thermals or escalate redesign.

## Related
- [[MC_HS_ETM_I1]] · [[Fan_TRV_I1]]
- [[MC Heatsink CHT — Consolidated Setup]] · [[Fan 3D Zone Setup]] · [[CHT Case Configurator — Math Behind Every Section]]
