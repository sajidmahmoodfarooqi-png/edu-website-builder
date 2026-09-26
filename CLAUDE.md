# Edu Website Builder — project registry & session ledger

Standing context for Claude Code and Google Antigravity. Keep under 15 KB.

Naming rule: the college site this kit came from is "the reference build". Its brand
name, domain, people and data never appear in this public (MIT) repo, the agent, the
library, or anything generated. Brand-specific work lives in the reference build's
private repo.

## Subsystem registry

| Subsystem | Key files | Purpose |
| :--- | :--- | :--- |
| Core skill & specs | `edu-website-builder/SKILL.md`, `edu-website-builder/references/` | AI building skill, module catalog, gotchas, materials guide |
| Needs Assessment Form | `edu-website-builder/references/needs-assessment-form.md`, `edu-website-builder/assets/Needs-Assessment-Form.docx`, `Needs-Assessment-Form.pdf`, `edu-website-builder/scripts/render_form_docx.py` | 15-section intake form (Markdown source → Word, PDF) |
| Materials scaffolding | `edu-website-builder/scripts/scaffold_materials.py` | Creates up to 22 labelled intake folders + CSV templates |
| Agent design | `docs/AGENT_DESIGN.md` | Module library, `institution.json` spec, deterministic generator, Claude Agent SDK agent, gates |
| Release | `releases/Educational-Institution-Website-Kit.zip` | Brand-free kit v2.1 (no theme code yet) |

## Roadmap

- **Done:** NAF v2, kit v2.1, agent design v0.2 — merged to `main` (PR #1, 2026-09-26).
- **Now:** Phase A — read-only inventory of the reference build (Antigravity; brief and
  outputs in the reference build's private repo). Waiting for its hand-back.
- **Next:** Claude Code reviews Phase A (D1–D10), then Phase B: brand-free `edu-core`
  module library with `__PFX__`, verified in Docker.

## Protocol

- Run the quality checks before any handoff; never commit keys or passwords.
- Before committing here, scan changed files for the reference build's brand.

## Session ledger

### Agent design + NAF v2 — Status & Handoff, 2026-09-25/26
- **Changes Made**: NAF v2 (15 sections: mobile app, directorates, academic ops,
  accessibility, roles, security/handover, code-prefix field); module catalog, gotchas,
  materials guide and `scaffold_materials.py` (7 new folders) updated; Word/PDF
  regenerated. `docs/AGENT_DESIGN.md` v0.2 with owner decisions (§10): per-build code
  prefix via `__PFX__`, Docker, intake portal for NAF uploads, MIT, first NAF
  submitter = pilot. Release zip v2.1 made brand-free (theme boilerplate and
  server-specific scripts removed); author credit kept in README by owner choice.
- **Database / Schema**: none.
- **Verification**: scaffold script run with `--all` (22 folders); PDF text checked;
  brand scan of every changed file (incl. inside zip/docx/pdf) = only the README credit.
- **Git**: squashed to one commit (`a62a517`), merged to `main` as `e455534` via PR #1.
