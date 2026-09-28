---
concept: Reference (stress-free) temperature for insert-moulded parts
origin_project: Busbar G-Bridge Thermal Fatigue
domain: Solid Mechanics
status: budding
created: 2026-09-24
aliases: ["stress-free temperature", "reference temperature moulding"]
sources: ["[[Thermal_Fatigue_Approach_and_TODO]]", "[[Daily Log#2026-09-24]]"]
extracted_from: ["[[Thermal_Fatigue_Approach_and_TODO]]"]
tags: [structural, thermal-stress, reference-temperature, cte, moulding, fatigue]
---

# Reference temperature is the moulding temp, not ambient

## Working definition (project-specific)
Thermal strain is `ε_th = α·(T − T_ref)`, so the **reference (stress-free) temperature** sets the entire ΔT baseline. For an **insert-/over-moulded** busbar-in-plastic assembly, T_ref is the **moulding/cure temperature** — the temperature at which the plastic solidified around the metal with zero stress — **not ambient, and not the Icepak cold instant.** Get it wrong and every thermal strain is off by the whole offset, silently.

## Notes / derivations / snippets
- Set explicitly per body in Static Structural (Geometry → Reference Temperature, or Analysis Settings) — never leave it at the 22 °C default for a moulded assembly.
- Needs a **real number from the moulding process spec**, not an assumption. (Open question Q3 for the G-Bridge.)
- Intuition: the part is already "pre-strained" from cure-down to ambient before any electrical load. Ignoring that under-counts the strain the plastic actually carries.
- Pairs with the contact decision: [[Contact model must match how the part is made]].

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Solid Mechanics]]`)
- [x] Sources cited

## Atlas Connections
- [[Solid Mechanics]] · [[Heat Transfer]]
- [[Material properties required for a fatigue study]] · [[Thermal_Fatigue_Approach_and_TODO]]
