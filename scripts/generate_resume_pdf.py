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
    tagline = p["tagline"].replace("•", "|")
    combined_title = f'{p["title"].replace("//", "|")} | {tagline}'
    pdf.cell(0, 15, combined_title, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    location_contact = f'{p["location"]} | {p["remote"]} | {p["phone"]} | {p["email"]}'
    pdf.cell(0, 14, location_contact, align="C", new_x="LMARGIN", new_y="NEXT")

    contact = f'{p["linkedin"].replace("https://", "")} | {p["github"].replace("https://", "")}'
    pdf.cell(0, 14, contact, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.section_title("Professional Summary")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(0, 11.5, config["summary"])

    pdf.section_title("Core Expertise")
    for s in config["skills"]:
        pdf.set_font("Helvetica", "B", 9)
        pdf.write(11.5, f'{s["category"]}: ')
        pdf.set_font("Helvetica", "", 9)
        # Cap the tag list rendered in the PDF (the website shows the full list from
        # resume.json) so six categories of curated skills stay on page 1.
        pdf.write(11.5, ", ".join(s["tags"][:7]))
        pdf.ln(11.5)

    print("Before Prof Exp:", pdf.get_y()); pdf.section_title("Professional Experience")
    all_jobs = config.get("experience", []) + config.get("additionalExperience", [])
    for job in all_jobs:
        achievements = job.get("achievements", [])
        if "summary" in job:
            achievements = [job["summary"]]
            
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

    pdf.section_title("Selected DevOps & Platform Engineering Highlights")
    for prog in config.get("selectedEngineeringPrograms") or []:
        bullets = prog.get("bullets") or []
        tech = prog.get("technology") or []
        tech_line = ("Tech: " + ", ".join(tech)) if tech else ""
        block_h = 11.5 + sum(pdf.bullet_height(b) for b in bullets)
        if tech_line:
            block_h += pdf.indented_text_height(tech_line)
        block_h += 2
        if pdf.will_page_break(block_h):
            pdf.add_page()
            pdf.section_title("Selected DevOps & Platform Engineering Highlights (Continued)")
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
            pdf.cell(0, 11.5, link_clean, new_x="LMARGIN", new_y="NEXT")
            for h in proj["highlights"]:
                pdf.bullet(h)
            pdf.ln(2)

    pdf.section_title("Education & Certification")
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
