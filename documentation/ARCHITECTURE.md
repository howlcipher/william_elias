# Portfolio Architecture & Maintenance

How this repository turns one canonical evidence file into the website and the targeted PDF résumés, and how to change it safely. The [README](../README.md) is the recruiter-facing summary.

The architecture is **one person → one canonical evidence base → one broad website → three targeted résumé views (one primary, two secondary) → one legacy compatibility alias**.

| Résumé | File | Headline | Listing | Target role families |
|---|---|---|---|---|
| Software Engineering & Developer Tools | `William_Elias_Software_Platform_Resume.pdf` | Software & Automation Engineer | primary | Software Engineer (Developer Tools / Developer Productivity / Internal Tools), Platform Software, Backend |
| Security Software & Automation | `William_Elias_Security_Automation_Resume.pdf` | Software & Security Automation Engineer | secondary | Security Automation, Security Tools / Security Products software, Software Security, development-focused DevSecOps |
| Production & DevOps | `William_Elias_Production_DevOps_Resume.pdf` | Production & DevOps Automation Engineer | secondary | Production Engineering, DevOps, Azure DevOps, CI/CD, Release Engineering, automation-heavy SRE |

The Software Engineering file keeps its earlier `Software_Platform` name so existing links keep working. `William_Elias_Resume.pdf` is a generated **byte-for-byte copy of the Production & DevOps résumé** for links already in applications, LinkedIn, email, and bookmarks; it is not a separate résumé, the website does not link it, and tests and CI fail if it ever differs from its variant.

The security résumé is security *software and automation* work, not security operations: it does not claim penetration testing, SOC, incident-response, or security-architecture roles.

## Evidence and publication

Use the [career evidence reconciliation](career_evidence_reconciliation.md) for current wording, confidence, and restrictions. Historical audits are useful for explaining prior decisions. They do not authorize reintroducing superseded claims.

The portal leads the software résumé, configuration discovery and Git-history tooling lead the security résumé, and production remediation leads the Production & DevOps résumé. The site shows the broader body of work, including explicitly qualified prototypes.

