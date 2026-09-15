# William Elias

**DevOps, Software & Production Engineer**
Python • C#/.NET • Go • Azure DevOps • CI/CD • REST APIs
Open to U.S. Remote Opportunities

[Live Portfolio](https://howlcipher.github.io/william_elias/) · [Download Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

| | |
|---|---|
| **60** | Repositories in CI/CD standardization scope |
| **104** | Applications inventoried for delivery standardization |
| **67** | Distinct exposed secrets identified/classified |

---

## About This Repository

This is the source for the resume website above: a professional, modern, and highly performant resume site built with HTML, CSS, and vanilla JavaScript. It positions William for U.S. fully remote DevOps, Azure DevOps, Production Engineering, internal-tools/automation/backend software engineering, infrastructure automation, developer productivity, platform engineering, and security automation / DevSecOps roles.

## Confirmed Professional Content

The current content reflects an independent work-machine audit of internal professional repositories and supersedes the previous factual-correction pass.

**CI/CD standardization — verified scope:** 60 distinct repositories and 104 applications. William built inventory, verification, and reusable pipeline/template automation. Durable evidence includes 56 Azure DevOps build/release definitions across 28 standardized application repositories, 27/28 build verifications, 25/28 representative deployment-path dry runs, several latent delivery defects resolved, and 109 existing definitions reviewed/classified (95 legacy and 14 aligned).

**Security and credential remediation:** Python tooling scanned source code and Git history for exposed credentials, and BFG Repo-Cleaner was used to scrub historical records across 100+ repositories. A measured scan processed 2,832 files and identified 67 distinct exposed secrets in approximately 25 seconds; remediation records are complete.

**Deployment automation:** A Go-based self-service deployment CLI was designed and delivered, covering the build-to-rollback lifecycle with guided setup, Azure DevOps REST integration, generated pipeline configuration, host auditing, and automated post-deployment verification.

**Production-support and internal tooling:** An internal .NET 8 Blazor Web App using Interactive Server, C#, ASP.NET Core, SQL Server, and SQLite is built and maintained for production support. It has per-module access policies, database-backed workflows, retained audit history, DBA approve-only deployment scripts, live configuration/object diffing, pre-change/pre-CAB visibility, and service-desk request tracking. Separate Python/FastAPI dashboards and operational tooling remain distinct from the portal. Auth0/OAuth/OIDC/IAM troubleshooting is professional identity experience, not Azure identity architecture ownership.

**Security / backend:** A scoped OAuth 2.1 resource server integrates an enterprise AI assistant with internal engineering documentation, including JWT/JWKS validation, content allowlisting, and explicit `alg=none` token-bypass defenses.

**Container and infrastructure modernization:** A zero-disk-secret Blazor Web App container migration proof of concept was designed with fail-fast secret validation, database-connectivity health checks, and IIS-fronted container hosting. Server/container migration paths were investigated and disaster-recovery pipeline definitions were audited to identify broken or obsolete deployment paths and support remediation planning. No completed production server migration or zero-downtime DR cutover is claimed.

The current role is **Production Support Engineer | DevOps & Automation**, with the latter a résumé descriptor, in **Auburn Hills, MI · Hybrid**. Remote availability describes the desired next role. Additional Technical Foundations covers academic/project Java, Kotlin, Android Development, Digital Forensics, FTK Imager, EnCase, and Wireshark, without implying professional forensics employment.

Treat this canonical general portfolio and résumé as complete after the factual-correction publication checks. Future content changes should follow new real experience or a specific target role. See the [current handoff](documentation/portfolio_optimization_handoff.md) for provenance and validation. The [evidence manifest](documentation/portfolio_optimization_evidence.json) records 231 passing tests, two-page PDF inspection, 20 viewport/theme checks, and byte-identical live artifact verification following publication in PR #10.

## Deployment & Architecture
- **Data Source**: A single `resume.json` acts as the canonical source of truth for all content, including the `seo` block (canonical URL, OG/Twitter site name, curated `knowsAbout` list) used for structured data.
- **Generated Assets**: Python scripts generate `config.js`, `index.html`, `robots.txt`, `sitemap.xml`, `preview.jpg`, and `William_Elias_Resume.pdf` from `resume.json`. `scripts/build_html.py` reads the source layout in `scripts/site_template.html` and generates body content, metadata, structured data, and the 1200 × 630 social preview using the existing portrait. Edit the template for structural HTML changes; never use the generated page as the template. The PDF retains 10-point body text, clickable links, and all three engineering highlights together on page two.
- **Website vs. PDF**: The two artifacts are deliberately different. The website shows breadth; the PDF is selective. `experience` renders as "Professional Experience" while `additionalExperience` gets its own compressed "Earlier Experience" section further down the PDF. `selectedEngineeringPrograms` (eight entries) is **website-only**; the PDF instead renders `pdfEngineeringHighlights`, a curated three-entry condensation, under "Selected Engineering Highlights". All `projects` appear on the website, but only those with `pdfInclude: true` reach the PDF's "Selected Open-Source Engineering" section. Core Expertise shows every tag on the website. The PDF uses an explicit `skills[].pdfTags` selection when present (a non-empty unique subset of the website tags), otherwise the leading `PDF_SKILL_TAG_LIMIT` tags; a skill category can also carry `pdfInclude: false` to stay website-only entirely (the same idiom, applied to `skills` instead of `projects`), which keeps "Additional Technical Foundations" website-only. Software & Backend includes website basics while its PDF selection prioritizes recruiter-relevant Python/FastAPI and C#/.NET/Blazor backend skills.
- **Experience Qualifiers**: Website skill cards show `skills[].context`. Optional `skills[].pdfContext` is a non-empty string rendered in parentheses beside the PDF category, before its tags. Keep it compact: AI tooling is qualified as "Internal tools & projects" and Automation as "Python/PowerShell professionally; Go in projects". Omit the field when no extra qualifier is needed; do not substitute project or proof-of-concept work for professional production experience. GitHub Actions remains explicitly project experience in its tag.
- **Section Order**: Hero → metrics → About → Engineering Impact → Professional Experience (including Earlier Experience) → Open Source → Core Expertise → Education → Contact.
- **Deployment**: Deployed via classic GitHub Pages (serving directly from the `main` branch).
- **CI/CD**: GitHub Actions verify tests and ensure that the generated assets are fresh, but CI does not mutate the repository or push commits.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `resume.json` file. No need to touch HTML!
- **Engineering Impact**: Eight professional programs lead with outcomes; native expandable "Implementation & validation" disclosures retain detailed evidence, validation counts, and shared-ownership qualifications. They work with keyboard controls and without JavaScript.
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Readable Role Title**: A dedicated dark-theme text color keeps the small mobile role title above 4.5:1 contrast while retaining the existing decorative accent colors.
- **Mobile Responsive**: Custom hamburger menu and flexible layout, including a hero photo that reflows between the tagline and contact actions on narrow viewports instead of trailing the whole hero.
- **Print/PDF Download**: Embedded download link for the PDF version.
- **Persistent Resume CTA**: A distinct "Resume" action lives in both the desktop navbar and the mobile menu, so it's reachable after scrolling past the hero.
- **Recruiter Contact CTA**: A focused "Open to U.S. Remote Opportunities" section before the footer surfaces Email/LinkedIn/Resume/GitHub actions, generated from `resume.json`.
- **Scroll-Aware Navigation**: An `IntersectionObserver`-based active state highlights the nav link for the section currently in view (`aria-current="page"` plus a non-color underline indicator).
- **SEO / Structured Data**: Canonical link, complete OG/Twitter metadata, and a generated JSON-LD `ProfilePage`/`Person` block, plus a generated `robots.txt` and `sitemap.xml`.
- **Terminal-Style Intro**: One-time CSS typewriter reveal on the tagline (respects `prefers-reduced-motion`).
- **Live "Last Synced" Widget**: Footer pulls the latest commit from the GitHub API and shows it as a relative timestamp + short SHA. Cached in localStorage for 10 minutes to stay polite to GitHub's unauthenticated rate limit.

## How to Update Your Information

All your information is stored in the canonical `resume.json` file. Do not manually edit generated artifacts. Use `scripts/site_template.html` for layout changes and `style.css` / `script.js` for styling and interactions.

1. Open `resume.json` in any text editor and update your information.
2. Regenerate the derived files by running the build sequence:
   ```bash
   python scripts/build_config.py
   python scripts/build_html.py
   python scripts/generate_resume_pdf.py
   ```
   *(Note: This requires development dependencies, see below)*
3. Verify your changes and run the automated tests.
4. Update `README.md` and `change_log.md`, review the diff, and make a signed conventional commit including all generated outputs. Publishing to `main` is a separate deployment action. CI checks freshness without modifying or committing files.

### Adding a New Job
Find the `experience` array in `resume.json` and add a new object to the top of the list:

```json
{
    "date": "March 2026 - Present",
    "title": "Senior Security Engineer",
    "company": "New Company Inc.",
    "location": "Remote",
    "achievements": [
        "First bullet point goes here.",
        "Second bullet point goes here."
    ]
}
```

Professional depth beyond the `experience` entries lives in `selectedEngineeringPrograms`, rendered as "Engineering Impact" using each entry's `bullets` and optional expandable `details`. To change the PDF's curated evidence, edit `pdfEngineeringHighlights`. Each headline metric and PDF highlight identifies its `sourceProgram`; tests verify numerical claims against that specific program. Preserve scope, dry-run, co-led, and contributed qualifications; avoid dynamic deployment/adoption counts. Open-source/personal work lives in `projects`; the PDF currently selects HowlPlane and RedrawUS via `pdfInclude: true`. The website AI capability stack comes from `aiEngineeringCapabilities`.

## Local Development & Validation

Since this is a static site, you can view it locally by simply double-clicking `index.html` in your browser.

Before committing your changes, you should validate them end-to-end to ensure config validity, fresh generated files, and passing tests. Run the following sequence in your terminal from the project root:

```bash
# 1. Use Python 3.12, matching CI, and install pinned dependencies
python3.12 -m venv /tmp/william-elias-venv
source /tmp/william-elias-venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium --with-deps

# 2. Rebuild all derived files
python scripts/build_config.py && python scripts/build_html.py && python scripts/generate_resume_pdf.py

# 3. Run the test suite
PYTHONPATH=. pytest tests/
```

The suite builds all six artifacts in two independent temporary directories containing only source inputs. It checks both checked-in freshness and byte-for-byte repeatability, including PDF and social preview, without rewriting the working tree. Navigation tests wait up to five seconds for the requested scroll position and active state while preserving smooth scrolling.

Also render and inspect both PDF pages and review the website at 320, 390, 810, 1024, and 1440 pixels across dark, light, and both contrast modes before publishing. The full suite uses Chromium; other browser engines are not covered. See [the optimization handoff](documentation/portfolio_optimization_handoff.md) for the latest validation evidence, reviewer perspectives, environment limitations, and deferred work.
