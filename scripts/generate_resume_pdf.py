#!/usr/bin/env python3
"""Render William_Elias_Resume.pdf from config.js so the site and PDF share one source of truth.

Usage: python3 scripts/generate_resume_pdf.py
"""
import json
import re
import sys
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
    required_top = ["personal", "summary", "skills", "experience", "projects", "education"]
    for k in required_top:
        if k not in config:
            raise ValueError(f"Validation failed: Missing required top-level field '{k}'")
    
    for k in ["skills", "experience", "projects", "education"]:
        if not isinstance(config.get(k), list):
            raise ValueError(f"Validation failed: '{k}' must be an array")
            
    p = config.get("personal", {})
    for url_field in ["linkedin", "github"]:
        val = p.get(url_field, "")
        if not (val.startswith("http://") or val.startswith("https://")):
            raise ValueError(f"Validation failed: 'personal.{url_field}' must be a valid URL starting with http:// or https://")

    for i, job in enumerate(config.get("experience", [])):
        if not isinstance(job.get("achievements"), list):
            raise ValueError(f"Validation failed: 'experience[{i}].achievements' must be an array")
            
    for i, proj in enumerate(config.get("projects", [])):
        if not isinstance(proj.get("highlights"), list):
            raise ValueError(f"Validation failed: 'projects[{i}].highlights' must be an array")


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


def build(config: dict, out_path: Path):
    p = config["personal"]
    pdf = ResumePDF()
    pdf.set_title(f'{p["name"]} - Resume')
    pdf.set_author(p["name"])
    pdf.set_creator("generate_resume_pdf.py")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 22, p["name"].upper(), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9.5)
    contact = f'{p["phone"]} | {p["email"]} | {p["linkedin"].replace("https://", "")} | {p["github"].replace("https://", "")}'
    pdf.cell(0, 14, contact, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9.5)
    tagline = p["tagline"].replace("•", "|")
    pdf.cell(0, 14, tagline, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.section_title("Professional Summary")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(0, 13, config["summary"])

    pdf.section_title("Core Skills")
    for s in config["skills"]:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.write(13, f'{s["category"]}: ')
        pdf.set_font("Helvetica", "", 9.5)
        pdf.write(13, ", ".join(s["tags"]))
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

    pdf.section_title("Projects")
    for proj in config["projects"]:
        block_h = 14 + 13 + sum(pdf.bullet_height(h) for h in proj["highlights"]) + 2
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 14, proj["name"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9.5)
        pdf.cell(0, 13, proj["subtitle"], new_x="LMARGIN", new_y="NEXT")
        for h in proj["highlights"]:
            pdf.bullet(h)
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
