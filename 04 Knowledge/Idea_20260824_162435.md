---
type: engineering_note
domain: power_electronics
project: none
date: 2026-03-30
folder: 04 Knowledge
extracted_concepts:
  - SVPWM
  - IGBT
  - Diode
  - Conduction Loss
  - Switching Loss
  - Reverse Recovery Loss
  - Inverter Thermal Model
  - Duty Cycle
---

# Inverter Analytical Thermal Loss Model (SVPWM)

This note defines the mathematical framework for converting electrical driving parameters and semiconductor characteristics into heat load metrics for a 3-phase [[Inverter]] operating with [[SVPWM]] (Space Vector Pulse Width Modulation).

---

### Block 1: The Input Dashboard (Control Variables)

These parameters define operating conditions and semiconductor datasheet constants at elevated [[Junction Temperature]] ($T_j$).

* **Motor/Battery Demands:** 
  * Peak Current ($I_{pk}$)
  * DC Bus Voltage ($V_{dc}$)
  * [[Modulation Index]] ($m$)
  * [[Power Factor]] ($\cos\phi$)
    
* **Controller Settings:** 
  * [[Switching Frequency]] ($f_{sw}$)
    
* **Datasheet Constants (at Hot $T_j$):** 
  * [[IGBT]] threshold voltage ($V_{CE0}$)
  * [[IGBT]] bulk resistance ($r_C$)
  * [[Diode]] forward voltage ($V_{F0}$)
  * [[Diode]] bulk resistance ($r_D$)
  * Turn-on switching energy loss ($E_{on}$)
  * Turn-off switching energy loss ($E_{off}$)
  * Reverse recovery energy ($E_{rr}$) / charge ($Q_{rr}$)
  * Reference Voltage/Current ($V_{ref}$, $I_{ref}$)

---

### Block 2: The SVPWM Geometry Engine (Current Integrators)

This engine calculates average and RMS currents split between the [[IGBT]] and the freewheeling [[Diode]] based on the [[SVPWM]] [[Duty Cycle]].

* **Transistor ([[IGBT]]) Integrators:**
  * Average Current: 
    $$I_{T,avg} = I_{pk} \left( \frac{1}{2\pi} + \frac{m\cos\phi}{8} \right)$$
        
  * RMS Current Squared: 
    $$I_{T,rms}^2 = I_{pk}^2 \left( \frac{1}{8} + \frac{m\cos\phi}{3\pi} \right)$$
        
* **[[Diode]] Integrators:**
  * Average Current: 
    $$I_{D,avg} = I_{pk} \left( \frac{1}{2\pi} - \frac{m\cos\phi}{8} \right)$$
        
  * RMS Current Squared: 
    $$I_{D,rms}^2 = I_{pk}^2 \left( \frac{1}{8} - \frac{m\cos\phi}{3\pi} \right)$$

---

### Block 3: The Heat Generation Modules

Electrical parameters convert to heat ($W$) through conduction and switching mechanisms.

#### 3A: Transistor Conduction Loss
Combines knee voltage and slope resistance losses:
$$P_{cond,T} = (V_{CE0} \cdot I_{T,avg}) + (r_C \cdot I_{T,rms}^2)$$

#### 3B: Transistor Switching Loss
Scales turn-on and turn-off energy transients across operating voltage and current levels:
$$P_{sw,T} = f_{sw} \cdot (E_{on} + E_{off}) \cdot \left( \frac{V_{dc}}{V_{ref}} \right) \cdot \left( \frac{I_{pk}}{I_{ref}} \right) \cdot \left( \frac{1}{\pi} \right)$$

#### 3C: Diode Conduction Loss
$$P_{cond,D} = (V_{F0} \cdot I_{D,avg}) + (r_D \cdot I_{D,rms}^2)$$

#### 3D: Diode Reverse Recovery Loss
$$P_{rr,D} = f_{sw} \cdot E_{rr} \cdot \left( \frac{V_{dc}}{V_{ref}} \right) \cdot \left( \frac{1}{\pi} \right)$$

*(Note: Negligible ($0\text{ W}$) when utilizing [[Silicon Carbide]] / [[SiC]] MOSFET body diodes or Schottky barrier diodes).*

---

### Block 4: Total Thermal Output ($Q_{loss}$)

Combines loss terms per switch position and aggregates total dissipation across the multi-phase bridge for [[Heat Sink]] dimensioning.

* **Heat per Switch Position ([[IGBT]] + [[Diode]]):**
  $$P_{switch} = P_{cond,T} + P_{sw,T} + P_{cond,D} + P_{rr,D}$$
    
* **Total Inverter Heat (3-Phase, 6-Switch System):**
  $$Q_{Total} = 6 \cdot P_{switch}$$

---

## Atlas Connections
* [[Power Electronics]]
* [[Thermal Management]]
* [[Motor Control]]
* [[Heat Transfer]]