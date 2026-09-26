# Edu Website Builder — session ledger

Naming rule: the college site this kit came from is "the reference build". Its brand
name, domain, people and data never appear in this public (MIT) repo, the agent, the
library, or anything generated. Brand-specific work lives in the reference build's
private repo.

## Agent design + NAF v2 — Status & Handoff, 2026-09-25
- **Changes Made**: NAF v2 (15 sections: mobile app, directorates, academic ops,
  accessibility, roles, security/handover, code-prefix field); module catalog, gotchas,
  materials guide and `scaffold_materials.py` (7 new folders) updated; Word/PDF
  regenerated and refreshed in the release zip. `docs/AGENT_DESIGN.md` v0.2 with owner
  decisions (§10): per-build code prefix via `__PFX__`, Docker, intake portal for NAF
  uploads, MIT, first NAF submitter = pilot.
- **Database / Schema**: none.
- **Verification**: scaffold script run with `--all` (22 folders); PDF text checked;
  brand grep on skill, docs and PDF = 0 hits.
- **Next Steps**:
  - Done 2026-09-26: release zip v2.1 is brand-free (theme boilerplate + server-specific
    scripts removed, skill copy refreshed); author credit kept in README by owner choice.
  - Phase A handed to Antigravity 2026-09-26 via the universal hub (brief and outputs in
    the reference build's private repo). Waiting for its hand-back.
  - After Phase A: Claude Code reviews D1–D10, then Phase B (edu-core library in Docker).
  - Pushed 2026-09-26 as one squashed commit to `origin/needs-assessment-v2` (not merged to `main`).
