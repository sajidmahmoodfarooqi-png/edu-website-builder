# Edu Website Builder Agent — Design (draft v0.2, 2026-09-25)

**Status:** draft; owner decisions recorded in §10. Nothing is built yet.
**Author:** Sajid Mahmood Farooqi, with Claude Code.
**Licence:** MIT (agent, library, form, generator).

> **Naming rule.** The college site this kit was distilled from is called the
> **reference build** in every agent-facing artefact. Its brand name, domain,
> people, photos and data must not appear anywhere in the agent, its prompts,
> the module library, tests, fixtures, or anything the agent generates. A
> denylist check (§4.4) enforces this.

---

## 1. What we are building

A service where an institution **uploads its filled Needs Assessment Form
(NAF)**, approves a build plan, supplies its materials, and receives a working,
tested website + portal on its own hosting — built by an agent that assembles
already-proven modules and stops for a human at every decision that is
outward-facing or irreversible.

**Goals**

1. Any institution gets a reference-build-grade site from **assembled, tested
   modules**, not from code the model writes fresh each time.
2. Fixes proven on the reference build reach every site built from the library.
3. The agent does the mechanical 90%; people make every decision that matters
   (plan, content, credentials, go-live).
4. Free/open-source stack; runs on ordinary shared hosting.

**Non-goals (v1)**

- Hosting institutions' sites. Each site lives on the institution's own hosting.
- Writing the institution's content. The agent places what it is given and marks
  gaps; it never invents history, people, or policy.
- iOS apps, paid gateways, paid SMS/WhatsApp APIs.

## 2. Why the current kit is not enough

Today: Claude Code + the `edu-website-builder` skill. The skill describes modules
in prose; the model re-implements them per build. The release zip adds a theme
boilerplate, but:

| Gap | Evidence |
|---|---|
| Generator only re-colours | `build_site_from_form.py` reads name/domain/colours, copies the whole theme, writes one `brand-tokens.css`. Module ticks are parsed as `True` and never used. |
| Boilerplate still carries the reference brand | 92 files in the zip mention the reference institution. |
| Boilerplate is stale | 2026-08-30 snapshot: no mobile API/app, no directorate portals, no timetable in-charge, no accessibility engine, no passcode helper. |
| No verification step | Nothing checks a generated site works before handover. |

The hard part is not the LLM loop; it is having a **brand-free module library**
to drive. That is Phase A–B (§8).

## 3. Architecture

```
 ┌───────────────────────────────┐
 │  INTAKE PORTAL (web)          │  institution uploads NAF, approves plan,
 │  status page per build        │  uploads non-personal materials
 └──────────────┬────────────────┘
                │ build request
 ┌──────────────▼───────────────────────────────────────────────────┐
 │  AGENT (Claude Agent SDK, Python)                                │
 │  orchestrator + subagents + tools + code-enforced approval gates │
 └───────────────┬───────────────────────────────┬──────────────────┘
                 │ writes / validates            │ calls
 ┌───────────────▼──────────────┐   ┌────────────▼─────────────────┐
 │  SPEC: institution.json      │──▶│  GENERATOR (plain Python)    │
 │  compiled from the NAF;      │   │  deterministic, no LLM       │
 │  approved by the institution │   └────────────┬─────────────────┘
 └──────────────────────────────┘                │ reads
                                   ┌─────────────▼─────────────────┐
                                   │  MODULE LIBRARY (edu-core)    │
                                   │  brand-free, one folder +     │
                                   │  manifest per module          │
                                   └───────────────────────────────┘
```

**Design rule:** the LLM decides and explains; deterministic code generates. The
same spec always produces the same site, and the generator is tested like any
other program. The model reads messy inputs (NAF, CSVs, scanned timetables),
writes the spec, places content, diagnoses failures, and talks to people.

### 3.1 Module library (`edu-core`)

The reference build's theme with every institution-specific value replaced by a
placeholder, split into modules. Each module is a folder with a manifest:

