---
name: edu-website-builder
description: >-
  Build a complete website for an educational institution (school, college,
  university, academy) from a filled-out Needs Assessment Form, and generate
  that blank form for a client to fill in. Use this whenever someone wants to
  build, scaffold, plan, or quote an institution/campus website — even if they
  don't say "needs assessment" — including phrasings like "build a site like
  this for another college", "set up our school's website", "I have the
  requirements form filled in, build the site", or "create a needs-assessment /
  requirements form for a college website". Covers the full proven stack: WordPress custom theme;
  department/faculty/news/gallery/downloads/contact/FAQ pages; admissions
  application + committee review; student/staff/parent portal (attendance,
  results, notifications); alumni directory + membership card; flash campaigns;
  bilingual/RTL; and the shared-hosting deployment workflow. Prefer this skill
  over building an education website ad hoc.
---

# Educational institution website builder

This skill turns a **Needs Assessment Form** into a working
educational-institution website, using patterns proven on a real, live build.
It has two entry points — figure out which one the user needs:

- **A) They want the blank form** (to hand to a prospective client, or to fill
  in themselves). Give them
  [`references/needs-assessment-form.md`](references/needs-assessment-form.md) —
  the editable Markdown source of truth — and, for a non-technical person to
  type into, the ready-made **fillable Word hand-out** at
  [`assets/Needs-Assessment-Form.docx`](assets/Needs-Assessment-Form.docx)
  (regenerate it from the Markdown with
  [`scripts/render_form_docx.py`](scripts/render_form_docx.py) if the form
  changes). Don't interrogate them; the form does that.
- **B) They have a filled form** (or describe their needs in chat). Treat that
  as the spec and **build the site**. This is the main workflow below.

If it's ambiguous, ask once which they want; default to A if they seem to be
starting out, B if they've provided requirements.

## The build workflow (entry point B)

