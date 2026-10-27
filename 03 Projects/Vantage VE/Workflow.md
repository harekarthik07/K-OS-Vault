---
type: workflow
project: Vantage VE
---

# Workflow — Vantage VE

> Same K-OS vault rules as [[Raptee Vantage/Workflow|Raptee Vantage]]. This note only records what's **different** for Vantage VE.

Vantage VE is the **R&D / engineering-tools** platform, separate from production
Vantage (QC / verdicts). The daily loop, four buckets (Daily Log → Experiments /
Concepts / Results), `/note` and `/eod` all work the same — see the Raptee Vantage
[[Raptee Vantage/Workflow|Workflow]] for the full agreement.

Differences specific to this project:

- **No live verdicts gate shipping here** — this is design/modeling, not production QC.
  Exception: Powertrain Phase-3 (NVH) does produce PASS/FAIL and reuses the production
  golden-limit machinery; when touching that, the verdict rules apply.
- **Never assume numbers.** On any modeling calc, every physical value is user-supplied;
  only formulae are hardcoded. Ask before using a value. (Standing feedback.)
- **Trust lives in units, validity ranges, and warnings** — not the formula. Every
  calculator states its assumptions and warns when an input crosses the formula's cliff.
- Repo lives outside the main Vantage repo at `..\Raptee-Vantage-VE`; interpreter `py -3.14`.

## Related
[[00 Home]] · [[Powertrain Tool]] · [[Calculator Library]] · [[Raptee Vantage/Workflow|Raptee Vantage Workflow]]
