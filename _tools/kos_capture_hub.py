"""
K-OS Capture Hub v3

Changes from v2:
  * Global hotkey quick-capture (Ctrl+Alt+K) — capture without leaving your app
  * Short notes skip the AI entirely (instant, free); long notes get formatted
  * Concept cards spawn on the 2nd mention, not the 1st (kills card flood)
  * Dedup: a concept already in Knowledge/ or Concepts/ links instead of duplicating
  * API key read from _meta/.env or $GEMINI_API_KEY — never hardcoded
  * Friday nudge: opens Harvest when concepts have been incubating too long
  * System tray: closing the window minimizes to tray instead of quitting, so
    the hotkey stays alive. Quit from the tray menu when you actually want out.

Must live at <vault>/_tools/kos_capture_hub.py — paths resolve relative to this file.
Self-check: python kos_capture_hub.py --selftest
"""

import ctypes
import json
import os
import queue
import re
import sys
import threading
import time
from ctypes import wintypes

# GUI and API imports live further down, after the --selftest gate, so the
# self-check runs on a machine without customtkinter/PIL/watchdog installed.

# ---------------- PATHS ----------------
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
MENTIONS_FILE = os.path.join(META_DIR, "concept-mentions.json")
ACTIVE_PROJECT_FILE = os.path.join(META_DIR, ".active_project")
ENV_FILE = os.path.join(META_DIR, ".env")

# ---------------- TUNING ----------------
AI_THRESHOLD = 200      # chars; below this a Daily Log capture skips the AI
MENTION_THRESHOLD = 2   # spawn a concept card on the Nth mention
HARVEST_STALE_DAYS = 14

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# ---------------- PALETTE ----------------
BG         = "#0a0a0a"
SURFACE    = "#141414"
SURFACE_2  = "#1c1c1c"
SURFACE_3  = "#242424"
BORDER     = "#262626"
TEXT       = "#ededed"
TEXT_MUTED = "#a1a1aa"
TEXT_DIM   = "#71717a"
ACCENT     = "#22c55e"
ACCENT_HOV = "#16a34a"
ACCENT_INK = "#052e16"
DANGER     = "#ef4444"
WARN       = "#f59e0b"
INFO       = "#60a5fa"

F_SANS = "Segoe UI Variable"
F_MONO = "JetBrains Mono"


# ============================================================
# CONFIG / SECRETS
# ============================================================

