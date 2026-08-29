#!/usr/bin/env python3
"""Render William_Elias_Resume.pdf from resume.json so the site and PDF share one source of truth.

Usage: python3 scripts/generate_resume_pdf.py
"""
import json
import re
import sys
import datetime
from pathlib import Path

from fpdf import FPDF

SITE_DIR = Path(__file__).resolve().parent.parent
MARGIN = 24  # 0.33 * 72, to ensure it strictly fits onto 2 pages
# Cap the tag list rendered per Core Expertise category. The website shows every
# tag from resume.json; the PDF shows the curated leading slice, so tag order in
# resume.json determines what a recruiter sees on page 1. A skill category can also
# carry "pdfInclude": false to stay website-only entirely (same idiom as
# projects[].pdfInclude), keeping breadth-only categories off the PDF's page budget.
PDF_SKILL_TAG_LIMIT = 6


def load_config(config_path: Path | str | None = None) -> dict:
    if config_path is None:
        config_path = SITE_DIR / "resume.json"
    raw = Path(config_path).read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except Exception as e:
        raise ValueError(f"Failed to parse resume.json. Underlying error: {e}") from e

def validate_config(config: dict):
    required_top = ["personal", "summary", "skills", "experience", "projects", "education", "selectedEngineeringPrograms", "pdfEngineeringHighlights"]
    for k in required_top:
        if k not in config:
            raise ValueError(f"Validation failed: Missing required top-level field '{k}'")

    for k in ["skills", "experience", "projects", "education", "selectedEngineeringPrograms", "pdfEngineeringHighlights"]:
        if not isinstance(config.get(k), list):
            raise ValueError(f"Validation failed: '{k}' must be an array")
            
    p = config.get("personal", {})
    for field in ["name", "title", "phone", "email", "tagline"]:
        if not p.get(field):
            raise ValueError(f"Validation failed: 'personal.{field}' is required and must be non-empty")

    for url_field in ["linkedin", "github"]:
        val = p.get(url_field, "")
        if not (val.startswith("http://") or val.startswith("https://")):
            raise ValueError(f"Validation failed: 'personal.{url_field}' must be a valid URL starting with http:// or https://")

    for i, skill in enumerate(config.get("skills", [])):
        for field in ["category", "tags"]:
            if field not in skill or not skill[field]:
                raise ValueError(f"Validation failed: 'skills[{i}].{field}' is required and must be non-empty")

    for i, job in enumerate(config.get("experience", [])):
        for field in ["company", "date", "title"]:
            if not job.get(field):
                raise ValueError(f"Validation failed: 'experience[{i}].{field}' is required and must be non-empty")
        if not isinstance(job.get("achievements"), list):
            raise ValueError(f"Validation failed: 'experience[{i}].achievements' must be an array")
            
    for i, proj in enumerate(config.get("projects", [])):
        for field in ["name", "subtitle"]:
            if not proj.get(field):
                raise ValueError(f"Validation failed: 'projects[{i}].{field}' is required and must be non-empty")
        if not isinstance(proj.get("highlights"), list):
            raise ValueError(f"Validation failed: 'projects[{i}].highlights' must be an array")
        if "link" in proj:
            val = proj["link"]
            if val and not (val.startswith("http://") or val.startswith("https://")):
                raise ValueError(f"Validation failed: 'projects[{i}].link' must be a valid URL starting with http:// or https://")

    for i, edu in enumerate(config.get("education", [])):
        for field in ["degree", "school"]:
            if not edu.get(field):
                raise ValueError(f"Validation failed: 'education[{i}].{field}' is required and must be non-empty")

    for i, prog in enumerate(config.get("selectedEngineeringPrograms", [])):
        if not prog.get("name"):
            raise ValueError(f"Validation failed: 'selectedEngineeringPrograms[{i}].name' is required and must be non-empty")

    for i, hl in enumerate(config.get("pdfEngineeringHighlights", [])):
        if not hl.get("name"):
            raise ValueError(f"Validation failed: 'pdfEngineeringHighlights[{i}].name' is required and must be non-empty")
        if not hl.get("bullets") or not isinstance(hl.get("bullets"), list):
            raise ValueError(f"Validation failed: 'pdfEngineeringHighlights[{i}].bullets' must be a non-empty array")

