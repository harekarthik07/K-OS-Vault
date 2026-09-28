---
type: dashboard
cssclasses:
  - dashboard
---

# 🧭 K-OS

**[[Inbox]]** · **[[K-OS Protocol]]** · **[[Workflows]]** · `03 Projects` · `04 Knowledge`

```dataviewjs
const tasks = dv.pages('"03 Projects"').file.tasks.where(t => !t.completed);
const open = tasks.length;
const today = dv.date("today");
const week = tasks.where(t => t.due && t.due <= today.plus({ days: 7 })).length;
const overdue = tasks.where(t => t.due && t.due < today).length;
const active = dv.pages('"03 Projects"').where(p => p.type == "project_home" && p.status == "active").length;
const concepts = dv.pages('"03 Projects"').where(p => p.status == "incubating").length;

const stats = [
  ["Active projects", active, ""],
  ["Open tasks", open, ""],
  ["Due ≤ 7 days", week, "warn"],
  ["Overdue", overdue, overdue > 0 ? "bad" : "good"],
  ["Incubating", concepts, ""],
];

const strip = dv.el("div", "", { cls: "dash-stats" });
strip.innerHTML = stats.map(([label, val, tone]) =>
  `<div class="ds-tile ${tone}"><div class="ds-val">${val}</div><div class="ds-label">${label}</div></div>`
).join("");
```

---

## 🎯 Missions — objective → milestones

> One card per active project: its objective, every milestone (phase) with live progress, and the next open task. Click a title to open the project.

