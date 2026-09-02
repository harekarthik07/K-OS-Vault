## I. Section Classification

Your notes logically break down into the following functional categories:

1. **Fundamentals & Objectives:** Introduction and key benefits of external flow analysis.
    
2. **High-Level Methodology:** The three-stage CFD workflow.
    
3. **Domain & Discretization (Pre-Processing):** CAD clean-up and meshing strategies.
    
4. **Physics & Numerical Methods (Solve):** Solver selection, turbulence modeling, and convergence.
    
5. **Data Extraction & Interpretation (Post-Processing):** Visualizing and engineering the results.
    
6. **Quality Control:** Best practices and key takeaways.

## II. Detailed Section Expansions

### 1. Fundamentals & Objectives

External flow analysis aims to understand how a fluid behaves when it is forced to flow _around_ an obstacle. This is fundamentally different from internal flow (like pipes), as the outer boundaries are theoretically infinite (the far-field).

- **Aerodynamic Forces:** The primary goal is often predicting forces. The solver calculates these forces by integrating surface pressure and shear stress over the body. We typically analyze these as dimensionless coefficients:
    
    - **Drag Coefficient ($C_D$):**
        
        $$C_D = \frac{D}{\frac{1}{2}\rho v^2 S}$$
        
    - **Lift Coefficient ($C_L$):**
        
        $$C_L = \frac{L}{\frac{1}{2}\rho v^2 S}$$
        
- **Flow Separation & Wakes:** As fluid flows over a curved surface (like an airfoil or a car roof), it experiences pressure gradients. An _adverse pressure gradient_ forces the flow to slow down and eventually detach from the surface, creating a turbulent "wake" or recirculation zone (what your notes refer to as the "dead in the regions" or void).
### 2. High-Level Methodology

The standard three-stage workflow (Pre-Processing, Solve, Post-Processing) is iterative. Rarely does a simulation succeed perfectly on the first try. A poor result in Post-Processing (e.g., non-physical pressure spikes) usually requires a return to Pre-Processing to refine the mesh in that specific area.

### 3. Domain & Discretization (Pre-Processing)

This is where the foundation of an accurate solution is built.

- **CAD Defeaturing:** Small details (like bolt heads or minor gaps) drastically increase the cell count and can cause mesh quality issues (like highly skewed cells) without actually affecting the macro-level fluid physics.
    
- **Domain Sizing:** The rule of "5–10 downstream" is critical. If the outlet boundary is too close to the body, it artificially restricts the development of the wake, forcing the solver to suppress natural pressure fluctuations, which ruins drag predictions.
    
- **Boundary Layer & $y^+$:** To capture flow separation accurately, the mesh must resolve the boundary layer. The dimensionless wall distance, $y^+$, dictates the height of the first mesh cell off the wall:
    
    $$y^+ = \frac{u_* y}{\nu}$$
    
    For models resolving the viscous sublayer (like $k-\omega$ SST), you generally target $y^+ < 1$. The inflation layer growth rate (1.1–1.3) ensures that the volume change between adjacent cells remains gradual, preventing truncation errors in the numerical derivatives.

### CAD Defeaturing & Domain Strategy

Proper geometry preparation prevents wasted computational effort and poor cell quality.

- Eliminate non-essential details like small fillets, flush fasteners, or minor gaps unless they directly alter the macro-level flow or wake.
    
- Resolve overlapping faces and sharp, acute angles to prevent near-zero feature sizes, which inherently cause highly skewed mesh cells.
    
- Set domain dimensions conservatively: maintain 2.5 to 5 body lengths upstream/laterally, and 5 to 10 body lengths downstream to allow full wake development without artificially suppressing pressure fluctuations at the outlet.

### Boundary Layer Dynamics & Separation

- **The Boundary Layer:** This is the thin region of fluid directly adjacent to the surface where viscous forces dominate, causing the flow velocity to drop from freestream speed down to exactly zero at the surface (the no-slip condition).
    
- **Flow Separation:** As fluid moves over a curved geometry, it often encounters an _adverse pressure gradient_ (where pressure increases in the direction of the flow). This gradient drains the boundary layer's momentum, eventually causing the fluid to stop, reverse direction, and detach from the surface, forming a recirculating wake.
    
- **Resolution Strategy:** To predict exactly where this separation occurs, the mesh must explicitly resolve these steep near-wall velocity gradients using prismatic inflation layers, relying on a gradual growth rate (typically 1.1–1.3) to prevent numerical truncation errors.
    

### Understanding $y^+$ ($y$-Plus)

The dimensionless wall distance, $y^+$, acts as a coordinate system for the boundary layer, dictating exactly which flow region your first mesh cell occupies.

- **The Equation:**
    
    $$y^+ = \frac{u_* y}{\nu}$$
    
    where $u_*$ is the friction velocity, $y$ is the absolute distance from the wall to the first cell center, and $\nu$ is the fluid's kinematic viscosity.
    
- **Friction Velocity ($u_*$):** This is not a physical flow velocity, but a mathematical scale derived from the wall shear stress ($\tau_w$), representing the local frictional forces acting on the fluid.
    
- **Targeting $y^+ < 1$:** This strict requirement forces the first cell squarely into the _viscous sublayer_—the innermost slice of the boundary layer. This allows the solver to calculate wall shear stress and flow separation directly from the flow physics, rather than estimating them using empirical wall functions.
    

