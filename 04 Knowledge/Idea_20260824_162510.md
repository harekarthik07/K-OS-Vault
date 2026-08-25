---
type: engineering_note
domain: thermal
project: none
date: 2026-08-18
folder: "04 Knowledge"
extracted_concepts:
  - Del Operator
  - Transient Heat Equation
  - Fourier's Law
  - Gradient
  - Divergence
  - Laplacian Operator
  - Thermal Resistance
  - Lumped Mass Model
  - Biot Number
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

# Derivation of the Transient Heat Equation, Lumped Mass Systems, and Convection Dynamics

## Module 2.1: The Mathematics of the Del Operator ($\nabla$)

The symbol $\nabla$ (pronounced "Nabla" or "Del") is a [[Vector Differential Operator]]. By itself, it acts as an operator machine that computes spatial variations over a three-dimensional field (such as a temperature field or a [[Heat Flux]] vector).

In [[Cartesian Coordinates]] ($x, y, z$), the [[Del Operator]] is defined as:

$$\nabla = \hat{i} \frac{\partial}{\partial x} + \hat{j} \frac{\partial}{\partial y} + \hat{k} \frac{\partial}{\partial z}$$

### 1. The Gradient ($\nabla T$) — Scalar to Vector

Temperature ($T$) is a scalar quantity. Applying the [[Del Operator]] directly to $T$ computes the [[Gradient]]:

$$\nabla T = \hat{i} \frac{\partial T}{\partial x} + \hat{j} \frac{\partial T}{\partial y} + \hat{k} \frac{\partial T}{\partial z}$$