```yaml
# modules/hostel/module.yaml
id: hostel
title: Hostel / Provost portal
naf_section: "9"                      # which NAF ticks enable it
requires: [shell, portal-core, portal-passcodes]
database: portal                      # which of the 4 databases it uses
schema: schema/hostel.sql             # CREATE TABLE IF NOT EXISTS …
files:
  - inc/hostel-handler.php
  - template-hostel-subsite.php
routes: [{path: /hostel/, subdomain: hostel}]
nav: {group: Portals, label: Hostel, gate_on: template-hostel-subsite.php}
options: [__PFX___hostel_provost_config]
passcode_slots: [hostel_provost, hostel_bursar]
materials: 20-hostel                  # intake folder it ingests
ingest: ingest/hostel.py              # rooms.csv → hostel tables
spec_keys: [hostel.merit_formula, hostel.blocks]
checks: tests/hostel.http             # HTTP checks run after build
placeholders: ["{{INSTITUTION_SHORT}}", "{{OFFICE_EMAIL:provost}}"]
```

Modules (from `references/module-catalog.md`): shell, home, about/heritage,
leadership, departments, department-subsites, faculty-directory, news, events,
gallery, downloads, contact, faq, help-centre, committees, privacy,
visitor-counter, admissions, results, flash-campaigns, portal-core,
academic-ops, parent-view, roles, mobile-api, pwa, android-app, qec, sas,
sports, hostel, blog-journal, alumni, accessibility, webmaster-health,
security-hardening, portal-passcodes.

**Code prefix (decided).** Library code uses the token `__PFX__` wherever a
function, option, table, CSS class, cookie, session or REST namespace needs a
prefix. Each build's prefix is **the institution's choice** (NAF §12 “Code
prefix”) or, if left blank, **the agent's suggestion** derived from the short
name/domain, shown in the build plan for approval. Validation: 2–10 lowercase
letters/digits, starts with a letter, not a WordPress/PHP reserved word, not on
the brand denylist. The generator substitutes it everywhere, and the golden
builds use different prefixes so a missed substitution fails a test.

### 3.2 The spec: `institution.json`

The single source of truth for one build, compiled from the NAF and validated
against a JSON Schema. Every NAF section maps to a key:

```jsonc
{
  "spec_version": 1,
  "library_version": "1.0.0",           // pins the module library
  "code_prefix": "gcmt",                 // NAF §12, or suggested
  "institution": {                        // §1
    "name_en": "…", "name_local": "…", "short": "…", "type": "degree_college",
    "city": "…", "founded": 1950, "levels": ["intermediate", "bs"],
    "size": {"students": 3000, "staff": 150, "departments": 16}
  },
  "brand": {                              // §2
    "domain": "example.edu.pk", "dns_control": "self",
    "colors": {"primary": "#14233f", "secondary": "#b8912e", "accent": "#ffffff"},
    "per_department_accents": true, "open_graph": true, "json_ld": true
  },
  "languages": {"primary": "en", "second": "ur", "rtl_scopes": ["faq", "notices"], "tts": ["en", "ur"]},
  "modules": {"department-subsites": "now", "admissions": "now", "portal-core": "now",
              "academic-ops": "later", "android-app": "later", "hostel": "off"},
  "admissions": {"online_levels": ["bs"],
                 "external_portal": {"level": "intermediate", "name": "…", "url": "…", "capture_first": true},
                 "committee_review": true, "doc_verification_gate": true},
  "portal": {"student_login": ["google", "regno_cnic"], "staff_login": ["google"],
             "parent_view": true, "whatsapp_tool": false},
  "offices": [{"office": "vp_academics", "email": "…"},
              {"office": "hod", "department": "geography", "email": "…"}],
  "hosting": {"type": "shared", "ssh": true, "db_limit": 4, "subdomains": true, "smtp": "google_workspace"},
  "constraints": {"free_only": true, "no_tracking": true},
  "gaps": [{"what": "Principal's message", "owner": "Principal's office"}]
}
```

