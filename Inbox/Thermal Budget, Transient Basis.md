## Part 1 — Thermal Budget, Transient Basis (FINAL)

**Objective:** determine whether the T30 MC heatsink holds Tj ≤ 95 °C at logged dyno loads, given a 4-minute peak-output duty.

**Why transient:** the tests run 240 s against a dominant time constant of 393 s. The system reaches only 46% of its eventual temperature, so a steady-state analysis would answer a question nobody asked.

---

### SECTION A — Resistances

_Theory: §1 thermal-electrical analogy. Resistances in series add._

#### A.1 — Rjc (junction → case)

```
Rjc = 0.009 K/W                          [datasheet]
```

⚠️ Spec sheet labels this `RthCH`; true `RthJC` marked TBD.

#### A.2 — R_TIM (case → heatsink)

```
R = t/(k_TIM·A)
R_TIM = 0.00999 K/W                      [datasheet]
```

Back-check: `t/k = R·A = 9.09e-5` → 0.27 mm at k = 3 W/mK. Plausible.

#### A.3 — R_cond (1D conduction through base)

```
R = L/(k·A)
  = 0.018/(150.624 × 0.00909815)
  = 0.013135 K/W                         [DERIVED]
```

#### A.4 — R_spread (source constriction)

_Lee/Yovanovich, isoflux circular source on circular plate._

```
a  = √(A_src/π)  = 0.05381 m
b  = √(A_base/π) = 0.08740 m
ε  = a/b = 0.6157
τ  = t/b = 0.2059
Bi = h·b/k = 0.01857

λ  = π + 1/(ε√π) = 4.0579
φc = (tanh λτ + λ/Bi)/(1 + (λ/Bi)tanh λτ) = 1.4578
ψ  = ½(1−ε)^1.5·φc = 0.1737

R_sp = ψ/(k·a·√π) = 0.01209 K/W          [DERIVED, A_base assumed]
```

Bi ≪ 1 → adiabatic-edge limit. R_sp varies only 1.6% as h goes 10→150, so no circularity with the fitted h.

#### A.5 — Rhs reconciliation

```
theory = 0.013135 + 0.01209 = 0.0252
fitted = 0.0275                (11 runs, RMSE 1.0 K)
residual +9% → within k/geometry uncertainty
→ USE 0.0275
```

#### A.6 — R_conv (heatsink → air)

```
R = 1/(h·A_fin) = 1/(32 × 0.232) = 0.13470 K/W
```

⚠️ h = 32 **calibrated, not derived**. → Part 2.

#### A.7 — Totals

```
R_series = 0.009 + 0.00999 + 0.0275 = 0.04649 K/W
R_total  = 0.04649 + 0.13470        = 0.18119 K/W
```

|Element|R|Share|Confidence|
|---|---|---|---|
|Rjc|0.00900|5.0%|⚠️|
|R_TIM|0.00999|5.5%|◐|
|Rhs|0.02750|15.2%|✅|
|**R_conv**|**0.13470**|**74.3%**|⚠️|
|**Total**|**0.18119**|||

---

### SECTION B — Capacitances

_Theory: §1, C = m·c_p._

```
C_plate = 0.574 kg × 871 J/kgK =  500 J/K
C_hs    = 2.737 kg × 871 J/kgK = 2384 J/K
```

⚠️ C_hs is the casting only. Housing, mounting plate, and busbars are thermally attached and excluded. Real value likely higher → current results **conservative**.

**Lumping validity** (§2):

```
Bi = h·L/k = 32 × 0.018/150.624 = 0.0038 ≪ 0.1     ✅
diffusion time = L²/α = 5 s  vs  τ₂ = 393 s        ✅ 78× separation
```

---

### SECTION C — Transient model

_Theory: §4–5._

#### C.1 — Governing equations

```
C_p ·dθ₁/dt = Q − (θ₁−θ₂)/R_s
C_hs·dθ₂/dt = (θ₁−θ₂)/R_s − θ₂/R_c        θ = T − T_amb
```

#### C.2 — State matrix

```
A = [ −1/(R_s C_p)      1/(R_s C_p)         ]   [ −0.04302   0.04302 ]
    [  1/(R_s C_hs)   −(1/R_s+1/R_c)/C_hs   ] = [  0.00902  −0.01214 ]
```

#### C.3 — Eigenvalues → time constants

```
λ₁ = −0.05261 → τ₁ =  19.0 s      junction ↔ sink
λ₂ = −0.00255 → τ₂ = 392.7 s      assembly → air  (dominant)
```

**Not** `C_hs·R_conv = 321 s` — that ignores the junction mass discharging through the same convection path. Quick estimate: `(C_p+C_hs)·R_c = 388 s` ✓

#### C.4 — Solution

```
Tj(t) = T_amb + 85.16 − 14.44·e^(−t/19.0) − 70.72·e^(−t/392.7)      [at 470 W]
```

At 240 s: `1 − e^(−240/392.7) = 46%` risen.

---

### SECTION D — Results at 240 s

|Q|Tj @240s, 36 °C|Tj @240s, 45 °C|Tj steady, 36 °C|
|---|---|---|---|
|356 W|71.4|80.4|100.5|
|428 W|78.6|87.6|113.5|
|470 W|82.8|91.8|121.2|
|492 W|**85.0**|**94.0**|125.1|

**All logged runs pass 95 °C at 240 s.** Worst case 94.0 °C (492 W, 45 °C ambient) — 1 K margin.

Validation: 82.8 °C predicted vs ~81 °C measured at comparable load. ✓

---

### SECTION E — Power limits vs duration

|T_amb|240 s|480 s|Steady|
|---|---|---|---|
|34 °C|613 W|446 W|337 W|
|36 °C|593 W|431 W|326 W|
|41 °C|543 W|395 W|298 W|
|45 °C|**502 W**|**365 W**|276 W|

The rating is a **function of duration**, not a single number. 240 s rating ≈ 1.82× continuous.

**Time to reach 95 °C:**

|Q|@36 °C|@45 °C|
|---|---|---|
|356 W|894 s|513 s|
|428 W|489 s|333 s|
|470 W|391 s|274 s|
|492 W|353 s|**250 s**|

At worst case you have 250 s. **The 240 s test sits 10 s inside the limit.**

---

### SECTION F — Conclusions

1. **Design passes the 4-minute duty**, worst case 94.0 °C vs 95 °C limit.
2. **Margin is thin at hot ambient.** 492 W at 45 °C hits 95 °C at 250 s — 4% beyond test duration. Not a comfortable margin.
3. **Continuous operation fails** by 26 K at 470 W. Deration must be time-aware, not a single power cap.
4. **Rhs = 0.0275 validated and closed.** 11 runs, RMSE 1.0 K, theory within 9%.
5. **Convection is 74% of the budget.** Any real margin comes from airflow, not conduction.

---

### SECTION G — Open items

|#|Item|Why it matters|
|---|---|---|
|1|**h = 32 fitted, never derived**|74% of the budget rests on it → Part 2|
|2|**C_hs excludes housing/plate/busbars**|Now governs the answer. Under-estimate → results conservative|
|3|**No long-cooldown dyno run**|Only clean way to measure C (Q=0 → pure decay)|
|4|**A_base assumed 0.024 m²**|±25% on R_sp. One CAD measurement|
|5|**Rjc may be RthCH, not RthJC**|Eats a tight budget directly|
|6|**Is 95 °C Tj, case, or sink?**|At 470 W: Tj 121, case 117, sink 99 — different verdicts|
|7|**Repeated-burst duty not modelled**|Heat may ratchet across cycles. Realistic fie|