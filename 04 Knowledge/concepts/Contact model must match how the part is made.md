---
concept: Contact model must match how the part is made
origin_project: Busbar G-Bridge Thermal Fatigue
domain: Solid Mechanics
status: budding
created: 2026-09-24
aliases: ["bonded vs frictional contact", "contact manufactures stress"]
sources: ["[[Thermal_Fatigue_Approach_and_TODO]]", "[[Daily Log#2026-09-24]]"]
extracted_from: ["[[Thermal_Fatigue_Approach_and_TODO]]"]
tags: [structural, contact, fea, fatigue, interface]
---

# Contact model must match how the part is made

## Working definition (project-specific)
At a dissimilar-material interface the **contact definition can invent or erase the very stress the study is about.** Choose it from how the assembly is physically made, not from the CAD:

| Manufacture | Correct contact | Why |
|---|---|---|
| Over-/insert-moulded | **Bonded** | plastic cast around metal — no interface to slip |
| Press-fit / snap-fit | **Frictional** (real μ) | bonded here **manufactures stress that doesn't exist** |

## Notes / derivations / snippets
- This is the busbar↔plastic interface — the exact location the fatigue is about — so the contact model matters more here than almost anywhere else in the model.
- A wrong bonded assumption on a press-fit joint inflates the interface strain range and therefore the (already uncertain) fatigue estimate.
- Decision needs the real manufacturing method (Open question Q2). Don't assume from geometry.
- Couples with [[Reference temperature is the moulding temp, not ambient]] — both hinge on the same "how was it made" answer.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] Linked to a Knowledge MOC (`[[Solid Mechanics]]`)
- [x] Sources cited

## Atlas Connections
- [[Solid Mechanics]]
- [[Reference temperature is the moulding temp, not ambient]] · [[Thermal_Fatigue_Approach_and_TODO]]