```dataviewjs
const proj = dv.pages('"03 Projects"')
  .where(p => p.type == "project_home" && p.status == "active")
  .sort(p => p.file.name, 'asc');

const wrap = dv.el("div", "", { cls: "dash-missions" });
let html = "";

for (const p of proj) {
  const name = p.project ?? p.file.folder.split("/").pop();
  const obj  = p.objective ?? "—";

  // parse phase (milestone) headers + count checkboxes in each block
  const txt = await dv.io.load(p.file.path);
  const re = /^###\s+(✅|🟢|⚪)\s+Phase\s+(\d+)\s+—\s+(.+?)\s*$/gm;
  let heads = [], m;
  while ((m = re.exec(txt)) !== null) heads.push({ st: m[1], num: m[2], name: m[3], idx: m.index });

  let dAll = 0, tAll = 0;
  const chips = heads.map((h, i) => {
    const end = (i + 1 < heads.length) ? heads[i + 1].idx : txt.length;
    const block = txt.slice(h.idx, end);
    const done = (block.match(/- \[x\]/gi) || []).length;
    const total = (block.match(/- \[[ x]\]/gi) || []).length;
    dAll += done; tAll += total;
    const pct = total ? Math.round(done / total * 100) : (h.st === "✅" ? 100 : 0);
    const cls = h.st === "✅" ? "done" : (h.st === "🟢" ? "active" : "todo");
    const tip = `Phase ${h.num} — ${h.name}` + (total ? ` (${done}/${total})` : "");
    const inner = h.st === "✅" ? "✓" : (cls === "active" && total ? `${pct}%` : "");
    return `<span class="chip ${cls}" title="${tip.replace(/"/g,'&quot;')}">P${h.num}<i>${inner}</i></span>`;
  }).join("");

  const pctAll = tAll ? Math.round(dAll / tAll * 100) : 0;
  const nextTask = dv.pages(`"${p.file.folder}"`).file.tasks.where(t => !t.completed).first();
  const next = nextTask ? nextTask.text.replace(/[✅📅🔼⏫🔽🔺#].*$/, "").trim() : "all clear ✓";

  const eod = dv.pages(`"${p.file.folder}"`)
    .where(pg => pg.file.name.startsWith("EOD"))
    .sort(pg => pg.file.name, 'desc').first();
  const eodHtml = eod
    ? `<a class="internal-link" href="${eod.file.path}" data-href="${eod.file.path}">${eod.file.name}</a>`
    : "none yet";

  html += `
    <div class="mission">
      <div class="m-head">
        <a class="m-title internal-link" href="${p.file.path}" data-href="${p.file.path}">${name}</a>
        <span class="m-phase">${p.current_phase ?? "—"}</span>
      </div>
      <div class="m-obj">🎯 ${obj}</div>
      <div class="m-chips">${chips || '<span class="chip todo">no milestones</span>'}</div>
      <div class="m-foot">
        <div class="m-bar"><div class="m-fill" style="width:${pctAll}%"></div></div>
        <span class="m-pct">${dAll}/${tAll} · ${pctAll}%</span>
      </div>
      <div class="m-next">▸ ${next}</div>
      <div class="m-eod">🗓 latest EOD: ${eodHtml}</div>
    </div>`;
}
wrap.innerHTML = html;
```

> [!info]- ℹ️ How tasks flow — what goes in and out
> **Source of truth:** every task is a literal `- [ ]` checkbox under a **Phase (= milestone)** in a project's `00 Home`. Nothing is hidden — open the file and you see it.
>
> **Adding a task — three ways, same result:**
> - **Manual:** type `- [ ] do X 📅 2026-10-05 ⏫` under that phase's `**Tasks:**` in the project's `00 Home` (or in the Daily Log for loose items).
> - **Semi-auto:** the **⚡ Quick Add** form below — pick project + file + priority + due, hit Enter. It writes the checkbox for you.
> - **Via Claude:** ask me; I place it under the right phase and can define new milestones/objectives too.
>
> **Priorities:** `🔺` highest · `⏫` high · `🔼` medium · `🔽` low. **Due:** `📅 YYYY-MM-DD`.
>
> **Completing (OUT):** click the checkbox or press `Ctrl+L`. The milestone chip %, the mission bar, and the stat strip all recompute live.
>
> **Milestones:** a phase flips `⚪→🟢→✅` as you edit its heading; the chip colour and % follow. When a phase completes, replace its task list with a one-line outcome + link.

## ⚡ Quick Add Task

```dataviewjs
const activeProjects = dv.pages('"03 Projects"')
  .where(p => p.type == "project_home" && p.status == "active")
  .sort(p => p.project || p.file.folder);

const container = dv.el("div", "", { cls: "dash-quick-add" });

container.createEl("div", { cls: "dqa-header", text: "⚡ Quick Add Task to Project" });

const formRow = container.createEl("div", { cls: "dqa-row" });

// 1. Project Selector
const selProj = formRow.createEl("select", { cls: "dqa-select-proj" });
for (const p of activeProjects) {
  const name = p.project ?? p.file.folder.split("/").pop();
  selProj.createEl("option", { text: name, value: p.file.folder });
}

// 2. Target File
const selDest = formRow.createEl("select", { cls: "dqa-select-dest" });
selDest.createEl("option", { text: "Roadmap (00 Home)", value: "00 Home.md" });
selDest.createEl("option", { text: "Daily Log", value: "Daily Log.md" });

// 3. Task text input
const taskInput = formRow.createEl("input", {
  type: "text",
  placeholder: "What needs to be done? (Hit Enter to save)",
  cls: "dqa-input-text"
});

// 4. Priority selector
const selPriority = formRow.createEl("select", { cls: "dqa-select-prio" });
selPriority.createEl("option", { text: "Priority: Normal", value: "" });
selPriority.createEl("option", { text: "Priority: ⏫ High", value: " ⏫" });
selPriority.createEl("option", { text: "Priority: 🔼 Medium", value: " 🔼" });
selPriority.createEl("option", { text: "Priority: 🔽 Low", value: " 🔽" });

// 5. Due date picker
const dateInput = formRow.createEl("input", { type: "date", cls: "dqa-input-date" });

// 6. Submit button
const submitBtn = formRow.createEl("button", { text: "➕ Add Task", cls: "dqa-btn" });

taskInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    submitBtn.click();
  }
});