### 3.3 Generator

`generate.py --spec institution.json --library edu-core --out site/`:

1. Resolve enabled modules + `requires` in dependency order; fail on a missing
   dependency or a hosting limit (e.g. more databases than the plan allows →
   suggest merging portal + alumni).
2. Copy module files into a fresh theme named after the prefix; substitute
   `__PFX__` and all `{{…}}` placeholders from the spec.
3. Emit brand tokens, nav, router manifest (department slugs + aliases), one
   combined schema per database, `*.example.php` configs.
4. Emit `site/BUILD_REPORT.md`: modules, unfilled placeholders, gaps.
5. Run the brand-denylist scan on the output; any hit fails the build.

It never touches credentials and never deploys.

### 3.4 Intake portal (decided: institutions upload their NAF)

A small web app, run by the operator of the service:

- **Upload:** NAF as .docx / .pdf / .md (the fillable Word form is the default).
  The agent parses it and returns a **build plan page** — modules now/later,
  suggested code prefix, defaults chosen, gaps — which the institution approves
  or comments on (Gate G1).
- **Materials:** after G1 the portal lists exactly which labelled folders are
  needed (the `scaffold_materials.py` set for the approved modules) and accepts
  a zip or per-folder uploads, with immediate checks (photo names, CSV headers,
  file types).
- **Personal data is not uploaded here.** Student, guardian and staff rosters,
  CNICs and phone numbers go **straight into the institution's own site** after
  handover, through the site's CSV import screens — the service never holds
  them. The NAF says this plainly.
- **Credentials** (hosting SSH/SFTP, database, SMTP, OAuth client) are entered
  into an encrypted vault field, never e-mailed, never shown to the model, and
  **deleted automatically at handover**. The portal recommends a temporary
  SFTP/SSH user the institution revokes afterwards.
- **Status page** per build: stage, open questions, gaps, gate approvals.
- Accounts: one institution contact (official e-mail, verified) per build.

The portal is ordinary web software and is built after the agent works locally
(Phase G).

## 4. The agent

Built on the **Claude Agent SDK (Python)** — Python because the kit's tooling is
Python. The SDK supplies the agent loop, file/shell tools, subagents, hooks and
permission control; we add the custom tools below.

### 4.1 Pipeline and gates

```
 1 INTAKE ─▶ 2 SPEC ══G1══▶ 3 MATERIALS ─▶ 4 GENERATE ─▶ 5 INGEST ─▶ 6 VERIFY (docker)
                                                                        │
     10 HANDOVER ◀══G4══ 9 VERIFY (live) ◀── 8 DEPLOY ◀══G3══ 7 STAGING ◀┘ (G2 before 7)
```

| Stage | What happens | Gate (who) |
|---|---|---|
| 1 Intake | Parse the uploaded NAF; list what is unclear. | — |
| 2 Spec | Compile `institution.json`; publish the build plan page. | **G1 — institution approves the plan** |
| 3 Materials | Request the needed folders; check uploads; report gaps. | — |
| 4 Generate | Run the generator. | — |
| 5 Ingest | Load non-personal materials into the Docker site; transcribe PDF/scanned timetables into CSV **for the institution to confirm** before loading. | — |
| 6 Verify | Lint, quality shield, each module's HTTP checks against the Docker site; fix-and-retry loop. | — |
| 7 Staging | Deploy to a staging subdomain on the institution's host for them to click through. | **G2 — institution says "stage it"** |
| 8 Deploy | Production deploy (overlay copy, config-timestamp check, migrations, opcache reset, cache purge). | **G3 — institution says "go live"** + operator confirms |
| 9 Verify live | Same checks against the live domain; cache-layer checks. | — |
| 10 Handover | Institution's admin signs in → one-time portal passcodes; they import personal rosters; ops guide + technical report generated from the spec; credentials deleted from the vault. | **G4 — institution signs off** |

The **pilot** is simply the first institution that submits a NAF: its build runs
the full pipeline with the operator reviewing every stage, not just the gates.

