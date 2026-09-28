---
type: gotcha
concept: Unit mismatch in CAE data transfer
domain: CAE
status: seedling
created: 2026-09-28
aliases: ["m vs mm import", "1000x geometry error", "coordinate magnitude assert"]
sources: ["[[IcepakThermalBridge_Progress_Log]]"]
tags: [cae, data-transfer, units, sanity-check, gotcha]
related: ["[[Export fields on the solid mesh, not a bounding-box grid]]", "[[IcepakThermalBridge_Flowchart]]"]
---

# Unit mismatch in CAE data transfer

> [!warning] The rule
> Every tool handoff that carries coordinates or a field can silently apply the wrong length unit. A CSV written in **mm** and read as **m** (or vice-versa) gives a **1000×** geometry error with **no error raised** — the import just lands the data in the wrong place or scale.

## Why it bites
- Exporters/importers rarely store the unit *inside* the file. The reader assumes a unit; if the assumption is wrong the data is off by 10³ and everything downstream (mapping, contours, stress) is quietly wrong.
- Same failure class as temperature-unit ambiguity (°C read as K is 273° out) — see the `.fld` header auto-detect fix in [[IcepakThermalBridge_Progress_Log]].

## The check (the fix)
On every import step, **assert the coordinate magnitude against the declared length unit** before using the data:
- Compare the imported bounding-box extent to the model's known size.
- If they differ by ~1000× (or ~0.001×), stop and warn — do not silently rescale.

## Where used
- [[IcepakThermalBridge_Flowchart]] — import step (backlog assert, Busbar G-Bridge tool)
- Section 5 CAE verification spine: "Unit and data-transfer sanity"

## Status note
`seedling` — rule captured; the automatic assert in `IcepakThermalBridge` import is still on the tool backlog (code lives outside the vault at `D:\Hare Karthik\Ansys\_ACT\IcepakThermalBridge\`).

---
`unit mismatch` · `mm vs m` · `1000x` · `coordinate magnitude assert` · `data-transfer sanity` · `CAE handoff`
