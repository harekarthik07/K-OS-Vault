---
type: concept
domain: power_electronics
project: none
date: 2026-03-30
folder: 04 Knowledge
extracted_concepts:
  - Insulated-Gate Bipolar Transistor
  - Semiconductor Physics
  - Conductivity Modulation
  - Space Vector Modulation
  - MOSFET
  - BJT
  - Silicon Carbide
  - Field-Oriented Control
  - Reverse Recovery Charge
  - Junction Temperature
  - Electro-Thermal Multiphysics
---

# IGBT Physics, Operation & Mathematical Modeling

## Masterclass Roadmap

To master how an [[Insulated-Gate Bipolar Transistor]] (IGBT) works—and why power electronics loss models use specific threshold equations, integrals, and switching energy scalings—the system is broken down step by step:

1. **Step 1: [[Semiconductor Physics]] & Internal Architecture** (Device construction and [[Conductivity Modulation]]).
2. **Step 2: On-State Conduction & The $V_{CE0} + r_C \cdot i$ Mathematical Model** (Connecting solid-state physics to conduction equations).
3. **Step 3: Hard-Switching Dynamics & The Current Tail** (Physical origin of $E_{on}$, $E_{off}$, and recovery losses).
4. **Step 4: [[Space Vector Modulation]] Waveform Integration** (Deriving the $\frac{1}{2\pi} + \frac{m\cos\phi}{8}$ average and $\frac{1}{8} + \frac{m\cos\phi}{3\pi}$ [[Root Mean Square]] geometric terms).

---

## Step 1: [[Semiconductor Physics]] & Internal Architecture

### 1. What is an IGBT?

An [[Insulated-Gate Bipolar Transistor]] is a three-terminal power semiconductor device (Gate, Collector, Emitter) designed to combine the **high input impedance and fast voltage-controlled gate** of a [[MOSFET]] with the **high current density and low saturation voltage** of a [[BJT]] (Bipolar Junction Transistor).

```
        Gate (G)
           │
      ┌────┴────┐
      │ MOSFET  │  (Controls the base current)
      └────┬────┘
           │ (Base current)
      ┌────┴────┐
      │   BJT   │  (Carries high main current with low V_CE)
      └────┬────┘
           │
     Collector (C) / Emitter (E)
```

### 2. Internal Layer Stack & Physical Cross-Section

From top to bottom, a standard vertical N-channel [[Insulated-Gate Bipolar Transistor]] consists of the following layers:

```
[Emitter Metal Contact] ─── (E)
────────────────────────────────────────────
  N+ Source/Emitter  │  P-well (Body)  │  N+ Source/Emitter
─────────────────────┴─────────────────┴────
                     P-Base
────────────────────────────────────────────
              N- Drift Region 
     (Thick, lightly doped; withstands high voltage)
────────────────────────────────────────────
              N+ Buffer Layer (in Punch-Through / Field-Stop IGBTs)
────────────────────────────────────────────
              P+ Collector Substrate
────────────────────────────────────────────
[Collector Metal Contact] ─── (C)
```

* **Gate Terminal:** Sits above a thin Silicon Dioxide ($\text{SiO}_2$) insulating dielectric layer covering the P-well channel region.
* **$N^-$ Drift Region:** A wide, lightly doped layer that sustains the high DC bus voltage ($V_{dc}$) in the off-state.
* **$P^+$ Collector Substrate:** The key feature distinguishing an [[Insulated-Gate Bipolar Transistor]] from a power [[MOSFET]]. In a standard N-channel [[MOSFET]], this bottom layer is $N^+$. Replacing it with a $P^+$ layer forms an internal $P\text{-}N$ junction at the bottom.

### 3. How the IGBT Operates (Turn-On & Conduction)

#### A. MOS Channel Formation
When a positive gate-to-emitter voltage ($V_{GE} > V_{GE(th)}$, typically $+15\text{ V}$) is applied:
* The electric field across the oxide attracts electrons into the surface of the $P$-well.
* This creates a conductive **inversion layer (N-channel)** underneath the gate oxide, connecting the $N^+$ emitter to the $N^-$ drift region.
* Electrons start flowing from the emitter through this MOS channel into the $N^-$ drift region.

