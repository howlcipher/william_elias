import json
import re

import pypdf

from scripts.generate_resume_pdf import build, load_config, SITE_DIR


def _extract_pdf_text(cfg, tmp_path):
    out_pdf = tmp_path / "content_check.pdf"
    build(cfg, out_pdf)
    reader = pypdf.PdfReader(out_pdf)
    return "\n".join(page.extract_text() for page in reader.pages)


class TestResumeJsonValidity:
    def test_resume_json_is_valid_json(self):
        raw = (SITE_DIR / "resume.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        assert isinstance(data, dict)


class TestHeadlineAndPositioning:
    def test_headline_includes_devops_and_platform(self):
        cfg = load_config()
        title = cfg["personal"]["title"]
        assert "DevOps" in title
        assert "Platform" in title

    def test_headline_includes_production_support(self):
        cfg = load_config()
        assert "Production Support" in cfg["personal"]["title"]


class TestPipelineMetric:
    def test_summary_states_100_plus_pipelines_created(self):
        cfg = load_config()
        assert "100+ Azure DevOps pipelines" in cfg["summary"]
        assert "created" in cfg["summary"].lower()

    def test_summary_does_not_claim_all_pipelines_live(self):
        cfg = load_config()
        summary_lower = cfg["summary"].lower()
        assert re.search(r"\blive\b", summary_lower) is None
        assert "live production pipelines" not in summary_lower

    def test_no_outdated_four_live_pipelines_metric(self):
        cfg = load_config()
        blob = json.dumps(cfg).lower()
        assert "live ci/cd pipelines shipped" not in blob
        assert "four live" not in blob

    def test_three_defensible_metrics_present_in_stats(self):
        cfg = load_config()
        values = {s["value"] for s in cfg["stats"]}
        assert "100+" in values
        assert "40+ hrs" in values
        assert "60%" in values
        assert len(cfg["stats"]) == 3


class TestProductionSupportContent:
    def test_freshservice_rendered_in_skills(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        assert "Freshservice" in blob

    def test_sla_based_support_rendered(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        assert "SLA" in blob

    def test_oauth_and_iam_rendered(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        assert "OAuth" in blob
        assert "0Auth" not in blob
        assert "Identity and Access Management" in blob

    def test_azure_monitoring_stack_rendered(self):
        cfg = load_config()
        blob = json.dumps(cfg)
        for term in ("Azure Monitor", "Application Insights", "KQL"):
            assert term in blob

    def test_jira_rendered_outside_exclusively_ai_context(self):
        cfg = load_config()
        categories_with_jira = [
            s["category"] for s in cfg["skills"] if "Jira" in s.get("tags", [])
        ]
        assert categories_with_jira, "Jira should appear in at least one skill category"
        non_ai_categories = [c for c in categories_with_jira if "AI" not in c]
        assert non_ai_categories, "Jira must not be confined to an AI-only skill category"

    def test_networking_skills_rendered(self):
        cfg = load_config()
        networking = next(
            s for s in cfg["skills"] if s["category"] == "Infrastructure & Networking"
        )
        for term in ("Cisco", "Meraki", "VLANs", "Firewalls"):
            assert term in networking["tags"]

    def test_stellantis_section_has_production_support_and_monitoring(self):
        cfg = load_config()
        stellantis = next(
            j for j in cfg["experience"] if j["company"] == "Stellantis Financial Services"
        )
        bullets_blob = " ".join(stellantis["achievements"])
        assert "Freshservice" in bullets_blob
        assert "Azure Monitor" in bullets_blob
        assert "Application Insights" in bullets_blob


class TestNoUnsupportedClaims:
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


class TestPdfIncludesEarlierExperience:
    def test_additional_experience_present_in_pdf(self, tmp_path):
        cfg = load_config()
        text = _extract_pdf_text(cfg, tmp_path)
        assert "EARLIER TECHNICAL EXPERIENCE" in text.upper()
        for job in cfg["additionalExperience"]:
            assert job["company"] in text
            assert job["title"] in text

    def test_pdf_includes_100_plus_pipeline_metric(self, tmp_path):
        cfg = load_config()
        text = _extract_pdf_text(cfg, tmp_path)
        assert "100+ Azure DevOps pipelines" in text


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
        assert "Production Support" in html_content
