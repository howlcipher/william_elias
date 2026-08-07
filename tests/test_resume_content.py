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
        stellantis = next(j for j in cfg["experience"] if "Stellantis Financial Services" in j["company"])
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
        assert "56" in values
        assert "100+" in values
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
        assert "approximately 60-application estate" in summary_lower

    def test_summary_does_not_claim_100_plus_pipelines(self):
        cfg = load_config()
        assert "100+ azure devops ci/cd pipelines" not in cfg["summary"].lower()
        assert "100+ azure devops" not in cfg["summary"].lower()

    def test_no_100_plus_pipeline_claim_anywhere(self, tmp_path):
        cfg = load_config()
        banned = (
            "100+ azure devops ci/cd pipelines",
            "100+ azure devops pipelines",
            "built 100+ azure devops",
            "100 azure devops ci/cd pipelines",
        )
        blob = json.dumps(cfg).lower()
        for phrase in banned:
            assert phrase not in blob, f"resume.json still contains '{phrase}'"

        config_js = (SITE_DIR / "config.js").read_text(encoding="utf-8").lower()
        index_html = (SITE_DIR / "index.html").read_text(encoding="utf-8").lower()
        for phrase in banned:
            assert phrase not in config_js, f"config.js still contains '{phrase}'"
            assert phrase not in index_html, f"index.html still contains '{phrase}'"

        pages = _extract_pdf_pages(cfg, tmp_path)
        pdf_blob = "\n".join(pages).lower()
        for phrase in banned:
            assert phrase not in pdf_blob, f"PDF still contains '{phrase}'"

    def test_verified_cicd_rollout_numbers_present(self, tmp_path):
        cfg = load_config()
        blob = json.dumps(cfg)
        assert "56 Azure DevOps build/release definitions" in blob
        assert "28 applications" in blob
        assert "27" in blob
        assert "25 deployment plans" in blob or "25 of 28" in blob

        pages = _extract_pdf_pages(cfg, tmp_path)
        pdf_blob = "\n".join(pages)
        assert "56 Azure DevOps" in pdf_blob
        assert "28 applications" in pdf_blob
        assert "27" in pdf_blob

    def test_no_deployment_completion_implied(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        banned_phrases = (
            "deployed 28 applications",
            "rolled out 28 applications",
            "migrated 28 applications to production",
            "production deployments completed",
            "28 applications deployed",
            "28 applications to production",
        )
        for phrase in banned_phrases:
            assert phrase not in blob, f"resume.json implies deployment via '{phrase}'"
        assert "zero applications" in blob or "zero deployments" in blob

    def test_estate_organization_numbers_kept_separate_from_created_definitions(self):
        cfg = load_config()
        cicd = next(p for p in cfg["selectedEngineeringPrograms"] if "CI/CD" in p["name"])
        blob = json.dumps(cicd)
        assert "157" in blob
        assert "95" in blob
        # 157/95 describe organization/inventory, not creation -- guard against
        # phrasing that would fold them into the "56 created" claim.
        assert "157 azure devops build/release definitions created" not in blob.lower()
        assert "built 157" not in blob.lower()

    def test_credential_remediation_metric_intact(self):
        cfg = load_config()
        values = {s["value"] for s in cfg["stats"]}
        assert "100+" in values
        stats_blob = json.dumps(cfg["stats"])
        assert "credential" in stats_blob.lower() or "repositories" in stats_blob.lower()
        summary_and_experience = cfg["summary"] + json.dumps(cfg["experience"])
        assert "100+ repositories" in summary_and_experience

    def test_cicd_program_preserves_verified_metrics(self):
        cfg = load_config()
        cicd = next(p for p in cfg["selectedEngineeringPrograms"] if "CI/CD" in p["name"])
        blob = json.dumps(cicd)
        assert "56" in blob
        assert "28" in blob
        assert "27" in blob
        assert "25" in blob
        assert "six" in blob.lower()
        assert "zero" in blob.lower()


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
        for term in ("MCP", "RAG"):
            assert any(term in tag for tag in ai_skills["tags"])

    def test_automation_category_reflects_curated_language_breadth(self):
        cfg = load_config()
        automation = next(s for s in cfg["skills"] if s["category"] == "Automation & Software Engineering")
        tags = automation["tags"]
        for core in ("Python", "PowerShell", "C#", "Go", "SQL"):
            assert core in tags
        assert "Java" not in tags



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

    def test_pdf_includes_only_selected_projects(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        assert "Multi-Agent Engineering Library" in blob
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

    def test_no_kubernetes_family_terms_anywhere(self, tmp_path):
        # Kubernetes/K8s/AKS/EKS/GKE must not appear as a general skill, in the
        # summary, skills categories, or SEO keywords -- the defensible container
        # experience is Docker/Docker Compose/Helm/Rancher Desktop/IIS ARR only.
        cfg = load_config()
        blob = json.dumps(cfg)
        for term in ("Kubernetes", "AKS", "EKS", "GKE"):
            assert term not in blob, f"'{term}' should not appear anywhere in resume.json"
        assert re.search(r"\bK8s\b", blob, re.IGNORECASE) is None

        config_js = (SITE_DIR / "config.js").read_text(encoding="utf-8")
        index_html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        for term in ("Kubernetes", "AKS", "EKS", "GKE"):
            assert term not in config_js
            assert term not in index_html

        pages = _extract_pdf_pages(cfg, tmp_path)
        pdf_blob = "\n".join(pages)
        for term in ("Kubernetes", "AKS", "EKS", "GKE"):
            assert term not in pdf_blob

    def test_seo_knows_about_excludes_kubernetes(self):
        cfg = load_config()
        knows_about = cfg.get("seo", {}).get("knowsAbout", [])
        for term in knows_about:
            assert "kubernetes" not in term.lower()

    def test_helm_and_docker_retained_as_infrastructure_tags(self):
        # Helm/Docker/Docker Compose/Rancher Desktop are real, scoped experience
        # (packaging + a WSL2 container-host POC) and should remain.
        cfg = load_config()
        infra = next(s for s in cfg["skills"] if s["category"] == "Infrastructure & Networking")
        assert "Docker" in infra["tags"]
        assert "Docker Compose" in infra["tags"]
        assert "Helm" in infra["tags"]
        assert "Rancher Desktop" in infra["tags"]

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
        assert "SELECTED DEVOPS & PLATFORM ENGINEERING HIGHLIGHTS" not in pages[0].upper()
        assert pages[1].upper().lstrip().startswith("SELECTED DEVOPS & PLATFORM ENGINEERING HIGHLIGHTS")

    def test_page_one_has_summary_expertise_and_experience(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        page_one_upper = pages[0].upper()
        assert "PROFESSIONAL SUMMARY" in page_one_upper
        assert "CORE EXPERTISE" in page_one_upper
        assert "PROFESSIONAL EXPERIENCE" in page_one_upper

    def test_page_two_has_education(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        page_two_upper = pages[1].upper()
        assert "EDUCATION & CERTIFICATION" in page_two_upper

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

    def test_all_six_employers_present_in_pdf(self, tmp_path):
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        expected_employers = [job["company"] for job in cfg["experience"]] + [
            job["company"] for job in cfg["additionalExperience"]
        ]
        assert len(expected_employers) == 6
        for company in expected_employers:
            assert company in blob, f"'{company}' missing from generated PDF"


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
