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
    def test_public_headline_positioning(self):
        cfg = load_config()
        title = cfg["personal"]["title"]
        assert "Software" in title
        assert "DevOps" in title
        assert "Automation Engineer" in title
        assert "Platform Engineer" not in title

    def test_public_headline_does_not_lead_with_production_support(self):
        cfg = load_config()
        assert "Production Support" not in cfg["personal"]["title"]

    def test_tagline_states_software_automation_and_reliability_positioning(self):
        cfg = load_config()
        tagline = cfg["personal"]["tagline"]
        assert "Software" in tagline or "Building" in tagline
        assert "Automating" in tagline or "Automation" in tagline
        assert "Reliable" in tagline or "Reliability" in tagline

    def test_summary_leads_with_software_devops_automation_positioning(self):
        cfg = load_config()
        assert cfg["summary"].startswith("Software, DevOps, and automation engineer with 10+ years")
        assert "Senior DevOps" not in cfg["summary"]
        assert "Platform Engineer" not in cfg["summary"]

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
        # "estate" framing keeps the ~60 figure as scope, never as applications
        # migrated or deployed.
        assert "60-application estate" in summary_lower

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
        "Software & Backend",
        "Web Development",
        "DevOps & Delivery",
        "Automation",
        "Production & Reliability",
        "Infrastructure & Application Operations",
        "Security & Identity",
        "AI-Enabled Engineering",
        "Additional Programming Foundations",
        "Additional Hands-On Technologies",
    }

    def test_curated_categories_present(self):
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
        ai_skills = next(s for s in cfg["skills"] if s["category"] == "AI-Enabled Engineering")
        for term in ("MCP", "RAG"):
            assert any(term in tag for tag in ai_skills["tags"])

    def test_languages_and_tools_reflected_in_software_and_automation(self):
        cfg = load_config()
        software = next(s for s in cfg["skills"] if s["category"] == "Software & Backend")
        automation = next(s for s in cfg["skills"] if s["category"] == "Automation")
        combined = software["tags"] + automation["tags"]
        for core in ("Python", "FastAPI", "PowerShell", "C#", "Go", "SQL Server"):
            assert core in combined
        assert "Java" not in combined

    def test_web_development_category_has_frontend_basics(self):
        cfg = load_config()
        web = next(s for s in cfg["skills"] if s["category"] == "Web Development")
        for tag in ("JavaScript", "HTML", "CSS"):
            assert tag in web["tags"]

    def test_additional_programming_foundations_represents_java_as_coursework(self):
        cfg = load_config()
        foundations = next(
            s for s in cfg["skills"] if s["category"] == "Additional Programming Foundations"
        )
        assert "Java" in foundations["tags"]
        # The non-professional framing has to live in the visible category name itself --
        # render_skills() has no subtitle field to attach a caveat to.
        assert "Foundations" in foundations["category"]
        assert "Professional" not in foundations["category"]

    def test_new_website_only_categories_excluded_from_pdf(self, tmp_path):
        cfg = load_config()
        blob = "\n".join(_extract_pdf_pages(cfg, tmp_path))
        assert "Web Development" not in blob
        assert "Additional Programming Foundations" not in blob



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

    def test_every_program_has_bullets_and_technology(self):
        cfg = load_config()
        for prog in cfg["selectedEngineeringPrograms"]:
            assert prog.get("bullets"), f"{prog['name']} missing bullets"
            assert prog.get("technology"), f"{prog['name']} missing technology"


class TestPdfEngineeringHighlights:
    """The PDF carries a curated condensation of the website's six programs.

    `selectedEngineeringPrograms` is website-only and shows breadth;
    `pdfEngineeringHighlights` is PDF-only and shows the strongest evidence.
    """

    EXPECTED_HIGHLIGHTS = {
        "CI/CD & Release Engineering",
        "Security & Secrets Remediation",
        "Platform Reliability & Developer Enablement",
    }

    def test_three_curated_highlights_present(self):
        cfg = load_config()
        names = {h["name"] for h in cfg["pdfEngineeringHighlights"]}
        assert names == self.EXPECTED_HIGHLIGHTS

    def test_every_highlight_has_bullets_and_technology(self):
        cfg = load_config()
        for hl in cfg["pdfEngineeringHighlights"]:
            assert hl.get("bullets"), f"{hl['name']} missing bullets"
            assert hl.get("technology"), f"{hl['name']} missing technology"

    def test_pdf_renders_only_the_curated_highlights(self, tmp_path):
        cfg = load_config()
        blob = "\n".join(_extract_pdf_pages(cfg, tmp_path))
        for name in self.EXPECTED_HIGHLIGHTS:
            assert name in blob, f"'{name}' missing from generated PDF"
        # Website-only programs must stay off the PDF so page 2 stays scannable.
        for name in ("Server Migration & DR Cutover", "Internal Web Apps & Support Portal"):
            assert name not in blob, f"'{name}' should be website-only, not in the PDF"

    def test_website_retains_all_six_programs(self):
        # Breadth belongs on the portfolio even though the PDF is selective.
        index_html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        for prog in load_config()["selectedEngineeringPrograms"]:
            assert html.escape(prog["name"], quote=True) in index_html

    def test_highlight_metrics_are_supported_by_website_programs(self):
        # Every number the PDF claims must trace back to the fuller program
        # descriptions, so condensing can never introduce an unsupported metric.
        cfg = load_config()
        supporting = json.dumps(cfg["selectedEngineeringPrograms"])
        supporting_numbers = set(re.findall(r"\d[\d,]*", supporting))
        for hl in cfg["pdfEngineeringHighlights"]:
            for bullet in hl["bullets"]:
                for number in re.findall(r"\d[\d,]*", bullet):
                    assert number in supporting_numbers, (
                        f"'{number}' in PDF highlight '{hl['name']}' has no support "
                        "in selectedEngineeringPrograms"
                    )


