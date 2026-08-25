---
type: concept
domain: thermal
project: none
date: 2026-03-30
folder: 04 Knowledge
extracted_concepts:
  - Thermal Resistance
  - Thermal Interface Material
  - Thermal Conduction
  - Heatsink
  - Junction Temperature
  - IGBT
  - Thermal Spreading
  - Biot Number
  - Lumped Capacitance Model
---

# 1D Thermal Resistance Network and Transient Heat Equations

In thermal system design, heat flow through solid layers and fluid interfaces can be modeled analogously to an electrical circuit. Heat dissipation ($Q_{loss}$) acts as the current, while temperature differences ($\Delta T$) represent potential differences (voltage drops) across a network of [[Thermal Resistance]] elements.

---

## 1D Thermal Resistance Network Structure

For an [[IGBT]] power module mounted to an air-cooled [[Heatsink]], the equivalent thermal circuit path is expressed sequentially from junction to ambient:

$$T_j \xrightarrow{\;\;R_{JC}\;\;} T_c \xrightarrow{\;\;R_{TIM}\;\;} T_{base} \xrightarrow{\;\;R_{cond}\;\;} T_{fins} \xrightarrow{\;\;R_{conv}\;\;} T_\infty$$

### 1. Junction-to-Case Resistance ($R_{JC}$)
Internal conduction resistance within the semiconductor package (from silicon die through substrate solder to the copper baseplate). Supplied directly by component datasheets (e.g., $0.05\text{ }^\circ\text{C/W}$).

### 2. Case-to-Heatsink Resistance ($R_{TIM}$)
Thermal resistance across the [[Thermal Interface Material]] (TIM) applied between the module baseplate and the primary cooling structure. Modeled via 1D [[Thermal Conduction]]:

$$R_{TIM} = \frac{BLT}{k_{paste} \cdot A_{contact}}$$

Where $BLT$ is the [[Bond Line Thickness]], $k_{paste}$ is the thermal conductivity of the interface compound, and $A_{contact}$ is the contact surface area.

### 3. Heatsink Base Conduction Resistance ($R_{cond}$)
Conduction through the solid baseplate of the alloy [[Heatsink]] before distributing to extended surfaces:

$$R_{cond} = \frac{L_{base}}{k_{base} \cdot A_{base}}$$

Where $k_{base}$ is the material conductivity (e.g., $96\text{ W/m}\cdot\text{K}$ for ADC12 aluminum) and $L_{base}$ is baseplate thickness.

#### Baseplate Area & [[Thermal Spreading]]
The area parameter $A_{base}$ represents the planar surface perpendicular to heat flux:
* **Strict 1D Model (Conservative Bound):** Assumes heat travels in a straight column down from the chip footprint ($A_{base} = A_{contact}$). This yields a maximum conservative calculation for [[Thermal Resistance]].
* **3D Spreading Model ($A_{eff}$):** Accounts for lateral heat distribution through the baseplate (typically evaluated at a $45^\circ$ spreading angle):

$$A_{eff} \approx (W_{IGBT} + 2L_{base}) \times (L_{IGBT} + 2L_{base})$$

### 4. Extended Surface Convection Resistance ($R_{conv}$)
The resistance to external fluid dissipation across the fin array, incorporating [[Fin Efficiency]] ($\eta_f$) and total surface area ($A_{total}$):

$$R_{conv} = \frac{1}{\eta_0 \cdot h \cdot A_{total}}$$

$$\eta_0 = 1 - \frac{A_{fin}}{A_{total}}(1 - \eta_f)$$

### Total Equivalent System Resistance ($R_{tot}$)
Because the conduction and convection paths are aligned in series:

$$R_{tot} = R_{JC} + R_{TIM} + R_{cond} + R_{conv}$$

---

## Global Steady-State Thermal Model

Under continuous operating conditions, thermal energy storage within structural masses drops to zero ($dT/dt = 0$). Applying the steady-state thermal Ohm's law yields the equilibrium [[Junction Temperature]] ($T_j$):

$$T_j = T_\infty + Q_{loss} \cdot \left( R_{JC} + R_{TIM} + R_{cond} + R_{conv} \right)$$

To maintain semiconductor reliability, operational limits require $T_j \le T_{j,max}$ (typically $150^\circ\text{C}$).

---

## Global Transient Thermal Response

During transient power surges, thermal storage in low-mass components differs significantly from high-mass cooling structures:

1. **Fast-Response Domain (Silicon & TIM):** Microscopic mass yields negligible [[Thermal Mass]] ($C_{th} \approx 0$). These layers respond instantaneously to power dissipation changes:
   $$\Delta T_{fast} = Q_{loss} \cdot (R_{JC} + R_{TIM} + R_{cond})$$

2. **Slow-Response Domain (Bulk Heatsink):** Large structural mass produces a dominant thermal time constant ($\tau = R_{conv} C_{th}$). 

When the characteristic [[Biot Number]] is low ($Bi \ll 0.1$), internal thermal gradients inside the baseplate are negligible relative to surface convection. Applying a [[Lumped Capacitance Model]] yields the differential energy balance:

$$Q_{loss} - \frac{T_{hs} - T_\infty}{R_{conv}} = C_{th} \frac{dT_{hs}}{dt}$$

Integrating from initial thermal equilibrium ($T_{hs}(0) = T_\infty$) produces the temporal response of the [[Heatsink]]:

$$T_{hs}(t) = T_\infty + Q_{loss} \cdot R_{conv} \cdot \left( 1 - e^{-\frac{t}{R_{conv} C_{th}}} \right)$$

### Superposition for Total Transient Temperature

Combining the instantaneous jump across the low-mass semiconductor layers with the transient response of the primary bulk structure yields the complete governing equation for [[Junction Temperature]]:

$$T_j(t) = T_\infty + Q_{loss} \cdot (R_{JC} + R_{TIM} + R_{cond}) + Q_{loss} \cdot R_{conv} \cdot \left( 1 - e^{-\frac{t}{R_{conv} C_{th}}} \right)$$

---

## Atlas Connections
* [[Thermal Management]]
* [[Heat Transfer]]
* [[Power Electronics]]