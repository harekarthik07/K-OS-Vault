## Lumped Capacitance Thermal Networks

This is the theory behind everything we did. Four ideas stacked.

---

### 1. The thermal-electrical analogy

Heat flow obeys the same algebra as current flow.

|Electrical|Thermal|Units|
|---|---|---|
|Voltage `V`|Temperature `T`|°C|
|Current `I`|Heat flow `Q`|W|
|Resistance `R`|Thermal resistance|K/W|
|Capacitance `C`|Thermal mass `mc_p`|J/K|
|`V = IR`|`ΔT = QR`||
|`I = C dV/dt`|`Q = C dT/dt`||

So a heatsink is literally an RC circuit. Everything you know about capacitors charging applies.

**Thermal capacitance:**

```
C = m × c_p
C_hs = 2.737 kg × 871 J/kgK = 2384 J/K
```

It takes 2384 joules to raise the heatsink by 1 K.

---

### 2. When are you allowed to lump?

The whole method treats each body as **one uniform temperature**. That's a lie — the heatsink base is hotter at the IGBT than at the edges. The question is whether the lie is small enough.

**Biot number** — the test:

```
Bi = h·L / k
   = (resistance to conducting heat within the body)
     ─────────────────────────────────────────────
     (resistance to removing heat from the surface)
```

For your heatsink:

```
Bi = 32 × 0.018 / 150.624 = 0.0038
```

**Rule: Bi < 0.1 → lumping is valid.** You're at 0.004, 25× inside the limit. Aluminium conducts so much better than air convects that the sink is nearly isothermal.

Cross-check by timescale — thermal diffusivity `α = k/(ρc_p) = 6.45e-5 m²/s`:

```
diffusion time across 18 mm = L²/α = 5 s
```

Heat crosses the base in 5 s; the sink takes ~390 s to heat up. 78× separation, so the base is always internally equilibrated. **Lumping is justified.**

(Note: this is a _different_ Biot number from the one in the spreading correlation, which used `b` — the plate radius — as the length. Same formula, different characteristic length, different question.)

---

### 3. One node: where the exponential comes from

Simplest case — one mass, one resistance:

```
        Q
        ↓
      ┌─────┐
      │  C  │ ── R ── T_amb
      └─────┘
```

Energy balance: _stored = in − out_

```
C · dθ/dt = Q − θ/R          where θ = T − T_amb
```

Separate and integrate:

```
θ(t) = QR · (1 − e^(−t/RC))
```

Two things fall out:

- **Steady state** `θ_∞ = QR` — set `dθ/dt = 0`, capacitance drops out entirely. This is why `R = ΔT/Q` only holds at steady state.
- **Time constant** `τ = RC` — at `t = τ` you're 63% risen; at `3τ`, 95%; at `5τ`, 99%.

**R sets where you end up. C sets how fast you get there.** That's why fitting a transient can't separate them — you're only ever seeing the product.

---

### 4. Two nodes: why you need them

One node can't represent your system, because the junction and the heatsink have very different masses and are separated by a resistance. So:

```
   Q
   ↓
 ┌────┐         ┌─────┐
 │ Tj │── R_s ──│ Ths │── R_c ── T_amb
 │C_p │         │C_hs │
 └────┘         └─────┘
  500            2384
 0.0465         0.1347
```

Energy balance at **each** node:

```
C_p  · dθ₁/dt = Q − (θ₁−θ₂)/R_s          in: Q,  out: to sink
C_hs · dθ₂/dt = (θ₁−θ₂)/R_s − θ₂/R_c     in: from junction, out: to air
```

Two coupled ODEs. Write as a matrix:

```
θ' = A·θ + b

A = [ −1/(R_s C_p)       1/(R_s C_p)         ]
    [  1/(R_s C_hs)    −(1/R_s + 1/R_c)/C_hs ]
```

Each row is just "heat in minus heat out, divided by my capacitance."

---

### 5. Eigenvalues = time constants

For `θ' = Aθ`, solutions have the form `θ = v·e^(λt)`. Substituting gives `Av = λv` — the eigenvalue problem.

For your system:

```
λ₁ = −0.05261  →  τ₁ = 19.0 s
λ₂ = −0.00255  →  τ₂ = 392.7 s
```

Full solution = steady state + decaying modes:

```
Tj(t) = 36 + 85.16 − 14.44·e^(−t/19) − 70.72·e^(−t/393)
```

**Physical meaning:**

- `τ₁ = 19 s` — the small junction mass equilibrating with the sink. Fast.
- `τ₂ = 393 s` — the whole assembly heating the air. Slow, dominates everything past a minute.

---

### 6. The mistake I made, and why it matters

I kept quoting `τ₂ = C_hs × R_conv = 2384 × 0.1347 = 321 s`. **Wrong.**

That treats the heatsink as if only _its own_ capacitance discharges through `R_conv`. But the junction's 500 J/K also has to get out through the same convection path. The real answer is 393 s — 22% larger.

Better quick estimate:

```
(C_p + C_hs) × R_c = 2884 × 0.1347 = 388 s   ✓ close to 393
```

**The lesson:** in a multi-node network, time constants are _not_ the individual RC products. You need the eigenvalues. `RC` per branch is only a rough guide, and it under-predicts.

---

### 7. What this gives you

Everything in Part 1 comes from these four ideas:

|Result|From|
|---|---|
|`R = ΔT/Q` only at steady state|§3, capacitance drops out|
|Lumping is valid here|§2, Bi = 0.004|
|82.8 °C at 240 s|§5, eigenvalue solution|
|Can't separate R from C on a short run|§3, you only see the product|
|Cooldown measures C·R cleanly|§3 with Q=0 → pure decay|

**Where to read more:** Incropera & DeWitt, _Fundamentals of Heat and Mass Transfer_, Ch. 5 (transient conduction, lumped capacitance and the Biot criterion). For the electrical-network treatment specifically, any power-electronics thermal text covering Cauer and Foster networks — that's the same two-node ladder, and it's what IGBT datasheets give you as `Zth` curves.