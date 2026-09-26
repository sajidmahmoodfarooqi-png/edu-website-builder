#!/usr/bin/env python3
"""
Create the labeled `website-materials/` intake folders for an educational-
institution website build, each with a `_README.txt` (what to drop in + format)
and, where useful, a CSV template with the correct header row.

Usage:
  python scaffold_materials.py --root <project-dir> [--only KEY,KEY,...] [--all]

Keys (create only the ones the Needs Assessment Form ticked; branding, hero,
and misc are always created):
  about leadership departments faculty news events gallery downloads
  admissions portal committees contact roles mobileapp qec societies
  sports hostel journal

Examples:
  python scaffold_materials.py --root .            # core only (branding/hero/misc)
  python scaffold_materials.py --root . --all      # every folder
  python scaffold_materials.py --root . --only departments,admissions,portal
"""
import argparse, os, sys

ALWAYS = ["branding", "hero", "misc"]

FOLDERS = {
    "branding":    "01-branding",
    "hero":        "02-hero-and-campus",
    "about":       "03-about-and-history",
    "leadership":  "04-leadership",
    "departments": "05-departments",
    "faculty":     "06-faculty-directory",
    "news":        "07-news-and-notices",
    "events":      "08-events",
    "gallery":     "09-gallery",
    "downloads":   "10-downloads",
    "admissions":  "11-admissions",
    "portal":      "12-portal-roster",
    "committees":  "13-committees-societies",
    "contact":     "14-contact-details",
    "roles":       "15-roles-and-offices",
    "mobileapp":   "16-mobile-app",
    "qec":         "17-qec",
    "societies":   "18-student-societies",
    "sports":      "19-sports",
    "hostel":      "20-hostel",
    "journal":     "21-journal-and-blog",
    "misc":        "99-anything-else",
}

READMES = {
    "branding": "Put here:\n"
        "  - logo.png  (transparent background; add logo.svg if you have it)\n"
        "  - favicon.png  (square, ~512x512, optional)\n"
        "  - colors.txt  (hex codes: primary #..., secondary #..., accent #...)\n"
        "  - brand fonts .ttf/.otf WITH their licence (free/OSS only), optional\n",
    "hero": "Put here:\n"
        "  - 1-3 wide LANDSCAPE photos for the homepage hero (>=1600px wide)\n"
        "  - any general campus photos\n"
        "  - credits.txt if any photo needs a visible credit (optional)\n",
    "about": "Put here:\n"
        "  - about.md (or about.docx): your institution's story/history\n"
        "  - historical / heritage photos (freely named)\n",
    "leadership": "Put here:\n"
        "  - 'Principal Full Name.jpg'  (portrait)\n"
        "  - message.md (or .docx): the message text\n"
        "  - details.txt: full name + exact title/designation\n",
    "departments": "Create ONE SUBFOLDER PER DEPARTMENT, named as the department\n"
        "(e.g. 'Geography', 'Computer Science'). Inside each subfolder:\n"
        "  - banner.jpg  (landscape banner)\n"
        "  - profile.md (or .docx): intro, vision, mission, programme details\n"
        "    (name, duration, seats, fee, affiliation), achievements, research\n"
        "  - scheme-of-studies.pdf  (or .csv with headers:\n"
        "    semester,course_code,course_title,credit_hours)\n"
        "  - labs/  subfolder with lab / department photos (optional)\n"
        "  - accent.txt  (optional: the department's own hex colour)\n"
        "  - faculty/  subfolder containing:\n"
        "      * one portrait per teacher, NAMED AS THEIR FULL NAME\n"
        "        (e.g. 'Zulfiqar Ali.jpg')\n"
        "      * faculty.csv  (copy 'faculty-template.csv' from the\n"
        "        05-departments folder into each department's faculty/ folder\n"
        "        and rename it faculty.csv)\n",
    "faculty": "Only needed if you want ONE combined sitewide directory.\n"
        "  - faculty.csv  (template provided here)\n"
        "  - photos not needed if already under each department's faculty/ folder\n",
    "news": "Put here:\n"
        "  - a few starter notices as .md/.docx/.txt (title + date + body)\n"
        "  - any attachment PDFs\n",
    "events": "Put here:\n  - events.csv  (template provided here)\n",
    "gallery": "Put here:\n"
        "  - the photos\n"
        "  - captions.csv  (template provided here; photos without a row still work)\n",
    "downloads": "Put here:\n"
        "  - the documents (prospectus, forms, date sheets, results) as PDF,\n"
        "    with CLEAR human filenames (e.g. BS-Admission-Form-2026.pdf)\n"
        "  - list.csv (optional; template provided here)\n",
    "admissions": "Put here:\n"
        "  - the official admission form(s) as PDF\n"
        "  - programmes.csv  (template provided here)\n"
        "  - portal.txt: if a level uses an EXTERNAL govt/university portal,\n"
        "    its name + exact URL (and a banner image for it)\n"
        "  - any required document-checklist wording\n",
    "portal": "CSV files the student/staff portal imports (fill what you have;\n"
        "the rest can be added in the admin screens later). NEVER put real\n"
        "passwords in these files. Templates provided here:\n"
        "  - staff.csv, students.csv, guardians.csv, programs.csv,\n"
        "    sections.csv, subjects.csv, enrollments.csv, offerings.csv,\n"
        "    timetable.csv\n"
        "  - the current timetable as PDF/image too, if that's what you have\n",
    "committees": "Create ONE SUBFOLDER PER COMMITTEE, named as the committee.\n"
        "Inside each:\n"
        "  - members.csv  (headers: name,role,photo)\n"
        "  - the member photos\n"
        "  - header.jpg (optional)\n",
    "contact": "Put here:\n"
        "  - contact.txt: address, phone(s), public email, office hours, AND the\n"
        "    email address(es) that should receive contact-form messages\n"
        "  - map.txt (optional): latitude,longitude or a Google Maps link\n",
    "roles": "Who holds which office, so access is right on day one.\n"
        "  - offices.csv  (template provided here). Use OFFICIAL emails.\n"
        "    Include every HoD and coordinator, one row per department.\n",
    "mobileapp": "Put here:\n"
        "  - app-icon.png  (square, 1024x1024, no transparency)\n"
        "  - app-name.txt: the app's display name\n"
        "  - custodian.txt: name/office of the person who will keep the app's\n"
        "    signing key safe (NEVER put the key itself here)\n",
    "qec": "Put here:\n"
        "  - questionnaire.docx/.pdf, only if you don't use the HEC standard one\n"
        "  - SAR and other QEC documents (PDF) to publish\n"
        "  - cycles.txt: evaluation windows (e.g. last 2 weeks of each semester)\n",
    "societies": "Put here:\n"
        "  - societies.csv and cabinet.csv  (templates provided here)\n"
        "  - one logo/photo per society, NAMED AS THE SOCIETY\n"
        "  - events.csv for upcoming events (same headers as 08-events)\n",
    "sports": "Put here:\n"
        "  - disciplines.csv  (template provided here)\n"
        "  - photos of teams / grounds / trophies\n",
    "hostel": "Put here:\n"
        "  - rooms.csv  (template provided here): ONE ROW PER BED\n"
        "  - rules.md: hostel rules, fee, and the merit formula you use\n"
        "  - hostel photos\n",
    "journal": "Put here:\n"
        "  - journal.txt: journal name, ISSN (if any), scope, frequency\n"
        "  - editorial-board.csv  (template provided here) + member photos\n"
        "  - author-guidelines.md\n"
        "  - any back issues as PDF\n",
    "misc": "Anything that doesn't fit the other folders — extra photos,\n"
        "reference material, notes, a document describing a special requirement.\n"
        "Nothing here is required.\n",
}

