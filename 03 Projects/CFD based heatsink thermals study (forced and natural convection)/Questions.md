---
type: questions
project: CFD based heatsink thermals study (forced and natural convection)
---

# Open Questions

- [ ] Q1 — After convergence, does the actual mesh y+ on the HS surfaces match the assumed Yplus-for-HTC (needed for a correct h report)?
- [ ] Q2 — Does the fan dead-zone h from CFD line up with the dyno-measured value used to validate the boussinesq baseline?

# Answered

- Why Boussinesq and not incompressible-ideal-gas? → Fan-dominated case (low Richardson number) means the boussinesq buoyancy-linearization error is negligible, and it's validated against dyno while ideal-gas destabilized the fan coupling. See [[MC Heatsink CHT — Consolidated Setup]].
