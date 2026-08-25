---
type: engineering_note
domain: power_electronics
project: none
date: 2026-03-30
folder: 04 Knowledge
extracted_concepts:
  - IGBT
  - Conductivity Modulation
  - Space-Vector Pulse Width Modulation
  - Conduction Loss
  - Switching Loss
  - Current Tail
  - SiC MOSFET
  - Reverse Recovery Charge
---

# IGBT Physics, Mathematical Modeling & SVPWM Integration

## Masterclass Roadmap Overview

To model an [[Insulated Gate Bipolar Transistor]] ([[IGBT]]) with specific threshold equations, closed-form integrals, and switching energy scalings, the physical behavior is structured into four core areas:

1. **Semiconductor Physics & Internal Architecture:** Layer construction and [[Conductivity Modulation]].
2. **On-State Conduction & Mathematical Modeling:** Connecting solid-state mechanisms to the $V_{CE0} + r_C \cdot i$ conduction model.
3. **Hard-Switching Dynamics & The Current Tail:** Physical origin of [[Turn-On Loss]] ($E_{on}$), [[Turn-Off Loss]] ($E_{off}$), and [[Reverse Recovery]] losses.
4. **SVPWM Waveform Integration:** Deriving the geometric integration terms for [[Space-Vector Pulse Width Modulation]] ([[SVPWM]]).

---

## Step 1: Semiconductor Physics & Internal Architecture

### 1. Device Definition

An [[IGBT]] is a three-terminal power semiconductor device ([[Gate Terminal]], [[Collector Terminal]], [[Emitter Terminal]]) designed to combine the high input impedance and fast voltage-controlled gate of a power [[MOSFET]] with the high current density and low saturation voltage of a [[Bipolar Junction Transistor]] ([[BJT]]).

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

From top to bottom, a standard vertical N-channel [[IGBT]] consists of the following layers:

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
* **$P^+$ Collector Substrate:** The key feature distinguishing an [[IGBT]] from a power [[MOSFET]]. In a standard N-channel [[MOSFET]], this bottom layer is $N^+$. Replacing it with a $P^+$ layer forms an internal $P\text{-}N$ junction at the bottom.

### 3. Device Operation (Turn-On & Conduction)

#### MOS Channel Formation
When a positive gate-to-emitter voltage ($V_{GE} > V_{GE(th)}$, typically $+15\text{ V}$) is applied:
* The electric field across the oxide attracts electrons into the surface of the P-well.
* This creates a conductive **[[Inversion Layer]] (N-channel)** underneath the [[Gate Oxide]], connecting the $N^+$ emitter to the $N^-$ [[Drift Region]].
* Electrons flow from the emitter through this MOS channel into the $N^-$ drift region.

#### BJT Action & Minority Carrier Injection
* The flow of electrons into the $N^-$ drift region provides the base current for the wide-base $P\text{-}N\text{-}P$ bipolar structure ($P^+$ collector $\rightarrow$ $N^-$ drift $\rightarrow$ P-body).
* This forward-biases the bottom $P^+\text{/ }N^-$ junction.
* The $P^+$ substrate injects a massive stream of **minority carriers (holes)** into the $N^-$ drift region.

#### Conductivity Modulation
* The $N^-$ drift region is flooded simultaneously with electrons (from the MOS channel) and holes (from the $P^+$ collector), forming a dense **[[Electron-Hole Plasma]]**.
* This high carrier concentration reduces the effective electrical resistivity of the thick $N^-$ drift layer by several orders of magnitude compared to an unmodulated drift region.
* Because of [[Conductivity Modulation]], an [[IGBT]] can block high voltages ($600\text{ V}$ to $6.5\text{ kV}$) while maintaining a low on-state voltage drop at hundreds of amperes.

---

## Step 2: Physical Origin of Loss Equations

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

### 1. Mathematical Model: $V_{CE}(i) = V_{CE0} + r_C \cdot i$

The [[IGBT]] on-state voltage drop is modeled as:

$$V_{CE}(i) = V_{CE0} + r_C \cdot i$$

This equation reflects two internal physical mechanisms:

