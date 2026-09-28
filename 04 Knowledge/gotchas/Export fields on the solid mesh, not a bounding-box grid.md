---
concept: Export fields on the solid mesh, not a bounding-box grid
origin_project: Busbar G-Bridge Thermal Fatigue
domain: CAE
status: budding
created: 2026-09-24
aliases: ["void contamination in field export", "object mesh export vs grid export"]
sources: ["[[IcepakThermalBridge_Progress_Log]]", "[[IcepakThermalBridge_Flowchart]]"]
extracted_from: ["[[IcepakThermalBridge_Progress_Log]]"]
tags: [cae, field-export, mapping, icepak, mesh, tooling]
---

# Export fields on the solid mesh, not a bounding-box grid

## Working definition (project-specific)
When exporting a solved field (temperature) to map onto another solver's body, **export on the solid's own mesh**, not on a uniform Cartesian grid over its bounding box. Most of a ribbed/thin-walled part's bounding box is **void** — grid points there return the surrounding fluid temperature, and triangulation drags mapped body values toward ambient in exactly the thin-wall regions that dominate CTE-mismatch strain.

## Notes / derivations / snippets
- Object-mesh export (Fields Calculator, `export_method: "object"`) contains **no air points by construction**.
- Grid export (`ExportOnGrid` over the bbox) is kept only as a documented fallback, and then needs **ambient rejection** — drop rows within a tolerance of the configured ambient before writing the CSV.
- Trade-off: a refined solid mesh can produce millions of nodes — far more than the target Mechanical mesh needs — so **decimate** to a `max_source_points` cap; it doesn't materially change what maps.
- General principle for any solver-to-solver field handoff: sample where the material *is*, not where its bounding box is.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]] · [[Heat Transfer]]
- [[IcepakThermalBridge_Progress_Log]] · [[IcepakThermalBridge_Flowchart]]