### 4.2 Subagents

| Subagent | Job | Model |
|---|---|---|
| orchestrator | Runs the pipeline, owns the gates, writes to the status page. | Opus 5.5 |
| spec-writer | NAF → `institution.json` + build plan; re-plans on comments. | Opus 5.5 |
| ingester | Materials → content/rows; photo-to-person matching; timetable transcription. | Sonnet 5 (CSV), Opus 5.5 (scans) |
| content-filler | Places supplied copy; drafts FAQ/help from the spec for the institution to edit; never invents facts. | Sonnet 5 |
| qa | Runs checks, reads failures, proposes minimal fixes or flags a library bug. | Sonnet 5 |
| deployer | Runs stage/deploy/verify tools only; no file edits. | Haiku 4.5 |

### 4.3 Tools

| Tool | Wraps | Side effects |
|---|---|---|
| `read_naf(path)` | NAF parser (.docx/.pdf/.md) | none |
| `validate_spec(path)` | JSON Schema, dependency check, prefix rules, denylist | none |
| `plan_page(spec)` | renders the build plan for the portal | writes plan |
| `scaffold_materials(keys)` | `scripts/scaffold_materials.py` | creates folders |
| `check_materials(root)` | names, headers, file types, required files | none |
| `generate_site(spec)` | generator | writes `site/` |
| `ingest(module, root)` | module's `ingest/*.py` | writes Docker DB |
| `docker_env(action)` | `docker compose` WordPress + MariaDB + PHP (up/reset/down) | local containers |
| `run_checks(target, modules)` | lint + quality shield + module `.http` checks | none |
| `stage(site)` / `deploy(site)` | overlay deploy script | **remote writes — gated** |
| `verify_live(domain)` | HTTP checks + cache headers | none |
| `report(kind)` | build report, ops guide, technical report from the spec | writes docs |

### 4.4 Guardrails in code

- **Gates:** a permission callback denies `stage`/`deploy` unless the gate
  record for that build is approved in the portal database by the institution
  contact (and, for G3, the operator). The model cannot write gate records.
- **Pre-tool hooks** block: reading vault/credential files, printing secrets,
  `rm -rf` on remote paths, network calls other than the institution's host and
  package registries, writes outside the build directory.
- **Secrets** are injected into deploy tools at run time from the vault; the
  model only sees "credential present: yes/no".
- **Brand denylist:** the reference institution's names, domain, e-mail
  domain and known staff names; scanned in the library (CI), in every
  generated site, and in agent prompts. Any hit fails.
- **No default passcodes:** every build includes `portal-passcodes`.
- **Audit log** per build: tool, arguments (secrets masked), result, gate
  decisions with who/when.

### 4.5 Sketch

```python
# agent/main.py — sketch only; verify names against the current SDK release
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition
from tools import builder_server, gate_guard, block_secrets

options = ClaudeAgentOptions(
    model="claude-opus-5-5",
    mcp_servers={"builder": builder_server},        # tools of §4.3
    allowed_tools=["mcp__builder__*", "Read", "Edit", "Write", "Bash"],
    agents={
        "spec-writer": AgentDefinition(description="NAF → institution.json", prompt=SPEC_PROMPT, model="opus"),
        "ingester":    AgentDefinition(description="Materials → Docker site", prompt=INGEST_PROMPT, model="sonnet"),
        "qa":          AgentDefinition(description="Run checks, fix",         prompt=QA_PROMPT, model="sonnet"),
        "deployer":    AgentDefinition(description="Deploy + verify only",    prompt=DEPLOY_PROMPT, model="haiku",
                                       tools=["mcp__builder__deploy", "mcp__builder__verify_live"]),
    },
    can_use_tool=gate_guard,
    hooks={"PreToolUse": [block_secrets]},
    cwd=build_dir,
)
```

## 5. What only people can do

- **Institution:** the content; credentials; DNS and hosting-panel steps
  (subdomains, SSL, docroots); the Android signing key and its custodian;
  approving G1–G4; importing personal rosters; sharing portal passcodes;
  staff training.
