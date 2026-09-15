import html
import json
import re
from html.parser import HTMLParser

from scripts.generate_resume_pdf import SITE_DIR, build, load_config
import pypdf


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


def test_proof_precedes_keyword_inventory():
    page = (SITE_DIR / "index.html").read_text()
    ids = ["hero-content-target", "stats-target", "about", "programs", "experience", "projects", "skills", "education", "contact-cta"]
    positions = [page.index(f'id="{section}"') for section in ids]
    assert positions == sorted(positions)
    assert '>Engineering Impact</h2>' in page


def test_about_is_three_short_paragraphs_without_repeated_delivery_counts():
    cfg = load_config()
    assert len(cfg["about"].split("\n\n")) == 3
    assert len(cfg["about"].split()) <= 170
    first_impression = cfg["about"] + cfg["summary"] + cfg["personal"]["supporting"]
    for count in ("56", "27/28", "25/28", "60", "104", "866", "67"):
        assert count not in first_impression


def test_headline_metrics_have_independent_program_evidence():
    cfg = load_config()
    assert [s["value"] for s in cfg["stats"]] == ["60", "104", "67"]
    programs = {p["name"]: p for p in cfg["selectedEngineeringPrograms"]}
    sources = []
    for stat in cfg["stats"]:
        source = programs[stat["sourceProgram"]]
        assert stat["value"] in " ".join(source["bullets"] + source.get("details", []))
        sources.append(stat["sourceProgram"])
    assert len(set(sources)) >= 2
    assert "scope" in cfg["stats"][0]["label"]
    assert "inventoried" in cfg["stats"][1]["label"]
    assert "secret" in cfg["stats"][2]["label"].lower()


def test_pdf_highlight_numbers_are_supported_by_their_specific_program():
    cfg = load_config()
    programs = {p["name"]: p for p in cfg["selectedEngineeringPrograms"]}
    for highlight in cfg["pdfEngineeringHighlights"]:
        source = programs[highlight["sourceProgram"]]
        evidence = set(re.findall(r"\d[\d,]*", json.dumps(source)))
        assert set(re.findall(r"\d[\d,]*", " ".join(highlight["bullets"]))) <= evidence


def test_general_pdf_balances_software_delivery_and_production(tmp_path):
    cfg = load_config()
    output = tmp_path / "resume.pdf"
    build(cfg, output)
    reader = pypdf.PdfReader(output)
    text = " ".join(" ".join(p.extract_text().split()) for p in reader.pages)
    assert len(reader.pages) == 2
    assert text.count("56 Azure DevOps") >= 1
    for term in ("60", "104", "28", "27", "25 of 28", "dry-run", "ASP.NET Core", "Blazor", "Interactive Server", "FastAPI", "SQL Server", "KQL", "BFG Repo-Cleaner", "Go", "deployment CLI", "Git History", "Auth0", "HowlPlane", "RedrawUS"):
        assert term in text, term
    for stale in ("Razor Pages", "Azure Key Vault", "Managed Identity", "six latent"):
        assert stale not in text, f"stale term found: {stale}"
    assert "AI Router" not in text
    assert text.index("PROFESSIONAL EXPERIENCE") < text.index("CORE EXPERTISE")
    links = [str(a.get_object().get("/A", {}).get("/URI", "")) for p in reader.pages for a in p.get("/Annots", [])]
    assert f'mailto:{cfg["personal"]["email"]}' in links
    for project in cfg["projects"]:
        assert (project["link"] in links) == bool(project.get("pdfInclude"))


def test_seo_and_cta_copy_are_canonical():
    cfg = load_config()
    page = (SITE_DIR / "index.html").read_text()
    assert html.escape(cfg["seo"]["description"], quote=True) in page
    assert "William Elias" in cfg["seo"]["description"]
    assert len(cfg["seo"]["description"]) <= 160
    assert html.escape(cfg["personal"]["contactCopy"], quote=True) in page
    assert "Platform Engineering" in cfg["seo"]["knowsAbout"]


def test_recruiter_positioning_keeps_each_primary_role_and_differentiator_visible():
    cfg = load_config()
    title = cfg["personal"]["title"]
    assert title == "DevOps, Software & Production Engineer"
    for term in ("DevOps", "Software", "Production"):
        assert term in title
    assert cfg["personal"]["supporting"] == (
        "Python • C#/.NET • Go • Azure DevOps • CI/CD • REST APIs"
    )

    canonical = json.dumps(cfg)
    for term in ("Python", "Security Automation", "AI-Enabled Engineering"):
        assert term in canonical
    assert "U.S. fully remote" in cfg["personal"]["contactCopy"]


def test_engineering_impact_is_the_requested_eight_card_order():
    cfg = load_config()
    assert [program["name"] for program in cfg["selectedEngineeringPrograms"]] == [
        "CI/CD & Release Engineering",
        "Software & Internal Developer Tools",
        "Python Automation & Developer Productivity",
        "Deployment Automation & Release Tooling",
        "Security & Credential Remediation",
        "APIs, OAuth & Secure Integration",
        "Production Reliability & Observability",
        "Infrastructure Modernization & Containerization",
    ]


def test_verified_cicd_and_security_scope_language_remains_unambiguous():
    cfg = load_config()
    cicd = next(p for p in cfg["selectedEngineeringPrograms"] if p["name"] == "CI/CD & Release Engineering")
    cicd_text = " ".join(cicd["bullets"] + cicd["details"])
    for term in (
        "60-repository, 104-application",
        "56 Azure DevOps build/release pipeline definitions across 28 standardized application repositories",
        "representative deployment paths for 25 of 28 standardized repositories",
    ):
        assert term in cicd_text
    security = next(p for p in cfg["selectedEngineeringPrograms"] if p["name"].startswith("Security"))
    assert "67 distinct exposed secrets" in json.dumps(security)


def test_no_phone_or_street_address_in_public_source():
    personal = load_config()["personal"]
    assert "phone" not in personal
    assert "address" not in personal
