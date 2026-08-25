---
title: Heatsink Thermal Analysis — Theory and Worked Example
aliases:
  - Heatsink Theory
  - Thermal Teaching Doc
  - HS Thermal Fundamentals
  - How a Heatsink Works
tags:
  - thermal/heat-transfer
  - thermal/conduction
  - thermal/convection
  - thermal/transient
  - thermal/resistance-network
  - method/foster-network
  - method/cauer-network
  - domain/ETM
  - project/T30
  - component/heatsink
  - component/IGBT
  - type/teaching
  - type/worked-example
  - status/verified
up: "[[Electro-Thermal Management MOC]]"
related:
  - "[[Heatsink Sizing Tool]]"
  - "[[Dyno Run 44 Data]]"
  - "[[Foster Network]]"
  - "[[Cauer Network]]"
  - "[[Heatsink Thermal RLC Network]]"
  - "[[CFD Surface Film Coefficient]]"
  - "[[HS-I1 Heatsink Spec]]"
audience: Engineering team, no heat transfer background assumed
created: 2026-08-19
---

> [!map] Concept map
> **Mechanisms** — [[Conduction]] · [[Convection]] · [[Radiation]]
> **Laws** — [[Fourier's Law]] · [[Newton's Law of Cooling]]
> **Resistance** — [[Thermal Resistance]] · [[Spreading Resistance]] · [[Thermal Resistance Network]]
> **Surfaces** — [[Fin Efficiency]] · [[Boundary Layer]] · [[Heat Transfer Coefficient]]
> **Transient** — [[Thermal Capacitance]] · [[Biot Number]] · [[Thermal Time Constant]] · [[Lumped Capacitance Method]] · [[Foster vs Cauer Networks]]
> **Design** — [[Resistance Budget]] · [[Ambient Sensitivity]]

# Heatsink Thermal Analysis
## Part 1: Theory · Part 2: Worked Example

> [!info] How to read this document
> **Part 1** builds the theory from scratch. No numbers, no product values — just where each equation comes from and what it means. Read it once, top to bottom.
> **Part 2** applies every single equation from Part 1 to our actual heatsink, one step at a time. If you have never done heat transfer before, you should still be able to follow it.

---
---

# PART 1 — THEORY

---

## 1. The problem we are solving

An electronic component generates heat. That heat must reach the surrounding air, or the component gets hotter and hotter until it fails.

Heat only moves for one reason: **a temperature difference exists.** Heat always flows from hot to cold, never the reverse. This is the second law of thermodynamics and it is the only thing driving everything in this document.

Heat moves in three ways:

| Mode | What happens | Needs |
|---|---|---|
| **[[Conduction]]** | Energy passes through stationary material | Solid contact |
| **[[Convection]]** | Moving fluid carries energy away | Fluid flow |
| **[[Radiation]]** | Energy leaves as electromagnetic waves | Nothing — works in vacuum |

In a heatsink, conduction moves heat from the chip through the metal, and convection moves it from the metal into the air. Radiation is usually small at these temperatures and is often neglected.

Our job is to **quantify** each step so we can predict temperature and design against it.

---

## 2. Conduction

### 2.1 The physical mechanism

In a solid, atoms are locked in place but they vibrate. Heat them and they vibrate harder. A vibrating atom nudges its neighbour, which nudges the next one, and energy travels through the material without the material itself moving.

In metals there is a second, much faster mechanism: **free electrons**. Metals have electrons not bound to any single atom, and these drift through the lattice carrying energy. This is why metals conduct heat well and why the same materials that conduct electricity well also conduct heat well.

### 2.2 Building Fourier's law from intuition

Ask what the heat flow through a slab should depend on. Common sense gives four answers:

1. **More temperature difference → more heat flow.** Double the difference, double the flow. So heat flow is proportional to $\Delta T$.
2. **Bigger area → more heat flow.** Twice the area is like two slabs side by side. So proportional to $A$.
3. **Thicker slab → less heat flow.** The energy has further to travel. So inversely proportional to $L$.
4. **Better material → more heat flow.** Call that property $k$, the [[Thermal Conductivity|thermal conductivity]]. Proportional to $k$.

Put those four together:

$$q \propto \frac{k A \Delta T}{L}$$

Experiments confirm this is not just proportional but **exactly equal**. Written in differential form for a general case where temperature varies continuously with position:

$$\boxed{q = -kA\frac{dT}{dx}}$$

This is **[[Fourier's Law|Fourier's law]]**.

> [!note] Why the minus sign
> $dT/dx$ is positive when temperature increases as you move in the $+x$ direction. But heat flows the *other* way — toward the cold side. The minus sign makes $q$ come out positive when heat flows in $+x$. It carries no physics beyond "hot to cold".

**Units check:** $k$ is in W/mK. So $k \cdot A \cdot (dT/dx)$ = (W/mK)(m²)(K/m) = W. Correct — heat flow is in watts.

Typical conductivity values, to build intuition:

| Material class | $k$ (W/mK) | Comment |
|---|---|---|
| Copper | ~400 | Excellent |
| Aluminium alloys | ~150–200 | Good, and light |
| Steel | ~50 | Mediocre |
| Thermal pastes | ~1–5 | Poor, but far better than air |
| Plastics | ~0.2 | Insulator |
| Air (still) | ~0.026 | Insulator |

> [!important] Why thermal paste exists
> Two metal surfaces bolted together look flat but touch only at microscopic high spots — typically 1–2% of the apparent area. The gaps are filled with air at $k = 0.026$. Paste at $k = 1$ or higher is roughly 40 times better than the air it replaces. The paste is not there because it conducts well; it is there because **air conducts terribly**.

### 2.3 Deriving thermal resistance

Take a flat slab of thickness $L$ and uniform area $A$, with steady heat flow. "Steady" means nothing is heating up or cooling down — whatever goes in comes out. So $q$ is the same at every position.

Rearrange Fourier's law and separate variables:

$$q\,dx = -kA\,dT$$

Integrate from one face to the other. Let $x$ go from $0$ to $L$, and $T$ from $T_1$ to $T_2$:

$$q\int_0^L dx = -kA\int_{T_1}^{T_2} dT$$

$$qL = -kA(T_2 - T_1) = kA(T_1 - T_2)$$

Solve for the temperature difference:

$$T_1 - T_2 = q\left(\frac{L}{kA}\right)$$

Look at the bracket. It contains **only geometry and material** — nothing about how much heat is flowing. Give it a name:

$$\boxed{R_{cond} = \frac{L}{kA} \quad [\text{K/W}]}$$
^R-conduction

And the relationship becomes:

$$\boxed{\Delta T = q \times R}$$

### 2.4 What [[Thermal Resistance|thermal resistance]] means

$R$ has units of kelvin per watt. Read it as:

> **"How many degrees of temperature difference I must pay for every watt I push through."**

- **Low resistance** — heat crosses easily, small temperature penalty. Good.
- **High resistance** — heat struggles, large temperature penalty. Bad.

Resistance gets **worse** when the layer is thicker, the material is a poorer conductor, or the area is smaller.

> [!tip] This is the single most useful idea in the document
> Every heat transfer mechanism can be forced into the form $\Delta T = q R$. Once everything is a resistance, the whole problem becomes arithmetic — add them up. That is what makes complex thermal systems tractable.

---

## 3. Convection

### 3.1 The physical mechanism

Convection is heat carried away by a **moving fluid**. It happens in two stages:

1. Air molecules touching the hot surface pick up energy **by conduction** across an extremely thin layer.
2. Those heated molecules **physically move away**, carrying that energy with them, and cooler molecules take their place.

Stage 2 is what makes convection powerful. Pure conduction into still air would be hopeless — air is an insulator. But if the hot air is continuously swept away and replaced, energy leaves fast.

### 3.2 The boundary layer

Right at any solid surface, fluid velocity is exactly zero. This is the **no-slip condition** and it is always true. Velocity then rises with distance from the wall until it reaches the free stream value.

This slow-moving film near the wall is the **[[Boundary Layer|boundary layer]]**, and it is the real bottleneck. All the heat must first conduct across it before the bulk flow can carry it away.

This gives the central insight:

> [!important] Faster flow = thinner boundary layer = better cooling
> The reason a fan helps is not that it "blows the heat away". It is that faster flow makes the boundary layer thinner, so the conduction bottleneck is shorter.

Two categories:

| Type | Driver | Relative strength |
|---|---|---|
| **Natural convection** | Hot fluid becomes less dense and rises on its own | Weak |
| **Forced convection** | A fan or pump drives the flow | Strong — typically 5 to 20 times better |

