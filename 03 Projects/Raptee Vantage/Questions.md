---
type: questions
project: Raptee Vantage
---

# Open Questions

- [ ] Q1 — Is `dyno_tests.db` at repo root actually dead? CLAUDE.md flags it as likely stale but unverified. Confirm before deleting.
- [ ] Q2 — Should Dyno move to the golden-version model like BB-EOL / VCH-EOL, or is the envelope-table approach deliberate?
- [ ] Q3 — Dyno has no `in_verdict` equivalent. Should test/dummy dyno runs be excludable the same way?
- [ ] Q5 — Why do `Raptee-Backend` / `Raptee-Intake` restart counts keep climbing (14→18 and 13→17 over 2026-10-27) when releases only restart the frontend? Check `pm2 logs Raptee-Backend`.
- [ ] Q6 — Dyno Motor ΔT batch average climbs from 46 °C (S1) to 60 °C (S13, over the 59.4 °C limit). Part change, assembly, or rig? Needs input from the line. See [[2026-10-27 Dyno batch trend analysis]].
- [ ] Q7 — 8 dyno files have unreadable bike numbers (`2026_08_27-45_01-BK` … `45_07`, `2026_08_29-3.3-BK`). Rename the files, or teach the parser? Fix at intake if they're test files.
- [ ] Q8 — Should `_dyno_verdict_for_bike` get the wrong-procedure check, so `/api/bike-verdict` / Fleet agree with the Dyno Overview? (Verdict change — plan first.)

# Answered

- [x] Q4 — `_dyno_verdict_for_bike` only checks `TIME_S = 120`. Is one time slice enough? **Yes, deliberately.** 60 s is still inside the thermal response, so it gives false results; don't reintroduce a multi-snapshot scan.
