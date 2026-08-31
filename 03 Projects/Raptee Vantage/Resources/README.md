---
type: folder_readme
project: Raptee Vantage
---

# Resources

External references, links, docs, datasheets.

## Repo
- `CLAUDE.md` — the git-committed team handbook this vault mirrors and extends
- Remote: Raptee-Energy/Raptee-Vantage

## Key config files (in repo root)
| File | Purpose |
|---|---|
| `master_params.json` | parameter master list |
| `intake_config.json` | watch folders + filename patterns |
| `ecosystem.config.js` | PM2 process config — **don't shorten the restart guards** |

## Claude Code tooling for this project

**Skills** (`.claude/skills/`)
| Command | Does |
|---|---|
| `/note` | capture one thing into this vault, mid-work |
| `/eod` | end-of-day triage into Concepts / Experiments / Results / Questions |
| `/ship` | deploy + actually verify health after |
| `/add-param` | add a QC parameter across all 5 layers |

**Subagents** (`.claude/agents/`)
`verdict-tracer` · `db-schema-explorer` · `api-route-finder` · `intake-debugger`

See [[Workflow]] for when each one fires.

## Obsidian MCP connection

Vault reaches Claude Code via the `obsidian-local-rest-api` plugin's MCP server
at `http://127.0.0.1:27123/mcp/`, registered as MCP server `obsidian` in **local
scope**. Only works while Obsidian is open.

⚠️ **`claude mcp list` saying "✔ Connected" does not mean the running session can
use the tools.** The MCP server can be live and registered while the session that
started before it still has no obsidian tools in its toolbox. Symptom: connection
checks all pass, but Claude says the tools aren't available.
**Fix: restart the Claude Code session.** Registering or reconnecting mid-session
is not enough.

Quick check the plugin is alive at all:
```bash
curl http://127.0.0.1:27123/mcp/
# → "Authorization required" means running; connection refused means Obsidian is closed
```

## To add
- [ ] PM2 docs link
- [ ] FastAPI / Next.js version notes
- [ ] EOL station vendor docs
