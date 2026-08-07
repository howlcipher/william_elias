# William Elias

**Senior DevOps / Platform Engineer**
CI/CD & Release Automation | Production Reliability
Open to U.S. Remote Roles

[Live Portfolio](https://howlcipher.github.io/william_elias/) · [Download Resume (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

| | |
|---|---|
| **~60** | Applications in CI/CD delivery-standardization scope |
| **100+** | Repositories credential-remediated |
| **300+** | Legacy applications retired |

---

## About This Repository

This is the source for the resume website above: a professional, modern, and highly performant resume site built with HTML, CSS, and vanilla JavaScript.

## Deployment & Architecture
- **Data Source**: A single `resume.json` acts as the canonical source of truth for all content.
- **Generated Assets**: The static `config.js` used by the browser, the SEO meta tags and pre-rendered body content in `index.html`, and the downloadable `William_Elias_Resume.pdf` are all generated from `resume.json` via Python scripts. The PDF renders `resume.json`'s `additionalExperience` array as a compact "Earlier Technical Experience" section, and forces a page break so "Selected Engineering Programs" always starts on page 2.
- **Deployment**: Deployed via classic GitHub Pages (serving directly from the `main` branch).
- **CI/CD**: GitHub Actions verify tests and ensure that the generated assets are fresh, but CI does not mutate the repository or push commits.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `resume.json` file. No need to touch HTML!
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Mobile Responsive**: Custom hamburger menu and flexible layout.
- **Print/PDF Download**: Embedded download link for the PDF version.
- **View Source**: Hero pill linking straight to this repo.
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
4. Commit all changes (including the updated `resume.json`, `config.js`, `index.html`, and `William_Elias_Resume.pdf`) and push to `main`. CI will verify that the generated files are up to date before changes are fully integrated.

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

Professional depth beyond the four-bullet `experience` entries lives in `selectedEngineeringPrograms` (rendered on the website and, via each entry's compact `pdfBullet`, in the PDF's page-2 "Selected Engineering Programs" section). Open-source/personal work lives in `projects` (rendered on the website as "Selected Open-Source Engineering"; omitted from the PDF to preserve the two-page limit). The AI capability stack shown on the website comes from `aiEngineeringCapabilities`.

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
