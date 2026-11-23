# William Elias

**Software & Automation Engineer**
Developer Productivity • Internal Tools • Secure Automation
Open to U.S. Remote Opportunities

[Portfolio](https://howlcipher.github.io/william_elias/) · [Primary résumé (PDF)](https://howlcipher.github.io/william_elias/William_Elias_Software_Platform_Resume.pdf) · [LinkedIn](https://linkedin.com/in/wylelias) · [GitHub](https://github.com/howlcipher)

I build internal software and tools for safer releases and faster diagnosis. My work spans internal applications, release automation, Python tooling, and application security controls. Production troubleshooting informs how I design and verify changes.

## Targeted résumés

| Résumé | Focus |
| --- | --- |
| [Software Engineering & Developer Tools](William_Elias_Software_Platform_Resume.pdf) | Developer productivity, internal tools, platform software |
| [Security Software & Automation](William_Elias_Security_Automation_Resume.pdf) | Security tooling, automation, development-focused DevSecOps |
| [Production & DevOps](William_Elias_Production_DevOps_Resume.pdf) | Production and release engineering, reliability automation |

The legacy [William_Elias_Resume.pdf](William_Elias_Resume.pdf) URL mirrors Production & DevOps.

## Independent projects

Public repositories include [HowlPlane](https://github.com/howlcipher/howlplane), [HowlProof](https://github.com/howlcipher/howlproof), and [HowlFrame](https://github.com/howlcipher/howlframe). These are independent projects developed with AI coding assistants under my direction and review.

## Build and review

Résumé highlights add technical context alongside the achievement bullets. Tests check that a variant does not repeat the same bullet in both sections.

`resume.json` holds canonical facts and `resume_variants.json` selects résumé content by ID. See the [architecture guide](documentation/ARCHITECTURE.md), [evidence review](documentation/career_evidence_reconciliation.md), and [LinkedIn copy](documentation/linkedin_profile.md).

```bash
pip install -r requirements-dev.txt
playwright install chromium --with-deps
python scripts/maintain.py          # Validate rules, regenerate all artifacts & verify
python scripts/maintain.py --check  # CI verification mode (isolated build freshness check)
PYTHONPATH=. pytest tests/ -W error
```

Individual generator scripts (`build_config.py`, `build_html.py`, `generate_resume_pdf.py`, `generate_linkedin_banner.py`, `generate_linkedin_profile.py`, `generate_github_profile_readme.py`) can also be run independently as needed.

Use Python 3.12 and install Poppler for the PDF checks. Pytest runs serially by default. CI uses Ubuntu 24.04 for the pinned Playwright version.
