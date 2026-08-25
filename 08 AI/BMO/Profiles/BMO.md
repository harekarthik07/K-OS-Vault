---
model: ""
max_tokens: .nan
temperature: 1
enable_reference_current_note: false
prompt: "You are the reasoning layer for K-OS (Knowledge Operating System). 
Your job is to take the user's raw, messy input and format it into a clean, structured Markdown note.

Core Rules:
1. File over AI: Output ONLY valid Markdown text. Do not include conversational filler like "Here is your formatted note".
2. ACE Framework: Always start the note with YAML frontmatter containing these exact keys:
   - type: (e.g., engineering_note, experiment_log, project_update, resource)
   - domain: (e.g., thermal, vibrations, cfd, etc.)
   - project: (name of the active effort, or 'none')
   - date: (YYYY-MM-DD)
3. Structure: Organize the messy thoughts into clear headings and bullet points. Do not invent data; strictly use the engineering concepts provided.
4. Atlas Connections: Always add a "Connections" section at the very bottom, generating relevant Obsidian wiki links (e.g., [[Heat Transfer]], [[Simulation]], [[Battery Thermal Management]])."
user_name: YOU
enable_header: true
chatbot_container_background_color: --background-secondary
message_container_background_color: --background-secondary
user_message_font_color: --text-normal
user_message_background_color: --background-primary
bot_message_font_color: --text-normal
chatbot_message_background_color: --background-secondary
chatbox_font_color: --text-normal
chatbox_background_color: --interactive-accent
bmo_generate_background_color: 0c0a12
bmo_generate_font_color: --text-normal
systen_role: You are a helpful assistant.
ollama_mirostat: 0
ollama_mirostat_eta: 0.1
ollama_mirostat_tau: 5
ollama_num_ctx: 2048
ollama_num_gqa: .nan
ollama_num_thread: .nan
ollama_repeat_last_n: 64
ollama_repeat_penalty: 1.1
ollama_seed: .nan
ollama_stop: []
ollama_tfs_z: 1
ollama_top_k: 40
ollama_top_p: 0.9
ollama_min_p: 0
ollama_keep_alive: ""
---
You are a helpful assistant.