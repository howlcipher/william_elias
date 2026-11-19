"""User-confirmed professional facts supersede prior portfolio assertions."""
import json
import re

import pytest

from conftest import VARIANT_NAMES
from scripts.generate_resume_pdf import SITE_DIR, load_config


@pytest.fixture(scope="module")
def config():
    return load_config()


@pytest.mark.parametrize("source", ["canonical", "variants", "config.js", "index.html", "README.md", "documentation/linkedin_profile.md",
                                    *(f"pdf:{name}" for name in VARIANT_NAMES)])
def test_false_and_stale_claims_absent(config, variant_pdfs, source):
    if source == "canonical":
        text = json.dumps(config)
    elif source == "variants":
        text = (SITE_DIR / "resume_variants.json").read_text()
    elif source.startswith("pdf:"):
        text = variant_pdfs[source[4:]]["text"]
    else:
        text = (SITE_DIR / source).read_text()
    text = " ".join(text.lower().split())
    for term in (
        "interactive server", "dba approve", "build-to-rollback", "100+ repositories",
        "60-repository", "104-application", "56 azure devops", "66 build/release",
        "27/28", "28/28", "25/28", "25 of 28", "2,832", "866 raw", "67 distinct", "22-query",
        "cleanup records are complete", "managed identity", "xunit", "62 automated tests",
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


def test_configuration_discovery_and_git_history_use_distinct_tools(config):
    role = config["experience"][0]
    facts = {a["id"]: a["text"] for a in role["achievements"]}
    discovery = facts["ach-secrets-discovery"]
    history = facts["ach-git-history-tooling"]
    assert {"C#/.NET", "configuration"} <= set(discovery.split())
    assert not re.search(r"python|migration|rotation|revocation", discovery, re.I)
    assert "Python" in history and "BFG Repo-Cleaner" in history and "git-filter-repo" in history
    assert not re.search(r"scrubbed|rotated|revoked|completed|migrated", history, re.I)


def test_portal_stack_permissions_and_shipping_boundaries(config):
    portal = next(p for p in config["selectedEngineeringPrograms"] if p["id"] == "program-internal-software")
    assert {"C#", ".NET 10", "ASP.NET Core Razor Pages", "Razor Class Libraries",
            "SQL Server", "SQLite"} <= set(portal["technology"])
    text = " ".join(portal["bullets"] + portal["details"])
    for term in ("authorization", "audit", "windows authentication", "active directory",
                 "production", "development", "qa", "multiple developers"):
        assert term in text.lower()
    assert not re.search(r"blazor|interactive server|dba|fastapi|sole", json.dumps(portal), re.I)


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_current_employment_and_remote_target_are_distinct(config, variant_pdfs, variant):
    pdf_text = variant_pdfs[variant]["text"]
    role = config["experience"][0]
    assert role["title"] == role["officialTitle"]
    assert role["officialTitle"] == "Senior Production Support Engineer"
    assert role["promotion"] == {
        "effectiveDate": "2026-09",
        "previousOfficialTitle": "Production Support Engineer",
    }
    assert role["location"] == "Auburn Hills, MI · Hybrid"
    assert config["personal"]["remote"] == "Open to U.S. Remote Opportunities"
    for term in (role["title"], "Promoted September 2026; previously Production Support Engineer",
                 "Auburn Hills, MI", "Hybrid"):
        assert term in pdf_text


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_identity_and_foundations_keep_experience_context(config, variant_pdfs, variant):
    pdf_text = variant_pdfs[variant]["text"]
    skills = {s["category"]: s for s in config["skills"]}
    security = skills["Security & Identity"]
    assert "Auth0" not in security["tags"]
    assert "Auth0" not in json.dumps(config)
    # The OAuth resource-server work was removed at William's request; no OAuth claim remains.
    assert "oauth" not in json.dumps(config).lower()
    assert "oauth" not in pdf_text.lower()
    assert {"Secrets Discovery", "Git History Tooling", "Authorization", "Audit Controls"} <= set(security["tags"])
    assert "Audit Controls" in (security.get("pdfTags") or security["tags"])
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
    assert "Auth0" not in pdf_text
    assert "Serilog" not in pdf_text
    assert "Serilog" not in json.dumps(config)


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_pdf_software_selection_retains_backend_strength_without_web_bloat(config, variants, variant_pdfs, variant):
    software = next(s for s in config["skills"] if s["id"] == "skill-software-backend")
    assert {"JavaScript", "HTML", "CSS"} <= set(software["tags"])
    assert "FastAPI" in software["tags"]
    assert {"Python", "C#", "ASP.NET Core", "Razor Pages", "REST APIs", "SQLite"} <= set(software["pdfTags"])
    selected = variants["variants"][variant].get("skillTags", {}).get(software["id"], software["pdfTags"])
    expertise = variant_pdfs[variant]["text"].split("CORE EXPERTISE")[1].split("SELECTED ENGINEERING")[0]
    for tag in selected:
        assert tag in expertise
    assert "SQLite" in expertise
    for term in ("Docker", "Helm", "Rancher", "WSL2"):
        assert term not in expertise
    web = ("JavaScript", "HTML", "CSS")
    for term in web:
        assert term not in expertise


def test_delivery_prototype_stays_out_of_professional_resume_claims(config, variants, variant_pdfs):
    prototype = next(p for p in config["selectedEngineeringPrograms"] if p["id"] == "program-deployment-tooling")
    assert "prototype" in prototype["name"].lower()
    assert "proof of concept" in " ".join(prototype["details"]).replace("-", " ")
    assert re.search(r"push and rollback .*unimplemented", " ".join(prototype["details"]), re.I)
    assert "verification was incomplete" in " ".join(prototype["details"])
    for variant in variants["variants"]:
        text = variant_pdfs[variant]["text"].lower()
        assert "deployment cli" not in text
        assert "blazor" not in text
    page = (SITE_DIR / "index.html").read_text()
    for card in re.findall(r'<article class="program-card.*?</article>', page, re.S):
        if "Blazor" in card:
            assert 'id="program-infrastructure-modernization"' in card
            assert "proof of concept" in card


def test_linkedin_shares_the_primary_resumes_selected_career_facts(config, variants, variant_pdfs):
    markdown = (SITE_DIR / "documentation/linkedin_profile.md").read_text()
    current = config["experience"][0]
    experience = markdown.split("## Current Experience")[1].split("## Earlier Experience")[0]
    assert f'**{current["officialTitle"]}**' in experience
    software = variants["variants"]["software_platform"]
    achievements = {item["id"]: item["text"] for item in current["achievements"]}
    assert [line[2:] for line in experience.splitlines() if line.startswith("- ")] == [
        achievements[key] for key in software["experienceAchievementIds"][current["id"]]
    ]
    pdf = variant_pdfs["software_platform"]["text"]
    for line in experience.splitlines():
        if line.startswith("- "):
            assert line[2:] in pdf
    assert config["about"] in markdown
    assert config["seo"]["canonicalUrl"] + software["file"] in markdown
    assert "coding assistants for implementation and review" in markdown


def test_security_highlight_describes_completed_discovery_work(config, variant_pdfs):
    highlight = next(h for h in config["pdfEngineeringHighlights"] if h["id"] == "highlight-discovery-boundary")
    program = next(p for p in config["selectedEngineeringPrograms"] if p["name"] == highlight["sourceProgram"])
    assert set(highlight["bullets"]) <= set(program["details"])
    text = variant_pdfs["security_automation"]["text"].lower().split("earlier experience")[0]
    assert "integrity checks" in text
    assert not re.search(r"canceled|migration|rotated|revoked", text)


def test_linkedin_prior_role_uses_canonical_experience(config, variants):
    markdown = (SITE_DIR / "documentation/linkedin_profile.md").read_text()
    earlier = markdown.split("## Earlier Experience")[1].split("## Skills")[0]
    role = next(role for role in config["experience"] if role["id"] == "exp-hbk")
    selected = variants["variants"]["software_platform"]["experienceAchievementIds"][role["id"]]
    assert role["title"] in earlier and role["date"] in earlier
    assert [line[2:] for line in earlier.splitlines() if line.startswith("- ")] == [
        a["text"] for a in role["achievements"] if a["id"] in selected
    ]
