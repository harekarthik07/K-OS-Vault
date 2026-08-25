---
type: engineering_note
domain: thermal
project: none
date: 2026-08-18
folder: 04 Knowledge
extracted_concepts:
  - Del Operator
  - Temperature Gradient
  - Divergence
  - Transient Heat Equation
  - Fourier's Law
  - Laplace Operator
  - Thermal Resistance
  - Thermal Capacitance
  - Biot Number
  - Lumped Capacitance Model
  - Thermal Time Constant
  - Newton's Law of Cooling
  - Reynolds Number
  - Prandtl Number
  - Nusselt Number
  - Grashof Number
  - Rayleigh Number
  - Fin Efficiency
  - Fin Effectiveness
---

# Foundations of Conduction, Convection, and Thermal Field Theory

---

## 1. The Del Operator ($\nabla$) and Vector Calculus in Heat Transfer

The symbol $\nabla$ (pronounced "Nabla" or "Del") is a [[Vector Differential Operator]]. By itself, it is an operator that acts upon scalar fields (like a 3D temperature distribution) or vector fields (like heat flux).

In Cartesian coordinates ($x, y, z$), the [[Del Operator]] is defined as:

$$\nabla = \hat{i} \frac{\partial}{\partial x} + \hat{j} \frac{\partial}{\partial y} + \hat{k} \frac{\partial}{\partial z}$$

### The Gradient ($\nabla T$) — Scalar to Vector

When applied directly to a scalar [[Temperature Gradient]] field $T(x,y,z)$, it computes the spatial gradient vector:

$$\nabla T = \hat{i} \frac{\partial T}{\partial x} + \hat{j} \frac{\partial T}{\partial y} + \hat{k} \frac{\partial T}{\partial z}$$

