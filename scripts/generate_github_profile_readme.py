"""Generate canonical GitHub profile README from resume.json."""

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOWLCIPHER_REPO = ROOT.parent / "howlcipher"

# Presentation focus mappings for profile display, grounded in canonical subtitles
CANONICAL_FOCUS_MAP = {
    "project-howlplane": "AI Engineering Control Plane",
    "project-howlproof": "Independent Software Verification",
    "project-howlframe": "Language & Compiler Runtime",
    "project-password-arena": "Defensive Security Arena",
    "project-howldream": "Experimental Evaluation Lab",
}


def render_readme(data):
    personal = data["personal"]
    canonical_base = data["seo"]["canonicalUrl"].rstrip("/")
    current_role = next((role for role in data["experience"] if role.get("id") == "exp-stellantis"), data["experience"][0])
    official_title = current_role["officialTitle"]
    company = current_role["company"]
    location = personal.get("location", "Michigan")

    projects_by_id = {p["id"]: p for p in data.get("projects", [])}

    # Core flagship repositories derived dynamically from canonical projects
    featured_order = [
        "project-howlplane",
        "project-howlproof",
        "project-howlframe",
        "project-password-arena",
        "project-howldream",
    ]

    rows = []
    for pid in featured_order:
        proj = projects_by_id.get(pid)
        if not proj:
            continue
        repo_name = proj["link"].rstrip("/").split("/")[-1]
        focus = CANONICAL_FOCUS_MAP.get(pid, proj.get("subtitle", "Engineering Project"))
        tech = ", ".join(proj.get("tags", [])[:3])
        highlights = " ".join(proj.get("highlights", []))
        rows.append(f"| **[{repo_name}]({proj['link']})** | {focus} | {tech} | {highlights} |")

    # william_elias portfolio row
    portfolio_highlights = "Accessible, multi-theme engineering portfolio with automated resume generation and 400+ deterministic verification tests."
    rows.append(f"| **[william_elias](https://github.com/howlcipher/william_elias)** | Portfolio & Build Tooling | Python, Playwright, HTML/CSS | {portfolio_highlights} |")
    project_table = "\n".join(rows)

    return f"""# {personal['name']}

**{personal['title']}** | Developer Productivity • Internal Tools • Defensive Security  
**Location:** {location} (Open to U.S. Remote Opportunities)

[Portfolio]({canonical_base}/) • [Software & Platform Resume (PDF)]({canonical_base}/William_Elias_Software_Platform_Resume.pdf) • [LinkedIn]({personal['linkedin']})

---

## Professional Focus

I am a Software & Automation Engineer specializing in developer productivity, internal operational tools, deployment safeguards, and defensive security tooling.

Currently, I serve as a **{official_title}** at {company}, where I build and maintain internal operational web platforms, preflight deployment drift checks, reusable Azure DevOps pipeline templates, and telemetry-driven diagnostic tooling.

---

## Core Engineering Repositories

| Repository | Focus | Technologies / Focus | Highlights |
| :--- | :--- | :--- | :--- |
{project_table}

---

## Technical Stack & Tooling

- **Languages:** Python (Asyncio, pytest), C# (.NET / ASP.NET Core), SQL (T-SQL), Go, Bash, PowerShell, JavaScript, HTML5/CSS3
- **Frameworks & Web:** ASP.NET Core Razor Pages, FastAPI, Flask, Playwright
- **Platforms & Systems:** Azure DevOps (Multi-stage YAML pipelines), SQL Server, SQLite, IIS, Linux, Git
- **Engineering Practices:** Preflight Drift Checks, Standardized Pipeline Templates, Deterministic Verification, Server-Specific File Safeguards

---

## Resumes & Contact

- **Personal Portfolio:** [{canonical_base}/]({canonical_base}/)
- **Software & Platform Engineering Resume:** [Download PDF]({canonical_base}/William_Elias_Software_Platform_Resume.pdf)
- **LinkedIn Profile:** [{personal['linkedin']}]({personal['linkedin']})
- **Direct Contact:** See portfolio contact links
"""


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub profile README from resume.json")
    parser.add_argument("--sync-repo", action="store_true", help="Synchronize output to sibling howlcipher repo if present")
    args = parser.parse_args()

    resume_path = ROOT / "resume.json"
    with open(resume_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    readme_content = render_readme(data)

    # 1. Write to documentation/github_profile_readme.md in william_elias
    target_doc = ROOT / "documentation" / "github_profile_readme.md"
    target_doc.parent.mkdir(parents=True, exist_ok=True)
    target_doc.write_text(readme_content, encoding="utf-8")
    print(f"Wrote {target_doc}")

    # 2. Write to sibling howlcipher repo if requested or flagged via environment
    should_sync = args.sync_repo or (os.environ.get("SYNC_PROFILE_REPO") == "1")
    if should_sync and HOWLCIPHER_REPO.exists() and HOWLCIPHER_REPO.is_dir():
        target_repo_readme = HOWLCIPHER_REPO / "README.md"
        target_repo_readme.write_text(readme_content, encoding="utf-8")
        print(f"Wrote {target_repo_readme}")


if __name__ == "__main__":
    main()
