---
concept: Powertrain Tool
project: Vantage VE
domain: Motor Control
status: incubating
created: 2026-10-10
sources: [[[Daily Log#2026-10-10]]]
extracted_from: []
---

# Powertrain Tool

## Working definition (project-specific)
A Vantage VE tool that reads a dyno torque/RPM log + a bike spec sheet and produces
the standard powertrain views. Two unrelated families, built in phases.

The powertrain chain: **Battery → Inverter (VCU) → Motor → fixed reduction → chain/belt → Wheel.**
Likely single-speed (one fixed gear ratio, no shifting) — so "gear ratio" is one
constant, not a gearbox of ratios.

## Phase 1 — Performance & curves (build first; teaches the concepts)
Input: one dyno torque/RPM log + one bike spec sheet.

| Output | Answers | Built from |
|---|---|---|
| Torque curve | force vs motor RPM | dyno log (direct) |
| Power curve | P = torque × 2π·RPM/60 | dyno log (derived) |
| Wheel force / tractive effort | torque at the wheel | torque × gear ratio ÷ wheel radius |
| Road-load & top speed | where push = drag | spec: mass, CD, frontal area, Crr |

Hardcoded formulae only: `P = T·ω`, `F_drag = ½·ρ·CD·A·v²`, `F_roll = Crr·m·g`.
Top speed = where tractive effort curve crosses the road-load curve.
Every number (CD, A, Crr, air density, gear ratio, wheel radius, mass) is user-supplied.
Refuse to run on blanks. **No assumed values.**

## Phase 3 — NVH / gear health (later; reuses QC golden-limit machinery)
Input: vibration/acoustic log. Output: gear OK / suspect (PASS/FAIL).

| Metric | Catches | Plain idea |
|---|---|---|
| RMS level | overall loudness | average energy of the shaking |
| Crest factor (peak ÷ RMS) | a single bad tooth / bearing | smooth hum = low crest; periodic bang = spike |
| Gear-mesh frequency (RPM × teeth) | gear whine | a peak right at that frequency |
| Order tracking | separates gear noise from motor noise | lock analysis to shaft rotation, not clock time |

Same rule as production suites: **any fail → fail**, golden limits, Teams notify.

## The concept glossary (plain words)
- **Torque** = twisting force. **Power** = torque × speed (rate of work).
- **Gear ratio** = motor turns per wheel turn; short gear = more grunt, lower top speed.
- **CD** = how slippery through air. **Crr** = tyre rolling drag. Both are road-load terms.
- **Crest factor** = peak ÷ RMS of a vibration signal; a defect detector.

## Notes / derivations / snippets
- Phase-1 math (torque/power, drag, gear ratio) overlaps the [[Calculator Library]]
  Engineering-Mechanics calcs — reuse those components, don't re-derive.

## Promotion checklist (before flipping status: promoted)
- [ ] Definition is generalizable, not project-specific
- [ ] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Motor Control]]`)
- [ ] Sources cited

## Atlas Connections
- [[Motor Control]]
- [[Vibrations]]
- [[Calculator Library]]
