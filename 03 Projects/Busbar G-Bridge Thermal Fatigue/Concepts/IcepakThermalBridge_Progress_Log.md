---
tags: [CAE, thermal, ansys, icepak, mechanical, ACT-extension, progress-log]
aliases: [Icepak Mechanical Bridge, thermal bridge ACT, ITB, batch AEDT bridge]
status: active — icepak-to-mechanical link working, fatigue not started
created: 2026-09
project: Busbar G-Bridge Thermal Fatigue
related:
  - "[[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]]"
  - "[[IcepakThermalBridge_Flowchart]]"
  - "[[Thermal_Fatigue_Approach_and_TODO]]"
---

# IcepakThermalBridge — Progress Log

> [!note] Scope of this note
> Covers only the **Icepak → Mechanical temperature transfer** problem: getting a solved Icepak field reliably onto Mechanical bodies as an Imported Body Temperature load. Thermal fatigue itself has not started — see [[Thermal_Fatigue_Approach_and_TODO]].

## 1. Starting point — the native link

Workbench has a built-in mechanism for this: link `Electronics Thermal (Icepak) → Solution` to `Static Structural → Setup`, then in Mechanical add an **Imported Body Temperature** scoped to the target bodies.

**It didn't work.** The `Source Body` dropdown in the Imported Body Temperature's Details pane stayed empty even once:
- the Icepak solve was confirmed converged (contour plot showing 30.5–52.5 °C across all 6 solids in AEDT itself),
- the geometry link was verified correct (shared `A2 → B3` back to the same CAD),
- the solution link was verified correct (`Setup1 : SteadyState` resolved in the Details pane),
- AEDT was fully saved and closed, and the systems were force-refreshed.

Root cause was never confirmed. Working theory going in: something about the design's imported EM-loss coupling (Maxwell feeding Icepak) interfering with the metadata the native link reads. **Decision: stop debugging the native link, build a file-based bridge instead.** → [[Busbar_GBridge_Thermal_Fatigue_Problem_Statement]] for the physics chain this sits inside.

## 2. First working version — direct COM attach

Built a custom **ACT extension**, `IcepakThermalBridge`, adding toolbar buttons inside Mechanical:

- **Icepak side** (`icepak.py`): use AEDT's Fields Reporter (`ExportOnGrid`) to export a temperature grid to `.fld`, convert to CSV.
- **Mechanical side** (`mechanical.py`): create an External Data import, scope it to a body, call `Import()`.
- **Orchestrator** (`main.py`): WinForms mapping dialog (Icepak object name → Mechanical body name), batch loop over all 6 bodies.

This got a **single body (`G_Bridge`) working manually** — confirmed against the Icepak contour.

### Bugs found and fixed in this iteration

| Bug | Symptom | Fix |
|---|---|---|
| `Activator.CreateInstance` spawns a **new empty AEDT process** instead of attaching to the running one | Every field call returned nothing | Switch to `Marshal.GetActiveObject` — *later found this was also wrong, see §3* |
| CSV validator read `parts[3]` unconditionally | In Transient mode column 3 is **Z**, not temperature — validation passed garbage silently | Read the temperature column index from the CSV header |
| Bounding box units hardcoded as `"mm"` | Wrong grid location on any non-mm project | Read `editor.GetModelUnits()` |
| No idempotency | Every re-run stacked another `Imported Body Temperature` object in the tree | Name objects `ITB_<target>`, delete-and-recreate on re-run |
| No void/air rejection | `ExportOnGrid` samples the **bounding box**, not the solid — points outside the object return ambient, dragging mapped values toward ambient via triangulation | Reject rows within tolerance of the configured ambient temperature before writing CSV |
| Transient mode fabricated `temp + 5.0` as a second time point | Would produce a strain range and "fatigue life" that look plausible and mean nothing | Refuse synthetic transient data unless an explicit test-only flag is set |
| Hardcoded `C:\Temp\Icepak_ACT` | Collides across projects/users | Configurable `work_dir`, defaults to `<project>/IcepakBridge` |

## 3. Correction — why COM attach was never going to work

