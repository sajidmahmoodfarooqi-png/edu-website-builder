# Module catalog

Every module below is a proven pattern from a real, live educational-institution
build. Each entry says **what it is**, **what it needs from the form**, the
**default implementation**, and its **phase**. Build only the modules the filled
form ticks. Prefer a plain solution before adding a plugin or library.

Default stack (unless the form asks otherwise): **WordPress custom theme** for
all editable content (non-technical staff can maintain it), plus **custom
PHP + its own MySQL database** for the dynamic/portal features (kept independent
of WordPress so the applicant/portal data survives a CMS change). Free/OSS only.
A static-site variant (e.g. Astro) is possible for a purely informational site
with no logins — offer it only if the form wants no interactive features.

Content types are WordPress **custom post types (CPT)** with **ACF/Secure Custom
Fields** for structured fields; each gets an archive + single template following
the WordPress template hierarchy. Enqueue CSS/JS properly; bump a theme version
constant to bust asset caches.

---

## Always built (the shell)

**Site shell** — header with brand (logo + institution name, in both languages
if bilingual), primary nav (hand-coded list is fine for a fixed nav; use
dropdowns for large groups like Departments/Portals), footer, a mobile
hamburger, and a responsive, accessible base (semantic HTML, alt text, sensible
headings, readable contrast). *Needs:* institution name (both languages), logo,
brand colours, nav structure implied by which pages are ticked. Bilingual/RTL:
apply `dir="rtl" lang="xx"` only to the content that needs it, never globally.

---

## Informational modules