class ResumePDF(FPDF):
    def __init__(self):
        super().__init__(format="Letter", unit="pt")
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(True, margin=MARGIN)

    def section_title(self, text):
        self.ln(10)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 14, text.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9)
        indent = 12
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.r_margin - self.l_margin - indent, 11.5, f"- {text}")

    def bullet_height(self, text, indent=12):
        self.set_font("Helvetica", "", 9)
        width = self.w - self.r_margin - self.l_margin - indent
        lines = self.multi_cell(width, 11.5, f"- {text}", dry_run=True, output="LINES")
        return len(lines) * 11.5

    def keep_together(self, height):
        """Force a page break now if `height` of content wouldn't fit on the
        current page, so a block's header never gets orphaned from its body."""
        if self.will_page_break(height):
            self.add_page()

    def wrapped_text_height(self, text, size=9):
        self.set_font("Helvetica", "", size)
        width = self.w - self.r_margin - self.l_margin
        lines = self.multi_cell(width, 11.5, text, dry_run=True, output="LINES")
        return len(lines) * 11.5

    def indented_text_height(self, text, indent=12, size=8.5, line_h=11):
        self.set_font("Helvetica", "I", size)
        width = self.w - self.r_margin - self.l_margin - indent
        lines = self.multi_cell(width, line_h, text, dry_run=True, output="LINES")
        return len(lines) * line_h

    def indented_text(self, text, indent=12, size=8.5, line_h=11):
        self.set_font("Helvetica", "I", size)
        self.set_x(self.l_margin + indent)
        self.set_text_color(90, 90, 90)
        self.multi_cell(self.w - self.r_margin - self.l_margin - indent, line_h, text)
        self.set_text_color(0, 0, 0)

    def centered_link_row(self, entries, height=14, separator=" | "):
        """Render `entries` of (visible_text, url) centered on one line, each
        segment individually clickable.

        A cell carries at most one link, so the row is laid out segment by
        segment instead of as a single centered cell. The visible text is
        byte-identical to the plain-text version, which keeps ATS extraction
        unchanged; only the link annotations are new."""
        # Cells normally pad their text by c_margin; zeroing it here makes each
        # segment exactly as wide as its glyphs, so the row centers precisely and
        # each link's clickable rectangle hugs its own text.
        previous_margin = self.c_margin
        self.c_margin = 0
        try:
            sep_width = self.get_string_width(separator)
            widths = [self.get_string_width(text) for text, _ in entries]
            total = sum(widths) + sep_width * (len(entries) - 1)
            self.set_x((self.w - total) / 2)
            for i, ((text, url), width) in enumerate(zip(entries, widths)):
                if i:
                    self.cell(sep_width, height, separator)
                self.cell(width, height, text, link=url or "")
        finally:
            self.c_margin = previous_margin
        self.ln(height)


