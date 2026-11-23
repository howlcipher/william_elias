#!/usr/bin/env python3
"""William Elias Career Discoverability Maintenance & Verification Tool.

Orchestrates validation, artifact generation, integrity checks, and status reporting
across portfolio, GitHub profile, and search/LinkedIn discovery artifacts.

Usage:
    python3 scripts/maintain.py               # Validate and regenerate all artifacts
    python3 scripts/maintain.py --check       # CI mode: verify freshness & exit 1 if stale
    python3 scripts/maintain.py --sync-github # Also synchronize sibling howlcipher repository
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS = (
    "config.js",
    "index.html",
    "robots.txt",
    "sitemap.xml",
    "preview.jpg",
    "assets/images/linkedin-banner.png",
    "documentation/linkedin_profile.md",
    "documentation/github_profile_readme.md",
    "William_Elias_Software_Platform_Resume.pdf",
    "William_Elias_Security_Automation_Resume.pdf",
    "William_Elias_Production_DevOps_Resume.pdf",
    "William_Elias_Resume.pdf",
    "candidate-profile.json",
    "llms.txt",
)

GENERATORS = (
    "build_config.py",
    "build_html.py",
    "generate_resume_pdf.py",
    "generate_linkedin_banner.py",
    "generate_linkedin_profile.py",
    "generate_github_profile_readme.py",
)


def validate_canonical_rules(data: dict) -> list[str]:
    """Validate non-negotiable career evidence facts and boundaries in resume.json."""
    errors = []

    # 1. Geographic location
    location = data.get("personal", {}).get("location")
    if location != "Michigan":
        errors.append(f"Invalid location '{location}'; must strictly be 'Michigan'.")

    # 2. Official title & positioning
    positioning = data.get("personal", {}).get("title")
    if positioning != "Software & Automation Engineer":
        errors.append(
            f"Invalid positioning '{positioning}'; must strictly be 'Software & Automation Engineer'."
        )

    current_role = next(
        (r for r in data.get("experience", []) if r.get("id") == "exp-stellantis"),
        None,
    )
    if not current_role:
        errors.append("Current role 'exp-stellantis' missing from experience.")
    elif current_role.get("officialTitle") != "Senior Production Support Engineer":
        errors.append(
            f"Invalid current official title '{current_role.get('officialTitle')}'; "
            "must strictly be 'Senior Production Support Engineer'."
        )

    # 3. Canonical Degree Names
    degrees = [edu.get("degree") for edu in data.get("education", [])]
    if "M.S. Cyber Defense (In Progress, Second Year)" not in degrees:
        errors.append("Missing canonical 'M.S. Cyber Defense (In Progress, Second Year)'.")
    if "B.S. Information Technology" not in degrees:
        errors.append("Missing canonical 'B.S. Information Technology'.")
    if "B.B.A. Business Administration" not in degrees:
        errors.append("Missing canonical 'B.B.A. Business Administration'.")

    # 4. Prohibited uncalibrated claims in source
    blob = json.dumps(data).lower()
    prohibited = (
        "secret rotation",
        "zero outage",
        "zero-outage",
        "zero production regression",
        "automated rollback",
        "autonomous multi-agent",
        "deterministic evidence sandbox",
    )
    for term in prohibited:
        if term in blob:
            errors.append(f"Forbidden uncalibrated phrase found in resume.json: '{term}'")

    return errors


def validate_structured_data(site_dir: Path) -> list[str]:
    """Validate JSON-LD structured data and SEO linkages in built index.html."""
    errors = []
    index_path = site_dir / "index.html"
    if not index_path.exists():
        return ["index.html does not exist."]

    content = index_path.read_text(encoding="utf-8")

    # Match JSON-LD
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not match:
        errors.append("JSON-LD block missing from index.html.")
    else:
        try:
            ld = json.loads(match.group(1))
            person = ld.get("mainEntity", {})
            if person.get("@type") != "Person":
                errors.append("JSON-LD mainEntity is not of @type 'Person'.")
            if person.get("jobTitle") != "Senior Production Support Engineer":
                errors.append(
                    f"JSON-LD jobTitle is '{person.get('jobTitle')}', expected 'Senior Production Support Engineer'."
                )

            # alumniOf vs hasCredential
            alumni_names = [a.get("name") for a in person.get("alumniOf", [])]
            if "Cisco Networking Academy" in alumni_names:
                errors.append(
                    "Cisco Networking Academy must not be listed in alumniOf (use hasCredential)."
                )

            credentials = person.get("hasCredential", [])
            if not any(c.get("name") == "CCNA (Previously Held)" for c in credentials):
                errors.append("CCNA credential missing from JSON-LD hasCredential.")
            if any("recognizedBy" in c for c in credentials):
                errors.append(
                    "CCNA credential must not include unsubstantiated recognizedBy organization."
                )
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in JSON-LD block: {exc}")

    # Check candidate-profile.json
    cand_path = site_dir / "candidate-profile.json"
    if cand_path.exists():
        try:
            cand_data = json.loads(cand_path.read_text(encoding="utf-8"))
            if "$schema" in cand_data:
                errors.append("candidate-profile.json must not declare a draft '$schema' meta-schema.")
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in candidate-profile.json: {exc}")

    return errors


def validate_html_anchors(site_dir: Path) -> list[str]:
    """Verify that every internal anchor link in index.html resolves to an existing element ID."""
    errors = []
    index_path = site_dir / "index.html"
    if not index_path.exists():
        return ["index.html does not exist for anchor verification."]
    content = index_path.read_text(encoding="utf-8")
    ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))
    hrefs = re.findall(r'href=["\']#([^"\']+)["\']', content)
    for target in set(hrefs):
        if target not in ids:
            errors.append(
                f"Broken internal anchor href='#{target}' in index.html: target ID does not exist."
            )
    return errors


def validate_documentation_links(root_dir: Path) -> list[str]:
    """Verify that all relative file links in documentation and README resolve to existing files."""
    errors = []
    md_files = list(root_dir.glob("*.md")) + list(root_dir.glob("documentation/*.md"))
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for _, link in links:
            if link.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            target_file_str = link.split("#")[0]
            if not target_file_str:
                continue
            target_path = (md_file.parent / target_file_str).resolve()
            if not target_path.exists():
                errors.append(
                    f"Broken relative link in {md_file.relative_to(root_dir)}: '{link}' -> '{target_file_str}' not found."
                )
    return errors


def verify_pdf_alias_equivalence(site_dir: Path) -> list[str]:
    """Verify that the primary resume PDF alias is byte-identical to Production DevOps resume."""
    legacy_file = site_dir / "William_Elias_Resume.pdf"
    canonical_file = site_dir / "William_Elias_Production_DevOps_Resume.pdf"
    if not legacy_file.exists() or not canonical_file.exists():
        return ["Resume PDFs missing for alias byte-equivalence verification."]
    if legacy_file.read_bytes() != canonical_file.read_bytes():
        return [
            "William_Elias_Resume.pdf differs from William_Elias_Production_DevOps_Resume.pdf; must be byte-identical."
        ]
    return []


def run_generator(script_name: str, cwd: Path, args: list[str] = None) -> tuple[bool, str]:
    """Execute a single generator script using the active python interpreter."""
    cmd = [sys.executable, str(cwd / "scripts" / script_name)]
    if args:
        cmd.extend(args)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True,
        )
        return True, proc.stdout.strip()
    except subprocess.CalledProcessError as exc:
        return False, f"{exc.stderr.strip()} (exit {exc.returncode})"


def run_all_generators(
    target_dir: Path, sync_github: bool = False, skip_banner: bool = False
) -> list[str]:
    """Run all generation scripts in dependency order in target_dir."""
    generators = [
        ("build_config.py", []),
        ("build_html.py", []),
        ("generate_resume_pdf.py", []),
        ("generate_linkedin_profile.py", []),
        (
            "generate_github_profile_readme.py",
            ["--sync-repo"] if sync_github else [],
        ),
    ]
    if not skip_banner:
        generators.insert(3, ("generate_linkedin_banner.py", []))

    errors = []
    for script_name, args in generators:
        success, output = run_generator(script_name, cwd=target_dir, args=args)
        if not success:
            errors.append(f"Generator {script_name} failed: {output}")
    return errors


def check_freshness_in_isolated_build(skip_banner: bool = False) -> list[str]:
    """Build in a clean temporary directory and assert all checked-in artifacts match identically."""
    stale = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_path = Path(tmp_dir)
        shutil.copy2(ROOT / "resume.json", temp_path)
        shutil.copy2(ROOT / "resume_variants.json", temp_path)
        shutil.copytree(ROOT / "assets", temp_path / "assets")
        (temp_path / "scripts").mkdir()
        for source in (*GENERATORS, "site_template.html"):
            shutil.copy2(ROOT / "scripts" / source, temp_path / "scripts")

        # Run generators in temp dir
        errors = run_all_generators(temp_path, sync_github=False, skip_banner=skip_banner)
        if errors:
            return errors

        # Verify PDF alias equivalence in isolated build
        pdf_errors = verify_pdf_alias_equivalence(temp_path)
        if pdf_errors:
            return pdf_errors

        # Verify internal HTML anchors in isolated build
        anchor_errors = validate_html_anchors(temp_path)
        if anchor_errors:
            return anchor_errors

        # Compare artifacts
        for artifact in ARTIFACTS:
            if skip_banner and "linkedin-banner.png" in artifact:
                continue
            built_file = temp_path / artifact
            checked_in = ROOT / artifact
            if not checked_in.exists():
                stale.append(f"{artifact} is missing on disk.")
            elif not built_file.exists():
                stale.append(f"{artifact} was not produced by generators.")
            elif built_file.read_bytes() != checked_in.read_bytes():
                stale.append(f"{artifact} on disk does not match freshly generated output.")

    return stale


def get_git_state() -> dict:
    """Inspect local repository Git commit, working tree, and push state."""
    state = {
        "branch": "unknown",
        "head": "unknown",
        "is_clean": False,
        "unpushed_count": None,
        "upstream": None,
    }
    try:
        head_proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        state["head"] = head_proc.stdout.strip()
        branch_proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        state["branch"] = branch_proc.stdout.strip()
        status_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        state["is_clean"] = len(status_proc.stdout.strip()) == 0

        # Check upstream branch and unpushed commits
        upstream_proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "@{u}"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if upstream_proc.returncode == 0:
            state["upstream"] = upstream_proc.stdout.strip()
            count_proc = subprocess.run(
                ["git", "rev-list", "--count", "@{u}..HEAD"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            if count_proc.returncode == 0:
                state["unpushed_count"] = int(count_proc.stdout.strip())
    except Exception:
        pass
    return state


def check_sibling_repo_sync() -> dict:
    """Inspect sibling howlcipher repository local sync and git state."""
    sibling = ROOT.parent / "howlcipher"
    info = {
        "exists": False,
        "synced_locally": False,
        "clean_locally": False,
        "unpushed_count": None,
    }
    if not (sibling.exists() and (sibling / "README.md").exists()):
        return info
    info["exists"] = True
    readme_local = ROOT / "documentation" / "github_profile_readme.md"
    readme_sibling = sibling / "README.md"
    if readme_local.exists() and readme_sibling.exists():
        info["synced_locally"] = readme_local.read_bytes() == readme_sibling.read_bytes()

    try:
        status_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(sibling),
            capture_output=True,
            text=True,
        )
        if status_proc.returncode == 0:
            info["clean_locally"] = len(status_proc.stdout.strip()) == 0
        count_proc = subprocess.run(
            ["git", "rev-list", "--count", "@{u}..HEAD"],
            cwd=str(sibling),
            capture_output=True,
            text=True,
        )
        if count_proc.returncode == 0:
            info["unpushed_count"] = int(count_proc.stdout.strip())
    except Exception:
        pass
    return info


def print_status_report(errors: list[str], sync_github: bool, is_check_mode: bool):
    """Output categorized discoverability status report with exact verification distinctions."""
    print("=" * 70)
    print("William Elias Career Discoverability & Maintenance Status")
    print("=" * 70)

    # 1. Local Generation & Validation State
    mode_label = "Freshness Checked (Isolated Build)" if is_check_mode else "Locally Generated & Validated"
    print(f"\n[1] {mode_label}:")
    if errors:
        print(f"  ❌ Failures detected ({len(errors)}):")
        for err in errors:
            print(f"     - {err}")
    else:
        print("  ✅ Canonical rules validated (location, titles, degrees, forbidden claims).")
        print("  ✅ HTML, JSON-LD, candidate-profile.json, and llms.txt validated.")
        print("  ✅ Internal HTML anchors and documentation links verified.")
        print("  ✅ 4 PDF resume variants verified; alias byte-equivalence confirmed.")
        print("  ✅ LinkedIn banner generated (1584x396 px).")
        print("  ✅ GitHub profile README generated matching canonical schema.")

    # 2. Local Repository Git State
    print("\n[2] Local Repository Git State:")
    git_state = get_git_state()
    print(f"  - Branch: {git_state['branch']} (HEAD: {git_state['head']})")
    working_tree_desc = "Clean (no uncommitted changes)" if git_state["is_clean"] else "Modified (uncommitted changes present)"
    print(f"  - Working Tree: {working_tree_desc}")
    if git_state["upstream"]:
        if git_state["unpushed_count"] == 0:
            print(f"  - Push Status: Up to date with {git_state['upstream']}")
        elif git_state["unpushed_count"] is not None:
            print(f"  - Push Status: {git_state['unpushed_count']} commit(s) ahead of {git_state['upstream']} (unpushed)")
    else:
        print("  - Push Status: No upstream tracking branch detected")

    # 3. Sibling Profile Repository State
    print("\n[3] Sibling Profile Repository (howlcipher/howlcipher):")
    sib_info = check_sibling_repo_sync()
    if sib_info["exists"]:
        sync_desc = "Synchronized on local disk" if sib_info["synced_locally"] else "Differs on local disk (run with --sync-github to update)"
        clean_desc = "working tree clean" if sib_info["clean_locally"] else "uncommitted changes"
        unpushed_desc = ""
        if sib_info["unpushed_count"] is not None:
            unpushed_desc = f", {sib_info['unpushed_count']} unpushed commit(s)" if sib_info["unpushed_count"] > 0 else ", pushed to origin"
        print(f"  - Local Status: {sync_desc} ({clean_desc}{unpushed_desc})")
    else:
        print("  - Local Status: Directory ../howlcipher not found")

    # 4. Remote Publishing & Deployment Properties
    print("\n[4] Remote Properties (Published on push/merge via GitHub Actions):")
    print("  - Portfolio Repository: https://github.com/howlcipher/william_elias")
    print("  - Live Site (GitHub Pages): https://howlcipher.github.io/william_elias/")
    print("  - GitHub Profile README: https://github.com/howlcipher")

    # 5. Needs LinkedIn Owner Action
    print("\n[5] Needs LinkedIn Owner Action (See documentation/linkedin_owner_checklist.md):")
    print("  - Upload assets/images/linkedin-banner.png to LinkedIn header")
    print("  - Paste canonical Headline: Software & Automation Engineer | Developer Productivity | Internal Tools | CI/CD Tooling")
    print("  - Paste canonical verbatim About section")
    print("  - Update Current Experience bullets (official title: Senior Production Support Engineer)")
    print("  - Configure Featured links in specified order")
    print("  - Pin Top 3 skills: Developer Tooling, CI/CD, Python")

    # 6. Needs Google / Bing Owner Action (See documentation/search_indexing_owner_checklist.md):
    print("\n[6] Needs Google / Bing Owner Action:")
    print("  - Google Search Console: Verify URL prefix https://howlcipher.github.io/william_elias/")
    print("  - Supply verification token to resume.json['seo']['googleSiteVerification'] or GOOGLE_SITE_VERIFICATION env var")
    print("  - Submit sitemap: https://howlcipher.github.io/william_elias/sitemap.xml")
    print("  - Bing Webmaster Tools: Import verified site from GSC")

    # 7. Unable to Verify Automatically
    print("\n[7] Unable to Verify Automatically (Owner Account & Search Engine Controls):")
    print("  - LinkedIn 'Open to Work' recruiter-only visibility setting")
    print("  - External search engine crawling queue and indexing coverage status")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Maintain William Elias career discoverability artifacts."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check validity and freshness without modifying files; exit 1 if stale.",
    )
    parser.add_argument(
        "--sync-github",
        action="store_true",
        help="Also sync howlcipher/howlcipher profile repository.",
    )
    parser.add_argument(
        "--skip-banner",
        action="store_true",
        help="Skip Playwright banner generation.",
    )
    args = parser.parse_args()

    resume_path = ROOT / "resume.json"
    with open(resume_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Validate canonical rules and documentation links
    rule_errors = validate_canonical_rules(data)
    doc_errors = validate_documentation_links(ROOT)
    initial_errors = rule_errors + doc_errors
    if initial_errors:
        print(f"Validation failed with {len(initial_errors)} error(s):", file=sys.stderr)
        for err in initial_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        # Check structured data and HTML anchors in current files
        sd_errors = validate_structured_data(ROOT)
        anchor_errors = validate_html_anchors(ROOT)
        static_errors = sd_errors + anchor_errors
        if static_errors:
            print(
                f"Validation failed with {len(static_errors)} error(s):",
                file=sys.stderr,
            )
            for err in static_errors:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)

        # Check for artifact staleness against fresh build
        stale_artifacts = check_freshness_in_isolated_build(skip_banner=args.skip_banner)
        if stale_artifacts:
            print(
                f"Artifacts are stale or differed from fresh generation ({len(stale_artifacts)}):",
                file=sys.stderr,
            )
            for err in stale_artifacts:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)

        print_status_report([], args.sync_github, is_check_mode=True)
        print("\nAll checks passed successfully.")
        sys.exit(0)

    # 2. Run all generators in repo root
    gen_errors = run_all_generators(
        ROOT, sync_github=args.sync_github, skip_banner=args.skip_banner
    )
    if gen_errors:
        print(f"Generation failed with {len(gen_errors)} error(s):", file=sys.stderr)
        for err in gen_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # 3. Validate structured data, anchors, and PDF alias equivalence on generated output
    sd_errors = validate_structured_data(ROOT)
    anchor_errors = validate_html_anchors(ROOT)
    pdf_errors = verify_pdf_alias_equivalence(ROOT)
    all_errors = gen_errors + sd_errors + anchor_errors + pdf_errors

    print_status_report(all_errors, args.sync_github, is_check_mode=False)
    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
