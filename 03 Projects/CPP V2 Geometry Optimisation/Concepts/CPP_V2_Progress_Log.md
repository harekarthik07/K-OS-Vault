---
tags: [CPP, AIS-156, vibration, modal, harmonic-response, V2]
date: 2026-10-30
objective: "CPP geometry optimisation — V2 from A1 baseline"
phase: "Progress Log"
related: "[[CPP_V2_Problem_Statement]] [[CPP_V2_Approach_and_TODO]] [[CPP_V2_Flowchart]]"
---

# CPP V2 — Progress Log

## 2026-10-30

- Confirmed Modal + Harmonic Response setup in Ansys: Fixed Support + Frictionless Support (physical stopper contact, verified legit), inertial-acceleration-load method (not Base Excitation toggle) — confirmed mathematically equivalent for stress/relative-deformation, 2% damping applied consistently.
- Pulled `BBP0050-VIB-B.2.xlsx` report (comparison doc: A1 baseline vs V2 new vs 9.1.2 interim).
- Found and corrected stale/duplicate values in the report:
  - V2 Max Stress confirmed from Ansys = **13.664 MPa** (matches report, was genuinely correct).
  - A1 Max Stress corrected to **13.635 MPa** (report previously showed a stale duplicate of V2's value).
  - A1 Max Deflection corrected to **0.081351 mm** (report previously showed a stale duplicate of V2's 0.694 mm).
- **Key finding:** stress essentially unchanged A1→V2 (+0.2%), but deflection increased ~8.5× (0.0814 mm → 0.694 mm) at the same failure location (mount/boss area). Flagged as a stiffness regression requiring root-cause diagnosis before V2 geometry is finalised.
- 9.1.2 (interim iteration) noted as failing endurance margin (0.98×) — not pursuing further, reference only.
- Next session starts with: pulling Frequency Response + mode shape at the V2 peak-deflection mount to diagnose root cause (see [[CPP_V2_Approach_and_TODO]] TODO list).