# CSV templates written as header-only files (exact headers the build expects).
CSV_TEMPLATES = {
    "faculty":     {"faculty.csv": "name,designation,department,subject,qualification,email"},
    "events":      {"events.csv": "title,date,time,venue,description"},
    "gallery":     {"captions.csv": "filename,caption,tags"},
    "downloads":   {"list.csv": "filename,label,category"},
    "admissions":  {"programmes.csv": "level,programme,seats,fee"},
    "portal": {
        "staff.csv":       "full_name,google_email,is_active,roles",
        "students.csv":     "registration_no,first_name,last_name,program_code,section,google_email,personal_email,cnic_or_bform",
        "programs.csv":     "code,name,level",
        "sections.csv":     "section,program_code,term",
        "subjects.csv":     "code,name,program_code",
        "enrollments.csv":  "registration_no,section,term",
        "guardians.csv":    "registration_no,guardian_name,relation,phone_e164,email",
        "offerings.csv":    "subject_code,section,term,teacher_google_email,combined_with_sections",
        "timetable.csv":    "section,subject,day,period,start_time,end_time,room",
    },
    "roles":     {"offices.csv": "office,department,full_name,official_email"},
    "societies": {"societies.csv": "society,incharge_name,incharge_email,description",
                  "cabinet.csv": "name,position,program,photo"},
    "sports":    {"disciplines.csv": "discipline,incharge_name,season,venue"},
    "hostel":    {"rooms.csv": "hostel,block,room,bed,status"},
    "journal":   {"editorial-board.csv": "name,role,affiliation,email,photo"},
    # sample dropped at the top of 05-departments; copy into each dept's faculty/ folder as faculty.csv
    "departments": {"faculty-template.csv":
                    "name,designation,subject,qualification,email,phone,is_head"},
}


def write_file(path, content):
    if os.path.exists(path):
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="project folder (materials go in <root>/website-materials)")
    ap.add_argument("--only", default="", help="comma-separated keys to create (plus the always-on ones)")
    ap.add_argument("--all", action="store_true", help="create every folder")
    args = ap.parse_args()

    if args.all:
        keys = list(FOLDERS.keys())
    else:
        chosen = [k.strip() for k in args.only.split(",") if k.strip()]
        bad = [k for k in chosen if k not in FOLDERS]
        if bad:
            print("Unknown key(s):", ", ".join(bad), "\nValid:", ", ".join(FOLDERS), file=sys.stderr)
            return 2
        keys = list(dict.fromkeys(ALWAYS + chosen))

    base = os.path.join(args.root, "website-materials")
    os.makedirs(base, exist_ok=True)
    write_file(os.path.join(base, "_START-HERE.txt"),
               "Fill these labeled folders with your materials, then hand the\n"
               "project back to Claude (edu-website-builder skill) and say the\n"
               "materials are ready. Read each folder's _README.txt for what to\n"
               "put in it and the format. See the full guide: references/\n"
               "materials-folder-guide.md in the skill.\n")

    created = []
    for k in keys:
        folder = os.path.join(base, FOLDERS[k])
        os.makedirs(folder, exist_ok=True)
        write_file(os.path.join(folder, "_README.txt"), READMES[k])
        for fname, header in CSV_TEMPLATES.get(k, {}).items():
            write_file(os.path.join(folder, fname), header + "\n")
        created.append(FOLDERS[k])

    print("Created under", base + ":")
    for c in sorted(created):
        print("  -", c)
    print("\nEach folder has a _README.txt. Full guide: materials-folder-guide.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
