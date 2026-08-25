---
type: engineering_note
domain: power_electronics
project: none
date: 2026-03-30
folder: "04 Knowledge"
---

# Inverter Semiconductor Electro-Thermal Loss Modelling

## Overview
This note details the electro-thermal loss formulation for traction inverter power switches ([[IGBT]] and [[SiC MOSFET]]) driven by [[Field-Oriented Control]] (FOC) using [[Space-Vector Pulse Width Modulation]] (SVPWM). It defines physical loss mechanisms, mathematical derivations for [[Conduction Loss]] and [[Switching Loss]], and temperature scaling parameters required for coupled [[Electro-Thermal Multiphysics]] (ETM) co-simulation.

---

## 1. Key Definitions & Terminology

| Acronym | Full Form | Physical Meaning & Role in Inverter Dynamics |
| :--- | :--- | :--- |
| **IGBT** | Insulated Gate Bipolar Transistor | Main semiconductor switch combining [[MOSFET]] gate control with BJT high-current density and low $V_{CE(sat)}$ drop. |
| **MOSFET** | Metal-Oxide-Semiconductor Field-Effect Transistor | Voltage-controlled switch. Behaves as a pure resistor ($R_{DS(on)}$) when on, eliminating the $P\text{-}N$ junction barrier potential tax. |
| **SiC** | [[Silicon Carbide]] | Wide-bandgap semiconductor material. [[SiC MOSFET]] devices feature near-zero [[Reverse Recovery Charge]] ($Q_{rr} \approx 0$) and lower switching losses than Si [[IGBT]]s. |
| **FOC** | [[Field-Oriented Control]] | Algorithm independently decoupling magnetic flux ($I_d$) and torque ($I_q$) vector components in AC motor drives. |
| **SVPWM** | [[Space-Vector Pulse Width Modulation]] | Vector switching scheme dictating phase duty cycle: $d(t) = \frac{1}{2}\left[1 + m\cos\phi\sin(\omega t)\right]$. |
| **PMSM / IPMSM** | Permanent Magnet Synchronous Motor | AC traction motor driven by the inverter power stage. |
| **RMS** | Root Mean Square | Effective thermal heating current: $I_{rms} = \sqrt{\frac{1}{T}\int_0^T i(t)^2 dt}$. |
| **ETM** | [[Electro-Thermal Multiphysics]] | Two-way coupled simulation (e.g., [[Ansys Maxwell]] to [[Ansys Icepak]]) mapping electrical loss to temperature and updating fluid/thermal properties. |

---

## 2. Parameter Breakdown & Physics

### On-State & Conduction Terms
*   **Collector-Emitter Voltage ($V_{CE}$):** Total voltage drop across the conducting [[IGBT]]. Formulated as:
    $$V_{CE}(i) = V_{CE0} + r_C \cdot i$$
*   **Threshold Voltage ($V_{CE0}$):** $P\text{-}N$ junction barrier potential ($\sim 0.7\text{ V} - 1.0\text{ V}$). Multiplied by **average current** ($I_{avg}$) due to linear integration across the half-cycle.
*   **Slope Resistance ($r_C$):** Bulk semiconductor ohmic resistance. Multiplied by **RMS current squared** ($I_{rms}^2$) due to quadratic $I^2R$ power loss dissipation.

### Motor Control Variables ([[SVPWM]] Integration)
*   **Modulation Index ($m$):** Scaled ratio ($0 \le m \le 1.0$) representing actual fundamental voltage output relative to available DC-link bus voltage.
*   **Displacement Power Factor ($\cos\phi$):** Cosine of the phase angle $\phi$ between stator voltage and [[Phase Current]]. Dictates mechanical vs. reactive magnetic energy transfer.
*   **Combined Factor ($m\cos\phi$):** Scales phase current integration over the [[SVPWM]] duty cycle equation, defining continuous conduction times between the active switch and freewheeling diode.

### Switching Energy & Voltage Scaling
*   **$E_{on}, E_{off}$ (Turn-On / Turn-Off Energy):** Transient energy loss ($\mu\text{J}$) per pulse caused by voltage and current overlap during switching transitions. $E_{off}$ is dominated by the [[IGBT]] tail current.
*   **Reference Conditions ($V_{ref}, I_{ref}$):** Lab test conditions specified in manufacturer datasheets.
*   **DC-Link Voltage ($V_{dc}$):** Actual operational DC busbar voltage.
*   **Scaling Factor:** Datasheet switching energies must be dynamically scaled to operating conditions:
    $$\text{Scaling Factor} = \left(\frac{V_{dc}}{V_{ref}}\right) \cdot \left(\frac{I_{pk}}{I_{ref}}\right)$$

