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
MARGIN = 0.75 * 72  # 54pt, matches the source PDF's visual margins


def load_config(config_path: Path | str | None = None) -> dict:
    if config_path is None:
        config_path = SITE_DIR / "resume.json"
    raw = Path(config_path).read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except Exception as e:
        raise ValueError(f"Failed to parse resume.json. Underlying error: {e}") from e

def validate_config(config: dict):
    required_top = ["personal", "summary", "skills", "experience", "projects", "education", "selectedEngineeringPrograms"]
    for k in required_top:
        if k not in config:
            raise ValueError(f"Validation failed: Missing required top-level field '{k}'")

    for k in ["skills", "experience", "projects", "education", "selectedEngineeringPrograms"]:
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
        self.set_font("Helvetica", "", 9.5)
        indent = 12
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.r_margin - self.l_margin - indent, 13, f"- {text}")

    def bullet_height(self, text, indent=12):
        self.set_font("Helvetica", "", 9.5)
        width = self.w - self.r_margin - self.l_margin - indent
        lines = self.multi_cell(width, 13, f"- {text}", dry_run=True, output="LINES")
        return len(lines) * 13

    def keep_together(self, height):
        """Force a page break now if `height` of content wouldn't fit on the
        current page, so a block's header never gets orphaned from its body."""
        if self.will_page_break(height):
            self.add_page()

    def wrapped_text_height(self, text, size=9.5):
        self.set_font("Helvetica", "", size)
        width = self.w - self.r_margin - self.l_margin
        lines = self.multi_cell(width, 13, text, dry_run=True, output="LINES")
        return len(lines) * 13

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

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 15, p["title"].replace("//", "|"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9.5)
    contact = f'{p["phone"]} | {p["email"]} | {p["linkedin"].replace("https://", "")} | {p["github"].replace("https://", "")}'
    pdf.cell(0, 14, contact, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9.5)
    tagline = p["tagline"].replace("•", "|")
    pdf.cell(0, 14, tagline, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.section_title("Professional Summary")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(0, 13, config["summary"])

    pdf.section_title("Core Expertise")
    for s in config["skills"]:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.write(13, f'{s["category"]}: ')
        pdf.set_font("Helvetica", "", 9.5)
        # Cap the tag list rendered in the PDF (the website shows the full list from
        # resume.json) so six categories of curated skills stay on page 1.
        pdf.write(13, ", ".join(s["tags"][:9]))
        pdf.ln(14)

    pdf.section_title("Professional Experience")
    for job in config["experience"]:
        block_h = 14 + 13 + sum(pdf.bullet_height(a) for a in job["achievements"]) + 2
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 140, 14, job["company"])
        pdf.set_font("Helvetica", "", 9.5)
        pdf.cell(140, 14, job["date"], align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9.5)
        title_line = job["title"] + (f' | {job["location"]}' if job.get("location") else "")
        pdf.cell(0, 13, title_line, new_x="LMARGIN", new_y="NEXT")
        for a in job["achievements"]:
            pdf.bullet(a)
        pdf.ln(2)

    # Deliberate page break: Selected Engineering Programs always starts a fresh
    # page, even when page 1 has unused whitespace, so the section reads as one
    # coherent block rather than splitting mid-program.
    pdf.add_page()

    pdf.section_title("Selected Engineering Programs")
    for prog in config.get("selectedEngineeringPrograms") or []:
        pdf_bullet = prog.get("pdfBullet") or ""
        tech = prog.get("technology") or []
        tech_line = ("Technology: " + ", ".join(tech)) if tech else ""
        block_h = 14
        if pdf_bullet:
            block_h += pdf.bullet_height(pdf_bullet)
        if tech_line:
            block_h += pdf.indented_text_height(tech_line)
        block_h += 2
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 14, prog.get("name", ""), new_x="LMARGIN", new_y="NEXT")
        if pdf_bullet:
            pdf.bullet(pdf_bullet)
        if tech_line:
            pdf.indented_text(tech_line)
        pdf.ln(2)

    additional_experience = config.get("additionalExperience") or []
    if additional_experience:
        pdf.section_title("Earlier Technical Experience")
        for job in additional_experience:
            summary = job.get("summary", "")
            block_h = 14 + pdf.wrapped_text_height(summary) + 2
            pdf.keep_together(block_h)
            pdf.set_font("Helvetica", "B", 9.5)
            header = f'{job.get("company", "")} - {job.get("title", "")} | {job.get("date", "")}'
            pdf.cell(0, 14, header, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.multi_cell(0, 13, summary)
            pdf.ln(2)

    pdf.section_title("Education & Certifications")
    pdf.set_font("Helvetica", "", 9.5)
    for e in config["education"]:
        year = f' ({e["year"]})' if e.get("year") else ""
        pdf.cell(0, 14, f'{e["degree"]} - {e["school"]}{year}', new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out_path))


if __name__ == "__main__":
    cfg = load_config()
    validate_config(cfg)
    out = SITE_DIR / "William_Elias_Resume.pdf"
    build(cfg, out)
    print(f"Wrote {out}")