submitBtn.onclick = async () => {
  const desc = taskInput.value.trim();
  if (!desc) {
    new Notice("⚠️ Please enter a task description first.");
    return;
  }
  const folder = selProj.value;
  const fileName = selDest.value;
  const filePath = `${folder}/${fileName}`;
  const file = app.vault.getAbstractFileByPath(filePath);

  if (!file) {
    new Notice(`❌ Could not locate ${filePath}`);
    return;
  }

  let taskText = `- [ ] ${desc}`;
  if (selPriority.value) {
    taskText += selPriority.value;
  }
  if (dateInput.value) {
    taskText += ` 📅 ${dateInput.value}`;
  }

  try {
    const content = await app.vault.read(file);
    let updated = "";
    if (fileName === "00 Home.md") {
      if (content.includes("**Tasks:**")) {
        updated = content.replace("**Tasks:**", `**Tasks:**\n${taskText}`);
      } else {
        updated = content + `\n\n### Tasks\n${taskText}\n`;
      }
    } else {
      const todayStr = moment().format("YYYY-MM-DD");
      if (content.includes(`## ${todayStr}`)) {
        updated = content.replace(`## ${todayStr}`, `## ${todayStr}\n${taskText}`);
      } else {
        updated = content + `\n\n## ${todayStr}\n${taskText}\n`;
      }
    }

    await app.vault.modify(file, updated);
    new Notice(`✅ Task added to ${selProj.options[selProj.selectedIndex].text}!`);
    taskInput.value = "";
    dateInput.value = "";
    selPriority.selectedIndex = 0;
  } catch (err) {
    new Notice(`❌ Failed to save task: ${err.message}`);
    console.error(err);
  }
};
```

## ✅ Task Tracker

> [!tip]- 💡 Task Actions & Shortcuts
> - **Complete:** Click the checkbox `[ ]` directly to mark done.
> - **Edit / Delete / Re-prioritize:** Hover over any task line and click the ✏️ **pencil icon** (or right-click → **Edit Task**). You can edit the text, set priority, change due date, or delete the task completely.
> - **Cancel:** In the edit popup, set the status to `Cancelled [-]`.

> [!danger]+ 🚨 Overdue & Today
> ```tasks
> not done
> path includes 03 Projects
> due before tomorrow
> sort by due
> sort by priority
> group by folder
> ```

> [!warning]+ ⏳ Due in Next 7 Days
> ```tasks
> not done
> path includes 03 Projects
> due after today
> due before in 8 days
> sort by due
> sort by priority
> group by folder
> ```

> [!note]+ 📋 All Open Tasks by Project
> ```tasks
> not done
> path includes 03 Projects
> sort by due
> sort by priority
> group by folder
> ```

> [!success]- 🏁 Recently Completed (Last 7 Days)
> ```tasks
> done
> path includes 03 Projects
> done after 7 days ago
> sort by done reverse
> group by folder
> ```

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

## 🧠 Ideaverse — knowledge

> The theory the projects consume and give back. **Maps** are the domain entry points; **concepts** are atomic pages (seedling → budding → evergreen); **gotchas** are bugs turned into rules; **weekly** holds the harvest notes. Promotion happens in `/weekly`.

| Domain map | Maturity legend |
|---|---|
| [[Power Electronics]] · [[Thermal Management]] · [[Heat Transfer]] · [[CFD]] · [[Solid Mechanics]] | 🌱 seedling · 🌿 budding · 🌳 evergreen |

> [!warning]- ⚠️ Gotchas — check these at every gate
> ```dataview
> LIST
> FROM "04 Knowledge/gotchas"
> SORT file.name ASC
> ```

> [!tip]- 🌿 Concepts by maturity
> ```dataview
> LIST rows.file.link
> FROM "04 Knowledge/concepts"
> GROUP BY status
> SORT status ASC
> ```

> [!example]- 🗓 Recent weekly reviews
> ```dataview
> LIST
> FROM "04 Knowledge/weekly"
> SORT file.name DESC
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