### 3.3 Newton's law of cooling

The boundary layer physics is genuinely complicated — it depends on velocity, geometry, fluid properties, surface roughness and temperature. Rather than solve it every time, we bundle all of it into one number:

$$\boxed{q = hA(T_s - T_\infty)}$$
^newton-cooling

where $h$ is the **[[Heat Transfer Coefficient|heat transfer coefficient]]** in W/m²K, $T_s$ is surface temperature and $T_\infty$ is the fluid temperature far away.

This is less a law of physics than a **definition of $h$**. All the difficulty has been pushed into that one symbol.

### 3.4 Convective resistance

Rearrange into the same form as conduction:

$$T_s - T_\infty = q\left(\frac{1}{hA}\right) \quad\Longrightarrow\quad \boxed{R_{conv} = \frac{1}{hA}}$$
^R-convection

Same units, same meaning, and it can now be added to conduction resistances directly.

### 3.5 The crucial difference between $k$ and $h$

> [!warning] $h$ is NOT a material property
> $k$ is a property of a substance. Look it up in a table and it is correct.
> $h$ is a property of a **situation** — this geometry, this air speed, this surface, this temperature. Change the fan, the ducting, or the vehicle speed and $h$ changes.

This is why $h$ must ultimately be obtained by **measurement or CFD**, not from a handbook. Any thermal model that assumes a handbook $h$ is only as trustworthy as that assumption.

Rough ranges for air:

| Situation | $h$ (W/m²K) |
|---|---|
| Natural convection, still air | 5–15 |
| Light forced convection | 25–75 |
| Strong forced convection | 75–250 |

---

## 4. Extended surfaces (fins)

### 4.1 Why fins exist

Since $R_{conv} = 1/(hA)$, there are only two ways to improve convection: raise $h$ or raise $A$.

Raising $h$ means a bigger fan — costing power, noise, weight and reliability.

Raising $A$ means adding surface. Fins are the cheapest way to multiply surface area within a fixed footprint. A finned surface can have five to ten times the area of the flat plate it replaces.

### 4.2 Why a fin is not as good as it looks

Here is the catch. Heat must **conduct from the fin root out to the tip**, and it is losing heat to the air along the entire way. So less and less heat remains as you move outward, which means the temperature falls continuously from root to tip.

Cooler surface means smaller $(T_s - T_\infty)$, which means less heat rejected per unit area.

**The tip of a fin is worth less than the root.** A tall thin fin made of a poor conductor may have a tip that is barely above ambient and contributes almost nothing.

### 4.3 Deriving the fin equation

Take a thin slice of fin at position $x$, of thickness $dx$. Energy balance on that slice at steady state:

$$\underbrace{q_x}_{\text{conducted in}} = \underbrace{q_{x+dx}}_{\text{conducted out}} + \underbrace{dq_{conv}}_{\text{lost to air}}$$

Conduction in and out, from Fourier's law:

$$q_x - q_{x+dx} = -\frac{dq}{dx}dx = kA_c\frac{d^2T}{dx^2}dx$$

Convection loss from the slice's exposed perimeter $P$:

$$dq_{conv} = hP\,dx\,(T - T_\infty)$$

Setting them equal and dividing through by $dx$:

$$kA_c\frac{d^2T}{dx^2} = hP(T-T_\infty)$$

Define excess temperature $\theta = T - T_\infty$ to simplify:

$$\frac{d^2\theta}{dx^2} = \frac{hP}{kA_c}\theta$$

The group on the right has units of 1/m². Name its square root:

$$\boxed{m = \sqrt{\frac{hP}{kA_c}}}$$

For a thin rectangular fin of thickness $t$ and width $w$ where $w \gg t$, the perimeter is approximately $2w$ and the cross-section is $wt$, so:

$$m \approx \sqrt{\frac{2h}{kt}}$$

The equation is now:

$$\frac{d^2\theta}{dx^2} = m^2\theta$$

This is a standard second-order ODE whose solution is a combination of $\cosh$ and $\sinh$. Applying the boundary conditions (known root temperature, negligible heat loss from the tip) gives the temperature profile:

$$\boxed{T(x) = T_\infty + (T_{root}-T_\infty)\frac{\cosh[m(L-x)]}{\cosh(mL)}}$$

At the tip ($x = L$), $\cosh(0) = 1$, so:

$$T_{tip} = T_\infty + \frac{T_{root}-T_\infty}{\cosh(mL)}$$

### 4.4 [[Fin Efficiency|Fin efficiency]]

We want a single number for "how much worse is this real fin than a perfect one".

$$\eta_f = \frac{\text{heat the real fin rejects}}{\text{heat it would reject if it were all at root temperature}}$$

Integrating the profile above gives the standard result:

$$\boxed{\eta_f = \frac{\tanh(mL)}{mL}}$$
^fin-efficiency

Everything hinges on the dimensionless group $mL$:

| $mL$ | $\eta_f$ | Interpretation |
|---|---|---|
| 0.5 | 0.92 | Short, thick, conductive — nearly perfect |
| 1.0 | 0.76 | Typical practical fin |
| 2.0 | 0.48 | Too long — the outer half is wasted |
| 3.0 | 0.33 | Mostly wasted metal |

> [!tip] Design rule
> Aim for $mL$ around 1. Beyond $mL \approx 2$ you are adding metal, mass and cost for very little cooling. Since $m = \sqrt{2h/(kt)}$, if you want a **taller** fin you must also make it **thicker** or use a **better conductor** to keep $mL$ reasonable.

### 4.5 Overall surface efficiency

A real heatsink is not all fin. The flat base between the fins sits at full root temperature and is therefore 100% efficient. Blending the efficient base with the less efficient fins:

$$\boxed{\eta_0 = 1 - \frac{A_{fin}}{A_{total}}(1-\eta_f)}$$

And the convective resistance including this correction:

$$\boxed{R_{conv} = \frac{1}{\eta_0\,h\,A_{total}}}$$

---

## 5. [[Spreading Resistance|Spreading resistance]]

### 5.1 Why the simple formula fails

The plane wall formula $R = L/(kA)$ assumes heat enters over the **full** area $A$ and travels **straight** through.

That is true when the source covers the whole face. It is **false** when a small heat source sits on a large plate — which is exactly what an electronic component on a heatsink is.

The heat enters through a small patch and must **fan out sideways** before it can reach all the fins.

### 5.2 Two competing effects

**Effect 1 — helps.** The heat eventually gets to use the whole plate, which is much larger than the source. More area is good.

**Effect 2 — hurts.** All the heat must funnel through the small entry patch, and then funnel again to reach the far corners. This constriction is a genuine extra resistance.

The second effect is called **[[Spreading Resistance|spreading resistance]]** (or constriction resistance).

### 5.3 The correct decomposition

$$\boxed{R_{plate} = \underbrace{\frac{t}{k\,A_{plate}}}_{\text{1D term, FULL plate area}} + \underbrace{R_{spread}}_{\text{penalty for small source}}}$$

> [!warning] The most common mistake
> The first term uses the **full plate area**, not the source area. It represents the ideal case where heat has already spread perfectly. $R_{spread}$ is the extra cost of the source being smaller than the plate. Using the source area in the 1D term and omitting $R_{spread}$ is wrong twice over — the two errors partly cancel, which is why the mistake survives so long undetected.

### 5.4 What controls spreading resistance

| Factor | Effect on $R_{spread}$ |
|---|---|
| Source much smaller than plate | Increases strongly |
| Thicker plate | **Decreases** — more room to spread |
| Higher conductivity | Decreases |
| Stronger cooling on the back | Increases slightly |

The standard analytical solution is the **Lee–Yovanovich correlation**. It converts the rectangular source and plate to equivalent circles, forms three dimensionless groups, and returns a dimensionless spreading resistance. The full sequence is applied in Part 2.

### 5.5 The optimum plate thickness

This produces a result that surprises most people:

- $R_{spread}$ **falls** as the plate gets thicker (more room to spread sideways)
- $R_{1D}$ **rises** as the plate gets thicker (heat travels further)

Because one rises and one falls, **there is an optimum thickness**. Making a base plate thinner to save weight can make the heatsink *worse*.

> [!tip] Rule
> **Small source on a large plate → thicker base is better** (spreading dominates).
> **Large source covering most of the plate → thinner is better** (1D dominates).

---

## 6. [[Thermal Resistance Network|Resistance network modelling]]

### 6.1 The electrical analogy

Every mechanism so far reduced to $\Delta T = q R$. That is Ohm's law with different labels:

