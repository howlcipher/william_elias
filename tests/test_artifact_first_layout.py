"""Approved information hierarchy: software artifacts first, metrics in context.

The site leads with what William builds, keeps every operational metric but
places it inside the engineering work it describes, separates professional
from independent work, and explains the two targeted resumes near the top.
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
    for name in ("Self-Service Deployment CLI", "Internal Production-Support Software",
                 "Python Developer &amp; Operations Tooling"):
        assert name in build
    for tech in ("Go", ".NET 8", "Blazor", "Python", "FastAPI"):
        assert f"<span>{html.escape(tech)}</span>" in build
    # Headline figures (the wide CI/CD card) stay below What I Build. The
    # credential count is a normal bullet on its card, not a <strong> figure.
    figure_values = [s["value"] for s in cfg["stats"] if f"<strong>{s['value']}</strong>" in page]
    assert {"60", "104"} <= set(figure_values)
    first_metric = min(page.index(f"<strong>{value}</strong>") for value in figure_values)
    assert page.index('id="what-i-build"') < first_metric


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
        "program-deployment-tooling", "program-internal-software", "program-python-productivity"]


def test_selected_work_renders_in_site_order(page, cfg):
    positions = [page.index(f'id="{pid}"') for pid in cfg["site"]["selectedWork"]["order"]]
    assert positions == sorted(positions)


def test_every_headline_metric_stays_visible_inside_its_program(page, cfg):
    programs = {p["name"]: p["id"] for p in cfg["selectedEngineeringPrograms"]}
    wide = set(cfg["site"]["selectedWork"]["wide"])
    for stat in cfg["stats"]:
        program_id = programs[stat["sourceProgram"]]
        card = page.split(f'id="{program_id}"')[1].split("</article>")[0]
        assert stat["value"] in card
        if program_id in wide:
            assert f"<strong>{stat['value']}</strong>" in card
            assert html.escape(stat["label"]) in card
        else:
            assert "program-metrics" not in card


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


def test_cicd_context_lines_keep_units_and_qualifiers(cfg):
    lines = {line["label"]: line["text"] for line in cfg["site"]["selectedWork"]["context"]["program-cicd-release"]}
    assert set(lines) == {"Scope", "Implementation", "Verification"}
    assert "60" in lines["Scope"] and "104" in lines["Scope"]
    assert re.search(r"60[- ]repositor", lines["Scope"]) and re.search(r"104[- ]application", lines["Scope"])
    assert "56" in lines["Implementation"] and "28" in lines["Implementation"]
    verification = lines["Verification"].lower()
    assert "dry-run" in verification and "representative" in verification
    assert "25 of 28" in verification and "deployment paths" in verification
    assert "27" in verification
    # Dry-run validation must never read as deployment.
    assert not re.search(r"\bdeployed\b|\bin production\b", verification)


def test_credential_scan_stays_a_body_bullet(cfg):
    security = next(p for p in cfg["selectedEngineeringPrograms"] if p["id"] == "program-security-remediation")
    bullet = next(b for b in security["bullets"] if "2,832" in b)
    for fact in ("2,832 files", "67 distinct exposed secrets", "approximately 25 seconds"):
        assert fact in bullet
    work = cfg["site"]["selectedWork"]
    assert "program-security-remediation" not in work.get("context", {})
    assert "program-security-remediation" not in work.get("restatedBullets", {})


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


def test_exactly_two_resume_paths_and_no_persona_switcher(page):
    variants = load_variants()["variants"]
    assert len(variants) == 2
    hrefs = set(re.findall(r'data-resume-variant="([a-z_]+)"', page))
    assert hrefs == set(variants)
    for marker in ("data-persona", "role-switch", "persona-toggle", "site-mode"):
        assert marker not in page


def test_portfolio_note_links_the_source(page, cfg):
    note = section(page, "portfolio-build")
    assert cfg["personal"]["sourceRepo"] in note
    assert html.escape(cfg["site"]["portfolioNote"], quote=False) in note


def test_json_ld_keeps_the_official_job_title(page):
    block = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S).group(1)
    person = json.loads(block)["mainEntity"]
    assert person["jobTitle"] == "Production Support Engineer"


def test_site_copy_contains_no_unsupported_scope_terms(cfg):
    site_text = json.dumps(cfg["site"]).lower()
    for term in ("kubernetes", "terraform", "aws", "gcp", "razor pages", "revenue", "roi",
                 "cost savings", "users", "adopted", "passionate", "results-driven", "rockstar"):
        assert term not in site_text, term


def test_restated_bullets_keep_every_number_visible_in_their_card(page, cfg):
    programs = {p["id"]: p for p in cfg["selectedEngineeringPrograms"]}
    for program_id, indices in cfg["site"]["selectedWork"]["restatedBullets"].items():
        assert cfg["site"]["selectedWork"]["context"][program_id], program_id
        card = page.split(f'id="{program_id}"')[1].split("</article>")[0]
        for index in indices:
            bullet = programs[program_id]["bullets"][index]
            assert f"<li>{html.escape(bullet, quote=True)}</li>" not in card.split("<details")[0]
            for number in re.findall(r"\d[\d,]*", bullet):
                assert number in card, (program_id, number)
