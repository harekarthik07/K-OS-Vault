---
type: engineering_note
domain: power_electronics
project: none
date: 2026-03-31
folder: '04 Knowledge'
extracted_concepts:
  - Insulated-Gate Bipolar Transistor
  - Conductivity Modulation
  - Hard Switching
  - Space Vector Modulation
  - MOSFET
  - Bipolar Junction Transistor
  - Current Tail
  - Junction Temperature
  - Field-Oriented Control
  - Reverse Recovery Charge
  - Silicon Carbide
  - Root Mean Square
---

# IGBT Physics, Operation & Mathematical Modeling

This guide breaks down the physical architecture, solid-state physics, switching behavior, and mathematical modeling of an [[Insulated-Gate Bipolar Transistor]] (IGBT), connecting internal semiconductor dynamics to closed-form loss calculations under [[Space Vector Modulation]] (SVPWM).

---

## Roadmap & Learning Structure

1. **Semiconductor Physics & Internal Architecture:** Layer structure and [[Conductivity Modulation]].
2. **On-State Conduction & Mathematical Modeling:** Connecting solid-state physics to $V_{CE0} + r_C \cdot i$.
3. **Hard-Switching Dynamics & The Current Tail:** Physical origin of $E_{on}$, $E_{off}$, and recovery losses.
4. **SVPWM Waveform Integration:** Deriving closed-form average and [[Root Mean Square]] (RMS) geometric terms.

---

## Step 1: Semiconductor Physics & Internal Architecture

### 1. Device Definition

An [[Insulated-Gate Bipolar Transistor]] (IGBT) is a three-terminal power semiconductor device (Gate, Collector, Emitter) designed to combine the high input impedance and fast voltage-controlled gate of a power [[MOSFET]] with the high current density and low saturation voltage of a [[Bipolar Junction Transistor]] (BJT).

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

### 2. Layer Architecture & Physical Cross-Section

From top to bottom, a standard vertical N-channel IGBT consists of the following layers:

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
* **$P^+$ Collector Substrate:** The key feature distinguishing an IGBT from a power [[MOSFET]]. In a standard N-channel [[MOSFET]], this bottom layer is $N^+$. Replacing it with a $P^+$ layer forms an internal $P\text{-}N$ junction at the bottom.

### 3. Conduction Dynamics

#### MOS Channel Formation
When a positive gate-to-emitter voltage ($V_{GE} > V_{GE(th)}$, typically $+15\text{ V}$) is applied:
* The electric field across the oxide attracts electrons into the surface of the $P$-well.
* This creates a conductive inversion layer (N-channel) underneath the gate oxide, connecting the $N^+$ emitter to the $N^-$ drift region.
* Electrons start flowing from the emitter through this MOS channel into the $N^-$ drift region.

#### BJT Action & Minority Carrier Injection
* The flow of electrons into the $N^-$ drift region provides the base current for the wide-base $P\text{-}N\text{-}P$ bipolar structure ($P^+$ collector $\rightarrow$ $N^-$ drift $\rightarrow$ $P$-body).
* This forward-biases the bottom $P^+\text{/ }N^-$ junction.
* The $P^+$ substrate injects a massive stream of minority carriers (holes) into the $N^-$ drift region.

#### Conductivity Modulation
* The $N^-$ drift region is flooded simultaneously with electrons (from the MOS channel) and holes (from the $P^+$ collector), forming a dense electron-hole plasma.
* [[Conductivity Modulation]] reduces the effective electrical resistivity of the thick $N^-$ drift layer by several orders of magnitude compared to an unmodulated drift region.
* This allows an IGBT to block high voltages ($600\text{ V}$ to $6.5\text{ kV}$) while maintaining a low on-state voltage drop at hundreds of amperes.

---

## Step 2: Physical Origin of Conduction Loss Equations

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

The IGBT on-state voltage drop is modeled as:

$$V_{CE}(i) = V_{CE0} + r_C \cdot i$$

This reflects two internal physical mechanisms:
1. **The Knee / Threshold Voltage ($V_{CE0}$):** Sourced directly from the forward voltage drop of the bottom $P^+\text{-}N$ junction ($P^+$ collector to $N^-$ drift). Even at near-zero current, this junction creates a voltage barrier of approximately $0.7\text{ V}$ to $1.0\text{ V}$.
2. **The Slope Resistance ($r_C$):** Represents the remaining series resistance across the conductivity-modulated drift layer, the MOS inversion channel, and the bulk metallization/bond wires.

### 2. Time-Averaged Conduction Loss Integration

$$P_{cond,T} = V_{CE0} \cdot I_{T,avg} + r_C \cdot I_{T,rms}^2$$

```
Instantaneous Power:  p(t) = v_CE(t) · i(t) = [V_CE0 + r_C · i(t)] · i(t)
                           = V_CE0 · i(t) + r_C · [i(t)]²

Time-Averaged Power:  P_cond,T = V_CE0 · (Average of i(t)) + r_C · (Average of [i(t)]²)
                              = V_CE0 · I_T,avg + r_C · I_T,rms²
```

