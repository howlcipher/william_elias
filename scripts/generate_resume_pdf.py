#!/usr/bin/env python3
"""Render the targeted résumé PDFs from resume.json + resume_variants.json.

resume.json is the single canonical evidence base. resume_variants.json only
selects and orders canonical items by stable ID (plus presentation-only
headline text), so every variant is a view of the same facts. The legacy
William_Elias_Resume.pdf is a byte-for-byte copy of the configured
compatibility variant, never a separately maintained résumé.

Usage: python3 scripts/generate_resume_pdf.py
"""
import json
import re
import shutil
import datetime
from pathlib import Path

from fpdf import FPDF

SITE_DIR = Path(__file__).resolve().parent.parent
MARGIN = 24  # 0.33 * 72, to ensure it strictly fits onto 2 pages
# Cap the tag list rendered per Core Expertise category. The website shows every
# tag from resume.json; the PDF shows the curated leading slice, so tag order in
# resume.json determines what a recruiter sees on page 1. Optional pdfTags select
# a concise subset explicitly when the broader website tag order is unsuitable.
# A skill category can also carry "pdfInclude": false to stay website-only
# entirely; variants cannot select such a category. A variant's skillTags may
# override the tag selection with another unique subset of the website tags.
PDF_SKILL_TAG_LIMIT = 6
VARIANTS_FILE = "resume_variants.json"
VARIANT_REQUIRED_KEYS = (
    "label", "audience", "file", "title", "supporting", "summaryStatementIds",
    "experienceAchievementIds", "skillIds", "highlightIds", "projectIds",
)
VARIANT_OPTIONAL_KEYS = ("skillTags",)
# Presentation-only strings a variant may carry. Everything factual comes from
# canonical items referenced by ID.
VARIANT_TEXT_KEYS = ("label", "audience", "title", "supporting")
VARIANT_TEXT_MAX = 90
NUMBER_PATTERN = re.compile(r"\d[\d,]*")
YEARS_CLAIM_PATTERN = re.compile(r"\b(\d+)\+ years\b")


def load_config(config_path: Path | str | None = None) -> dict:
    if config_path is None:
        config_path = SITE_DIR / "resume.json"
    raw = Path(config_path).read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except Exception as e:
        raise ValueError(f"Failed to parse resume.json. Underlying error: {e}") from e


def validate_config(config: dict):
    required_top = ["personal", "positioningStatements", "skills", "experience", "projects", "education", "selectedEngineeringPrograms", "pdfEngineeringHighlights"]
    for k in required_top:
        if k not in config:
            raise ValueError(f"Validation failed: Missing required top-level field '{k}'")

    for k in ["skills", "experience", "projects", "education", "selectedEngineeringPrograms", "pdfEngineeringHighlights"]:
        if not isinstance(config.get(k), list):
            raise ValueError(f"Validation failed: '{k}' must be an array")

    p = config.get("personal", {})
    for field in ["name", "title", "email", "tagline"]:
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
        if "pdfContext" in skill:
            context = skill["pdfContext"]
            if not isinstance(context, str) or not context.strip():
                raise ValueError(
                    f"Validation failed: 'skills[{i}].pdfContext' "
                    "must be a non-empty string when provided"
                )
        if "pdfTags" in skill:
            tags = skill["pdfTags"]
            if (not isinstance(tags, list) or not tags
                    or any(not isinstance(tag, str) or tag not in skill["tags"]
                           for tag in tags)
                    or len(set(tags)) != len(tags)):
                raise ValueError(
                    f"Validation failed: 'skills[{i}].pdfTags' "
                    "must be a non-empty unique subset of tags"
                )

    for i, job in enumerate(config.get("experience", [])):
        for field in ["company", "date", "title"]:
            if not job.get(field):
                raise ValueError(f"Validation failed: 'experience[{i}].{field}' is required and must be non-empty")
        if not isinstance(job.get("achievements"), list):
            raise ValueError(f"Validation failed: 'experience[{i}].achievements' must be an array")
        for j, achievement in enumerate(job["achievements"]):
            if not isinstance(achievement, dict) or not achievement.get("text"):
                raise ValueError(f"Validation failed: 'experience[{i}].achievements[{j}]' must be an object with non-empty text")

    for i, proj in enumerate(config.get("projects", [])):
        for field in ["name", "subtitle"]:
            if not proj.get(field):
                raise ValueError(f"Validation failed: 'projects[{i}].{field}' is required and must be non-empty")
        if not isinstance(proj.get("highlights"), list):
            raise ValueError(f"Validation failed: 'projects[{i}].highlights' must be an array")
        for field in ("link", "liveUrl"):
            if field in proj:
                val = proj[field]
                if val and not (val.startswith("http://") or val.startswith("https://")):
                    raise ValueError(
                        f"Validation failed: 'projects[{i}].{field}' must be a valid URL "
                        "starting with http:// or https://"
                    )

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

    index = canonical_index(config)

    programs = {p.get("name"): p for p in config.get("selectedEngineeringPrograms", [])}
    for i, hl in enumerate(config.get("pdfEngineeringHighlights", [])):
        source = programs.get(hl.get("sourceProgram"))
        if source is None:
            raise ValueError(f"Validation failed: 'pdfEngineeringHighlights[{i}].sourceProgram' must name an engineering program")
        missing = untraced_numbers(" ".join(hl["bullets"]), [source])
        if missing:
            raise ValueError(
                f"Validation failed: 'pdfEngineeringHighlights[{i}]' numbers {missing} "
                f"are not in its source program '{hl['sourceProgram']}'"
            )

    for i, statement in enumerate(config.get("positioningStatements") or []):
        where = f"positioningStatements[{i}]"
        if not isinstance(statement.get("text"), str) or not statement["text"].strip():
            raise ValueError(f"Validation failed: '{where}.text' must be a non-empty string")
        evidence_ids = statement.get("evidenceIds")
        if not isinstance(evidence_ids, list) or not evidence_ids:
            raise ValueError(f"Validation failed: '{where}.evidenceIds' must be a non-empty array")
        evidence = []
        for evidence_id in evidence_ids:
            kind, item = index.get(evidence_id, (None, None))
            if kind is None or kind == "positioningStatements":
                raise ValueError(f"Validation failed: '{where}' references unknown evidence ID '{evidence_id}'")
            evidence.append(item)
        missing = untraced_numbers(statement["text"], evidence)
        if missing:
            raise ValueError(f"Validation failed: '{where}' numbers {missing} are not traceable to its evidence")


