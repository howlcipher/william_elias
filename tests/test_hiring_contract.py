import html
import json
import re
from html.parser import HTMLParser

import pytest

from conftest import VARIANT_NAMES
from scripts.generate_resume_pdf import SITE_DIR, load_config, load_variants


class StructuredDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json = False
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.in_json = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_json = False

    def handle_data(self, data):
        if self.in_json:
            self.blocks.append(json.loads(data))


def test_structured_data_is_parseable_without_stripping_html_comments():
    parser = StructuredDataParser()
    parser.feed((SITE_DIR / "index.html").read_text())
    assert len(parser.blocks) == 1
    profile = parser.blocks[0]
    assert profile["@type"] == "ProfilePage"
    assert profile["mainEntity"]["name"] == "William Elias"
    assert profile["isPartOf"]["@type"] == "WebSite"
    assert profile["isPartOf"]["url"] == load_config()["seo"]["canonicalUrl"]


def test_artifacts_precede_metrics_and_keyword_inventory():
    page = (SITE_DIR / "index.html").read_text()
    ids = ["hero-content-target", "about", "what-i-build", "resume-downloads", "programs", "experience", "projects",
           "education", "skills", "portfolio-build", "contact-cta"]
    positions = [page.index(f'id="{section}"') for section in ids]
    assert positions == sorted(positions)
    assert '>Selected Work</h2>' in page
    assert 'id="stats-target"' not in page


def test_about_is_three_short_paragraphs_without_repeated_delivery_counts():
    cfg = load_config()
    paragraphs = [part.strip() for part in cfg["about"].split("\n\n") if part.strip()]
    assert len(paragraphs) == 3
    assert len(cfg["about"].split()) <= 170
    page = (SITE_DIR / "index.html").read_text()
    about = page.split('id="about"')[1].split("</section>")[0]
    assert ">About</h2>" in about
    for paragraph in paragraphs:
        assert html.escape(paragraph) in about
    variants = load_variants()["variants"].values()
    first_impression = " ".join([
        cfg["about"], cfg["personal"]["supporting"],
        *(s["text"] for s in cfg["positioningStatements"]),
        *(v["title"] + v["supporting"] for v in variants),
    ])
    for count in ("56", "27/28", "25/28", "60", "104", "866", "67"):
        assert count not in first_impression


def test_pdf_highlight_numbers_are_supported_by_their_specific_program():
    cfg = load_config()
    programs = {p["name"]: p for p in cfg["selectedEngineeringPrograms"]}
    for highlight in cfg["pdfEngineeringHighlights"]:
        source = programs[highlight["sourceProgram"]]
        evidence = set(re.findall(r"\d[\d,]*", json.dumps(source)))
        assert set(re.findall(r"\d[\d,]*", " ".join(highlight["bullets"]))) <= evidence


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_each_targeted_pdf_balances_software_delivery_and_production(variant_pdfs, variants, variant):
    cfg = load_config()
    reader = variant_pdfs[variant]["reader"]
    text = variant_pdfs[variant]["text"]
    assert 1 <= len(reader.pages) <= 2
    for term in ("ASP.NET Core", "Razor Pages", "FastAPI", "SQL Server", "SQLite"):
        assert term in text
    for stale in ("Auth0", "OAuth", "Serilog", "Blazor", "Interactive Server", "Managed Identity"):
        assert stale not in text
    assert text.index("PROFESSIONAL EXPERIENCE") < text.index("CORE EXPERTISE")
    assert cfg["site"]["projectsIntro"] in text
    links = [a.get_object().get("/A", {}).get("/URI") for p in reader.pages for a in p.get("/Annots", [])]
    assert f'mailto:{cfg["personal"]["email"]}' in links
    selected = set(variants["variants"][variant]["projectIds"])
    for project in cfg["projects"]:
        assert (project["link"] in links) == (project["id"] in selected)


def test_seo_and_cta_copy_are_canonical():
    cfg = load_config()
    page = (SITE_DIR / "index.html").read_text()
    assert html.escape(cfg["seo"]["description"], quote=True) in page
    assert "William Elias" in cfg["seo"]["description"]
    assert len(cfg["seo"]["description"]) <= 160
    assert html.escape(cfg["personal"]["contactCopy"], quote=True) in page


def test_recruiter_positioning_keeps_each_primary_role_and_differentiator_visible():
    cfg = load_config()
    assert cfg["personal"]["title"] == "Software & Automation Engineer"
    for term in ("Developer Productivity", "Internal Tools", "Security Automation", "Azure DevOps"):
        assert term in cfg["seo"]["knowsAbout"]
    assert "Production" in load_variants()["variants"]["production_devops"]["title"]
    assert "remote" in cfg["personal"]["contactCopy"].lower()


def test_verified_cicd_and_security_scope_language_remains_unambiguous():
    cfg = load_config()
    delivery = next(p for p in cfg["selectedEngineeringPrograms"] if p["id"] == "program-cicd-release")
    assert "subset" in " ".join(delivery["bullets"]).lower()
    details = " ".join(delivery["details"]).lower()
    for phase in ("inventory", "pipeline configuration", "build checks", "dry runs", "production deployments"):
        assert phase in details
    assert re.search(r"dry runs.*separately from production deployments", details)
    assert not re.search(r"\d", json.dumps(delivery))
    assert not cfg["stats"]


def test_no_phone_or_street_address_in_public_source():
    personal = load_config()["personal"]
    assert "phone" not in personal
    assert "address" not in personal
