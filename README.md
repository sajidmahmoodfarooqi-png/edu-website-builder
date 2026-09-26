# Educational Institution Website Builder

A reusable toolkit — a **Needs Assessment Form** plus an AI **skill** — that turns
one filled-in requirements form into a complete website for a school, college, or
university, with minimal back-and-forth.

It was distilled from a real, production project: the full website and portal
system for **Government Graduate College Asghar Mall, Rawalpindi**
([gpgcam.edu.pk](https://gpgcam.edu.pk)).

---

## The achievement behind it

A complete, live institutional website and management platform, built and deployed
end-to-end on **free / open-source software and ordinary shared hosting** — no paid
services, no VPS:

- **Public site** — home, history, 16 department pages, faculty directory,
  news & notices, gallery, downloads, contact, and a bilingual **English + Urdu
  (right-to-left)** FAQ.
- **Online admissions** — application forms with database storage and hardened
  document uploads, applicant **status tracking**, an **Admissions Committee
  review portal** (shortlist / reject / confirm with email notifications and a
  document checklist), a **printable application**, jurisdiction-aware NOC rules,
  duplicate-application prevention, and redirect-to-government-portal support for
  intermediate admissions.
- **Student / Faculty / Parent portal** — Google Sign-In (plus a registration-no
  fallback), period-wise attendance, assessments and published results, notices,
  dashboards, email + in-app notifications, and a no-login **tokenised parent
  view**.
- **College Administration portal** — Controller of Examinations / VP records and
  exports.
- **Alumni** — self-registration verified by a college document, a public
  directory, and a private, printable **membership card**.
- **Admin conveniences** — a webmaster health-check dashboard, roster CSV imports,
  a timetable grid, and scheduled flash-announcement campaigns.
- **Academic operations** *(added Sept 2026)* — course offerings and teacher
  allotment with combined cohorts and parallel electives, a clash-checked
  timetable with its own In-charge portal, homework, nightly parent absence
  digests, and department-scoped roles (VP Academics, HoDs, coordinators).
- **Department sub-sites** — 15 self-contained tabbed department sites on their
  own subdomains, served by one shared router.
- **Mobile app** — installable PWA plus a native Android app (student, faculty,
  parent) on a JSON API, with Google Sign-In and self-hosted over-the-air updates
  (no Play Store).
- **Directorates** — Quality Enhancement Cell (anonymous HEC-rubric teacher
  evaluations, SAR), Student Affairs societies & events, Sports Directorate
  (trials, squads, fixtures), and Hostel/Provost (merit admissions, bed rack,
  bursar clearance, gate passes, roll-call).
- **Scholarship & heritage** — an academic blog and a peer-reviewed e-journal
  (institutional-email submissions, consent-based review), and a heritage
  timeline and archive back to the college's 1904 founding.
- **Accessibility** — an audio daily briefing for blind students, read-aloud
  notices in English and Urdu, high-contrast mode, and a screen-reader timetable.
- Built responsive and accessible, hardened (security headers, upload
  re-encoding, no-cache discipline across CDN/page-cache/opcache layers), and
  deployed with a safe, credential-preserving workflow.

## From one project to a repeatable skill

Building that surfaced a repeatable shape for *any* institution. This repo packages
it so the next school/college/university can get a similar site with the
requirements gathered **once**, upfront:

1. **Fill the Needs Assessment Form** — institution identity, branding, languages,
   which pages and interactive features are wanted (phased now/later), hosting, and
   an assets checklist. Provided as editable **Markdown**, a fillable **Word**
   document, and a **PDF** for printing.
2. **Drop your files into labeled folders** — a predefined `website-materials/`
   structure (logo, photos, faculty lists, department profiles, documents…), each
   folder with a README and CSV templates, so nothing has to be chased up later.
3. **Hand it to the AI skill** — it reads the form, produces a build plan, scaffolds
   the site and every chosen module with your branding, populates from your folders,
   flags what's still missing, and deploys only on your go-ahead.

## Where it is going

A design for turning this kit into a website-building agent — a de-branded
module library, an `institution.json` spec compiled from the form, a deterministic
generator, and a Claude Agent SDK agent with human approval gates — is drafted in
[`docs/AGENT_DESIGN.md`](docs/AGENT_DESIGN.md).

## What's in this repo

```
edu-website-builder/
├── SKILL.md                              the skill: workflow + entry points
├── references/
│   ├── needs-assessment-form.md          the fillable form (Markdown source)
│   ├── materials-folder-guide.md         the labeled-folders intake system
│   ├── module-catalog.md                 every page/feature that can be built
│   └── architecture-and-gotchas.md       stack, deployment & hard-won lessons
├── scripts/
│   ├── scaffold_materials.py             auto-creates the labeled intake folders
│   └── render_form_docx.py               regenerates the Word form from Markdown
└── assets/
    └── Needs-Assessment-Form.docx        the fillable Word hand-out
Needs-Assessment-Form.pdf                 quick-view PDF of the form
```

It's an [Agent Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills):
drop the `edu-website-builder/` folder into a Claude skills directory (or install
the packaged `.skill`) and it activates when you ask to build an institution
website. Everything here is documentation and tooling — **no website source code,
no credentials, no personal data.**

## Credit

Conceived, developed and designed by **Sajid Mahmood Farooqi**, Professor and Head
of the Department of Geography, Government Graduate College Asghar Mall, Rawalpindi.

## License

Released under the [MIT License](LICENSE) — free to use and adapt.
