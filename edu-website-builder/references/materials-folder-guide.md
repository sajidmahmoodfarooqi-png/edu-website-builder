# Materials folder guide

After the Needs Assessment Form is filled, the client puts every file the site
needs into a set of **labeled folders** inside the project folder. When the
folders are named exactly as below and filled in the stated formats, the build
reads straight from them — almost no questions needed.

Two ways to create the folders:
- **Let the skill scaffold them** — run
  [`scripts/scaffold_materials.py`](../scripts/scaffold_materials.py), which
  creates the labeled folders (tailored to what the form ticked) with a
  `_README.txt` in each. This avoids typos in folder names. **Preferred.**
- **Or create them by hand** using the exact names below.

Everything lives under one root folder: **`website-materials/`** (in the project
folder). Only create the folders you actually need — the table says which are
core and which depend on a form tick.

## How many folders?

| Folder | Create it when… |
|---|---|
| `01-branding` | Always |
| `02-hero-and-campus` | Always |
| `03-about-and-history` | "About/Our Story" ticked |
| `04-leadership` | "Leadership/Principal's message" ticked |
| `05-departments` | "Departments/Programmes" ticked |
| `06-faculty-directory` | "Faculty directory" ticked |
| `07-news-and-notices` | "News & Notices" ticked |
| `08-events` | "Events" ticked |
| `09-gallery` | "Gallery" ticked |
| `10-downloads` | "Downloads" ticked |
| `11-admissions` | Any admissions feature ticked |
| `12-portal-roster` | Student/staff portal ticked |
| `13-committees-societies` | "Committees/Societies" ticked |
| `14-contact-details` | "Contact" ticked |
| `99-anything-else` | Always (catch-all) |

Alumni needs **no** intake folder — alumni add themselves through the site's
self-registration form.

## File format standards (apply everywhere)

- **Photos:** JPG, PNG, or WEBP. Hero/campus/banner shots **landscape, ≥1600px
  wide**. Portraits roughly **3:4 (e.g. 900×1200)**. Keep each under ~5 MB.
- **Text / copy:** Markdown (`.md`) preferred; Word (`.docx`) or plain `.txt`
  accepted. Write naturally — headings and bullets are fine.
- **Data / lists:** `.csv`, UTF-8, **first row must be the exact headers** given
  below. (Excel "Save As → CSV UTF-8".)
- **Naming a person's photo:** name the file **exactly as the person's full
  name** (e.g. `Ayesha Khan.jpg`). This is how photos get matched to people —
  a mismatched or vague name (`IMG_2043.jpg`) means it can't be placed
  automatically.

---

## What goes in each folder

### `01-branding/`  *(always)*
- Logo/monogram: **PNG with a transparent background** (add an `.svg` too if you
  have one). Name it `logo.png`.
- Favicon (optional): a square `favicon.png`, ideally 512×512.
- Brand colours: a `colors.txt` with hex codes — `primary #14233f`,
  `secondary #b8912e`, `accent #ffffff` (or just describe them).
- Brand fonts (optional): `.ttf`/`.otf` files **with their licence** (free/OSS
  fonts only unless you own a licence).

### `02-hero-and-campus/`  *(always)*
- 1–3 wide landscape photos for the homepage hero (best building/campus shots).
- Any general campus photos for use across the site.
- If a photo has a required credit, note it in a `credits.txt`.

### `03-about-and-history/`
- `about.md` (or `.docx`): the institution's story/history in your words.
- Historical or heritage photos, freely named.

### `04-leadership/`
- Portrait photo of the principal/VC (`Principal Full Name.jpg`).
- `message.md` (or `.docx`): the message text.
- `details.txt`: full name + exact title/designation.
- Repeat (extra portrait + short bio) for any other leaders to feature.

### `05-departments/`
One **subfolder per department, named as the department** (e.g.
`Geography/`, `Computer Science/`). Inside each:
- A **banner image** (landscape) — name it `banner.jpg`.
- `profile.md` (or `.docx`): intro, vision, mission, programme/degree details
  (name, duration, seats, fee, affiliation), notable achievements.
- A **`faculty/`** subfolder containing:
  - one **portrait per teacher, named as their full name** (`Zulfiqar Ali.jpg`),
  - a **`faculty.csv`** with headers:
    `name,designation,subject,qualification,email,phone,is_head`
    (`is_head` = `yes` for the Head of Department, else blank).

### `06-faculty-directory/`  *(only if you want one combined sitewide list)*
- A single **`faculty.csv`**, headers:
  `name,designation,department,subject,qualification,email`
- Photos aren't needed here if they're already in each department's `faculty/`
  folder — those are reused.

### `07-news-and-notices/`
- A few starter items as `.md`/`.docx`/`.txt` (title + date + body), plus any
  attachment PDFs. Ongoing news is posted by staff later; this is just seed
  content.

### `08-events/`
- `events.csv`, headers: `title,date,time,venue,description`.

### `09-gallery/`
- The photos, plus a **`captions.csv`**, headers: `filename,caption,tags`
  (`tags` separated by `;`). Photos without a caption row still work.

### `10-downloads/`
- The actual documents (prospectus, admission forms, date sheets, past papers,
  result PDFs) with **clear, human filenames** (`BS-Admission-Form-2026.pdf`).
- Optional `list.csv`, headers: `filename,label,category`.

### `11-admissions/`
- The official **admission form(s)** as PDF (the online form mirrors their fields
  and document checklist).
- `programmes.csv`, headers: `level,programme,seats,fee` (`level` e.g.
  `BS`/`Intermediate`/`Lateral Entry`).
- If a level is handled by an **external government/university portal**: a
  `portal.txt` with its **name + exact URL**, and a banner image for it.
- Any specific **document-checklist** wording you require from applicants.

### `12-portal-roster/`  *(student/staff portal only)*
CSV files the portal imports. Provide what you have — students/staff can also be
added in the admin screens later. Use these exact headers:
- `staff.csv`: `full_name,google_email,is_active,roles` (`roles` from
  `admin`/`teacher`/`exam_cell`, separated by `;`)
- `students.csv`: `registration_no,first_name,last_name,program_code,section,
  google_email,personal_email,cnic_or_bform`
- `programs.csv`: `code,name,level`
- `sections.csv`, `subjects.csv`, `enrollments.csv`, `timetable.csv` — the skill
  supplies blank templates in this folder if you scaffold it; fill what applies.
- **Never** put real passwords in these files.

### `13-committees-societies/`
Per committee, a subfolder named as the committee, containing:
- `members.csv`, headers: `name,role,photo` (`photo` = a filename in the same
  folder, or blank),
- the member photos, and an optional `header.jpg`.

### `14-contact-details/`
- `contact.txt`: postal address, phone number(s), public email, office hours,
  and the **email address(es) that should receive contact-form messages**.
- `map.txt` (optional): latitude,longitude or a Google Maps link.

### `99-anything-else/`  *(always)*
Anything that doesn't fit above — extra photos, reference material, notes,
a document describing a special requirement. Nothing here is required; it's a
safe place so nothing gets lost.

---

## After filling the folders

Hand the project back to Claude (with the edu-website-builder skill) and say the
materials are ready. The build ingests each folder, matches photos to people by
name, populates every module, and lists anything still missing as clearly-marked
placeholders — so the site is complete except for what genuinely wasn't provided.