class TestEducationHonesty:
    """The master's degree is in progress and the CCNA is lapsed.

    Both qualifiers are load-bearing: dropping either would turn an accurate
    entry into a false credential claim, so they are asserted through to the
    rendered PDF rather than only in resume.json.
    """

    def _entry(self, cfg, prefix):
        return next(e for e in cfg["education"] if e["degree"].startswith(prefix))

    def test_masters_marked_in_progress_and_not_claimed_complete(self):
        cfg = load_config()
        masters = self._entry(cfg, "M.S.")
        assert "In Progress" in masters["degree"]
        assert masters["school"] == "Dakota State University"
        # A bare degree line with no qualifier would read as conferred.
        assert masters["degree"] != "M.S. Cyber Defense"
        blob = json.dumps(cfg).lower()
        for phrase in ("m.s. cyber defense, completed", "master of science completed"):
            assert phrase not in blob

    def test_ccna_marked_previously_held(self):
        cfg = load_config()
        ccna = self._entry(cfg, "CCNA")
        assert "previously held" in ccna["degree"].lower()

    def test_qualifiers_survive_into_the_pdf(self, tmp_path):
        cfg = load_config()
        blob = "\n".join(_extract_pdf_pages(cfg, tmp_path))
        assert "In Progress" in blob
        assert "Previously Held" in blob

    def test_masters_stays_out_of_the_headline(self):
        # Education supports the story; it is not the positioning.
        cfg = load_config()
        for field in (cfg["personal"]["title"], cfg["personal"]["tagline"]):
            assert "Cyber Defense" not in field
            assert "M.S." not in field


class TestPdfContactLinks:
    def test_pdf_header_exposes_portfolio_linkedin_and_github(self, tmp_path):
        # The PDF is the selective document; the portfolio is the proof layer
        # behind it, so the header has to point at all three.
        cfg = load_config()
        page_one = _extract_pdf_pages(cfg, tmp_path)[0]
        assert "linkedin.com/in/wylelias" in page_one
        assert "github.com/howlcipher" in page_one
        portfolio = re.sub(r"^https?://", "", cfg["seo"]["canonicalUrl"]).rstrip("/")
        assert portfolio in page_one

    def test_pdf_links_are_annotations_not_replacements_for_text(self, tmp_path):
        # Clickable URLs must not cost ATS-readable text: every link annotation
        # target also has to appear as extractable characters.
        import pypdf

        cfg = load_config()
        out_pdf = tmp_path / "link_check.pdf"
        build(cfg, out_pdf)
        reader = pypdf.PdfReader(out_pdf)
        blob = "\n".join(page.extract_text() for page in reader.pages)

        targets = set()
        for page in reader.pages:
            for annot in page.get("/Annots") or []:
                uri = annot.get_object().get("/A", {}).get("/URI")
                if uri:
                    targets.add(str(uri))

        assert targets, "expected clickable link annotations in the PDF"
        for uri in targets:
            assert re.sub(r"^https?://", "", uri).rstrip("/") in blob


class TestSelectedOpenSourceProjects:
    EXPECTED_PROJECTS = {
        "Multi-Agent Engineering Library",
        "AI Router",
        "HowlFrame",
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

    def test_helm_and_docker_framed_as_hands_on_project_technologies(self):
        # Helm/Docker/Docker Compose/Rancher Desktop are framed as hands-on / project technologies.
        cfg = load_config()
        hands_on = next(s for s in cfg["skills"] if "Hands-On" in s["category"])
        assert "Docker" in hands_on["tags"]
        assert "Docker Compose" in hands_on["tags"]
        assert "Helm" in hands_on["tags"]
        assert "Rancher Desktop" in hands_on["tags"]
        # Ensure Docker and Helm are not placed beside core infrastructure experience
        infra = next(s for s in cfg["skills"] if s["category"] == "Infrastructure & Application Operations")
        assert "Docker" not in infra["tags"]
        assert "Helm" not in infra["tags"]

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

    def test_engineering_highlights_carry_into_page_two(self, tmp_path):
        # The strongest highlight (CI/CD) lands on page 1 under the experience
        # block; the rest continue on page 2 under a "(Continued)" heading, so no
        # highlight header is ever orphaned from its bullets.
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        assert "SELECTED ENGINEERING HIGHLIGHTS" in pages[0].upper()
        assert pages[1].upper().lstrip().startswith("SELECTED ENGINEERING HIGHLIGHTS (CONTINUED)")

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

    def test_additional_experience_rendered_as_its_own_section(self, tmp_path):
        # Earlier roles are split out of Professional Experience into a compressed
        # section so they establish the progression without eating resume space.
        cfg = load_config()
        pages = _extract_pdf_pages(cfg, tmp_path)
        blob = "\n".join(pages)
        assert "EARLIER EXPERIENCE" in blob.upper()
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

    def test_seo_meta_description_mentions_software_devops_automation(self):
        html_content = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        desc_match = re.search(r'<meta name="description" content="(.*?)">', html_content)
        assert desc_match
        desc = desc_match.group(1)
        assert "Software" in desc
        assert "DevOps" in desc
        assert "automation" in desc.lower()
        assert "Senior DevOps" not in desc