* **The Threshold Term ($V_{CE0} \cdot I_{T,avg}$):** Linear with respect to current, integrating to the average current $I_{T,avg}$.
* **The Resistive Term ($r_C \cdot I_{T,rms}^2$):** Quadratic with respect to current, integrating to the mean of the current squared ($I_{T,rms}^2$).

> **Comparison vs. [[Silicon Carbide]] (SiC) MOSFETs:** A [[MOSFET]] has no internal $P\text{-}N$ junction in its main forward conduction path; it behaves as a pure resistor $R_{DS(on)}$. Consequently, [[MOSFET]] conduction loss scales purely with $I_{rms}^2$. At low currents (light vehicle loads), the IGBT continuously pays the $V_{CE0} \cdot I$ threshold penalty, making [[Silicon Carbide]] MOSFETs more efficient under light-load driving cycles.

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

### 1. Turn-On Dynamics ($E_{on}$)
During [[Hard Switching]] turn-on:
* When $V_{GE} > V_{GE(th)}$, current rises rapidly ($dI_C/dt$) through the MOS channel.
* While current is rising to its peak, the voltage across the device ($V_{CE}$) is still clamped to the DC bus voltage by the inductive load.
* The simultaneous presence of high $V_{CE}$ and high $I_C$ generates turn-on energy loss $E_{on}$.

### 2. Turn-Off Dynamics ($E_{off}$) and the Current Tail
* When $V_{GE}$ drops to $0\text{ V}$ or $-8\text{ V}$, the MOS inversion channel closes almost immediately, stopping electron injection.
* However, the $N^-$ drift region remains flooded with stored minority carriers (holes).
* Because the external circuit cannot extract these holes rapidly through the non-conducting top channel, they must either be swept out by the expanding depletion region electric field or decay via natural carrier recombination.
* This produces a prolonged current decay known as the **[[Current Tail]]**.
* Because $V_{CE}$ has already recovered to the full DC bus voltage ($V_{dc}$) while this tail current continues to flow, the power product $V_{CE} \cdot I_{tail}$ dissipates substantial turn-off switching energy ($E_{off}$).

### Comparative Summary: IGBT vs. SiC MOSFET

| Parameter / Feature | Silicon IGBT | SiC [[MOSFET]] | Engineering Significance |
| :--- | :--- | :--- | :--- |
| **Conduction Mechanism** | Bipolar (Electrons + Holes) with [[Conductivity Modulation]] | Unipolar (Majority Carrier Electrons only) | IGBT achieves high current density at high voltage; SiC has no $P\text{-}N$ forward knee. |
| **On-State Characteristic** | Knee + Slope: $V_{CE0} + r_C \cdot i$ | Purely Resistive: $R_{DS(on)} \cdot i$ | SiC is much more efficient at light/partial loads. |
| **Turn-Off Tail Current** | Yes (Minority carrier recombination) | No (Pure majority carrier device) | SiC achieves lower $E_{off}$, enabling higher switching frequencies ($f_{sw}$). |
| **Freewheeling Path** | Requires separate antiparallel diode | Body diode / Synchronous channel rectification | IGBT inverter modules require copackaged Si/SiC diodes. |

---

## Step 4: SVPWM Integrals & Analytical Averaging

To calculate inverter losses without dynamic transient thermal co-simulations, closed-form mathematical integrals average the switching and conduction behavior over one fundamental electrical output period.

### 1. Core Functions
Under [[Field-Oriented Control]] and [[Space Vector Modulation]] (SVPWM):
* **Phase Current:** $i(t) = I_{pk}\sin(\omega t)$
* **SVPWM Duty Function:** $d(t) = \frac{1}{2}[1 + m\cos\phi\sin(\omega t)]$

### 2. Conduction Loss Derivations

#### A. Average Current Integral (Threshold Voltage Term)
To calculate $I_{T,avg}$ for the $V_{CE0}$ threshold term:

$$I_{T,avg} = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}\sin(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding the integral:
1. **$\frac{1}{2\pi}$ Baseline:** Integrating $\frac{1}{2}\sin(x)$ yields $\frac{1}{2\pi} \approx 0.1592$.
2. **$\frac{1}{8}$ Modulation Term:** Integrating $\frac{1}{2}\sin^2(x)$ yields the $\frac{m\cos\phi}{8}$ term.

$$I_{T,avg} = I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right)$$

#### B. RMS Current Squared Integral (Resistive Term)
To calculate $I_{T,rms}^2$ for the slope resistance $r_C$ or [[MOSFET]] $R_{DS(on)}$:

$$I_{T,rms}^2 = \frac{1}{2\pi} \int_{0}^{\pi} I_{pk}^2\sin^2(x) \cdot \frac{1}{2}[1 + m\cos\phi\sin(x)] \,dx$$