1. **Threshold Voltage ($V_{CE0}$):** Sourced directly from the forward voltage drop of the bottom $P^+\text{-}N$ junction ($P^+$ collector to $N^-$ drift). Even at near-zero current, this junction must be overcome, creating a barrier of approximately $0.7\text{ V}$ to $1.0\text{ V}$.
2. **Slope Resistance ($r_C$):** Represents the remaining series resistance across the conductivity-modulated drift layer, the MOS inversion channel, and the bulk metallization/bond wires.

### 2. Conduction Loss Modeling (Average vs. RMS Current)

The conduction loss integral is written as:

$$P_{cond,T} = V_{CE0} \cdot I_{T,avg} + r_C \cdot I_{T,rms}^2$$

```
Instantaneous Power:  p(t) = v_CE(t) · i(t) = [V_CE0 + r_C · i(t)] · i(t)
                           = V_CE0 · i(t) + r_C · [i(t)]²

Time-Averaged Power:  P_cond,T = V_CE0 · (Average of i(t)) + r_C · (Average of [i(t)]²)
                              = V_CE0 · I_T,avg + r_C · I_T,rms²
```

* **Threshold Term ($V_{CE0} \cdot I_{T,avg}$):** Linear with respect to current, integrating to the average current $I_{T,avg}$.
* **Resistive Term ($r_C \cdot I_{T,rms}^2$):** Quadratic with respect to current, integrating to the mean of the current squared ($I_{T,rms}^2$).

> **Comparison vs. SiC MOSFETs:** A [[SiC MOSFET]] has no internal $P\text{-}N$ junction in its main forward conduction path; it behaves as a pure resistor $R_{DS(on)}$. Consequently, [[MOSFET]] conduction loss scales purely with $I_{rms}^2$. At light loads, the [[IGBT]] continuously pays the $V_{CE0} \cdot I$ threshold penalty, making [[SiC MOSFET]] devices more efficient under light-load operating conditions.

---

## Step 3: Hard-Switching Physics & The Current Tail

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

### 1. Turn-On Loss ($E_{on}$)
* When $V_{GE}$ rises above $V_{GE(th)}$, current rises rapidly ($dI_C/dt$) through the MOS channel.
* While current is rising to its peak, the voltage across the device ($V_{CE}$) remains clamped to the DC bus voltage by the inductive load.
* The simultaneous presence of high $V_{CE}$ and high $I_C$ generates the turn-on energy loss $E_{on}$.

### 2. Turn-Off Loss ($E_{off}$) and the Current Tail
* When $V_{GE}$ is pulled low ($0\text{ V}$ or $-8\text{ V}$), the MOS inversion channel closes rapidly, stopping electron injection.
* However, the $N^-$ drift region remains flooded with stored minority carriers (holes).
* Because the external circuit cannot extract these holes rapidly through the non-conducting top channel, they must be swept out by the expanding depletion region electric field or decay via natural **carrier recombination**.
* This causes the collector current to exhibit a long decay time, known as the **[[Current Tail]]**.
* Because $V_{CE}$ has already recovered back to the full DC bus voltage ($V_{dc}$) while this tail current continues to flow, the power product $V_{CE} \cdot I_{tail}$ dissipates substantial turn-off switching energy ($E_{off}$).

### 3. Structural Comparison: Silicon IGBT vs. SiC MOSFET

| Parameter / Feature | [[Silicon IGBT]] | [[SiC MOSFET]] | Engineering Significance |
| :--- | :--- | :--- | :--- |
| **Conduction Mechanism** | Bipolar (Electrons + Holes) with [[Conductivity Modulation]] | Unipolar (Majority Carrier Electrons only) | [[IGBT]] achieves high current density at high voltage; [[SiC]] has no $P\text{-}N$ forward knee. |
| **On-State Characteristic** | Knee + Slope: $V_{CE0} + r_C \cdot i$ | Purely Resistive: $R_{DS(on)} \cdot i$ | [[SiC]] is much more efficient at light/partial loads. |
| **Turn-Off Tail Current** | Yes (Minority carrier recombination) | No (Pure majority carrier device) | [[SiC]] achieves lower $E_{off}$, enabling higher [[Switching Frequency]] ($f_{sw}$). |
| **Freewheeling Path** | Requires separate [[Antiparallel Diode]] | Body diode / Synchronous channel rectification | [[IGBT]] inverter modules require copackaged Si or SiC diodes. |

---