**Home / front page** — hero (image + name + tagline), a few highlight stats, a
sign-in/admissions call-to-action band high on the page, section teasers
(departments, principal's message, story), news. *Needs:* hero photo, tagline,
which sections to feature.

**About / Our Story / History** — long-form narrative page. *Needs:* the copy
(or bullet points to expand), historical photos.

**Leadership / Principal's message** — portrait + signed message + title.
*Needs:* photo, message text, name/title.

**Departments / Programmes** — CPT `department`; ACF: intro, vision, mission,
established year, Head of Department, a **faculty repeater** (name, designation,
subject, photo), programme/degree details (name, duration, seats, fee,
affiliation), placements/career-paths chips, a photo gallery. Archive grid +
single page. Gate any "degree-granting only" grids by an explicit exclusion list
of service departments, and centralise that list in one constant so every
surface (archive, admissions dropdown, homepage count) agrees. *Needs:* the
department list, per-department content, banners, faculty lists + photos.

**Faculty / staff directory** — a single sitewide list, usually its own CPT
`faculty_member`. **Watch the sync gap:** if the directory is a separate CPT
from each department's own faculty repeater, nothing keeps them in step — build
a small "health check" that flags drift (a person on a department page missing
from the directory, or vice-versa), and treat the department-page data as
authoritative. *Needs:* whether they want a combined directory; the roster.

**News & Notices** — CPT with date, body, optional attachment; archive + single.
Standardise one label everywhere ("News & Notices"). *Needs:* nothing upfront;
staff post over time.

**Events / Calendar** — CPT with date/venue. *Needs:* event list if any.

**Gallery** — CPT `gallery_image` with a caption + tags; a dependency-free
lightbox for enlarging. *Needs:* photos + captions.

**Downloads** — a page listing downloadable documents (prospectus, forms, date
sheets, results). *Needs:* the files.

**Contact** — a hardened contact form → email to configured recipients, with a
honeypot, email-header-injection guards, CSV-formula-injection guards, and a
flat-file backup. *Needs:* recipient email(s).

**FAQ** — bilingual accordion using native `<details>/<summary>` (no JS
dependency, accessible for free). Organise by topic (Applying, Portal, Alumni).
*Needs:* the Q&A content, or generate a sensible starter set from the other
modules and let staff edit.

**Committees / Societies** — a generic `committee_page` CPT (members repeater
with photos + roles, an optional second team, a header image). *Needs:* member
lists + photos.

---

## Interactive / dynamic modules (custom PHP + own MySQL DB)

Each of these stores data in a **separate MySQL database from WordPress**, via
PDO with `ATTR_EMULATE_PREPARES => false` and parameterised queries. Reads
credentials from a **gitignored config file** (ship a `.example` copy). Any file
upload is **hardened**: `is_uploaded_file()`, `getimagesize()` + an IMAGETYPE
allowlist (JPEG/PNG/WEBP), **GD re-encode** (strips any appended payload),
server-generated random filenames, stored **outside the web root** with an
`.htaccess` deny, and streamed to authorised reviewers only (never a public URL).

**Admissions — application + review** — public apply form (personal details,
academic record per level, hardened document uploads) → DB row; a status-tracking
page reached by an unguessable per-applicant token (emailed on submit); optional
committee-review area (list with status filters, per-applicant detail,
Shortlist/Reject/Confirm with emails, a document checklist, a printable
application). Support **redirecting a level to an external portal** (e.g. a
government admissions system) while capturing basic details first. Block
duplicate applications (by ID number) and validate every dropdown value
server-side — never trust the form to have enforced eligibility. *Needs:*
levels/programmes, whether committee review is wanted, external-portal details,
document checklist.

**Student / staff portal** — session auth (institutional Google OAuth via plain
cURL, no library; plus an optional registration-no + hashed-ID fallback);
period-wise attendance marking (teacher-scoped); assessments/marks + publish;
notices with audience scoping; a parent/guardian **tokenised view** (no login);
notifications (email + in-app only — no paid SMS/WhatsApp); role dashboards.
Portal users are never WordPress users, so register both `admin_post_` and
`admin_post_nopriv_` handlers. Rate-limit any password login. *Needs:* which
sub-features, sign-in method, roster data (entered later), a Google OAuth client.

**College administration portal** (Controller of Exams / VP) — a third
session/identity type that can view/download records but never mark attendance or
enter marks; scope every read to that account's own level. *Needs:* the office
accounts.

**Alumni** — self-registration (verified by a college-related document, reviewed
before listing); public directory (table: photo/name/contact/profession/…, with
contact shown only on consent); a **private membership card** reachable only via
a per-alum HMAC-signed link (no public card column); a personalised directory
view for the alum. *Needs:* whether directory/card are wanted.

**Results lookup** — roll number → result, read from an uploaded/imported result
set. *Needs:* result data format.

**Flash pop-up campaigns** — a `flash_popup` CPT with image(s), schedule
(show-from/until), frequency, scope; rendered on a cacheable page via a **static
bootstrap + an uncached AJAX endpoint** (never bake time-sensitive content into
cached HTML); auto-retire via cron. Optional front-end password-gated "campaign
manager" for non-technical staff. *Needs:* nothing upfront.

**Security hardening** (always, once dynamic features exist) — hardening headers
(X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy, HSTS), disable
XML-RPC/pingback, block user-enumeration (REST users + `?author=`), remove
version-disclosure files, and a **brute-force lockout on `wp-login.php`**.
Theme code, no plugin. Default passcodes on any front-end portal are stored
hashed and must be rotated at handover — never written into docs or git.

---

## Modules added after the first release (proven on the live build, Sept 2026)

**Department / directorate sub-sites** — each department (and each directorate
below) gets a self-contained tabbed mini-site (overview, faculty, scheme of
studies, research, labs gallery, contact) served by **one shared template +
a router**, reachable both as a path (`/geography/`) and, if DNS allows, a
subdomain (`geography.example.edu.pk`). Keep a static manifest of slugs and
aliases (`cs` → `computer-science`) so every surface resolves the same way;
serve subdomains through the one bootstrap rather than per-subdomain docroots.
Gate nav links on the target template existing. *Needs:* DNS control (§2),
per-department accent colour/banner, scheme-of-studies data.

**Academic operations** (extends the portal) — programmes / terms / subjects /
sections master data; **course offerings** where department coordinators allot
teachers to subject+section, with **combined cohorts** (one offering covering
several sections/departments) and **parallel electives**; a **timetable grid**
with teacher/room/section clash checks, variable period lengths, and a
front-end **Timetable In-charge portal** restricted to the named office. The
teacher-ownership gate (a teacher may only mark/enter for offerings they own,
403 otherwise) is enforced in both web handlers and the API. Combined periods
must write attendance for **every** section in the cohort, grouped on the same
key the save uses. *Needs:* offerings/allotments, current timetable.

**Homework + nightly parent digests** — teacher-posted homework per offering;
a cron job that rolls up the day's absences into one email per guardian.
*Needs:* guardian contacts.

**Role hierarchy** — beyond student/teacher/parent: Principal (read-only),
VP Academics, **department-scoped** HoDs and coordinators (see only their own
department), Controller of Examinations, timetable committee, registrar. Map
roles to offices, not people, so staff transfers are a data change. *Needs:*
the office list (form §11).

**Mobile app** — three tiers, cheapest first: (1) **PWA** (manifest + service
worker, installable from the browser); (2) Trusted Web Activity wrapper;
(3) **native Android (Jetpack Compose) app** on a JSON REST API
(`/wp-json/<ns>/v1/…`) with SHA-256-hashed bearer tokens, Google Sign-In via
the browser, and a student/parent shell + faculty shell (classes, roll,
marks, homework, notices). **Self-hosted OTA updates** (a version endpoint +
APK on the institution's own server; optional forced update) avoid Google
Play. Parent links open in-app via Android App Links (`assetlinks.json`).
**Never let the page cache store authenticated API responses** (a real
cross-account leak on the live build) and handle LiteSpeed stripping the
`Authorization` header (`REDIRECT_HTTP_AUTHORIZATION` fallback). One
production keystore per institution, kept by a named custodian. *Needs:*
tier choice, keystore custodian, app name/icon.

**Accessibility engine** — a floating accessibility control (high contrast,
font scaling, keyboard shortcuts), an **audio daily briefing** of today's
classes/attendance using the browser's speech synthesis (English + Urdu
voices; handle Chrome's empty first `getVoices()` and its ~15 s cut-off), a
list-view timetable for screen readers, “Listen” buttons on notices,
`role="alert"` form errors; TalkBack merged semantics + haptics in the app.
Pair it with a staff publishing rule: no image-only notices. *Needs:* whether
any students rely on assistive tech.

**Help Centre** — per-role how-to pages (`/portal/help/`), screenshot
walkthroughs and an optional in-dashboard guided tour; bilingual FAQ entries
for every portal and the app. Don't advertise videos that don't exist.

**QEC portal** — controlled evaluation cycles; the HEC-style questionnaire;
responses **anonymous but de-duplicated** by hashing student + offering +
cycle; Director analytics; public SAR documents. *Needs:* rubric, cycle dates.

**Student Affairs / Societies portal** — societies directory, cabinet roster,
events calendar (auto-archives past events), membership applications approved
by the in-charge; high-priority events can cross-post as portal notices.

**Sports Directorate portal** — disciplines, events, fixtures/results, student
trial registration, trial scoring (0–10) and squad building, CSV export.

**Hostel / Provost portal** — merit-based hostel application (configurable
formula, e.g. marks% × 0.6 + capped distance × 0.4) with public merit search;
Provost control centre: room-and-bed rack (occupied/vacant/damaged, race-safe
bed transfer), scrutiny + provisional allotment with challan, **bursar
fee-clearance** that activates the resident, leave approval, night roll-call,
complaints; resident self-service (gate passes, complaints, attendance).
Beds under a formal allotment are protected from direct edits.

**Academic blog + research journal** — two tracks on one submission system:
blog articles and a peer-reviewed journal with an editor-set submission window,
**institutional-email-only** submissions (enforced server-side), and a
consent-based editorial review step before publication.

**Heritage & history** — timeline, historical photo archive with a lightbox
scoped to the clicked set, founding documents; Schema.org JSON-LD
(`CollegeOrUniversity`) + Open Graph for rich link previews.

**Webmaster health check** — read-only admin dashboard that flags 404s,
schema drift, and faculty-directory ↔ department-page drift, with explicit
confirm-to-fix sync. Pair with a **pre-flight quality shield** script run
before each deploy (PHP lint, CSS isolation, clean mirror).

**WhatsApp absence alerts (off-site, optional)** — kept *outside* the website:
a free desktop tool on an office PC where staff review absences and send
templated local-language messages. The site itself stays free of paid SMS /
WhatsApp Business APIs.

---

## Phasing

A typical order: **shell + informational pages** first (a real, useful site on
day one), then admissions, then the student portal (master data → offerings →
timetable → roster → auth → attendance → notices → assessments → homework →
notifications → parent view → dashboards), then department sub-sites, the
mobile app (PWA first, native later), directorate portals (QEC, societies,
sports, hostel), journal/blog, alumni / campaigns / results as wanted.
Accessibility and the help centre grow alongside each phase, not at the end. Ship each phase working and tested before the
next. Don't build a login area before there's content worth logging in for.
