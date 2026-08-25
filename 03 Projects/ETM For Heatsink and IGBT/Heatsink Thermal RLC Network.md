---
title: Heatsink Thermal RLC Network — Foster and Cauer
aliases:
  - Heatsink RLC Network
  - Thermal Circuit Model
  - Foster vs Cauer for Heatsink
  - Cauer Network Explanation
tags:
  - thermal/heat-transfer
  - thermal/transient
  - thermal/resistance-network
  - method/lumped-capacitance
  - method/foster-network
  - method/cauer-network
  - domain/ETM
  - project/T30
  - type/reference
  - status/verified
up: "[[Electro-Thermal Management MOC]]"
related:
  - "[[Heatsink Theory and Worked Example]]"
  - "[[Heatsink Hand Calculation Worksheet]]"
  - "[[Dyno Run 44 Data]]"
  - "[[Thermal Time Constant]]"
  - "[[Lumped Capacitance Method]]"
created: 2026-08-19
---

# Heatsink Thermal RLC Network

> [!abstract] What this note covers
> How to represent the IGBT-on-heatsink thermal path as an equivalent electrical circuit. Why it's called "RLC" but really has no L. The two competing modelling philosophies — **Foster** (mathematical, fits terminal behaviour) and **Cauer** (physical, ladder of real material layers) — when each applies, and where they can and cannot be identified from measurement.

---
![[corrected_parallel_RC_network.png]]
## 1. Why draw it as a circuit at all

Every heat transfer mechanism reduces to $\Delta T = q R$ or $q = C\,dT/dt$. Those are Ohm's law and the capacitor equation with different labels.
Once every layer is drawn as an electrical component, three things become free:

1. **Kirchhoff's laws apply directly** — KCL at every node, KVL around every loop.
2. **Existing circuit tools work** — Simulink, PLECS, SPICE all solve thermal circuits without modification.
3. **Intuition transfers** — engineers who understand RC filters immediately understand RC thermal networks.

## 2. The "RLC" name — and why there's no L

^no-inductance

Full electrical circuits have R (resistance), L (inductance) and C (capacitance).

Thermal circuits use only **R and C**. Inductance has no thermal analogue because:

- Inductance opposes *changes in current*. Heat has no momentum — you can start and stop a heat flow instantly and no back-force arises.
- Inductance stores energy in a magnetic field. Heat stores energy only as raised temperature of matter — that's capacitance.

So while people say "RLC network" out of habit, thermal networks are strictly **RC**. If you ever see an inductor in a thermal circuit diagram, it's a mistake.

> [!info] Named after the family, used in a subset
> Same as how "arithmetic" covers add, subtract, multiply, divide — you can do a whole calculation using only add and subtract. "RLC network" names the family; the thermal subset uses R and C only.

## 3. Sign convention and the "current source" for heat

^current-source-analogy

In electrical circuits current usually comes from a voltage source. In thermal circuits **heat comes from a current source** — the IGBT dumps a specified number of watts regardless of how hot things get.

$$Q_{IGBT} \equiv \text{current source injecting 636 W}$$

Ambient temperature is the reference — the **ground rail**. Just like an electrical ground, every capacitor's other terminal connects to it because temperatures are all measured *relative* to ambient.

$$T_\infty \equiv \text{voltage source fixed at 34 °C, pinned to ground rail}$$

## 4. The building blocks

^building-blocks

| Physical layer | Component | Symbol | Units |
|---|---|---|---|
| Heat generated in silicon | Current source | Q | W |
| Thermal path resistance | Resistor | R | K/W |
| Material that stores heat | Capacitor to ground | C | J/K |
| Ambient temperature | Fixed voltage source | T∞ | K or °C |
| A node in the metal | Voltage node | T | K or °C |

Every capacitor has **one terminal at a temperature node and one terminal at ambient**. This is the same as electrical — a capacitor storing energy is measured against ground.



**Six R's and two C's.** The full parameter table:



### The Updated Parameter Table

Using the corrected 3.36 kg casting mass and the CFD-derived parallel split, the full physical parameter set is:

