---
type: sop
status: active
supersedes: ["05 Daily Workflow.md", "Daily Task Based Workflow.md", "00 Rules.md"]
---

# K-OS Workflow — the one to actually follow

Everything else in this SOPs folder is earlier thinking that led here. This is
the version that matches the real tool (`_tools/kos_capture_hub.py` v3). If
this file and an older one disagree, this one wins.

The core idea hasn't changed since the earlier draft, and it's correct:

> **Log messy while working. Distill clean later.** Don't organize while
> you're thinking — organizing is a different task, done on a different day.

## The loop

```
Work  ──►  Ctrl+Alt+K  ──►  keep working
                │
                ▼ (2nd time you mention a concept)
          card appears in Concepts/
                │
                ▼ (Friday)
          Harvest: Promote / Gist / Discard
                │
                ▼ (promoted ones)
          04 Knowledge/<Domain>/  — permanent, reusable, done
```

You touch three things: the hotkey, the Harvest tab, and (rarely) a new
project folder. Nothing else needs your attention.

---

## Daily — while working

Whenever something happens worth remembering: result, number, question,
realization, dead end.

**`Ctrl+Alt+K`** → type a fragment → **Enter**.

```
Rth junction-to-case measured 0.42, datasheet says 0.38
[[Foster Network]] fits the transient better than Cauer
Q: does TIM thickness matter more than conductivity here?
```

Rules for this step, and only this step:

- **Don't write sentences.** Fragments are correct. This isn't a note, it's a
  timestamp with content attached.
- **Wrap real technical terms** in `[[double brackets]]` — `[[Thermal
  Resistance]]`, `[[IGBT]]`. Don't bracket verbs or filler words. This is the
  only "structure" you owe the system at capture time.
- **Plain Enter is free and instant** (under 200 characters, no API call).
  Use it almost always.
- **Shift+Enter** if you're pasting something long and messy and want it
  formatted — costs a few seconds and an API call. Use it rarely.
- Screenshot of a plot or mesh? Open the main window, `Ctrl+V`, **Append to
  Daily Log**.

At the end of the day, one closing line:
```
next: run case 5 with refined BL mesh, check y+ under 2
```
Tomorrow-you reads that first and knows exactly where to resume. That's the
entire daily discipline. Two minutes, spread across the day.

**You never open a "Knowledge" note during this step.** If it feels like you
should be organizing, stop — that's not today's job.

---

## Weekly — Friday, 15 minutes

The app opens straight to **Harvest** on Fridays if anything's been sitting
more than two weeks. Otherwise open it yourself.

For each concept card:

| Decision | When | What happens |
|---|---|---|
| **Promote** | You'll need this on a *different* project someday | AI rewrites it generic, files it under `04 Knowledge/<Domain>/`, logged in `_meta/concept-registry.md` |
| **Gist** | Only makes sense inside this one project | Stays in `<project>/Concepts/`, marked done, never asked again |
| **Discard** | False positive, not actually a concept | Deleted |

This is the *only* organizing you do. You're triaging things the system
already surfaced — not hunting for what to organize.

A card only exists because you mentioned the same `[[Concept]]` twice. First
mention logs silently. Second mention spawns the card. This kills the flood
of one-off cards that would otherwise bury Friday under noise.

---

## Occasional — starting a new project

```powershell
Copy _templates/Project/  ->  03 Projects/<New Project Name>/
```
Delete the `_*.md` template source files from the copy. Fill in `00 Home.md`
with the goal and `domain_primary`. Set it as **Active Project** in the
sidebar. If the domain doesn't exist yet in `_meta/domains.json`, add five
lines there first.

That's the entire ceremony for a new project. No MOC, no tagging scheme, no
setup beyond this.

---

## Rare — vault maintenance

Every few months, not before: prune stale `Gist` cards nobody's referenced,
tidy `04 Knowledge/_MOCs/`, archive a finished project by setting
`status: archived` in its `00 Home.md`. Skip this until the vault actually
has enough notes for it to matter — a MOC for 12 notes is wasted effort.

---

## The one rule that isn't optional: multi-PC sync

You work from two machines. Obsidian Git auto-commits and auto-pushes on its
own timer on *both*. If you capture on PC A without PC B having pulled first,
the same `Daily Log.md` diverges and you get a merge conflict — this has
already happened once.

**Before a capture session on a PC you haven't touched in a while:**
```powershell
git pull
```
or in Obsidian: `Ctrl+P` → `Git: Pull`. Two seconds. Do it out of habit, the
same way you'd check email before replying to a thread.

If a conflict still happens: open the file in **Source Mode** (`Ctrl+E`),
find the `<<<<<<< HEAD` / `=======` / `>>>>>>> origin/main` block, delete
those three marker lines, keep both sides of content (they're both real
captures, not competing edits), save, `Git: Commit all changes`, `Git: Push`.

---

## What you are never doing

- Writing a "Knowledge" note directly. Everything starts as a fragment in a
  Daily Log or a Concept card. Knowledge is where things *retire to*, not
  where they're born.
- Tagging, YAML wrangling, or manual MOC upkeep on a day-to-day basis. That's
  Year-2 machinery — irrelevant at current note counts, and premature
  structure is why the first version of this SOP collapsed under its own
  planning.
- Deciding what's "important enough" to capture. If it crossed your mind
  during work, `Ctrl+Alt+K` it. The Friday triage is where judgment gets
  applied — not at capture time.

If you ever catch yourself organizing *while* learning, that's the signal to
stop and just keep working. Organizing has its own slot in the week; it
isn't now.