## Step 4: SVPWM Waveform Integration

Closed-form mathematical integrals allow calculation of inverter losses over one fundamental electrical output period without transient time-domain simulation.

### 1. Core Functions: Current and Duty Cycle

When driving a motor using [[Space-Vector Pulse Width Modulation]] ([[SVPWM]]) and [[Field-Oriented Control]] ([[Field-Oriented Control|FOC]]), two primary functions dictate semiconductor heat generation:

* **Phase Current:** Modeled as a sinusoidal wave, $i(t) = I_{pk}\sin(\omega t)$.
* **SVPWM Duty Function:** The fraction of time a specific transistor conducts, defined as:

$$d(t) = \frac{1}{2}[1 + m\cos\phi\sin(\omega t)]$$

### 2. Conduction Integrals

#### Average Current Integral (For $V_{CE0}$)

Integrating $i(t) \cdot d(t)$ over the conducting half-cycle yields $I_{T,avg}$:

$$I_{T,avg} = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}\sin(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding this integration splits into two terms:

1. **Baseline Term ($\frac{1}{2\pi}$):** The integral of $\frac{1}{2}\sin(x)$ yields $\frac{1}{2\pi} \approx 0.1592$. This represents the load-independent average current baseline.
2. **Modulation Term ($\frac{1}{8}$):** The integral of $\frac{1}{2}\sin^2(x)$ yields the $\frac{m\cos\phi}{8}$ term.

Final closed-form expression:

$$I_{T,avg} = I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right)$$

#### RMS Squared Integral (For $I^2R$ Losses)

Integrating $i^2(t) \cdot d(t)$ yields $I_{T,rms}^2$:

$$I_{T,rms}^2 = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}^2\sin^2(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding the terms:

1. **Baseline Term ($\frac{1}{8}$):** Derived from integrating $\frac{1}{2}\sin^2(x)$ over a half-cycle.
2. **Modulation Correction ($\frac{1}{3\pi}$):** The geometric integral of $\sin^3(x)$ from $0$ to $\pi$ evaluates to $\frac{4}{3}$. Multiplying by duty coefficients yields $\frac{1}{3\pi} \approx 0.1061$.

Final closed-form expression:

$$I_{T,rms}^2 = I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

### 3. Switching Loss Averaging Factors

Switching losses ($E_{on} + E_{off}$) occur at every PWM pulse and scale linearly with instantaneous current:

* **Per-Device Averaging Factor ($\frac{1}{\pi}$):** A transistor hard-switches during half of the fundamental period. The mathematical mean of $\sin(x)$ over a half-period is $\frac{2}{\pi} \approx 0.6366$. Combining the half-period switching window with this average yields the per-device factor $\frac{1}{\pi} \approx 0.3183$.
* **System Aggregate Factor ($\frac{6}{\pi}$):** In a 3-phase inverter, the six switches are phase-shifted by $60^\circ$ and do not switch at peak current simultaneously. Summing individual integrations yields the aggregate factor $\frac{6}{\pi} \approx 1.910$. Using a naive $6 \times \text{peak}$ calculation overestimates switching loss by a factor of $\frac{\pi}{2} \approx 1.57\times$.

---

## Step 5: Complete Inverter Loss Framework

Total heat generated per switch position in an inverter assembly is:

$$P_{switch} = P_{cond,T} + P_{sw,T} + P_{cond,D} + P_{rr,D}$$

### 1. Transistor Conduction Loss ($P_{cond,T}$)
$$P_{cond,T} = V_{CE0} \cdot I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right) + r_C \cdot I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

### 2. Transistor Switching Loss ($P_{sw,T}$)
$$P_{sw,T} = f_{sw} (E_{on} + E_{off}) \left( \frac{V_{dc}}{V_{ref}} \right) \left( \frac{I_{pk}}{I_{ref}} \right) \left( \frac{1}{\pi} \right)$$

### 3. Diode Conduction Loss ($P_{cond,D}$)
$$P_{cond,D} = V_{D0} \cdot I_{pk} \left( \frac{1}{2\pi} - \frac{m\cos\phi}{8} \right) + r_D \cdot I_{pk}^2 \left( \frac{1}{8} - \frac{m\cos\phi}{3\pi} \right)$$

