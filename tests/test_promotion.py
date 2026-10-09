import json

import pytest
from pypdf import PdfReader

from scripts.build_html import render_experience, render_json_ld
from scripts.generate_resume_pdf import build, load_config, load_variants, validate_config


def promoted_config():
    config = load_config()
    role = config["experience"][0]
    role["officialTitle"] = "Senior Production Support Engineer"
    role["title"] = "Senior Production Support Engineer | DevOps & Automation"
    role["promotion"] = {
        "effectiveDate": "2026-09",
        "previousOfficialTitle": "Production Support Engineer",
    }
    return config


def test_promotion_metadata_is_valid_and_chronological():
    validate_config(load_config())
    validate_config(promoted_config())


@pytest.mark.parametrize(
    ("update", "message"),
    [
        (lambda promotion: promotion.pop("effectiveDate"), "exactly 'effectiveDate'"),
        (lambda promotion: promotion.update(effectiveDate="2023-01"), "within the employer tenure"),
        (lambda promotion: promotion.update(effectiveDate="2026-13"), "YYYY-MM format"),
        (lambda promotion: promotion.update(previousOfficialTitle=" "), "non-empty string"),
    ],
)
def test_invalid_promotion_metadata_fails_validation(update, message):
    config = promoted_config()
    update(config["experience"][0]["promotion"])
    with pytest.raises(ValueError, match=message):
        validate_config(config)


def test_roles_without_promotion_metadata_remain_valid():
    config = load_config()
    validate_config(config)
    role = config["experience"][1]
    rendered = render_experience([role])
    assert "timeline-promotion" not in rendered
    assert role["title"] in rendered


def test_website_and_json_ld_render_promotion_and_official_title():
    config = promoted_config()
    role = config["experience"][0]
    rendered = render_experience([role])
    assert "Senior Production Support Engineer | DevOps &amp; Automation" in rendered
    assert "Promoted September 2026; previously Production Support Engineer" in rendered
    assert role["date"] in rendered
    person = json.loads(render_json_ld(config))["mainEntity"]
    assert person["jobTitle"] == "Senior Production Support Engineer"


@pytest.mark.parametrize("variant", ["software_platform", "production_devops"])
def test_targeted_pdf_keeps_title_progression_and_shared_achievements(tmp_path, variant):
    config = promoted_config()
    output = tmp_path / f"{variant}.pdf"
    build(config, output, variant, load_variants())
    reader = PdfReader(output)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    assert "Senior Production Support Engineer | DevOps & Automation" in text
    assert "Promoted September 2026; previously Production Support Engineer" in text
    assert "Feb 2023 - Present" in text
    assert "CI/CD standardization program" in text
    assert len(reader.pages) == 2
