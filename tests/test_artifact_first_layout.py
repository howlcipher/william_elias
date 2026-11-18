"""Approved information hierarchy: software artifacts first, metrics in context.

The site leads with professional software and explains the targeted resumes near the top.
"""
import html
import json
import re

import pytest

from scripts.generate_resume_pdf import SITE_DIR, load_config, load_variants


@pytest.fixture(scope="module")
def page():
    return (SITE_DIR / "index.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def cfg():
    return load_config()


def section(page, section_id):
    return page.split(f'id="{section_id}"')[1].split("</section>")[0]


def test_what_i_build_names_the_three_artifact_families_before_any_metric(page, cfg):
    build = section(page, "what-i-build")
    items = cfg["site"]["whatIBuild"]["items"]
    assert [item["programId"] for item in items] == cfg["site"]["selectedWork"]["featured"]
    for item in items:
        assert html.escape(item["name"]) in build
        for tech in item["stack"]:
            assert f"<span>{html.escape(tech)}</span>" in build
    assert "program-metrics" not in build


def test_what_i_build_cards_link_to_their_case_studies(page, cfg):
    program_ids = {p["id"] for p in cfg["selectedEngineeringPrograms"]}
    for item in cfg["site"]["whatIBuild"]["items"]:
        assert item["programId"] in program_ids
        assert f'href="#{item["programId"]}"' in page
        assert f'id="{item["programId"]}"' in page
        assert item["provenance"] == "Professional"


def test_selected_work_orders_every_program_once_with_software_first(cfg):
    work = cfg["site"]["selectedWork"]
    program_ids = [p["id"] for p in cfg["selectedEngineeringPrograms"]]
    assert sorted(work["order"]) == sorted(program_ids)
    assert work["order"][:3] == work["featured"] == [
        "program-internal-software", "program-cicd-release", "program-python-productivity"]


def test_selected_work_renders_in_site_order(page, cfg):
    positions = [page.index(f'id="{pid}"') for pid in cfg["site"]["selectedWork"]["order"]]
    assert positions == sorted(positions)


def test_every_headline_metric_stays_visible_inside_its_program(page, cfg):
    from scripts.build_html import render_programs

    program = next(p for p in cfg["selectedEngineeringPrograms"] if p["id"] == "program-cicd-release")
    stats = [{"value": "12", "label": "Example build checks", "sourceProgram": program["name"]}]
    markup = render_programs([program], {"wide": [program["id"]]}, stats)
    assert "<strong>12</strong>" in markup
    assert "Example build checks" in markup
    assert "program-metrics" not in page


def test_security_card_uses_the_standard_program_pattern(page, cfg):
    """Paired cards are title, body bullets, tags, and the disclosure — no hero stat."""
    card = page.split('id="program-security-remediation"')[1].split("</article>")[0]
    security = next(p for p in cfg["selectedEngineeringPrograms"] if p["id"] == "program-security-remediation")
    body = card.split("<details")[0]
    assert "program-metrics" not in card
    assert "program-context" not in card
    assert "<dt>" not in card
    for bullet in security["bullets"]:
        assert f"<li>{html.escape(bullet, quote=True)}</li>" in body
    assert 'class="skill-tags"' in card
    assert "Implementation &amp; validation" in card


def test_professional_and_independent_work_are_labelled(page, cfg):
    work = section(page, "programs")
    assert work.count('<p class="provenance-label">Professional</p>') == len(cfg["selectedEngineeringPrograms"])
    projects = section(page, "projects")
    label = cfg["site"]["projectsProvenanceLabel"]
    assert projects.count(f">{html.escape(label)}</p>") == len(cfg["projects"])
    assert "Independent" in label
    assert "Professional" not in projects.split('id="projects-target"')[1]


def test_current_role_links_to_selected_work_instead_of_repeating_case_studies(page, cfg):
    experience = section(page, "experience")
    summary = cfg["site"]["experienceSummaries"]["exp-stellantis"]
    assert html.escape(summary, quote=False) in experience
    assert 'href="#programs"' in experience
    current = cfg["experience"][0]
    for achievement in current["achievements"]:
        assert html.escape(achievement["text"], quote=False) not in experience
    for achievement in cfg["experience"][1]["achievements"]:
        assert html.escape(achievement["text"], quote=False) in experience


def test_two_primary_resume_paths_one_secondary_and_no_persona_switcher(page):
    variants = load_variants()["variants"]
    assert len(variants) == 3
    listing = {name: v.get("listing", "primary") for name, v in variants.items()}
    assert listing == {"software_platform": "primary", "security_automation": "primary",
                       "production_devops": "secondary"}
    hrefs = set(re.findall(r'data-resume-variant="([a-z_]+)"', page))
    assert hrefs == set(variants)
    # The hero offers only the two primary résumés.
    hero = page.split('id="hero-content-target"')[1].split("</header>")[0]
    assert set(re.findall(r'data-resume-variant="([a-z_]+)"', hero)) == {"software_platform", "security_automation"}
    for marker in ("data-persona", "role-switch", "persona-toggle", "site-mode"):
        assert marker not in page


def test_portfolio_note_links_the_source(page, cfg):
    note = section(page, "portfolio-build")
    assert cfg["personal"]["sourceRepo"] in note
    assert html.escape(cfg["site"]["portfolioNote"], quote=False) in note


def test_json_ld_keeps_the_official_job_title(page):
    block = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S).group(1)
    person = json.loads(block)["mainEntity"]
    assert person["jobTitle"] == "Senior Production Support Engineer"


def test_site_copy_contains_no_unsupported_scope_terms(cfg):
    site_text = json.dumps(cfg["site"]).lower()
    for term in ("kubernetes", "terraform", "aws", "gcp", "revenue", "roi",
                 "cost savings", "users", "adopted", "passionate", "results-driven", "rockstar"):
        assert term not in site_text, term


def test_restated_bullets_keep_every_number_visible_in_their_card(page, cfg):
    from scripts.build_html import render_programs

    program = {"id": "program-example", "name": "Example", "bullets": ["12 build checks"]}
    work = {
        "restatedBullets": {program["id"]: [0]},
        "context": {program["id"]: [{"label": "Verification", "text": "Ran 12 build checks"}]},
    }
    card = render_programs([program], work)
    assert "<li>12 build checks</li>" not in card
    assert "<dt>Verification</dt><dd>Ran 12 build checks</dd>" in card
