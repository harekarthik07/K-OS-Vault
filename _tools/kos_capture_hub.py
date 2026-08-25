"""
K-OS Capture Hub v2 — modern UI + Option B workflow.

Layout: sidebar nav (Capture / Harvest / Preview / Sync), sticky active-project.
Workflow: append to Daily Log by default; spawn on-disk concept cards into the
active project's Concepts/ folder; harvest scans those cards instead of a JSON blob.

Paths are computed relative to this file, so this script MUST live in
<vault>/_tools/kos_capture_hub.py.
"""

import customtkinter as ctk
import os
import time
import re
import threading
import queue
import json
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
from google import genai
from google.genai import types
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------------- CONFIG ----------------
API_KEY = "YOUR_API_KEY_HERE"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
PROJECTS_DIR = os.path.join(VAULT_DIR, "03 Projects")
KNOWLEDGE_DIR = os.path.join(VAULT_DIR, "04 Knowledge")
RESOURCES_DIR = os.path.join(VAULT_DIR, "06 Resources")
INBOX_DIR = os.path.join(VAULT_DIR, "Inbox")
ATTACHMENTS_DIR = os.path.join(VAULT_DIR, "Attachments")
META_DIR = os.path.join(VAULT_DIR, "_meta")
DOMAINS_FILE = os.path.join(META_DIR, "domains.json")
REGISTRY_FILE = os.path.join(META_DIR, "concept-registry.md")
ACTIVE_PROJECT_FILE = os.path.join(META_DIR, ".active_project")

# ---------------- PALETTE (modern dashboard, Vantage-inspired) ----------------
BG          = "#0a0a0a"
SURFACE     = "#141414"
SURFACE_2   = "#1c1c1c"
SURFACE_3   = "#242424"
BORDER      = "#262626"
BORDER_HOV  = "#404040"
TEXT        = "#ededed"
TEXT_MUTED  = "#a1a1aa"
TEXT_DIM    = "#71717a"
ACCENT      = "#22c55e"
ACCENT_HOV  = "#16a34a"
ACCENT_INK  = "#052e16"
DANGER      = "#ef4444"
DANGER_HOV  = "#dc2626"
WARN        = "#f59e0b"
INFO        = "#60a5fa"
PURPLE      = "#a78bfa"

F_SANS = "Segoe UI Variable"
F_MONO = "JetBrains Mono"


# ============================================================
# BACKING FUNCTIONS
# ============================================================

def load_domains():
    if not os.path.exists(DOMAINS_FILE):
        return {}
    try:
        with open(DOMAINS_FILE, encoding="utf-8") as f:
            return json.load(f).get("domains", {})
    except Exception:
        return {}


def route_domain(text, ai_domain):
    """Canonical bucket name from AI-emitted domain string; None if unknown."""
    domains = load_domains()
    lowered = (ai_domain or "").lower().strip()
    for name, cfg in domains.items():
        if name.lower() == lowered:
            return name
        for alias in cfg.get("aliases", []):
            if alias.lower() == lowered:
                return name
    txt_l = (text or "").lower()
    scores = {name: sum(1 for kw in cfg.get("keywords", []) if kw.lower() in txt_l)
              for name, cfg in domains.items()}
    scores = {k: v for k, v in scores.items() if v}
    return max(scores, key=scores.get) if scores else None


def load_active_project():
    if os.path.exists(ACTIVE_PROJECT_FILE):
        try:
            return open(ACTIVE_PROJECT_FILE, encoding="utf-8").read().strip() or None
        except Exception:
            return None
    return None


def save_active_project(name):
    try:
        os.makedirs(META_DIR, exist_ok=True)
        with open(ACTIVE_PROJECT_FILE, "w", encoding="utf-8") as f:
            f.write(name or "")
    except Exception:
        pass


def list_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    return sorted([d for d in os.listdir(PROJECTS_DIR)
                   if os.path.isdir(os.path.join(PROJECTS_DIR, d)) and not d.startswith("_")])


def parse_frontmatter(text):
    """Tiny YAML frontmatter parser — flat key: value only."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def clean_codefence(txt):
    txt = (txt or "").strip()
    if txt.startswith("```markdown"): txt = txt[11:].strip()
    elif txt.startswith("```md"):     txt = txt[5:].strip()
    elif txt.startswith("```"):       txt = txt[3:].strip()
    if txt.endswith("```"):           txt = txt[:-3].strip()
    return txt


def safe_filename(s):
    return re.sub(r'[<>:"/\\|?*\[\]]', '', s or '').strip()


def append_to_daily_log(project, content, image_embed=""):
    """Prepend today's block to the project's Daily Log.md; group by ## YYYY-MM-DD."""
    project_dir = os.path.join(PROJECTS_DIR, project)
    daily_log_path = os.path.join(project_dir, "Daily Log.md")
    today = time.strftime("%Y-%m-%d")
    now = time.strftime("%H:%M")

    header = f"---\ntype: daily_log\nproject: {project}\n---\n\n# Daily Log — {project}\n\nAppend newest at top. One `##` per day.\n"
    if not os.path.exists(daily_log_path):
        os.makedirs(project_dir, exist_ok=True)
        with open(daily_log_path, "w", encoding="utf-8") as f:
            f.write(header)

    with open(daily_log_path, "r", encoding="utf-8") as f:
        existing = f.read()

    block = f"\n### {now}\n{content.strip()}\n{image_embed}\n"
    today_header = f"## {today}"

    if today_header in existing:
        lines = existing.splitlines(keepends=True)
        out, inserted = [], False
        for line in lines:
            out.append(line)
            if not inserted and line.strip() == today_header:
                out.append(block)
                inserted = True
        existing = "".join(out)
    else:
        marker = "Append newest at top. One `##` per day."
        new_day = f"\n\n{today_header}\n{block.rstrip()}\n"
        if marker in existing:
            existing = existing.replace(marker, marker + new_day, 1)
        else:
            existing = existing.rstrip() + new_day

    with open(daily_log_path, "w", encoding="utf-8") as f:
        f.write(existing)
    return daily_log_path