### The $k-\omega$ SST Turbulence Model

RANS (Reynolds-Averaged Navier-Stokes) models solve additional transport equations to account for the chaotic fluctuations of turbulence without requiring a supercomputer to model every single eddy.

- **Turbulent Kinetic Energy ($k$):** Represents the physical kinetic energy contained within the fluctuating turbulent eddies.
    
- **Specific Dissipation Rate ($\omega$):** Represents the rate at which this turbulent energy dissipates into internal thermal energy due to viscous forces.
    
- **The SST Formulation:** The Shear Stress Transport (SST) variant is the industry standard for external aerodynamics. It intelligently blends two models: it uses $k-\omega$ near the wall (which excels at predicting flow separation in adverse pressure gradients) and seamlessly switches to the $k-\epsilon$ model in the freestream (which avoids the standard $k-\omega$ model's oversensitivity to inlet boundary conditions).
### The Boundary Layer and $y^+$

The dimensionless wall distance, $y^+$, is critical for determining how your near-wall mesh interacts with your chosen turbulence model.

- $y^+$ is calculated using the friction velocity ($u_\tau$), absolute distance to the wall ($y$), and the fluid's kinematic viscosity ($\nu$):
    
    $$y^+ = \frac{u_\tau y}{\nu}$$
    
- For wall-resolved simulations capturing adverse pressure gradients (using models like $k-\omega$ SST), target $y^+ < 1$ to place the first cell firmly inside the viscous sublayer.
    
- If using wall functions (like standard $k-\epsilon$), target $30 < y^+ < 300$ to place the first cell in the log-law region, avoiding the buffer layer ($5 < y^+ < 30$) where standard turbulence models struggle to predict accurate shear stress.
    

### Inflation Layers & Mesh Transitions

Once the first cell height is calculated, inflation layers smoothly transition the mesh from the wall into the freestream.

- Maintain a gradual mesh growth rate (typically 1.15 to 1.3) between adjacent inflation layers to avoid numerical truncation errors in the solver.
    
- Generate a minimum of 15 to 20 inflation layers for wall-resolved meshes to ensure the entire boundary layer thickness is captured within the structured prismatic cells.
    
- Verify that the volume transition from the final inflation layer to the core tetrahedral or polyhedral mesh is smooth to prevent localized solver instability.
    

### Strategic Mesh Refinement

High-quality meshes prioritize density precisely where the physics demand it.

- Apply volumetric refinement zones (density boxes) to capture high-gradient regions, such as stagnation points, leading edges, and trailing edge vortex shedding.
    
- Utilize curvature-based refinement on curved surfaces to ensure the physical geometry is smoothly represented with at least two cells across any meaningful curved feature.

### 4. Physics & Numerical Methods (Solve)

Your **CFD and Fluid Mechanics** file highlights several crucial solver settings. Selecting the right physics dictates numerical stability and physical accuracy.

|**Setting**|**Selection Criteria**|**Description**|
|---|---|---|
|**Solver Type**|Pressure-Based vs. Density-Based|Use Pressure-Based for incompressible flows ($Ma < 0.3$). Use Density-Based for compressible flows with shockwaves ($Ma > 0.3$).|
|**Turbulence Model**|$k-\omega$ SST|The industry standard for external aerodynamics. It blends the $k-\omega$ model near the wall (great for adverse pressure gradients) with $k-\epsilon$ in the free stream.|
|**Advanced Corrections**|Low-Re & Curvature|**Low-Re correction** helps accurately model flows where viscous forces dominate locally. **Curvature correction** modifies the turbulence production terms in regions of strong streamline curvature (like leading edges or vortices).|

- **Pressure-Velocity Coupling:**
    
    - **SIMPLE/SIMPLEC:** Good for steady-state, incompressible flows. SIMPLEC converges slightly faster for simpler flows.
        
    - **PISO:** Highly recommended for transient (time-dependent) simulations because it maintains continuity at every time step.
        
    - **Coupled:** Solves momentum and pressure-based continuity equations simultaneously. It uses more RAM but is highly robust and recommended for complex aerodynamics.
        

### 5. Data Extraction & Interpretation (Post-Processing)

Translating colorful contours into actionable engineering data is the final hurdle.

- **Pressure Coefficient ($C_p$):** Instead of raw pressure, engineers look at surface $C_p$ distribution to find stagnation points ($C_p = 1$) and high-velocity suction peaks ($C_p < 0$).
    
- **Wake Visualization:** Plotting Turbulent Kinetic Energy (TKE) or using $\lambda_2$ criterion isosurfaces helps visualize exactly where the flow becomes chaotic and sheds vortices (identifying the "dead regions").
    

### 6. Quality Control & Best Practices

A converged residual graph is meaningless if the mesh is poor or the physics are wrong.

- **Quality Metrics:**
    
    - **Orthogonal Quality:** Should ideally be $> 0.1$. It measures how close the angle between adjacent cell faces is to optimal.
        
    - **Skewness:** Must be kept $< 0.95$ (ideally $< 0.8$). Highly skewed cells cause the solver equations to become ill-conditioned, leading to divergence.
        
- **Monitor Points:** Always monitor physical values like $C_D$ and $C_L$ over iterations. True convergence is reached when these values flatline, even if the equation residuals have already dropped below $10^{-4}$.