#### B. BJT Action & Minority Carrier Injection
* The flow of electrons into the $N^-$ drift region provides the base current for the wide-base $P\text{-}N\text{-}P$ bipolar structure ($P^+$ collector $\rightarrow$ $N^-$ drift $\rightarrow$ $P$-body).
* This forward-biases the bottom $P^+\text{/ }N^-$ junction.
* The $P^+$ substrate injects a massive stream of **minority carriers (holes)** into the $N^-$ drift region.

#### C. [[Conductivity Modulation]] (The Core Superpower of the IGBT)
* The $N^-$ drift region is flooded simultaneously with electrons (from the MOS channel) and holes (from the $P^+$ collector), forming a dense **electron-hole plasma**.
* This high carrier concentration reduces the effective electrical resistivity of the thick $N^-$ drift layer by several orders of magnitude compared to an unmodulated drift region.
* Because of [[Conductivity Modulation]], an [[Insulated-Gate Bipolar Transistor]] can block high voltages ($600\text{ V}$ to $6.5\text{ kV}$) while maintaining a very low on-state voltage drop at hundreds of amperes.

---

## Step 2: The Physical Origin of Loss Equations

```
   V_CE (On-State Voltage)
      ▲
      │                 /  Slope = r_C (Slope resistance)
      │                /
      │               /
      │              /
V_CE0 ┼─────────────/
      │            /
      │           /
      └──────────┴────────────────► Collector Current (I_C)
```

### 1. Why $V_{CE}(i) = V_{CE0} + r_C \cdot i$

The [[Insulated-Gate Bipolar Transistor]] on-state voltage drop is modeled as:

$$V_{CE}(i) = V_{CE0} + r_C \cdot i$$

This equation reflects two internal physical mechanisms:

1. **The Knee / Threshold Voltage ($V_{CE0}$):**
   * Sourced directly from the forward voltage drop of the bottom $P^+\text{-}N$ junction ($P^+$ collector to $N^-$ drift).
   * Even at near-zero current, this junction must be overcome, creating a barrier of approximately $0.7\text{ V}$ to $1.0\text{ V}$.
2. **The Slope Resistance ($r_C$):**
   * Represents the remaining series resistance across the conductivity-modulated drift layer, the MOS inversion channel, and the bulk metallization/bond wires.

### 2. Why IGBT Conduction Loss Uses Both Average and RMS Current

The conduction loss integral is expressed as:

$$P_{cond,T} = V_{CE0} \cdot I_{T,avg} + r_C \cdot I_{T,rms}^2$$

```
Instantaneous Power:  p(t) = v_CE(t) · i(t) = [V_CE0 + r_C · i(t)] · i(t)
                           = V_CE0 · i(t) + r_C · [i(t)]²

Time-Averaged Power:  P_cond,T = V_CE0 · (Average of i(t)) + r_C · (Average of [i(t)]²)
                              = V_CE0 · I_T,avg + r_C · I_T,rms²
```

* **The Threshold Term ($V_{CE0} \cdot I_{T,avg}$):** Linear with respect to current, integrating to the average current $I_{T,avg}$.
* **The Resistive Term ($r_C \cdot I_{T,rms}^2$):** Quadratic with respect to current, integrating to the mean of the current squared ($I_{T,rms}^2$).

> **Key Difference vs. [[Silicon Carbide]] MOSFETs:** A [[MOSFET]] has no internal $P\text{-}N$ junction in its main forward conduction path; it behaves as a pure resistor $R_{DS(on)}$. Consequently, [[MOSFET]] conduction loss scales purely with $I_{rms}^2$. At low currents (light vehicle loads), the [[Insulated-Gate Bipolar Transistor]] continuously pays the $V_{CE0} \cdot I$ threshold penalty, which makes [[Silicon Carbide]] [[MOSFET]] devices significantly more efficient in light-load driving cycles.

---

## Step 3: Hard-Switching Physics & The "Current Tail"

```
Switching Turn-Off Waveforms:

Gate Voltage (V_GE)
 15V ──┐
       └─── 0V / -8V
 Collector-Emitter Voltage (V_CE)
       ┌──────────────── V_dc
 0V ───┘
 Collector Current (I_C)
 I_pk ───┐
         │\  (Fast MOS Channel turn-off)
         │ └───┐  <── Current Tail (Slow minority carrier recombination)
         │     └─── 0A
         │◄────►│
          E_off Energy Loss Area
```