def untraced_numbers(text: str, evidence: list) -> list:
    """Numbers in `text` that do not appear in the canonical `evidence` items.

    "N+ years" is traced to the earliest start year among dated evidence
    items instead, since tenure is derived from dates rather than stated.
    """
    for match in YEARS_CLAIM_PATTERN.finditer(text):
        years = [int(y) for item in evidence
                 for y in re.findall(r"\b(?:19|20)\d\d\b", str(item.get("date", "")))]
        if not years or datetime.date.today().year - min(years) < int(match.group(1)):
            return [match.group(0)]
    supported = set(NUMBER_PATTERN.findall(json.dumps(evidence, ensure_ascii=False)))
    remaining = YEARS_CLAIM_PATTERN.sub("", text)
    return [n for n in NUMBER_PATTERN.findall(remaining) if n not in supported]


def load_variants(variants_path: Path | str | None = None) -> dict:
    if variants_path is None:
        variants_path = SITE_DIR / VARIANTS_FILE
    try:
        return json.loads(Path(variants_path).read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Failed to parse {VARIANTS_FILE}. Underlying error: {e}") from e


def _strings(value):
    if isinstance(value, dict):
        for key, inner in value.items():
            yield key
            yield from _strings(inner)
    elif isinstance(value, list):
        for inner in value:
            yield from _strings(inner)
    elif isinstance(value, str):
        yield value
    else:
        yield repr(value)


def _unique_id_list(value, where, index, kind):
    if not isinstance(value, list) or not value:
        raise ValueError(f"Validation failed: '{where}' must be a non-empty array of IDs")
    if len(set(value)) != len(value):
        raise ValueError(f"Validation failed: '{where}' must not repeat IDs")
    for item_id in value:
        if index.get(item_id, (None,))[0] != kind:
            raise ValueError(f"Validation failed: '{where}' references unknown {kind} ID '{item_id}'")
    return [index[item_id][1] for item_id in value]


def validate_variants(config: dict, variants: dict):
    """Variants may only select/reorder canonical items and add short headline text.

    Any digit anywhere in the variant document fails validation, so a variant
    can never introduce its own metric; every number on a résumé comes from a
    referenced canonical item.
    """
    if not isinstance(variants, dict) or set(variants) != {"compatibility", "variants"}:
        raise ValueError("Validation failed: variants must contain exactly 'compatibility' and 'variants'")
    for text in _strings(variants):
        if any(ch.isdigit() for ch in text):
            raise ValueError(f"Validation failed: variant configuration must not contain numbers: {text!r}")
    index = canonical_index(config)
    defined = variants["variants"]
    if not isinstance(defined, dict) or not defined:
        raise ValueError("Validation failed: 'variants' must be a non-empty object")
    files = set()
    for name, variant in defined.items():
        where = f"variants.{name}"
        if not isinstance(variant, dict):
            raise ValueError(f"Validation failed: '{where}' must be an object")
        unknown = set(variant) - set(VARIANT_REQUIRED_KEYS) - set(VARIANT_OPTIONAL_KEYS)
        if unknown:
            raise ValueError(f"Validation failed: '{where}' has unsupported keys {sorted(unknown)}")
        for key in VARIANT_REQUIRED_KEYS:
            if key not in variant:
                raise ValueError(f"Validation failed: '{where}.{key}' is required")
        for key in VARIANT_TEXT_KEYS:
            value = variant[key]
            if not isinstance(value, str) or not value.strip() or len(value) > VARIANT_TEXT_MAX:
                raise ValueError(f"Validation failed: '{where}.{key}' must be short presentation text")
        if not re.fullmatch(r"[A-Za-z_]+\.pdf", variant["file"]) or variant["file"] in files:
            raise ValueError(f"Validation failed: '{where}.file' must be a unique PDF filename")
        files.add(variant["file"])

        _unique_id_list(variant["summaryStatementIds"], f"{where}.summaryStatementIds", index, "positioningStatements")
        skills = _unique_id_list(variant["skillIds"], f"{where}.skillIds", index, "skills")
        for skill in skills:
            if skill.get("pdfInclude") is False:
                raise ValueError(f"Validation failed: '{where}.skillIds' selects website-only skill '{skill['id']}'")
        skill_tags = variant.get("skillTags", {})
        if not isinstance(skill_tags, dict):
            raise ValueError(f"Validation failed: '{where}.skillTags' must be an object")
        for skill_id, tags in skill_tags.items():
            if skill_id not in variant["skillIds"]:
                raise ValueError(f"Validation failed: '{where}.skillTags' references unselected skill '{skill_id}'")
            allowed = index[skill_id][1]["tags"]
            if (not isinstance(tags, list) or not tags or len(set(tags)) != len(tags)
                    or any(tag not in allowed for tag in tags)):
                raise ValueError(f"Validation failed: '{where}.skillTags.{skill_id}' must be a non-empty unique subset of tags")
        _unique_id_list(variant["highlightIds"], f"{where}.highlightIds", index, "pdfEngineeringHighlights")
        _unique_id_list(variant["projectIds"], f"{where}.projectIds", index, "projects")

        selections = variant["experienceAchievementIds"]
        if not isinstance(selections, dict):
            raise ValueError(f"Validation failed: '{where}.experienceAchievementIds' must be an object")
        for job_id, achievement_ids in selections.items():
            if index.get(job_id, (None,))[0] != "experience":
                raise ValueError(f"Validation failed: '{where}.experienceAchievementIds' references unknown experience ID '{job_id}'")
            owned = {a["id"] for a in index[job_id][1]["achievements"]}
            _unique_id_list(achievement_ids, f"{where}.experienceAchievementIds.{job_id}", index, "achievement")
            stray = [a for a in achievement_ids if a not in owned]
            if stray:
                raise ValueError(f"Validation failed: '{where}.experienceAchievementIds.{job_id}' selects achievements of another role: {stray}")

    compatibility = variants["compatibility"]
    if (not isinstance(compatibility, dict) or set(compatibility) != {"file", "variant"}
            or compatibility["variant"] not in defined
            or not re.fullmatch(r"[A-Za-z_]+\.pdf", str(compatibility["file"]))
            or compatibility["file"] in files):
        raise ValueError("Validation failed: 'compatibility' must alias a defined variant under a distinct PDF filename")


def resolve_variant(config: dict, variants: dict, name: str) -> dict:
    """Build the render view for one variant from canonical items only."""
    if name not in variants["variants"]:
        raise ValueError(f"Validation failed: unknown résumé variant '{name}'")
    variant = variants["variants"][name]
    index = canonical_index(config)
    selections = variant["experienceAchievementIds"]
    experience = []
    for job in config["experience"]:
        chosen = selections.get(job["id"])
        achievements = [index[a][1] for a in chosen] if chosen is not None else list(job["achievements"])
        experience.append({**job, "achievements": achievements})
    skills = []
    for skill_id in variant["skillIds"]:
        skill = dict(index[skill_id][1])
        if skill_id in variant.get("skillTags", {}):
            skill["pdfTags"] = variant["skillTags"][skill_id]
        skills.append(skill)
    return {
        "name": name,
        "label": variant["label"],
        "file": variant["file"],
        "title": variant["title"],
        "supporting": variant["supporting"],
        "summary": " ".join(index[s][1]["text"] for s in variant["summaryStatementIds"]),
        "experience": experience,
        "skills": skills,
        "highlights": [index[h][1] for h in variant["highlightIds"]],
        "projects": [index[p][1] for p in variant["projectIds"]],
    }


# Canonical collections whose entries carry a stable, human-readable "id".
# Variant selection references these IDs, never array positions.
ID_COLLECTIONS = (
    "skills", "experience", "additionalExperience", "selectedEngineeringPrograms",
    "pdfEngineeringHighlights", "projects", "education",
)
ID_PATTERN = re.compile(r"^[a-z]+(?:-[a-z]+)+$")


def canonical_index(config: dict) -> dict:
    """Return {id: (kind, item)} for every identified canonical item.

    IDs must be unique across the whole document, lowercase-hyphenated, and
    free of digits so they can never encode an array position or a metric.
    """
    index = {}

    def register(kind, item, where):
        item_id = item.get("id") if isinstance(item, dict) else None
        if not isinstance(item_id, str) or not ID_PATTERN.match(item_id):
            raise ValueError(f"Validation failed: '{where}.id' must be a lowercase hyphenated ID without digits")
        if item_id in index:
            raise ValueError(f"Validation failed: duplicate canonical ID '{item_id}'")
        index[item_id] = (kind, item)

    for kind in ID_COLLECTIONS:
        for i, item in enumerate(config.get(kind) or []):
            register(kind, item, f"{kind}[{i}]")
    for i, job in enumerate(config.get("experience") or []):
        for j, achievement in enumerate(job.get("achievements") or []):
            register("achievement", achievement, f"experience[{i}].achievements[{j}]")
    for i, statement in enumerate(config.get("positioningStatements") or []):
        register("positioningStatements", statement, f"positioningStatements[{i}]")
    return index


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
        self.set_font("Helvetica", "", 10)
        indent = 12
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.r_margin - self.l_margin - indent, 13, f"- {text}", align="L")

    def bullet_height(self, text, indent=12):
        self.set_font("Helvetica", "", 10)
        width = self.w - self.r_margin - self.l_margin - indent
        lines = self.multi_cell(width, 13, f"- {text}", dry_run=True, output="LINES")
        return len(lines) * 13

    def keep_together(self, height):
        """Force a page break now if `height` of content wouldn't fit on the
        current page, so a block's header never gets orphaned from its body."""
        if self.will_page_break(height):
            self.add_page()

    def wrapped_text_height(self, text, size=9):
        self.set_font("Helvetica", "", size)
        width = self.w - self.r_margin - self.l_margin
        lines = self.multi_cell(width, 13, text, dry_run=True, output="LINES")
        return len(lines) * 13

    def indented_text_height(self, text, indent=12, size=9, line_h=12):
        self.set_font("Helvetica", "I", size)
        width = self.w - self.r_margin - self.l_margin - indent
        lines = self.multi_cell(width, line_h, text, dry_run=True, output="LINES")
        return len(lines) * line_h

    def indented_text(self, text, indent=12, size=9, line_h=12):
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


