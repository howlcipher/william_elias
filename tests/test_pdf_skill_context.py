import pypdf
import pytest

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


def test_current_pdf_preserves_ai_and_go_experience_levels(tmp_path):
    config = load_config()
    skills = {skill["category"]: skill for skill in config["skills"]}
    expected = {
        "AI-Enabled Engineering": "Internal tools & projects",
        "Automation": "Python/PowerShell professionally; Go in projects",
    }
    output = tmp_path / "resume.pdf"
    build(config, output)
    pages = pypdf.PdfReader(output).pages
    text = " ".join(pages[0].extract_text().split())
    for category, context in expected.items():
        assert skills[category]["pdfContext"] == context
        assert f"{category} ({context}):" in text
    assert len(pages) == 2


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
    text = " ".join(pypdf.PdfReader(output).pages[0].extract_text().split())
    software = text.split("Software & Backend:")[1].split("DevOps & Delivery:")[0]
    assert "ASP.NET Core" in software
    assert "SQL Server" not in software
