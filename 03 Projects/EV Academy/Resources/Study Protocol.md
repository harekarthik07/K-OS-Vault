---
type: resource
project: EV Academy
tags: [ev-academy, protocol]
---

# EV Academy — Study Protocol

Up: [[00 Home|EV Academy]] · [[Curriculum]]

## Loop
```
/studystart (chat) → recall quiz (3 Qs) → lesson → apply → gate
/studydone  (chat) → one handoff block → paste into Claude Code: "ingest" → vault updated
```

## /studystart — Karthik sends
```
/studystart
Last: <"Next session" line from the last session note>
Time today: <min>
Energy: <high / ok / low>     (low = review-only day)
```

## /studydone — Claude returns exactly this
```
=== EV-ACADEMY HANDOFF ===
date: YYYY-MM-DD
session: NNN
course: EV10X
gate: passed | partial | failed

=== FILE: 03 Projects/EV Academy/daily/YYYY-MM-DD Session NNN.md ===
<full note>

=== FILE: 04 Knowledge/concepts/<Concept Name>.md ===
<full note, K-OS concept format>

=== FILE: 04 Knowledge/gotchas/<Gotcha claim>.md ===
<full note>

=== DAILY LOG ===
- [[YYYY-MM-DD Session NNN]] — <one line> · gate: <status>

=== QUESTIONS ===
- [ ] <open apply task or question>

=== PROGRESS ===
<course> | <lesson> | <gate>
=== END ===
```
No MOC blocks: maps in `04 Knowledge/maps/` build themselves from `domain`.

## Rules
1. One concept per session. Gate before advance.
2. Concepts in Karthik's own words. `status`: seedling = seen once · budding = passed a gate · evergreen = used in ≥2 projects or validated vs data.
3. Every reusable mistake becomes a gotcha, linked from the concept's `## Gotchas`.
4. `domain` must exactly match `_meta/domains.json`.