def build(config: dict, out_path: Path):
    p = config["personal"]
    pdf = ResumePDF()
    pdf.set_title(f'{p["name"]} - Resume')
    pdf.set_author(p["name"])
    pdf.set_creator("generate_resume_pdf.py")
    # Make generation deterministic for CI byte-for-byte checks.
    # Stream compression is also disabled: fpdf2 compresses via zlib, and different
    # zlib builds (e.g. zlib-ng vs stock zlib) produce different compressed bytes for
    # identical content, which broke byte-for-byte comparison across environments.
    pdf.set_creation_date(datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc))
    pdf.compress = False
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 22, p["name"].upper(), align="C", new_x="LMARGIN", new_y="NEXT")

    # Title and tagline get their own lines: the target role should read as the
    # headline, not as the first half of a long combined string.
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 14, p["title"].replace("//", "|").upper(), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "I", 9.5)
    pdf_tagline = p.get("pdfSupporting") or p.get("supporting") or p["tagline"]
    pdf.cell(0, 13, pdf_tagline.replace("•", "|"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    location_contact = f'{p["location"]} | {p["remote"]} | {p["phone"]} | {p["email"]}'
    pdf.cell(0, 14, location_contact, align="C", new_x="LMARGIN", new_y="NEXT")

    # LinkedIn, GitHub, and the portfolio site, each clickable. The portfolio is
    # the broader proof layer behind this selective document, so the PDF has to
    # point at it; it comes from the same seo.canonicalUrl the site is built from.
    links = [
        (p["linkedin"].replace("https://", "").rstrip("/"), p["linkedin"]),
        (p["github"].replace("https://", "").rstrip("/"), p["github"]),
    ]
    portfolio = (config.get("seo") or {}).get("canonicalUrl") or ""
    if portfolio:
        links.append((re.sub(r"^https?://", "", portfolio).rstrip("/"), portfolio))
    pdf.centered_link_row(links)

    pdf.section_title("Professional Summary")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 11.5, config.get("resumeSummary") or config["summary"])

    pdf.section_title("Core Expertise")
    for s in config["skills"]:
        if s.get("pdfInclude") is False:
            continue
        pdf.set_font("Helvetica", "B", 9)
        pdf.write(11.5, f'{s["category"]}: ')
        pdf.set_font("Helvetica", "", 9)
        pdf.write(11.5, ", ".join(s["tags"][:PDF_SKILL_TAG_LIMIT]))
        pdf.ln(11.5)

    # Only the two current-era roles carry bullets here; earlier roles get their
    # own compressed section further down so they cost minimal page space.
    pdf.section_title("Professional Experience")
    for job in config.get("experience", []):
        achievements = job.get("achievements", [])
        block_h = 11.5 + 11.5 + sum(pdf.bullet_height(a) for a in achievements) + 2
        if pdf.will_page_break(block_h):
            pdf.add_page()
            pdf.section_title("Professional Experience (Continued)")
            
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 140, 11.5, job["company"])
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(140, 11.5, job["date"], align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9.5)
        title_line = job["title"] + (f' | {job["location"]}' if job.get("location") else "")
        pdf.cell(0, 11.5, title_line, new_x="LMARGIN", new_y="NEXT")
        for a in achievements:
            pdf.bullet(a)
        pdf.ln(2)

    # Sourced from pdfEngineeringHighlights, a curated 3-entry condensation of the
    # website's selectedEngineeringPrograms. The site keeps all six programs; the
    # PDF carries only the strongest evidence so page 2 stays scannable.
    first_hl = (config.get("pdfEngineeringHighlights") or [{}])[0]
    first_bullets = first_hl.get("bullets") or []
    first_tech = first_hl.get("technology") or []
    first_tech_line = ("Tech: " + ", ".join(first_tech)) if first_tech else ""
    first_block_h = 28 + 11.5 + sum(pdf.bullet_height(b) for b in first_bullets)
    if first_tech_line:
        first_block_h += pdf.indented_text_height(first_tech_line)
    first_block_h += 2
    if pdf.will_page_break(first_block_h):
        pdf.add_page()

    pdf.section_title("Selected Engineering Highlights")
    for prog in config.get("pdfEngineeringHighlights") or []:
        bullets = prog.get("bullets") or []
        tech = prog.get("technology") or []
        tech_line = ("Tech: " + ", ".join(tech)) if tech else ""
        block_h = 11.5 + sum(pdf.bullet_height(b) for b in bullets)
        if tech_line:
            block_h += pdf.indented_text_height(tech_line)
        block_h += 2
        if pdf.will_page_break(block_h):
            pdf.add_page()
            pdf.section_title("Selected Engineering Highlights (Continued)")
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.cell(0, 11.5, prog.get("name", ""), new_x="LMARGIN", new_y="NEXT")
        for b in bullets:
            pdf.bullet(b)
        if tech_line:
            pdf.indented_text(tech_line)
        pdf.ln(2)

    pdf_projects = [p for p in config.get("projects", []) if p.get("pdfInclude")]
    if pdf_projects:
        pdf.section_title("Selected Open-Source Engineering")
        for proj in pdf_projects:
            block_h = 11.5 + 11.5 + sum(pdf.bullet_height(h) for h in proj["highlights"]) + 2
            pdf.keep_together(block_h)
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.cell(0, 11.5, proj["name"], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9)
            link_clean = proj["link"].replace("https://", "")
            # Sized to the text, not the full line, so the clickable region
            # matches what is actually underlined-looking to the reader.
            pdf.cell(pdf.get_string_width(link_clean), 11.5, link_clean,
                     link=proj["link"], new_x="LMARGIN", new_y="NEXT")
            for h in proj["highlights"]:
                pdf.bullet(h)
            pdf.ln(2)

    earlier_jobs = config.get("additionalExperience") or []
    if earlier_jobs:
        # Compressed to two lines per role: these establish the infrastructure and
        # networking progression into DevOps without consuming resume space.
        pdf.section_title("Earlier Experience")
        for job in earlier_jobs:
            summary = job.get("summary", "")
            block_h = 11.5 + (pdf.bullet_height(summary) if summary else 0) + 2
            pdf.keep_together(block_h)
            pdf.set_font("Helvetica", "B", 9.5)
            title_line = f'{job["title"]}, {job["company"]}'
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 140, 11.5, title_line)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(140, 11.5, job["date"], align="R", new_x="LMARGIN", new_y="NEXT")
            if summary:
                pdf.bullet(summary)
            pdf.ln(2)

    pdf.section_title("Education & Certifications")
    pdf.set_font("Helvetica", "", 9)
    for e in config["education"]:
        year = f' ({e["year"]})' if e.get("year") else ""
        pdf.cell(0, 11.5, f'{e["degree"]} - {e["school"]}{year}', new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out_path))


if __name__ == "__main__":
    cfg = load_config()
    validate_config(cfg)
    out = SITE_DIR / "William_Elias_Resume.pdf"
    build(cfg, out)
    print(f"Wrote {out}")
