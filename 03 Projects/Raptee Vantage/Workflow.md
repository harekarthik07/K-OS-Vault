---
type: workflow
project: Raptee Vantage
---

# Workflow — how Claude and this vault work together

> Read this first. It defines where knowledge goes so that neither of us has to re-derive it tomorrow.

This vault is Claude's **RAG / second brain** for Raptee Vantage. `CLAUDE.md` in
the repo is the team-wide, git-committed handbook. This vault is the personal,
evolving layer — it mirrors CLAUDE.md and is meant to grow past it.

---

## The daily loop at a glance

| When | Trigger | What happens |
|---|---|---|
| Starting work on a suite | *(automatic)* | Claude reads the suite note + [[Verdict Engine]] before touching code |
| Something is learned | **`/note`** | one thing captured into the right note, ~10 seconds |
| Investigating a bad verdict | **`verdict-tracer`** agent | traces the evidence chain; findings land via `/note` |
| Adding a QC parameter | **`/add-param`** | walks all five layers so none is missed |
| Deploying | **`/ship`** | pre-flight → build → reload → verify |
| End of day | **`/eod`** | sweeps the day into Concepts / Experiments / Results / Questions |

`/note` is the workhorse. `/eod` is the safety net for what `/note` missed.

---

## The four buckets

Everything we learn lands in exactly one of these. The rule for choosing is
**how long it stays true**:

| Bucket | Holds | Lifespan | Example |
|---|---|---|---|
| **Daily Log** | today's raw work | days | "chased a BB-EOL all-FAIL, turned out to be barcode exclusion" |
| **Experiments/** | one investigation, start to verdict | months | `2026-08-30 BB-EOL all-fail investigation` |
| **Concepts/** | how the system actually works | until the code changes | [[Verdict Engine]], [[BB-EOL]] |
| **Results/** | what shipped and what it changed | permanent record | `2026-08-31 in_verdict bulk toggle shipped` |

Plus [[Questions]] for anything unresolved, and `Resources/` for external links.

**Choosing test:** *"Would I want to be told this before touching the code
tomorrow?"* → Concepts. *"Is this the story of one specific hunt?"* → Experiments.
*"Is this just what happened today?"* → Daily Log.

---

## During the day

When something is learned mid-session, it gets written **immediately** — not at
the end. `/note` exists so this costs nothing.

- **A new landmine** → [[Landmines]], right away. Highest-value notes in the vault
  and the easiest to forget.
- **A decision with a reason** ("we do X because Y") → the relevant Concept note.
- **A correction to an existing note** → fix the note. Never add a contradicting one.
- Everything else → [[Daily Log]].

## End of day — `/eod`

1. Anything durable → promote into `Concepts/`
2. Any completed hunt → write up as an `Experiments/` note
3. Anything shipped → `Results/`
4. Anything still open → [[Questions]]
5. Leave the Daily Log entry in place as the record

`/eod` always shows the triage table before writing. Re-route anything that
landed in the wrong bucket.

## Before touching verdict logic

**Read [[Verdict Engine]] and the relevant suite note first.** Every time, no
command needed. This is the standing rule — the whole reason the vault exists is
so that verdict changes are made with the full picture, not a locally-plausible guess.

For a specific bad verdict, the `verdict-tracer` agent walks the evidence chain.
The debugging order is in [[Verdict Engine]] — cache, then identity, then
exclusion, then golden version, then the parameter, then the code.

---

## What Claude does without being asked

- **Check the vault before answering** anything about verdicts, suites, or limits.
  Prefer what's written here over re-reading 3,000 lines of `fastapi_server.py`.
- **Verify before asserting.** Vault notes are point-in-time. If a note cites a
  file or line number, confirm it still exists before acting on it. If it's stale,
  fix the note.
- **Write landmines as they're found**, without asking permission.
- **Don't over-explain.** If it's already in the vault, link it — don't re-derive it.
- **Ask before changing a Concept note's meaning.** Adding is free; rewriting the
  definition of how the verdict engine works is a decision, not an edit.

## What does NOT go here

- Anything already in `CLAUDE.md` verbatim — link instead of duplicating
- Code structure that's obvious from reading the code
- Conversation-specific chatter with no future value
- Secrets, tokens, credentials

---

## Vault vs. Claude's memory

Two different stores, easy to confuse:

| | Holds | Loaded |
|---|---|---|
| **This vault** | how Vantage works — architecture, verdict logic, landmines | on demand, via MCP |
| **`memory/`** | how to work with sarath — preferences, standing feedback | automatically, every session |

`/eod` updates both when relevant. Don't mirror the vault into memory.

---

## Note templates

Use the standard vault templates — don't invent new shapes:

- `_templates/Project/Concepts/_concept-template.md`
- `_templates/Project/Experiments/_experiment-template.md`
- `_templates/Project/Results/_results-template.md`

`Ctrl+P` → *Templater: Create new note from template*.

Suite notes follow the shape established in [[BB-EOL]]: frontmatter with
`backend` / `db` / `api_prefix`, then data flow → identification → grading logic
→ gotchas → key files → related.

## Naming

- Experiments: `YYYY-MM-DD <short description>` — date first, so they sort
- Results: `YYYY-MM-DD <what shipped>`
- Concepts: the concept's name, no date

## Link liberally

A `[[link]]` to a note that doesn't exist yet is **not an error** — it's a marker
for something worth writing. Obsidian shows these as unresolved; they're a to-do list.

## Related
[[00 Home]] · [[Conventions]] · [[Verdict Engine]] · [[Daily Log]]
