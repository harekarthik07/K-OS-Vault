---
type: resource
project: EV Academy
tags: [ev-academy, curriculum]
---

# EV Academy — Curriculum

Up: [[00 Home|EV Academy]] · [[Study Protocol]] · [[Progress]]

## How it runs
- **Daily (≈90 min):** 10 min recall quiz → 50 min lesson → 30 min apply (hand calc or Ansys tie-in).
- **Gate:** a lesson is done only when Karthik explains it back correctly. Fail → re-teach.
- **Saturday:** weekly review (K-OS `weekly`) — 10-question quiz + review note in `04 Knowledge/weekly/`.
- **Every lesson ends with the CAE question:** how would I simulate or validate this?

## Semester 1 — EV Powertrain Foundations (Weeks 1–9)
| Code | Course | Wks | Domain | Core topics | Exit test |
|---|---|---|---|---|---|
| EV101 | EV Systems Overview | 1 | Power Electronics | Energy flow, ECU roles, regen, derating, HV vs LV | Draw the T30 powertrain from memory |
| EV102 | Battery Cells & Packs | 2 | Battery & BMS | NMC/LFP, form factors, V/Ah/Wh, IR, C-rate, S/P, Bernardi heat, ageing, thermal runaway | Size a pack for range & peak power; compute heat |
| EV103 | Battery Management Systems | 2 | Battery & BMS | Cell monitoring, SOC (coulomb counting, OCV, Kalman), SOH, balancing, SOP, contactors, isolation, faults | Walk a fault from detection to contactor open |
| EV104 | Electric Machines | 2 | Motor Control | Torque–speed, PMSM/IM/SRM, back-EMF, Kt/Ke, losses, efficiency maps, demag, cooling | Read an efficiency map; locate loss peaks |
| EV105 | Motor Controllers | 2 | Power Electronics | DC→3φ, MOSFET/IGBT/SiC, PWM, FOC (d/q), field weakening, switching & conduction losses | Explain FOC plainly; compute switching losses |

**Practical:** pack heat budget for a T30 ride cycle (hand calc vs your Ansys model).

## Semester 2 — Integration & Two-Wheeler Dynamics (Weeks 10–18)
| Code | Course | Wks | Domain | Core topics | Exit test |
|---|---|---|---|---|---|
| EV201 | VCU & Vehicle Control | 2 | Motor Control | Torque request chain, ride modes, regen blending, traction control, CAN, state machines, limp modes | Trace a throttle twist through every ECU |
| EV202 | Charging & HV Safety | 1 | Battery & BMS | AC/DC charging, CC-CV, charger↔BMS handshake, isolation, IP, AIS-156/038 | Explain a charge session end-to-end |
| VD201 | 2W Geometry & Statics | 2 | Vehicle Dynamics | Wheelbase, CoG, rake, trail, offset, weight distribution | Compute trail from rake/offset/tyre radius |
| VD202 | 2W Longitudinal | 1 | Vehicle Dynamics | Road load, rolling resistance, aero, gradeability, weight transfer, braking, ABS | Road-load equation; 0–60 time |
| VD203 | 2W Lateral | 2 | Vehicle Dynamics | Lean, counter-steering, gyroscopics, camber thrust, slip, wobble & weave | Explain counter-steering; derive lean angle |
| VD204 | 2W Suspension & Chassis | 1 | Vehicle Dynamics | Fork, monoshock, spring rate, damping, sag, anti-squat, chain pull, frame stiffness | Pick spring rate for load & frequency |

**Practical:** T30 energy model (speed trace → power → current → heat → range).

## Semester 3 — Four-Wheeler & Advanced (Weeks 19–24)
| Code | Course | Wks | Domain | Core topics | Exit test |
|---|---|---|---|---|---|
| VD301 | 4W Suspension Geometry | 2 | Vehicle Dynamics | Camber, caster, toe, KPI, scrub radius, Ackermann, roll centre | Explain each angle and its failure mode |
| VD302 | Tyres & Handling | 1 | Vehicle Dynamics | Slip angle, cornering stiffness, Pacejka, understeer gradient, bicycle model | Classify under/oversteer from data |
| VD303 | Ride & NVH | 2 | Vibrations | Quarter-car, transmissibility, road PSD, motor whine, Campbell diagram | Build a quarter-car model |
| EV301 | EV Thermal Architecture | 1 | Thermal Management | Pack+motor+MC loop, energy management, range estimation | Design a 2W thermal loop |

## Parallel CAE track (the 30-min apply block)
| Code | Module | With | Domain | Focus |
|---|---|---|---|---|
| CAE1 | Battery Thermal | EV102–103 | Thermal Management | Fluent MSMD (NTGK/ECM/P2D), cooling plates, Tmax/ΔT |
| CAE2 | Motor & MC Thermal | EV104–105 | Thermal Management | Loss maps as heat sources, winding/magnet temps, MOSFET Tj |
| CAE3 | Structural & Vibration | VD2xx | Solid Mechanics | Frame stiffness, modal, random vibration, bracket fatigue |
| CAE4 | Verification & Validation | all | CFD | Mesh independence, correlation, uncertainty, V&V plans |
| CAE5 | System-level & ROM | Sem 2–3 | Thermal Management | Twin Builder 1D, ROMs, 3D→system coupling |

## Capstone (Weeks 25–26)
**T30 Digital Twin Lite:** logged ride → road load → motor/MC losses → pack current & heat → thermal ROM → predicted temps vs logged → V&V report (`Results/`).

## Reading list
See `06 Resources/` → [[EV Academy Reading - Battery & BMS]] · [[EV Academy Reading - Power Electronics]] · [[EV Academy Reading - Vehicle Dynamics]]
