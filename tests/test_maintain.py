"""Unit tests for scripts/maintain.py maintenance tooling."""

import copy
import json
import subprocess
import sys
from pathlib import Path
import pytest

from scripts.maintain import (
    validate_canonical_rules,
    validate_documentation_links,
    validate_html_anchors,
    validate_structured_data,
    verify_pdf_alias_equivalence,
    ROOT,
)


@pytest.fixture(scope="module")
def canonical():
    return json.loads((ROOT / "resume.json").read_text(encoding="utf-8"))


def test_validate_canonical_rules_passes_on_valid_resume(canonical):
    errors = validate_canonical_rules(canonical)
    assert errors == [], f"Unexpected validation errors: {errors}"


def test_validate_canonical_rules_catches_invalid_location(canonical):
    bad = copy.deepcopy(canonical)
    bad["personal"]["location"] = "Dallas, TX"
    errors = validate_canonical_rules(bad)
    assert any("Invalid location" in err for err in errors)


def test_validate_canonical_rules_catches_invalid_title(canonical):
    bad = copy.deepcopy(canonical)
    bad["experience"][0]["officialTitle"] = "Lead DevOps Architect"
    errors = validate_canonical_rules(bad)
    assert any("Senior Production Support Engineer" in err for err in errors)


def test_validate_canonical_rules_catches_invalid_positioning(canonical):
    bad = copy.deepcopy(canonical)
    bad["personal"]["title"] = "Full Stack Ninja"
    errors = validate_canonical_rules(bad)
    assert any("Software & Automation Engineer" in err for err in errors)


def test_validate_canonical_rules_catches_forbidden_phrases(canonical):
    bad = copy.deepcopy(canonical)
    bad["summary"] = "Implemented enterprise secret rotation across production."
    errors = validate_canonical_rules(bad)
    assert any("secret rotation" in err for err in errors)


def test_validate_canonical_rules_catches_missing_bs_information_technology(canonical):
    bad = copy.deepcopy(canonical)
    bad["education"] = [e for e in bad["education"] if e.get("degree") != "B.S. Information Technology"]
    errors = validate_canonical_rules(bad)
    assert any("B.S. Information Technology" in err for err in errors)


def test_validate_structured_data_passes_on_current_workspace():
    errors = validate_structured_data(ROOT)
    assert errors == [], f"Structured data validation failed: {errors}"


def test_validate_structured_data_catches_unsubstantiated_recognized_by(tmp_path):
    (tmp_path / "index.html").write_text(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfilePage",'
        '"mainEntity":{"@type":"Person","name":"William Elias","jobTitle":"Senior Production Support Engineer",'
        '"alumniOf":[{"@type":"CollegeOrUniversity","name":"Rochester College"}],'
        '"hasCredential":[{"@type":"EducationalOccupationalCredential","name":"CCNA (Previously Held)",'
        '"recognizedBy":{"@type":"Organization","name":"Cisco Networking Academy"}}]}}</script>',
        encoding="utf-8",
    )
    errors = validate_structured_data(tmp_path)
    assert any("must not include unsubstantiated recognizedBy" in err for err in errors)


def test_validate_structured_data_catches_schema_in_candidate_profile(tmp_path):
    (tmp_path / "index.html").write_text(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfilePage",'
        '"mainEntity":{"@type":"Person","name":"William Elias","jobTitle":"Senior Production Support Engineer",'
        '"alumniOf":[{"@type":"CollegeOrUniversity","name":"Rochester College"}],'
        '"hasCredential":[{"@type":"EducationalOccupationalCredential","name":"CCNA (Previously Held)"}]}}</script>',
        encoding="utf-8",
    )
    (tmp_path / "candidate-profile.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "entity": "CandidateProfile"}),
        encoding="utf-8",
    )
    errors = validate_structured_data(tmp_path)
    assert any("must not declare a draft '$schema'" in err for err in errors)


def test_verify_pdf_alias_equivalence_passes_on_current_workspace():
    errors = verify_pdf_alias_equivalence(ROOT)
    assert errors == [], f"PDF alias equivalence failed: {errors}"


def test_verify_pdf_alias_equivalence_catches_mismatch(tmp_path):
    (tmp_path / "William_Elias_Resume.pdf").write_bytes(b"content_a")
    (tmp_path / "William_Elias_Production_DevOps_Resume.pdf").write_bytes(b"content_b")
    errors = verify_pdf_alias_equivalence(tmp_path)
    assert any("differs" in err for err in errors)


def test_maintain_cli_check_flag():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "maintain.py"), "--check", "--skip-banner"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "All checks passed successfully." in proc.stdout
    assert "Freshness Checked (Isolated Build):" in proc.stdout
    assert "Local Repository Git State:" in proc.stdout
    assert "Sibling Profile Repository (howlcipher/howlcipher):" in proc.stdout


def test_validate_html_anchors_passes_on_current_workspace():
    errors = validate_html_anchors(ROOT)
    assert errors == [], f"Anchor validation errors: {errors}"


def test_validate_html_anchors_catches_missing_target(tmp_path):
    (tmp_path / "index.html").write_text(
        '<a href="#missing-target">Click</a><div id="existing-target"></div>',
        encoding="utf-8",
    )
    errors = validate_html_anchors(tmp_path)
    assert any("missing-target" in err for err in errors)


def test_validate_documentation_links_passes_on_current_workspace():
    errors = validate_documentation_links(ROOT)
    assert errors == [], f"Documentation link errors: {errors}"


def test_validate_documentation_links_catches_missing_target(tmp_path):
    doc_dir = tmp_path / "documentation"
    doc_dir.mkdir()
    (doc_dir / "test.md").write_text(
        "[Missing Doc](../non_existent_file.md)",
        encoding="utf-8",
    )
    errors = validate_documentation_links(tmp_path)
    assert any("non_existent_file.md" in err for err in errors)
