---
concept: AEDT 2022R2+ uses gRPC not COM — drive it headless
origin_project: Busbar G-Bridge Thermal Fatigue
domain: CAE
status: budding
created: 2026-09-24
aliases: ["Marshal.GetActiveObject fails on AEDT", "headless batch AEDT"]
sources: ["[[IcepakThermalBridge_Progress_Log]]", "[[Daily Log#2026-09-24]]"]
extracted_from: ["[[IcepakThermalBridge_Progress_Log]]"]
tags: [cae, ansys, aedt, automation, tooling, gRPC, com]
---

# AEDT 2022R2+ uses gRPC not COM — drive it headless

## Working definition (project-specific)
From **Ansys Electronics Desktop 2022 R2 onward, AEDT defaults to gRPC and does not register in the Windows COM Running Object Table.** So `Marshal.GetActiveObject` (attach-to-running-instance) returns `0x800401E3 (MK_E_UNAVAILABLE)` — there is no COM session to attach to. This reproduces from a bare PowerShell process, so it is not a Workbench/sandbox quirk.

## Notes / derivations / snippets
- gRPC is *not* a drop-in fix from an ACT extension: gRPC needs **PyAEDT on CPython 3 + grpcio**, but ACT extensions run **IronPython 2.7 on .NET** inside Mechanical — the two runtimes can't share the channel.
- **The robust pattern is headless batch, no live session at all:**
  ```
  write a script → ansysedt.exe -ng -RunScriptAndExit → read the result files back
  ```
  Works whether or not AEDT is open; indifferent to COM/gRPC registration.
- Cost: a full AEDT cold start + licence checkout per invocation. Amortise by doing discovery (units, setups, solids, bboxes) **and** every export in **one** batch call, and cache discovery to disk.
- Add a **project-lock check** first: `-ng` has no UI, so an already-open `.aedt` makes batch mode silently open read-only. Check the lock's owning PID against running processes so a stale lock from a crash doesn't block a retry.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [ ] Linked to a Knowledge MOC (`[[CFD]]`)
- [x] Sources cited

## Atlas Connections
- [[CFD]]
- [[IcepakThermalBridge_Progress_Log]] · [[IcepakThermalBridge_Flowchart]]
