---
concept: Spreading (constriction) resistance
origin_project: ETM For Heatsink and IGBT
domain: Heat Transfer
status: budding
created: 2026-09-15
aliases: ["Spreading resistance", "Constriction resistance", "Yovanovich spreading"]
sources: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]", "[[Daily Log#2026-09-15]]"]
extracted_from: ["[[2026-09-15 MC_HS_ETM_I2 — Thermal Budget & Parameter Derivation (validated)]]"]
tags: [heat-transfer, conduction, spreading-resistance, heatsink, method]
---

# Spreading resistance — heat enters over the source, not the whole base

## Working definition (project-specific)
When heat enters a plate over a **small source footprint** (the IGBT) and must spread to a **larger base** before convecting away, the constriction of the flux lines adds a real, calculable resistance **on top of** 1D conduction `L/(kA)`. Using the full base area in `L/(kA)` and ignoring spreading under-counts `R_hs`.

```
R_hs = L/(k·A_contact)  +  R_spread(Lee/Yovanovich)
     = 0.01313          +  0.01877              = 0.03190 K/W
```

## Notes / derivations / snippets
- **Lee/Yovanovich isoflux circular-source model:** `a=sqrt(A_src/pi)`, `b=sqrt(A_base/pi)`, `eps=a/b`, `tau=t/b`, `Bi=hb/k`; then `lambda=pi+1/(eps·sqrt(pi))`, `phi_c=(tanh(lambda·tau)+lambda/Bi)/(1+(lambda/Bi)tanh(lambda·tau))`, `psi=0.5(1-eps)^1.5·phi_c`, `R_sp=psi/(k·a·sqrt(pi))`.
- **Insensitive to h — no circularity.** With `lambda/Bi ≈ 206 ≫ 1`, phi_c → 1/tanh(lambda·tau); sweeping h 10→150 moves R_sp by only 1.6 %. Using a calibrated h inside a resistance that helps justify that calibration is harmless.
- `Bi ≪ 1` = **adiabatic-edge limit**: the base spreads heat far faster than convection removes it, so R_sp is set by geometry and k alone. **A_base is the only sensitive input** — must come from CAD (guessing 0.024 vs true 0.0343 m² moved R_sp 0.0121 → 0.0188).
- Ties to design: base thickness L trades spreading (thicker helps) vs conduction (thicker hurts) — optimum here 18.1 mm, part is 18 mm.

## Maturity checklist (before promoting to evergreen)
- [x] Definition is generalizable, not project-specific
- [x] At least one equation or diagram
- [ ] Linked to a Knowledge MOC (`[[Heat Transfer]]`)
- [x] Sources cited

## Atlas Connections
- [[Heat Transfer]] · [[Thermal Management]]
- [[Thermal Resistance model of Heatsink With IGBT]] · [[Convection dominates the thermal budget]]
