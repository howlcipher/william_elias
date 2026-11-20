"""Generate canonical GitHub profile README from resume.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOWLCIPHER_REPO = ROOT.parent / "howlcipher"


def render_readme(data):
    personal = data["personal"]
    canonical_base = data["seo"]["canonicalUrl"].rstrip("/")
    current_role = next((role for role in data["experience"] if role.get("id") == "exp-stellantis"), data["experience"][0])
    official_title = current_role["officialTitle"]
    company = current_role["company"]
    location = personal.get("location", "Michigan")

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

| Repository | Focus | Tech Stack | Highlights |
| :--- | :--- | :--- | :--- |
| **[howlplane](https://github.com/howlcipher/howlplane)** | AI Engineering Control Plane | Python, Go, JSONL | Coordinates coding-agent tasks and reviews with policy limits, repeatable verification, and human-in-the-loop authority boundaries. |
| **[howlproof](https://github.com/howlcipher/howlproof)** | Independent Software Verification | Python, Subprocess | Adversarial evaluation toolkit that tests local artifacts, captures reproducible evidence, and issues advisory verdicts. |
| **[howlframe](https://github.com/howlcipher/howlframe)** | Language & Compiler Runtime | Go, Python, HFIR, VM | Experimental compiler and toolchain in Go with typed intermediate representations, bytecode, and capability-bounded execution. |
| **[password_arena](https://github.com/howlcipher/password_arena)** | Defensive Security Arena | Python, zxcvbn, Cryptography | Local adversarial learning sandbox measuring password entropy progression, structural penalties, and attack budgets. |
| **[howldream](https://github.com/howlcipher/howldream)** | Experimental Evaluation Lab | Python, AST Analysis | Bounded architectural proposal engine evaluating divergent AI proposals and failure modes under inspectable conditions. |
| **[william_elias](https://github.com/howlcipher/william_elias)** | Portfolio & Build Tooling | Python, Playwright, HTML/CSS | Accessible, multi-theme engineering portfolio with automated resume generation and 400+ deterministic verification tests. |

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
    resume_path = ROOT / "resume.json"
    with open(resume_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    readme_content = render_readme(data)

    # 1. Write to documentation/github_profile_readme.md in william_elias
    target_doc = ROOT / "documentation" / "github_profile_readme.md"
    target_doc.parent.mkdir(parents=True, exist_ok=True)
    target_doc.write_text(readme_content, encoding="utf-8")
    print(f"Wrote {target_doc}")

    # 2. Write to howlcipher repo if it exists locally
    if HOWLCIPHER_REPO.exists() and HOWLCIPHER_REPO.is_dir():
        target_repo_readme = HOWLCIPHER_REPO / "README.md"
        target_repo_readme.write_text(readme_content, encoding="utf-8")
        print(f"Wrote {target_repo_readme}")


if __name__ == "__main__":
    main()
