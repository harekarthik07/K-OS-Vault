---
type: template
template_of: eod
tags: [K-OS, template, eod]
---
<%*
// /eod — compiles the day. Save as 03 Projects/<Project>/daily/EOD_<date>_<Project>_<phase>.md
-%>
---
tags: [daily-log, <project-tag>]
date: <% tp.date.now("YYYY-MM-DD") %>
objective: <what today was for>
phase: <Phase N — status>
related: []
---

# EOD — <% tp.date.now("YYYY-MM-DD") %> — <Project> — <phase>

## What we set out to do
## What we actually did
## Results & numbers
| Quantity | Value | Location | Status (verified/assumed/needs-checking) |
|---|---|---|---|
| | | | |

## Decisions made and why

## Learnings & theory
<!-- one line each, tagged so /weekly can harvest. Link an existing page, or write → new -->
- #learning/concept — <insight> → [[ ]]
- #learning/gotcha — <failure mode turned into a rule> → new
- #learning/method — <a check/procedure that worked> → [[ ]]

## Blocked & open
## Next session starts with
## For Claude Code
## Vault links
