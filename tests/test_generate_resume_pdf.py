import json
from pathlib import Path
import pytest

from scripts.generate_resume_pdf import ResumePDF, build, load_config, validate_config, SITE_DIR


class TestLoadConfig:
    def test_load_config_default(self):
        """Verify load_config loads and parses the default site config.js correctly."""
        cfg = load_config()
        assert isinstance(cfg, dict)
        assert "personal" in cfg
        assert "summary" in cfg
        assert "skills" in cfg
        assert "experience" in cfg
        assert "projects" in cfg
        assert "education" in cfg
        assert cfg["personal"]["name"] == "William Elias"




class TestOrphanPreventionLogic:
    @pytest.fixture
    def pdf(self):
        pdf = ResumePDF()
        pdf.add_page()
        return pdf

    def test_bullet_height_single_line(self, pdf: ResumePDF):
        """Verify bullet_height returns height for a single-line bullet (13pt per line)."""
        text = "Short achievement line."
        height = pdf.bullet_height(text)
        assert height == 11.5

    def test_bullet_height_multi_line(self, pdf: ResumePDF):
        """Verify bullet_height calculates wrapping line height for long text."""
        long_text = (
            "Independently architected a reusable Azure DevOps CI/CD framework "
            "designed to scale delivery from one pipeline to 70+ .NET applications "
            "hosted on IIS, using YAML templates, Python, PowerShell, artifact creation, "
            "deployments, and approval gates."
        )
        height = pdf.bullet_height(long_text)
        # Should wrap into multiple lines (e.g. 3 lines = 39pt)
        assert height > 11.5
        assert height % 11.5 == 0

    def test_bullet_height_custom_indent(self, pdf: ResumePDF):
        """Verify modifying indent adjusts available width and resulting height."""
        long_text = "A moderately long sentence to test wrapping behavior under wider or narrower indents."
        h_narrow = pdf.bullet_height(long_text, indent=300)
        h_wide = pdf.bullet_height(long_text, indent=0)
        assert h_narrow >= h_wide

    def test_keep_together_no_break(self, pdf: ResumePDF):
        """Verify keep_together does not add a page if content fits on current page."""
        initial_page = pdf.page_no()
        pdf.keep_together(50)
        assert pdf.page_no() == initial_page

    def test_keep_together_forces_page_break(self, pdf: ResumePDF):
        """Verify keep_together forces a new page when content exceeds page bounds."""
        initial_page = pdf.page_no()
        # Set Y close to bottom of page (page height 792, margin 54 -> max trigger 738)
        pdf.set_y(700)
        pdf.keep_together(100)  # 700 + 100 = 800 > 738
        assert pdf.page_no() == initial_page + 1
        assert pdf.get_y() == pdf.t_margin


class TestPDFBuilder:
    def test_build_generates_pdf_file(self, tmp_path: Path):
        """Verify build() creates a valid PDF output file from config dict."""
        cfg = load_config()
        out_pdf = tmp_path / "test_output.pdf"
        build(cfg, out_pdf)

        assert out_pdf.exists()
        assert out_pdf.stat().st_size > 0
        with open(out_pdf, "rb") as f:
            header = f.read(5)
            assert header == b"%PDF-"


class TestValidateConfig:
    def test_validate_config_success(self):
        cfg = load_config()
        validate_config(cfg)
        
    def test_validate_config_missing_field(self):
        cfg = load_config()
        del cfg["skills"]
        with pytest.raises(ValueError, match="Validation failed: Missing required top-level field 'skills'"):
            validate_config(cfg)
            
    def test_validate_config_bad_url(self):
        cfg = load_config()
        cfg["personal"]["linkedin"] = "ftp://linkedin.com"
        with pytest.raises(ValueError, match="must be a valid URL"):
            validate_config(cfg)

    def test_validate_config_not_array(self):
        cfg = load_config()
        cfg["experience"] = "Not an array"
        with pytest.raises(ValueError, match="must be an array"):
            validate_config(cfg)

    @pytest.mark.parametrize("field", ["name", "phone", "email", "tagline"])
    def test_validate_config_missing_personal_field(self, field):
        cfg = load_config()
        del cfg["personal"][field]
        with pytest.raises(ValueError, match=f"Validation failed: 'personal.{field}' is required"):
            validate_config(cfg)

    @pytest.mark.parametrize("field", ["company", "date", "title"])
    def test_validate_config_missing_experience_field(self, field):
        cfg = load_config()
        del cfg["experience"][0][field]
        with pytest.raises(ValueError, match=f"Validation failed: 'experience\\[0\\].{field}' is required"):
            validate_config(cfg)

    @pytest.mark.parametrize("field", ["category", "tags"])
    def test_validate_config_missing_skills_field(self, field):
        cfg = load_config()
        del cfg["skills"][0][field]
        with pytest.raises(ValueError, match=f"Validation failed: 'skills\\[0\\].{field}' is required"):
            validate_config(cfg)

    @pytest.mark.parametrize("field", ["name", "subtitle"])
    def test_validate_config_missing_projects_field(self, field):
        cfg = load_config()
        del cfg["projects"][0][field]
        with pytest.raises(ValueError, match=f"Validation failed: 'projects\\[0\\].{field}' is required"):
            validate_config(cfg)

    @pytest.mark.parametrize("field", ["degree", "school"])
    def test_validate_config_missing_education_field(self, field):
        cfg = load_config()
        del cfg["education"][0][field]
        with pytest.raises(ValueError, match=f"Validation failed: 'education\\[0\\].{field}' is required"):
            validate_config(cfg)
