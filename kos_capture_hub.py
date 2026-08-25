import customtkinter as ctk
import os
import time
import re
import threading
import queue
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
from google import genai
from google.genai import types
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------------- CONFIGURATION ----------------
API_KEY = "YOUR_API_KEY_HERE"

# Standard Vault Directories
VAULT_DIR = r"."
PROJECTS_DIR = os.path.join(VAULT_DIR, "03 Projects")
KNOWLEDGE_DIR = os.path.join(VAULT_DIR, "04 Knowledge")
RESOURCES_DIR = os.path.join(VAULT_DIR, "06 Resources")
INBOX_DIR = os.path.join(VAULT_DIR, "Inbox")
ATTACHMENTS_DIR = os.path.join(VAULT_DIR, "Attachments")
INCUBATOR_FILE = os.path.join(VAULT_DIR, "incubator_state.json")

def load_incubator_state():
    if os.path.exists(INCUBATOR_FILE):
        try:
            with open(INCUBATOR_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_incubator_state(state):
    try:
        with open(INCUBATOR_FILE, "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"Error saving incubator state: {e}")

def add_incubator_concepts(project, text, concepts):
    state = load_incubator_state()
    for concept in concepts:
        # Check if already exists
        exists = any(item.get("concept") == concept and item.get("project") == project for item in state)
        if not exists:
            state.append({
                "concept": concept,
                "project": project,
                "source_text": text,
                "timestamp": time.time()
            })
    save_incubator_state(state)

def get_system_prompt(manual_keywords=""):
    prompt = '''
You are the reasoning layer for an engineering Knowledge Operating System (K-OS) based on Nick Milo's Ideaverse (LYT Framework). 
Your job is to take raw, messy input - text and/or images (like Ansys thermal gradients, MATLAB vibration plots, heat sink designs, or test bench photos) - and format it into clean, structured Markdown notes that seamlessly bridge Projects (Efforts) to Knowledge (Atlas).

Core Rules:

1. Output Format: Output ONLY valid Markdown text with YAML frontmatter. No conversational chatter.

2. ACE Framework Frontmatter:
   Include YAML frontmatter with these exact keys:
   - type: (e.g., engineering_note, dyno_log, simulation_analysis, design_review, resource, concept)
   - domain: (e.g., thermal, vibrations, solid_mechanics, power_electronics, cfd)
   - project: (project name, or 'none')
   - date: (YYYY-MM-DD)
   - folder: MUST be exactly one of: '03 Projects', '04 Knowledge', or '06 Resources'
   - extracted_concepts: list of atomic engineering concept names extracted from this note (e.g., [Thermal Impedance, IGBT Conduction Loss, Modulation Index])

3. Project-to-Knowledge Pipeline:
   - If the note represents active project data, test bench results, or dyno logs -> set folder to '03 Projects'.
   - If the note represents a general reusable engineering principle, formula, or core concept -> set folder to '04 Knowledge'.
   - Ensure reusable concepts discovered during project work are explicitly named in `extracted_concepts`.

4. Ideaverse Keyword & Link Generation Rules:
   - ATOMIC NOUN LINKS ONLY: Wrap ONLY standardized, title-cased singular/plural noun phrases representing atomic technical concepts, parameters, physical laws, software tools, or hardware components in [[WikiLink]] syntax (e.g., [[Junction Temperature]], [[IGBT]], [[Modulation Index]], [[FEA]], [[Thermal Resistance]], [[SVPWM]]).
   - DO NOT LINK: Verbs, action phrases, generic words, or full sentences (e.g., NEVER link [[implementing lookup tables]] or [[testing today]]).
   - INLINE HORIZONTAL LINKS: Embed [[WikiLinks]] directly within prose sentences where technical terms naturally appear.
   - ATLAS VERTICAL CONNECTIONS: End the note with an '## Atlas Connections' section linking ONLY to top-level domain MOCs (Maps of Content) like [[Power Electronics]], [[Thermal Management]], [[Heat Transfer]], [[Motor Control]].

5. Technical & Image Accuracy:
   - Act as an expert mechanical/electrical engineer.
   - Accurately parse math formulas using LaTeX ($...$ or $$...$$).
   - Integrate visual data summaries (max temperatures, flow anomalies, thermal time constants) if images are attached.

6. PRESERVE INFORMATION (NO OVER-SUMMARIZATION):
   - You MUST retain all technical details, derivations, thoughts, and nuance from the user's raw input.
   - Do NOT heavily summarize or omit original information. Reorganize and format for clarity using Markdown headers and lists, but keep the original length and detail intact.
'''
    if manual_keywords:
        prompt += f"\n\nCRITICAL INSTRUCTION FOR KEYWORDS:\nThe user has manually provided these exact keywords: {manual_keywords}\nYou MUST inject these manual keywords into the text where appropriate, ensuring they appear as exact [[WikiLinks]] in the prose AND in the YAML frontmatter `extracted_concepts` list."
    return prompt

class KOSWatcherHandler(FileSystemEventHandler):
    """Background Watchdog Event Handler for Inbox directory."""
    def __init__(self, process_callback):
        super().__init__()
        self.process_callback = process_callback
        self.processed_files = set()

    def on_created(self, event):
        self._handle_event(event)

    def on_modified(self, event):
        self._handle_event(event)

    def _handle_event(self, event):
        if event.is_directory or not event.src_path.endswith(('.txt', '.md')):
            return

        filename = os.path.basename(event.src_path)
        if filename.startswith("Idea_") or filename.startswith(".") or filename in self.processed_files:
            return

        self.processed_files.add(filename)
        threading.Thread(target=self.process_callback, args=(event.src_path,), daemon=True).start()

class KOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        
        self.title("K-OS Intelligence Hub • Thinking Visualized")
        self.geometry("1100x850")
        self.minsize(980, 750)
        self.configure(fg_color="#0B0E14") # Cyberpunk Dark Background

        self.client = genai.Client(api_key=API_KEY)
        self.log_queue = queue.Queue()
        self.watcher_active = True
        self.image_path = None
        self.tk_image = None
        self.pil_image_obj = None # To store direct clipboard image

        self.setup_ui()
        self.setup_watchdog()

        self.after(100, self.poll_log_queue)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind Ctrl+V to paste from clipboard
        self.bind("<Control-v>", lambda e: self.paste_from_clipboard())

    def setup_ui(self):
        # ---------------- TOP HEADER BAR ----------------
        self.header_frame = ctk.CTkFrame(self, fg_color="#111622", corner_radius=12, height=70, border_width=1, border_color="#232B3E")
        self.header_frame.pack(fill="x", padx=16, pady=(14, 8))
        self.header_frame.pack_propagate(False)

        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.pack(side="left", padx=18, pady=10)

        self.title_label = ctk.CTkLabel(
            title_box, 
            text="⚡ K-OS INTELLIGENCE HUB", 
            font=("Segoe UI Variable", 22, "bold"), 
            text_color="#00D2FF"
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            title_box, 
            text="Intake Engine • Neural Capture Studio", 
            font=("Segoe UI Variable", 12), 
            text_color="#8F96A3"
        )
        self.subtitle_label.pack(anchor="w")

        header_actions = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_actions.pack(side="right", padx=16, pady=12)

        self.btn_open_vault = ctk.CTkButton(
            header_actions,
            text="📂 Open Vault",
            width=100,
            height=32,
            font=("Segoe UI Variable", 12, "bold"),
            fg_color="#232B3E",
            hover_color="#333D56",
            command=self.open_vault_folder
        )
        self.btn_open_vault.pack(side="left", padx=4)

        # ---------------- TABS ----------------
        self.tabview = ctk.CTkTabview(
            self, 
            fg_color="#111622",
            segmented_button_fg_color="#0B0E14",
            segmented_button_selected_color="#232B3E",
            segmented_button_selected_hover_color="#333D56",
            segmented_button_unselected_color="#0B0E14",
            text_color="#00D2FF",
            corner_radius=12
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        self.tab_studio = self.tabview.add("⚡ Capture Studio")
        self.tab_preview = self.tabview.add("👁️ Markdown Preview & Inspector")
        self.tab_sync = self.tabview.add("📡 Live Sync & History")
        self.tab_harvest = self.tabview.add("🌾 Knowledge Harvest")

        self.setup_studio_tab()
        self.setup_preview_tab()
        self.setup_sync_tab()
        self.setup_harvest_tab()

    def setup_studio_tab(self):
        self.tab_studio.grid_columnconfigure(0, weight=6)
        self.tab_studio.grid_columnconfigure(1, weight=4)
        self.tab_studio.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: DATA INTAKE
        # ==========================================
        left_panel = ctk.CTkFrame(self.tab_studio, fg_color="transparent")
        left_panel.grid(row=0, column=0, padx=(0, 8), pady=0, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(7, weight=1)

        # Note Title
        title_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        title_row.grid(row=0, column=0, sticky="ew", pady=(4, 8))
        
        ctk.CTkLabel(title_row, text="Note Title:", font=("Segoe UI Variable", 13, "bold"), text_color="#A0AEC0").pack(side="left")
        self.btn_suggest_title = ctk.CTkButton(
            title_row, text="✨ Suggest Title", width=100, height=24, 
            fg_color="#8B5CF6", hover_color="#7C3AED", font=("Segoe UI Variable", 11, "bold"),
            command=self.suggest_title
        )
        self.btn_suggest_title.pack(side="right")
        
        self.title_input = ctk.CTkEntry(
            left_panel, placeholder_text="Leave blank for auto-timestamp (e.g., IGBT_Thermal_20260818.md)",
            height=36, font=("Consolas", 12), fg_color="#0B0E14", border_color="#232B3E"
        )
        self.title_input.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        # Manual Keywords
        keyword_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        keyword_row.grid(row=2, column=0, sticky="ew", pady=(4, 8))
        
        ctk.CTkLabel(keyword_row, text="Manual Keywords / Concepts:", font=("Segoe UI Variable", 13, "bold"), text_color="#A0AEC0").pack(side="left")
        self.btn_suggest_concepts = ctk.CTkButton(
            keyword_row, text="✨ Suggest Concepts", width=120, height=24, 
            fg_color="#232B3E", hover_color="#333D56", text_color="#00D2FF", font=("Segoe UI Variable", 11, "bold"),
            command=self.suggest_concepts
        )
        self.btn_suggest_concepts.pack(side="right")
        
        self.keyword_input = ctk.CTkEntry(
            left_panel, placeholder_text="e.g., [[Junction Temperature]], [[IGBT Loss]]",
            height=36, font=("Consolas", 12), fg_color="#0B0E14", border_color="#232B3E"
        )
        self.keyword_input.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        # Raw Text Area
        text_lbl_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        text_lbl_row.grid(row=4, column=0, sticky="ew", pady=(4, 4))
        ctk.CTkLabel(text_lbl_row, text="Raw Engineering Notes:", font=("Segoe UI Variable", 13, "bold"), text_color="#A0AEC0").pack(side="left")

        self.raw_text_input = ctk.CTkTextbox(
            left_panel, font=("JetBrains Mono", 12), fg_color="#0B0E14", border_color="#232B3E", border_width=1, corner_radius=8
        )
        self.raw_text_input.grid(row=5, column=0, sticky="nsew", pady=(0, 12))

        # Push Action
        self.btn_process = ctk.CTkButton(
            left_panel, 
            text="⚡ Structure & Push to Vault", 
            font=("Segoe UI Variable", 15, "bold"), 
            height=50,
            fg_color="#00D2FF",
            hover_color="#00B4DB",
            text_color="#0B0E14",
            corner_radius=8,
            command=self.process_note
        )
        self.btn_process.grid(row=6, column=0, sticky="ew", pady=4)

        self.status_label = ctk.CTkLabel(left_panel, text="Ready to capture", font=("Segoe UI Variable", 12), text_color="#94A3B8")
        self.status_label.grid(row=7, column=0, pady=(4, 0), sticky="n")

        # ==========================================
        # RIGHT PANEL: SELECTORS & MULTIMODAL
        # ==========================================
        right_panel = ctk.CTkFrame(self.tab_studio, fg_color="transparent")
        right_panel.grid(row=0, column=1, padx=(8, 0), pady=0, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)

        # Selectors Card
        selectors_card = ctk.CTkFrame(right_panel, fg_color="#161C2B", corner_radius=12, border_width=1, border_color="#232B3E")
        selectors_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        
        ctk.CTkLabel(selectors_card, text="🗂️ Routing & Meta", font=("Segoe UI Variable", 14, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=16, pady=(12, 4))

        # Domain
        ctk.CTkLabel(selectors_card, text="Engineering Domain:", font=("Segoe UI Variable", 11), text_color="#8F96A3").pack(anchor="w", padx=16, pady=(4, 0))
        self.domain_option = ctk.CTkOptionMenu(
            selectors_card, 
            values=["Auto-Detect (AI)", "Thermal Management & Heat Transfer", "CFD & Aerodynamics", "FEA & Structural / Vibrations", "Power Electronics & ETM", "Motor Control & Dynamics", "Testing & Validation / Dyno", "Materials & Manufacturing", "General Engineering & Math"],
            height=32, font=("Segoe UI Variable", 12), fg_color="#232B3E", button_color="#00D2FF", button_hover_color="#00B4DB"
        )
        self.domain_option.pack(fill="x", padx=16, pady=(0, 10))

        # Note Type
        ctk.CTkLabel(selectors_card, text="Note Type Template:", font=("Segoe UI Variable", 11), text_color="#8F96A3").pack(anchor="w", padx=16, pady=(0, 0))
        self.type_option = ctk.CTkOptionMenu(
            selectors_card, 
            values=["Auto-Detect", "Engineering Note (Theory/Concept)", "Simulation Analysis (FEA/CFD)", "Test Bench & Dyno Log", "Design Review / Teardown", "Mathematical Derivation", "Fleeting Quick Note"],
            height=32, font=("Segoe UI Variable", 12), fg_color="#232B3E", button_color="#00D2FF", button_hover_color="#00B4DB"
        )
        self.type_option.pack(fill="x", padx=16, pady=(0, 10))

        # Target Folder
        ctk.CTkLabel(selectors_card, text="Target Vault Location:", font=("Segoe UI Variable", 11), text_color="#8F96A3").pack(anchor="w", padx=16, pady=(0, 0))
        self.project_option = ctk.CTkOptionMenu(
            selectors_card, values=["Inbox"],
            height=32, font=("Segoe UI Variable", 12), fg_color="#232B3E", button_color="#00D2FF", button_hover_color="#00B4DB"
        )
        self.project_option.pack(fill="x", padx=16, pady=(0, 10))
        self.refresh_projects()

        # Model Selector
        ctk.CTkLabel(selectors_card, text="AI Model (Reasoning Engine):", font=("Segoe UI Variable", 11), text_color="#8F96A3").pack(anchor="w", padx=16, pady=(0, 0))
        self.model_option = ctk.CTkOptionMenu(
            selectors_card, 
            values=["gemini-3.7-flash", "gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.5-pro"],
            height=32, font=("Segoe UI Variable", 12), fg_color="#232B3E", button_color="#8B5CF6", button_hover_color="#7C3AED"
        )
        self.model_option.pack(fill="x", padx=16, pady=(0, 16))
        self.model_option.set("gemini-3.6-flash")

        # Telemetry Card
        telemetry_card = ctk.CTkFrame(right_panel, fg_color="#161C2B", corner_radius=12, border_width=1, border_color="#232B3E")
        telemetry_card.grid(row=1, column=0, sticky="nsew", pady=0)
        right_panel.grid_rowconfigure(1, weight=1)
        telemetry_card.grid_columnconfigure(0, weight=1)
        telemetry_card.grid_rowconfigure(2, weight=1)

        t_hdr = ctk.CTkFrame(telemetry_card, fg_color="transparent")
        t_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 4))
        ctk.CTkLabel(t_hdr, text="📋 Multimodal Snip", font=("Segoe UI Variable", 14, "bold"), text_color="#FFFFFF").pack(side="left")
        
        self.btn_remove_img = ctk.CTkButton(
            t_hdr, text="✕ Clear", width=60, height=22, font=("Segoe UI Variable", 11),
            fg_color="#3B1C1C", hover_color="#522424", text_color="#FF8080", command=self.clear_image
        )

        t_btns = ctk.CTkFrame(telemetry_card, fg_color="transparent")
        t_btns.grid(row=1, column=0, sticky="ew", padx=16, pady=(4, 8))
        
        self.btn_paste = ctk.CTkButton(
            t_btns, text="📋 Paste Snip (Ctrl+V)", height=32, font=("Segoe UI Variable", 12, "bold"),
            fg_color="#232B3E", hover_color="#333D56", command=self.paste_from_clipboard
        )
        self.btn_paste.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_select_img = ctk.CTkButton(
            t_btns, text="📎 Attach", height=32, width=80, font=("Segoe UI Variable", 12),
            fg_color="#232B3E", hover_color="#333D56", command=self.select_image
        )
        self.btn_select_img.pack(side="right", padx=(4, 0))

        self.image_preview = ctk.CTkLabel(
            telemetry_card, 
            text="[ No Image Attached ]\nSupports direct clipboard paste.", 
            font=("Segoe UI Variable", 11), fg_color="#0B0E14", text_color="#64748B", corner_radius=8
        )
        self.image_preview.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))


    def setup_preview_tab(self):
        self.tab_preview.grid_columnconfigure(0, weight=1)
        self.tab_preview.grid_rowconfigure(0, weight=1)

        self.preview_text = ctk.CTkTextbox(
            self.tab_preview, font=("JetBrains Mono", 13), fg_color="#0B0E14", text_color="#A0AEC0",
            border_color="#232B3E", border_width=1, corner_radius=8
        )
        self.preview_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        btn_frame = ctk.CTkFrame(self.tab_preview, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))

        self.btn_copy_md = ctk.CTkButton(
            btn_frame, text="📋 Copy Markdown", font=("Segoe UI Variable", 12, "bold"),
            fg_color="#232B3E", hover_color="#333D56", command=self.copy_preview
        )
        self.btn_copy_md.pack(side="left")

        self.btn_open_md = ctk.CTkButton(
            btn_frame, text="👁️ Open in Obsidian", font=("Segoe UI Variable", 12, "bold"),
            fg_color="#8B5CF6", hover_color="#7C3AED", command=self.open_last_note
        )
        self.btn_open_md.pack(side="right")
        self.btn_open_md.configure(state="disabled")
        self.last_note_path = None


    def setup_sync_tab(self):
        self.tab_sync.grid_columnconfigure(0, weight=1)
        self.tab_sync.grid_rowconfigure(1, weight=1)

        mon_hdr = ctk.CTkFrame(self.tab_sync, fg_color="transparent")
        mon_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=12)

        ctk.CTkLabel(mon_hdr, text="📡 Background Sync Monitor", font=("Segoe UI Variable", 16, "bold"), text_color="#FFFFFF").pack(side="left")

        self.btn_toggle_watcher = ctk.CTkButton(
            mon_hdr, text="Pause Watcher", width=120, height=30, font=("Segoe UI Variable", 12, "bold"),
            fg_color="#232B3E", hover_color="#333D56", command=self.toggle_watcher
        )
        self.btn_toggle_watcher.pack(side="right")
        
        self.watcher_badge = ctk.CTkLabel(
            mon_hdr, text="🟢 ACTIVE", font=("Segoe UI Variable", 11, "bold"),
            fg_color="#102A24", text_color="#10B981", corner_radius=8, padx=12, pady=4
        )
        self.watcher_badge.pack(side="right", padx=16)

        self.watcher_log_box = ctk.CTkTextbox(
            self.tab_sync, font=("Consolas", 12), fg_color="#0B0E14", text_color="#94A3B8",
            border_color="#232B3E", border_width=1, corner_radius=8
        )
        self.watcher_log_box.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.log_watcher_msg("⚡ K-OS Watcher Engine initialized. Monitoring Inbox...")


    # ---------------- FUNCTIONALITY ----------------

    def setup_harvest_tab(self):
        self.tab_harvest.grid_columnconfigure(0, weight=1)
        self.tab_harvest.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(self.tab_harvest, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        ctk.CTkLabel(hdr, text="🌾 Incubator & Triage", font=("Segoe UI Variable", 16, "bold"), text_color="#FFFFFF").pack(side="left")

        self.btn_refresh_harvest = ctk.CTkButton(
            hdr, text="🔄 Refresh", width=100, height=30, font=("Segoe UI Variable", 12, "bold"),
            fg_color="#232B3E", hover_color="#333D56", command=self.refresh_harvest_list
        )
        self.btn_refresh_harvest.pack(side="right")

        self.harvest_scroll = ctk.CTkScrollableFrame(self.tab_harvest, fg_color="#0B0E14", corner_radius=8)
        self.harvest_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        
        # We will populate this on refresh
        self.harvest_items = []
        
        # Initial populate
        self.after(500, self.refresh_harvest_list)

    def refresh_harvest_list(self):
        for widget in self.harvest_scroll.winfo_children():
            widget.destroy()
        
        state = load_incubator_state()
        if not state:
            ctk.CTkLabel(self.harvest_scroll, text="No concepts incubating.", text_color="#94A3B8").pack(pady=20)
            return

        for idx, item in enumerate(state):
            concept = item.get("concept", "Unknown")
            project = item.get("project", "Unknown")
            
            row = ctk.CTkFrame(self.harvest_scroll, fg_color="#161C2B", corner_radius=8)
            row.pack(fill="x", pady=4, padx=4)
            
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=12, pady=8)
            
            ctk.CTkLabel(info_frame, text=concept, font=("Segoe UI Variable", 14, "bold"), text_color="#00D2FF").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Source: {project}", font=("Segoe UI Variable", 11), text_color="#8F96A3").pack(anchor="w")

            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=12, pady=8)
            
            ctk.CTkButton(btn_frame, text="✅ Promote", width=80, fg_color="#10B981", hover_color="#059669", text_color="#000000", command=lambda c=concept, p=project, text=item.get("source_text", ""): self.promote_concept(c, p, text)).pack(side="left", padx=4)
            ctk.CTkButton(btn_frame, text="📦 Keep as Gist", width=100, fg_color="#232B3E", hover_color="#333D56", command=lambda c=concept, p=project: self.remove_from_incubator(c, p)).pack(side="left", padx=4)
            ctk.CTkButton(btn_frame, text="🗑️ Discard", width=70, fg_color="#EF4444", hover_color="#DC2626", text_color="#FFFFFF", command=lambda c=concept, p=project: self.remove_from_incubator(c, p)).pack(side="left", padx=4)

    def remove_from_incubator(self, concept, project):
        state = load_incubator_state()
        state = [item for item in state if not (item.get("concept") == concept and item.get("project") == project)]
        save_incubator_state(state)
        self.refresh_harvest_list()

    def promote_concept(self, concept, project, source_text):
        try:
            self.status_label.configure(text=f"⚡ Synthesizing {concept}...")
            self.update()
            
            prompt = f"Write a comprehensive, standalone Knowledge Base article about the engineering concept '{concept}'. Incorporate the following context gathered from the project '{project}':\n\n{source_text}\n\nUse the required ACE YAML frontmatter with type: concept and folder: '04 Knowledge'."
            model = self.model_option.get()
            resp = self.client.models.generate_content(
                model=model, 
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=get_system_prompt(""))
            )
            
            formatted = resp.text.strip()
            if formatted.startswith("```markdown"): formatted = formatted[11:].strip()
            elif formatted.startswith("```md"): formatted = formatted[5:].strip()
            elif formatted.startswith("```"): formatted = formatted[3:].strip()
            if formatted.endswith("```"): formatted = formatted[:-3].strip()
                
            safe_concept = concept.replace("[[", "").replace("]]", "").replace(" ", "_").replace("/", "")
            dest_dir = os.path.join(VAULT_DIR, "04 Knowledge")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, f"{safe_concept}.md")
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
                
            self.remove_from_incubator(concept, project)
            messagebox.showinfo("Promoted", f"Successfully promoted {concept} to Knowledge Base!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to promote: {e}")
        finally:
            self.status_label.configure(text="Ready")


    def refresh_projects(self):
        self.projects_list = ["Inbox", "04 Knowledge", "06 Resources"]
        try:
            if os.path.exists(PROJECTS_DIR):
                for item in sorted(os.listdir(PROJECTS_DIR)):
                    if os.path.isdir(os.path.join(PROJECTS_DIR, item)):
                        self.projects_list.append(item)
        except Exception as e:
             pass

        if hasattr(self, 'project_option'):
            current_val = self.project_option.get()
            self.project_option.configure(values=self.projects_list)
            if current_val in self.projects_list:
                self.project_option.set(current_val)
            else:
                self.project_option.set(self.projects_list[0])

    def paste_from_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            if img is not None:
                if isinstance(img, list): # file paths copied
                    for f in img:
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                            self.load_image_from_path(f)
                            return
                elif isinstance(img, Image.Image):
                    self.image_path = None
                    self.pil_image_obj = img
                    self.display_image(img)
                    return
            
            # If no image, try getting text
            try:
                text = self.clipboard_get()
                if text:
                    self.raw_text_input.insert("insert", text)
            except:
                pass

        except Exception as e:
            print(f"Clipboard paste error: {e}")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.load_image_from_path(file_path)

    def load_image_from_path(self, file_path):
        self.image_path = file_path
        self.pil_image_obj = None
        try:
            pil_image = Image.open(file_path)
            self.display_image(pil_image)
        except Exception as e:
            self.image_preview.configure(text=f"Error loading image: {e}", image="")

    def display_image(self, pil_image):
        baseheight = 180
        wpercentage = (baseheight / float(pil_image.size[1]))
        wsize = int((float(pil_image.size[0]) * float(wpercentage)))
        if wsize > 0 and baseheight > 0:
            pil_image_resized = pil_image.resize((wsize, baseheight), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(pil_image_resized)
            self.image_preview.configure(text="", image=self.tk_image)
            self.btn_remove_img.pack(side="right")

    def clear_image(self):
        self.image_path = None
        self.tk_image = None
        self.pil_image_obj = None
        self.image_preview.configure(text="[ No Image Attached ]\nSupports direct clipboard paste.", image="")
        self.btn_remove_img.pack_forget()

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
            try:
                os.startfile(os.path.abspath(self.last_note_path))
            except:
                pass

    def log_watcher_msg(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        self.log_queue.put(f"{timestamp} {msg}\n")

    def poll_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.watcher_log_box.insert("end", msg)
            self.watcher_log_box.see("end")
        self.after(200, self.poll_log_queue)

    def toggle_watcher(self):
        if self.watcher_active:
            self.watcher_active = False
            self.watcher_badge.configure(text="🔴 PAUSED", fg_color="#301A1A", text_color="#FF6B6B")
            self.btn_toggle_watcher.configure(text="Resume Watcher")
            self.log_watcher_msg("⏸️ Watcher paused by user.")
        else:
            self.watcher_active = True
            self.watcher_badge.configure(text="🟢 ACTIVE", fg_color="#102A24", text_color="#10B981")
            self.btn_toggle_watcher.configure(text="Pause Watcher")
            self.log_watcher_msg("▶️ Watcher resumed.")

    def setup_watchdog(self):
        os.makedirs(INBOX_DIR, exist_ok=True)
        self.event_handler = KOSWatcherHandler(self.handle_inbox_file_background)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=INBOX_DIR, recursive=False)
        self.observer.start()

    def handle_inbox_file_background(self, file_path):
        if not self.watcher_active:
            return

        filename = os.path.basename(file_path)
        self.log_watcher_msg(f"📥 Inbox Event: {filename}")
        time.sleep(1)

        try:
            if not os.path.exists(file_path):
                return
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()

            if not raw_text.strip(): return
            if raw_text.startswith("---") and ("type:" in raw_text or "domain:" in raw_text): return

            self.log_watcher_msg(f"🧠 Formatting via Background Engine...")
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=raw_text,
                config=types.GenerateContentConfig(
                    system_instruction=get_system_prompt(""),
                )
            )
            formatted_content = response.text
            
            # Clean markdown codeblocks
            formatted_content = formatted_content.strip()
            if formatted_content.startswith("```markdown"):
                formatted_content = formatted_content[11:].strip()
            elif formatted_content.startswith("```md"):
                formatted_content = formatted_content[5:].strip()
            elif formatted_content.startswith("```"):
                formatted_content = formatted_content[3:].strip()
            if formatted_content.endswith("```"):
                formatted_content = formatted_content[:-3].strip()

            target_folder = "04 Knowledge"
            folder_match = re.search(r"folder:\s*(.+)", formatted_content, re.IGNORECASE)
            if folder_match:
                extracted = folder_match.group(1).strip().strip("'").strip('"')
                if extracted in ["03 Projects", "04 Knowledge", "06 Resources"]:
                    target_folder = extracted

            # Extract concepts for Incubator
            concept_match = re.search(r"extracted_concepts:\s*\[(.*?)\]", formatted_content, re.IGNORECASE)
            if concept_match and target_folder == "03 Projects":
                concept_list = [c.strip() for c in concept_match.group(1).split(",") if c.strip()]
                add_incubator_concepts("Inbox_Auto", raw_text, concept_list)

            dest_dir = os.path.join(VAULT_DIR, target_folder)
            os.makedirs(dest_dir, exist_ok=True)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_filename = f"Idea_{timestamp}.md"
            dest_path = os.path.join(dest_dir, new_filename)

            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)

            try:
                if os.path.exists(file_path) and os.path.abspath(file_path) != os.path.abspath(dest_path):
                    os.remove(file_path)
            except: pass
            self.log_watcher_msg(f"✅ Routed -> {target_folder}/{new_filename}")
        except Exception as e:
            self.log_watcher_msg(f"❌ Error: {e}")

    # --- AI Generators ---
    def suggest_title(self):
        text = self.raw_text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Info", "Enter some raw text first to suggest a title.")
            return
            
        self.btn_suggest_title.configure(text="⏳...", state="disabled")
        self.update()
        try:
            prompt = "Generate a concise, professional markdown file title (without extension) for the following engineering note. Only return the title string, max 6 words. Note:\n" + text[:2000]
            model = self.model_option.get()
            resp = self.client.models.generate_content(model=model, contents=prompt)
            self.title_input.delete(0, "end")
            self.title_input.insert(0, resp.text.strip().replace("\"", "").replace("'", ""))
        except Exception as e:
            print(f"Title generation error: {e}")
        finally:
            self.btn_suggest_title.configure(text="✨ Suggest Title", state="normal")

    def suggest_concepts(self):
        text = self.raw_text_input.get("1.0", "end").strip()
        if not text: return
        self.btn_suggest_concepts.configure(text="⏳...", state="disabled")
        self.update()
        try:
            prompt = "Extract 2-4 core engineering concepts or keywords from this text. Return them as a comma separated list of WikiLinks (e.g. [[Concept A]], [[Concept B]]). No other text. Text:\n" + text[:2000]
            model = self.model_option.get()
            resp = self.client.models.generate_content(model=model, contents=prompt)
            self.keyword_input.delete(0, "end")
            self.keyword_input.insert(0, resp.text.strip())
        except Exception as e:
            print(f"Concept extraction error: {e}")
        finally:
            self.btn_suggest_concepts.configure(text="✨ Suggest Concepts", state="normal")

    def process_note(self):
        target = self.project_option.get()
        text = self.raw_text_input.get("1.0", "end").strip()
        custom_title = self.title_input.get().strip()
        keywords = self.keyword_input.get().strip()
        domain = self.domain_option.get()
        note_type = self.type_option.get()
        model_selection = self.model_option.get()
        
        if not text and not self.image_path and not self.pil_image_obj:
            messagebox.showwarning("Input Required", "Please enter raw text or attach/paste an image.")
            return

        self.status_label.configure(text=f"⚡ {model_selection} is structuring...", text_color="#00D2FF")
        self.btn_process.configure(state="disabled", text="⏳ Processing...")
        self.update()

        try:
            contents = []
            image_embed_string = ""
            
            # Context Hints
            hints = f"Hint: User selected Domain: '{domain}'. Template Type: '{note_type}'.\n\n"
            text_payload = hints + text

            img_to_process = None
            if self.pil_image_obj:
                img_to_process = self.pil_image_obj
            elif self.image_path:
                img_to_process = Image.open(self.image_path)

            if img_to_process:
                contents.append(img_to_process)
                os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
                img_name = f"snip_{int(time.time())}.png"
                dest_img_path = os.path.join(ATTACHMENTS_DIR, img_name)
                img_to_process.save(dest_img_path, format="PNG")
                image_embed_string = f"\n\n![[{img_name}]]\n"
            
            if text_payload:
                contents.append(text_payload)

            response = self.client.models.generate_content(
                model=model_selection, 
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=get_system_prompt(keywords),
                )
            )
            
            formatted_content = response.text
            
            # Clean markdown codeblocks
            formatted_content = formatted_content.strip()
            if formatted_content.startswith("```markdown"):
                formatted_content = formatted_content[11:].strip()
            elif formatted_content.startswith("```md"):
                formatted_content = formatted_content[5:].strip()
            elif formatted_content.startswith("```"):
                formatted_content = formatted_content[3:].strip()
            if formatted_content.endswith("```"):
                formatted_content = formatted_content[:-3].strip()
                
            if image_embed_string:
                formatted_content += image_embed_string

            # Determine Destination Directory
            if target == "Inbox":
                dest_dir = INBOX_DIR
            elif target == "04 Knowledge":
                dest_dir = KNOWLEDGE_DIR
            elif target == "06 Resources":
                dest_dir = RESOURCES_DIR
            else:
                dest_dir = os.path.join(PROJECTS_DIR, target)
                
            os.makedirs(dest_dir, exist_ok=True)
            
            if custom_title:
                new_filename = f"{custom_title}.md"
                if not new_filename.endswith(".md"): new_filename += ".md"
            else:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                # Clean domain name for filename if available
                safe_domain = "Note"
                if domain != "Auto-Detect (AI)":
                    safe_domain = domain.split()[0].replace("&", "").replace("/", "")
                new_filename = f"{safe_domain}_{timestamp}.md"
                
            dest_path = os.path.join(dest_dir, new_filename)

            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)

            # Extract concepts for Incubator
            concept_match = re.search(r"extracted_concepts:\s*\[(.*?)\]", formatted_content, re.IGNORECASE)
            if concept_match and target not in ["Inbox", "04 Knowledge", "06 Resources"]:
                concept_list = [c.strip() for c in concept_match.group(1).split(",") if c.strip()]
                add_incubator_concepts(target, text, concept_list)

            self.status_label.configure(text=f"✅ SUCCESS! Note pushed to {target}", text_color="#10B981")
            
            # Update Preview Tab
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", formatted_content)
            self.last_note_path = dest_path
            self.btn_open_md.configure(state="normal")
            
            self.log_watcher_msg(f"📌 Capture saved -> {target}/{new_filename}")
            
            # Switch to preview tab automatically
            self.tabview.set("👁️ Markdown Preview & Inspector")
            
            # Optional: Clear form
            # self.raw_text_input.delete("1.0", "end")
            # self.title_input.delete(0, "end")
            # self.clear_image()
            
        except Exception as e:
             self.status_label.configure(text=f"❌ API Error", text_color="#FF6B6B")
             messagebox.showerror("API Error", f"Failed to process with Gemini:\n{e}")
        finally:
            self.btn_process.configure(state="normal", text="⚡ Structure & Push to Vault")

    def on_closing(self):
        if hasattr(self, 'observer') and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        self.destroy()

if __name__ == "__main__":
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    os.makedirs(INBOX_DIR, exist_ok=True)
    app = KOSApp()
    app.mainloop()
