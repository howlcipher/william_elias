import pypdf
import pytest

from conftest import VARIANT_NAMES
from scripts.generate_resume_pdf import build, load_config, validate_config


@pytest.mark.parametrize("context", [None, 42, [], "", "   "])
def test_pdf_context_rejects_invalid_values(context):
    config = load_config()
    config["skills"][0]["pdfContext"] = context
    with pytest.raises(ValueError, match=r"skills\[0\].pdfContext"):
        validate_config(config)


def test_pdf_context_is_optional_and_renders_beside_its_category(tmp_path):
    config = load_config()
    for skill in config["skills"]:
        skill.pop("pdfContext", None)
    validate_config(config)
    config["skills"][0]["pdfContext"] = "Professional experience"
    validate_config(config)
    output = tmp_path / "qualified.pdf"
    build(config, output)
    text = " ".join(
        " ".join(page.extract_text().split())
        for page in pypdf.PdfReader(output).pages
    )
    assert "Software & Backend (Professional experience): Python" in text
    assert "DevOps & Delivery: Azure DevOps" in text


@pytest.mark.parametrize("variant", VARIANT_NAMES)
def test_each_pdf_preserves_ai_and_go_experience_levels(variant_pdfs, variants, variant):
    config = load_config()
    skills = {skill["id"]: skill for skill in config["skills"]}
    expected = {
        "skill-ai-engineering": "Internal tools & projects",
        "skill-automation-tooling": "Python/PowerShell professionally; Go for deployment tooling; uv for Python standardization",
        "skill-devops-delivery": "Azure DevOps professionally; containerization proof of concept",
    }
    for skill_id, context in expected.items():
        assert skills[skill_id]["pdfContext"] == context
    text = variant_pdfs[variant]["text"]
    # A selected category always carries its canonical qualifier; variants
    # cannot drop or rewrite it because pdfContext is canonical, not variant data.
    for skill_id in variants["variants"][variant]["skillIds"]:
        skill = skills[skill_id]
        if skill.get("pdfContext"):
            assert f'{skill["category"]} ({skill["pdfContext"]}):' in text
    assert "skill-automation-tooling" in variants["variants"][variant]["skillIds"]
    assert len(variant_pdfs[variant]["pages"]) == 2


@pytest.mark.parametrize("tags", [None, "Python", [], ["Unknown"], ["Python", "Python"], [42], [["Python"]]])
def test_pdf_tags_reject_invalid_or_unverified_selection(tags):
    config = load_config()
    config["skills"][0]["pdfTags"] = tags
    with pytest.raises(ValueError, match=r"skills\[0\].pdfTags"):
        validate_config(config)


def test_pdf_tags_default_to_leading_slice_when_omitted(tmp_path):
    config = load_config()
    config["skills"][0].pop("pdfTags")
    validate_config(config)
    output = tmp_path / "default-tags.pdf"
    build(config, output)
    text = " ".join(
        " ".join(page.extract_text().split()) for page in pypdf.PdfReader(output).pages
    )
    software = text.split("Software & Backend:")[1].split("SELECTED ENGINEERING")[0]
    assert "ASP.NET Core" in software
    assert "SQL Server" not in software
