import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = sys.argv[1]; OUT = sys.argv[2]
NAVY = RGBColor(0x14, 0x23, 0x3f)
GREY = RGBColor(0x5b, 0x61, 0x6b)
GOLD = "b8912e"

src = open(SRC, encoding="utf-8").read()
src = re.sub(r"<!--.*?-->", "", src, flags=re.S)  # drop HTML comments

doc = Document()
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(10.5)
for s in doc.sections:
    s.top_margin = s.bottom_margin = Inches(0.7)
    s.left_margin = s.right_margin = Inches(0.8)

def bottom_border(p, color=GOLD, size="18"):
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", size), ("w:space", "4"), ("w:color", color)):
        b.set(qn(k), v)
    pBdr.append(b); pPr.append(pBdr)

TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`|_{4,}|\[[ xX]\])")

def add_runs(p, text):
    for tok in TOKEN.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = p.add_run(tok[2:-2]); r.bold = True; r.font.color.rgb = NAVY
        elif tok.startswith("`") and tok.endswith("`"):
            r = p.add_run(tok[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(9.5)
        elif re.fullmatch(r"_{4,}", tok):
            r = p.add_run(" " * 26); r.underline = True
        elif re.fullmatch(r"\[[ xX]\]", tok):
            p.add_run(("☒" if tok[1] in "xX" else "☐") + " ")
        else:
            p.add_run(tok)

lines = src.splitlines()
for raw in lines:
    line = raw.rstrip()
    if not line.strip():
        continue
    if line.strip() == "---":
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2); bottom_border(p, "d9d9d9", "6")
        continue
    m = re.match(r"^(#{1,4})\s+(.*)$", line)
    if m:
        level, txt = len(m.group(1)), m.group(2)
        p = doc.add_paragraph()
        if level == 1:
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(txt); r.bold = True; r.font.size = Pt(19); r.font.color.rgb = NAVY
            bottom_border(p, GOLD, "20")
        elif level == 2:
            p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
            r = p.add_run(txt); r.bold = True; r.font.size = Pt(13.5); r.font.color.rgb = NAVY
            bottom_border(p, GOLD, "10")
        else:
            p.paragraph_format.space_before = Pt(6)
            r = p.add_run(txt); r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = GREY
        continue
    if line.lstrip().startswith("> "):
        p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.15)
        r0 = p.add_run(""); add_runs(p, line.lstrip()[2:])
        for r in p.runs:
            r.italic = True
            if r.font.color.rgb is None: r.font.color.rgb = GREY
        continue
    if re.match(r"^\s*[-*]\s+", line):
        content = re.sub(r"^\s*[-*]\s+", "", line)
        p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(3)
        if not re.match(r"^\[[ xX]\]", content):
            p.add_run("•  ")
        add_runs(p, content)
        continue
    p = doc.add_paragraph(); add_runs(p, line)

# A short "how to fill" note under the title (the .md's guidance lived in an HTML comment)
# Insert it right after the first heading paragraph.
note = doc.add_paragraph()
note.paragraph_format.space_before = Pt(2)
rn = note.add_run("How to fill this form:  Type your answers on the dotted lines. Tick a box by "
                  "replacing ☐ with ☒ (or type an x next to it). Leave anything you're "
                  "unsure about blank. Attach your files (logo, photos, documents) separately. "
                  "Save and email the completed form back.")
rn.italic = True; rn.font.size = Pt(9.5); rn.font.color.rgb = GREY
# move it to just after the title (index 1)
body = doc.element.body
body.remove(note._p)
title_p = doc.paragraphs[0]._p
title_p.addnext(note._p)

doc.save(OUT)
print("saved", OUT, "-", len(doc.paragraphs), "paragraphs")