Read the reference files before planning:
[`needs-assessment-form.md`](references/needs-assessment-form.md) (so you know
what every field means),
[`module-catalog.md`](references/module-catalog.md) (what each module is, needs,
and how it's built),
[`materials-folder-guide.md`](references/materials-folder-guide.md) (the labeled
folders the client fills with logos/photos/docs/rosters, and the required
formats), and
[`architecture-and-gotchas.md`](references/architecture-and-gotchas.md) (stack,
deployment, and the caching/security/testing lessons that will otherwise bite).

### 1. Parse the form and reflect it back

Extract: institution identity + branding, languages, audiences/goals, which
**content pages** are ticked, which **interactive features** are ticked (and
Now-vs-Later), hosting/tech, constraints, and which **assets** they have.

Produce a short **build plan** and show it to the user before writing code:
- the chosen stack (default WordPress custom theme + custom PHP/MySQL for
  dynamic features; a static site only if they want zero interactive features),
- the module list, split into **Phase 1 (now)** and **later phases**,
- what you'll scaffold vs. what needs their content/assets/credentials,
- anything **missing but required** — flag it plainly rather than inventing it.

Get a quick nod on the plan. Don't over-ask: pick sensible defaults for anything
the form left blank and state them, rather than opening a long Q&A.

### 2. Set up the labeled materials folders — then let the client fill them

This is what keeps the build near-conversation-free: instead of asking for
assets one at a time, give the client **one known folder structure** to drop
everything into. Immediately after the plan is agreed:

- **Create the folders for them** by running
  [`scripts/scaffold_materials.py`](scripts/scaffold_materials.py) with the keys
  for the modules the form ticked, e.g.
  `python scaffold_materials.py --root <project> --only departments,admissions,portal`
  (branding, hero, and misc are always created). This makes
  `website-materials/` with each labeled folder, a `_README.txt` in each saying
  exactly what to put and in what format, and CSV templates with the correct
  headers — so there are no folder-name typos and no format guesswork.
- **Tell the client which folders now exist and what goes in each** (summarise
  from [`materials-folder-guide.md`](references/materials-folder-guide.md)),
  emphasising the two rules that prevent most rework: **name each person's photo
  exactly as their full name**, and **keep the CSV headers as given**.
- When they say the folders are filled, **ingest each one**: match photos to
  people by name, read the CSVs and docs, and populate every module. List
  anything still missing as clearly-marked placeholders rather than guessing.

If the client would rather create the folders by hand, point them at the guide —
the names and formats are all there.

### 3. Be honest about what needs the client

The form removes ~90% of the back-and-forth, not 100%. These still come from the
client, so surface them early and use clearly-marked placeholders meanwhile:
- **Real content** (copy, photos, logo, faculty lists) — build the structure now,
  mark gaps ("[ADD: department vision]", initials-placeholder for missing
  photos) so nothing looks broken and it's obvious what's outstanding.
- **Credentials** (hosting SSH/DB, SMTP, Google OAuth client) — needed only at
  deployment / for portal sign-in, never committed.
- **Paid-gateway features** (online fee payment) — flag as out of scope for a
  free/OSS build and suggest in-person or a free alternative.

### 4. Scaffold the shell, then build ticked modules

Build in the phase order from the catalog: **shell + informational pages first**
(a genuinely useful site on day one), then admissions, then the portal
(roster → auth → attendance → notices → assessments → notifications → parent
view → dashboards), then alumni / campaigns / results.

- Apply branding (logo, colours, fonts, both-language name) to the shell.
- For each content module: create its CPT + ACF fields + archive/single
  templates per the catalog; populate with supplied content, placeholder the
  rest.
- For each dynamic module: its own MySQL DB + PDO helper + gitignored config,
  hardened uploads, the auth/token model described in the catalog, and the
  security hardening once any dynamic feature exists.
- Reuse a block the third time it appears — factor it into a template part.
  Match the surrounding code's conventions; enqueue assets properly; keep it
  responsive and accessible.

### 5. Test the way that actually catches bugs

Drive the **real code path**, not just function calls: real HTTP requests, real
`curl -F` uploads, real sessions with a cookie jar. Check the negative/boundary
cases (duplicate submission rejected, out-of-scope access 404s, wrong token
rejected, upload of a non-image rejected). Seed realistic data, verify the exact
expected result, then remove every test row and disposable script. See the
testing notes in `architecture-and-gotchas.md`.

### 6. Deploy only with credentials and explicit approval

Deployment is outward-facing and hard to reverse — **confirm before doing it**,
and only when the client has provided hosting access. Follow the
`git archive` → single-tar SFTP → overlay-copy → verify-config-timestamps →
`wp eval-file` migrations → **web-reachable opcache reset** → `litespeed-purge` →
verify-live sequence in `architecture-and-gotchas.md`. Respect all four caching
layers, and verify against the live domain (not just "no fatal error") before
calling it done.

## Guardrails

- **Free / open-source only** by default (per the usual institution constraint) —
  no paid services or licensed libraries unless the form explicitly allows it;
  if a task seems to need one, flag it and offer a free alternative.
- **No tracking/analytics or third-party embeds** unless asked.
- **Never commit** real DB credentials, OAuth secrets, or applicant/contact/
  portal data — all gitignored.
- **Confirm before** any deploy, destructive change, or restructuring of existing
  pages/data. A build for a *new* institution starts clean; a rebuild of an
  existing site must not delete their current site without an explicit go-ahead
  and a backup first.
- Keep the client's data private; don't send it anywhere they didn't ask.

## Adapting the defaults

The proven build is one institution's shape; another's will differ. The form is
deliberately broad — honour what's ticked, scale modules to their size (a small
school may want only home/about/news/contact; a university may want every
portal), and don't impose features they didn't ask for. When the form and these
references disagree with an explicit client instruction, the client wins — note
the deviation and proceed.
