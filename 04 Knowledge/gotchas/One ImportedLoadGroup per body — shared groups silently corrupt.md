---
concept: One ImportedLoadGroup per body
origin_project: Busbar G-Bridge Thermal Fatigue
domain: CAE
status: budding
created: 2026-09-24
aliases: ["ImportExternalDataFiles replaces the collection", "shared ImportedLoadGroup bug"]
sources: ["[[IcepakThermalBridge_Progress_Log]]", "[[IcepakThermalBridge_Flowchart]]"]
extracted_from: ["[[IcepakThermalBridge_Progress_Log]]"]
tags: [cae, ansys, mechanical, act-extension, imported-load, tooling]
---

# One ImportedLoadGroup per body — shared groups silently corrupt

## Working definition (project-specific)
In Ansys Mechanical, `ImportExternalDataFiles()` **replaces the entire file collection** of an `ImportedLoadGroup`. So sharing one group across multiple bodies means importing body #2 silently detaches body #1's CSV — body #1's object stays in the tree, still scoped, now backed by the **wrong file, with no error raised.** Only the last body in a batch ends up correct.

## Notes / derivations / snippets
- Fix: **one `ImportedLoadGroup` per target body**, named and matched to its owning import object (`ITB_<target>`), so cleanup removes each set cleanly.
- This is a silent-correctness failure — it produces plausible, wrong results. The class of bug to fear most in a mapping tool.
- Related scoping robustness: resolve the target body by **Named Selection → body name → GeoBody ID** fallback, because CAD-regenerated names (`Body-Move/Copy2[1]`) break exact-name matching and *look* solved-but-not-solved.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] Linked to a Knowledge MOC (`[[Solid Mechanics]]`)
- [x] Sources cited

## Atlas Connections
- [[Solid Mechanics]]
- [[IcepakThermalBridge_Progress_Log]] · [[IcepakThermalBridge_Flowchart]]