def _read_env_file():
    """Parse _meta/.env as flat KEY=value. Missing file is fine."""
    out = {}
    if not os.path.exists(ENV_FILE):
        return out
    try:
        with open(ENV_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return out


def load_api_key():
    """$GEMINI_API_KEY wins, then _meta/.env. Empty string = AI disabled, app still runs."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    env = _read_env_file()
    return env.get("GEMINI_API_KEY") or env.get("API_KEY") or ""


def load_model():
    return os.environ.get("KOS_MODEL") or _read_env_file().get("KOS_MODEL") or "gemini-2.5-flash"


# ============================================================
# DOMAIN / CONCEPT LOGIC  (pure — covered by --selftest)
# ============================================================

def _load_domains_cfg():
    try:
        with open(DOMAINS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_domains():
    return _load_domains_cfg().get("domains", {})


def load_aliases():
    """{normalized alias -> Canonical Display Name}. Restart the hub to reload."""
    out = {}
    for canon, alist in (_load_domains_cfg().get("concept_aliases") or {}).items():
        out[normalize_concept(canon)] = canon
        for a in alist or []:
            out[normalize_concept(a)] = canon
    return out


def normalize_concept(s):
    """Casefold + strip wikilinks/punctuation so 'Thermal_Resistance' == '[[thermal  resistance]]'."""
    s = (s or "").replace("[[", "").replace("]]", "").strip().lower()
    s = re.sub(r"[_\-]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def resolve_concepts(names, aliases=None):
    """Map raw concept strings to canonical display names, dropping blanks and dupes."""
    if aliases is None:
        aliases = load_aliases()
    seen, out = set(), []
    for raw in names or []:
        cleaned = (raw or "").replace("[[", "").replace("]]", "").strip().strip('"').strip("'")
        if not cleaned:
            continue
        canon = aliases.get(normalize_concept(cleaned), cleaned)
        key = normalize_concept(canon)
        if key and key not in seen:
            seen.add(key)
            out.append(canon)
    return out


def route_domain(text, ai_domain):
    """Canonical bucket name for an AI-emitted domain string; keyword fallback; None if unknown."""
    domains = load_domains()
    lowered = (ai_domain or "").lower().strip()
    for name, cfg in domains.items():
        if name.lower() == lowered or lowered in [a.lower() for a in cfg.get("aliases", [])]:
            return name
    txt_l = (text or "").lower()
    scores = {n: sum(1 for kw in c.get("keywords", []) if kw.lower() in txt_l)
              for n, c in domains.items()}
    scores = {k: v for k, v in scores.items() if v}
    return max(scores, key=scores.get) if scores else None


# ---------------- mention counting ----------------

def load_mentions():
    try:
        with open(MENTIONS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_mentions(data):
    os.makedirs(META_DIR, exist_ok=True)
    try:
        with open(MENTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
    except Exception:
        pass


def record_mentions(concepts, project):
    """Bump counters. Return only the concepts that just hit MENTION_THRESHOLD.

    Uses == not >= so a card spawns exactly once. If you discard a card, further
    mentions won't resurrect it — that's intentional.
    """
    data = load_mentions()
    today = time.strftime("%Y-%m-%d")
    ready = []
    for c in concepts:
        key = normalize_concept(c)
        if not key:
            continue
        e = data.get(key) or {"display": c, "count": 0, "projects": [], "first_seen": today}
        e["count"] += 1
        e["last_seen"] = today
        if project and project not in e["projects"]:
            e["projects"].append(project)
        data[key] = e
        if e["count"] == MENTION_THRESHOLD:
            ready.append(e["display"])
    save_mentions(data)
    return ready


# ---------------- existing-knowledge lookup ----------------

def find_existing_concept(name):
    """(kind, path) if this concept already lives in Knowledge or any project's Concepts/.

    ponytail: linear scan of the vault. Fine at a few hundred notes; build an
    index in _meta/ if capture ever feels slow.
    """
    target = normalize_concept(name)
    if not target:
        return (None, None)
    for root, _dirs, files in os.walk(KNOWLEDGE_DIR):
        for fn in files:
            if fn.endswith(".md") and normalize_concept(fn[:-3]) == target:
                return ("knowledge", os.path.join(root, fn))
    if os.path.isdir(PROJECTS_DIR):
        for proj in sorted(os.listdir(PROJECTS_DIR)):
            cdir = os.path.join(PROJECTS_DIR, proj, "Concepts")
            if not os.path.isdir(cdir):
                continue
            for fn in os.listdir(cdir):
                if fn.endswith(".md") and normalize_concept(fn[:-3]) == target:
                    return ("incubating", os.path.join(cdir, fn))
    return (None, None)


# ============================================================
# VAULT I/O
# ============================================================

def parse_frontmatter(text):
    """Flat `key: value` YAML frontmatter only — enough for our own files."""
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
    for fence in ("```markdown", "```md", "```"):
        if txt.startswith(fence):
            txt = txt[len(fence):].strip()
            break
    if txt.endswith("```"):
        txt = txt[:-3].strip()
    return txt


def safe_filename(s):
    return re.sub(r'[<>:"/\\|?*\[\]]', "", s or "").strip()


def list_projects():
    if not os.path.isdir(PROJECTS_DIR):
        return []
    return sorted(d for d in os.listdir(PROJECTS_DIR)
                  if os.path.isdir(os.path.join(PROJECTS_DIR, d)) and not d.startswith("_"))


def load_active_project():
    try:
        with open(ACTIVE_PROJECT_FILE, encoding="utf-8") as f:
            return f.read().strip() or None
    except Exception:
        return None


def save_active_project(name):
    os.makedirs(META_DIR, exist_ok=True)
    try:
        with open(ACTIVE_PROJECT_FILE, "w", encoding="utf-8") as f:
            f.write(name or "")
    except Exception:
        pass


DAILY_LOG_MARKER = "Append newest at top. One `##` per day."


def append_to_daily_log(project, content):
    """Add a timestamped block under today's `## YYYY-MM-DD`, creating the day if needed."""
    project_dir = os.path.join(PROJECTS_DIR, project)
    path = os.path.join(project_dir, "Daily Log.md")
    today = time.strftime("%Y-%m-%d")
    now = time.strftime("%H:%M")

    if not os.path.exists(path):
        os.makedirs(project_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"---\ntype: daily_log\nproject: {project}\n---\n\n"
                    f"# Daily Log — {project}\n\n{DAILY_LOG_MARKER}\n")

    with open(path, encoding="utf-8") as f:
        existing = f.read()

    block = f"\n### {now}\n{content.strip()}\n"
    day_header = f"## {today}"

    if day_header in existing:
        out, inserted = [], False
        for line in existing.splitlines(keepends=True):
            out.append(line)
            if not inserted and line.strip() == day_header:
                out.append(block)
                inserted = True
        existing = "".join(out)
    else:
        new_day = f"\n\n{day_header}\n{block.rstrip()}\n"
        if DAILY_LOG_MARKER in existing:
            existing = existing.replace(DAILY_LOG_MARKER, DAILY_LOG_MARKER + new_day, 1)
        else:
            existing = existing.rstrip() + new_day

    with open(path, "w", encoding="utf-8") as f:
        f.write(existing)
    return path


def create_concept_card(project, concept, domain, source_snippet, source_ref=""):
    """Spawn an incubating card. No-op if the concept already exists anywhere."""
    kind, existing = find_existing_concept(concept)
    if kind:
        return None
    concepts_dir = os.path.join(PROJECTS_DIR, project, "Concepts")
    os.makedirs(concepts_dir, exist_ok=True)
    safe = safe_filename(concept)
    if not safe:
        return None
    path = os.path.join(concepts_dir, f"{safe}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"---\nconcept: {concept}\nproject: {project}\ndomain: {domain or ''}\n"
            f"status: incubating\ncreated: {time.strftime('%Y-%m-%d')}\n"
            f"sources: [\"{source_ref or 'Daily Log'}\"]\n---\n\n"
            f"# {concept}\n\n"
            f"## Working definition (project-specific)\n"
            f"<!-- what this means in the context of {project} -->\n\n"
            f"## Raw context (auto-captured)\n{(source_snippet or '').strip()[:2000]}\n\n"
            f"## Promotion checklist\n"
            f"- [ ] Definition is generalizable, not project-specific\n"
            f"- [ ] At least one equation or diagram\n"
            f"- [ ] Linked to a Knowledge MOC\n"
            f"- [ ] Sources cited\n\n"
            f"## Atlas Connections\n- [[{domain or ''}]]\n"
        )
    return path


def scan_incubating_concepts():
    results = []
    if not os.path.isdir(PROJECTS_DIR):
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
                results.append({"concept": fm.get("concept", fn[:-3]), "project": proj,
                                "domain": fm.get("domain", ""), "created": fm.get("created", ""),
                                "path": path, "body": text})
    return results


def harvest_overdue(days=HARVEST_STALE_DAYS):
    cutoff = time.time() - days * 86400
    for item in scan_incubating_concepts():
        try:
            if time.mktime(time.strptime(item["created"], "%Y-%m-%d")) < cutoff:
                return True
        except Exception:
            continue
    return False


def set_concept_status(path, new_status):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r"^status:.*$", f"status: {new_status}", text, count=1, flags=re.MULTILINE)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass


