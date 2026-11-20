"""Regression tests protecting factual integrity across generated artifacts and documentation."""

import json
from pathlib import Path
import re
import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def canonical():
    return json.loads((ROOT / "resume.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def candidate_json():
    return json.loads((ROOT / "candidate-profile.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def llms_txt():
    return (ROOT / "llms.txt").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def index_html():
    return (ROOT / "index.html").read_text(encoding="utf-8")


def test_geographic_location_is_strictly_canonical(canonical, candidate_json, llms_txt, index_html):
    assert canonical["personal"]["location"] == "Michigan"
    assert candidate_json["candidate"]["location"] == "Michigan"
    assert "- Location: Michigan" in llms_txt

    prohibited_geo = ("dallas", "fort worth", "dfw")
    for text_source, name in [
        (index_html, "index.html"),
        (json.dumps(candidate_json), "candidate-profile.json"),
        (llms_txt, "llms.txt"),
        ((ROOT / "documentation/github_profile_recommendations.md").read_text(), "github_profile_recommendations.md"),
        ((ROOT / "documentation/identity_network_audit.md").read_text(), "identity_network_audit.md"),
        ((ROOT / "documentation/search_visibility_report.md").read_text(), "search_visibility_report.md"),
    ]:
        lower_text = text_source.lower()
        for geo in prohibited_geo:
            assert geo not in lower_text, f"Found conflicting location '{geo}' in {name}"


def test_degree_names_match_canonical_records(canonical, candidate_json, llms_txt):
    degrees = [edu["degree"] for edu in canonical["education"]]
    assert "M.S. Cyber Defense (In Progress, Second Year)" in degrees
    assert "B.S. Information Technology" in degrees
    assert "B.B.A. Business Administration" in degrees

    assert "M.S. Cyber Defense" in llms_txt
    assert "B.B.A. Business Administration" in llms_txt
    assert "Computer Science" not in llms_txt
    assert "B.B.A. in Management" not in llms_txt

    checklist_text = (ROOT / "documentation/linkedin_owner_checklist.md").read_text(encoding="utf-8")
    assert "- **Colorado State University Global Campus:** B.S. Information Technology" in checklist_text
    assert "Management Information Systems" not in checklist_text

    candidate_degrees = [e["degree"] for e in candidate_json["candidate"]["education"]]
    assert "M.S. Cyber Defense (In Progress, Second Year)" in candidate_degrees
    assert "B.S. Information Technology" in candidate_degrees
    assert "B.B.A. Business Administration" in candidate_degrees
    assert not any("Computer Science" in d for d in candidate_degrees)
    assert not any("in Management" in d for d in candidate_degrees)


def test_unsupported_security_and_rotation_claims_absent(index_html, candidate_json, llms_txt):
    prohibited = (
        "secret rotation runbook", "secret rotation with zero", "zero-outage",
        "zero outage", "remediation completed", "enterprise-wide credential remediation",
    )
    for text_source, name in [
        (index_html, "index.html"),
        (json.dumps(candidate_json), "candidate-profile.json"),
        (llms_txt, "llms.txt"),
    ]:
        lower_text = text_source.lower()
        for term in prohibited:
            assert term not in lower_text, f"Found unsupported security claim '{term}' in {name}"


def test_unsupported_automated_rollback_claims_absent(index_html, candidate_json, llms_txt):
    prohibited = (
        "automated rollback trigger", "automated rollback safeguarding",
        "zero production regression", "zero-production-regression",
    )
    for text_source, name in [
        (index_html, "index.html"),
        (json.dumps(candidate_json), "candidate-profile.json"),
        (llms_txt, "llms.txt"),
    ]:
        lower_text = text_source.lower()
        for term in prohibited:
            assert term not in lower_text, f"Found unsupported deployment claim '{term}' in {name}"

    # Container deployment CLI must remain identified as prototype / proof of concept
    assert "status-prototype" in index_html
    cli_card = index_html.split('id="program-deployment-tooling"')[1].split("</article>")[0]
    assert "Proof of Concept" in cli_card
    assert "Production Deployed" not in cli_card


def test_llms_txt_and_candidate_json_match_canonical_career_facts(canonical, candidate_json, llms_txt):
    expected_title = canonical["experience"][0]["officialTitle"]
    expected_positioning = canonical["personal"]["title"]
    expected_company = canonical["experience"][0]["company"]

    assert candidate_json["candidate"]["officialCurrentTitle"] == expected_title
    assert candidate_json["candidate"]["positioningTitle"] == expected_positioning
    assert candidate_json["candidate"]["verifiedExperience"][0]["company"] == expected_company

    assert f"- Official Current Title: {expected_title} (Employer: {expected_company})" in llms_txt
    assert f"- Positioning Title: {expected_positioning}" in llms_txt


def test_cubs_color_tokens_and_appearance_modes_preserved():
    css = (ROOT / "style.css").read_text(encoding="utf-8")

    # Dark palette tokens (root)
    assert "--paper: #0b1422;" in css
    assert "--panel: #122035;" in css
    assert "--panel-solid: #172944;" in css
    assert "--ink: #eef3fb;" in css
    assert "--muted: #9eb0cb;" in css
    assert "--blue: #9fd3f4;" in css
    assert "--blue-deep: #4f8db8;" in css
    assert "--red: #ef4444;" in css
    assert "--line: #32587f;" in css

    # Light palette tokens
    assert '[data-theme="light"]' in css
    assert "--paper: #a8d8f0;" in css
    assert "--panel: #d9effb;" in css
    assert "--blue: #063d7a;" in css
    assert "--red: #b91c1c;" in css

    # Colorblind themes
    assert '[data-theme="colorblind"]' in css
    assert '[data-theme="colorblind"].dark-mode-colorblind' in css


def test_unsupported_autonomy_and_sandbox_claims_absent(index_html, candidate_json, llms_txt):
    prohibited = (
        "architect of autonomous",
        "autonomous multi-agent coordination frameworks",
        "deterministic evidence sandbox",
    )
    for text_source, name in [
        (index_html, "index.html"),
        (json.dumps(candidate_json), "candidate-profile.json"),
        (llms_txt, "llms.txt"),
    ]:
        lower_text = text_source.lower()
        for term in prohibited:
            assert term not in lower_text, f"Found uncalibrated claim '{term}' in {name}"

    # HowlProof badge must be Software Verification, not Evidence Sandbox
    assert "Evidence Sandbox" not in index_html
    assert "Software Verification" in index_html


def test_deployment_diagram_is_conceptual_and_non_sequential(index_html):
    assert "Conceptual architecture diagram of deployment safeguard layers" in index_html
    assert "Figure 1: Conceptual architecture of deployment safeguard layers" in index_html

    # Ensure no sequential directional arrow markers asserting an automated execution pipeline
    assert 'marker-end="url(#arrow)"' not in index_html

    # Ensure stages are named as architectural layers rather than execution sequence numbers
    assert "1. Preflight Drift Checks" not in index_html
    assert "2. Standardized Templates" not in index_html
    assert "3. Artifacts & Safeguards" not in index_html
    assert ">Preflight Drift Checks<" in index_html
    assert ">Standardized Templates<" in index_html
    assert ">Artifacts &amp; Safeguards<" in index_html


def test_github_profile_readme_matches_canonical_source(canonical):
    readme_path = ROOT / "documentation" / "github_profile_readme.md"
    assert readme_path.exists(), "documentation/github_profile_readme.md must exist"
    readme_text = readme_path.read_text(encoding="utf-8")

    current_role = next((role for role in canonical["experience"] if role.get("id") == "exp-stellantis"), canonical["experience"][0])
    official_title = current_role["officialTitle"]
    company = current_role["company"]
    location = canonical["personal"]["location"]
    canonical_base = canonical["seo"]["canonicalUrl"].rstrip("/")

    # Check identity facts
    assert f"**Senior Production Support Engineer** at {company}" in readme_text
    assert f"**Location:** {location} (Open to U.S. Remote Opportunities)" in readme_text
    assert f"[Portfolio]({canonical_base}/)" in readme_text
    assert f"[Software & Platform Resume (PDF)]({canonical_base}/William_Elias_Software_Platform_Resume.pdf)" in readme_text

    # Check project derivation from canonical resume.json
    projects_by_id = {p["id"]: p for p in canonical.get("projects", [])}
    for pid in ("project-howlplane", "project-howlproof", "project-howlframe", "project-password-arena", "project-howldream"):
        proj = projects_by_id[pid]
        repo_name = proj["link"].rstrip("/").split("/")[-1]
        assert f"[{repo_name}]({proj['link']})" in readme_text
        # Check that canonical highlights are present in the table
        for highlight in proj["highlights"]:
            assert highlight in readme_text

    # Ensure prohibited uncalibrated claims are absent
    prohibited = (
        "architect of autonomous",
        "deterministic evidence sandbox",
        "secret rotation",
        "automated rollback",
    )
    lower_readme = readme_text.lower()
    for term in prohibited:
        assert term not in lower_readme, f"Found prohibited term '{term}' in GitHub profile README"

    # Header check
    assert "| Repository | Focus | Technologies / Focus | Highlights |" in readme_text


def test_json_ld_alumni_of_and_credentials_semantics(index_html):
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', index_html, re.DOTALL)
    assert match, "JSON-LD script block not found"
    data = json.loads(match.group(1))
    person = data["mainEntity"]

    # alumniOf should only contain degree-granting universities
    alumni_names = [inst["name"] for inst in person.get("alumniOf", [])]
    assert "Dakota State University" in alumni_names
    assert "Colorado State University Global Campus" in alumni_names
    assert "Rochester College" in alumni_names
    assert "Cisco Networking Academy" not in alumni_names

    # hasCredential should contain CCNA without unsubstantiated recognizedBy organization
    credentials = person.get("hasCredential", [])
    assert len(credentials) == 1
    assert credentials[0]["@type"] == "EducationalOccupationalCredential"
    assert credentials[0]["name"] == "CCNA (Previously Held)"
    assert "recognizedBy" not in credentials[0], "Course provider must not be classified as recognizing authority"


def test_candidate_profile_schema_field_absent(candidate_json):
    assert "$schema" not in candidate_json
    assert candidate_json.get("entity") == "CandidateProfile"