* **Physical Meaning:** The gradient creates a vector pointing in the direction of the *steepest temperature increase*. [[Fourier's Law]] ($\mathbf{q}^{\prime\prime} = -k \nabla T$) includes a negative sign because [[Heat Flux]] moves in the direction of steepest temperature drop.

### The Divergence ($\nabla \cdot \mathbf{q}^{\prime\prime}$) — Vector to Scalar

Taking the dot product of the [[Del Operator]] with a vector field such as [[Heat Flux]] ($\mathbf{q}^{\prime\prime}$) yields the [[Divergence]]:

$$\nabla \cdot \mathbf{q}^{\prime\prime} = \frac{\partial q_x}{\partial x} + \frac{\partial q_y}{\partial y} + \frac{\partial q_z}{\partial z}$$

* **Physical Meaning:** [[Divergence]] measures the net spatial volumetric outflow of heat per unit volume from a differential point.
  * If $\nabla \cdot \mathbf{q}^{\prime\prime} > 0$, net thermal energy is leaving the point.
  * If $\nabla \cdot \mathbf{q}^{\prime\prime} < 0$, thermal energy is accumulating at the point.

---

## 2. Derivation of the 3D Transient Heat Equation

The governing [[Partial Differential Equation]] (PDE) for transient conduction is derived from the [[First Law of Thermodynamics]] applied to a microscopic, 3D cubic control volume ($dx \cdot dy \cdot dz$).

$$\text{Rate of Energy In} - \text{Rate of Energy Out} + \text{Rate of Energy Generated} = \text{Rate of Energy Stored}$$

### Step-by-Step Terms:

1. **Internal Generation Term:**
   Volumetric heat generation density rate $Q_v$ ($\text{W/m}^3$), such as [[Joule Heating]] inside an [[IGBT]] silicon die or busbar.

2. **Transient Energy Storage Term:**
   Governed by density ($\rho$) and [[Specific Heat Capacity]] ($c_p$):
   $$\text{Rate of Storage} = \rho c_p \frac{\partial T}{\partial t}$$

3. **Net Conduction Rate Term:**
   Net heat accumulation due to spatial conduction across boundaries is given by the negative divergence of the flux vector:
   $$\text{Net Heat Conduction} = -\nabla \cdot \mathbf{q}^{\prime\prime}$$

4. **Combined Energy Balance Equation:**
   $$-\nabla \cdot \mathbf{q}^{\prime\prime} + Q_v = \rho c_p \frac{\partial T}{\partial t}$$

Substituting [[Fourier's Law]] ($\mathbf{q}^{\prime\prime} = -k \nabla T$):

$$-\nabla \cdot (-k \nabla T) + Q_v = \rho c_p \frac{\partial T}{\partial t}$$

Canceling the double negative yields the general **3D Transient Heat Conduction Equation**:

$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + Q_v$$

This PDE forms the mathematical foundation for finite element solvers such as [[Ansys Icepak]] and general thermal [[FEA]] / [[CFD]] codes.

---

## 3. The Laplace Operator ($\nabla^2$) and Physical Diffusion

When isotropic thermal conductivity is constant throughout space ($k = \text{constant}$), $k$ pulls out of the differential operator:

$$\nabla \cdot (k \nabla T) = k (\nabla \cdot \nabla T)$$

Expanding the dot product yields the second-order spatial derivatives:

$$\nabla \cdot \nabla T = \left( \hat{i}\frac{\partial}{\partial x} + \hat{j}\frac{\partial}{\partial y} + \hat{k}\frac{\partial}{\partial z} \right) \cdot \left( \hat{i}\frac{\partial T}{\partial x} + \hat{j}\frac{\partial T}{\partial y} + \hat{k}\frac{\partial T}{\partial z} \right) = \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2}$$

This sum is defined as the **[[Laplace Operator]] ($\nabla^2$)**:

$$k \nabla^2 T = k \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2} \right)$$

### Physical Interpretation of the Laplacian

* **First Derivative ($\nabla T$):** Represents local slope (direction and magnitude of maximum variation).
* **Second Derivative ($\nabla^2 T$):** Represents spatial curvature or concavity, comparing local point temperature against the immediate spatial neighborhood average.

#### The Local Average Rule:
* $\nabla^2 T > 0$: Point temperature is *lower* than neighboring average; heat flows *into* the point.
* $\nabla^2 T < 0$: Point temperature is *higher* than neighboring average; heat flows *out* of the point.
* $\nabla^2 T = 0$: Point temperature equals neighboring average; steady spatial distribution without local accumulation.

In unheated conditions ($Q_v = 0$), the transient thermal response simplifies to pure thermal diffusion:

$$\rho c_p \frac{\partial T}{\partial t} = k \nabla^2 T$$

---

## 4. 1D Reduction & Thermal Resistance Analogy

### 3D to 1D Mathematical Collapse
Starting from the 3D differential transient equation:

$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + Q_v$$

Applying three physical assumptions:
1. **Steady-State Condition:** $\frac{\partial T}{\partial t} = 0$.
2. **Zero Internal Generation in Solid Domain:** $Q_v = 0$.
3. **1D Unidirectional Heat Flow ($x$-direction):** $\frac{\partial T}{\partial y} = \frac{\partial T}{\partial z} = 0$.

The 3D PDE collapses to an [[Ordinary Differential Equation]] (ODE):

$$\frac{d}{dx} \left( k \frac{dT}{dx} \right) = 0$$

Integrating with respect to $x$:

$$k \frac{dT}{dx} = C_1 \quad \implies \quad q_x = -k \frac{dT}{dx} = \text{constant}$$

To express this in total heat power $Q$ ($\text{W}$) across cross-sectional area $A$:

$$Q = -k A \frac{dT}{dx}$$

Integrating across a wall thickness $L$ from $T_{hot}$ at $x=0$ to $T_{cold}$ at $x=L$:

$$Q \int_{0}^{L} dx = -k A \int_{T_{hot}}^{T_{cold}} dT \quad \implies \quad Q \cdot L = k A (T_{hot} - T_{cold})$$

Rearranging into structural form analogous to Ohm's Law ($I = \frac{\Delta V}{R}$):

$$Q = \frac{\Delta T}{\left( \frac{L}{k A} \right)}$$

Where the denominator defines **[[Thermal Resistance]] ($R_\theta$)**:

$$R_{\theta} = \frac{L}{k A} \quad \left[\frac{^\circ\text{C}}{\text{W}}\right]$$

### Thermal Mass & Capacitance Calculation
Transient thermal energy absorption depends on [[Thermal Capacitance]] ($C_{th}$):

$$C_{th} = m \cdot c_p = \rho \cdot V \cdot c_p \quad \left[\frac{\text{J}}{\text{K}}\right]$$

*Example Calculation (ADC12 Baseplate Segment):*
* Material Properties: ADC12 Die-Cast Aluminum ($\rho = 2740\text{ kg/m}^3$, $c_p = 963\text{ J/kg}\cdot\text{K}$, $k = 96\text{ W/m}\cdot\text{K}$).
* Volume: $A = 0.01\text{ m}^2$, Thickness $L = 0.005\text{ m} \implies V = 0.00005\text{ m}^3$.
* Mass: $m = 2740 \cdot 0.00005 = 0.137\text{ kg}$.
* Thermal Capacitance: $C_{th} = 0.137 \cdot 963 \approx 132\text{ J/}^\circ\text{C}$.

---

## 5. The Biot Number ($Bi$) & Lumped Capacitance Criterion

The [[Biot Number]] ($Bi$) is a dimensionless ratio comparing internal conduction resistance within a solid to external boundary convection resistance:

$$Bi = \frac{h L_c}{k} = \frac{R_{cond}}{R_{conv}}$$

Where:
* $h$ = [[Convection Heat Transfer Coefficient]] ($\text{W/m}^2\cdot\text{K}$)
* $L_c$ = Characteristic Length ($V / A_s$)
* $k$ = Thermal conductivity of the solid ($\text{W/m}\cdot\text{K}$)

```
   Bi << 0.1 (Lumped Mass)           Bi = 1 (Intermediate)            Bi >> 1 (Spatial Gradients)
      +---------------+              +---------------+              +---------------+
      | T1          T1|              | T1          T2|              | T_core   T_surf|
      |               |              |   \        /  |              |   |        |  |
      | T1          T1|              |    T_avg  /   |              |   |_______/   |
      +---------------+              +---------------+              +---------------+
     Flat temp profile               Moderate curvature             Steep temp profile
```

![[Pasted image 20260818165811.png]]

### The Lumped Mass Criterion ($Bi \ll 0.1$)
* **$Bi \ll 0.1$:** Internal conduction resistance is negligible relative to external surface convection. Thermal diffusion inside the body occurs significantly faster than heat rejection to the environment. Spatial temperature gradients inside the solid vanish ($\nabla T \approx 0$). The domain collapses from a 3D PDE to a 0D transient [[Lumped Capacitance Model]].
* **$Bi \gg 0.1$:** Convection dominates heat removal while conduction inside the solid is slow. Large internal thermal gradients form. 3D transient conduction analysis via [[Ansys Icepak]] or explicit [[FEA]] is required.

---

## 6. Transient Dynamics & Thermal Time Constant ($\tau$)

For systems satisfying $Bi \ll 0.1$, the global 0D transient energy balance is:

$$Q_{in} - h A (T(t) - T_{\infty}) = \rho V c_p \frac{dT}{dt}$$

Solving this 1st-order linear ODE yields the exponential thermal step-response:

$$T(t) = T_{\infty} + \frac{Q_{in}}{hA} + \left( T_i - T_{\infty} - \frac{Q_{in}}{hA} \right) e^{-t/\tau}$$

Where **[[Thermal Time Constant]] ($\tau$)** is defined as:

$$\tau = R_{conv} \cdot C_{th} = \left( \frac{1}{hA} \right) (\rho V c_p) = \frac{\rho V c_p}{hA} \quad [\text{seconds}]$$

### Time-Domain Characteristics:
* $t = 1\tau$: System completes **63.2%** of full transient thermal transition.
* $t = 3\tau$: System reaches **95.0%** of steady-state value.
* $t = 5\tau$: System reaches **99.3%** (deemed practical steady-state).

```
   Temp (T)
     ^
     |                                    ...--- Steady State (100%)
     |                             ...--'' | (95% at 3τ)
     |                      ...--''        |
     |               ...--''               |
     |        ...--'' (63.2% at 1τ)        |
     | ..--''                              |
     +----------------------------------------------------> Time (t)
     0               1τ                   3τ          5τ
```

### Engineering Trade-Off Analysis:

| Parametric Configuration | Thermal Mass ($C_{th}$) | Convection Resistance ($R_{conv}$) | Time Constant ($\tau$) | Transient Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **High Baseplate Mass / Low Airflow** | Large | High | Large (e.g., $120\text{ s}$) | Slow temperature rise under transient pulse load; slow cooling recovery. |
| **Thin Baseplate / High Airflow** | Small | Low | Small (e.g., $5\text{ s}$) | Rapid temperature rise under power spikes; near-instant cooling when load drops. |

---

## 7. Forced Convection Mechanics & Fan Dynamics

Heat transfer between a solid surface and a surrounding fluid is governed by [[Newton's Law of Cooling]]:

$$Q_{out} = h A (T_s - T_{\infty}) = \frac{T_s - T_{\infty}}{R_{conv}}$$

Where the external [[Convection Heat Transfer Coefficient]] resistance is:

$$R_{conv} = \frac{1}{h A}$$

### Determination of $h$ via Non-Dimensional Fluid Mechanics

The convective heat transfer coefficient $h$ is a flow field property calculated using three primary dimensionless parameters:

#### 1. Reynolds Number ($Re$)
Ratio of inertial forces to viscous forces:

$$Re = \frac{\rho_{air} V L_c}{\mu_{air}} = \frac{V L_c}{\nu_{air}}$$

#### 2. Prandtl Number ($Pr$)
Ratio of momentum diffusivity to thermal diffusivity:

$$Pr = \frac{\nu_{air}}{\alpha_{air}} \approx 0.71 \quad \text{(for air at standard conditions)}$$

#### 3. Nusselt Number ($Nu$)
Ratio of convective to pure conductive heat transfer across the fluid boundary layer:

$$Nu = \frac{h L_c}{k_{fluid}}$$

For forced laminar flow over flat plates/fins:

$$Nu = 0.664 \cdot Re^{1/2} \cdot Pr^{1/3}$$

Solving for $h$:

$$h = \frac{Nu \cdot k_{air}}{L_c}$$

*(Note: $k_{air} \approx 0.026\text{ W/m}\cdot\text{K}$, distinct from solid aluminum thermal conductivity $k_{sol}$).*

### Thermodynamic Limit via Mass Flow Rate ($\dot{m}$)
Convective removal capacity is globally bounded by fluid enthalpy transport capabilities based on the mass flow rate ($\dot{m}$):

$$Q = \dot{m} \cdot c_{p,air} \cdot \Delta T_{air}$$

If volumetric flow rate (CFM) is insufficient, air becomes thermally saturated down-channel ($\Delta T_{air}$ increases excessively), degrading cooling performance at downstream fins.

---

## 8. Natural & Mixed Convection Regimes

Convection dynamics depend on whether movement is driven by external pressure gradients or temperature-induced buoyancy forces:

1. **Forced Convection:** External pressure gradient forces flow ($Re$ dominates).
2. **Natural Convection:** Fluid density variations driven by gravity ($g$) generate buoyancy forces.
3. **Mixed Convection:** Forced and natural convection operate simultaneously.
   * Criterion: Evaluate $\frac{Gr}{Re^2}$.
   * $\frac{Gr}{Re^2} \ll 1 \implies$ Pure forced convection.
   * $\frac{Gr}{Re^2} \gg 1 \implies$ Pure natural convection.
   * $\frac{Gr}{Re^2} \approx 1 \implies$ Mixed convection regime.

### The Grashof Number ($Gr$) & Rayleigh Number ($Ra$)
Buoyancy strength is quantified by the [[Grashof Number]]:

$$Gr = \frac{g \beta (T_s - T_\infty) L_c^3}{\nu^2}$$

Where $\beta = \frac{1}{T_\infty}$ (for ideal gas absolute ambient temperature in Kelvin).

Combining $Gr$ with $Pr$ yields the [[Rayleigh Number]]:

$$Ra = Gr \cdot Pr = \frac{g \beta (T_s - T_\infty) L_c^3}{\nu \alpha}$$

* $Ra < 10^9$: Laminar free convection boundary layer.
* $Ra > 10^9$: Turbulent free convection boundary layer.

### Nusselt Number Correlations ($Nu$) Summary

| Flow Regime | System Geometry | Nusselt Correlation Formula |
| :--- | :--- | :--- |
| **Forced Laminar** | Flat Plate / Fin surface | $Nu = 0.664 \, Re^{1/2} \, Pr^{1/3}$ |
| **Forced Turbulent** | Flat Plate / Fin surface | $Nu = 0.037 \, Re^{4/5} \, Pr^{1/3}$ |
| **Natural Laminar** | Vertical Plate | $Nu = C \cdot Ra^{1/4}$ |
| **Natural Turbulent** | Vertical Plate | $Nu = C \cdot Ra^{1/3}$ |
| **Cross-Flow (Cylinder)** | Pipe / Bluff Body | Churchill-Bernstein Equation: <br> $Nu = 0.3 + \frac{0.62 Re^{1/2} Pr^{1/3}}{\left[ 1 + (0.4/Pr)^{2/3} \right]^{1/4}} \left[ 1 + \left( \frac{Re}{282000} \right)^{5/8} \right]^{4/5}$ |

---

## 9. Fin Physics, Efficiency, and Effectiveness

### The General Fin Differential Equation
Analyzing a 1D differential element of a extended surface fin ($dx$) yields the energy balance:

$$\frac{d^2\theta}{dx^2} - \left(\frac{h P}{k A_c}\right) \theta = 0$$

Where:
* $\theta(x) = T(x) - T_\infty$ (Temperature excess relative to ambient)
* $P$ = Perimeter of fin cross-section
* $A_c$ = Cross-sectional area of fin
* $k$ = Thermal conductivity of fin material

Defining the **Fin Parameter ($m$)**:

$$m = \sqrt{\frac{h P}{k A_c}} \quad [\text{m}^{-1}]$$

Rewriting the general governing ODE:

$$\frac{d^2\theta}{dx^2} - m^2 \theta = 0$$

### Fin Efficiency ($\eta_f$)
Defined as the ratio of actual fin heat transfer rate to ideal heat transfer rate if the entire fin were maintained at the base temperature ($T_b$):

$$\eta_f = \frac{Q_{fin}}{Q_{ideal}} = \frac{\tanh(m L_c)}{m L_c}$$

*(Assuming an adiabatic fin tip).*

```
   Efficiency (η_f)
    1.0 |-------\
        |        \
        |         \
        |          \
        |           '---...
      0 +------------------------> Fin Length parameter (mL)
```

* **Engineering Implications for Lower Conductivity Alloys (e.g., ADC12, $k=96\text{ W/m}\cdot\text{K}$):**
  Larger $m$ values reduce $\eta_f$ rapidly as length $L$ increases. Shorter, thicker fins yield higher overall efficiency than tall, thin profile extensions in cast alloys.

### Fin Effectiveness ($\epsilon_f$)
Assesses performance benefit of adding an extended surface relative to an un-finned base surface area ($A_c$):

$$\epsilon_f = \frac{Q_{fin}}{h A_c (T_b - T_\infty)} = \sqrt{\frac{k P}{h A_c}}$$

* $\epsilon_f < 2$: Fin acts as a thermal barrier/insulator (restricting airflow while adding resistance).
* $\epsilon_f \ge 2$: Fin enhances overall thermal dissipation.
* High effectiveness is maximized by high thermal conductivity $k$, high perimeter-to-area ratio $P/A_c$, and low surface convective coefficient environments (e.g., natural/forced air cooling vs. high-$h$ liquid cooling).

---

## Atlas Connections

* [[Thermal Management]]
* [[Heat Transfer]]
* [[Fluid Mechanics]]
* [[Power Electronics]]