Expanding the integral:
1. **$\frac{1}{8}$ Term:** Derived from integrating $\frac{1}{2}\sin^2(x)$ over a half-cycle.
2. **$\frac{1}{3\pi}$ Term:** The geometric integral $\int_0^\pi \sin^3(x)\,dx = \frac{4}{3}$. Multiplying by duty coefficients yields $\frac{1}{3\pi} \approx 0.1061$.

$$I_{T,rms}^2 = I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

### 3. Switching Loss Averaging Factors

Switching losses ($E_{on} + E_{off}$) occur at every PWM pulse and scale linearly with instantaneous current:
* **Per-Device Factor ($\frac{1}{\pi}$):** A switch hard-switches during half of the fundamental period. The mean of $\sin(x)$ over $[0, \pi]$ is $\frac{2}{\pi}$. Combining the duty window gives $\frac{1}{\pi} \approx 0.3183$.
* **System Aggregate Factor ($\frac{6}{\pi}$):** Summing all six switches in a three-phase bridge (staggered by $60^\circ$) yields an aggregate scaling factor of $\frac{6}{\pi} \approx 1.910$. Using a naive $6 \times \text{peak}$ calculation overestimates total inverter switching loss by $\frac{\pi}{2} \approx 1.57\times$.

---

## Technical Loss Equations & Definitions

### 1. Four-Part Switch Power Loss
Total heat dissipation per switch position:

$$P_{switch} = P_{cond,T} + P_{sw,T} + P_{cond,D} + P_{rr,D}$$

#### Transistor Conduction Loss
$$P_{cond,T} = V_{CE0} \cdot I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right) + r_C \cdot I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

#### Transistor Switching Loss
$$P_{sw,T} = f_{sw} (E_{on} + E_{off}) \left( \frac{V_{dc}}{V_{ref}} \right) \left( \frac{I_{pk}}{I_{ref}} \right) \left( \frac{1}{\pi} \right)$$

#### Diode Conduction Loss
$$P_{cond,D} = V_{D0} \cdot I_{pk} \left( \frac{1}{2\pi} - \frac{m\cos\phi}{8} \right) + r_D \cdot I_{pk}^2 \left( \frac{1}{8} - \frac{m\cos\phi}{3\pi} \right)$$

#### Diode Reverse Recovery Loss
$$P_{rr,D} = f_{sw} \cdot E_{rec} \left( \frac{V_{dc}}{V_{ref}} \right) \left( \frac{I_{pk}}{I_{ref}} \right) \left( \frac{1}{\pi} \right)$$

---

## Master Engineering Glossary

| Term / Acronym | Definition | Physical Role |
| :--- | :--- | :--- |
| **[[Insulated-Gate Bipolar Transistor]]** | Hybrid semiconductor switch | Combines MOS gate input with bipolar main conduction path. |
| **[[MOSFET]]** | Field-effect transistor | Unipolar majority carrier switch; purely resistive $R_{DS(on)}$ channel. |
| **[[Silicon Carbide]]** | Wide-bandgap material | Enables high temperature rating, zero [[Reverse Recovery Charge]], and fast switching. |
| **[[Field-Oriented Control]]** | Vector drive algorithm | Controls $d$-axis (flux) and $q$-axis (torque) currents independently. |
| **[[Space Vector Modulation]]** | Advanced PWM technique | Maximizes DC bus utilization and dictates semiconductor duty ratio $d(t)$. |
| **[[Conductivity Modulation]]** | Carrier flooding effect | Floods $N^-$ drift region with minority carriers, dropping on-state resistance. |
| **[[Hard Switching]]** | Forced turn-on/off | Switching across non-zero voltage/current, dissipating $E_{on}$ and $E_{off}$. |
| **[[Current Tail]]** | Turn-off decay phenomenon | Stored minority carrier recombination during IGBT turn-off. |
| **[[Reverse Recovery Charge]] ($Q_{rr}$)** | Diode stored charge | Charge swept out during diode turn-off, generating $P_{rr,D}$ heat spikes. |
| **[[Junction Temperature]] ($T_j$)** | Silicon die temperature | Dictates internal resistance; higher $T_j$ increases $r_C$ and switching energy. |
| **[[Root Mean Square]] (RMS)** | Effective AC heating value | Quadrature current integration used for resistive $I^2R$ loss modeling. |
| **ETM** | Electro-Thermal Multiphysics | Coupled electromagnetic-thermal co-simulation framework (e.g., [[Ansys Electronics Desktop]]). |
| **[[Computational Fluid Dynamics]]** | Fluid flow solver | Numerical solver (e.g., URANS, LES) for cooling performance analysis. |

---

## Atlas Connections

* [[Power Electronics]]
* [[Thermal Management]]
* [[Motor Control]]
* [[Semiconductor Physics]]