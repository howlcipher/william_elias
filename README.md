# William Elias

**Software & Automation Engineer**
Software Development • Developer Tooling • Security Automation • Platform Engineering
Open to U.S. Remote Opportunities

[Live Portfolio](https://howlcipher.github.io/william_elias/) · [Software Engineering & Developer Tools Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Software_Platform_Resume.pdf) · [Security Software & Automation Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Security_Automation_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

I build developer tools, internal applications, APIs, and automation that replace manual work with tested, maintainable software, in Python, Go, and C#/.NET. Security automation is a growing specialization: I am in the second year of an M.S. in Cyber Defense at Dakota State University, expected Winter 2027. Several years of production, infrastructure, and CI/CD work shape how I design software for the systems it runs on.

## Professional Work

At Stellantis Financial Services US (official title: Senior Production Support Engineer, promoted September 2026; résumé descriptor: Software & Automation):

* **Go self-service deployment CLI.** I designed and delivered a CLI that covers the build-to-rollback lifecycle: guided setup, project scaffolding, Azure DevOps REST integration, generated pipeline configuration, build/push/deploy, rollback, status, host auditing, and post-deployment verification.
* **.NET 8 Blazor internal application.** I built and maintain a modular C#/ASP.NET Core application on SQL Server and SQLite. It has per-module access policies, database-backed workflows, retained audit history, DBA approve-only deployment scripts, and live configuration diffing for pre-change review.
* **Python/FastAPI tooling.** This covers dashboards, Azure DevOps REST automation, failed-payload triage, scheduled query-to-email reporting, XML integration-log parsing, and a reusable operations CLI. I also standardized the team's Python tooling on uv.
* **Credential discovery and remediation.** I wrote Python tooling that scans source code and Git history for exposed credentials, plus Git-history remediation with BFG Repo-Cleaner across 100+ repositories (a scope separate from the CI/CD program). A measured scan processed 2,832 files and found 67 distinct exposed secrets in about 25 seconds.
* **CI/CD standardization.** The scope was a 60-repository, 104-application estate. I built the inventory, verification, and reusable pipeline templates, including 56 Azure DevOps build/release definitions across 28 standardized repositories. Builds passed in 27 of 28; dry runs validated representative deployment paths for 25 of 28.

| | |
|---|---|
| **60** | Repositories in CI/CD standardization scope |
| **104** | Applications inventoried for delivery standardization |
| **67** | Distinct exposed secrets identified/classified |

Earlier: DevOps Engineer (Python automation) at HBK, preceded by network and infrastructure engineering roles going back to 2015.

## Independent Projects

These are personal projects built outside employment with AI coding assistants, under my direction and review. None of them is an employer production system.

* **[HowlPlane](https://github.com/howlcipher/howlplane)**: a Python/Go engineering control plane. It routes work across coding agents, reconciles independent reviews, runs deterministic verification, and gates consequential actions behind human approval. It grew out of my earlier [AI Router](https://github.com/howlcipher/ai_router), a standalone coding-agent orchestrator that is the predecessor of HowlPlane's routing layer.
* **[HowlFrame](https://github.com/howlcipher/howlframe)**: an experimental language and toolchain written in Go. It has a lexer, parser, typed AST/IR, bytecode VM, WebAssembly target, and a capability-based security model enforced by the VM.
* **[Password Arena](https://github.com/howlcipher/password_arena)**: a synthetic-only attacker/defender simulation for password-strength experiments. It uses bounded budgets, reproducible test modes, CSPRNG generation, and audit reports, with pytest, mypy, and Ruff checks.
* Also: [Baseball Optimizer](https://github.com/howlcipher/baseball_optimizer) (Rust/Axum REST API) and [RedrawUS](https://github.com/howlcipher/redistricting-map) (geospatial data pipelines and an interactive map).

## What I'm Looking For

I'm looking for U.S. fully remote software engineering roles in these areas:

* developer tools and developer productivity
* security products and security automation
* internal tools
* platform software
* backend engineering

## Resumes

| Resume | Best for |
|---|---|
| [Software Engineering & Developer Tools](https://howlcipher.github.io/william_elias/William_Elias_Software_Platform_Resume.pdf) | Software, developer tools, internal tools, platform, and backend roles |
| [Security Software & Automation](https://howlcipher.github.io/william_elias/William_Elias_Security_Automation_Resume.pdf) | Security automation, security tooling, and development-focused DevSecOps roles |
| [Production & DevOps](https://howlcipher.github.io/william_elias/William_Elias_Production_DevOps_Resume.pdf) (secondary) | Production engineering, DevOps, CI/CD, and release engineering roles |

The older `William_Elias_Resume.pdf` URL still works. It is a byte-for-byte copy of the Production & DevOps resume.

---

## About This Repository

This repository is the source for the portfolio site and the PDF resumes. The site is static HTML, CSS, and vanilla JavaScript, published with GitHub Pages from `main`. `resume.json` is the only source of professional facts. `resume_variants.json` defines each resume as a selection of canonical items by ID. Python scripts generate `index.html`, the metadata, the social preview, the LinkedIn banner, and every PDF. Tests enforce evidence tracing, the two-page limit, ATS text extraction, accessibility, and freshness of every generated file.

To rebuild and test:

```bash
pip install -r requirements-dev.txt && playwright install chromium --with-deps   # Python 3.12; needs poppler-utils
python scripts/build_config.py && python scripts/build_html.py && python scripts/generate_resume_pdf.py && python scripts/generate_linkedin_banner.py
PYTHONPATH=. pytest tests/
```

See [documentation/ARCHITECTURE.md](documentation/ARCHITECTURE.md) for the data model, evidence boundaries, how to change facts or resume selections safely, and the full validation workflow.
