"""Targeted résumé variants are ID-driven views of one canonical evidence base."""
import copy
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

import pypdf
import pytest

from conftest import VARIANT_NAMES
from scripts.generate_resume_pdf import (
    SITE_DIR, VARIANT_TEXT_KEYS, build, canonical_index, generate_all, load_config,
    load_variants, resolve_variant, validate_config, validate_variants,
)

LEGACY_PDF = "William_Elias_Resume.pdf"
EXPECTED_FILES = {
    "software_platform": "William_Elias_Software_Platform_Resume.pdf",
    "security_automation": "William_Elias_Security_Automation_Resume.pdf",
    "production_devops": "William_Elias_Production_DevOps_Resume.pdf",
}
PRIMARY = ("software_platform",)


@pytest.fixture
def config():
    return load_config()


@pytest.fixture
def variant_doc():
    return load_variants()


def _numbers(text):
    return set(re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", text))


# --- Variant contract -------------------------------------------------------

def test_three_targeted_variants_and_one_compatibility_alias(variant_doc):
    assert {n: v["file"] for n, v in variant_doc["variants"].items()} == EXPECTED_FILES
    assert list(variant_doc["variants"]) == list(EXPECTED_FILES)
    listed = {n: v.get("listing", "primary") for n, v in variant_doc["variants"].items()}
    assert tuple(n for n, value in listed.items() if value == "primary") == PRIMARY
    assert listed["production_devops"] == "secondary"
    assert variant_doc["compatibility"] == {"file": LEGACY_PDF, "variant": "production_devops"}
    assert LEGACY_PDF not in {v["file"] for v in variant_doc["variants"].values()}


def test_shipped_variants_validate(config, variant_doc):
    validate_config(config)
    validate_variants(config, variant_doc)


@pytest.mark.parametrize("field,kind", [
    ("summaryStatementIds", "positioningStatements"), ("skillIds", "skills"),
    ("highlightIds", "pdfEngineeringHighlights"), ("projectIds", "projects"),
])
def test_variant_references_exist_with_the_right_kind(config, variant_doc, field, kind):
    index = canonical_index(config)
    for variant in variant_doc["variants"].values():
        for item_id in variant[field]:
            assert index[item_id][0] == kind


@pytest.mark.parametrize("field", ["summaryStatementIds", "skillIds", "highlightIds", "projectIds"])
def test_unknown_id_fails_generation(config, variant_doc, field, tmp_path):
    variant_doc["variants"]["software_platform"][field].append("project-does-not-exist")
    with pytest.raises(ValueError, match="unknown"):
        build(config, tmp_path / "x.pdf", "software_platform", variant_doc)


@pytest.mark.parametrize("field,wrong_kind_id", [
    ("projectIds", "skill-software-backend"), ("skillIds", "project-howlplane"),
    ("highlightIds", "program-cicd-release"), ("summaryStatementIds", "highlight-deployment-tooling"),
])
def test_id_of_the_wrong_kind_fails(config, variant_doc, field, wrong_kind_id):
    variant_doc["variants"]["production_devops"][field].append(wrong_kind_id)
    with pytest.raises(ValueError, match="unknown"):
        validate_variants(config, variant_doc)


def test_repeated_id_fails(config, variant_doc):
    ids = variant_doc["variants"]["production_devops"]["projectIds"]
    ids.append(ids[0])
    with pytest.raises(ValueError, match="must not repeat"):
        validate_variants(config, variant_doc)


def test_achievements_must_belong_to_the_selected_role(config, variant_doc):
    variant_doc["variants"]["software_platform"]["experienceAchievementIds"]["exp-hbk"].append("ach-internal-dotnet-app")
    with pytest.raises(ValueError, match="another role"):
        validate_variants(config, variant_doc)


def test_unknown_role_or_achievement_fails(config, variant_doc):
    broken = copy.deepcopy(variant_doc)
    broken["variants"]["software_platform"]["experienceAchievementIds"]["exp-nowhere"] = ["ach-internal-dotnet-app"]
    with pytest.raises(ValueError, match="unknown experience ID"):
        validate_variants(config, broken)
    variant_doc["variants"]["software_platform"]["experienceAchievementIds"]["exp-stellantis"].append("ach-invented-claim")
    with pytest.raises(ValueError, match="unknown achievement ID"):
        validate_variants(config, variant_doc)


def test_website_only_skill_cannot_be_selected(config, variant_doc):
    variant_doc["variants"]["software_platform"]["skillIds"].append("skill-technical-foundations")
    with pytest.raises(ValueError, match="website-only"):
        validate_variants(config, variant_doc)


@pytest.mark.parametrize("tags", [["Kubernetes"], [], ["Python", "Python"], "Python"])
def test_skill_tag_override_must_be_a_canonical_subset(config, variant_doc, tags):
    variant_doc["variants"]["software_platform"].setdefault("skillTags", {})["skill-software-backend"] = tags
    with pytest.raises(ValueError, match="skillTags"):
        validate_variants(config, variant_doc)


def test_skill_tag_override_requires_the_skill_to_be_selected(config, variant_doc):
    variant_doc["variants"]["production_devops"].setdefault("skillTags", {})["skill-ai-engineering"] = ["Human Review"]
    with pytest.raises(ValueError, match="unselected skill"):
        validate_variants(config, variant_doc)


@pytest.mark.parametrize("key,value", [
    ("title", "Software Engineer with 15 years"),
    ("supporting", "Python • 104 applications"),
    ("audience", "Teams of 50+"),
])
def test_variant_cannot_introduce_numeric_claims(config, variant_doc, key, value):
    variant_doc["variants"]["software_platform"][key] = value
    with pytest.raises(ValueError, match="must not contain numbers"):
        validate_variants(config, variant_doc)


@pytest.mark.parametrize("key", ["summary", "achievements", "experience", "projects", "metrics", "bullets"])
def test_variant_cannot_carry_its_own_professional_records(config, variant_doc, key):
    variant_doc["variants"]["production_devops"][key] = ["Led a platform team."]
    with pytest.raises(ValueError, match="unsupported keys"):
        validate_variants(config, variant_doc)


@pytest.mark.parametrize("value", ["featured", "", True, None])
def test_variant_listing_must_be_primary_or_secondary(config, variant_doc, value):
    variant_doc["variants"]["security_automation"]["listing"] = value
    with pytest.raises(ValueError, match="listing"):
        validate_variants(config, variant_doc)


def test_at_least_one_variant_must_be_primary(config, variant_doc):
    for variant in variant_doc["variants"].values():
        variant["listing"] = "secondary"
    with pytest.raises(ValueError, match="at least one variant must be listed as primary"):
        validate_variants(config, variant_doc)


def test_variant_presentation_text_cannot_become_prose(config, variant_doc):
    variant_doc["variants"]["production_devops"]["supporting"] = "Built and owned the entire Azure cloud platform. " * 3
    with pytest.raises(ValueError, match="short presentation text"):
        validate_variants(config, variant_doc)


def test_variants_do_not_duplicate_canonical_prose(config, variant_doc):
    canonical_text = []
    for job in config["experience"]:
        canonical_text += [a["text"] for a in job["achievements"]]
    canonical_text += [s["text"] for s in config["positioningStatements"]]
    canonical_text += [b for h in config["pdfEngineeringHighlights"] for b in h["bullets"]]
    canonical_text += [h for p in config["projects"] for h in p["highlights"]]
    for variant in variant_doc["variants"].values():
        assert set(variant) <= {"label", "audience", "file", "title", "supporting", "summaryStatementIds",
                                "experienceAchievementIds", "skillIds", "skillTags", "highlightIds", "projectIds",
                                "listing"}
        for key in VARIANT_TEXT_KEYS:
            assert all(variant[key] not in text for text in canonical_text if len(variant[key]) > 40)
            assert len(variant[key]) <= 90


def test_selection_follows_ids_not_array_positions(config, variant_doc):
    before = resolve_variant(config, variant_doc, "software_platform")
    shuffled = copy.deepcopy(config)
    for key in ("skills", "projects", "pdfEngineeringHighlights", "positioningStatements"):
        shuffled[key].reverse()
    shuffled["experience"][0]["achievements"].reverse()
    after = resolve_variant(shuffled, variant_doc, "software_platform")
    for key in ("summary", "skills", "projects", "highlights"):
        assert before[key] == after[key]
    assert before["experience"][0]["achievements"] == after["experience"][0]["achievements"]


def test_unknown_variant_name_fails(config, variant_doc, tmp_path):
    with pytest.raises(ValueError, match="unknown résumé variant"):
        build(config, tmp_path / "x.pdf", "platform_cloud", variant_doc)


@pytest.mark.parametrize("compatibility", [
    {"file": LEGACY_PDF, "variant": "cloud"},
    {"file": "William_Elias_Production_DevOps_Resume.pdf", "variant": "production_devops"},
    {"file": LEGACY_PDF, "variant": "production_devops", "summaryStatementIds": []},
])
def test_compatibility_alias_must_point_at_a_defined_variant(config, variant_doc, compatibility):
    variant_doc["compatibility"] = compatibility
    with pytest.raises(ValueError, match="compatibility"):
        validate_variants(config, variant_doc)


# --- Canonical evidence integrity ------------------------------------------

def test_every_positioning_statement_traces_to_existing_evidence(config):
    index = canonical_index(config)
    for statement in config["positioningStatements"]:
        assert statement["evidenceIds"]
        for evidence_id in statement["evidenceIds"]:
            assert evidence_id in index and index[evidence_id][0] != "positioningStatements"


def test_statement_with_untraceable_number_fails(config):
    config["positioningStatements"][1]["text"] += " Supported 300 engineers."
    with pytest.raises(ValueError, match="not traceable"):
        validate_config(config)


def test_statement_years_claim_must_match_dated_evidence(config):
    statement = next(s for s in config["positioningStatements"] if s["id"] == "summary-software-opening")
    statement["text"] += " Claims 25+ years."
    with pytest.raises(ValueError, match="not traceable"):
        validate_config(config)


def test_statement_with_unknown_evidence_fails(config):
    config["positioningStatements"][0]["evidenceIds"].append("program-kubernetes-platform")
    with pytest.raises(ValueError, match="unknown evidence ID"):
        validate_config(config)


def test_highlight_number_must_come_from_its_source_program(config):
    config["pdfEngineeringHighlights"][0]["bullets"][0] += " Served 250 teams."
    with pytest.raises(ValueError, match="not in its source program"):
        validate_config(config)


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_every_number_in_a_pdf_comes_from_canonical_data(variant_pdfs, variant):
    canonical = _numbers((SITE_DIR / "resume.json").read_text(encoding="utf-8"))
    canonical |= _numbers(json.dumps(load_config(), ensure_ascii=False))
    assert _numbers(variant_pdfs[variant]["text"]) <= canonical


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_qualifiers_survive_into_each_pdf(variant_pdfs, variant):
    text = variant_pdfs[variant]["text"]
    for qualifier in ("In Progress", "Previously Held",
                      "Go in independent projects and prototyping",
                      "Senior Production Support Engineer",
                      "Promoted September 2026; previously Production Support Engineer",
                      "limited to development or QA"):
        assert qualifier in text


# --- Variant emphasis -------------------------------------------------------

def test_software_platform_leads_with_software_and_tooling(variant_pdfs, variant_doc):
    text = variant_pdfs["software_platform"]["text"]
    assert "SOFTWARE & AUTOMATION ENGINEER" in text
    experience = text.split("PROFESSIONAL EXPERIENCE")[1].split("CORE EXPERTISE")[0]
    terms = ("ASP.NET Core Razor Pages", "Azure DevOps templates", "integer-overflow", "FastAPI webhook")
    assert all(term in experience for term in terms)
    assert [experience.index(term) for term in terms] == sorted(experience.index(term) for term in terms)
    assert text.split("CORE EXPERTISE")[1].lstrip().startswith("Software & Backend")
    assert "Infrastructure & Application Operations" not in text


def test_security_automation_leads_with_security_tooling(variant_pdfs):
    text = variant_pdfs["security_automation"]["text"]
    assert "SOFTWARE & SECURITY AUTOMATION ENGINEER" in text
    experience = text.split("PROFESSIONAL EXPERIENCE")[1].split("CORE EXPERTISE")[0]
    assert experience.index("C#/.NET 8") < experience.index("BFG Repo-Cleaner") < experience.index("authorization and audit")
    assert text.split("CORE EXPERTISE")[1].lstrip().startswith("Security & Identity")
    assert "Password Arena" in text and "synthetic" in text
    for term in ("penetration test", "pentest", "red team", "soc analyst", "threat hunting",
                 "security architect", "incident responder", "key vault", "rotated", "oauth", "iam"):
        assert not re.search(r"\b" + re.escape(term) + r"\b", text.lower())


def test_production_devops_leads_with_delivery_and_reliability(variant_pdfs):
    text = variant_pdfs["production_devops"]["text"]
    assert "PRODUCTION & DEVOPS AUTOMATION ENGINEER" in text
    experience = text.split("PROFESSIONAL EXPERIENCE")[1].split("CORE EXPERTISE")[0]
    assert experience.lstrip().startswith("Stellantis")
    assert experience.index("integer-overflow") < experience.index("Azure DevOps templates") < experience.index("KQL")
    for term in ("Azure Monitor", "Application Insights", "Incident Triage", "RCA",
                 "Cisco / Meraki", "Load Balancers", "Firewalls", "IIS", "Active Directory", "disaster-recovery"):
        assert term in text
    assert text.split("CORE EXPERTISE")[1].lstrip().startswith("DevOps & Delivery")
    assert "AI-Assisted Engineering" not in text


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_targeted_pdf_does_not_inflate_scope(variant_pdfs, variant):
    text = variant_pdfs[variant]["text"].lower()
    for term in ("kubernetes", "terraform", "aws", "gcp", "azure cloud", "cloud platform owner",
                 "internal developer platform", "led a team", "zero-downtime", "cutover",
                 "completed migration", "platform engineer at", "senior software engineer",
                 "senior platform engineer", "senior devops"):
        assert term not in text, term
    assert "senior production support engineer" in text
    assert text.count("senior ") == 1


# --- Generated files and compatibility alias --------------------------------

@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    directory = tmp_path_factory.mktemp("site")
    for name in ("resume.json", "resume_variants.json"):
        shutil.copy2(SITE_DIR / name, directory)
    return directory, generate_all(directory)


def test_generation_writes_every_variant_and_the_alias(generated):
    directory, written = generated
    assert sorted(p.name for p in written) == sorted([*EXPECTED_FILES.values(), LEGACY_PDF])
    for path in written:
        assert path.read_bytes().startswith(b"%PDF-")


@pytest.mark.parametrize("filename", [*EXPECTED_FILES.values(), LEGACY_PDF])
def test_every_generated_pdf_is_exactly_two_pages(generated, filename):
    directory, _ = generated
    assert len(pypdf.PdfReader(directory / filename).pages) == 2


@pytest.mark.parametrize("filename", [*EXPECTED_FILES.values(), LEGACY_PDF])
def test_checked_in_pdf_is_exactly_two_pages(filename):
    assert len(pypdf.PdfReader(SITE_DIR / filename).pages) == 2


def test_legacy_pdf_is_a_byte_copy_of_the_production_devops_variant(generated):
    directory, _ = generated
    alias = (directory / LEGACY_PDF).read_bytes()
    assert alias == (directory / EXPECTED_FILES["production_devops"]).read_bytes()
    assert alias != (directory / EXPECTED_FILES["software_platform"]).read_bytes()
    assert alias != (directory / EXPECTED_FILES["security_automation"]).read_bytes()
    # The checked-in alias cannot drift from its source either.
    assert (SITE_DIR / LEGACY_PDF).read_bytes() == (SITE_DIR / EXPECTED_FILES["production_devops"]).read_bytes()


def test_legacy_alias_follows_the_configured_variant(tmp_path):
    for name in ("resume.json",):
        shutil.copy2(SITE_DIR / name, tmp_path)
    doc = load_variants()
    doc["compatibility"]["variant"] = "software_platform"
    (tmp_path / "resume_variants.json").write_text(json.dumps(doc), encoding="utf-8")
    generate_all(tmp_path)
    assert (tmp_path / LEGACY_PDF).read_bytes() == (tmp_path / EXPECTED_FILES["software_platform"]).read_bytes()


def test_default_build_renders_the_compatibility_variant(config, tmp_path):
    build(config, tmp_path / "default.pdf")
    assert (tmp_path / "default.pdf").read_bytes() == (SITE_DIR / LEGACY_PDF).read_bytes()


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_pdf_metadata_is_fixed_for_reproducible_bytes(variant_pdfs, variant, tmp_path):
    metadata = variant_pdfs[variant]["reader"].metadata
    assert metadata["/CreationDate"] == "D:20240101000000Z"
    assert metadata["/Title"] == f"William Elias - {load_variants()['variants'][variant]['label']}"
    # fpdf2 derives the trailer /ID from the document content, so with the fixed
    # creation date and uncompressed streams an independent rebuild is identical.
    rebuilt = tmp_path / "rebuilt.pdf"
    build(load_config(), rebuilt, variant)
    assert rebuilt.read_bytes() == variant_pdfs[variant]["path"].read_bytes()
    assert rebuilt.read_bytes() == (SITE_DIR / EXPECTED_FILES[variant]).read_bytes()


# --- ATS / text extraction --------------------------------------------------

SECTIONS = ("PROFESSIONAL SUMMARY", "PROFESSIONAL EXPERIENCE", "CORE EXPERTISE",
            "SELECTED ENGINEERING HIGHLIGHTS", "SELECTED OPEN-SOURCE ENGINEERING",
            "EARLIER EXPERIENCE", "EDUCATION & CERTIFICATIONS")
ATS_KEYWORDS = {
    "software_platform": ("Software", "Automation", "Developer Productivity", "Internal Tools", "Python", "Go",
                          "C#", ".NET", "ASP.NET Core", "Razor Pages", "REST APIs", "CI/CD", "Azure DevOps",
                          "FastAPI", "HowlPlane", "HowlProof"),
    "security_automation": ("Security Automation", "Secrets Discovery", "Git History Tooling",
                            "BFG Repo-Cleaner", "Authorization", "Audit Controls", "Cyber Defense",
                            "Python", "C#", "HowlProof", "Password Arena"),
    "production_devops": ("DevOps", "Azure DevOps", "CI/CD", "Release", "Production", "Reliability", "KQL",
                          "Application Insights", "Azure Monitor", "Python", "PowerShell", "IIS",
                          "Windows Server", "SQL Server", "RCA"),
}


@pytest.fixture(scope="module")
def pdftotext():
    executable = shutil.which("pdftotext")
    if executable is None:
        pytest.skip("pdftotext (poppler-utils) is not installed")
    return executable


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_ats_text_extraction(pdftotext, variant):
    config = load_config()
    path = SITE_DIR / EXPECTED_FILES[variant]
    raw = subprocess.run([pdftotext, "-enc", "UTF-8", str(path), "-"], check=True,
                         capture_output=True, text=True).stdout
    text = " ".join(raw.split())
    assert "�" not in raw and "(cid:" not in raw
    # Sections extract in reading order, so no column interleaving.
    positions = [text.index(section) for section in SECTIONS]
    assert positions == sorted(positions)
    assert text.startswith("WILLIAM ELIAS")
    personal = config["personal"]
    for contact in (personal["email"], "linkedin.com/in/wylelias", "github.com/howlcipher",
                    "howlcipher.github.io/william_elias", "Open to U.S. Remote Opportunities"):
        assert contact in text, contact
    # Experience prose is readable verbatim; every selected bullet survives.
    view = resolve_variant(config, load_variants(), variant)
    for job in view["experience"]:
        assert job["company"] in text and job["date"] in text
        for achievement in job["achievements"]:
            assert " ".join(achievement["text"].split()) in text, achievement["id"]
    assert "Brüel & Kjær" in text
    for keyword in ATS_KEYWORDS[variant]:
        assert keyword in text, keyword


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_ats_keywords_are_text_not_graphics(variant_pdfs, variant):
    reader = variant_pdfs[variant]["reader"]
    for page in reader.pages:
        assert not page.images
    for keyword in ATS_KEYWORDS[variant]:
        assert keyword in variant_pdfs[variant]["text"]


# --- Website ---------------------------------------------------------------

def test_website_offers_one_primary_resume_and_both_specialist_versions():
    page = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    pdf_links = re.findall(r'href="([^"]+\.pdf)"', page)
    assert set(pdf_links) == set(EXPECTED_FILES.values())
    assert f'href="{LEGACY_PDF}"' not in page
    primary_files = [EXPECTED_FILES[name] for name in PRIMARY]
    hero = page.split('class="resume-actions"')[1].split("</div>")[0]
    assert [f for f in EXPECTED_FILES.values() if f in hero] == primary_files
    choice = page.split('id="resume-downloads"')[1].split("</section>")[0]
    assert [f for f in EXPECTED_FILES.values() if f in choice] == list(EXPECTED_FILES.values())
    secondary = choice.split('resume-secondary-actions')[1]
    assert all(EXPECTED_FILES[name] in secondary for name in ("security_automation", "production_devops"))
    assert not any(f in secondary for f in primary_files)
    mobile = page.split('<ul class="mobile-nav-links">')[1].split("</ul>")[0]
    assert [f for f in EXPECTED_FILES.values() if f in mobile] == primary_files
    assert 'data-resume-variant="software_platform"' in page
    assert "Resume PDF" not in page


def test_legacy_pdf_remains_published_at_its_url():
    assert (SITE_DIR / LEGACY_PDF).is_file()


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_pdf_text_stays_inside_the_page(pdftotext, variant):
    path = SITE_DIR / EXPECTED_FILES[variant]
    raw = subprocess.run([pdftotext, "-bbox", str(path), "-"], check=True,
                         capture_output=True).stdout
    document = ET.fromstring(raw)
    pages = document.findall(".//{*}page")
    assert 1 <= len(pages) <= 2
    for page in pages:
        width = float(page.attrib["width"])
        height = float(page.attrib["height"])
        words = page.findall("{*}word")
        assert words
        for word in words:
            left, top, right, bottom = (float(word.attrib[key]) for key in ("xMin", "yMin", "xMax", "yMax"))
            assert 12 <= left < right <= width - 12, word.text
            assert 12 <= top < bottom <= height - 12, word.text


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_engineering_highlights_do_not_repeat_experience_bullets(config, variant_doc, variant):
    view = resolve_variant(config, variant_doc, variant)
    experience = {
        " ".join(achievement["text"].lower().split())
        for role in view["experience"]
        for achievement in role["achievements"]
    }
    highlights = {
        " ".join(bullet.lower().split())
        for highlight in view["highlights"]
        for bullet in highlight["bullets"]
    }
    assert not experience & highlights
