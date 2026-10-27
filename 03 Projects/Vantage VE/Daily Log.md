---
type: daily_log
project: Vantage VE
---

# Daily Log — Vantage VE

Append newest at top. One `##` per day.

---

## 2026-10-27
**Did:**
- **Hardened VE auth:** default-deny middleware on every `/api` route except health + login (12 routes were open on the LAN, incl. DBC activate). Login lockout: 5 bad passwords → 15 min, counted from the audit table. Removed admin JWT from `localStorage`. Unknown usernames pay the same bcrypt cost (no account enumeration). `selfcheck_auth.py` covers it.
- Tried **HTTPS on the R&D LAN** (own name-constrained CA + Node TLS proxy on :3443) — then **reverted**: installing a CA on every client PC was too much friction.
- Unified "VANTAGE - VE" branding typography.
- **One LabBar for every lab** (breadcrumb · context chips · filters · ≤2 actions, rest in overflow). Removed the tab rows that duplicated the sidebar; made it one full-bleed sticky strip in thermal, road and powertrain. Dropped 43 orphaned thermal.css rules.
- **Dropped the Thermal Lab overview** — `/thermal` now lands on Case & Regime (`THERMAL_HOME` derived from `STAGES[0]`).
- Added a **contributor walkthrough** (branch per person, separate preview ports, admin review → merge → deploy).
- **NVH lab group** started: sidebar group + `/nvh` placeholder page (Powertrain Phase 2, no backend yet).
- Vault: created this Vantage VE project log and committed it.
**Learned:**
- Default-deny > opt-in: a route someone forgets to decorate is closed, not open.
- Chrome that repeats the sidebar is clutter — the top bar shows context, never navigation.
- Audit timestamps are whole seconds → count lockout failures by row id, not ts (self-check caught it).
**Next:**
- Get a publicly trusted cert under raptee.com (covers Vantage QC too). Until then passwords + cookies cross the LAN in plain HTTP. See [[Questions|Q5]].
- Scaffold the NVH tool behind `/nvh` (needs [[Questions|Q4]] log format).

## 2026-10-26
**Did:**
- **Road Suite moved into VE** — Phase 1 backend (`backend/road_engine/`, Go CAN decoder, DBC library, `/api/road/*`) and Phase 2 frontend (`/road`). Now `ready: True`.
- Fixed two bugs carried from main Vantage: lucide `File` icon shadowed the `File` constructor (every upload threw); `thermal_ride.ingest` never closed its ExcelFile (WinError 32 on purge).
- VE got its **own cookie `ve-session`** — sharing `vantage-session` on the same host let main Vantage clobber VE logins (cookies ignore ports).
- **Admin Console** `/admin`: users, sessions (revocable, jti-tracked in `ve_auth.db`), audit log, system info, tool visibility. `add_user.py` for CLI logins.
- Own tab icon + branded loading screen; universal sidebar + top header across all labs.
**Learned:**
- Cookies are per host, not per port — two apps on one box need distinct cookie names.

## 2026-10-24
**Did:**
- Home console fits the viewport; T30 digital twin recoloured (VCU / PDU / DC-DC / OBC split).
- **CAD model 493 MB → 21 MB** (weld + simplify + meshopt), node names kept for click-to-navigate.
- Deploy fix: stop frontend before `next build` (was the 579 restarts on VE-Frontend); abort deploy on build failure. Dropped `--reload` from pm2 (it bounced everyone's session on any .py edit).
**Learned:**
- pm2 must run un-elevated — daemon + dump are per user, admin-shell `pm2 save` never resurrects.

## 2026-10-23
**Did:**
- Home page rebuilt as a console on real data. Thermal Lab UI: console header, workflow stepper, keyboard nav.
- Light mode made a real theme; contrast sweep over all lab pages (e.g. 1d-design 10 failures → 0).
**Learned:**
- Root cause was the accent used as **text**: hard-coded `HEAT_ACCENT #F0644B` and light accent `#d94a2f` (4.22:1, under 4.5).

## 2026-10-21 → 10-22
**Did:**
- Thermal physics core pinned with tests; fixed negative h in opposed mixed flow.
- One shared case across the thermal suite; stopped the model assuming unlimited ambient air.

## 2026-10-14
**Did:**
- Route-based thermal section, Powertrain tool shipped, 3D vehicle navigator.
- Retired the two reduced 1D thermal models; ported Calibrate h. Dev backend runs with `--reload`.

## 2026-10-10
**Did:**
- Brainstormed two new Vantage VE tools: Powertrain tool and subject-wise Calculator Library.
- Created this project in the vault; roadmap seeded (Powertrain P1 → Calc shell → Powertrain NVH).
- Wrote `PLANNING_powertrain_and_calc_library.md` into the Raptee-Vantage-VE repo.
**Learned:**
- Powertrain splits into two unrelated families: performance physics (torque/power/CD/gear ratio) and NVH health (gear noise/crest factor). Build performance first — it teaches the concepts.
- The Calculator Library is **not a textbook** — it's one registry-driven shell; each calc = one data row. "Both audiences" = a single "Show working steps" toggle, not a second app.
- Powertrain Phase-1 math overlaps Engineering-Mechanics calcs → the two tools share components.
**Next:**
- Confirm dyno log fields; collect one bike spec sheet + one sample dyno log.
**Concepts touched:** [[Powertrain Tool]] [[Calculator Library]]

### Build — Powertrain Phase 1 (same day)
**Did:**
- Decided **not** to port Road Suite into VE yet; proceeded with Powertrain.
- Built the Powertrain Phase-1 **backend**: `backend/powertrain_engine/powertrain.py`
  (power curve, tractive effort, road load, top speed — pure functions, formulae
  hardcoded, every value a required arg; only `g` is a constant). Self-check
  `selfcheck_powertrain.py` passes (hand-derived numbers).
- Wired `/api/powertrain/analyze` into `server.py` under a new POWERTRAIN banner;
  manifest entry `ready:True`. Verified: engine import OK, server import OK, route
  registered, analyze returns correct top speed (113.1 km/h on the test log).
- Built the **frontend** `frontend/app/powertrain/page.js` (blank spec inputs, paste
  dyno log, dual-axis torque/power chart, tractive-vs-road-load chart with top-speed
  marker). Matches Thermal conventions (usePlotlyTheme, getApiUrl, theme tokens).
**Learned:**
- VE launcher navigation is a 3D bike model (`VehicleNavigator`), not manifest cards;
  the `/api/tools` manifest only feeds the "active tools" count. New tools integrate
  by live route + manifest entry, same as Thermal.
- `getApiUrl` returns `""` client-side (Next proxy → 127.0.0.1); server-side string
  still says 8002 (pre-existing quirk, harmless for client fetches).
**Next (open):**
- Browser-verify the Powertrain UI: `launch_vantage_ve.bat` → open `/powertrain`.
- Dyno-log ingestion: paste works now; CSV/XLSX upload + reading from the Dyno DB is TODO.
- Resolve [[Questions#Open Questions|Q1]] (CF = crest factor vs Crr) before Phase 3.
