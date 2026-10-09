# William Elias

**Software & Automation Engineer**
Developer Tooling • Platform Engineering • CI/CD • Production Engineering
Open to U.S. Remote Opportunities

[Live Portfolio](https://howlcipher.github.io/william_elias/) · [Software & Platform Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Software_Platform_Resume.pdf) · [Production & DevOps Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Production_DevOps_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

| | |
|---|---|
| **60** | Repositories in CI/CD standardization scope |
| **104** | Applications inventoried for delivery standardization |
| **67** | Distinct exposed secrets identified/classified |

---

## About This Repository

This is the source for the portfolio website above and William's résumés: a fast static site built with HTML, CSS, and vanilla JavaScript, plus two targeted PDF résumés generated from the same data.

The architecture is **one person → one canonical evidence base → one broad website → two targeted résumé views**:

* **One canonical website.** The site is William's general professional profile. It presents him as a **Software & Automation Engineer** who builds software, automation, developer tools, delivery systems, and production engineering systems that make software easier to build, ship, secure, troubleshoot, and operate. It is not itself one of the targeted résumés.
* **Two targeted résumés**, both derived from `resume.json`:

| Résumé | File | Headline | Target role families |
|---|---|---|---|
| Software & Platform | `William_Elias_Software_Platform_Resume.pdf` | Software & Automation Engineer | Developer Productivity, Developer Experience / DevEx, Developer Platform, Software Engineer — Developer Infrastructure / Internal Platform / Tooling, Internal Tools, Platform Software, Infrastructure Software, automation-focused Software Engineering |
| Production & DevOps | `William_Elias_Production_DevOps_Resume.pdf` | Production & DevOps Automation Engineer | Production Engineering, DevOps, Azure DevOps, CI/CD, Build & Release / Release Engineering, Infrastructure Automation, automation-heavy SRE, DevSecOps / Security Automation where appropriate |

* **Legacy PDF compatibility.** `William_Elias_Resume.pdf` already lives in applications, LinkedIn, email, and bookmarks, so it keeps working. It is a generated **byte-for-byte copy of the Production & DevOps résumé** (the closest match to the previous DevOps / Production / CI/CD-positioned résumé), not a third résumé. Its target is set by `compatibility` in `resume_variants.json`, and tests and CI fail if it ever differs from that variant. The website links only the two targeted résumés.

The Software & Platform résumé leads with the Go self-service deployment CLI, Python developer-productivity tooling, and the C#/.NET internal application, and adds HowlPlane and HowlFrame. The Production & DevOps résumé leads with CI/CD standardization scope and validation, release tracking and KQL diagnostics, production reliability, and infrastructure investigation work. Both keep the same facts, metrics, qualifiers, and official job titles.

## Confirmed Professional Content

The current content reflects an independent work-machine audit of internal professional repositories and supersedes the previous factual-correction pass.

**CI/CD standardization — verified scope:** 60 distinct repositories and 104 applications. William built inventory, verification, and reusable pipeline/template automation. Durable evidence includes 56 Azure DevOps build/release definitions across 28 standardized application repositories, 27/28 build verifications, 25/28 representative deployment-path dry runs, several latent delivery defects resolved, and 109 existing definitions reviewed/classified (95 legacy and 14 aligned).

**Security and credential remediation:** Python tooling scanned source code and Git history for exposed credentials, and BFG Repo-Cleaner was used to scrub historical records across 100+ repositories. A measured scan processed 2,832 files and identified 67 distinct exposed secrets in approximately 25 seconds; remediation records are complete.

**Deployment automation:** A Go-based self-service deployment CLI was designed and delivered, covering the build-to-rollback lifecycle with guided setup, Azure DevOps REST integration, generated pipeline configuration, host auditing, and automated post-deployment verification.

**Production-support and internal tooling:** An internal .NET 8 Blazor Web App using Interactive Server, C#, ASP.NET Core, SQL Server, and SQLite is built and maintained for production support. It has per-module access policies, database-backed workflows, retained audit history, DBA approve-only deployment scripts, live configuration/object diffing, pre-change/pre-CAB visibility, and service-desk request tracking. Separate Python/FastAPI dashboards and operational tooling remain distinct from the portal.

**Security / backend:** A scoped OAuth 2.1 resource server integrates an enterprise AI assistant with internal engineering documentation, including JWT/JWKS validation, content allowlisting, and explicit `alg=none` token-bypass defenses.

**Container and infrastructure modernization:** A zero-disk-secret Blazor Web App container migration proof of concept was designed with fail-fast secret validation, database-connectivity health checks, and IIS-fronted container hosting. Server/container migration paths were investigated and disaster-recovery pipeline definitions were audited to identify broken or obsolete deployment paths and support remediation planning. No completed production server migration or zero-downtime DR cutover is claimed.

The current role is **Senior Production Support Engineer | DevOps & Automation**, with the latter a résumé descriptor, in **Auburn Hills, MI · Hybrid**. The official employer-issued title, `Senior Production Support Engineer` (promoted September 2026; previously `Production Support Engineer`), is stored as `officialTitle` and is the only value used for the JSON-LD `jobTitle`; positioning terms (Software & Automation Engineer, platform, DevEx, DevOps) appear only in descriptive fields. Remote availability describes the desired next role. Additional Technical Foundations covers academic/project Java, Kotlin, Android Development, Digital Forensics, FTK Imager, EnCase, and Wireshark, without implying professional forensics employment.

Future content changes should follow new real experience. See the [current handoff](documentation/portfolio_optimization_handoff.md) for provenance and the [targeted résumé validation](documentation/targeted_resume_validation.md) for the factual-drift review and verification of this architecture. The [evidence manifest](documentation/portfolio_optimization_evidence.json) is the historical record of the 2026-09 factual-correction publication and is kept unchanged.

## Deployment & Architecture
- **Canonical data**: `resume.json` is the single source of professional facts, including the `seo` block (canonical URL, site name, descriptions, curated `knowsAbout`) used for metadata and structured data.
- **Variant selection**: `resume_variants.json` defines each targeted résumé as a *selection* of canonical items by stable ID — `summaryStatementIds`, `experienceAchievementIds` (per role, ordered), `skillIds`, optional `skillTags` (a subset of a skill's website tags), `highlightIds`, and `projectIds` — plus presentation-only `label`, `audience`, `title`, `supporting`, and `file`. It cannot hold experience, achievements, project descriptions, or metrics: unknown keys, unknown or wrong-kind IDs, achievements from another role, website-only skills, prose-length text, and **any digit anywhere in the file** fail generation.
- **Canonical IDs**: lowercase, hyphenated, digit-free, and unique across the document — `skill-*`, `exp-*` (roles), `ach-*` (individual achievements), `program-*` (website Selected Work), `highlight-*` (PDF condensations), `project-*`, `edu-*`, and `summary-*` (positioning statements). Selection never depends on array position.
- **Evidence-linked summaries**: résumé summaries are assembled from `positioningStatements`, each with `evidenceIds` pointing at the canonical roles, programs, skills, or education that support it. Numbers in a statement must appear in its evidence; "N+ years" is checked against the earliest dated evidence. `pdfEngineeringHighlights` keep a `sourceProgram`, and their numbers must appear in that program.
- **Generated assets**: `scripts/build_config.py` writes `config.js` with only `personal.sourceRepo` and `personal.sourceBranch`, which is all `script.js` reads (the footer last-synced widget). It does not republish the rest of `resume.json`. `scripts/build_html.py` reads `scripts/site_template.html`, `resume.json`, and `resume_variants.json` and writes `index.html`, metadata, JSON-LD, `robots.txt`, `sitemap.xml`, and the 1200 × 630 `preview.jpg`; `scripts/generate_resume_pdf.py` writes both targeted PDFs and then copies the compatibility variant to `William_Elias_Resume.pdf`. `scripts/generate_linkedin_banner.py` reads the current `personal.title` and tagline and writes `assets/images/linkedin-banner.png`, so a rebuild cannot republish a retired headline. CI rebuilds that PNG and fails if it differs from the committed file. Edit the template for structural HTML changes; never use the generated page as the template.
- **Site presentation (`resume.json` → `site`)**: website-only ordering and copy that never reach the PDFs. `whatIBuild` lists the three artifact families shown first; `selectedWork` orders the eight programs (the three `featured` software artifacts share the first row in equal columns and equal height, `wide` programs span the row, the rest pair up with equal heights), labels them Professional, and adds Scope / Implementation / Verification context lines on the wide CI/CD card (`restatedBullets` names the canonical bullets those lines restate, so they are not repeated on the page); `experienceSummaries` replaces a role's case-study bullets with a one-line summary that links to Selected Work; `projectsProvenanceLabel` and `projectsIntro` mark open-source work as independent; `portfolioNote` is the short build note. The 60 and 104 headline figures render inside the wide CI/CD card. The 67 secret count stays in the credential-remediation card as a normal bullet with the measured-scan facts. The copy in `site` was rewritten through HowlWriter's native, fidelity-checked path; see `documentation/targeted_resume_validation.md`.
- **Website vs. PDFs**: The website shows breadth: all eight `selectedEngineeringPrograms`, every project, every skill tag, and Additional Technical Foundations. Each PDF is selective: chosen achievements in a chosen order, chosen skill categories (website-only categories with `pdfInclude: false` cannot be selected), chosen highlights, and chosen open-source projects under "Selected Open-Source Engineering". Earlier Experience and Education appear in both PDFs. Canonical qualifiers such as `skills[].pdfContext` (e.g. "Python/PowerShell professionally; Go for deployment tooling") always render with their category; variants cannot remove them.
- **Résumé UX**: two plain links, "Software & Platform Resume" and "Production & DevOps Resume", appear in the hero, in the mobile menu, and with a one-sentence explanation plus audience hints in the "Two Targeted Resumes" section right after What I Build (`#resume-downloads`). The navbar "Resumes" control jumps to that labelled choice. There is no dropdown or hover-only behavior; controls are at least 44 × 44 CSS pixels and stack at narrow widths.
- **Determinism**: PDFs use a fixed creation date and uncompressed streams, so fpdf2's content-derived document ID and every byte are reproducible across environments. The alias is a file copy.
- **Section Order**: Hero → About → What I Build → Two Targeted Resumes → Selected Work → Professional Experience (including Earlier Experience) → Open Source & Independent Engineering → Education → Core Expertise → How This Portfolio Is Built → Contact.
- **Deployment**: Deployed via classic GitHub Pages (serving directly from the `main` branch).
- **CI/CD**: GitHub Actions runs the tests (with `poppler-utils` for `pdftotext` ATS checks), rebuilds everything, fails if any generated file — including all three PDFs and `assets/images/linkedin-banner.png` — is stale, and checks the alias is identical to its variant. CI does not mutate the repository or push commits.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `resume.json` file. No need to touch HTML!
- **What I Build**: three professional artifact families (Go deployment CLI, .NET 8 Blazor production-support app, Python/FastAPI tooling) with their stacks, ahead of any metric, each linking to its case study.
- **Selected Work**: Eight professional programs, software artifacts first, with metrics shown in context; native expandable "Implementation & validation" disclosures retain detailed evidence, validation counts, and shared-ownership qualifications. They work with keyboard controls and without JavaScript.
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Readable Role Title**: A dedicated dark-theme text color keeps the small mobile role title above 4.5:1 contrast while retaining the existing decorative accent colors.
- **Mobile Responsive**: Custom hamburger menu and flexible layout, including a hero photo that reflows between the tagline and contact actions on narrow viewports instead of trailing the whole hero.
- **Targeted Resume Downloads**: Software & Platform and Production & DevOps PDFs in the hero, mobile menu, and the Two Targeted Resumes section.
- **Persistent Resume CTA**: A navbar "Resumes" action is visible at every width and jumps to the labelled résumé choice.
- **Recruiter Contact CTA**: A focused "Open to U.S. Remote Opportunities" section before the footer surfaces Email/LinkedIn/GitHub, generated from `resume.json` and `resume_variants.json`.
- **Scroll-Aware Navigation**: An `IntersectionObserver`-based active state highlights the nav link for the section currently in view (`aria-current="page"` plus a non-color underline indicator).
- **SEO / Structured Data**: Canonical link, complete OG/Twitter metadata, and a generated JSON-LD `ProfilePage`/`Person` block, plus a generated `robots.txt` and `sitemap.xml`.
- **Terminal-Style Intro**: The tagline is shown in full, with a blinking caret. The caret animation is disabled under `prefers-reduced-motion`. There is no typewriter reveal.
- **Live "Last Synced" Widget**: Footer pulls the latest commit from the GitHub API and shows it as a relative timestamp + short SHA. Cached in localStorage for 10 minutes to stay polite to GitHub's unauthenticated rate limit.

## How to Update Your Information

All professional facts live in `resume.json`; which facts each résumé shows lives in `resume_variants.json`. Do not manually edit generated artifacts. Use `scripts/site_template.html` for layout changes and `style.css` / `script.js` for styling and interactions.

1. Update facts in `resume.json` (or selection in `resume_variants.json`).
2. Regenerate the derived files:
   ```bash
   python scripts/build_config.py
   python scripts/build_html.py
   python scripts/generate_resume_pdf.py
   python scripts/generate_linkedin_banner.py
   ```
3. Run the tests and inspect all four PDF pages (both résumés are required to stay exactly two pages).
4. Update `README.md` and `change_log.md`, review the diff, and commit the sources together with all generated outputs. Publishing to `main` is a separate deployment action. CI checks freshness without modifying or committing files.

### Updating facts safely
- Change a fact in **one** place: the canonical item in `resume.json`. Both résumés and the website pick it up.
- Keep scope, dry-run, co-led, contributed, proof-of-concept, investigation, academic, and project qualifiers. Do not turn Azure DevOps into Azure cloud ownership, project work into professional work, or shared work into sole ownership.
- Keep historical job titles exactly as issued; the current role's `officialTitle` feeds structured data.
- A new number in a positioning statement needs evidence carrying that number; a new number in a PDF highlight must already appear in its `sourceProgram`. Validation fails otherwise.

### Changing what a résumé shows
- Reorder or drop items by editing the ID lists in `resume_variants.json`. To show a different skill selection, use `skillTags` with a subset of that skill's canonical tags.
- Need wording that does not exist yet? Add a canonical item (for example a new `positioningStatements` entry with `evidenceIds`, or a new `pdfEngineeringHighlights` entry with `sourceProgram`) to `resume.json`, then reference its ID. Never paste prose or metrics into the variant file.
- To change which variant the legacy `William_Elias_Resume.pdf` mirrors, change `compatibility.variant`. Do not add a third résumé configuration.

### Adding a New Job
Find the `experience` array in `resume.json` and add a new object to the top of the list. Give the role and each achievement a stable ID, and record the employer-issued title in `officialTitle`:

```json
{
    "id": "exp-new-company",
    "date": "March 2026 - Present",
    "title": "Senior Security Engineer",
    "officialTitle": "Senior Security Engineer",
    "company": "New Company Inc.",
    "location": "Remote",
    "achievements": [
        {"id": "ach-new-first", "text": "First bullet point goes here."},
        {"id": "ach-new-second", "text": "Second bullet point goes here."}
    ]
}
```

Then add the role's achievement IDs, in the order you want, to each variant's `experienceAchievementIds` (a role left out shows all of its achievements in canonical order). Professional depth beyond the `experience` entries lives in `selectedEngineeringPrograms`, rendered as "Selected Work" with expandable `details`. Each headline metric identifies its `sourceProgram`; tests verify numerical claims against that specific program. Avoid dynamic deployment/adoption counts. Open-source/personal work lives in `projects`; each variant selects projects by ID. The website AI capability stack comes from `aiEngineeringCapabilities`.

## Local Development & Validation

Since this is a static site, you can view it locally by simply double-clicking `index.html` in your browser.

Before committing your changes, you should validate them end-to-end to ensure config validity, fresh generated files, and passing tests. Run the following sequence in your terminal from the project root:

```bash
# 1. Use Python 3.12, matching CI, and install pinned dependencies
python3.12 -m venv /tmp/william-elias-venv
source /tmp/william-elias-venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium --with-deps
sudo apt-get install -y poppler-utils  # pdftotext/pdftoppm for ATS checks and page renders

# 2. Rebuild all derived files
python scripts/build_config.py && python scripts/build_html.py && python scripts/generate_resume_pdf.py && python scripts/generate_linkedin_banner.py

# 3. Run the test suite
PYTHONPATH=. pytest tests/
```

The suite builds all nine artifacts (including both targeted PDFs, the legacy alias, and the LinkedIn banner) in two independent temporary directories containing only source inputs. It checks both checked-in freshness and byte-for-byte repeatability, including PDF, social preview, and `assets/images/linkedin-banner.png`, without rewriting the working tree. Navigation tests wait up to five seconds for the requested scroll position and active state while preserving smooth scrolling.

It also checks variant integrity, exact two-page counts, the alias, `pdftotext` ATS extraction, résumé control tap targets, and keyboard focus. Also render and inspect all four targeted-PDF pages (`pdftoppm -png -r 80 <file>.pdf page`) and review the website at 320, 390, 810, 1024, and 1440 pixels across dark, light, and both contrast modes before publishing. The full suite uses Chromium; other browser engines are not covered. See [the optimization handoff](documentation/portfolio_optimization_handoff.md) for the latest validation evidence, reviewer perspectives, environment limitations, and deferred work.
