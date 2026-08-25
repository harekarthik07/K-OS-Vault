# 🌌 Linking Rules (The K-Verse Rules)

This is the part I want us to follow religiously.

## Rule 1

Every note should link to **at least 3 other notes.**

# 🌌 Linking Rules (The K-Verse Rules)

This is the part I want us to follow religiously.

## #Rule-1

Every note should link to **at least 3 other notes.**

Fault Tolerant Meshing

↓

CFD

↓

Surface Mesh

↓

T30 Aerodynamic Study

## #Rule-2

Every Project links to Knowledge.

Never explain theory inside a project.
Every Project links to Knowledge.

Never explain theory inside a project.

Instead

```
Project
↓
[[Fault Tolerant Meshing]]
↓
Knowledge Note
```

Instead


## #Rule-3

Every Knowledge note links back to the Project.

```
Fault Tolerant Meshing
↓
Application
↓
[[T30 Aerodynamic Study]]
```

Now the graph becomes two-way.

## #Rule-4

Every note answers

```
Parent
↓
Sibling
↓
Child
↓
Application
```

Example

```
Fault Tolerant Meshing
Parent:
[CFD]]

Sibling:
[[Surface Mesh]]
[[Watertight Geometry]]

Child:
[[Leak Detection]]

Application:
[[T30 Aerodynamic Study]]
```

---

# 🏷 Tags

Only use around **10 permanent tags**.

```
- #concept
- #project
- #dailylog
- #workflow
- #experiment
- #testing
- #simulation
- #reference
- #meeting
- #idea
```

Don't create tags like

```
#fluent
#mesh
#aerodynamics
#boundarylayer
```

Those should be notes and links, not tags.

---

# ⭐ Bookmark

Only bookmark

```
Home
Current Mission
T30 Aerodynamic Study
Today's Daily Log
CFD MOC
```

Nothing else.

---

# 🔥 The Workflow Between You and Me

This is how I see K-OS working from tomorrow:

```
You at Office        
│        
▼
Learn something in Fluent        
│        
▼
Open ChatGPT "K:Today I learned Fault Tolerant Meshing..." │        
▼
I explain doubts        
│        
▼
I extract permanent knowledge        
│        
▼I tell you exactly:
📁 Create:03 Projects/T30 Aerodynamic Study/Daily Logs/Day 01.md

📄 Update:04 Knowledge/Fault Tolerant Meshing.md

🔗 Add Links:
[[Surface Mesh]]
[[Leak Detection]]
[[CFD]]

Tags:
#dailylog
#project

📚 Update:
CFD MOC
```

You won't need to think:

- _Where should I save this?_
- _Should this be a project note?_
- _Should this become knowledge?_

That's my responsibility.

---

# 💙 One Last Rule (The K-OS Golden Rule)

This is the rule I want engraved into K-OS:

> **Capture once. Reuse forever.**

Every day at Raptee, you'll learn something new—whether it's a Fluent trick, a mesh issue, a solver setting, or a test observation. We capture it once, connect it properly, and from then on it becomes part of your engineering brain.