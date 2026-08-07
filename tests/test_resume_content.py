import html
import json
import re

import pypdf

from scripts.generate_resume_pdf import build, load_config, SITE_DIR


def _extract_pdf_pages(cfg, tmp_path):
    out_pdf = tmp_path / "content_check.pdf"
    build(cfg, out_pdf)
    reader = pypdf.PdfReader(out_pdf)
    return [page.extract_text() for page in reader.pages]


class TestResumeJsonValidity:
    def test_resume_json_is_valid_json(self):
        raw = (SITE_DIR / "resume.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        assert isinstance(data, dict)


class TestHeadlineAndPositioning:
    def test_public_headline_is_devops_platform(self):
        cfg = load_config()
        title = cfg["personal"]["title"]
        assert "DevOps" in title
        assert "Platform" in title

    def test_public_headline_does_not_lead_with_production_support(self):
        # The public-facing headline should read as Senior DevOps/Platform Engineer,
        # not Production Support -- that title is preserved only as the official
        # Stellantis job title inside the experience entry.
        cfg = load_config()
        assert "Production Support" not in cfg["personal"]["title"]

    def test_tagline_states_cicd_and_reliability_positioning(self):
        cfg = load_config()
        tagline = cfg["personal"]["tagline"]
        assert "CI/CD" in tagline or "Release" in tagline
        assert "Reliability" in tagline

    def test_official_stellantis_title_preserved(self):
        cfg = load_config()
        stellantis = next(j for j in cfg["experience"] if j["company"] == "Stellantis Financial Services")
        assert stellantis["title"] == "Production Support Engineer - DevOps & Automation"

    def test_remote_availability_present(self):
        cfg = load_config()
        assert "remote" in cfg["personal"]
        assert "remote" in cfg["personal"]["remote"].lower() or "u.s." in cfg["personal"]["remote"].lower()


class TestKeyMetrics:
    def test_three_defensible_metrics_present_in_stats(self):
        cfg = load_config()
        values = {s["value"] for s in cfg["stats"]}
        assert "~60" in values
        assert "100+" in values
        assert "300+" in values
        assert len(cfg["stats"]) == 3

    def test_estate_scope_not_overstated_as_migrated_or_deployed(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        assert "~60 applications migrated" not in blob
        assert "60 applications deployed" not in blob
        assert "60 applications migrated" not in blob

    def test_summary_states_true_program_scope(self):
        cfg = load_config()
        summary_lower = cfg["summary"].lower()
        assert "approximately 60" in summary_lower
        assert "100+ repositories" in summary_lower

    def test_summary_does_not_claim_100_plus_pipelines(self):
        # The "100+" metric belongs to repositories credential-remediated, not
        # pipelines created -- this was the exact inflation the truth-mode pass
        # corrected. Guard against it silently creeping back in.
        cfg = load_config()
        assert "100+ azure devops pipelines" not in cfg["summary"].lower()
        assert "100+ pipelines" not in cfg["summary"].lower()

    def test_cicd_program_preserves_28_of_60_distinction(self):
        cfg = load_config()
        cicd = next(p for p in cfg["selectedEngineeringPrograms"] if "CI/CD" in p["name"])
        blob = json.dumps(cicd)
        assert "28 of 60" in blob
        assert "27" in blob


class TestCoreExpertiseCategories:
    EXPECTED_CATEGORIES = {
        "DevOps & Release Engineering",
        "Automation & Software Engineering",
        "Security & Identity",
        "Observability & Reliability",
        "Infrastructure & Networking",
        "AI & Agentic Systems",
    }

    def test_six_curated_categories_present(self):
        cfg = load_config()
        categories = {s["category"] for s in cfg["skills"]}
        assert categories == self.EXPECTED_CATEGORIES

    def test_ai_category_is_subordinate_not_generic_expert_claim(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        for phrase in ("ai expert", "machine learning expert", "llm expert"):
            assert phrase not in blob

    def test_ai_category_has_credible_agentic_tooling(self):
        cfg = load_config()
        ai_skills = next(s for s in cfg["skills"] if s["category"] == "AI & Agentic Systems")
        for term in ("Claude Code", "MCP", "RAG", "Ollama"):
            assert any(term in tag for tag in ai_skills["tags"])


class TestSelectedEngineeringPrograms:
    EXPECTED_PROGRAMS = {
        "CI/CD & Release Engineering",
        "Credential Hygiene & Secrets Remediation",
        "Server Migration & DR Cutover",
        "Internal Web Apps & Support Portal",
        "Observability & Telemetry",
        "Python Ops Automation & Estate Reduction",
    }

    def test_six_programs_present(self):
        cfg = load_config()
        names = {p["name"] for p in cfg["selectedEngineeringPrograms"]}
        assert names == self.EXPECTED_PROGRAMS

    def test_every_program_has_pdf_bullet_and_technology(self):
        cfg = load_config()
        for prog in cfg["selectedEngineeringPrograms"]:
            assert prog.get("pdfBullet"), f"{prog['name']} missing pdfBullet"
            assert prog.get("bullets"), f"{prog['name']} missing bullets"
            assert prog.get("technology"), f"{prog['name']} missing technology"


class TestSelectedOpenSourceProjects:
    EXPECTED_PROJECTS = {
        "Multi-Agent Engineering Library",
        "AI Router",
        "Zero",
        "Baseball Optimizer",
        "RedrawUS",
        "Password Arena",
    }

    def test_exactly_six_projects_present(self):
        cfg = load_config()
        assert len(cfg["projects"]) == 6
        names = {p["name"] for p in cfg["projects"]}
        assert names == self.EXPECTED_PROJECTS

    def test_every_project_has_link_highlights_and_tags(self):
        cfg = load_config()
        for proj in cfg["projects"]:
            assert proj.get("link", "").startswith("https://github.com/"), f"{proj['name']} missing a GitHub link"
            assert proj.get("highlights"), f"{proj['name']} missing highlights"
            assert proj.get("tags"), f"{proj['name']} missing tags"

    def test_redrawus_links_to_correct_repo_and_avoids_partisan_framing(self):
        cfg = load_config()
        proj = next(p for p in cfg["projects"] if p["name"] == "RedrawUS")
        assert proj["link"] == "https://github.com/howlcipher/redistricting-map"
        blob = " ".join(proj["highlights"] + [proj["subtitle"]]).lower()
        for term in ("democrat", "republican", "gerrymander", "partisan"):
            assert term not in blob, f"RedrawUS card should not lead with '{term}'"
        for tag in ("Python", "R", "Geospatial", "JavaScript", "Playwright"):
            assert tag in proj["tags"]

    def test_password_arena_links_to_correct_repo_and_avoids_ai_overclaims(self):
        cfg = load_config()
        proj = next(p for p in cfg["projects"] if p["name"] == "Password Arena")
        assert proj["link"] == "https://github.com/howlcipher/password_arena"
        blob = " ".join(proj["highlights"] + [proj["subtitle"]]).lower()
        for term in ("reinforcement learning", "trained ai agent", "autonomous password cracking", "neural network", "llm"):
            assert term not in blob, f"Password Arena card should not claim '{term}'"
        assert "agent systems" not in [t.lower() for t in proj["tags"]]
        for tag in ("Python", "Cybersecurity", "Docker", "pytest"):
            assert tag in proj["tags"]

    def test_projects_omitted_from_pdf(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        assert "RedrawUS" not in blob
        assert "Password Arena" not in blob


class TestNoUnsupportedClaims:
    def test_no_unsupported_cloud_infra_claims(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        for term in ("Terraform", "Kubernetes", "AKS"):
            assert term not in blob, f"'{term}' should not appear as claimed professional experience"

    def test_no_bare_aws_gcp_claims(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        assert re.search(r"\bAWS\b", blob) is None
        assert re.search(r"\bGCP\b", blob) is None

    def test_no_automated_identity_lifecycle_claim(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        assert "deprovisioning" not in blob
        assert "automated identity lifecycle" not in blob

    def test_no_zero_hallucination_or_fully_autonomous_claims(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        assert "zero-hallucination" not in blob
        assert "zero hallucination" not in blob
        assert "fully autonomous" not in blob

    def test_container_poc_not_framed_as_production_kubernetes(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        assert "production kubernetes" not in blob


class TestPdfLayout:
    def test_pdf_is_exactly_two_pages(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        assert len(pages) == 2

    def test_selected_engineering_programs_starts_page_two(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        assert "SELECTED ENGINEERING PROGRAMS" not in pages[0].upper()
        assert pages[1].upper().lstrip().startswith("SELECTED ENGINEERING PROGRAMS")

    def test_page_one_has_summary_expertise_and_experience(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        page_one_upper = pages[0].upper()
        assert "PROFESSIONAL SUMMARY" in page_one_upper
        assert "CORE EXPERTISE" in page_one_upper
        assert "PROFESSIONAL EXPERIENCE" in page_one_upper

    def test_page_two_has_earlier_experience_and_education(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        page_two_upper = pages[1].upper()
        assert "EARLIER TECHNICAL EXPERIENCE" in page_two_upper
        assert "EDUCATION" in page_two_upper

    def test_all_six_programs_render_in_pdf(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        for prog in cfg["selectedEngineeringPrograms"]:
            assert prog["name"] in blob

    def test_additional_experience_present_in_pdf(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        for job in cfg["additionalExperience"]:
            assert job["company"] in blob
            assert job["title"] in blob


class TestReadmeRecruiterFacing:
    def test_readme_leads_with_headline_and_remote(self):
        readme = (SITE_DIR / "README.md").read_text(encoding="utf-8")
        cfg = load_config()
        head = readme[:600]
        assert cfg["personal"]["title"] in head
        assert "Remote" in head

    def test_readme_surfaces_links_and_metrics(self):
        readme = (SITE_DIR / "README.md").read_text(encoding="utf-8")
        cfg = load_config()
        assert cfg["personal"]["linkedin"] in readme
        assert cfg["personal"]["github"] in readme
        for s in cfg["stats"]:
            assert s["value"] in readme

    def test_readme_preserves_developer_docs(self):
        readme = (SITE_DIR / "README.md").read_text(encoding="utf-8")
        assert "resume.json" in readme
        assert "PYTHONPATH=. pytest tests/" in readme


class TestGeneratedAssetsSynchronized:
    def test_config_js_matches_resume_json(self):
        cfg = load_config()
        config_js = (SITE_DIR / "config.js").read_text(encoding="utf-8")
        match = re.search(r"const config = (.*);\s*$", config_js, re.DOTALL)
        assert match, "config.js must define `const config = {...};`"
        embedded = json.loads(match.group(1))
        assert embedded == cfg

    def test_index_html_reflects_current_title(self):
        cfg = load_config()
        html_content = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert cfg["personal"]["name"] in html_content
        assert cfg["personal"]["title"] in html_content

    def test_index_html_has_programs_and_ai_capabilities_sections(self):
        html_content = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="programs"' in html_content
        assert 'id="ai-capabilities"' in html_content
        for prog in load_config()["selectedEngineeringPrograms"]:
            assert html.escape(prog["name"], quote=True) in html_content

    def test_index_html_reflects_remote_availability(self):
        cfg = load_config()
        html_content = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert cfg["personal"]["remote"] in html_content

    def test_seo_meta_description_mentions_devops_and_platform(self):
        html_content = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        desc_match = re.search(r'<meta name="description" content="(.*?)">', html_content)
        assert desc_match
        desc = desc_match.group(1)
        assert "DevOps" in desc
        assert "Platform" in desc