def build(config: dict, out_path: Path, variant: str | None = None, variants: dict | None = None):
    """Render one résumé variant. Defaults to the compatibility variant, i.e.
    exactly what William_Elias_Resume.pdf contains."""
    if variants is None:
        variants = load_variants()
    validate_variants(config, variants)
    view = resolve_variant(config, variants, variant or variants["compatibility"]["variant"])
    p = config["personal"]
    pdf = ResumePDF()
    pdf.set_title(f'{p["name"]} - {view["label"]}')
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
    pdf.cell(0, 14, view["title"].upper(), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "I", 9.5)
    pdf.cell(0, 13, view["supporting"].replace("•", "|"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.centered_link_row([
        (p["location"], None),
        (p["remote"], None),
        (p["email"], f'mailto:{p["email"]}'),
    ])

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
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 13, view["summary"], align="L")

    # Only the two current-era roles carry bullets here; earlier roles get their
    # own compressed section further down so they cost minimal page space.
    pdf.section_title("Professional Experience")
    for job in view["experience"]:
        achievements = job.get("achievements", [])
        block_h = 13 + 13 + sum(pdf.bullet_height(a["text"]) for a in achievements) + 2
        if pdf.will_page_break(block_h):
            pdf.add_page()
            pdf.section_title("Professional Experience (Continued)")

        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 140, 13, job["company"])
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(140, 13, job["date"], align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9.5)
        title_line = job["title"] + (f' | {job["location"]}' if job.get("location") else "")
        pdf.cell(0, 13, title_line, new_x="LMARGIN", new_y="NEXT")
        for a in achievements:
            pdf.bullet(a["text"])
        pdf.ln(2)

    pdf.section_title("Core Expertise")
    for s in view["skills"]:
        # A category line that wraps must not split across the page break.
        context = f' ({s["pdfContext"]})' if s.get("pdfContext") else ""
        line = f'{s["category"]}{context}: ' + ", ".join(s.get("pdfTags", s["tags"][:PDF_SKILL_TAG_LIMIT]))
        pdf.keep_together(pdf.wrapped_text_height(line, size=10))
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(13, s["category"])
        if s.get("pdfContext"):
            pdf.set_font("Helvetica", "I", 10)
            pdf.write(13, f' ({s["pdfContext"]})')
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(13, ': ')
        pdf.set_font("Helvetica", "", 10)
        pdf.write(13, ", ".join(s.get("pdfTags", s["tags"][:PDF_SKILL_TAG_LIMIT])))
        pdf.ln(13)

    # Sourced from the variant's highlightIds: curated condensations of the
    # website's selectedEngineeringPrograms. The site keeps all programs; each
    # PDF carries only the evidence its target roles care about most.
    highlights_height = 28
    for highlight in view["highlights"]:
        highlights_height += 15 + sum(pdf.bullet_height(b) for b in highlight['bullets'])
        if highlight.get('technology'):
            highlights_height += pdf.indented_text_height('Tech: ' + ', '.join(highlight['technology']))
    pdf.keep_together(highlights_height)

    pdf.section_title("Selected Engineering Highlights")
    for prog in view["highlights"]:
        bullets = prog.get("bullets") or []
        tech = prog.get("technology") or []
        tech_line = ("Tech: " + ", ".join(tech)) if tech else ""
        block_h = 13 + sum(pdf.bullet_height(b) for b in bullets)
        if tech_line:
            block_h += pdf.indented_text_height(tech_line)
        block_h += 2
        if pdf.will_page_break(block_h):
            pdf.add_page()
            pdf.section_title("Selected Engineering Highlights (Continued)")
        pdf.keep_together(block_h)
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(0, 13, prog.get("name", ""), new_x="LMARGIN", new_y="NEXT")
        for b in bullets:
            pdf.bullet(b)
        if tech_line:
            pdf.indented_text(tech_line)
        pdf.ln(2)

    pdf_projects = view["projects"]
    if pdf_projects:
        pdf.section_title("Selected Open-Source Engineering")
        for proj in pdf_projects:
            # Live Pages links render on the website cards. A second URL line
            # here pushed the software résumé onto a third page, so the PDF
            # keeps the repository link only.
            block_h = 13 + 13 + sum(pdf.bullet_height(h) for h in proj["highlights"]) + 2
            pdf.keep_together(block_h)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.cell(0, 13, proj["name"], new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            link_clean = proj["link"].replace("https://", "")
            # Sized to the text, not the full line, so the clickable region
            # matches what is actually underlined-looking to the reader.
            pdf.cell(pdf.get_string_width(link_clean), 13, link_clean,
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
            block_h = 13 + (pdf.bullet_height(summary) if summary else 0) + 2
            pdf.keep_together(block_h)
            pdf.set_font("Helvetica", "B", 10.5)
            title_line = f'{job["title"]}, {job["company"]}'
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin - 140, 13, title_line)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(140, 13, job["date"], align="R", new_x="LMARGIN", new_y="NEXT")
            if summary:
                pdf.bullet(summary)
            pdf.ln(2)

    pdf.section_title("Education & Certifications")
    pdf.set_font("Helvetica", "", 10)
    for e in config["education"]:
        year = f' ({e["year"]})' if e.get("year") else ""
        pdf.cell(0, 13, f'{e["degree"]} - {e["school"]}{year}', new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out_path))


def generate_all(site_dir: Path = SITE_DIR) -> list[Path]:
    """Write every variant PDF, then the legacy compatibility alias as a byte copy."""
    cfg = load_config(site_dir / "resume.json")
    validate_config(cfg)
    variants = load_variants(site_dir / VARIANTS_FILE)
    validate_variants(cfg, variants)
    written = []
    for name, variant in variants["variants"].items():
        out = site_dir / variant["file"]
        build(cfg, out, name, variants)
        written.append(out)
    compatibility = variants["compatibility"]
    alias = site_dir / compatibility["file"]
    shutil.copyfile(site_dir / variants["variants"][compatibility["variant"]]["file"], alias)
    written.append(alias)
    return written


if __name__ == "__main__":
    for path in generate_all():
        print(f"Wrote {path}")