def create_concept_card(project, concept, domain, source_snippet, source_ref=""):
    """Spawn incubating concept card in <project>/Concepts/; no-op if it already exists."""
    project_dir = os.path.join(PROJECTS_DIR, project)
    concepts_dir = os.path.join(project_dir, "Concepts")
    os.makedirs(concepts_dir, exist_ok=True)

    safe = safe_filename(concept)
    if not safe:
        return None
    path = os.path.join(concepts_dir, f"{safe}.md")
    if os.path.exists(path):
        return path

    today = time.strftime("%Y-%m-%d")
    src_line = source_ref if source_ref else "Daily Log"
    card = (
        f"---\n"
        f"concept: {concept}\n"
        f"project: {project}\n"
        f"domain: {domain or ''}\n"
        f"status: incubating\n"
        f"created: {today}\n"
        f"sources: [\"{src_line}\"]\n"
        f"---\n\n"
        f"# {concept}\n\n"
        f"## Working definition (project-specific)\n"
        f"<!-- what this means in the context of {project} -->\n\n"
        f"## Raw context (auto-captured)\n"
        f"{(source_snippet or '').strip()[:2000]}\n\n"
        f"## Promotion checklist\n"
        f"- [ ] Definition is generalizable, not project-specific\n"
        f"- [ ] At least one equation or diagram\n"
        f"- [ ] Linked to a Knowledge MOC\n"
        f"- [ ] Sources cited\n\n"
        f"## Atlas Connections\n"
        f"- [[{domain or ''}]]\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(card)
    return path


def scan_incubating_concepts():
    results = []
    if not os.path.exists(PROJECTS_DIR):
        return results
    for proj in sorted(os.listdir(PROJECTS_DIR)):
        cdir = os.path.join(PROJECTS_DIR, proj, "Concepts")
        if not os.path.isdir(cdir):
            continue
        for fn in sorted(os.listdir(cdir)):
            if not fn.endswith(".md") or fn.startswith("_"):
                continue
            path = os.path.join(cdir, fn)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except Exception:
                continue
            fm = parse_frontmatter(text)
            if fm.get("status", "").strip().lower() == "incubating":
                results.append({
                    "concept": fm.get("concept", fn[:-3]),
                    "project": proj,
                    "domain": fm.get("domain", ""),
                    "created": fm.get("created", ""),
                    "path": path,
                    "body": text,
                })
    return results


def set_concept_status(path, new_status):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r"^status:.*$", f"status: {new_status}", text, count=1, flags=re.MULTILINE)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass


def append_registry(concept, domain, project):
    os.makedirs(META_DIR, exist_ok=True)
    today = time.strftime("%Y-%m-%d")
    line = f"{today} | {concept} | {domain or 'Uncategorized'} | {project}\n"
    with open(REGISTRY_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def get_system_prompt(manual_keywords=""):
    prompt = '''
You are the reasoning layer for an engineering Knowledge Operating System (K-OS) based on Nick Milo's Ideaverse (LYT Framework).
Your job is to take raw, messy input - text and/or images (Ansys thermal gradients, MATLAB vibration plots, heatsink designs, test bench photos) - and format it into clean, structured Markdown notes that bridge Projects (Efforts) to Knowledge (Atlas).

Core Rules:

1. Output Format: Output ONLY valid Markdown with YAML frontmatter. No conversational chatter.

2. ACE Framework Frontmatter — include these exact keys:
   - type: (engineering_note, dyno_log, simulation_analysis, design_review, resource, concept)
   - domain: canonical name from _meta/domains.json (e.g. Thermal Management, Power Electronics, CFD)
   - project: project name, or 'none'
   - date: YYYY-MM-DD
   - folder: MUST be exactly one of: '03 Projects', '04 Knowledge', or '06 Resources'
   - extracted_concepts: list of atomic engineering concept names (e.g. [Thermal Impedance, IGBT Conduction Loss, Modulation Index])

3. Project-to-Knowledge Pipeline:
   - Active project data / test logs -> folder '03 Projects'
   - General reusable principle / formula -> folder '04 Knowledge'
   - Reusable concepts discovered mid-project MUST be named in `extracted_concepts`

4. WikiLink Rules:
   - ATOMIC NOUN LINKS ONLY: wrap standardized title-cased noun phrases in [[WikiLink]] (e.g. [[Junction Temperature]], [[IGBT]], [[Modulation Index]], [[FEA]])
   - DO NOT LINK verbs, actions, generic words, or full sentences
   - INLINE HORIZONTAL LINKS: embed [[WikiLinks]] directly within prose
   - END with '## Atlas Connections' section linking ONLY top-level domain MOCs (e.g. [[Power Electronics]], [[Thermal Management]])

5. Technical Accuracy: expert mech/EE voice. Parse math as LaTeX ($...$ or $$...$$). Summarize visual data from images.

6. PRESERVE INFORMATION: retain all technical details, derivations, and nuance. Do NOT over-summarize.
'''
    if manual_keywords:
        prompt += f"\n\nCRITICAL: user provided these exact keywords: {manual_keywords}\nInject them as [[WikiLinks]] in prose AND in the frontmatter `extracted_concepts` list."
    return prompt


# ============================================================
# WATCHDOG
# ============================================================

class KOSWatcherHandler(FileSystemEventHandler):
    def __init__(self, process_callback):
        super().__init__()
        self.process_callback = process_callback
        self.processed_files = set()

    def on_created(self, event):
        self._handle(event)

    def on_modified(self, event):
        self._handle(event)

    def _handle(self, event):
        if event.is_directory or not event.src_path.endswith(('.txt', '.md')):
            return
        fn = os.path.basename(event.src_path)
        if fn.startswith(("Idea_", ".")) or fn in self.processed_files:
            return
        self.processed_files.add(fn)
        threading.Thread(target=self.process_callback, args=(event.src_path,), daemon=True).start()


# ============================================================
# UI HELPERS
# ============================================================

def card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=10, border_width=1, border_color=BORDER, **kw)

def h_label(parent, text, size=13, color=TEXT):
    return ctk.CTkLabel(parent, text=text, font=(F_SANS, size, "bold"), text_color=color)

def m_label(parent, text, size=11, color=TEXT_MUTED):
    return ctk.CTkLabel(parent, text=text, font=(F_SANS, size), text_color=color)

def entry(parent, placeholder=""):
    return ctk.CTkEntry(parent, placeholder_text=placeholder, height=34,
                        font=(F_MONO, 12), fg_color=BG, border_color=BORDER, text_color=TEXT)

def option(parent, values):
    return ctk.CTkOptionMenu(parent, values=values, height=32, font=(F_SANS, 12),
                             fg_color=SURFACE_2, button_color=SURFACE_3, button_hover_color=BORDER_HOV,
                             text_color=TEXT, dropdown_fg_color=SURFACE_2, dropdown_text_color=TEXT)

def primary_button(parent, text, command):
    return ctk.CTkButton(parent, text=text, command=command, height=42,
                         font=(F_SANS, 13, "bold"), fg_color=ACCENT, hover_color=ACCENT_HOV,
                         text_color=ACCENT_INK, corner_radius=8)

def ghost_button(parent, text, command, width=None):
    kw = {"width": width} if width else {}
    return ctk.CTkButton(parent, text=text, command=command, height=34,
                         font=(F_SANS, 12), fg_color=SURFACE_2, hover_color=SURFACE_3,
                         text_color=TEXT, border_width=1, border_color=BORDER, corner_radius=6, **kw)


# ============================================================
# MAIN APP
# ============================================================

class KOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")

        self.title("K-OS · Capture Hub")
        self.geometry("1240x820")
        self.minsize(1080, 720)
        self.configure(fg_color=BG)

        self.client = genai.Client(api_key=API_KEY)
        self.log_queue = queue.Queue()
        self.watcher_active = True
        self.image_path = None
        self.tk_image = None
        self.pil_image_obj = None
        self.last_note_path = None
        self.active_project = load_active_project() or (list_projects()[0] if list_projects() else None)

        self._build_layout()
        self._build_sidebar()
        self._build_capture_view()
        self._build_harvest_view()
        self._build_preview_view()
        self._build_sync_view()
        self._show_view("capture")

        self.setup_watchdog()
        self.after(150, self._poll_log)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Control-v>", lambda e: self.paste_from_clipboard())

    # ---------- LAYOUT ----------
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0, width=240)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)

        self.views = {}

    def _build_sidebar(self):
        # Brand
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=20, pady=(22, 18))
        ctk.CTkLabel(brand, text="K-OS", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(brand, text="Capture Hub", font=(F_SANS, 11), text_color=TEXT_DIM).pack(anchor="w")

        # Active project chip
        proj_wrap = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        proj_wrap.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        ctk.CTkLabel(proj_wrap, text="ACTIVE PROJECT", font=(F_SANS, 10, "bold"), text_color=TEXT_DIM).pack(anchor="w", padx=4, pady=(0, 4))
        projects = list_projects() or ["(no projects)"]
        self.active_project_menu = option(proj_wrap, projects)
        self.active_project_menu.pack(fill="x")
        if self.active_project and self.active_project in projects:
            self.active_project_menu.set(self.active_project)
        else:
            self.active_project_menu.set(projects[0])
            self.active_project = projects[0] if projects[0] != "(no projects)" else None
        self.active_project_menu.configure(command=self._on_active_project_change)

        # Nav
        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.grid(row=2, column=0, sticky="ew", padx=12, pady=(16, 0))
        self._nav_buttons = {}
        for key, label in [("capture", "Capture"),
                           ("harvest", "Harvest"),
                           ("preview", "Preview"),
                           ("sync",    "Sync Log")]:
            b = ctk.CTkButton(nav, text=label, anchor="w", height=36,
                              font=(F_SANS, 13), fg_color="transparent", hover_color=SURFACE_2,
                              text_color=TEXT_MUTED, corner_radius=6,
                              command=lambda k=key: self._show_view(k))
            b.pack(fill="x", pady=2)
            self._nav_buttons[key] = b

        # Bottom: model + open vault
        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.grid(row=5, column=0, sticky="ew", padx=16, pady=16)
        ctk.CTkLabel(bottom, text="AI MODEL", font=(F_SANS, 10, "bold"), text_color=TEXT_DIM).pack(anchor="w", padx=4, pady=(0, 4))
        self.model_option = option(bottom, ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"])
        self.model_option.pack(fill="x", pady=(0, 10))
        self.model_option.set("gemini-2.5-flash")
        ghost_button(bottom, "Open Vault", self.open_vault_folder).pack(fill="x")

        # Watcher badge
        self.watcher_badge = ctk.CTkLabel(self.sidebar, text="●  watcher on", font=(F_SANS, 10, "bold"),
                                          text_color=ACCENT, fg_color="transparent")
        self.watcher_badge.grid(row=6, column=0, sticky="w", padx=20, pady=(0, 12))

    def _on_active_project_change(self, val):
        if val == "(no projects)":
            return
        self.active_project = val
        save_active_project(val)
        if hasattr(self, 'target_option'):
            self._refresh_target_menu()

    def _show_view(self, key):
        for k, v in self.views.items():
            v.grid_remove()
        self.views[key].grid(row=0, column=0, sticky="nsew")
        for k, b in self._nav_buttons.items():
            if k == key:
                b.configure(fg_color=SURFACE_2, text_color=TEXT)
            else:
                b.configure(fg_color="transparent", text_color=TEXT_MUTED)
        if key == "harvest":
            self.refresh_harvest_list()

    # ---------- CAPTURE VIEW ----------
    def _build_capture_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=6)
        view.grid_columnconfigure(1, weight=4)
        view.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(hdr, text="Capture", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")
        self.status_label = ctk.CTkLabel(hdr, text="Ready", font=(F_SANS, 12), text_color=TEXT_DIM)
        self.status_label.pack(side="right")

        # Left column: intake
        left = ctk.CTkFrame(view, fg_color="transparent")
        left.grid(row=1, column=0, sticky="nsew", padx=(28, 12))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(5, weight=1)

        # Title
        h_label(left, "Note Title", 12, TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 6))
        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        title_row.grid_columnconfigure(0, weight=1)
        self.title_input = entry(title_row, "Auto-timestamp if blank")
        self.title_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ghost_button(title_row, "Suggest", self.suggest_title, width=90).grid(row=0, column=1)

        # Keywords
        h_label(left, "Keywords / Concepts", 12, TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=(0, 6))
        kw_row = ctk.CTkFrame(left, fg_color="transparent")
        kw_row.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        kw_row.grid_columnconfigure(0, weight=1)
        self.keyword_input = entry(kw_row, "[[Junction Temperature]], [[IGBT Loss]]")
        self.keyword_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ghost_button(kw_row, "Suggest", self.suggest_concepts, width=90).grid(row=0, column=1)

        # Body
        h_label(left, "Raw Notes", 12, TEXT_MUTED).grid(row=4, column=0, sticky="w", pady=(0, 6))
        self.raw_text_input = ctk.CTkTextbox(left, font=(F_MONO, 13), fg_color=SURFACE, text_color=TEXT,
                                             border_color=BORDER, border_width=1, corner_radius=8)
        self.raw_text_input.grid(row=5, column=0, sticky="nsew")

        # Actions
        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=6, column=0, sticky="ew", pady=(14, 0))
        actions.grid_columnconfigure(0, weight=3)
        actions.grid_columnconfigure(1, weight=2)
        self.btn_daily = primary_button(actions, "Append to Daily Log", self._on_append_daily)
        self.btn_daily.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.btn_note = ghost_button(actions, "New Note …", self._on_new_note)
        self.btn_note.configure(height=42, font=(F_SANS, 13, "bold"))
        self.btn_note.grid(row=0, column=1, sticky="ew")

        # Right column: routing + image
        right = ctk.CTkFrame(view, fg_color="transparent")
        right.grid(row=1, column=1, sticky="nsew", padx=(12, 28))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        routing = card(right)
        routing.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        h_label(routing, "Routing", 13).pack(anchor="w", padx=16, pady=(14, 10))

        m_label(routing, "Target").pack(anchor="w", padx=16)
        self.target_option = option(routing, ["Daily Log (active)"])
        self.target_option.pack(fill="x", padx=16, pady=(4, 10))

        m_label(routing, "Domain").pack(anchor="w", padx=16)
        self.domain_option = option(routing, self._domain_menu_values())
        self.domain_option.pack(fill="x", padx=16, pady=(4, 10))
        self.domain_option.set("Auto (AI)")

        m_label(routing, "Note Type").pack(anchor="w", padx=16)
        self.type_option = option(routing, ["Auto", "Engineering Note", "Simulation", "Test/Dyno",
                                            "Design Review", "Derivation", "Fleeting"])
        self.type_option.pack(fill="x", padx=16, pady=(4, 14))

        # Image card
        img_card = card(right)
        img_card.grid(row=1, column=0, sticky="nsew")
        img_card.grid_rowconfigure(2, weight=1)
        img_card.grid_columnconfigure(0, weight=1)

        img_hdr = ctk.CTkFrame(img_card, fg_color="transparent")
        img_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        h_label(img_hdr, "Snip / Image", 13).pack(side="left")
        self.btn_remove_img = ctk.CTkButton(img_hdr, text="Clear", width=60, height=24, font=(F_SANS, 11),
                                            fg_color="transparent", hover_color=SURFACE_2, text_color=DANGER,
                                            command=self.clear_image, corner_radius=4)

        img_btns = ctk.CTkFrame(img_card, fg_color="transparent")
        img_btns.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        img_btns.grid_columnconfigure(0, weight=1)
        b1 = ghost_button(img_btns, "Paste (Ctrl+V)", self.paste_from_clipboard)
        b1.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        b2 = ghost_button(img_btns, "Attach", self.select_image, width=90)
        b2.grid(row=0, column=1)

        self.image_preview = ctk.CTkLabel(img_card, text="No image attached",
                                          font=(F_SANS, 11), fg_color=BG, text_color=TEXT_DIM, corner_radius=6)
        self.image_preview.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self._refresh_target_menu()
        self.views["capture"] = view

    def _domain_menu_values(self):
        return ["Auto (AI)"] + list(load_domains().keys())

    def _refresh_target_menu(self):
        values = ["Daily Log (active)", "New file in active project", "04 Knowledge", "06 Resources", "Inbox"]
        self.target_option.configure(values=values)
        self.target_option.set(values[0])

    # ---------- PREVIEW ----------
    def _build_preview_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(hdr, text="Preview", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")

        self.preview_text = ctk.CTkTextbox(view, font=(F_MONO, 13), fg_color=SURFACE, text_color=TEXT_MUTED,
                                           border_color=BORDER, border_width=1, corner_radius=8)
        self.preview_text.grid(row=1, column=0, sticky="nsew", padx=28)

        btns = ctk.CTkFrame(view, fg_color="transparent")
        btns.grid(row=2, column=0, sticky="ew", padx=28, pady=16)
        ghost_button(btns, "Copy Markdown", self.copy_preview).pack(side="left")
        self.btn_open_md = ghost_button(btns, "Open in Obsidian", self.open_last_note)
        self.btn_open_md.pack(side="right")
        self.btn_open_md.configure(state="disabled")

        self.views["preview"] = view

    # ---------- SYNC ----------
    def _build_sync_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(hdr, text="Sync Log", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")
        ghost_button(hdr, "Toggle Watcher", self.toggle_watcher, width=140).pack(side="right")

        self.watcher_log_box = ctk.CTkTextbox(view, font=(F_MONO, 12), fg_color=SURFACE, text_color=TEXT_MUTED,
                                              border_color=BORDER, border_width=1, corner_radius=8)
        self.watcher_log_box.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 24))
        self._log("watcher initialized · monitoring Inbox/")

        self.views["sync"] = view

    # ---------- HARVEST ----------
    def _build_harvest_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 8))
        ctk.CTkLabel(hdr, text="Harvest", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")
        self.harvest_count = ctk.CTkLabel(hdr, text="", font=(F_SANS, 12), text_color=TEXT_DIM)
        self.harvest_count.pack(side="left", padx=12)
        ghost_button(hdr, "Refresh", self.refresh_harvest_list, width=100).pack(side="right")

        sub = ctk.CTkLabel(view, text="Concept cards flagged status: incubating across all projects.",
                           font=(F_SANS, 12), text_color=TEXT_DIM)
        sub.grid(row=0, column=0, sticky="sw", padx=28, pady=(0, 16))

        self.harvest_scroll = ctk.CTkScrollableFrame(view, fg_color=BG, corner_radius=0)
        self.harvest_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 24))

        self.views["harvest"] = view

    def refresh_harvest_list(self):
        for w in self.harvest_scroll.winfo_children():
            w.destroy()
        items = scan_incubating_concepts()
        self.harvest_count.configure(text=f"· {len(items)} incubating")
        if not items:
            m_label(self.harvest_scroll, "Nothing to triage. Nice.", 13, TEXT_DIM).pack(pady=40)
            return

        for item in items:
            row = card(self.harvest_scroll)
            row.pack(fill="x", pady=6, padx=6)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=16, pady=12)
            ctk.CTkLabel(info, text=item["concept"], font=(F_SANS, 14, "bold"), text_color=TEXT).pack(anchor="w")
            meta = f"{item['project']}  ·  {item['domain'] or 'no domain'}  ·  {item['created']}"
            ctk.CTkLabel(info, text=meta, font=(F_SANS, 11), text_color=TEXT_DIM).pack(anchor="w", pady=(2, 0))

            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.pack(side="right", padx=12, pady=10)
            ctk.CTkButton(btns, text="Promote", width=90, height=32, font=(F_SANS, 12, "bold"),
                          fg_color=ACCENT, hover_color=ACCENT_HOV, text_color=ACCENT_INK, corner_radius=6,
                          command=lambda i=item: self._promote(i)).pack(side="left", padx=3)
            ctk.CTkButton(btns, text="Gist", width=70, height=32, font=(F_SANS, 12),
                          fg_color=SURFACE_2, hover_color=SURFACE_3, text_color=TEXT,
                          border_width=1, border_color=BORDER, corner_radius=6,
                          command=lambda i=item: self._mark_gist(i)).pack(side="left", padx=3)
            ctk.CTkButton(btns, text="Discard", width=80, height=32, font=(F_SANS, 12),
                          fg_color="transparent", hover_color=SURFACE_2, text_color=DANGER,
                          border_width=1, border_color=BORDER, corner_radius=6,
                          command=lambda i=item: self._discard(i)).pack(side="left", padx=3)

    def _mark_gist(self, item):
        set_concept_status(item["path"], "gist")
        self._log(f"gist · {item['concept']} ({item['project']})")
        self.refresh_harvest_list()

    def _discard(self, item):
        try:
            os.remove(item["path"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self._log(f"discard · {item['concept']} ({item['project']})")
        self.refresh_harvest_list()

    def _promote(self, item):
        def worker():
            try:
                self._set_status(f"promoting {item['concept']}…", INFO)
                prompt = (
                    f"Rewrite this incubating concept card as an evergreen Knowledge Base article "
                    f"about '{item['concept']}'. Strip project-specific references. Keep equations. "
                    f"Add generalized definition and typical examples. Use frontmatter with "
                    f"type: concept, folder: '04 Knowledge', domain: '{item['domain']}'. "
                    f"Source card:\n\n{item['body']}"
                )
                resp = self.client.models.generate_content(
                    model=self.model_option.get(), contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=get_system_prompt(""))
                )
                formatted = clean_codefence(resp.text)
                domain = item["domain"] or ""
                dest_dir = os.path.join(KNOWLEDGE_DIR, domain) if domain else KNOWLEDGE_DIR
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, f"{safe_filename(item['concept'])}.md")
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(formatted)
                append_registry(item["concept"], domain, item["project"])
                try: os.remove(item["path"])
                except Exception: pass
                self._log(f"promoted · {item['concept']} -> 04 Knowledge/{domain}")
                self._set_status("promoted", ACCENT)
                self.after(0, self.refresh_harvest_list)
            except Exception as e:
                self._set_status("promote failed", DANGER)
                messagebox.showerror("Promote failed", str(e))
        threading.Thread(target=worker, daemon=True).start()

    # ---------- IMAGE ----------
    def paste_from_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            if img is not None:
                if isinstance(img, list):
                    for f in img:
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                            self.load_image_from_path(f)
                            return
                elif isinstance(img, Image.Image):
                    self.image_path = None
                    self.pil_image_obj = img
                    self.display_image(img)
                    return
            try:
                text = self.clipboard_get()
                if text:
                    self.raw_text_input.insert("insert", text)
            except Exception:
                pass
        except Exception as e:
            print(f"Clipboard error: {e}")

    def select_image(self):
        p = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if p:
            self.load_image_from_path(p)

    def load_image_from_path(self, path):
        self.image_path = path
        self.pil_image_obj = None
        try:
            self.display_image(Image.open(path))
        except Exception as e:
            self.image_preview.configure(text=f"error: {e}", image="")

    def display_image(self, pil_image):
        baseheight = 180
        wp = baseheight / float(pil_image.size[1])
        ws = int(float(pil_image.size[0]) * wp)
        if ws > 0:
            resized = pil_image.resize((ws, baseheight), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_preview.configure(text="", image=self.tk_image)
            self.btn_remove_img.pack(side="right")

    def clear_image(self):
        self.image_path = None
        self.tk_image = None
        self.pil_image_obj = None
        self.image_preview.configure(text="No image attached", image="")
        self.btn_remove_img.pack_forget()

    # ---------- ACTIONS ----------
    def open_vault_folder(self):
        try:
            os.startfile(os.path.abspath(VAULT_DIR))
        except Exception:
            pass

    def copy_preview(self):
        self.clipboard_clear()
        self.clipboard_append(self.preview_text.get("1.0", "end-1c"))

    def open_last_note(self):
        if self.last_note_path and os.path.exists(self.last_note_path):
            try: os.startfile(os.path.abspath(self.last_note_path))
            except Exception: pass

    def toggle_watcher(self):
        self.watcher_active = not self.watcher_active
        if self.watcher_active:
            self.watcher_badge.configure(text="●  watcher on", text_color=ACCENT)
            self._log("watcher resumed")
        else:
            self.watcher_badge.configure(text="●  watcher paused", text_color=WARN)
            self._log("watcher paused")

    def _set_status(self, text, color=TEXT_DIM):
        self.status_label.configure(text=text, text_color=color)

    def _log(self, msg):
        self.log_queue.put(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

    def _poll_log(self):
        while not self.log_queue.empty():
            self.watcher_log_box.insert("end", self.log_queue.get())
            self.watcher_log_box.see("end")
        self.after(250, self._poll_log)

    # ---------- CAPTURE HANDLERS ----------
    def _on_append_daily(self):
        if not self.active_project:
            messagebox.showwarning("No project", "Pick an active project in the sidebar first.")
            return
        self._process(mode="daily")

    def _on_new_note(self):
        target = self.target_option.get()
        if target in ("Daily Log (active)",):
            self._process(mode="daily")
        else:
            self._process(mode="note", target=target)

    def _process(self, mode, target=None):
        text = self.raw_text_input.get("1.0", "end").strip()
        keywords = self.keyword_input.get().strip()
        custom_title = self.title_input.get().strip()
        domain_ui = self.domain_option.get()
        note_type = self.type_option.get()
        model = self.model_option.get()

        if not text and not self.image_path and not self.pil_image_obj:
            messagebox.showwarning("Empty", "Enter text or attach an image.")
            return

        self._set_status(f"{model} · structuring…", INFO)
        self.btn_daily.configure(state="disabled")
        self.btn_note.configure(state="disabled")
        self.update()

        def worker():
            try:
                # Build contents for Gemini
                contents = []
                image_embed = ""
                img = self.pil_image_obj or (Image.open(self.image_path) if self.image_path else None)
                if img is not None:
                    contents.append(img)
                    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
                    fn = f"snip_{int(time.time())}.png"
                    img.save(os.path.join(ATTACHMENTS_DIR, fn), format="PNG")
                    image_embed = f"\n\n![[{fn}]]\n"

                hints = f"Hint: user selected domain '{domain_ui}', type '{note_type}', active project '{self.active_project}'.\n\n"
                contents.append(hints + text)

                resp = self.client.models.generate_content(
                    model=model, contents=contents,
                    config=types.GenerateContentConfig(system_instruction=get_system_prompt(keywords)),
                )
                formatted = clean_codefence(resp.text) + image_embed

                # Extract frontmatter for routing
                fm = parse_frontmatter(formatted)
                ai_domain = fm.get("domain", "").strip("'").strip('"')
                canonical_domain = route_domain(text, ai_domain)
                concepts_raw = re.search(r"extracted_concepts:\s*\[(.*?)\]", formatted, re.IGNORECASE)
                concepts = []
                if concepts_raw:
                    concepts = [c.strip().strip('"').strip("'").strip("[]") for c in concepts_raw.group(1).split(",") if c.strip()]

                # Route
                if mode == "daily":
                    dest = append_to_daily_log(self.active_project, formatted, "")
                    label = f"Daily Log · {self.active_project}"
                else:
                    if target == "New file in active project":
                        dest_dir = os.path.join(PROJECTS_DIR, self.active_project)
                    elif target == "04 Knowledge":
                        dest_dir = os.path.join(KNOWLEDGE_DIR, canonical_domain) if canonical_domain else KNOWLEDGE_DIR
                    elif target == "06 Resources":
                        dest_dir = os.path.join(RESOURCES_DIR, canonical_domain) if canonical_domain else RESOURCES_DIR
                    else:
                        dest_dir = INBOX_DIR
                    os.makedirs(dest_dir, exist_ok=True)
                    fn = (custom_title if custom_title else f"Note_{time.strftime('%Y%m%d_%H%M%S')}")
                    if not fn.endswith(".md"): fn += ".md"
                    dest = os.path.join(dest_dir, fn)
                    with open(dest, "w", encoding="utf-8") as f:
                        f.write(formatted)
                    label = f"{os.path.basename(dest_dir)}/{fn}"

                # Spawn concept cards into active project's Concepts/
                if self.active_project and concepts:
                    src_ref = f"Daily Log#{time.strftime('%Y-%m-%d')}" if mode == "daily" else os.path.basename(dest)
                    for c in concepts:
                        c_clean = c.strip().replace("[[", "").replace("]]", "")
                        if c_clean:
                            create_concept_card(self.active_project, c_clean, canonical_domain, text, src_ref)

                # Update UI
                self.preview_text.delete("1.0", "end")
                self.preview_text.insert("1.0", formatted)
                self.last_note_path = dest
                self.btn_open_md.configure(state="normal")
                self._log(f"saved · {label}")
                if concepts:
                    self._log(f"  + {len(concepts)} concept card(s) into {self.active_project}/Concepts")
                self._set_status(f"saved to {label}", ACCENT)
            except Exception as e:
                self._set_status("API error", DANGER)
                messagebox.showerror("API Error", str(e))
            finally:
                self.btn_daily.configure(state="normal")
                self.btn_note.configure(state="normal")
        threading.Thread(target=worker, daemon=True).start()

    def suggest_title(self):
        text = self.raw_text_input.get("1.0", "end").strip()
        if not text:
            return
        try:
            prompt = "Generate a concise markdown file title (no extension, max 6 words) for this note. Return only the title.\n\n" + text[:2000]
            r = self.client.models.generate_content(model=self.model_option.get(), contents=prompt)
            self.title_input.delete(0, "end")
            self.title_input.insert(0, r.text.strip().replace('"', '').replace("'", ""))
        except Exception as e:
            print(f"title error: {e}")

    def suggest_concepts(self):
        text = self.raw_text_input.get("1.0", "end").strip()
        if not text:
            return
        try:
            prompt = "Extract 2-4 core engineering concepts as [[WikiLinks]], comma-separated, no other text.\n\n" + text[:2000]
            r = self.client.models.generate_content(model=self.model_option.get(), contents=prompt)
            self.keyword_input.delete(0, "end")
            self.keyword_input.insert(0, r.text.strip())
        except Exception as e:
            print(f"concepts error: {e}")

    # ---------- WATCHDOG ----------
    def setup_watchdog(self):
        os.makedirs(INBOX_DIR, exist_ok=True)
        self.event_handler = KOSWatcherHandler(self._handle_inbox_file)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=INBOX_DIR, recursive=False)
        self.observer.start()

    def _handle_inbox_file(self, file_path):
        if not self.watcher_active:
            return
        fn = os.path.basename(file_path)
        self._log(f"inbox event · {fn}")
        time.sleep(1)
        try:
            if not os.path.exists(file_path): return
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            if not raw.strip(): return
            if raw.startswith("---") and ("type:" in raw or "domain:" in raw): return

            self._log("  formatting…")
            resp = self.client.models.generate_content(
                model=self.model_option.get(), contents=raw,
                config=types.GenerateContentConfig(system_instruction=get_system_prompt("")),
            )
            formatted = clean_codefence(resp.text)
            fm = parse_frontmatter(formatted)
            canonical = route_domain(raw, fm.get("domain", ""))

            target_folder = "04 Knowledge"
            folder_match = re.search(r"folder:\s*(.+)", formatted, re.IGNORECASE)
            if folder_match:
                ext = folder_match.group(1).strip().strip("'").strip('"')
                if ext in ("03 Projects", "04 Knowledge", "06 Resources"):
                    target_folder = ext

            if target_folder == "04 Knowledge":
                dest_dir = os.path.join(KNOWLEDGE_DIR, canonical) if canonical else KNOWLEDGE_DIR
            elif target_folder == "06 Resources":
                dest_dir = os.path.join(RESOURCES_DIR, canonical) if canonical else RESOURCES_DIR
            elif self.active_project:
                # Route project notes into active project's Daily Log, not orphan files
                append_to_daily_log(self.active_project, formatted, "")
                try: os.remove(file_path)
                except Exception: pass
                self._log(f"  -> {self.active_project}/Daily Log")
                return
            else:
                dest_dir = INBOX_DIR

            os.makedirs(dest_dir, exist_ok=True)
            new_name = f"Idea_{time.strftime('%Y%m%d_%H%M%S')}.md"
            dest = os.path.join(dest_dir, new_name)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(formatted)
            try:
                if os.path.abspath(file_path) != os.path.abspath(dest):
                    os.remove(file_path)
            except Exception: pass
            self._log(f"  -> {os.path.relpath(dest, VAULT_DIR)}")

            # Concept cards into active project if we have one
            if self.active_project:
                concepts_raw = re.search(r"extracted_concepts:\s*\[(.*?)\]", formatted, re.IGNORECASE)
                if concepts_raw:
                    for c in concepts_raw.group(1).split(","):
                        c_clean = c.strip().strip('"').strip("'").replace("[[", "").replace("]]", "")
                        if c_clean:
                            create_concept_card(self.active_project, c_clean, canonical, raw, f"Inbox/{fn}")
        except Exception as e:
            self._log(f"  ! error: {e}")

    def on_closing(self):
        if hasattr(self, "observer") and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        self.destroy()


if __name__ == "__main__":
    for d in (PROJECTS_DIR, KNOWLEDGE_DIR, RESOURCES_DIR, INBOX_DIR, META_DIR):
        os.makedirs(d, exist_ok=True)
    KOSApp().mainloop()
