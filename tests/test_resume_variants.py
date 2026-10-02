"""Targeted résumé variants are ID-driven views of one canonical evidence base."""
import copy
import json
import re
import shutil
import subprocess

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
    "production_devops": "William_Elias_Production_DevOps_Resume.pdf",
}


@pytest.fixture
def config():
    return load_config()


@pytest.fixture
def variant_doc():
    return load_variants()


def _numbers(text):
    return set(re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", text))


# --- Variant contract -------------------------------------------------------

def test_two_targeted_variants_and_one_compatibility_alias(variant_doc):
    assert {n: v["file"] for n, v in variant_doc["variants"].items()} == EXPECTED_FILES
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
    variant_doc["variants"]["software_platform"]["experienceAchievementIds"]["exp-hbk"].append("ach-go-deployment-cli")
    with pytest.raises(ValueError, match="another role"):
        validate_variants(config, variant_doc)


def test_unknown_role_or_achievement_fails(config, variant_doc):
    broken = copy.deepcopy(variant_doc)
    broken["variants"]["software_platform"]["experienceAchievementIds"]["exp-nowhere"] = ["ach-go-deployment-cli"]
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
    variant_doc["variants"]["software_platform"]["skillTags"]["skill-software-backend"] = tags
    with pytest.raises(ValueError, match="skillTags"):
        validate_variants(config, variant_doc)


def test_skill_tag_override_requires_the_skill_to_be_selected(config, variant_doc):
    variant_doc["variants"]["production_devops"]["skillTags"]["skill-ai-engineering"] = ["MCP"]
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
                                "experienceAchievementIds", "skillIds", "skillTags", "highlightIds", "projectIds"}
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
    statement["text"] = statement["text"].replace("10+ years", "25+ years")
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


def test_verified_metrics_remain_canonical(config):
    blob = json.dumps(config, ensure_ascii=False)
    for claim in (
        "60-repository, 104-application", "56 Azure DevOps build/release", "28 standardized application repositories",
        "27 passed", "25 of 28", "109 existing definitions", "95 legacy", "14 already-aligned",
        "100+ repositories", "2,832 files", "67 distinct exposed secrets", "approximately 25 seconds",
        "22-query KQL library",
    ):
        assert claim in blob, claim


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_every_number_in_a_pdf_comes_from_canonical_data(variant_pdfs, variant):
    canonical = _numbers((SITE_DIR / "resume.json").read_text(encoding="utf-8"))
    canonical |= _numbers(json.dumps(load_config(), ensure_ascii=False))
    assert _numbers(variant_pdfs[variant]["text"]) <= canonical


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_qualifiers_survive_into_each_pdf(variant_pdfs, variant):
    text = variant_pdfs[variant]["text"]
    for qualifier in ("dry-run validated representative deployment paths", "remaining checks blocked",
                      "In Progress", "Previously Held", "Python/PowerShell professionally",
                      "Production Support Engineer | DevOps & Automation"):
        assert qualifier in text, qualifier
    if variant == "production_devops":
        assert "proof of concept" in text
        assert "Investigated server/container migration paths" in text


# --- Variant emphasis -------------------------------------------------------

def test_software_platform_leads_with_software_and_tooling(variant_pdfs, variant_doc):
    text = variant_pdfs["software_platform"]["text"]
    assert "SOFTWARE & AUTOMATION ENGINEER" in text
    assert "Developer Tooling | Platform Engineering | Python | Go | C#/.NET | CI/CD" in text
    experience = text.split("PROFESSIONAL EXPERIENCE")[1]
    assert experience.index("Go-based self-service deployment CLI") < experience.index("CI/CD standardization program")
    assert experience.index("Python/FastAPI") < experience.index("CI/CD standardization program")
    for term in ("initialization/scaffolding", "host auditing", "post-deployment verification", "HowlFrame",
                 "bytecode VM", "WebAssembly", "Blazor", "ASP.NET Core", "SQLite", "uv", "FastAPI"):
        assert term in text, term
    expertise = text.split("CORE EXPERTISE")[1]
    assert expertise.lstrip().startswith("Software & Backend")
    assert "Infrastructure & Application Operations" not in text


def test_production_devops_leads_with_delivery_and_reliability(variant_pdfs):
    text = variant_pdfs["production_devops"]["text"]
    assert "PRODUCTION & DEVOPS AUTOMATION ENGINEER" in text
    assert "CI/CD | Azure DevOps | Automation | Reliability | Python | Production Systems" in text
    experience = text.split("PROFESSIONAL EXPERIENCE")[1]
    assert experience.lstrip().startswith("Stellantis")
    assert experience.index("CI/CD standardization program") < experience.index("Go-based self-service deployment CLI")
    assert experience.index("22-query KQL library") < experience.index("Python/FastAPI")
    for term in ("109 existing definitions", "95 legacy", "14 already-aligned", "Azure Monitor",
                 "Application Insights", "Incident Triage", "RCA", "Cisco / Meraki", "Load Balancers",
                 "Firewalls", "IIS", "Active Directory", "disaster-recovery", "Go-based self-service deployment CLI"):
        assert term in text, term
    assert text.split("CORE EXPERTISE")[1].lstrip().startswith("DevOps & Delivery")
    assert "AI-Enabled Engineering" not in text


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_targeted_pdf_does_not_inflate_scope(variant_pdfs, variant):
    text = variant_pdfs[variant]["text"].lower()
    for term in ("kubernetes", "terraform", "aws", "gcp", "azure cloud", "cloud platform owner",
                 "internal developer platform", "led a team", "zero-downtime", "cutover",
                 "completed migration", "platform engineer at", "senior "):
        assert term not in text, term


# --- Generated files and compatibility alias --------------------------------

@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    directory = tmp_path_factory.mktemp("site")
    for name in ("resume.json", "resume_variants.json"):
        shutil.copy2(SITE_DIR / name, directory)
    return directory, generate_all(directory)


def test_generation_writes_all_three_filenames(generated):
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
    "software_platform": ("Software", "Automation", "Developer Tooling", "Platform Engineering", "Python", "Go",
                          "C#", ".NET", "ASP.NET Core", "REST API", "CI/CD", "Azure DevOps", "FastAPI",
                          "self-service", "Security", "OAuth"),
    "production_devops": ("DevOps", "Azure DevOps", "CI/CD", "Release", "Production", "Reliability", "KQL",
                          "Application Insights", "Azure Monitor", "Python", "PowerShell", "IIS",
                          "Windows Server", "SQL Server", "Credential Remediation", "RCA"),
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

def test_website_offers_only_the_two_targeted_resumes():
    page = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    pdf_links = re.findall(r'href="([^"]+\.pdf)"', page)
    assert set(pdf_links) == set(EXPECTED_FILES.values())
    assert f'href="{LEGACY_PDF}"' not in page
    for scope in ('class="resume-actions"', 'id="resume-downloads"'):
        block = page.split(scope)[1].split("</div>")[0]
        assert [f for f in EXPECTED_FILES.values() if f in block] == list(EXPECTED_FILES.values())
    assert 'data-resume-variant="software_platform"' in page
    assert "Resume PDF" not in page


def test_legacy_pdf_remains_published_at_its_url():
    assert (SITE_DIR / LEGACY_PDF).is_file()