| Electrical | Thermal | Meaning |
|---|---|---|
| Voltage $V$ | Temperature $T$ | The driving potential |
| Current $I$ | Heat flow $q$ | What flows |
| Resistance $R$ | $R_{th}$ | Opposition to flow |
| Capacitance $C$ | $C_{th}$ | Storage |
| $V = IR$ | $\Delta T = qR_{th}$ | The governing relation |

> [!note] This is not a loose metaphor
> The governing differential equations are mathematically identical. Every circuit technique — series and parallel combination, time constants, network reduction — transfers across exactly.

### 6.2 Series

When layers are stacked so that **all the heat passes through every layer in turn**, they are in series. Temperature drops add up:

$$\Delta T_{total} = qR_1 + qR_2 + qR_3 = q(R_1+R_2+R_3)$$

$$\boxed{R_{series} = R_1 + R_2 + R_3 + \dots}$$
^R-series

**Test for series:** does *all* the heat go through both? Then series.

### 6.3 Parallel

When heat has **a choice of routes** between the same two temperatures, the paths are in parallel. The heat splits, but each path sees the same $\Delta T$:

$$q_{total} = q_1 + q_2 = \Delta T\left(\frac{1}{R_1}+\frac{1}{R_2}\right)$$

$$\boxed{\frac{1}{R_{parallel}} = \frac{1}{R_1}+\frac{1}{R_2}+\dots}$$

**Test for parallel:** do both paths connect the same two temperatures? Then parallel.

> [!important] Parallel always helps
> Adding any parallel path — even a poor one — always lowers total resistance. A surface you had ignored is free cooling. This matters more than people expect.

### 6.4 Building a chain

The method for any thermal problem:

1. **List the nodes** — every point where you can define a temperature.
2. **Identify the resistance between each pair** — conduction, convection or spreading.
3. **Decide series or parallel** using the two tests above.
4. **Add them up** to get total resistance.
5. **Multiply by heat load** to get total temperature rise.

$$T_{hottest} = T_{ambient} + q \times R_{total}$$

### 6.5 Where you measure matters

A sensor reads the temperature **at its own node**, not at the hottest point. Only the resistances **between the sensor and ambient** appear in what it measures.

> [!tip] Practical consequence
> If the sensor sits below the hottest layer, then that layer's resistance does not affect the reading at all. This can dramatically simplify a model — you do not need to know a resistance that sits above your measurement point.

### 6.6 The [[Resistance Budget|resistance budget]] — the design tool

Turn the problem around. Fix the temperature limit and the heat load, and solve for the resistance you are **allowed**:

$$\boxed{R_{allowed} = \frac{T_{limit} - T_{ambient}}{q}}$$
^resistance-budget

Every layer draws from this budget.

> [!tip] Do this before opening CAD
> It takes three lines and tells you immediately whether the target is even achievable, and which layer to attack first. Many thermal designs fail because someone optimised the fins beautifully and then discovered the interface material had already consumed a third of the budget.

---

## 7. Transient behaviour — adding time

### 7.1 Why steady state is not enough

Everything above describes where temperature **ends up** after running forever. But many real tests are short. During a short run the component is still heating up and has not reached its final temperature.

Predicting *that* requires a new ingredient: **thermal mass**.

### 7.2 [[Thermal Capacitance|Thermal capacitance]]

To raise the temperature of a mass $m$ by $\Delta T$ you must supply energy:

$$E = m\,c_p\,\Delta T$$

where $c_p$ is specific heat in J/kgK. Define:

$$\boxed{C_{th} = m\,c_p \quad [\text{J/K}]}$$
^thermal-capacitance

This is **how much energy the object must absorb to get one degree hotter.** A large $C_{th}$ means the object warms slowly — it acts as a heat sponge.

### 7.3 Deriving the governing equation

Draw an imaginary boundary around the heatsink and apply conservation of energy:

$$\text{Energy IN} - \text{Energy OUT} = \text{Energy STORED}$$

Term by term, per unit time:

- **In** — the heat load $Q(t)$
- **Out** — convection to air, which by definition is $(T - T_\infty)/R_{conv}$
- **Stored** — the rate of change of internal energy, $C_{th}\,dT/dt$

$$\boxed{Q(t) - \frac{T-T_\infty}{R_{conv}} = C_{th}\frac{dT}{dt}}$$
^governing-ode

> [!abstract] This one equation is the entire transient model
> Everything that follows is either a solution to it or a simplification of it.

Working in **excess temperature** $\theta = T - T_\infty$ removes the constant (note $d\theta/dt = dT/dt$ since $T_\infty$ is constant):

$$C_{th}\frac{d\theta}{dt} + \frac{\theta}{R_{conv}} = Q(t)$$

### 7.4 When is this valid? The [[Biot Number|Biot number]]

The equation above uses **one temperature** for the whole heatsink. Real objects have temperature gradients inside them. When is one number good enough?

Compare the two resistances heat must cross:

$$\frac{\text{internal conduction resistance}}{\text{external convection resistance}} \approx \frac{L_c/(kA)}{1/(hA)} = \frac{hL_c}{k}$$

This ratio is the **Biot number**:

$$\boxed{Bi = \frac{h\,L_c}{k}}$$
^biot-number

where $L_c$ is a characteristic length (typically half-thickness for a slab).

- $Bi \ll 1$ — internal conduction is easy compared to getting heat into the air. The solid stays nearly **isothermal** ([[Lumped Capacitance Method]]) and one temperature is a good description. The usual threshold is $Bi < 0.1$.
- $Bi \gg 1$ — significant internal gradients. A single lump is invalid.

> [!important] What this really means
> When $Bi$ is small, the complicated 3D partial differential equation for heat conduction **collapses into the simple single ordinary differential equation above**. That collapse is what makes hand calculation possible at all. Metals with air cooling almost always satisfy it.

### 7.5 Solving the ODE

Take constant power $Q$ applied as a step at $t = 0$, starting from ambient so $\theta(0) = 0$.

Start from the energy balance:

$$C\frac{d\theta}{dt} = Q - \frac{\theta}{R}$$

Factor out $1/R$ on the right:

$$C\frac{d\theta}{dt} = \frac{1}{R}\left(QR - \theta\right)$$

Separate variables — all the $\theta$ terms on one side, all the $t$ terms on the other:

$$\frac{d\theta}{QR-\theta} = \frac{dt}{RC}$$

Integrate both sides from the start to time $t$:

$$\int_0^\theta \frac{d\theta'}{QR-\theta'} = \int_0^t \frac{dt'}{RC}$$

The left side integrates to a logarithm (note the sign from the chain rule):

$$-\ln(QR-\theta)\Big|_0^\theta = \frac{t}{RC}$$

$$-\ln(QR-\theta) + \ln(QR) = \frac{t}{RC}$$

$$\ln\left(\frac{QR}{QR-\theta}\right) = \frac{t}{RC}$$

Exponentiate both sides:

$$\frac{QR}{QR-\theta} = e^{t/RC} \quad\Longrightarrow\quad QR-\theta = QR\,e^{-t/RC}$$

Solve for $\theta$:

$$\boxed{\theta(t) = QR\left(1 - e^{-t/RC}\right)}$$
^step-response

### 7.6 What the two groups mean

Two distinct quantities emerged naturally:

$$\boxed{A = QR} \qquad\qquad \boxed{\tau = RC}$$

$$\theta(t) = A\left(1-e^{-t/\tau}\right)$$

**$A$ is HOW HIGH.** As $t \to \infty$ the exponential vanishes and $\theta \to A$. This is the final steady rise, in kelvin. It depends on heat load and resistance. **It does not depend on mass or time.**

**$\tau$ is HOW FAST.** It has units of seconds. It depends on resistance and capacitance. **It does not depend on the power level.**

> [!example] The bucket analogy
> Water pours into a bucket with a hole in the bottom. As the level rises, the leak gets faster. Eventually the level settles where inflow equals leakage.
> **$A$** is the final water level. **$\tau$** is how quickly it gets there.
> A bigger bucket (more mass) takes longer but settles at the same level. A smaller hole (more resistance) settles higher *and* takes longer.

### 7.7 The meaning of the [[Thermal Time Constant|time constant]]

Substitute $t = \tau$:

$$\theta(\tau) = A(1-e^{-1}) = A(1-0.368) = 0.632A$$

So **one time constant is the time to reach 63.2% of the final value.** The 63% is not arbitrary — it falls directly out of $e^{-1}$.

| Time elapsed | Fraction of final rise |
|---|---|
| $1\tau$ | 63% |
| $2\tau$ | 86% |
| $3\tau$ | 95% |
| $5\tau$ | 99.3% — effectively complete |

### 7.8 The design ratio $t/\tau$

Compare your run duration to the time constant. This single ratio tells you which physics governs:

| $t/\tau$ | Regime | What to design |
|---|---|---|
| $\ll 1$ | **Mass dominated** | Add thermal mass. Surface area barely matters — the heat has not reached the air yet. |
| $\approx 1$ | **Transient** | Both matter. Mass is doing real work. |
| $> 3$ | **Steady dominated** | Add surface area. Mass is nearly irrelevant. |

> [!warning] The trap
> A test that is short compared to $\tau$ can pass purely on thermal mass, while the design would fail in continuous use. Always compute the steady state value as well, and always check $t/\tau$ before concluding anything.

### 7.9 General power histories

The solution above assumes constant power and a cold start. Real duty cycles have neither. For a piecewise-constant power profile, apply this **exact** step-by-step recursion:

$$\boxed{\theta_{next} = QR + \left(\theta_{now} - QR\right)e^{-\Delta t/\tau}}$$
^recursion

Read it as: **the target value, plus the remaining gap to target decaying exponentially.**

This is exact for constant power over each interval, not an approximation. It handles hot starts (non-zero $\theta_{now}$) and varying power automatically, which is why it is the form to use in a spreadsheet.

### 7.10 More than one time constant

A real assembly is not one lump — it is a chain of masses, each with its own resistance and capacitance. Small masses near the heat source respond in seconds. Large masses respond in minutes.

A single sensor sees the **sum** of all of them:

$$\theta(t) = A_1\left(1-e^{-t/\tau_1}\right) + A_2\left(1-e^{-t/\tau_2}\right) + \dots$$

> [!example] Cup inside a drum
> Pour water into a small cup sitting inside a large drum. The cup fills in seconds; the drum takes minutes. A single measurement sees both filling at once.

**How to detect this:** fit a single exponential. If the residual error shows a systematic pattern rather than random scatter, more than one time constant is present.

> [!caution] An honest limitation
> This sum-of-exponentials form is called a **[[Foster vs Cauer Networks|Foster network]]**. It reproduces the measured behaviour at the terminals exactly, but its individual elements are **mathematical, not physical** — $A_1$ and $\tau_1$ do not correspond exactly to one specific piece of metal. Assigning physical identity to each term is interpretation, and should be stated as such. A **[[Foster vs Cauer Networks|Cauer network]]** (a physical ladder of alternating R and C) does map onto real layers, but obtaining one requires either detailed geometry or extra measurements.

---

## 8. The complete method

Putting the whole of Part 1 together, the procedure for any heatsink problem:

| Step | Action | Equation |
|---|---|---|
| 1 | Compute the resistance budget | $R_{allowed} = (T_{limit}-T_\infty)/Q$ |
| 2 | List every node and resistance | — |
| 3 | Conduction layers | $R = L/(kA)$ |
| 4 | Spreading, if source is small | $R_{plate} = t/(kA_{plate}) + R_{spread}$ |
| 5 | Fin efficiency | $m = \sqrt{2h/(kt)}$, $\eta_f = \tanh(mL)/(mL)$ |
| 6 | Convection | $R_{conv} = 1/(\eta_0 h A)$ |
| 7 | Combine series and parallel | $R_{total}$ |
| 8 | Steady state check | $T = T_\infty + QR_{total}$ |
| 9 | Thermal capacitance | $C = mc_p$ |
| 10 | Time constant and regime | $\tau = R_{conv}C$, check $t/\tau$ |
| 11 | Transient temperature | $\theta(t) = A(1-e^{-t/\tau})$ |
| 12 | Compare against limit and iterate | — |

---
---


---
---

# PART 2 — WORKED EXAMPLE

**Our motor controller heatsink.** Every number below comes from applying a Part 1 equation. Each step names the section it uses and shows the intermediate arithmetic, so you can reproduce it on paper with a calculator.

> [!info] How to use Part 2
> Work through Steps 1–15 in order. At each step, note (a) which Part 1 formula you are using, (b) the numbers, (c) the answer with units. Compare your answer to the **Expected** box before moving on. The whole downstream chain depends on each number being right.

---

## Step 0 — The data we start with

| Symbol      | Value  | Unit  | Where from                                           |
| ----------- | ------ | ----- | ---------------------------------------------------- |
| $Q$         | 636    | W     | Heat load (derived in Step 14)                       |
| $T_\infty$  | 34     | °C    | Ambient (initial NTC reading, dyno run 44)           |
| $T_{limit}$ | 95     | °C    | Deration threshold (set by MC team on module NTC)    |
| $t$         | 240    | s     | 4-minute full throttle test                          |
| $m$         | 3.7    | kg    | Heatsink mass (spec sheet)                           |
| $c_p$       | 871    | J/kgK | LM25 specific heat                                   |
| $k$         | 150.6  | W/mK  | LM25 conductivity                                    |
| $t_{base}$  | 0.018  | m     | Baseplate thickness (die face to fin root)           |
| $A_{src}$   | 0.0091 | m²    | Die footprint (91 cm², module bottom face)           |
| $A_{plate}$ | 0.028  | m²    | Finned face (200×140 mm — **assumed, to confirm**)   |
| $A_{conv}$  | 0.232  | m²    | Total wetted surface (TSA from spec sheet)           |
| BLT         | 0.0001 | m     | Paste bond line thickness (100 µm)                   |
| $k_{TIM}$   | 1.1    | W/mK  | Fasto paste                                          |
| $h$         | 45.7   | W/m²K | Measured convective coefficient (derived in Step 15) |

---

## PART A — STEADY STATE RESISTANCE CHAIN

## Step 1 — The resistance budget

**Theory used:** §6.6 — $R_{allowed} = (T_{limit}-T_\infty)/Q$

Before anything else, find out how much total resistance we are allowed.

$$R_{allowed} = \frac{95 - 34}{636} = \frac{61}{636}$$

> [!success] Expected
> **$R_{allowed} = 0.0959$ K/W**
> This is your total budget. Every layer combined must stay under this or the IGBT derates.

---

## Step 2 — Thermal paste resistance

**Theory used:** §2.3 — $R = L/(kA)$

The paste is a plane wall — it covers exactly the module face, so no spreading applies.

$$R_{TIM} = \frac{\text{BLT}}{k_{TIM} \times A_{src}} = \frac{0.0001}{1.1 \times 0.0091}$$

**Compute the denominator first:** $1.1 \times 0.0091 = 0.01001$

**Then:** $R_{TIM} = 0.0001 \,/\, 0.01001$

> [!success] Expected
> **$R_{TIM} = 0.00999$ K/W**
> **Temperature cost:** $\Delta T = 636 \times 0.00999 = 6.4$ K
> That's 10% of the entire budget spent on a layer one tenth of a millimetre thick. This is why paste selection matters so much.

---

## Step 3 — Baseplate resistance (the naive way — for comparison)

**Theory used:** §5.1 — why the simple formula fails

The obvious calculation, using die area:

$$R_{naive} = \frac{t_{base}}{k \times A_{src}} = \frac{0.018}{150.6 \times 0.0091}$$

**Denominator:** $150.6 \times 0.0091 = 1.3705$

**Then:** $R_{naive} = 0.018 \,/\, 1.3705$

> [!success] Expected
> **$R_{naive} = 0.0131$ K/W** — but this is **WRONG**
> The die covers only 32% of the plate. Heat must spread sideways. Do Step 4 for the correct answer.

---

## Step 4 — Baseplate resistance (with spreading, correct method)

**Theory used:** §5.3 and §A.6 — Lee–Yovanovich correlation

Eight sub-steps. Take your time.

### 4a. Convert rectangles to equivalent circles

The correlation is axisymmetric, so we replace each rectangle with a circle of the same area.

$$a = \sqrt{\frac{A_{src}}{\pi}} = \sqrt{\frac{0.0091}{3.1416}} = \sqrt{0.002896}$$

$$b = \sqrt{\frac{A_{plate}}{\pi}} = \sqrt{\frac{0.028}{3.1416}} = \sqrt{0.008913}$$

> [!success] Expected
> $a = 0.0538$ m (source equivalent radius)
> $b = 0.0944$ m (plate equivalent radius)

### 4b. Form the dimensionless groups

$\epsilon = a/b$ (how much of the plate the source covers)
$\tau_g = t_{base}/b$ (plate thickness vs plate size)
$h_{eff} = 1/(R_{conv} \times A_{plate})$ (backside cooling collapsed to a film)
$Bi = h_{eff} \times b / k$ (Biot number for the plate)

**Plug in** (use $R_{conv} = 0.0943$ from Step 7 — small chicken-and-egg; use the target value):

$\epsilon = 0.0538 / 0.0944 = 0.570$
$\tau_g = 0.018 / 0.0944 = 0.191$
$h_{eff} = 1 / (0.0943 \times 0.028) = 1 / 0.00264 = 379$ W/m²K
$Bi = 379 \times 0.0944 / 150.6 = 35.78 / 150.6 = 0.238$

> [!success] Expected
> $\epsilon = 0.570$, $\tau_g = 0.191$, $h_{eff} = 379$, $Bi = 0.238$

### 4c. Eigenvalue $\lambda$

$$\lambda = \pi + \frac{1}{\epsilon\sqrt{\pi}} = 3.1416 + \frac{1}{0.570 \times 1.7725} = 3.1416 + \frac{1}{1.0103} = 3.1416 + 0.990$$

> [!success] Expected
> $\lambda = 4.131$

### 4d. Correction factor $\Phi$

$$\Phi = \frac{\tanh(\lambda\tau_g) + \lambda/Bi}{1 + (\lambda/Bi)\tanh(\lambda\tau_g)}$$

**Step by step:**
$\lambda\tau_g = 4.131 \times 0.191 = 0.789$
$\tanh(0.789) = 0.658$ (use calculator's tanh function)
$\lambda/Bi = 4.131 / 0.238 = 17.36$

**Numerator:** $0.658 + 17.36 = 18.02$
**Denominator:** $1 + 17.36 \times 0.658 = 1 + 11.42 = 12.42$
$\Phi = 18.02 / 12.42$

> [!success] Expected
> $\Phi = 1.451$

### 4e. Dimensionless spreading $\psi$

$$\psi = 0.5 \times (1-\epsilon)^{1.5} \times \Phi$$

$1 - \epsilon = 1 - 0.570 = 0.430$
$(0.430)^{1.5} = 0.430 \times \sqrt{0.430} = 0.430 \times 0.6557 = 0.282$
$\psi = 0.5 \times 0.282 \times 1.451$

> [!success] Expected
> $\psi = 0.204$

### 4f. Spreading resistance

$$R_{spread} = \frac{\psi}{\sqrt{\pi} \times k \times a}$$

**Denominator:** $1.7725 \times 150.6 \times 0.0538 = 14.36$
$R_{spread} = 0.204 / 14.36$

> [!success] Expected
> $R_{spread} = 0.0142$ K/W

### 4g. 1D term (using FULL plate area, not die area!)

$$R_{1D} = \frac{t_{base}}{k \times A_{plate}} = \frac{0.018}{150.6 \times 0.028} = \frac{0.018}{4.217}$$

> [!success] Expected
> $R_{1D} = 0.0043$ K/W

### 4h. Total baseplate resistance

$$R_{base} = R_{1D} + R_{spread} = 0.0043 + 0.0142$$

> [!success] Expected
> **$R_{base} = 0.0185$ K/W**
> **Temperature cost:** $\Delta T = 636 \times 0.0185 = 11.8$ K
> This is **41% higher** than the naive answer from Step 3. That extra 3.4 K is real.

> [!tip] Sanity check
> The theoretical maximum for an infinitely thick plate is $1/(4ka) = 1/(4 \times 150.6 \times 0.0538) = 0.031$ K/W. We got about half of that, which makes sense since our source covers a third of the plate.

---

## Step 5 — Fin efficiency

**Theory used:** §4.3 and §4.4 — fin parameter $m$ and $\eta_f = \tanh(mL)/(mL)$

Take representative fin dimensions: thickness $t_{fin} = 2.5$ mm, height $L = 35$ mm.

### 5a. Fin parameter $m$

$$m = \sqrt{\frac{2h}{k \times t_{fin}}} = \sqrt{\frac{2 \times 45.7}{150.6 \times 0.0025}}$$

Numerator: $2 \times 45.7 = 91.4$
Denominator: $150.6 \times 0.0025 = 0.3765$
$m = \sqrt{91.4 / 0.3765} = \sqrt{242.8}$

> [!success] Expected
> $m = 15.6$ m⁻¹

### 5b. The dimensionless group $mL$

$$mL = 15.6 \times 0.035$$

> [!success] Expected
> $mL = 0.545$
> Target range 0.5 to 2.0. You're at the low end — fins could be taller.

### 5c. Fin efficiency

$$\eta_f = \frac{\tanh(mL)}{mL} = \frac{\tanh(0.545)}{0.545} = \frac{0.497}{0.545}$$

> [!success] Expected
> $\eta_f = 0.91$ (for straight rectangular fins)
> **Note:** Back-fitting from the measurement gives $\eta_f \approx 0.76$ because your fins are radial spider fins with longer heat paths. Use 0.76 for design work.

---

## Step 6 — Overall surface efficiency

**Theory used:** §4.5 — $\eta_0 = 1 - (A_{fin}/A_{total})(1-\eta_f)$

Take $A_{fin}/A_{total} = 0.811$ (from spec sheet: 63850/78752).

$$\eta_0 = 1 - 0.811 \times (1 - 0.76) = 1 - 0.811 \times 0.24 = 1 - 0.195$$

> [!success] Expected
> $\eta_0 = 0.81$
> In our model the measured $h = 45.7$ already has $\eta_0$ folded in (since it was back-fitted from the total conductance). So in Steps 7 onwards we use $\eta_0 = 1$ in the formula and the real effectiveness is already inside $h$.

---

## Step 7 — Convective resistance

**Theory used:** §3.4 and §4.5 — $R_{conv} = 1/(\eta_0 h A)$

$$R_{conv} = \frac{1}{h \times A_{conv}} = \frac{1}{45.7 \times 0.232}$$

Denominator: $45.7 \times 0.232 = 10.60$ W/K

$$R_{conv} = 1 / 10.60$$

> [!success] Expected
> **$R_{conv} = 0.0943$ K/W**
> **Temperature cost:** $\Delta T = 636 \times 0.0943 = 60.0$ K
> This is **77% of the whole rise**. Convection is the dominant resistance — where any redesign effort should go.

> [!important] Which area to use — a critical decision
> The spec sheet lists two areas: fins + inter-fin base = 0.0788 m², and total surface area (TSA) = 0.2320 m². Using only the fin area forces $h$ to 134 W/m²K — impossible for a 50 CFM fan. Using TSA gives $h$ = 45.7, matching the CFD contour. **The enclosure walls carry roughly a third of the cooling.** See §B.5.

---

## Step 8 — Total resistance and steady state

**Theory used:** §6.2 (series combination) and §6.5 (where the sensor sits)

The module NTC sits **inside the module, below the die** (§C.4). Only the resistances between the sensor and ambient appear:

$$R_{total} = R_{TIM} + R_{base} + R_{conv} = 0.00999 + 0.0185 + 0.0943$$

> [!success] Expected
> **$R_{total} = 0.1228$ K/W**

**Steady state temperature:**
$$T_{steady} = T_\infty + Q \times R_{total} = 34 + 636 \times 0.1228 = 34 + 78.1$$

> [!success] Expected
> **$T_{steady} = 112$ °C**
> Compare to Step 1 budget of $R_{allowed} = 0.0959$: we are **28% over budget** at steady state.
> The 4-minute test only passes because the sink hasn't reached steady state. That is what Part B explains.

**Where the kelvins are:**

| Layer | $R$ (K/W) | $\Delta T$ at 636 W | Share |
|---|---|---|---|
| Paste | 0.0100 | 6.4 K | 8% |
| Base plate | 0.0185 | 11.8 K | 15% |
| Fins to air | 0.0943 | 60.0 K | **77%** |
| **Total** | **0.1228** | **78.2 K** | 100% |

---

## PART B — TRANSIENT BEHAVIOUR

## Step 9 — Thermal capacitance

**Theory used:** §7.2 — $C_{th} = mc_p$

$$C_{th} = m \times c_p = 3.7 \times 871$$

> [!success] Expected
> **$C_{th} = 3223$ J/K**
> This is how much energy the heatsink absorbs per degree of rise. A big thermal sponge.

---

## Step 10 — Time constant

**Theory used:** §7.6 — $\tau = R_{conv} \times C_{th}$

$$\tau = 0.0943 \times 3223$$

> [!success] Expected
> **$\tau = 304$ s** (about 5 minutes)
> Rule of thumb: 63% of final rise after 1τ, 95% after 3τ, essentially done after 5τ ≈ 25 min.

---

## Step 11 — The transient design ratio

**Theory used:** §7.8 — compare $t/\tau$ to the regime table

$$t/\tau = 240 / 304$$

> [!success] Expected
> **$t/\tau = 0.79$**
> Squarely in the **transient regime**. Mass is doing real work here — do not remove it.

---

## Step 12 — Temperature rise at 4 minutes

**Theory used:** §7.5 — $\theta(t) = QR_{conv}(1-e^{-t/\tau})$

**Step by step:**
$Q \times R_{conv} = 636 \times 0.0943 = 60.0$ K (this is the eventual steady rise — the "A" in the theory)
$t/\tau = 0.79$
$e^{-0.79} = 0.454$ (use calculator's exp function)
$1 - 0.454 = 0.546$

$$\theta(240) = 60.0 \times 0.546$$

> [!success] Expected
> **$\theta(240) = 32.8$ K** — the heatsink body has risen 32.8 K above ambient in 4 minutes.
> It has only reached **55% of its eventual 60 K**. The other 45% never happens because the test ends first.

---

## Step 13 — Predicted NTC temperature

The NTC sees the heatsink rise **plus** the instantaneous drops through the paste and baseplate (these layers have negligible mass and respond instantly):

$$T_{NTC}(t) = T_\infty + \theta(t) + Q \times R_{TIM} + Q \times R_{base}$$

$$T_{NTC}(240) = 34 + 32.8 + 6.4 + 11.8$$

> [!success] Expected
> **$T_{NTC}(240) = 85$ °C**
> **Measured value:** 80.9 °C. Model is 4 K conservative.
> The discrepancy comes from our single-lump model not capturing the fast baseplate response (the two-time-constant fit resolves this). For a hand calculation, 4 K conservative is good.

> [!success] Why the 4-minute test passes — the answer
> At 240 seconds the heatsink has only reached 55% of its final temperature. The 3.7 kg of aluminium is still absorbing heat. Run it long enough and it would climb to 112 °C, but the test ends first.
> **This is why mass matters, and why removing mass to save weight would directly cost test margin.**

---

## PART C — INVERSE PROBLEM (using measurement to find heat load and h)

## Step 14 — Deriving heat load from the transient itself

**Theory used:** §7.6 — since $A = QR$ and $\tau = RC$, dividing cancels $R$

From fitting the measured curve with two exponentials (§7.10):
$A_2 = 60.0$ K (slow amplitude), $\tau_2 = 304$ s (slow time constant)

$$Q = \frac{A_2 \times C_{th}}{\tau_2} = \frac{60.0 \times 3223}{304}$$

Numerator: $60.0 \times 3223 = 193{,}380$
Then: $Q = 193{,}380 / 304$

> [!success] Expected
> **$Q = 636$ W**
> **This is the payoff.** The thermal transient measures IGBT loss directly — no efficiency assumption, no datasheet loss curves, no DC current measurement. Only input is $C_{th}$.
> At 24 kW input this implies 97.4% stage efficiency — realistic for a modern traction inverter.

> [!warning] This depends entirely on $C_{th}$
> If part of the 3.7 kg is thermally lazy (mounting brackets, far corners), effective capacitance is lower and derived $Q$ scales down with it. Confirming which mass is thermally connected is the highest-value open item.

---

## Step 15 — Deriving $h$ from measurement

**Theory used:** §3.4 — $R_{conv} = 1/(hA)$, inverted

From the fit: $R_{conv} = A_2/Q = 60.0/636 = 0.0943$ K/W

$$h = \frac{1}{R_{conv} \times A_{conv}} = \frac{1}{0.0943 \times 0.232}$$

Denominator: $0.0943 \times 0.232 = 0.02188$
$h = 1 / 0.02188$

> [!success] Expected
> **$h = 45.7$ W/m²K**
> Squarely in the "light forced convection" band (§3.5). Matches CFD to within 10%. Confirms that the whole enclosure surface is doing cooling work — not just the fins.

> [!important] This is the correct way round
> Because $h$ is a property of the *situation* and not of a material (§3.5), it must be measured. The original spreadsheet assumed $h = 70$ with a small area; reality is $h = 45.7$ with a large area. Two errors that partially cancelled.

---

## Step 16 — Verification summary

Fill this in on your worksheet after all 15 steps:

| Step | Quantity | Your answer | Expected | ✓? |
|---|---|---|---|---|
| 1 | $R_{allowed}$ | | 0.0959 K/W | |
| 2 | $R_{TIM}$ | | 0.00999 K/W | |
| 4h | $R_{base}$ | | 0.0185 K/W | |
| 5b | $mL$ | | 0.545 | |
| 5c | $\eta_f$ | | 0.91 | |
| 7 | $R_{conv}$ | | 0.0943 K/W | |
| 8 | $R_{total}$ | | 0.1228 K/W | |
| 8 | $T_{steady}$ | | 112 °C | |
| 9 | $C_{th}$ | | 3223 J/K | |
| 10 | $\tau$ | | 304 s | |
| 11 | $t/\tau$ | | 0.79 | |
| 12 | $\theta(240)$ | | 32.8 K | |
| 13 | $T_{NTC}(240)$ | | 85 °C | |
| 14 | $Q$ from fit | | 636 W | |
| 15 | $h$ from fit | | 45.7 W/m²K | |

If every row matches, your understanding is aligned with the calibrated model and you can move to Excel, MATLAB or Simulink with confidence.

---

## Step 17 — What the model is used for

Now that every resistance, capacitance and time constant is established, we can ask design questions.

### Ambient sensitivity

The physics is linear in temperature: the **rise** is identical in every case — only the starting point moves. That is what makes ambient so punishing.

| Ambient (°C) | NTC at 4 min | Margin to 95 °C | Time to 95 °C |
|---|---|---|---|
| 34 (as tested) | 80.3 °C | +14.7 K | 7.9 min |
| 40 | 86.3 °C | +8.7 K | 5.9 min |
| 45 | 91.3 °C | +3.7 K | ⚠️ 4.7 min |
| **50** | **96.3 °C** | **−1.3 K** | ❌ **3.8 min** |

> [!danger] This is the real design driver
> The design was validated at 34 °C where it passes with 14.7 K to spare. At ~50 °C — realistic for under-cowl summer conditions — the 4-minute test fails outright. **This, not the cold-start case, is what the heatsink must be sized against.**

### Where to spend effort

From the Step 8 table, convection is 77% of the problem. But the cheapest kelvins are elsewhere:

| Change | Kelvin gained | Cost |
|---|---|---|
| Paste $k$ 1.1 → 3.5 W/mK | 4.4 K | one tube |
| Move die off the fan hub | 3–6 K | layout only |
| +20% fin area | ~2.3 K | new casting |
| Reduce mass by 0.7 kg | **−4.6 K** | ❌ do not do this |

---

## What to do if a step doesn't match

| Common error | Where to look |
|---|---|
| $R_{TIM}$ off | Did you use $A_{src}$ (die area), not $A_{plate}$? |
| $R_{base}$ way off | Did you use $A_{plate}$ in $R_{1D}$ and remember to add $R_{spread}$? |
| $R_{conv}$ off by 3× | Are you using TSA (0.232), not just fin area (0.079)? |
| $\tau$ off | Did you use $m = 3.7$, $c_p = 871$? Check units on $C_{th}$ |
| $\theta(240)$ off | Watch the exponent sign — it's $-t/\tau$, not $-\tau/t$ |
| $T_{NTC}$ off | Did you forget to add the paste + baseplate drops on top? |



---
---

# PART 3 — THE THERMAL RC NETWORK

## 9. Why draw it as a circuit

Every heat transfer mechanism reduces to $\Delta T = qR$ or $q = C\,dT/dt$. Those are Ohm's law and the capacitor equation with different labels. Once every layer is drawn as an electrical component, Kirchhoff's laws apply directly, existing circuit tools (Simulink, SPICE) solve it without modification, and intuition transfers — engineers who understand RC filters immediately understand RC thermal networks.

^electrical-analogy-recap

### 9.1 The building blocks

| Physical layer | Circuit component | Symbol | Units |
|---|---|---|---|
| Heat generated in silicon | Current source | $Q$ | W |
| Thermal path resistance | Resistor | $R$ | K/W |
| Material that stores heat | Capacitor to ground | $C$ | J/K |
| Ambient temperature | Fixed voltage source | $T_\infty$ | °C |
| A node in the metal | Voltage node | $T$ | °C |

^building-blocks

### 9.2 Why there is no L (inductance)

Thermal circuits use **only R and C**. Inductance has no thermal analogue because:

- Inductance opposes *changes in current* — heat has no momentum. You can start and stop a heat flow instantly with no back-force.
- Inductance stores energy in a magnetic field — heat stores energy only as raised temperature of matter, which is capacitance.

People say "RLC network" out of habit. Thermal networks are strictly **RC**.

^no-inductance

### 9.3 Sign convention

**Heat is a current source.** The IGBT dumps 568 W regardless of how hot things get — just like a constant-current source in electronics.

**Ambient is the ground rail.** Every capacitor's other terminal connects to $T_\infty$ because temperatures are measured relative to ambient — just like voltages are measured relative to ground.

^sign-convention

---

## 10. The Cauer network — physical ladder

^cauer-network

### 10.1 The arrangement

[[Cauer Network|Wilhelm Cauer]] said: arrange R's and C's as a **ladder** — resistors along the top rail, capacitors dropping to ground between them.

```
Q ──R₁──┬──R₂──┬──R₃──┬── T_amb
        │      │      │
        C₁     C₂     C₃
        │      │      │
       GND    GND    GND
```

Heat flows **through** each R in sequence. At each junction, some energy goes into the local C (storage) and the rest continues down the chain.

### 10.2 Why Cauer is powerful — every element is a real thing

^cauer-physical

| Ladder position | $R$ | $C$ | What you can point at |
|---|---|---|---|
| Rung 1 | $R_{stack}$ = 0.025 K/W | $C_{plate}$ | Paste + baseplate, with baseplate mass |
| Rung 2 | $R_{conv}$ = 0.106 K/W | $C_{hs}$ | Fins-to-air, with outer sink mass |

**The intermediate node IS a real temperature.** The junction between rung 1 and rung 2 is $T_{plate}$ — the temperature of the baseplate metal. You could measure it with a thermocouple and it would match.

**Design changes map directly:**
- Better paste? → change $R_{TIM}$ from 0.010 to 0.003. Run the model. Done.
- Lighter sink? → change $C_{hs}$. The answer is physically correct because the element you changed maps to the thing you actually changed.
- More fin area? → change $R_{conv}$. The model responds correctly.

### 10.3 Why Cauer is hard to get

**You can't get it from one sensor.** The Cauer parameters require you to know physical layer properties independently — either from:
- Material data + geometry (what we did: $R_{TIM} = BLT/(kA)$, etc.)
- Multiple sensors (a thermocouple on the fin root gives the second node)
- FEA simulation

---

## 11. The Foster network — mathematical fit

^foster-network

### 11.1 The arrangement

[[Foster Network|Ernst Foster]] said: take a bunch of RC pairs and put them **side by side, all in parallel**.

```
         Q
         │
    ┌────┼────┐
    │         │
    R₁        R₂
    │         │
    C₁        C₂
    │         │
   GND       GND
```

Each branch is independent. Each has its own time constant $\tau_i = R_i C_i$. The total response is the **sum**:

$$\theta(t) = QR_1(1-e^{-t/\tau_1}) + QR_2(1-e^{-t/\tau_2})$$

### 11.2 Our heatsink in Foster form

^foster-values

| Branch | $R_i$ | $C_i$ | $\tau_i$ | $A_i = QR_i$ |
|---|---|---|---|---|
| Fast | 0.024 K/W | 1167 J/K | **28 s** | **13.6 K** |
| Slow | 0.106 K/W | 2867 J/K | **304 s** | **60.0 K** |

$\tau_1 = 0.024 \times 1167 = 28$ s. $\tau_2 = 0.106 \times 2867 = 304$ s.

Sum them and you get **exactly** the measured curve. That's where the four numbers from §E.2 came from.

### 11.3 Why Foster is beautiful

**You get it for free from measurement.** Fit two exponentials to the NTC trace → out come $A_1, \tau_1, A_2, \tau_2$ → convert to $R_i = A_i/Q$ and $C_i = \tau_i/R_i$. Done. No knowledge of geometry, materials, or layer thicknesses needed. Ten minutes of work.

### 11.4 Why Foster is dangerous

^foster-danger

**The branches don't correspond to physical layers.**

$R_1 = 0.024$ K/W — what physical layer is that? Not the paste (0.010). Not the baseplate (0.015). Not their sum (0.025). It's a mathematical construct with no physical identity.

$C_1 = 1167$ J/K — what mass is that? 1167/871 = 1.34 kg. There is no 1.34 kg chunk you can point at.

**The intermediate node has no physical meaning.** You cannot stick a thermocouple there because "there" doesn't exist as a real location.

> [!tip] The analogy that makes this click
> Think of [[Fourier Series|Fourier series]]. You can decompose any wave into a sum of sines. Each sine has an amplitude and frequency. But the individual sines don't correspond to physical things vibrating — they're mathematical components. **Foster RC pairs are the same idea applied to thermal transients** instead of waveforms.

### 11.5 The consequence that bites you

Someone asks *"what if I use better thermal paste?"* In the real heatsink, paste is one specific layer with $R = 0.010$ K/W. In the Foster network, that 0.010 is **smeared across both branches** in a way you cannot untangle. You can't change one number — you have to **refit the whole thing** from new measured data.

**Foster tells you what will happen. It cannot tell you why, and it cannot tell you what would happen if you changed something.**

---

## 12. Foster vs Cauer — the comparison

^foster-vs-cauer

### 12.1 The water analogy

Imagine water flowing through a building.

**Foster** is standing **outside** with a flow meter on the main pipe. You measure how fast the building fills. You decompose the filling curve into "a fast component and a slow component." But you have no idea whether the fast one is the bathrooms or the kitchen. You just know the total behaviour at the pipe.

**Cauer** is the **floor plan.** You know the pipe goes to the kitchen first (small room, fills fast), then to the living room (big room, fills slowly). You know the pipe diameter (resistance) and room size (capacitance) of each. If someone asks *"what if we made the kitchen bigger?"* you can answer directly.

### 12.2 Decision table

| You are... | Use | Why |
|---|---|---|
| Reading a datasheet $Z_{th}$ curve | **Foster** | that's how they're published |
| Predicting deration time on a known design | **Foster** | terminal behaviour is what matters |
| Designing a new heatsink | **Cauer** | you need to change individual layers |
| Running Simulink for the T30 | **Cauer** | matches physics, design-tuneable |
| Validating against a dyno run | **Foster** | it IS the measured data |

### 12.3 The one sentence for any meeting

> **Foster matches the measurement but can't answer "what if". Cauer answers "what if" but needs physical data to build.**

^one-sentence

---

## 13. The corrected RC circuit — our heatsink

^corrected-circuit

### 13.1 The topology

Heat from the IGBT crosses the massless stack ($R_{JC}$, $R_{TIM}$, $R_{base}$) to reach the baseplate node $T_{plate}$. From there it has **two paths to ambient** — in parallel:

```
Q → Tj ─R_JC─ Tc(NTC) ─R_TIM─ R_base ─ Tplate ──R_metal── Ths ─R_conv,HS─ T∞
                                           │                  │
                                        C_plate             C_hs
                                           │                  │
                                           ├──R_conv,B──────► T∞
                                           │
                                          GND
```

**Path 1 — Base direct:** $R_{conv,B} = 5.0$ K/W. The base surface under the IGBT, in the fan's dead zone. Carries only **12 W = 2%** of the heat.

**Path 2 — Lateral to outer fins:** $R_{metal} + R_{conv,HS} = 0.03 + 0.108 = 0.138$ K/W. Carries **556 W = 98%** of the heat.

**Parallel check:** $5.0 \parallel 0.138 = 0.1057$ K/W — matches the measured $R_{conv}$ exactly. ✓

### 13.2 Every value in the circuit

^circuit-values

| Component | Value | Physical meaning | Source |
|---|---|---|---|
| $Q$ | 568 W | IGBT electrical loss | derived from thermal fit |
| $R_{JC}$ | 0.042 K/W | Junction to case (0.25/6) | datasheet (to confirm) |
| $R_{TIM}$ | 0.010 K/W | Fasto paste, 100 µm | calculated |
| $R_{base}$ | 0.015 K/W | Baseplate incl. spreading | Yovanovich + measured |
| $C_{plate}$ | ~1300 J/K | Baseplate zone mass | **estimated** |
| $R_{conv,B}$ | 5.0 K/W | Base to air, fan dead zone | $h_B$=50, $A_B$=4000 mm² |
| $R_{metal}$ | ~0.03 K/W | Lateral conduction in sink | **estimated** |
| $C_{hs}$ | ~1600 J/K | Outer sink mass | **estimated** |
| $R_{conv,HS}$ | 0.108 K/W | Outer fins + walls to air | from total $G$ minus $G_B$ |
| $T_\infty$ | 34 °C | Ambient (ground rail) | measured |

### 13.3 Steady state node temperatures

| Node | Temperature | Rise above ambient |
|---|---|---|
| $T_\infty$ | 34 °C | — |
| $T_{hs}$ | 94 °C | 60 K (convection) |
| $T_{plate}$ | 102 °C | +8.5 K (base plate) |
| $T_c$ (NTC) | 108 °C | +5.7 K (paste) |
| $T_j$ | 132 °C | +23.9 K (junction) |

### 13.4 KCL equations (the governing ODEs)

**At $T_{plate}$** — three currents out plus storage:

$$C_{plate}\frac{d\theta_{plate}}{dt} = Q - \frac{\theta_{plate}}{R_{conv,B}} - \frac{\theta_{plate}-\theta_{hs}}{R_{metal}}$$

**At $T_{hs}$** — one current in, one out, plus storage:

$$C_{hs}\frac{d\theta_{hs}}{dt} = \frac{\theta_{plate}-\theta_{hs}}{R_{metal}} - \frac{\theta_{hs}}{R_{conv,HS}}$$

where $\theta = T - T_\infty$ is excess temperature above ambient.

**The massless stack gives NTC and junction by algebra:**

$$T_c = T_{plate} + Q \times (R_{TIM} + R_{base})$$
$$T_j = T_c + Q \times R_{JC}$$

### 13.5 What is confirmed vs estimated

^confidence-table

| Quantity | Confidence | Basis |
|---|---|---|
| $C_{th,total}$ = 2874 J/K | 🟢 **Confirmed** | $\tau_2/R_{conv}$ matches 3.3 kg to 0.4% |
| $R_{conv,total}$ = 0.1057 K/W | 🟢 **Confirmed** | from Foster fit |
| $R_{base}$ = 0.015 K/W | 🟢 **Confirmed** | Yovanovich matches measurement within 3.8% |
| $R_{TIM}$ = 0.010 K/W | 🟢 Calculated | standard formula |
| $Q$ = 568 W | 🟡 Depends on mass | derived via $C_{th}$ |
| $R_{conv,B}$ = 5.0 K/W | 🟠 Estimated | $h_B$=50 and $A_B$=4000 mm² assumed |
| $R_{metal}$ ≈ 0.03 K/W | 🟠 Estimated | geometry-based |
| $C_{plate}$/$C_{hs}$ split | 🟠 **Estimated** | Foster, not individually identifiable from one sensor |

---

## 14. MATLAB implementation

^matlab-implementation

Two models in one script. No toolboxes needed.

### 14.1 Foster model — exact, one line

```matlab
theta = A1*(1-exp(-t/tau1)) + A2*(1-exp(-t/tau2));
T_NTC = T_amb + theta;
```

Matches measurement by definition. Use for **prediction and validation**.

### 14.2 Cauer model — single-lump ODE, one recursion

```matlab
theta(i+1) = Q*R_conv + (theta(i) - Q*R_conv) * exp(-dt/tau);
T_NTC = T_amb + theta + Q(t)*R_stack;
```

Off by ~2 K in first 60 s, then <1 K. Use for **drive cycles and design changes** — because you can change $R_{conv}$, $C_{th}$, or $Q(t)$ and the model responds correctly.

**Key detail for drive cycles:** the $R_{stack}$ term uses $Q(t)$, not $Q_{constant}$. When power drops, the junction drops **immediately** while the sink stays hot. That's the correct physics.

### 14.3 Which to use when

| Task                                      | Model             |
| ----------------------------------------- | ----------------- |
| Will this duty cycle trip deration?       | Foster            |
| What if I change fin area / mass / paste? | Cauer             |
| Drive cycle with varying power            | Cauer (recursion) |
| Validate against a new dyno run           | Foster            |


## Summary — what we learned

1. **The resistance chain is paste 6.4 K + base plate 11.8 K + convection 60 K = 78 K rise.** Convection dominates at 77%.

2. **Spreading resistance matters.** The naive 1D formula was optimistic by 30%. Always use the full plate area in the 1D term and add $R_{spread}$ separately.

3. **The area to use is the total wetted area, not just the fins.** The enclosure walls carry about a third of the cooling as a parallel path.

4. **The 4-minute test passes because of thermal mass, not because of good cooling.** At $t/\tau = 0.79$ the heatsink reaches only 55% of its steady value. Steady state would be 112 °C.

5. **The heat load can be measured from the temperature curve** using $Q = A_2C_{th}/\tau_2$, with no electrical measurement needed.

6. **The design is not over-designed — it is under-tested.** At 34 °C there is 14.7 K of margin; at 50 °C it fails.

---

## Appendix — every formula used

| Section | Quantity | Formula |
|---|---|---|
| 2.2 | Fourier's law | $q = -kA\,dT/dx$ |
| 2.3 | Conduction resistance | $R = L/(kA)$ |
| 3.3 | Newton cooling | $q = hA(T_s-T_\infty)$ |
| 3.4 | Convection resistance | $R = 1/(hA)$ |
| 4.3 | Fin parameter | $m = \sqrt{2h/(kt)}$ |
| 4.3 | Fin temperature profile | $T(x) = T_\infty + (T_r-T_\infty)\cosh[m(L-x)]/\cosh(mL)$ |
| 4.4 | Fin efficiency | $\eta_f = \tanh(mL)/(mL)$ |
| 4.5 | Overall surface efficiency | $\eta_0 = 1-(A_{fin}/A_{tot})(1-\eta_f)$ |
| 5.3 | Plate with spreading | $R = t/(kA_{plate}) + R_{spread}$ |
| 5.4 | Spreading (Yovanovich) | $R_{spread} = \psi/(\sqrt{\pi}ka)$ |
| 6.2 | Series | $R = R_1+R_2+\dots$ |
| 6.3 | Parallel | $1/R = 1/R_1+1/R_2+\dots$ |
| 6.6 | Resistance budget | $R_{allowed} = (T_{limit}-T_\infty)/Q$ |
| 7.2 | Thermal capacitance | $C = mc_p$ |
| 7.3 | Governing equation | $Q - \theta/R = C\,d\theta/dt$ |
| 7.4 | Biot number | $Bi = hL_c/k$ |
| 7.5 | Step response | $\theta(t) = QR(1-e^{-t/RC})$ |
| 7.6 | Time constant | $\tau = RC$ |
| 7.9 | Piecewise recursion | $\theta_{next} = QR + (\theta_{now}-QR)e^{-\Delta t/\tau}$ |
| 7.10 | Two time constants | $\theta = A_1(1-e^{-t/\tau_1}) + A_2(1-e^{-t/\tau_2})$ |


---

## Notes to create from this

These are the atomic concepts this document depends on. Unresolved links will appear in the graph — create them as you go.

**Mechanisms and laws**
- [[Conduction]] — energy through stationary material
- [[Convection]] — energy carried by moving fluid
- [[Radiation]] — energy as electromagnetic waves
- [[Fourier's Law]] — see ^R-conduction
- [[Newton's Law of Cooling]] — see ^newton-cooling
- [[Thermal Conductivity]] — the material property $k$
- [[Heat Transfer Coefficient]] — the situation property $h$
- [[Boundary Layer]] — why flow speed controls cooling

**Resistance modelling**
- [[Thermal Resistance]] — the $\Delta T = qR$ idea
- [[Spreading Resistance]] — small source on a large plate
- [[Fin Efficiency]] — see ^fin-efficiency
- [[Thermal Resistance Network]] — series and parallel
- [[Resistance Budget]] — see ^resistance-budget

**Transient behaviour**
- [[Thermal Capacitance]] — see ^thermal-capacitance
- [[Biot Number]] — see ^biot-number
- [[Lumped Capacitance Method]] — when one temperature is enough
- [[Thermal Time Constant]] — see ^step-response
- [[Foster vs Cauer Networks]] — mathematical vs physical fits

**Project artefacts**
- [[HS-I1 Heatsink Spec]] · [[Dyno Run 44 Data]] · [[CFD Surface Film Coefficient]] · [[Heatsink Sizing Tool]]

---

## Transclusion examples

Pull a single equation into any other note without copying it:

```
![[Heatsink Theory and Worked Example#^resistance-budget]]
![[Heatsink Theory and Worked Example#^biot-number]]
![[Heatsink Theory and Worked Example#^Q-from-transient]]
```

Pull a whole section:

```
![[Heatsink Theory and Worked Example#5. Spreading resistance]]
```

## Dataview

Find everything in this thermal cluster:

````
```dataview
LIST
FROM #thermal/heat-transfer OR #domain/ETM
SORT file.name ASC
```
````
