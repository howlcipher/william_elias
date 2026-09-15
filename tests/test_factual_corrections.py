"""User-confirmed professional facts supersede prior portfolio assertions."""
import json
import re

import pypdf
import pytest

from scripts.generate_resume_pdf import SITE_DIR, build, load_config


@pytest.fixture(scope="module")
def config():
    return load_config()


@pytest.fixture(scope="module")
def pdf_text(config, tmp_path_factory):
    output = tmp_path_factory.mktemp("truth") / "resume.pdf"
    build(config, output)
    return " ".join(
        " ".join(page.extract_text().split())
        for page in pypdf.PdfReader(output).pages
    )


@pytest.mark.parametrize("source", ["canonical", "config.js", "index.html", "pdf"])
def test_false_and_stale_claims_absent(config, pdf_text, source):
    if source == "canonical":
        text = json.dumps(config)
    elif source == "pdf":
        text = pdf_text
    else:
        text = (SITE_DIR / source).read_text()
    text = " ".join(text.lower().split())
    for term in (
        "managed identity", "xunit", "62 automated tests",
        "156 automated tests", "first deployment pending",
        "pending approval", "zero applications", "go/no-go", "rollout pending",
        "formerly multi-agent engineering library",
        "evolved a shared agent knowledge library",
        "~60 applications", "60-application",
        "credential-remediated", "zero-downtime", "cutover",
        "157", "six latent", "migration to azure key vault", "ongoing key vault",
        "became the team standard", "drove adoption across the legacy application estate",
    ):
        assert term not in text, (source, term)


def test_security_is_python_git_bfg_without_invented_tests(config):
    field = "selectedEngineeringPrograms"
    security = next(p for p in config[field] if p["name"].startswith("Security"))
    assert security["name"] == "Security & Credential Remediation"
    assert {"Python", "Git", "BFG Repo-Cleaner"} <= set(security["technology"])
    text = json.dumps(security).lower()
    for term in ("100+ repositories", "67 distinct exposed secrets", "2,832", "25 seconds"):
        assert term in text
    for term in ("azure key vault", "managed identity", "azure sdk", "c#", ".net", "xunit", "62 automated tests", "test", "rollback"):
        assert term not in text


def test_portal_stack_and_capabilities_are_user_confirmed(config):
    portal = next(p for p in config["selectedEngineeringPrograms"] if p["name"].startswith("Software & Internal"))
    assert {"C#", ".NET 8", "Blazor", "Interactive Server", "ASP.NET Core", "SQL Server", "SQLite"} <= set(portal["technology"])
    assert "Razor Pages" not in portal["technology"]
    text = " ".join(portal["bullets"] + portal.get("details", []))
    for term in ("blazor", "interactive server", "dba", "diffing", "pre-change",
                 "service-desk", "database-backed", "asp.net core", "production support"):
        assert term in text.lower()
    assert "FastAPI" not in text
    assert "Razor Pages" not in text


def test_current_employment_and_remote_target_are_distinct(config, pdf_text):
    role = config["experience"][0]
    assert role["title"].split(" | ") == [
        "Production Support Engineer", "DevOps & Automation",
    ]
    assert role["location"] == "Auburn Hills, MI · Hybrid"
    assert config["personal"]["remote"] == "Open to U.S. Remote Opportunities"
    for term in (role["title"], "Auburn Hills, MI", "Hybrid", "OAuth", "OIDC"):
        assert term in pdf_text


def test_identity_and_foundations_keep_experience_context(config, pdf_text):
    skills = {s["category"]: s for s in config["skills"]}
    security = skills["Security & Identity"]
    assert {"Auth0", "OAuth / OIDC", "IAM", "Credential Remediation",
            "Git History Remediation", "PII Safeguards", "Audit Controls"} <= set(security["tags"])
    assert "Azure Key Vault" not in security["tags"]
    assert "Managed Identity" not in security["tags"]
    foundations = skills["Additional Technical Foundations"]
    assert set(foundations["tags"]) == {
        "Java", "Kotlin", "Android Development", "Digital Forensics",
        "FTK Imager", "EnCase", "Wireshark",
    }
    assert "not professional" in foundations["context"]
    assert foundations["pdfInclude"] is False
    for term in (foundations["category"], *foundations["tags"]):
        assert not re.search(r"\b" + re.escape(term) + r"\b", pdf_text)
    assert "Digital Forensics" not in security["tags"]


def test_pdf_software_selection_retains_backend_strength_without_web_bloat(config, pdf_text):
    software = config["skills"][0]
    assert {"JavaScript", "HTML", "CSS"} <= set(software["tags"])
    assert "FastAPI" in software["tags"]
    assert software["pdfTags"] == [
        "Python", "FastAPI", "C#", ".NET", "Blazor", "ASP.NET Core", "REST APIs", "SQL Server",
    ]
    expertise = pdf_text.split("CORE EXPERTISE")[1].split("SELECTED ENGINEERING")[0]
    for tag in software["pdfTags"]:
        assert tag in expertise
    for term in ("HTML", "CSS", "Docker", "Helm", "Rancher", "WSL2"):
        assert term not in expertise


def test_general_pdf_project_pair_and_security_scan_evidence(config, pdf_text):
    assert [p["name"] for p in config["projects"] if p.get("pdfInclude")] == [
        "HowlPlane", "RedrawUS",
    ]
    for term in ("HowlPlane", "RedrawUS", "67 distinct exposed secrets", "2,832", "25 seconds"):
        assert term in pdf_text
    assert "Baseball Optimizer" not in pdf_text