|**Component**|**Value**|**Physical meaning**|
|---|---|---|
|$Q$|568 W|Corrected IGBT loss back-calculated using 3.3 kg casting|
|$R_{JC}$|0.042 K/W|Silicon-to-case, 6 dies in parallel|
|$R_{TIM}$|0.010 K/W|Fasto paste, 100 μm[cite: 5, 6]|
|$R_{conv,B}$|5.0 K/W|Base region under IGBT (Fan dead zone, low $h$)|
|$R_{metal}$|~0.03 K/W|Lateral solid conduction through spider arms to outer fins|
|$R_{conv,HS}$|0.108 K/W|Outer fins and casing walls (High $h$)|
|$C_{plate}$|~1300 J/K|Baseplate-region mass, fast response[cite: 5, 6]|
|$C_{hs}$|~1600 J/K|Rest of the heatsink, slow response[cite: 5, 6]|

> [!danger] The Engineering Takeaway
> 
> $R_{conv,B}$ is so massive (5.0 K/W) that it acts as a thermal dead end. It carries only **12 W (2%)** of the total heat. Nearly ALL the heat (556 W, 98%) is forced to violently conduct laterally through $R_{metal}$ to reach the outer fins. **The direct base path is thermally useless.**

## 6. Applying Kirchhoff's laws — The Parallel ODEs

^governing-equations-parallel

At each node with capacitance, **KCL** dictates: heat flowing in − heat flowing out = rate of energy stored.

Because of the parallel split, the baseplate node ($T_{plate}$) now has **three** heat flow paths plus its storage:

**At the baseplate node** ($T_{plate}$):

$$\frac{T_c - T_{plate}}{R_{TIM}} - \frac{T_{plate} - T_{hs}}{R_{metal}} - \frac{T_{plate} - T_\infty}{R_{conv,B}} = C_{plate}\frac{dT_{plate}}{dt}$$

**At the outer heatsink node** ($T_{hs}$) (Unchanged in form):

$$\frac{T_{plate} - T_{hs}}{R_{metal}} - \frac{T_{hs} - T_\infty}{R_{conv,HS}} = C_{hs}\frac{dT_{hs}}{dt}$$

Solving these two coupled ODEs yields $T_{plate}(t)$ and $T_{hs}(t)$. Because $R_{JC}$ and $R_{TIM}$ are pure resistors with zero thermal mass, the case and junction temperatures react instantly and follow by simple algebra:

$$T_c(t) = T_{plate}(t) + Q \cdot R_{TIM}$$

$$T_j(t) = T_c(t) + Q \cdot R_{JC}$$

> [!important] The NTC reads $T_c$ The sensor sits at the case node, below the junction. Junction-to-case resistance is _above_ the sensor and does not appear in the reading.

## 7. Circuit behaviour at limiting times

^limiting-behaviour

### At t = 0⁺ (instant power on)

Both capacitors are uncharged, so they act like **short circuits** to ambient — meaning $T_{plate} = T_{hs} = T_\infty$ initially. All the injected heat can pass through the resistor chain, but the temperature rises are still zero because the caps hold the nodes down.

**Only the pure-resistor drops appear instantly.** The junction and case nodes jump immediately:

$$T_c(0^+) = T_\infty + 0 \quad \text{(caps hold plate at ambient)}$$

Wait — that isn't right. Let me be careful. Since $Q$ is a current source, the heat has to go somewhere. It flows into $C_{plate}$ initially, causing $T_{plate}$ to rise at rate $Q/C_{plate}$. So the instant behaviour is:

- $Q$ starts charging $C_{plate}$ first (nearest to source)
    
- $T_{plate}$ ramps up from 0 at initial rate $Q/C_{plate}$
    
- Once $T_{plate} > T_{hs}$, heat starts flowing through $R_{metal}$ to charge $C_{hs}$
    

### As t → ∞ (steady state)

Both capacitors are fully charged. No current flows into or out of them, so they act like **open circuits**. All the heat flows through the resistors straight to ambient:

$$T_{hs} = T_\infty + Q \cdot R_{conv, parallel} = 34 + 568 \times 0.1057 = 94\ \text{°C}$$

Same as if the capacitors weren't there. Which makes sense — steady state is where nothing changes, so storage is irrelevant.

## 8. What you can and can't identify from measurement

^identifiability

This is the crucial epistemological point.

Dyno run 44 gives **one temperature vs time curve** from **one sensor**. Fitting two exponentials extracts four numbers:

$$A_1 = 13.6\ \text{K}, \quad \tau_1 = 28\ \text{s}, \quad A_2 = 60.0\ \text{K}, \quad \tau_2 = 304\ \text{s}$$

That's it. **Four measurements.** But the full parallel circuit has:

