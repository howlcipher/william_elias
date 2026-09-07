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


def test_current_pdf_preserves_ai_and_container_experience_levels(tmp_path):
    config = load_config()
    skills = {skill["category"]: skill for skill in config["skills"]}
    expected = {
        "AI-Enabled Engineering": "Internal tools & projects",
        "Additional Hands-On Technologies":
            "Projects & container-host proof of concept",
    }
    output = tmp_path / "resume.pdf"
    build(config, output)
    pages = pypdf.PdfReader(output).pages
    text = " ".join(pages[0].extract_text().split())
    for category, context in expected.items():
        assert skills[category]["pdfContext"] == context
        assert f"{category} ({context}):" in text
    assert len(pages) == 2