- **Operator:** confirming G3; reviewing the first build end to end; handling
  library-bug reports from QA.

## 6. Keeping the library in step with the reference build

The reference build remains the proving ground; the library follows it.

- Reference-build commits that apply to the library are tagged `[lib]`.
- `port_fix.py <commit>` rewrites the reference prefix to `__PFX__`, strips
  identity values to placeholders, applies the patch to `edu-core`, runs the
  denylist; conflicts go to a person.
- The library is versioned; each site pins `library_version`. Upgrading a site =
  regenerate + checks + the normal gates.
- Security fixes are flagged so every site's contact gets an upgrade notice.

## 7. Testing the agent

- **Golden builds:** three fictitious institutions (small school; degree college;
  university with hostel), each with a filled NAF, materials and its own code
  prefix, committed as fixtures. Every change regenerates all three in Docker
  and must pass their checks and the denylist.
- **Parity test:** a spec describing the reference build's module set must pass
  the same functional checks the reference build passes (behaviour parity, run
  privately; no reference data enters the library).
- **Red-team fixtures:** contradictory NAF; wrong CSV headers; photos named
  `IMG_2043.jpg`; a materials upload containing a roster or a password — the
  agent must flag, not guess, and refuse to store the personal data/password.

## 8. Roadmap

| Phase | Deliverable | Who | Done when |
|---|---|---|---|
| **A. Inventory** | Every institution-specific value and every module boundary/dependency in the reference build, as data. | Antigravity (brief and outputs kept in the reference build's **private** repo — brand data never enters this public repo) | Inventory reviewed by owner |
| **B. Module library** | `edu-core`: brand-free code with `__PFX__`, manifests, schemas, checks. | Claude Code + Antigravity | Golden build 1 generates in Docker and passes |
| **C. Spec + generator** | JSON Schema, NAF → spec compiler, generator, `check_materials`, denylist. | Claude Code | All 3 golden builds pass |
| **D. Agent v1 (local)** | Stages 1–6 in Docker, gate G1 via CLI. | Claude Code | Golden build 2 built from its NAF alone |
| **E. Deploy stages** | Stages 7–10, gates G2–G4, vault, audit log. | Claude Code | Staging deploy to a test host passes live checks |
| **F. First institution** | Whoever submits the first NAF, with full operator review. | Operator + agent | Site live, G4 signed |
| **G. Intake portal** | The upload/approval/status web app. | Claude Code + Antigravity | An institution completes G1–G4 without e-mail |

Phases A–C are valuable on their own: they turn the kit into a real template.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Reference brand leaks into a client site | `__PFX__` + placeholders; denylist scan in CI and on every generated site. |
| Library drifts from the reference build | `[lib]` tagging + `port_fix.py`; golden builds. |
| Model invents content or passes a failing check | Deterministic generator; checks are code; gaps are placeholders in the build report. |
| Service holds credentials | Vault, model never sees them, temporary accounts, deleted at handover. |
| Service holds personal data | Rosters never uploaded to the service; imported by the institution into its own site. |
| Hosting differs (no SSH, 1 DB) | Spec validation fails early with a named alternative. |
| Token cost | Opus for planning/diagnosis only; Sonnet/Haiku for bulk; generator does the heavy lifting. |

## 10. Owner decisions (2026-09-25)

| # | Question | Decision |
|---|---|---|
| 1 | Code prefix | Per build: the institution's choice (NAF §12), else the agent's suggestion, approved at G1. Library uses `__PFX__`. The reference brand is never used anywhere in the agent. |
| 2 | Local environment | Docker (`docker compose`: WordPress + MariaDB + PHP). Local by WP Engine is not used. |
| 3 | Who runs it | Institutions upload their NAF through an intake portal (§3.4). |
| 4 | Licence | MIT. |
| 5 | Pilot | No pre-chosen pilot — the first institution to submit a NAF, with full operator review (§4.1). |