### 1. Turn-On ($E_{on}$)
* When $V_{GE}$ rises above $V_{GE(th)}$, current rises rapidly ($dI_C/dt$) through the MOS channel.
* While current is rising to its peak, the voltage across the device ($V_{CE}$) is still clamped to the DC bus voltage by the inductive load.
* The simultaneous presence of high $V_{CE}$ and high $I_C$ generates the turn-on energy loss $E_{on}$.

### 2. Turn-Off ($E_{off}$) and the Current Tail
* When $V_{GE}$ is pulled low ($0\text{ V}$ or $-8\text{ V}$), the MOS inversion channel closes almost immediately, stopping electron injection.
* However, the $N^-$ drift region is still flooded with stored minority carriers (holes).
* Because the external circuit cannot extract these holes rapidly through the non-conducting top channel, they must either be swept out by the expanding depletion region electric field or decay via natural **carrier recombination**.
* This causes the collector current to exhibit a long decay time, known as the **Current Tail**.
* Because $V_{CE}$ has already recovered back to the full DC bus voltage ($V_{dc}$) while this tail current continues to flow, the power product $V_{CE} \cdot I_{tail}$ dissipates substantial turn-off switching energy ($E_{off}$).

---

## Summary Comparison: IGBT vs. SiC MOSFET

| Parameter / Feature | Silicon [[Insulated-Gate Bipolar Transistor]] | [[Silicon Carbide]] [[MOSFET]] | Engineering Significance |
| :--- | :--- | :--- | :--- |
| **Conduction Mechanism** | Bipolar (Electrons + Holes) with [[Conductivity Modulation]] | Unipolar (Majority Carrier Electrons only) | IGBT achieves high current density at high voltage; SiC has no $P\text{-}N$ forward knee. |
| **On-State Characteristic** | Knee + Slope: $V_{CE0} + r_C \cdot i$ | Purely Resistive: $R_{DS(on)} \cdot i$ | SiC is much more efficient at light/partial loads. |
| **Turn-Off Tail Current** | Yes (Minority carrier recombination) | No (Pure majority carrier device) | SiC achieves significantly lower $E_{off}$, enabling higher switching frequencies ($f_{sw}$). |
| **Freewheeling Path** | Requires separate antiparallel diode | Body diode / Synchronous channel rectification | IGBT inverter modules require copackaged Si/SiC diodes. |

---

## Step 4: Demystifying SVPWM Integrals & Scaling

To accurately calculate inverter losses without needing complex, real-time transient simulations, closed-form mathematical integrals are used. These equations take the dynamic switching and conduction behavior of the [[Insulated-Gate Bipolar Transistor]] and average it over one fundamental electrical output period.

### 1. Core Functions: Current and Duty Cycle

When driving a motor using [[Space Vector Modulation]] (SVPWM) and [[Field-Oriented Control]] (FOC), two primary functions dictate heat generation in semiconductors:

* **The Phase Current:** Modeled as a sinusoidal wave, $i(t) = I_{pk}\sin(\omega t)$.
* **The [[Space Vector Modulation]] Duty Function:** The fraction of time a specific transistor is conducting at any given moment, defined as $d(t) = \frac{1}{2}[1 + m\cos\phi\sin(\omega t)]$.

To find the average or [[Root Mean Square]] power loss, integrate the product of these functions over the $180^\circ$ window where the specific switch conducts.

### 2. Deriving Conduction Factors

#### A. Average Current Integral (For $V_{CE0}$ Threshold)
Because an [[Insulated-Gate Bipolar Transistor]] has a constant threshold voltage penalty ($V_{CE0}$) scaling linearly with current, the average current $I_{T,avg}$ is determined by integrating $i(t) \cdot d(t)$ over the conducting half-cycle:

$$I_{T,avg} = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}\sin(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding this integration splits into two distinct terms:
1. **The $\frac{1}{2\pi}$ Baseline:** The integral of the first half ($\frac{1}{2}\sin(x)$) yields the average-current baseline of $\frac{1}{2\pi} \approx 0.1592$. This represents the basic, load-independent average current term.
2. **The $\frac{1}{8}$ Modulation Term:** The integral of the second half ($\frac{1}{2}\sin^2(x)$) yields the $\frac{m\cos\phi}{8}$ term.

Resulting in:

$$I_{T,avg} = I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right)$$

