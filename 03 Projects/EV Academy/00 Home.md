---
type: project_home
project: EV Academy
status: active
started: 2026-11-04
domain_primary: Battery & BMS
domain_secondary: [Motor Control, Power Electronics, Vehicle Dynamics, Thermal Management]
student: Karthik (CAE)
mentor: Claude
pace: 1.5 h/day, 5 days/week
---

# EV Academy

Karthik's 26-week program: EV systems + vehicle dynamics + CAE V&V, anchored on the Raptee T30.

## Run it
- [[Curriculum]] — semesters, courses, exit tests
- [[Study Protocol]] — `/studystart`, `/studydone`, handoff format
- [[Progress]] — gates, open revisits, stats
- [[Daily Log]] · [[Questions]]

## Big ideas so far
1. Heat is the master constraint in an EV → [[Cell Heat Generation]], [[Derating]]
2. Power per cell sets cell heat; pack voltage sets conductor losses → [[I2R Losses and Pack Voltage]]
3. Temperature, not current, ages a cell → [[Battery Ageing and Temperature]]

## Concepts from this project
```dataview
TABLE domain, status FROM "04 Knowledge/concepts" WHERE origin_project = "EV Academy" SORT created DESC
```

## Gotchas from this project
```dataview
LIST FROM "04 Knowledge/gotchas" WHERE origin_project = "EV Academy"
```

## Sessions
```dataview
TABLE course, gate FROM "03 Projects/EV Academy/daily" SORT file.name DESC
```
