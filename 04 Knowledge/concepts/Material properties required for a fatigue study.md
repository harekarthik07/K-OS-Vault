---
type: concept
concept: Material properties required for a fatigue study
domain: Solid Mechanics
status: seedling
created: 2026-09-24
aliases: ["fatigue material properties", "properties for thermal fatigue"]
tags: [solid-mechanics, fatigue, material-properties, cte, modulus, S-N]
---

# Material properties required for a fatigue study

A thermal-fatigue study is only as trustworthy as its inputs. What each property is for, and why it bites if wrong:

## Thermal side (drives the temperature field)
| Property | Symbol | Why it's needed |
|---|---|---|
| Thermal conductivity | `k` | sets the temperature field magnitude and gradients. Cast 383.0 Al (~96 W/m·K) vs copper (~380) changes everything downstream |
| Specific heat, density | `cp`, `ρ` | transient response — how fast the assembly heats/cools over the duty cycle |

## Elastic side (converts ΔT into stress/strain)
| Property | Symbol | Why it's needed |
|---|---|---|
| Young's modulus | `E(T)` | stiffness — turns strain into stress. **Temperature-dependent** for polymers |
| Poisson's ratio | `ν` | lateral coupling; mild temperature dependence |
| **Coefficient of thermal expansion** | `α(T)` | **the driver.** Thermal strain `ε_th = α·(T − T_ref)`. The Al–plastic **α mismatch** is the entire fatigue mechanism |
| Reference / stress-free temperature | `T_ref` | the ΔT baseline — moulding temp for insert-moulded parts, see [[Reference temperature is the moulding temp, not ambient]] |

## Strength & regime boundaries (validity checks)
| Property | Why it's needed |
|---|---|
| Yield / ultimate strength | is the response still linear-elastic, or is there plasticity? |
| **Glass transition `Tg`** | the regime switch for polymers (~110–125 °C for ABS+PC). Below → linear elastic OK; near/above → viscoelastic + temp-dependent props ([[Creep and stress relaxation]]) |

## Fatigue data (the life calculation itself)
| Property | Why it's needed |
|---|---|
| **S-N or Δε–N curve at operating temperature** | the actual life vs load relationship. Room-temp curves over-predict — [[Temperature-dependent fatigue of polymers]] |
| Mean-stress correction | tensile mean stress shortens life (Goodman/SWT) |
| (if hot/sustained) creep compliance / relaxation modulus (Prony) | for the viscoelastic model |

> [!warning] Metals-only shortcut does not apply
> Ansys's built-in Fatigue Tool uses **Coffin-Manson coefficients calibrated for metals.** ABS+PC needs its own S-N/Δε–N curve at temperature, or the study must be stated as **comparative-only** (design A vs B strain range), not an absolute cycle count.

## Sourcing
Supplier datasheet (temperature-dependent E, CTE, S-N), **CAMPUS / Material Data Center** for the exact grade, and the **moulding process spec** for `T_ref`.

## Related
- [[Fatigue — cyclic damage and life]] · [[Temperature-dependent fatigue of polymers]] · [[Creep and stress relaxation]]
- [[Reference temperature is the moulding temp, not ambient]] · [[Solid Mechanics]] · [[Thermal_Fatigue_Approach_and_TODO]]