### 4. Diode Reverse Recovery Loss ($P_{rr,D}$)
$$P_{rr,D} = f_{sw} \cdot E_{rec} \left( \frac{V_{dc}}{V_{ref}} \right) \left( \frac{I_{pk}}{I_{ref}} \right) \left( \frac{1}{\pi} \right)$$

---

## Technical Terminology Glossary

| Acronym / Term | Definition | Physical Significance |
| :--- | :--- | :--- |
| **[[IGBT]]** | Insulated Gate Bipolar Transistor | Hybrid switch combining MOSFET input characteristics with BJT high-current density. |
| **[[MOSFET]]** | Metal-Oxide-Semiconductor Field-Effect Transistor | Unipolar voltage-controlled switch with resistive $R_{DS(on)}$ on-state behavior. |
| **[[SiC]]** | Silicon Carbide | Wide-bandgap semiconductor offering high breakdown strength and minimal [[Reverse Recovery Charge]]. |
| **[[Field-Oriented Control]]** | Field-Oriented Control | Algorithm decoupling torque ($I_q$) and flux ($I_d$) control vectors in AC electric drives. |
| **[[Space-Vector Pulse Width Modulation]]** | Space-Vector Pulse Width Modulation | PWM generation technique maximizing DC-bus utilization and defining switch duty functions. |
| **[[PMSM]] / IPMSM** | Permanent Magnet Synchronous Motor | AC traction motor topology utilizing internal or surface magnets. |
| **[[Root Mean Square]]** | Root Mean Square | Effective thermal heating current value used for quadratic $I^2R$ calculations. |
| **[[Electro-Thermal Multiphysics]]** | Electro-Thermal Multiphysics | Iterative co-simulation linking electrical loss generation with thermal field solvers. |
| **[[CFD]]** | Computational Fluid Dynamics | Numerical fluid mechanics solver for predicting fluid flow and convective heat transfer coefficients. |
| **[[URANS]]** | Unsteady Reynolds-Averaged Navier-Stokes | Time-dependent turbulence model resolving large unsteady vortex dynamics. |
| **[[Large Eddy Simulation]]** | Large Eddy Simulation | High-fidelity CFD model directly resolving energy-carrying turbulent eddies. |
| **[[ANSYS Electronics Desktop]]** | Ansys Electronics Desktop | Integrated software environment running Maxwell electromagnetic and Icepak thermal solvers. |
| **[[Body of Influence]]** | Body of Influence | Localized geometric spatial mesh refinement volume used in [[CFD]] discretization. |

---

## Parameter Definitions

* **$V_{CE}$ ([[Collector-Emitter Voltage]]):** Total instantaneous voltage drop across the [[IGBT]] during conduction.
* **$V_{CE0}$ ([[Threshold Voltage]]):** Built-in potential voltage drop of the internal $P\text{-}N$ junction ($0.7\text{ V}$ to $1.0\text{ V}$).
* **$r_C$ ([[Slope Resistance]]):** Incremental series resistance of the conductivity-modulated drift region and channel.
* **$m$ ([[Modulation Index]]):** Peak phase voltage amplitude normalized to half the DC bus voltage ($0 \le m \le 1.0$).
* **$\cos\phi$ ([[Power Factor]]):** Displacement cosine of the phase angle between output voltage and current fundamental harmonics.
* **$E_{on}$ / $E_{off}$ ([[Switching Loss]] Energy):** Turn-on and turn-off energy dissipation per switching event ($\mu\text{J}$).
* **$V_{ref}$ / $I_{ref}$ (Reference Test Conditions):** Datasheet lab conditions at which switching energies were experimentally measured.
* **$V_{dc}$ (DC-Link Bus Voltage):** Operating voltage of the inverter DC energy storage bus.
* **$f_{sw}$ ([[Switching Frequency]]):** Pulse-width modulation carrier rate ($\text{Hz}$).
* **$Q_{rr}$ ([[Reverse Recovery Charge]]):** Stored minority charge swept from the antiparallel diode junction during turn-off.
* **$T_j$ ([[Junction Temperature]]):** Internal semiconductor die operating temperature ($^\circ\text{C}$).

---

## Atlas Connections

* [[Power Electronics]]
* [[Thermal Management]]
* [[Heat Transfer]]
* [[Motor Control]]