`Marshal.GetActiveObject` (§2's fix) still failed. Root cause, confirmed this time: **AEDT 2022 R2 onward defaults to gRPC and does not register itself in the Windows COM Running Object Table at all.** `Marshal.GetActiveObject` returning `0x800401E3` is not a sandboxing quirk of Workbench — it reproduces from a bare PowerShell process with zero Workbench involvement. There was never a running COM session to attach to.

> [!info] Why not switch to gRPC instead
> gRPC needs **PyAEDT on CPython 3** with `grpcio`. ACT extensions run **IronPython 2.7 on .NET** inside Mechanical. The two runtimes can't share that channel.

**Decision: batch mode.** Neither COM nor gRPC is needed if AEDT is driven headlessly:

```
write a script  →  ansysedt.exe -ng -RunScriptAndExit  →  read the result files back
```

This is slower per invocation (a full AEDT cold start + licence checkout each run) but has **no live-session dependency at all** — it works whether or not AEDT is open, and doesn't care about COM/gRPC registration. To amortise the cold-start cost, discovery (units, setups, solids, bounding boxes) and every mapped object's export now happen in **one batch invocation**, and discovery is cached to disk between runs.

Also added: a **project lock check** before starting a headless run — if the `.aedt` project is open in an interactive AEDT session, batch mode either fails outright or silently opens read-only with no dialog to explain why (`-ng` has no UI). The lock file's owning PID is checked against running processes so a stale lock from a crashed prior run doesn't block a legitimate retry.

## 4. Export method — grid vs. object mesh

Original approach sampled a uniform Cartesian **grid across the bounding box**. Problem: most of a ribbed plastic housing's bounding box is void, so most grid points land in air and return the surrounding fluid temperature — which then drags the mapped body temperature toward ambient in exactly the thin-wall regions that matter for CTE-mismatch strain.

Current approach exports on the **solid's own mesh** via the Fields Calculator (`export_method: "object"` in settings, grid kept as a documented fallback). This contains no air points by construction. Trade-off: a refined solid can produce millions of mesh nodes, far more resolution than the target Mechanical mesh needs, so a decimation step caps the exported point count (`max_source_points`) without materially changing what gets mapped.

## 5. Multi-body correctness — one `ImportedLoadGroup` per target

Found while extending from 1 body to 6: **`ImportExternalDataFiles()` replaces the group's entire file collection.** Sharing one `ImportedLoadGroup` across all 6 bodies meant importing busbar #2 silently detached body #1's CSV — the object stayed in the tree, still scoped, now backed by the wrong file, with **no error reported**. Only the last body processed in a batch ended up correct. Fixed: one `ImportedLoadGroup` per target body, named and matched to its owning import object so `Clear Imports` removes the whole set cleanly.

## 6. Other correctness fixes made along the way

- **Temperature unit auto-detection from the `.fld` header** — `ExportOnGrid`/Fields Calculator write no unit into the file itself; a wrong assumption is silently 273° out (°C vs K). The header is now parsed rather than assumed.
- **Named Selection → body name → GeoBody ID** fallback chain for scoping, because CAD-regenerated body names (`Body-Move/Copy2[1]` style) broke exact-name matching — this is what caused the empty `Source Body` dropdown symptom to *look* solved-but-not-solved during early manual testing.
- **Recursive body walk** through nested assemblies — a flat Geometry → Part → Body traversal missed bodies inside sub-assemblies, which is exactly how the busbar assembly imports.

## Current status

- ✅ Headless batch AEDT export working, no live-session dependency.
- ✅ Object-mesh export (no air contamination) with grid fallback and point decimation.
- ✅ Per-body idempotent import, one `ImportedLoadGroup` each, safe re-runs.
- ✅ Named Selection / body name / GeoBody ID scoping fallback.
- ⏳ **Not yet re-verified end-to-end** with this batch-mode rewrite for all 6 bodies (`AC_Busbar_A/B/C`, `DC_Busbar_A/B`, `G_Bridge`) inside the actual project. Single-body (`G_Bridge`) was verified against the Icepak contour on an earlier iteration of the tool, before the batch-mode rewrite.
- ⏳ Transient export path exists in config (`transient_time_points`) but has not been exercised against a real solved transient Icepak setup — only steady-state has been run.

## Key identifiers

`IcepakThermalBridge` · `ACT extension` · `headless batch AEDT` · `ansysedt.exe -ng -RunScriptAndExit` · `gRPC vs COM` · `Marshal.GetActiveObject` · `Imported Body Temperature` · `ExternalDataFileCollection` · `ImportedLoadGroup` · `Fields Calculator export` · `void rejection` · `ambient rejection` · `Named Selection scoping` · `discovery cache`
