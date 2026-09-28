---
tags: [K-OS, command, SOP]
command: /start
status: standing
---
# `/start [project]` — kick off a project

**Goal:** stand up a new project folder that plugs straight into the dashboard and the Ideaverse.

## Procedure (Claude)
1. Create `03 Projects/<Project-Name>/` with `daily/`, `Concepts/`, `Experiments/`, `Results/`, `Resources/`.
2. Create the note set (see [[Project_Note_Set_Template]]):
   - `00 Home.md` from `_templates/Project/00 Home.md` — fill `objective:` and the phase **roadmap** (these drive the dashboard mission monitor).
   - `<Project>_Problem_Statement.md` from **Universal_Project_Workflow_Template**, or **CAE_CFD_Project_Preset** for any FEA/CFD project.
   - `<Project>_Progress_Log.md`, `<Project>_Flowchart.md`, `<Project>_Approach_and_TODO.md`.
3. **Before writing Section 4 (Calc & Theory): search the Ideaverse** (`04 Knowledge/`) and link every existing concept/gotcha page that applies. New projects start from what we already know. Mark missing theory `#learning`.
4. Set frontmatter: `type: project_home`, `status: active`, `domain_primary`, `objective`, `current_phase: Phase 1`.
5. Confirm it appears on the [[Dashboard]] mission monitor.

## Gate
Project doesn't advance past Phase 1 until its Phase-1 gate (defined in §2/§5) passes — Sarath drives, Claude verifies.
