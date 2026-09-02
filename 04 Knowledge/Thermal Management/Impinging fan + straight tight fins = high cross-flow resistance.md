---
concept: Impinging fan over straight tight fins raises cross-flow resistance
origin_project: CFD based heatsink thermals study (forced and natural convection)
domain: Thermal Management
status: promoted
promoted: 2026-09-02
created: 2026-09-02
sources: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]", "[[Daily Log#2026-09-02]]"]
extracted_from: ["[[Fan PQ Health Check & Reverse-Flow Diagnosis]]"]
tags: [thermal, heatsink, fin-design, fan-model, impingement]
---

# Impinging fan + straight tight fins = high cross-flow resistance

## Working definition (project-specific)
An axial fan blowing **down onto** a heatsink discharges radially, over the full 360°. The fin field must be able to accept that. Two fin styles behave completely differently under the same fan:

| Fin style | Discharge paths | Result |
|---|---|---|
| Curved / open radial | all 360°, aligned with the natural flow | low K |
| Straight / tight parallel | 2 channel directions only | flow arriving off-axis slams into fin walls → large loss ⇒ high K |

## Notes / derivations / snippets
- The loss is not primarily *along* the channels — it's the **turning loss** at the entrance, where radial discharge has to bend into the channel axis. Off-axis sectors pay the most.
- A **central pin cluster** sitting in the hub shadow is doubly bad: it adds blockage exactly where the flow already has the least momentum (see [[Dead-zone h is a different regime, not a correction factor]]).
- Design heuristic: **align the fin discharge topology with the fan's discharge topology.** Radial fan ⇒ radial/curved fins. Ducted axial flow ⇒ straight parallel fins.
- Thermal trap: straight tight fins increase *area*, which looks good on paper, while collapsing *flow*. Net h·A can fall. Always price a fin change as a K ratio, not an area ratio.

## Promotion checklist ✅ promoted 2026-09-02
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [x] Linked to a Knowledge MOC (`[[Thermal Management]]`)
- [x] Sources cited

## Atlas Connections
- [[Thermal Management]] · [[CFD]]
- [[Tighter fins raise system K → operating point shifts left toward stall]] · [[Fan PQ Health Check & Reverse-Flow Diagnosis]]
