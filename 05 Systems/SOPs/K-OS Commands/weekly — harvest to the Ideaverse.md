---
tags: [K-OS, command, SOP]
command: /weekly
status: standing
---
# `/weekly` — harvest to the Ideaverse (Fri/Sat)

**Goal:** convert the week's `#learning` items into durable, linked knowledge. Every task gives theory back.

## Input
Every `#learning` line from this week's EODs and Progress Logs, across all projects.

## Procedure (Claude)
1. **Harvest** — collect all `#learning` items for the week; group by concept.
2. **Dedupe** — if a page exists in the Ideaverse, **update it** (add evidence, a new "where used" backlink, refined validity window). Never duplicate.
3. **Promote** — new pages from **Knowledge_Page_Template**: gotchas → `04 Knowledge/gotchas/`, everything else → `04 Knowledge/concepts/`.
4. **Link** — add each page to its domain map(s) in `04 Knowledge/maps/`, cross-link related concepts, backlink to source EODs/projects.
5. **Mature** — bump status (seedling → budding → evergreen) when a concept is used in ≥2 projects or validated against data.
6. **Backlog** — items too thin go to `index/Knowledge_Backlog.md`; reviewed next week.
7. **Write the weekly review** in `04 Knowledge/weekly/W<nn>_<date>_Review.md` from **Weekly_Review_Template**.

## Output
New/updated concept + gotcha pages, updated maps, and one weekly review note.