def append_registry(concept, domain, project):
    os.makedirs(META_DIR, exist_ok=True)
    with open(REGISTRY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d')} | {concept} | {domain or 'Uncategorized'} | {project}\n")


# ============================================================
# AI
# ============================================================

def get_system_prompt(manual_keywords=""):
    prompt = '''
You are the reasoning layer for an engineering Knowledge Operating System (K-OS) based on Nick Milo's Ideaverse (LYT Framework).
Take raw, messy input - text and/or images (Ansys thermal gradients, MATLAB vibration plots, heatsink designs, test bench photos) - and format it into clean, structured Markdown that bridges Projects (Efforts) to Knowledge (Atlas).

Core Rules:

1. Output ONLY valid Markdown with YAML frontmatter. No conversational chatter.

2. Frontmatter keys, exactly:
   - type: engineering_note | dyno_log | simulation_analysis | design_review | resource | concept
   - domain: canonical name from _meta/domains.json (e.g. Thermal Management, Power Electronics, CFD)
   - project: project name, or 'none'
   - date: YYYY-MM-DD
   - folder: exactly one of '03 Projects', '04 Knowledge', '06 Resources'
   - extracted_concepts: atomic concept names (e.g. [Thermal Impedance, IGBT Conduction Loss])

3. Routing: active project data / test logs -> '03 Projects'. Reusable principle or
   formula -> '04 Knowledge'. Reusable concepts found mid-project MUST appear in extracted_concepts.

4. WikiLinks:
   - Wrap ONLY title-cased atomic noun phrases: [[Junction Temperature]], [[IGBT]], [[FEA]]
   - NEVER link verbs, actions, generic words, or sentences
   - Embed links inline in prose
   - End with '## Atlas Connections' linking only top-level domain MOCs

5. Expert mech/EE voice. Math as LaTeX ($...$ or $$...$$). Summarize visual data from images.

6. PRESERVE INFORMATION: keep all technical detail, derivations, and nuance. Do NOT over-summarize.
'''
    if manual_keywords:
        prompt += (f"\n\nCRITICAL: the user supplied these keywords: {manual_keywords}\n"
                   f"Inject them as [[WikiLinks]] in the prose AND in extracted_concepts.")
    return prompt


# ============================================================
# SELF-CHECK  (runs before GUI imports: python kos_capture_hub.py --selftest)
# ============================================================

def _selftest():
    import shutil
    import tempfile
    global PROJECTS_DIR, KNOWLEDGE_DIR, META_DIR, MENTIONS_FILE

    assert normalize_concept("[[Junction  Temperature]]") == "junction temperature"
    assert normalize_concept("Thermal_Resistance") == "thermal resistance"
    assert normalize_concept("  Heat-Transfer ") == "heat transfer"

    aliases = {"tj": "Junction Temperature", "junction temperature": "Junction Temperature"}
    assert resolve_concepts(["[[Tj]]", "Heatsink", "junction  temperature"], aliases) == \
        ["Junction Temperature", "Heatsink"], "aliases must collapse duplicates"

    tmp = tempfile.mkdtemp(prefix="kos_test_")
    try:
        PROJECTS_DIR = os.path.join(tmp, "03 Projects")
        KNOWLEDGE_DIR = os.path.join(tmp, "04 Knowledge")
        META_DIR = os.path.join(tmp, "_meta")
        MENTIONS_FILE = os.path.join(META_DIR, "concept-mentions.json")
        os.makedirs(os.path.join(PROJECTS_DIR, "P1"), exist_ok=True)
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

        # daily log: creates the file, then groups a second entry under the same day header
        append_to_daily_log("P1", "first")
        append_to_daily_log("P1", "second")
        with open(os.path.join(PROJECTS_DIR, "P1", "Daily Log.md"), encoding="utf-8") as f:
            log = f.read()
        assert log.count(f"## {time.strftime('%Y-%m-%d')}") == 1, "one header per day"
        assert "first" in log and "second" in log

        # mention threshold: card only on the 2nd sighting, and only once
        assert record_mentions(["Thermal Impedance"], "P1") == []
        assert record_mentions(["Thermal Impedance"], "P1") == ["Thermal Impedance"]
        assert record_mentions(["Thermal Impedance"], "P1") == [], "fires once, not repeatedly"

        # dedup: a concept already promoted to Knowledge blocks a duplicate card
        os.makedirs(os.path.join(KNOWLEDGE_DIR, "Thermal Management"), exist_ok=True)
        with open(os.path.join(KNOWLEDGE_DIR, "Thermal Management", "Heatsink.md"), "w") as f:
            f.write("x")
        assert find_existing_concept("heatsink")[0] == "knowledge"
        assert create_concept_card("P1", "Heatsink", "Thermal Management", "ctx") is None
        assert create_concept_card("P1", "Fin Efficiency", "Heat Transfer", "ctx") is not None
        assert find_existing_concept("fin efficiency")[0] == "incubating"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selftest ok")


if __name__ == "__main__" and "--selftest" in sys.argv:
    _selftest()
    sys.exit(0)


from tkinter import filedialog, messagebox  # noqa: E402

import customtkinter as ctk  # noqa: E402
from PIL import Image, ImageDraw, ImageGrab, ImageTk  # noqa: E402
from watchdog.events import FileSystemEventHandler  # noqa: E402
from watchdog.observers import Observer  # noqa: E402

try:
    import pystray  # noqa: E402
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


# ============================================================
# GLOBAL HOTKEY  (Windows, stdlib ctypes — no extra dependency)
# ============================================================

WM_HOTKEY, MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_NOREPEAT = 0x0312, 0x0001, 0x0002, 0x0004, 0x4000
VK_K = 0x4B


class HotkeyListener(threading.Thread):
    """Registers global hotkeys and pumps their message loop on its own thread.

    ponytail: no tray icon — the taskbar entry is how you get the window back.
    Add pystray only if you actually want to hide it from the taskbar.
    """

    def __init__(self, bindings):
        super().__init__(daemon=True)
        self.bindings = bindings  # {hotkey_id: (modifiers, vk, callback)}

    def run(self):
        if sys.platform != "win32":
            return
        user32 = ctypes.windll.user32
        for hid, (mods, vk, _cb) in self.bindings.items():
            if not user32.RegisterHotKey(None, hid, mods | MOD_NOREPEAT, vk):
                print(f"[kos] hotkey {hid} already taken by another app")
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == WM_HOTKEY:
                binding = self.bindings.get(msg.wParam)
                if binding:
                    binding[2]()
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))


# ============================================================
# WATCHDOG
# ============================================================

class KOSWatcherHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.seen = set()

    def on_created(self, event):
        self._handle(event)

    def on_modified(self, event):
        self._handle(event)

    def _handle(self, event):
        if event.is_directory or not event.src_path.endswith((".txt", ".md")):
            return
        fn = os.path.basename(event.src_path)
        if fn.startswith(("Idea_", ".")) or fn in self.seen:
            return
        self.seen.add(fn)
        threading.Thread(target=self.callback, args=(event.src_path,), daemon=True).start()


# ============================================================
# UI HELPERS
# ============================================================

def card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=10,
                        border_width=1, border_color=BORDER, **kw)


def h_label(parent, text, size=13, color=TEXT):
    return ctk.CTkLabel(parent, text=text, font=(F_SANS, size, "bold"), text_color=color)


def m_label(parent, text, size=11, color=TEXT_MUTED):
    return ctk.CTkLabel(parent, text=text, font=(F_SANS, size), text_color=color)


def entry(parent, placeholder=""):
    return ctk.CTkEntry(parent, placeholder_text=placeholder, height=34, font=(F_MONO, 12),
                        fg_color=BG, border_color=BORDER, text_color=TEXT)


def option(parent, values):
    return ctk.CTkOptionMenu(parent, values=values, height=32, font=(F_SANS, 12),
                             fg_color=SURFACE_2, button_color=SURFACE_3, button_hover_color=BORDER,
                             text_color=TEXT, dropdown_fg_color=SURFACE_2, dropdown_text_color=TEXT)


def primary_button(parent, text, command):
    return ctk.CTkButton(parent, text=text, command=command, height=42, font=(F_SANS, 13, "bold"),
                         fg_color=ACCENT, hover_color=ACCENT_HOV, text_color=ACCENT_INK, corner_radius=8)


def ghost_button(parent, text, command, width=None):
    kw = {"width": width} if width else {}
    return ctk.CTkButton(parent, text=text, command=command, height=34, font=(F_SANS, 12),
                         fg_color=SURFACE_2, hover_color=SURFACE_3, text_color=TEXT,
                         border_width=1, border_color=BORDER, corner_radius=6, **kw)


# ============================================================
# APP
# ============================================================

class KOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.title("K-OS · Capture Hub")
        self.geometry("1180x800")
        self.minsize(1000, 700)
        self.configure(fg_color=BG)

        self.model = load_model()
        self.api_key = load_api_key()
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[kos] genai init failed: {e}")

        self.log_queue = queue.Queue()
        self.watcher_active = True
        self.image_path = None
        self.tk_image = None
        self.pil_image_obj = None
        self.last_note_path = None
        self._quick_win = None
        self.tray_icon = None

        projects = list_projects()
        saved = load_active_project()
        self.active_project = saved if saved in projects else (projects[0] if projects else None)

        self._build_layout()
        self._build_sidebar()
        self._build_capture_view()
        self._build_harvest_view()
        self._build_sync_view()

        # Friday nudge — land on Harvest when something has been rotting.
        if time.localtime().tm_wday == 4 and harvest_overdue():
            self._show_view("harvest")
            self._log(f"friday · concepts incubating >{HARVEST_STALE_DAYS}d — triage them")
        else:
            self._show_view("capture")

        if not self.api_key:
            self._set_status("no API key — raw capture only (see _meta/.env)", WARN)

        self.setup_watchdog()
        self.setup_hotkeys()
        self.setup_tray()
        self.after(150, self._poll_log)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Control-v>", lambda e: self.paste_from_clipboard())

    # ---------- layout ----------
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0, width=230)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(3, weight=1)
        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)
        self.views = {}

    def _build_sidebar(self):
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=20, pady=(22, 18))
        ctk.CTkLabel(brand, text="K-OS", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(brand, text="Capture Hub", font=(F_SANS, 11), text_color=TEXT_DIM).pack(anchor="w")

        wrap = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        wrap.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        ctk.CTkLabel(wrap, text="ACTIVE PROJECT", font=(F_SANS, 10, "bold"),
                     text_color=TEXT_DIM).pack(anchor="w", padx=4, pady=(0, 4))
        projects = list_projects() or ["(no projects)"]
        self.active_project_menu = option(wrap, projects)
        self.active_project_menu.pack(fill="x")
        self.active_project_menu.set(self.active_project or projects[0])
        self.active_project_menu.configure(command=self._on_project_change)

        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.grid(row=2, column=0, sticky="ew", padx=12, pady=(16, 0))
        self._nav_buttons = {}
        for key, label in (("capture", "Capture"), ("harvest", "Harvest"), ("sync", "Sync Log")):
            b = ctk.CTkButton(nav, text=label, anchor="w", height=36, font=(F_SANS, 13),
                              fg_color="transparent", hover_color=SURFACE_2, text_color=TEXT_MUTED,
                              corner_radius=6, command=lambda k=key: self._show_view(k))
            b.pack(fill="x", pady=2)
            self._nav_buttons[key] = b

        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))
        ctk.CTkLabel(bottom, text="Ctrl+Alt+K  quick capture", font=(F_MONO, 10),
                     text_color=TEXT_DIM).pack(anchor="w", pady=(0, 2))
        tray_hint = "Close = minimize to tray" if HAS_TRAY else "pystray not installed — close quits"
        ctk.CTkLabel(bottom, text=tray_hint, font=(F_MONO, 10),
                     text_color=TEXT_DIM).pack(anchor="w", pady=(0, 8))
        ghost_button(bottom, "Open Vault", self.open_vault_folder).pack(fill="x")

        self.watcher_badge = ctk.CTkLabel(self.sidebar, text="●  watcher on",
                                          font=(F_SANS, 10, "bold"), text_color=ACCENT)
        self.watcher_badge.grid(row=5, column=0, sticky="w", padx=20, pady=(8, 14))

    def _on_project_change(self, val):
        if val == "(no projects)":
            return
        self.active_project = val
        save_active_project(val)

    def _show_view(self, key):
        for v in self.views.values():
            v.grid_remove()
        self.views[key].grid(row=0, column=0, sticky="nsew")
        for k, b in self._nav_buttons.items():
            b.configure(fg_color=SURFACE_2 if k == key else "transparent",
                        text_color=TEXT if k == key else TEXT_MUTED)
        if key == "harvest":
            self.refresh_harvest_list()

    # ---------- capture view ----------
    def _build_capture_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=6)
        view.grid_columnconfigure(1, weight=4)
        view.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(hdr, text="Capture", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")
        self.btn_open_last = ghost_button(hdr, "Open last note", self.open_last_note, width=130)
        self.btn_open_last.pack(side="right")
        self.btn_open_last.configure(state="disabled")
        self.status_label = ctk.CTkLabel(hdr, text="Ready", font=(F_SANS, 12), text_color=TEXT_DIM)
        self.status_label.pack(side="right", padx=14)

        left = ctk.CTkFrame(view, fg_color="transparent")
        left.grid(row=1, column=0, sticky="nsew", padx=(28, 12))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(3, weight=1)

        h_label(left, "Keywords / Concepts", 12, TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 6))
        kw_row = ctk.CTkFrame(left, fg_color="transparent")
        kw_row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        kw_row.grid_columnconfigure(0, weight=1)
        self.keyword_input = entry(kw_row, "[[Junction Temperature]], [[IGBT Loss]]")
        self.keyword_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ghost_button(kw_row, "Suggest", self.suggest_concepts, width=90).grid(row=0, column=1)

        h_label(left, "Raw Notes", 12, TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.raw_text_input = ctk.CTkTextbox(left, font=(F_MONO, 13), fg_color=SURFACE, text_color=TEXT,
                                             border_color=BORDER, border_width=1, corner_radius=8)
        self.raw_text_input.grid(row=3, column=0, sticky="nsew")

        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        actions.grid_columnconfigure(0, weight=3)
        actions.grid_columnconfigure(1, weight=2)
        self.btn_daily = primary_button(actions, "Append to Daily Log", self._on_append_daily)
        self.btn_daily.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.btn_note = ghost_button(actions, "New Note …", self._on_new_note)
        self.btn_note.configure(height=42, font=(F_SANS, 13, "bold"))
        self.btn_note.grid(row=0, column=1, sticky="ew")
        m_label(left, f"Under {AI_THRESHOLD} chars saves instantly without the AI.",
                10, TEXT_DIM).grid(row=5, column=0, sticky="w", pady=(8, 0))

        right = ctk.CTkFrame(view, fg_color="transparent")
        right.grid(row=1, column=1, sticky="nsew", padx=(12, 28))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        routing = card(right)
        routing.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        h_label(routing, "Routing", 13).pack(anchor="w", padx=16, pady=(14, 10))
        m_label(routing, "Target (for New Note)").pack(anchor="w", padx=16)
        self.target_option = option(routing, ["New file in active project", "04 Knowledge",
                                              "06 Resources", "Inbox"])
        self.target_option.pack(fill="x", padx=16, pady=(4, 10))
        m_label(routing, "Domain").pack(anchor="w", padx=16)
        self.domain_option = option(routing, ["Auto (AI)"] + list(load_domains().keys()))
        self.domain_option.pack(fill="x", padx=16, pady=(4, 14))
        self.domain_option.set("Auto (AI)")

        known = card(right)
        known.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        h_label(known, "Already in your brain", 13).pack(anchor="w", padx=16, pady=(14, 6))
        self.known_label = ctk.CTkLabel(known, text="—", font=(F_SANS, 11), text_color=TEXT_DIM,
                                        justify="left", anchor="w", wraplength=300)
        self.known_label.pack(anchor="w", fill="x", padx=16, pady=(0, 14))

        img_card = card(right)
        img_card.grid(row=2, column=0, sticky="nsew")
        img_card.grid_rowconfigure(2, weight=1)
        img_card.grid_columnconfigure(0, weight=1)
        img_hdr = ctk.CTkFrame(img_card, fg_color="transparent")
        img_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        h_label(img_hdr, "Snip / Image", 13).pack(side="left")
        self.btn_remove_img = ctk.CTkButton(img_hdr, text="Clear", width=60, height=24,
                                            font=(F_SANS, 11), fg_color="transparent",
                                            hover_color=SURFACE_2, text_color=DANGER,
                                            command=self.clear_image, corner_radius=4)
        img_btns = ctk.CTkFrame(img_card, fg_color="transparent")
        img_btns.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        img_btns.grid_columnconfigure(0, weight=1)
        ghost_button(img_btns, "Paste (Ctrl+V)", self.paste_from_clipboard).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ghost_button(img_btns, "Attach", self.select_image, width=90).grid(row=0, column=1)
        self.image_preview = ctk.CTkLabel(img_card, text="No image attached", font=(F_SANS, 11),
                                          fg_color=BG, text_color=TEXT_DIM, corner_radius=6)
        self.image_preview.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.views["capture"] = view

    # ---------- harvest ----------
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
        ctk.CTkLabel(view, text="Concept cards flagged status: incubating, across all projects.",
                     font=(F_SANS, 12), text_color=TEXT_DIM).grid(row=0, column=0, sticky="sw",
                                                                  padx=28, pady=(0, 16))
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
        stale_cutoff = time.time() - HARVEST_STALE_DAYS * 86400
        for item in items:
            row = card(self.harvest_scroll)
            row.pack(fill="x", pady=6, padx=6)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=16, pady=12)
            ctk.CTkLabel(info, text=item["concept"], font=(F_SANS, 14, "bold"),
                         text_color=TEXT).pack(anchor="w")
            try:
                stale = time.mktime(time.strptime(item["created"], "%Y-%m-%d")) < stale_cutoff
            except Exception:
                stale = False
            meta = f"{item['project']}  ·  {item['domain'] or 'no domain'}  ·  {item['created']}"
            ctk.CTkLabel(info, text=meta + ("   ⚠ stale" if stale else ""), font=(F_SANS, 11),
                         text_color=WARN if stale else TEXT_DIM).pack(anchor="w", pady=(2, 0))
            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.pack(side="right", padx=12, pady=10)
            ctk.CTkButton(btns, text="Promote", width=90, height=32, font=(F_SANS, 12, "bold"),
                          fg_color=ACCENT, hover_color=ACCENT_HOV, text_color=ACCENT_INK,
                          corner_radius=6, command=lambda i=item: self._promote(i)).pack(side="left", padx=3)
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
        self._log(f"gist · {item['concept']}")
        self.refresh_harvest_list()

    def _discard(self, item):
        try:
            os.remove(item["path"])
            self._log(f"discard · {item['concept']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.refresh_harvest_list()

    def _promote(self, item):
        if not self.client:
            messagebox.showwarning("No API key", "Set GEMINI_API_KEY in _meta/.env to promote.")
            return

        def worker():
            try:
                from google.genai import types
                self._set_status(f"promoting {item['concept']}…", INFO)
                prompt = (f"Rewrite this incubating concept card as an evergreen Knowledge Base article "
                          f"about '{item['concept']}'. Strip project-specific references, keep equations, "
                          f"add a generalized definition and typical examples. Frontmatter must set "
                          f"type: concept, folder: '04 Knowledge', domain: '{item['domain']}'.\n\n{item['body']}")
                resp = self.client.models.generate_content(
                    model=self.model, contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=get_system_prompt("")))
                domain = item["domain"] or ""
                dest_dir = os.path.join(KNOWLEDGE_DIR, domain) if domain else KNOWLEDGE_DIR
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, f"{safe_filename(item['concept'])}.md")
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(clean_codefence(resp.text))
                append_registry(item["concept"], domain, item["project"])
                try:
                    os.remove(item["path"])
                except Exception:
                    pass
                self._log(f"promoted · {item['concept']} -> 04 Knowledge/{domain}")
                self._set_status("promoted", ACCENT)
                self.after(0, self.refresh_harvest_list)
            except Exception as e:
                self._set_status("promote failed", DANGER)
                messagebox.showerror("Promote failed", str(e))

        threading.Thread(target=worker, daemon=True).start()

    # ---------- sync ----------
    def _build_sync_view(self):
        view = ctk.CTkFrame(self.main, fg_color=BG)
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(1, weight=1)
        hdr = ctk.CTkFrame(view, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 16))
        ctk.CTkLabel(hdr, text="Sync Log", font=(F_SANS, 22, "bold"), text_color=TEXT).pack(side="left")
        ghost_button(hdr, "Toggle Watcher", self.toggle_watcher, width=140).pack(side="right")
        self.watcher_log_box = ctk.CTkTextbox(view, font=(F_MONO, 12), fg_color=SURFACE,
                                              text_color=TEXT_MUTED, border_color=BORDER,
                                              border_width=1, corner_radius=8)
        self.watcher_log_box.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 24))
        self._log("watcher initialized · monitoring Inbox/")
        self.views["sync"] = view

    # ============================================================
    # QUICK CAPTURE (hotkey)
    # ============================================================

    def setup_hotkeys(self):
        if sys.platform != "win32":
            self._log("hotkeys are Windows-only — skipped")
            return
        bindings = {
            1: (MOD_CONTROL | MOD_ALT, VK_K, lambda: self.after(0, self.show_quick_capture)),
            2: (MOD_CONTROL | MOD_ALT | MOD_SHIFT, VK_K, lambda: self.after(0, self._restore_main)),
        }
        HotkeyListener(bindings).start()
        self._log("hotkeys · Ctrl+Alt+K capture · Ctrl+Alt+Shift+K show window")

    def _make_tray_image(self):
        """Small green square with a 'K' — no icon asset needed."""
        size = 64
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((2, 2, size - 2, size - 2), radius=14, fill=ACCENT)
        d.text((size / 2, size / 2), "K", fill=ACCENT_INK, anchor="mm")
        return img

    def setup_tray(self):
        """Closing the window hides it; the app keeps running so the hotkey stays live.
        Quit only from this menu (or Ctrl+C in a console launch)."""
        if not HAS_TRAY or sys.platform != "win32":
            if not HAS_TRAY:
                self._log("pystray not installed — closing the window will quit the app")
            return

        menu = pystray.Menu(
            pystray.MenuItem("Show", lambda: self.after(0, self._restore_main), default=True),
            pystray.MenuItem("Capture (Ctrl+Alt+K)", lambda: self.after(0, self.show_quick_capture)),
            pystray.MenuItem("Quit K-OS", lambda: self.after(0, self._quit)),
        )
        self.tray_icon = pystray.Icon("kos_capture_hub", self._make_tray_image(), "K-OS Capture Hub", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _restore_main(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def show_quick_capture(self):
        """Borderless one-liner near the top of the screen. Enter saves, Esc cancels."""
        if self._quick_win is not None and self._quick_win.winfo_exists():
            self._quick_win.lift()
            self._quick_win.focus_force()
            return
        if not self.active_project:
            self._restore_main()
            messagebox.showwarning("No project", "Pick an active project first.")
            return

        win = ctk.CTkToplevel(self)
        win.configure(fg_color=BORDER)
        win.attributes("-topmost", True)
        win.overrideredirect(True)
        w, h = 640, 104
        win.geometry(f"{w}x{h}+{(win.winfo_screenwidth() - w) // 2}+150")
        # CustomTkinter re-applies window decorations after init; stamp it again.
        win.after(10, lambda: win.overrideredirect(True))

        inner = ctk.CTkFrame(win, fg_color=SURFACE, corner_radius=10)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        ctk.CTkLabel(inner, text=f"→  {self.active_project}  ·  Daily Log",
                     font=(F_SANS, 11, "bold"), text_color=ACCENT).pack(anchor="w", padx=16, pady=(10, 4))
        box = ctk.CTkEntry(inner, height=34, font=(F_MONO, 13), fg_color=BG,
                           border_color=BORDER, text_color=TEXT,
                           placeholder_text="what happened?")
        box.pack(fill="x", padx=16)
        ctk.CTkLabel(inner, text="Enter save   ·   Shift+Enter format with AI   ·   Esc cancel",
                     font=(F_MONO, 9), text_color=TEXT_DIM).pack(anchor="w", padx=16, pady=(6, 10))

        def close():
            self._quick_win = None
            win.destroy()

        def submit(use_ai):
            text = box.get().strip()
            close()
            if text:
                self.quick_save(text, use_ai=use_ai)

        box.bind("<Return>", lambda e: submit(False))
        box.bind("<Shift-Return>", lambda e: submit(True))
        win.bind("<Escape>", lambda e: close())
        box.bind("<Escape>", lambda e: close())
        self._quick_win = win
        win.after(60, box.focus_force)

    def quick_save(self, text, use_ai=False):
        threading.Thread(target=self._save_daily, args=(text, use_ai, None), daemon=True).start()

    # ============================================================
    # SAVE PATHS
    # ============================================================

    def _extract_concepts(self, text, ai_output=None):
        """Concepts from the AI's frontmatter if present, else the [[wikilinks]] you typed."""
        raw = []
        if ai_output:
            m = re.search(r"extracted_concepts:\s*\[(.*?)\]", ai_output, re.IGNORECASE | re.DOTALL)
            if m:
                raw = m.group(1).split(",")
        if not raw:
            raw = WIKILINK_RE.findall(text or "")
        raw += WIKILINK_RE.findall(self.keyword_input.get() if hasattr(self, "keyword_input") else "")
        return resolve_concepts(raw)

    def _handle_concepts(self, concepts, domain, source_text, source_ref):
        """Count mentions, report what you already know, spawn cards at the threshold."""
        if not concepts or not self.active_project:
            return
        known = []
        for c in concepts:
            kind, path = find_existing_concept(c)
            if kind:
                known.append(f"{c} — {'Knowledge' if kind == 'knowledge' else 'incubating'}")
        ready = record_mentions(concepts, self.active_project)
        created = []
        for c in ready:
            if create_concept_card(self.active_project, c, domain, source_text, source_ref):
                created.append(c)
        if created:
            self._log(f"  + card: {', '.join(created)}")
        if known:
            self._log(f"  ↳ already known: {', '.join(known)}")
        self.after(0, lambda: self.known_label.configure(
            text="\n".join(known) if known else "nothing matched — all new",
            text_color=INFO if known else TEXT_DIM))

    def _save_daily(self, text, use_ai, image):
        """Short + no image -> raw append, no API call. Otherwise let the AI format it."""
        try:
            if not self.active_project:
                self._set_status("no active project", WARN)
                return
            wants_ai = use_ai or image is not None or len(text) >= AI_THRESHOLD
            body, ai_out = text, None

            if wants_ai and self.client:
                self._set_status(f"{self.model} · formatting…", INFO)
                from google.genai import types
                contents = []
                if image is not None:
                    contents.append(image)
                    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
                    fn = f"snip_{int(time.time())}.png"
                    image.save(os.path.join(ATTACHMENTS_DIR, fn), format="PNG")
                    text += f"\n\n![[{fn}]]"
                contents.append(f"Hint: active project '{self.active_project}'.\n\n{text}")
                resp = self.client.models.generate_content(
                    model=self.model, contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=get_system_prompt(self.keyword_input.get().strip())))
                ai_out = clean_codefence(resp.text)
                body = ai_out
            elif wants_ai and not self.client:
                self._set_status("no API key — saved raw", WARN)

            path = append_to_daily_log(self.active_project, body)
            self.last_note_path = path
            self.after(0, lambda: self.btn_open_last.configure(state="normal"))
            tag = "ai" if ai_out else "raw"
            self._log(f"saved ({tag}) · {self.active_project}/Daily Log")
            self._set_status(f"saved to {self.active_project} · Daily Log", ACCENT)

            domain = route_domain(text, parse_frontmatter(ai_out or "").get("domain", ""))
            self._handle_concepts(self._extract_concepts(text, ai_out), domain, text,
                                  f"Daily Log#{time.strftime('%Y-%m-%d')}")
        except Exception as e:
            self._set_status("save failed", DANGER)
            self._log(f"! {e}")

    def _on_append_daily(self):
        text = self.raw_text_input.get("1.0", "end").strip()
        img = self.pil_image_obj or (Image.open(self.image_path) if self.image_path else None)
        if not text and img is None:
            messagebox.showwarning("Empty", "Enter text or attach an image.")
            return
        self._busy(True)
        threading.Thread(target=self._run_then_idle,
                         args=(self._save_daily, text, False, img), daemon=True).start()

    def _on_new_note(self):
        if not self.client:
            messagebox.showwarning("No API key", "New Note needs the AI. Set GEMINI_API_KEY in _meta/.env.")
            return
        text = self.raw_text_input.get("1.0", "end").strip()
        img = self.pil_image_obj or (Image.open(self.image_path) if self.image_path else None)
        if not text and img is None:
            messagebox.showwarning("Empty", "Enter text or attach an image.")
            return
        self._busy(True)
        threading.Thread(target=self._run_then_idle,
                         args=(self._save_note, text, self.target_option.get(), img), daemon=True).start()

    def _run_then_idle(self, fn, *args):
        try:
            fn(*args)
        finally:
            self.after(0, lambda: self._busy(False))

    def _busy(self, on):
        state = "disabled" if on else "normal"
        self.btn_daily.configure(state=state)
        self.btn_note.configure(state=state)

    def _save_note(self, text, target, image):
        try:
            from google.genai import types
            self._set_status(f"{self.model} · structuring…", INFO)
            contents = []
            if image is not None:
                contents.append(image)
                os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
                fn = f"snip_{int(time.time())}.png"
                image.save(os.path.join(ATTACHMENTS_DIR, fn), format="PNG")
                text += f"\n\n![[{fn}]]"
            hint = (f"Hint: domain '{self.domain_option.get()}', "
                    f"active project '{self.active_project}'.\n\n")
            contents.append(hint + text)
            resp = self.client.models.generate_content(
                model=self.model, contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=get_system_prompt(self.keyword_input.get().strip())))
            formatted = clean_codefence(resp.text)
            domain = route_domain(text, parse_frontmatter(formatted).get("domain", ""))

            if target == "New file in active project":
                dest_dir = os.path.join(PROJECTS_DIR, self.active_project or "")
            elif target == "04 Knowledge":
                dest_dir = os.path.join(KNOWLEDGE_DIR, domain) if domain else KNOWLEDGE_DIR
            elif target == "06 Resources":
                dest_dir = os.path.join(RESOURCES_DIR, domain) if domain else RESOURCES_DIR
            else:
                dest_dir = INBOX_DIR
            os.makedirs(dest_dir, exist_ok=True)

            title = safe_filename(parse_frontmatter(formatted).get("title", "")) \
                or f"Note_{time.strftime('%Y%m%d_%H%M%S')}"
            dest = os.path.join(dest_dir, f"{title}.md")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(formatted)

            self.last_note_path = dest
            self.after(0, lambda: self.btn_open_last.configure(state="normal"))
            rel = os.path.relpath(dest, VAULT_DIR)
            self._log(f"saved · {rel}")
            self._set_status(f"saved · {rel}", ACCENT)
            self._handle_concepts(self._extract_concepts(text, formatted), domain, text,
                                  os.path.basename(dest))
        except Exception as e:
            self._set_status("save failed", DANGER)
            messagebox.showerror("Error", str(e))

    def suggest_concepts(self):
        if not self.client:
            messagebox.showwarning("No API key", "Set GEMINI_API_KEY in _meta/.env.")
            return
        text = self.raw_text_input.get("1.0", "end").strip()
        if not text:
            return

        def worker():
            try:
                prompt = ("Extract 2-4 core engineering concepts as [[WikiLinks]], "
                          "comma separated, no other text.\n\n" + text[:2000])
                r = self.client.models.generate_content(model=self.model, contents=prompt)
                val = r.text.strip()
                self.after(0, lambda: (self.keyword_input.delete(0, "end"),
                                       self.keyword_input.insert(0, val)))
            except Exception as e:
                self._log(f"! concepts: {e}")

        threading.Thread(target=worker, daemon=True).start()

    # ============================================================
    # IMAGE / MISC
    # ============================================================

    def paste_from_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, list):
                for f in img:
                    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
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
            print(f"[kos] clipboard: {e}")

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
        h = 180
        w = int(pil_image.size[0] * (h / float(pil_image.size[1])))
        if w > 0:
            self.tk_image = ImageTk.PhotoImage(pil_image.resize((w, h), Image.Resampling.LANCZOS))
            self.image_preview.configure(text="", image=self.tk_image)
            self.btn_remove_img.pack(side="right")

    def clear_image(self):
        self.image_path = self.tk_image = self.pil_image_obj = None
        self.image_preview.configure(text="No image attached", image="")
        self.btn_remove_img.pack_forget()

    def open_vault_folder(self):
        try:
            os.startfile(VAULT_DIR)
        except Exception:
            pass

    def open_last_note(self):
        if self.last_note_path and os.path.exists(self.last_note_path):
            try:
                os.startfile(os.path.abspath(self.last_note_path))
            except Exception:
                pass

    def toggle_watcher(self):
        self.watcher_active = not self.watcher_active
        self.watcher_badge.configure(
            text="●  watcher on" if self.watcher_active else "●  watcher paused",
            text_color=ACCENT if self.watcher_active else WARN)
        self._log("watcher resumed" if self.watcher_active else "watcher paused")

    def _set_status(self, text, color=TEXT_DIM):
        self.after(0, lambda: self.status_label.configure(text=text, text_color=color))

    def _log(self, msg):
        self.log_queue.put(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

    def _poll_log(self):
        while not self.log_queue.empty():
            self.watcher_log_box.insert("end", self.log_queue.get())
            self.watcher_log_box.see("end")
        self.after(250, self._poll_log)

    # ============================================================
    # WATCHDOG
    # ============================================================

    def setup_watchdog(self):
        os.makedirs(INBOX_DIR, exist_ok=True)
        self.observer = Observer()
        self.observer.schedule(KOSWatcherHandler(self._handle_inbox_file), path=INBOX_DIR, recursive=False)
        self.observer.start()

    def _handle_inbox_file(self, file_path):
        if not self.watcher_active or not self.client:
            return
        fn = os.path.basename(file_path)
        self._log(f"inbox · {fn}")
        time.sleep(1)
        try:
            if not os.path.exists(file_path):
                return
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            if not raw.strip() or (raw.startswith("---") and "type:" in raw):
                return
            from google.genai import types
            resp = self.client.models.generate_content(
                model=self.model, contents=raw,
                config=types.GenerateContentConfig(system_instruction=get_system_prompt("")))
            formatted = clean_codefence(resp.text)
            fm = parse_frontmatter(formatted)
            domain = route_domain(raw, fm.get("domain", ""))
            folder = fm.get("folder", "").strip("'\"")

            if folder == "04 Knowledge":
                dest_dir = os.path.join(KNOWLEDGE_DIR, domain) if domain else KNOWLEDGE_DIR
            elif folder == "06 Resources":
                dest_dir = os.path.join(RESOURCES_DIR, domain) if domain else RESOURCES_DIR
            elif self.active_project:
                append_to_daily_log(self.active_project, formatted)
                try:
                    os.remove(file_path)
                except Exception:
                    pass
                self._log(f"  -> {self.active_project}/Daily Log")
                self._handle_concepts(self._extract_concepts(raw, formatted), domain, raw, f"Inbox/{fn}")
                return
            else:
                dest_dir = INBOX_DIR

            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, f"Idea_{time.strftime('%Y%m%d_%H%M%S')}.md")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(formatted)
            if os.path.abspath(file_path) != os.path.abspath(dest):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            self._log(f"  -> {os.path.relpath(dest, VAULT_DIR)}")
            self._handle_concepts(self._extract_concepts(raw, formatted), domain, raw, f"Inbox/{fn}")
        except Exception as e:
            self._log(f"  ! {e}")

    def on_closing(self):
        """The window close button hides to tray instead of quitting, so the
        Ctrl+Alt+K hotkey and Inbox watcher stay alive. Quit from the tray menu."""
        if self.tray_icon is not None:
            self.withdraw()
            self._log("minimized to tray · right-click the K-OS icon to reopen or quit")
        else:
            self._quit()

    def _quit(self):
        if getattr(self, "observer", None) and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        if self.tray_icon is not None:
            self.tray_icon.stop()
        self.destroy()


if __name__ == "__main__":
    for d in (PROJECTS_DIR, KNOWLEDGE_DIR, RESOURCES_DIR, INBOX_DIR, META_DIR):
        os.makedirs(d, exist_ok=True)
    KOSApp().mainloop()