* **Physical Meaning:** The gradient converts a scalar temperature field into a vector pointing in the direction of the steepest temperature increase. [[Fourier's Law]] ($\mathbf{q}^{\prime\prime} = -k \nabla T$) incorporates a negative sign because [[Heat Flux]] flows in the opposite direction (down the steepest temperature slope).

### 2. The Divergence ($\nabla \cdot \mathbf{q}^{\prime\prime}$) — Vector to Scalar

[[Heat Flux]] ($\mathbf{q}^{\prime\prime}$) is a vector quantity. Taking the dot product of the [[Del Operator]] and a vector calculates the [[Divergence]]:

$$\nabla \cdot \mathbf{q}^{\prime\prime} = \frac{\partial q_x}{\partial x} + \frac{\partial q_y}{\partial y} + \frac{\partial q_z}{\partial z}$$

* **Physical Meaning:** [[Divergence]] measures the net spatial flux leaving a microscopic differential volume.
  * If $\nabla \cdot \mathbf{q}^{\prime\prime} > 0$, net heat flow leaves the point (divergent outflow).
  * If $\nabla \cdot \mathbf{q}^{\prime\prime} < 0$, heat accumulates at that point.

---

## Module 2.2: Deriving the Transient Heat Equation

The governing [[Partial Differential Equation]] (PDE) of heat conduction is derived from the First Law of Thermodynamics: [[Conservation of Energy]].

Considering a microscopic, 3D cubic [[Control Volume]] ($dx \times dy \times dz$) inside an [[ADC12 Aluminum]] heat sink, the energy balance is:

$$\text{Rate of Energy In} - \text{Rate of Energy Out} + \text{Rate of Energy Generated} = \text{Rate of Energy Stored}$$

### Step 1: The Generation Term
If an [[IGBT]] dissipated energy into the structure, the rate of heat generated per unit volume is defined as $Q_v$ ($\text{W/m}^3$).

### Step 2: The Storage Term (Transient Phase)
Thermal accumulation within the differential mass is governed by material [[Density]] ($\rho$) and [[Specific Heat Capacity]] ($c_p$).

The rate of thermal energy storage over time ($t$) is:

$$\text{Rate of Storage} = \rho c_p \frac{\partial T}{\partial t}$$

### Step 3: The Conduction Term (In vs. Out)
Net heat accumulation due to spatial conduction equals the negative [[Divergence]] of the [[Heat Flux]] vector:

$$\text{Net Heat Conduction} = -\nabla \cdot \mathbf{q}^{\prime\prime}$$

### Step 4: Full PDE Formulation
Substituting these expressions back into the [[Conservation of Energy]] expression yields:

$$-\nabla \cdot \mathbf{q}^{\prime\prime} + Q_v = \rho c_p \frac{\partial T}{\partial t}$$

Substituting [[Fourier's Law]] ($\mathbf{q}^{\prime\prime} = -k \nabla T$) into the spatial flux term yields:

$$-\nabla \cdot (-k \nabla T) + Q_v = \rho c_p \frac{\partial T}{\partial t}$$

Canceling double negatives produces the standard 3D [[Transient Heat Equation]]:

$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + Q_v$$

Numerical [[FEA]] solvers (such as [[Ansys Icepak]]) construct finite-volume mesh matrices around this governing equation to calculate nodal temperature distributions.

---

## Emergence of the Laplacian Operator ($\nabla^2$)

When material [[Thermal Conductivity]] ($k$) is isotropic and uniform throughout the space (e.g., $k = 96\text{ W/m}\cdot\text{K}$ for [[ADC12 Aluminum]]), the divergence of the gradient ($\nabla \cdot \nabla$) simplifies into the [[Laplacian Operator]] ($\nabla^2$).

### 1. Mathematical Emergence of the Laplacian

Starting from the spatial conduction term:

$$\nabla \cdot (k \nabla T)$$

Pulling the constant $k$ out of the spatial differential:

$$k (\nabla \cdot \nabla T)$$

Expanding the dot product of the [[Del Operator]] with the [[Gradient]] vector:

$$k \left( \hat{i}\frac{\partial}{\partial x} + \hat{j}\frac{\partial}{\partial y} + \hat{k}\frac{\partial}{\partial z} \right) \cdot \left( \hat{i}\frac{\partial T}{\partial x} + \hat{j}\frac{\partial T}{\partial y} + \hat{k}\frac{\partial T}{\partial z} \right)$$

Evaluating the dot product generates the sum of second spatial derivatives:

$$k \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2} \right) = k \nabla^2 T$$

*(Note: The [[Laplacian Operator]] also appears in the [[Navier-Stokes Equations]] for momentum diffusion, expressed as $\mu \nabla^2 \mathbf{u}$ in [[CFD]]).*

### 2. Physical Interpretation of $\nabla^2 T$

* **First Derivative ($\nabla T$):** Represents spatial slope; governs the magnitude and vector path of [[Heat Flux]].
* **Second Derivative ($\nabla^2 T$):** Represents local spatial curvature (concavity). It compares the temperature at a specific spatial node relative to the localized mean temperature of surrounding nodes.

#### Local Spatial Average Behavior:
* **$\nabla^2 T > 0$ (Positive):** The local point is cooler than the surrounding regional average. Heat conducts inward toward the node.
* **$\nabla^2 T < 0$ (Negative):** The local point is hotter than the surrounding regional average. Heat conducts outward away from the node.
* **$\nabla^2 T = 0$ (Zero):** The local node equals the regional average. Spatial heat transfer is in a steady state without local accumulation.

Without internal volumetric generation ($Q_v = 0$), the transient spatial diffusion equation simplifies to:

$$\rho c_p \frac{\partial T}{\partial t} = k \nabla^2 T$$

---

## 1D Reduction & Thermal Resistance Networks

### Step 1: Fourier's Law (Governing Conduction)

$$\mathbf{q}^{\prime\prime} = -k \nabla T$$

For isotropic [[ADC12 Aluminum]], $k = 96\text{ W/m}\cdot\text{K}$.

### Step 2: 3D to 1D Mathematical Collapse

Starting from the general 3D equation:

$$\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + Q_v$$

Applying three physical boundary assumptions:
1. **Steady-State:** $\frac{\partial T}{\partial t} = 0$
2. **No Internal Generation in Baseplate:** $Q_v = 0$ (Heat is applied at boundary conditions from external [[IGBT]] sources).
3. **1D Heat Flow:** Temperature gradients exist purely in the $x$-direction ($\frac{\partial T}{\partial y} = 0, \frac{\partial T}{\partial z} = 0$).

The PDE collapses to an Ordinary Differential Equation (ODE):

$$\frac{d}{dx} \left( k \frac{dT}{dx} \right) = 0$$

Integrating with respect to $x$:

$$k \frac{dT}{dx} = C_1$$

Multiplying by cross-sectional area $A$ converts flux into thermal power $Q$ (Watts):

$$Q = -k A \frac{dT}{dx}$$

Integrating across a domain of thickness $L$ from boundary temperatures $T_{\text{hot}}$ ($x=0$) to $T_{\text{cold}}$ ($x=L$):

$$Q \int_{0}^{L} dx = -k A \int_{T_{\text{hot}}}^{T_{\text{cold}}} dT \implies Q \cdot L = k A (T_{\text{hot}} - T_{\text{cold}})$$

$$Q = \frac{k A \Delta T}{L}$$

### Step 3: Thermal Resistance Analogy ($R_{\theta}$)

Comparing thermal conduction to [[Ohm's Law]] ($I = \frac{\Delta V}{R}$):

$$Q = \frac{\Delta T}{\left( \frac{L}{k A} \right)}$$

$$\mathbf{R_{\theta, cond} = \frac{L}{k A} \quad [^\circ\text{C/W}]}$$

### Step 4: Thermal Capacitance ($C_{\text{th}}$)

Dynamic time delays depend on thermal energy storage within physical mass:

$$C_{\text{th}} = m \cdot c_p = \rho \cdot V \cdot c_p \quad [\text{J/}^\circ\text{C}]$$

*Sample Evaluation for $5\text{ mm}$ [[ADC12 Aluminum]] baseplate chunk ($0.01\text{ m}^2$ area, $V = 0.00005\text{ m}^3$):*
* $\rho = 2740\text{ kg/m}^3$, $c_p = 963\text{ J/kg}\cdot\text{K}$
* $m = \rho \cdot V = 2740 \cdot 0.00005 = 0.137\text{ kg}$
* $C_{\text{th}} = 0.137\text{ kg} \times 963\text{ J/kg}\cdot\text{K} \approx 132\text{ J/}^\circ\text{C}$

---

## Lumped Mass Systems & The Biot Number

### 1. The Biot Number ($Bi$) Criterion

The [[Biot Number]] is a dimensionless parameter evaluating internal conduction resistance versus external surface convection resistance:

$$Bi = \frac{h L_c}{k} = \frac{R_{\text{cond}}}{R_{\text{conv}}}$$

Where:
* $R_{\text{cond}} = \frac{L_c}{k A}$ ([[Conduction Resistance]])
* $R_{\text{conv}} = \frac{1}{h A}$ ([[Convection Resistance]])
* $L_c = \frac{V}{A_s}$ (Characteristic Length)

![[Pasted image 20260818165811.png]]

### 2. The Lumped Mass Boundary Condition ($Bi \ll 0.1$)

* **$Bi < 0.1$:** Internal thermal conduction is vastly faster than external surface convection. Spatial thermal gradients inside the body are negligible ($\nabla T \approx 0$). The spatial continuum collapses into a 0D point mass ($T(x,y,z,t) \approx T(t)$).
* **$Bi \approx 1$:** Internal conduction and external convection rates are comparable. Temperature profiles start to curve across the boundary.
* **$Bi \gg 1$:** High convection rate or low material conduction resistance limits internal heat distribution. Steep 3D spatial gradients develop, requiring full 3D transient differential modeling ([[Ansys Icepak]]).

### 3. Derivation of the 0D Energy Balance

Assuming $Bi \ll 0.1$, the 3D PDE reduces to a 0D transient ODE:

$$\text{Rate of Heat IN} - \text{Rate of Heat OUT} = \text{Rate of Energy STORED}$$

$$Q_{\text{in}} - h A_s (T - T_{\infty}) = \rho V c_p \frac{dT}{dt}$$

Integrating this first-order differential equation yields the dynamic heating response:

$$T(t) = T_{\infty} + \frac{Q_{\text{in}}}{h A_s} + \left( T_i - T_{\infty} - \frac{Q_{\text{in}}}{h A_s} \right) e^{-t/\tau}$$

### 4. The Thermal Time Constant ($\tau$)

The thermal transient rate is governed by the [[Thermal Time Constant]] $\tau$:

$$\tau = R_{\text{conv}} \cdot C_{\text{th}} = \left( \frac{1}{h A_s} \right) (\rho V c_p) = \frac{\rho V c_p}{h A_s} \quad [\text{seconds}]$$

#### Transient Milestones:
* $t = 1\tau \implies 63.2\%$ of maximum transient temperature rise.
* $t = 3\tau \implies 95.0\%$ of maximum transient temperature rise.
* $t = 5\tau \implies 99.0\%$ (Defined engineering steady-state condition).

---

## Convection Physics & Heat Transfer Coefficients

### Step 1: Newton's Law of Cooling

Convective transfer across surface boundaries into a fluid is modeled as:

$$Q_{\text{out}} = h A_s (T_s - T_{\infty})$$

Corresponding to an equivalent convection resistance:

$$R_{\text{conv}} = \frac{1}{h A_s}$$

### Step 2: Dimensionless Fluid Parameters

The [[Convection Heat Transfer Coefficient]] ($h$) is determined through empirical relations of key dimensionless parameters.

#### A. Reynolds Number ($Re$)
Ratio of inertial forces to viscous forces:

$$Re = \frac{\rho_{\text{fluid}} V L_c}{\mu_{\text{fluid}}} = \frac{V L_c}{\nu}$$

#### B. Prandtl Number ($Pr$)
Ratio of momentum diffusivity to thermal diffusivity:

$$Pr = \frac{\nu}{\alpha} = \frac{\mu c_p}{k_{\text{fluid}}}$$

*(For air at standard temperature/pressure, $Pr \approx 0.71$).*

#### C. Nusselt Number ($Nu$)
Ratio of convective to pure conductive heat transfer across the fluid boundary layer:

$$Nu = \frac{h L_c}{k_{\text{fluid}}}$$

Calculating $Nu$ allows direct extraction of $h$:

$$h = \frac{Nu \cdot k_{\text{fluid}}}{L_c}$$

### Step 3: Convection Categories

1. **Forced Convection:** Fluid velocity driven by external mechanical means (fans, pumps). Dominated by $Re$.
   * Laminar Flow over Flat Plate: $Nu = 0.664 Re^{1/2} Pr^{1/3}$
   * Turbulent Flow over Flat Plate: $Nu = 0.037 Re^{4/5} Pr^{1/3}$
2. **Natural (Free) Convection:** Buoyancy-driven flow resulting from fluid density gradients in a gravitational field ($g$). Dominated by the [[Grashof Number]] ($Gr$) and [[Rayleigh Number]] ($Ra = Gr \cdot Pr$).
3. **Mixed Convection:** Concurrent forced and natural phenomena ($Gr / Re^2 \approx 1$).

### Step 4: Natural Convection Formulations

The [[Grashof Number]] ($Gr$) evaluates buoyancy vs. viscous forces:

$$Gr = \frac{g \beta (T_s - T_{\infty}) L_c^3}{\nu^2}$$

Where $\beta = \frac{1}{T_{\infty}}$ (in Kelvin for ideal gases).

Natural convection [[Nusselt Number]] relationships typically take the form:

$$Nu = C \cdot Ra^n = C \cdot (Gr \cdot Pr)^n$$

* Laminar Natural Convection: $n = 1/4$
* Turbulent Natural Convection: $n = 1/3$

#### Flow Over Cylinders ([[Churchill-Bernstein Equation]]):

$$Nu = 0.3 + \frac{0.62 Re^{1/2} Pr^{1/3}}{\left[ 1 + (0.4/Pr)^{2/3} \right]^{1/4}} \left[ 1 + \left( \frac{Re}{282000} \right)^{5/8} \right]^{4/5}$$

### Step 5: Thermodynamic Limit (Mass Flow Saturation)

Convective surface heat transfer is bounded by fluid energy absorption limits determined by total mass flow rate $\dot{m}$ ($\text{kg/s}$):

$$Q = \dot{m} \cdot c_{p,\text{air}} \cdot \Delta T_{\text{air}}$$

---

## Fin Analysis & Extended Surfaces

### 1. The Governing Differential Equation for Fins

Considering a 1D differential fin element $dx$ with cross-sectional area $A_c$ and perimeter $P$:

$$\frac{d^2\theta}{dx^2} - \left( \frac{h P}{k A_c} \right) \theta = 0$$

Where $\theta(x) = T(x) - T_{\infty}$.

Defining the **Fin Parameter ($m$)**:

$$m = \sqrt{\frac{h P}{k A_c}} \quad [\text{m}^{-1}]$$

Rewriting the ODE:

$$\frac{d^2\theta}{dx^2} - m^2 \theta = 0$$

### 2. Fin Efficiency ($\eta_f$)

Assuming an adiabatic tip boundary condition ($\frac{d\theta}{dx}\Big|_{x=L} = 0$), [[Fin Efficiency]] is defined as actual heat transfer divided by ideal transfer if the entire fin were sustained at base temperature $T_b$:

$$\eta_f = \frac{\tanh(m L)}{m L}$$

* **Design Implication:** As fin height $L$ increases, $m L$ increases, leading to asymptotic saturation of $\tanh(mL) \to 1$. Efficiency decays as $\frac{1}{mL}$. Materials with lower conductivity (such as [[ADC12 Aluminum]], $k = 96\text{ W/m}\cdot\text{K}$) exhibit higher $m$ values, diminishing the performance return of excessively long fins.

### 3. Fin Effectiveness ($\epsilon_f$)

[[Fin Effectiveness]] evaluates total heat transfer added by the fin relative to heat transfer from the bare baseplate area without the fin:

$$\epsilon_f = \frac{Q_{\text{fin}}}{h A_c (T_b - T_{\infty})} = \sqrt{\frac{k P}{h A_c}}$$

* **$\epsilon_f < 2$:** Fin provides insufficient area or excessive conductive resistance, acting effectively as an insulating thermal blanket.
* **$\epsilon_f \ge 2$:** Extended surface enhancement provides performance gains.

---

## Atlas Connections

* [[Thermal Management]]
* [[Heat Transfer]]
* [[Fluid Mechanics]]
* [[Motor Control]]