#### B. RMS Squared Integral (For $I^2R$ Losses)
For slope resistance ($r_C$) and [[MOSFET]] $R_{DS(on)}$, power dissipates quadratically ($I^2R$). Integrate $i^2(t) \cdot d(t)$ to find $I_{T,rms}^2$:

$$I_{T,rms}^2 = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}^2\sin^2(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding this reveals:
1. **The $\frac{1}{8}$ Term:** Derived directly from integrating $\frac{1}{2}\sin^2(x)$ over a half-cycle. It serves as the $\sin^2$ load-independent conduction baseline.
2. **The $\frac{1}{3\pi}$ Term:** The geometric integral of $\sin^3(x)$ from $0$ to $\pi$ evaluates to $\frac{4}{3}$. Multiplying by duty coefficients and averaging yields $\frac{1}{3\pi} \approx 0.1061$. This acts as the power-factor and modulation correction.

Resulting in:

$$I_{T,rms}^2 = I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

### 3. Deriving Switching Averaging Factors

Switching losses ($E_{on} + E_{off}$) occur at every PWM pulse and scale linearly with instantaneous current at the moment of switching.

* **The $\frac{1}{\pi}$ Factor (Per Device):** A transistor only hard-switches during approximately half of the fundamental period. The mathematical mean of $\sin$ is $\frac{2}{\pi} \approx 0.6366$. Combining the half-period switching window with this sine average gives the $\frac{1}{\pi} \approx 0.3183$ per-device averaging factor.
* **The $\frac{6}{\pi}$ Factor (System Aggregate):** Summing six switches staggered $60^\circ$ apart gives an aggregate factor of $\frac{6}{\pi} \approx 1.910$. Naïvely multiplying peak switching loss by 6 overestimates switching loss by a factor of $\frac{\pi}{2} \approx 1.57\times$.

---

## Master Glossary: Engineering Acronyms

| Acronym | Full Form | Meaning in Solid-State & Thermal Physics |
| :--- | :--- | :--- |
| **IGBT** | **[[Insulated-Gate Bipolar Transistor]]** | Main semiconductor switch combining fast voltage control of a [[MOSFET]] with high current density of a [[BJT]]. |
| **MOSFET** | **Metal-Oxide-Semiconductor Field-Effect Transistor** | Unipolar switch behaving purely like a resistor ($R_{DS(on)}$) when conducting, with no threshold voltage knee. |
| **SiC** | **[[Silicon Carbide]]** | Wide-bandgap material with near-zero [[Reverse Recovery Charge]] ($Q_{rr} \approx 0$) and reduced switching losses. |
| **FOC** | **[[Field-Oriented Control]]** | Vector control algorithm managing magnetic flux ($I_d$) and torque ($I_q$) independently. |
| **SVPWM** | **[[Space Vector Modulation]]** | PWM technique defining the duty cycle equation $d(t) = \frac{1}{2}[1 + m\cos\phi\sin(\omega t)]$. |
| **PMSM / IPMSM**| **Permanent Magnet Synchronous Motor** | Traction motor topologies driven by three-phase inverters. |
| **RMS** | **[[Root Mean Square]]** | Effective heating value of AC current, critical for quadratic $I^2R$ power loss. |
| **ETM** | **[[Electro-Thermal Multiphysics]]** | Coupled electromagnetic and heat transfer simulation environment. |
| **CFD** | **[[Computational Fluid Dynamics]]** | Fluid flow and convection modeling solving Navier-Stokes equations. |
| **URANS** | **Unsteady Reynolds-Averaged Navier-Stokes** | Transient CFD model resolving time-averaged turbulent flows. |
| **LES** | **[[Large Eddy Simulation]]** | High-fidelity turbulence model resolving large eddies directly. |
| **AEDT** | **[[Ansys Electronics Desktop]]** | Engineering simulation suite integrating electromagnetic and thermal solvers. |
| **BOI** | **Body of Influence** | Mesh refinement boundary used in [[Computational Fluid Dynamics]] to control mesh density. |

---

## Module 1 Masterclass: The Physics Behind the Math

Total heat dissipation flowing into a heatsink baseplate per switch position is modeled as:

$$P_{switch} = P_{cond,T} + P_{sw,T} + P_{cond,D} + P_{rr,D}$$

### 1. Transistor Conduction Loss ($P_{cond,T}$)
Due to the built-in $P\text{-}N$ junction in an [[Insulated-Gate Bipolar Transistor]], a threshold voltage drop ($V_{CE0}$) exists alongside slope resistance ($r_C$).
* **Threshold Term ($V_{CE0} \cdot I_{T,avg}$):** Voltage drop is linear with current, integrated using average current $I_{T,avg}$.
* **Resistive Term ($r_C \cdot I_{T,rms}^2$):** Slope resistance causes quadratic $I^2R$ heating, integrated using [[Root Mean Square]] current squared ($I_{T,rms}^2$).

### 2. Transistor Switching Loss ($P_{sw,T}$)
Dynamic heat generated by toggling the [[Insulated-Gate Bipolar Transistor]] at switching frequency ($f_{sw}$):

$$P_{sw,T} = f_{sw} (E_{on} + E_{off}) \left( \frac{V_{dc}}{V_{ref}} \right) \left( \frac{I_{pk}}{I_{ref}} \right) \left( \frac{1}{\pi} \right)$$

* **Sinusoidal Averaging ($\frac{1}{\pi}$):** Because phase current varies sinusoidally, switches do not hard-switch at $I_{pk}$ continuously. Averaging over the active half-cycle yields $\frac{1}{\pi}$.

### 3. Diode Losses ($P_{cond,D}$ and $P_{rr,D}$)
When the [[Insulated-Gate Bipolar Transistor]] turns off, inductive phase current freewheels through the antiparallel diode.
* **Duty Complement ($1/2\pi - m\cos\phi/8$):** The negative sign reflects complementary conduction: higher transistor duty reduces freewheel diode conduction time.
* **Reverse Recovery ($P_{rr,D}$):** Dissipation from sweeping out minority [[Reverse Recovery Charge]] ($Q_{rr}$) when the diode turns off.

---

## Parameter Breakdown

### 1. On-State & Conduction Terms
* **$V_{CE}$ (Collector-Emitter Voltage):** Total voltage drop across the [[Insulated-Gate Bipolar Transistor]] during conduction.
* **$V_{CE0}$ (Threshold / Knee Voltage):** Forward drop of the internal $P\text{-}N$ junction ($0.7\text{ V}$ to $1.0\text{ V}$), multiplied by average current.
* **$r_C$ (Slope Resistance):** Bulk electrical resistance across the drift layer and channel, causing $I^2R$ loss multiplied by [[Root Mean Square]] current squared. Formula: $V_{CE}(i) = V_{CE0} + r_C \cdot i$.

### 2. Motor Control Variables (SVPWM)
* **$m$ (Modulation Index):** Ratio ($0$ to $1.0$) of commanded output voltage to available DC bus voltage.
* **$\cos\phi$ (Displacement Power Factor):** Cosine of the phase angle between voltage and current waveforms.
* **Combined Factor ($m\cos\phi$):** Modulates duty cycle distribution between active switch conduction and freewheeling diode conduction.

### 3. Switching Energy & Scaling Terms
* **$E_{on}, E_{off}$ (Turn-On / Turn-Off Energy):** Energy loss per switching event ($\mu\text{J}$). $E_{off}$ is dominated by the current tail.
* **$V_{ref}, I_{ref}$ (Reference Conditions):** Datasheet lab test parameters.
* **$V_{dc}$ (DC Bus Voltage):** Operational DC bus voltage across the inverter.
* **Scaling Ratio ($\frac{V_{dc}}{V_{ref}} \cdot \frac{I_{pk}}{I_{ref}}$):** Linearly scales lab switching loss measurements to operational voltage and peak current levels.

### 4. Critical Environmental & Operating Parameters
* **$f_{sw}$ (Switching Frequency):** PWM carrier frequency (typically $10\text{ kHz}$ to $20\text{ kHz}$). Switching losses scale linearly with $f_{sw}$.
* **$Q_{rr}$ ([[Reverse Recovery Charge]]):** Charge trapped in the diode junction that must be cleared during turn-off.
* **$T_j$ ([[Junction Temperature]]):** Silicon die temperature (typically operating up to $150^\circ\text{C}$). Increased $T_j$ increases effective resistance and switching energy, requiring thermal feedback in power modeling.

---

## Atlas Connections

* [[Power Electronics]]
* [[Thermal Management]]
* [[Motor Control]]
* [[Semiconductor Physics]]