# William Elias

**DevOps Engineer | CI/CD & Release Automation | Production Reliability**
Automating Software Delivery, Production Observability & AI-Enabled Tooling
Open to U.S. Remote Roles

[Live Portfolio](https://howlcipher.github.io/william_elias/) · [Download Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

| | |
|---|---|
| **~60** | Applications in CI/CD standardization scope |
| **56** | Build/release definitions created across 28 applications |
| **100+** | Repositories credential-remediated |

---

## About This Repository

This is the source for the resume website above: a professional, modern, and highly performant resume site built with HTML, CSS, and vanilla JavaScript.

## Deployment & Architecture
- **Data Source**: A single `resume.json` acts as the canonical source of truth for all content, including the `seo` block (canonical URL, OG/Twitter site name, curated `knowsAbout` list) used for structured data.
- **Generated Assets**: The static `config.js` used by the browser, the SEO/OG/Twitter meta tags, canonical link, JSON-LD structured data, and pre-rendered body content in `index.html`, `robots.txt`, `sitemap.xml`, and the downloadable `William_Elias_Resume.pdf` are all generated from `resume.json` via Python scripts. The generator paginates dynamically (measuring each block's height before placing it) and is tuned to keep the resume to two pages.
- **Website vs. PDF**: The two artifacts are deliberately different. The website shows breadth; the PDF is selective. `experience` renders as "Professional Experience" while `additionalExperience` gets its own compressed "Earlier Experience" section further down the PDF. `selectedEngineeringPrograms` (six entries) is **website-only**; the PDF instead renders `pdfEngineeringHighlights`, a curated three-entry condensation, under "Selected Engineering Highlights". All `projects` appear on the website, but only those with `pdfInclude: true` reach the PDF's "Selected Open-Source Engineering" section. Core Expertise shows every tag on the website and the leading `PDF_SKILL_TAG_LIMIT` tags per category in the PDF, so tag order in `resume.json` matters.
- **Deployment**: Deployed via classic GitHub Pages (serving directly from the `main` branch).
- **CI/CD**: GitHub Actions verify tests and ensure that the generated assets are fresh, but CI does not mutate the repository or push commits.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `resume.json` file. No need to touch HTML!
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Mobile Responsive**: Custom hamburger menu and flexible layout, including a hero photo that reflows between the tagline and contact actions on narrow viewports instead of trailing the whole hero.
- **Print/PDF Download**: Embedded download link for the PDF version.
- **Persistent Resume CTA**: A distinct "Resume" action lives in both the desktop navbar and the mobile menu, so it's reachable after scrolling past the hero.
- **Recruiter Contact CTA**: A focused "Open to U.S. Remote Opportunities" section before the footer surfaces Email/LinkedIn/Resume/GitHub actions, generated from `resume.json`.
- **Scroll-Aware Navigation**: An `IntersectionObserver`-based active state highlights the nav link for the section currently in view (`aria-current="page"` plus a non-color underline indicator).
- **SEO / Structured Data**: Canonical link, complete OG/Twitter metadata, and a generated JSON-LD `ProfilePage`/`Person` block, plus a generated `robots.txt` and `sitemap.xml`.
- **Terminal-Style Intro**: One-time CSS typewriter reveal on the tagline (respects `prefers-reduced-motion`).
- **Live "Last Synced" Widget**: Footer pulls the latest commit from the GitHub API and shows it as a relative timestamp + short SHA. Cached in localStorage for 10 minutes to stay polite to GitHub's unauthenticated rate limit.

## How to Update Your Information

All your information is stored in the canonical `resume.json` file. Do not manually edit `config.js` or the SEO meta tags/pre-rendered content in `index.html`.

1. Open `resume.json` in any text editor and update your information.
2. Regenerate the derived files by running the build sequence:
   ```bash
   python scripts/build_config.py
   python scripts/build_html.py
   python scripts/generate_resume_pdf.py
   ```
   *(Note: This requires development dependencies, see below)*
3. Verify your changes and run the automated tests.
4. Commit all changes (including the updated `resume.json`, `config.js`, `index.html`, `robots.txt`, `sitemap.xml`, and `William_Elias_Resume.pdf`) and push to `main`. CI will verify that the generated files are up to date before changes are fully integrated.

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

Professional depth beyond the `experience` entries lives in `selectedEngineeringPrograms`, rendered on the website as "Selected DevOps & Production Engineering" using each entry's `bullets` array. That array is website-only: to change what the PDF shows, edit `pdfEngineeringHighlights` instead, keeping every claim traceable to a program in `selectedEngineeringPrograms` (a test enforces that any number in a PDF highlight also appears there). Open-source/personal work lives in `projects` (rendered on the website as "Selected Open-Source Engineering"; entries with `pdfInclude: true` are also included in that PDF section, subject to the two-page limit). The AI capability stack shown on the website comes from `aiEngineeringCapabilities`.

## Local Development & Validation

Since this is a static site, you can view it locally by simply double-clicking `index.html` in your browser.

Before committing your changes, you should validate them end-to-end to ensure config validity, fresh generated files, and passing tests. Run the following sequence in your terminal from the project root:

```bash
# 1. Install development dependencies (only needed once)
pip install -r requirements-dev.txt
playwright install chromium --with-deps

# 2. Rebuild all derived files
python scripts/build_config.py && python scripts/build_html.py && python scripts/generate_resume_pdf.py

# 3. Run the test suite
PYTHONPATH=. pytest tests/
```

If the tests pass, your changes are ready to commit and push.