## Deployment & Architecture
- **Canonical data**: `resume.json` is the single source of professional facts, including the `seo` block (canonical URL, site name, descriptions, curated `knowsAbout`) used for metadata and structured data.
- **Variant selection**: `resume_variants.json` defines each targeted résumé as a *selection* of canonical items by stable ID — `summaryStatementIds`, `experienceAchievementIds` (per role, ordered), `skillIds`, optional `skillTags` (a subset of a skill's website tags), `highlightIds`, and `projectIds` — plus presentation-only `label`, `audience`, `title`, `supporting`, and `file`, and an optional `listing` (`primary` or `secondary`) that controls where the website offers the résumé. It cannot hold experience, achievements, project descriptions, or metrics: unknown keys, unknown or wrong-kind IDs, achievements from another role, website-only skills, prose-length text, and **any digit anywhere in the file** fail generation.
- **Canonical IDs**: lowercase, hyphenated, digit-free, and unique across the document — `skill-*`, `exp-*` (roles), `ach-*` (individual achievements), `program-*` (website Selected Work), `highlight-*` (PDF condensations), `project-*`, `edu-*`, and `summary-*` (positioning statements). Selection never depends on array position.
- **Evidence-linked summaries**: résumé summaries are assembled from `positioningStatements`, each with `evidenceIds` pointing at the canonical roles, programs, skills, or education that support it. Numbers in a statement must appear in its evidence; "N+ years" is checked against the earliest dated evidence. `pdfEngineeringHighlights` keep a `sourceProgram`, and their numbers must appear in that program.
- **Generated assets**: `scripts/build_config.py` writes `config.js` with only `personal.sourceRepo` and `personal.sourceBranch`, which is all `script.js` reads (the footer last-synced widget). It does not republish the rest of `resume.json`. `scripts/build_html.py` reads `scripts/site_template.html`, `resume.json`, and `resume_variants.json` and writes `index.html`, metadata, JSON-LD, `robots.txt`, `sitemap.xml`, and the 1200 × 630 `preview.jpg`; `scripts/generate_resume_pdf.py` writes the three targeted PDFs and then copies the compatibility variant to `William_Elias_Resume.pdf`. `scripts/generate_linkedin_banner.py` reads the current headline, tagline, and supporting line and writes `assets/images/linkedin-banner.png`, so a rebuild cannot republish a retired headline. CI rebuilds that PNG and fails if it differs from the committed file. Edit the template for structural HTML changes; never use the generated page as the template. The LinkedIn profile generator uses canonical About copy, official employment metadata, and the software variant's achievement and project selections. It writes Markdown for manual review.
- **Site presentation** uses the existing hero actions, What I Build cards, and ordered professional case studies. Selected Work leads with the internal portal, CI/CD safety, and Python tooling. Independent projects carry a separate provenance label.
- **Website vs. PDFs**: The website shows breadth: all seven `selectedEngineeringPrograms`, every project, every skill tag, and Additional Technical Foundations. Each PDF is selective: chosen achievements in a chosen order, chosen skill categories (website-only categories with `pdfInclude: false` cannot be selected), chosen highlights, and chosen open-source projects under "Selected Open-Source Engineering". Earlier Experience and Education appear in every PDF. Canonical qualifiers such as `skills[].pdfContext` (e.g. "Go in independent projects and prototyping") always render with their category; variants cannot remove them.
- **Résumé UX**: The software résumé is the primary download in the hero and mobile menu. All three are available in the Targeted Resumes section, with security and production listed as specialist options.
- **Determinism**: PDFs use a fixed creation date and uncompressed streams, so fpdf2's content-derived document ID and every byte are reproducible across environments. The alias is a file copy.
- **Section Order**: Hero → About → What I Build → Targeted Resumes → Selected Work → Professional Experience (including Earlier Experience) → Open Source & Independent Engineering → Education → Core Expertise → How This Portfolio Is Built → Contact.
- **Deployment**: Deployed via classic GitHub Pages (serving directly from the `main` branch).
- **CI/CD** runs serial pytest, checks Poppler ATS text extraction, and rebuilds and compares all generated files including the LinkedIn package and alias.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `resume.json` file. No need to touch HTML!
- **What I Build** links to portal, delivery automation, and Python case studies.
- **Selected Work** uses native implementation disclosures and includes qualified prototypes after the main professional work.
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Readable Role Title**: A dedicated dark-theme text color keeps the small mobile role title above 4.5:1 contrast while retaining the existing decorative accent colors.
- **Mobile Responsive**: Custom hamburger menu and flexible layout, including a hero photo that reflows between the tagline and contact actions on narrow viewports instead of trailing the whole hero.
- **Targeted Resume Downloads**: The software PDF is prominent throughout the site. All three PDFs are available in the Targeted Resumes section.
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
   python scripts/generate_linkedin_profile.py
   ```
3. Run the tests and inspect all six targeted-PDF pages (every résumé must stay exactly two pages).
4. Update `README.md` and `change_log.md`, review the diff, and commit the sources together with all generated outputs. Publishing to `main` is a separate deployment action. CI checks freshness without modifying or committing files.

### Updating facts safely
- Change a fact in **one** place: the canonical item in `resume.json`. Every résumé and the website pick it up.
- Keep scope, dry-run, co-led, contributed, proof-of-concept, investigation, academic, and project qualifiers. Do not turn Azure DevOps into Azure cloud ownership, project work into professional work, or shared work into sole ownership.
- Keep historical job titles exactly as issued; the current role's `officialTitle` feeds structured data.
- A new number in a positioning statement needs evidence carrying that number; a new number in a PDF highlight must already appear in its `sourceProgram`. Validation fails otherwise.

### Changing what a résumé shows
- Reorder or drop items by editing the ID lists in `resume_variants.json`. To show a different skill selection, use `skillTags` with a subset of that skill's canonical tags.
- Need wording that does not exist yet? Add a canonical item (for example a new `positioningStatements` entry with `evidenceIds`, or a new `pdfEngineeringHighlights` entry with `sourceProgram`) to `resume.json`, then reference its ID. Never paste prose or metrics into the variant file.
- To change which variant the legacy `William_Elias_Resume.pdf` mirrors, change `compatibility.variant`. Add a new variant only for a distinct target audience; each one must still fit two pages and pass every variant-parametrized test.

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
python scripts/generate_linkedin_profile.py

# 3. Run the test suite
PYTHONPATH=. pytest tests/
```

The suite builds all eleven artifacts (including the three targeted PDFs, the legacy alias, and the LinkedIn banner) in two independent temporary directories containing only source inputs. It checks both checked-in freshness and byte-for-byte repeatability, including PDF, social preview, and `assets/images/linkedin-banner.png`, without rewriting the working tree. Navigation tests wait up to five seconds for the requested scroll position and active state while preserving smooth scrolling.

It also checks variant integrity, exact two-page counts, the alias, `pdftotext` ATS extraction, résumé control tap targets, and keyboard focus. Also render and inspect all six targeted-PDF pages (`pdftoppm -png -r 80 <file>.pdf page`) and review the website at 320, 390, 810, 1024, and 1440 pixels across dark, light, and both contrast modes before publishing. The full suite uses Chromium; other browser engines are not covered. See the [career evidence reconciliation](career_evidence_reconciliation.md) for current publication questions.
