---
type: dashboard
cssclasses:
  - dashboard
---

# 🧭 K-OS

**[[Inbox]]** · **[[K-OS Protocol]]** · **[[Workflows]]** · `03 Projects` · `04 Knowledge`

---

## 🔥 Now

> What's actually in flight. If it's not here, it's not this week's problem.

```dataview
TABLE WITHOUT ID
  file.link AS "Project",
  current_phase AS "Phase",
  domain_primary AS "Domain"
FROM "03 Projects"
WHERE type = "project_home" AND status = "active"
SORT file.mtime DESC
```

## ✅ Next Actions

```tasks
not done
path includes 03 Projects
group by folder
hide task count
short mode
```

---

<div></div>

> [!question]- ❓ Open Questions
> ```dataview
> TASK
> FROM "03 Projects"
> WHERE !completed AND contains(file.name, "Questions")
> ```

> [!todo]- 📥 Inbox — needs filing
> ```dataview
> LIST file.mtime
> FROM "Inbox"
> WHERE !contains(file.folder, "_archive")
> SORT file.mtime DESC
> ```

> [!abstract]- 🧠 Incubating Concepts
> ```dataview
> LIST
> FROM "03 Projects"
> WHERE status = "incubating"
> GROUP BY file.folder
> ```

> [!info]- 🕒 Recent Activity — 7 days
> ```dataview
> TABLE WITHOUT ID file.link AS "Note", file.folder AS "Where"
> FROM "03 Projects" OR "04 Knowledge"
> WHERE file.mtime >= date(today) - dur(7 days)
> SORT file.mtime DESC
> LIMIT 15
> ```

---

## 📚 Knowledge

| Domain | MOC |
|---|---|
| Power Electronics | [[Power Electronics]] |
| Thermal Management | [[Thermal Management]] |
| Heat Transfer | [[Heat Transfer]] |
| CFD | [[CFD]] |
| Solid Mechanics | [[Solid Mechanics]] |

> [!example]- All knowledge notes by domain
> ```dataview
> LIST
> FROM "04 Knowledge" AND -"04 Knowledge/_MOCs"
> GROUP BY file.folder
> ```

---

## 🗂 Projects

```dataview
LIST
FROM "03 Projects"
WHERE type = "project_home"
SORT file.name ASC
```

> [!note]- Systems · Resources · Vault map
> **Systems**
> ```dataview
> LIST FROM "05 Systems"
> ```
>
> **Resources**
> ```dataview
> LIST FROM "06 Resources"
> ```
>
> **Vault map**
>
> | Bucket | Holds |
> |---|---|
> | `03 Projects/` | active work, one folder each |
> | `04 Knowledge/` | durable domain knowledge + MOCs |
> | `05 Systems/` | SOPs, workflows |
> | `06 Resources/` | external refs, papers |
> | `08 AI/` | BMO profiles, AI config |
> | `Inbox/` | raw captures pending triage |
> | `_templates/` · `_meta/` | project templates, domain routing |
