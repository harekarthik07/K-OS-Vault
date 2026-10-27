---
concept: Calculator Library
project: Vantage VE
domain: Solid Mechanics
status: incubating
created: 2026-10-10
sources: [[[Daily Log#2026-10-10]]]
extracted_from: []
---

# Calculator Library

## Working definition (project-specific)
A Vantage VE tool = **one calculator shell, many calculators**, subject-wise across
Engineering Mechanics, Machine Design, Heat Transfer, Fluid Mechanics. **Not a
textbook** — the "guide" is a short note attached to each calculator (assumptions +
the one formula + a line of intuition).

## One shell, registry-driven
Each calculator = one registry row (like `master_params.json` for physics):

| Field | Example (cantilever, UDL) |
|---|---|
| Name / category | "Cantilever – UDL" / Engineering Mechanics |
| Inputs | L, w, E, I |
| Formula (hardcoded) | δ_max = wL⁴/8EI, M_max = wL²/2 |
| Diagram | beam + arrows + BMD/SFD |
| Assumptions & valid range | small deflection, linear-elastic, prismatic |
| Reference | textbook / standard |

Adding a calculator = adding a data row + its formula. Not a new app per subject.

## The hard 90% (where trust lives — not the formula)
1. **Units** — SI internally, units shown on every input/output.
2. **Validity range** — warn when an input crosses the formula's cliff
   (small-deflection, Re < ~2300, fully-developed, steady-state).
3. **Sign & convention** — sagging vs hogging, up vs down; state once, draw it.
4. **No assumed numbers** — formula hardcoded, values user-supplied, refuse blanks.

## Audience = a view toggle, not a second app
"Both" (engineers + students) is served by one **"Show working steps"** toggle:
- collapsed → engineer mode: inputs → answer → assumptions/warnings.
- expanded → student mode: same calc, prints each substitution step + intuition.

Build engineer-first; the student view is a free expand. **Hold this line** — a
separate "student site" doubles cost.

## Notes / derivations / snippets
- The shell is lifted out of [[Powertrain Tool]] Phase 1 (the inputs → formula →
  plot + assumptions pattern), not designed separately.
- Seed set (5): cantilever UDL + UVL, Reynolds number, shaft diameter, one heat-transfer case.

## Promotion checklist (before flipping status: promoted)
- [ ] Definition is generalizable, not project-specific
- [ ] At least one equation or diagram
- [ ] Linked to a Knowledge MOC
- [ ] Sources cited

## Atlas Connections
- [[Solid Mechanics]]
- [[Heat Transfer]]
- [[CFD]]
- [[Powertrain Tool]]
