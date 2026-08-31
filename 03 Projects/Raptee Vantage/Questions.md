---
type: questions
project: Raptee Vantage
---

# Open Questions

- [ ] Q1 — Is `dyno_tests.db` at repo root actually dead? CLAUDE.md flags it as likely stale but unverified. Confirm before deleting.
- [ ] Q2 — Should Dyno move to the golden-version model like BB-EOL / VCH-EOL, or is the envelope-table approach deliberate?
- [ ] Q3 — Dyno has no `in_verdict` equivalent. Should test/dummy dyno runs be excludable the same way?
- [ ] Q4 — `_dyno_verdict_for_bike` only checks `TIME_S = 120`. Is a single time slice enough, or should the whole envelope be swept?

# Answered

-