### Thermal & Parasitic Losses
*   **Switching Frequency ($f_{sw}$):** Carrier frequency ($10\text{ kHz} - 20\text{ kHz}$). [[Switching Loss]] scales linearly with $f_{sw}$.
*   **Reverse Recovery Charge ($Q_{rr}$):** Charge trapped inside the antiparallel diode lattice prior to turn-off. Sweeping $Q_{rr}$ causes a localized current/power spike.
*   **Junction Temperature ($T_j$):** Silicon/SiC die operating temperature (max $\sim 150^\circ\text{C} - 175^\circ\text{C}$). Increased $T_j$ increases $r_C$ and $R_{DS(on)}$; losses must be calculated using hot-die datasheet curves.

---

## 3. Mathematical Governing Equations

Total power loss per switch position ($P_{switch}$) accounts for both the active transistor (T) and the antiparallel diode (D):

$$P_{switch} = P_{cond,T} + P_{sw,T} + P_{cond,D} + P_{rr,D}$$

```
+-------------------------------------------------------------------------+
|                        Switch Position Heat Dissipation                 |
|                                                                         |
|   +-------------------------------+   +-----------------------------+   |
|   |       Transistor (T)          |   |          Diode (D)          |   |
|   |  - Conduction: P_cond,T       |   |  - Conduction: P_cond,D     |   |
|   |  - Switching:  P_sw,T         |   |  - Rev Recovery: P_rr,D     |   |
|   +---------------+---------------+   +--------------+--------------+   |
|                   |                                  |                  |
|                   +------------------+---------------+                  |
|                                      |                                  |
|                                      v                                  |
|                           Total Heatsink Dissipation                    |
+-------------------------------------------------------------------------+
```

### 1. Transistor Conduction Loss ($P_{cond,T}$)
$$P_{cond,T} = V_{CE0} \cdot I_{T,avg} + r_C \cdot I_{T,rms}^2$$

Where current terms integrated over an [[SVPWM]] fundamental cycle are defined by:
$$I_{T,avg} = I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right)$$
$$I_{T,rms}^2 = I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$

### 2. Transistor Switching Loss ($P_{sw,T}$)
Averaging switching events over a sinusoidal AC fundamental half-cycle introduces a $\frac{1}{\pi}$ integration factor:

$$P_{sw,T} = f_{sw} \left(E_{on} + E_{off}\right) \cdot \left( \frac{V_{dc}}{V_{ref}} \right) \cdot \left( \frac{I_{pk}}{I_{ref}} \right) \cdot \left( \frac{1}{\pi} \right)$$

### 3. Antiparallel Diode Losses ($P_{cond,D}$ & $P_{rr,D}$)
Diode conduction losses use complementary duty cycles:
$$I_{D,avg} = I_{pk} \left( \frac{1}{2\pi} - \frac{m\cos\phi}{8} \right)$$

[[Reverse Recovery Charge]] loss component:
$$P_{rr,D} = \frac{1}{\pi} \cdot f_{sw} \cdot E_{rec} \cdot \left( \frac{V_{dc}}{V_{ref}} \right) \cdot \left( \frac{I_{pk}}{I_{ref}} \right)$$

---

## 4. Observations & Engineering Insights

*   **Duty Cycle Complementarity:** As [[Modulation Index]] ($m$) and [[Displacement Power Factor]] ($\cos\phi$) increase, conduction time shifts toward the transistor, lowering diode thermal stress while increasing transistor thermal load.
*   **Thermal Runaway Risk:** On-state resistance $r_C$ increases nonlinearly with [[Junction Temperature]] ($T_j$). Static room-temperature ($25^\circ\text{C}$) datasheet parameters underpredict inverter losses at maximum operating junction temperatures ($125^\circ\text{C} - 150^\circ\text{C}$) by up to $30\% - 40\%$, risking [[Thermal Runaway]].
*   **Si vs. SiC Trade-Off:** Switching to [[SiC MOSFET]] devices removes $V_{CE0}$ (eliminating the knee tax at light load) and virtually eliminates $P_{rr,D}$, enabling significantly higher switching frequencies ($f_{sw} > 40\text{ kHz}$) with reduced passive filtering requirements.

---

## 5. Action Items & Co-Simulation Next Steps

- [ ] Export phase current profiles from [[Motor Control]] simulations to benchmark FEA / [[Electro-Thermal Multiphysics]] loss calculations.
- [ ] Implement temperature-dependent lookup tables ($T_j \to r_C, E_{on}, E_{off}$) inside co-simulation scripts to prevent static parameter underestimation.
- [ ] Map computed dissipation maps directly into [[Ansys Icepak]] for thermal boundary layer evaluation.

---

## Atlas Connections
- [[Power Electronics MOC]]
- [[Thermal Management MOC]]
- [[Motor Control Systems]]
- [[Multiphysics Co-Simulation]]