$$R_{JC},\ R_{TIM},\ R_{metal},\ R_{conv,B},\ R_{conv,HS},\ C_{plate},\ C_{hs} \;=\; 7 \text{ unknowns}$$

**Seven unknowns from four measurements = underdetermined system**. Many combinations of resistances and capacitances produce the same measured curve.

To identify them, one of the following is needed:

|**Approach**|**What it does**|**Effort**|
|---|---|---|
|**Add a second sensor**|thermocouple on fin root → 8 measurements → full system identifiable|30 minutes|
|**Use datasheet values**|$R_{JC}$, $R_{TIM}$ known independently — reduces unknowns|free|
|**Use CAD/FEA**|steady-state conduction solve → geometric split of the 3.36 kg mass and $h$ mappings[cite: 5, 6]|1 hour|
|**Accept the terminal fit**|model reproduces measured behaviour but internal states are guesses|free — see [[#9. Foster network]]|

## 9. Foster network

^foster-network

A Foster network is a **sum of independent RC pairs, all in parallel between the source and ambient**:

```
                    Q
                    │
       ┌────┬────┬──┴──┬────┐
       │    │    │     │    │
       R₁   R₂  ...    Rₙ   Rn+1
       │    │          │    │
       C₁   C₂         Cₙ   (final resistor to ambient)
       │    │          │    │
      GND  GND        GND  GND
```

**Mathematical form:**

$$\theta(t) = \sum_{i=1}^n A_i\left(1 - e^{-t/\tau_i}\right), \qquad A_i = QR_i,\ \tau_i = R_iC_i$$

### Advantages

- **Direct from measurement** — every $(A_i, \tau_i)$ pair extracts trivially by curve fitting
    
- **Exact terminal behaviour** — reproduces measured $T(t)$ perfectly at the sensor
    
- **Standard datasheet form** — most IGBT/MOSFET datasheets specify $Z_{th}$ as Foster pairs
    

### The critical limitation

^foster-caveat

**Foster elements are mathematical, not physical.**

- $R_1$ does NOT correspond to a specific real layer
    
- $C_1$ does NOT equal any real chunk of material's $mc_p$
    
- Node temperatures in the Foster circuit have **no physical meaning** — the intermediate nodes are fictions
    

Foster is a **signal-processing model**. It works because any decaying transient can be decomposed into a sum of exponentials (like a Fourier series decomposes waveforms into sines). The RC pairs are the _coefficients_ of that decomposition, not physical objects.

> [!caution] What this means for design work Foster is useful for **predicting terminal temperatures**. It is useless for asking "how hot is the baseplate?" or "what if I change the TIM?" — because the elements don't correspond to anything you can change.

## 10. Cauer network

^cauer-network

A Cauer network is a **ladder** — R's in series along the top rail, C's dropping to ground between them:

```
    Q ──R₁──┬──R₂──┬──R₃──┬── ... ──── ambient
            │       │       │
            C₁      C₂      C₃
            │       │       │
           GND     GND     GND
```

Each R–C pair maps onto a **real material layer** in the physical stack.

### Advantages

- **Physically meaningful** — each node is a real temperature you could measure with a thermocouple
    
- **Compositional** — replace the TIM in reality → change $R_{TIM}$ in the model → results correctly reflect the change
    
- **Debuggable** — if the model diverges from measurement, you can point at _which layer_ is wrong
    

### The limitation

^cauer-caveat

Cauer is **harder to build**. It requires either:

- Detailed knowledge of every physical layer's mass, geometry and material, OR
    
- Multiple sensors to identify the ladder from measurement
    

You cannot convert a Foster fit into a Cauer ladder without additional information. There's a mathematical mapping only in specific cases and it can produce negative or physically impossible values.

## 11. Foster vs Cauer — decision table

^decision-table

|**You are...**|**Use**|**Why**|
|---|---|---|
|Reading a datasheet's $Z_{th}$ curve|**Foster**|that's how they're published|
|Predicting deration time on a known design|**Foster**|terminal behaviour is what matters|
|Designing a new heatsink|**Cauer**|you need to change individual layers|
|Interpreting the mass split from dyno data|**Cauer with caveats**|see below|
|Running Simulink for our T30 model|**Cauer** with 2 masses + measured R's|matches physics, tuneable|

### For our current situation

Our Simulink model should be **Cauer-form** because we want to change design parameters (fin area, mass, TIM) and see the effect. But we should be honest that **our 2-mass split is a physically-motivated guess, calibrated to match the measured Foster fit** — not a directly measured Cauer decomposition.

The workflow becomes:

1. Build Cauer network in Simulink with parameters estimated from geometry
    
2. Run the model, extract simulated NTC response
    
3. Curve-fit that simulated response as a Foster network (2 exponentials)
    
4. Compare Foster $(A_1, \tau_1, A_2, \tau_2)$ against measured
    
5. Iterate on the Cauer parameters until they match
    

## 12. The equivalence at the terminals

^foster-cauer-equivalent

Both networks can produce the **same measured NTC response**. That's the whole point — they're both valid representations of the terminal behaviour.

The difference is _inside_ the network:

|**Property**|**Foster**|**Cauer**|
|---|---|---|
|Terminal $T(t)$|Identical|Identical|
|Internal node meaning|None|Real material temperatures|
|Extractable from single-sensor data|Yes|No (underdetermined)|
|Element changes when hardware changes|Refit required|Direct parameter change|

## 13. Implementation checklist for Simulink

^simulink-checklist

Simscape blocks for the Cauer form:

- [ ] **Thermal Reference** → the ambient ground rail
    
- [ ] **Ideal Temperature Source** → sets ambient (input from Simulink signal)
    
- [ ] **Ideal Heat Flow Source** → injects Q (from losses model)
    
- [ ] **Thermal Resistor** → $R_{JC}$ = 0.042 K/W
    
- [ ] **Thermal Resistor** → $R_{TIM}$ = 0.010 K/W
    
- [ ] **Thermal Mass** → $C_{plate}$ (mass ≈ 1300 J/K)
    
- [ ] **Thermal Resistor** → $R_{metal}$ ≈ 0.03 K/W (lateral conduction)
    
- [ ] **Thermal Mass** → $C_{hs}$ (mass ≈ 1600 J/K)
    
- [ ] **Thermal Resistor** → $R_{conv,HS}$ = 0.108 K/W
    
- [ ] **Thermal Resistor** → $R_{conv,B}$ = 5.0 K/W
    

Plus sensors:

- [ ] **Temperature Sensor** at the case node → compare against measured NTC
    
- [ ] **Temperature Sensor** at the heatsink node → useful for future fin-thermocouple validation
    

## 14. Validation targets

^validation-targets

Once the model runs, it must reproduce these from dyno run 44[cite: 5]:

|**Check**|**Target**|**Tolerance**|
|---|---|---|
|$T_c$ at 244 s|80.9 °C[cite: 5]|±1 K[cite: 5]|
|Total rise at 250 s|47.0 K[cite: 5]|±1 K[cite: 5]|
|Time to reach 95 °C|8.5 min[cite: 5]|±30 s[cite: 5]|
|Steady state extrapolation|108 °C[cite: 5]|±3 K[cite: 5]|
|Foster fit $A_1$|13.6 K[cite: 5]|±1 K[cite: 5]|
|Foster fit $\tau_1$|28 s[cite: 5]|±5 s[cite: 5]|
|Foster fit $A_2$|60.0 K[cite: 5]|±3 K[cite: 5]|
|Foster fit $\tau_2$|304 s[cite: 5]|±20 s[cite: 5]|

If simulated NTC matches all eight, the Cauer parameters are calibrated correctly[cite: 5].

## Notes to create from this

**Method notes**

- [[Foster Network]] — mathematical sum of RC pairs, see ^foster-network[cite: 5]
    
- [[Cauer Network]] — physical ladder of RC pairs, see ^cauer-network[cite: 5]
    
- [[Foster vs Cauer Networks]] — comparison, see ^decision-table[cite: 5]
    
- [[Thermal RC Network]] — general concept, see ^building-blocks[cite: 5]
    
- [[System Identifiability]] — why measurements limit models, see ^identifiability[cite: 5]
    

**Related in this vault**

- [[Heatsink Theory and Worked Example]] — the physics behind every R and C[cite: 5]
    
- [[Heatsink Hand Calculation Worksheet]] — pen-and-paper walkthrough[cite: 5]
    
- [[Dyno Run 44 Data]] — the four measured Foster parameters[cite: 5]
    
- [[HS-I1 Heatsink Spec]] — the physical mass, area, material inputs[cite: 5]
    

## Transclusion examples

```
![[Heatsink Thermal RLC Network#^full-circuit]]
![[Heatsink Thermal RLC Network#^cauer-mapping]]
![[Heatsink Thermal RLC Network#^validation-targets]]
```
