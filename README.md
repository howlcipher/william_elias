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

`resume.json` holds canonical facts and `resume_variants.json` selects résumé content by ID. See the [architecture guide](documentation/ARCHITECTURE.md), [evidence review](documentation/career_evidence_reconciliation.md), and [LinkedIn copy](documentation/linkedin_profile.md).

```bash
pip install -r requirements-dev.txt
playwright install chromium --with-deps
python scripts/build_config.py
python scripts/build_html.py
python scripts/generate_resume_pdf.py
python scripts/generate_linkedin_banner.py
python scripts/generate_linkedin_profile.py
PYTHONPATH=. pytest tests/ -W error
```

Use Python 3.12 and install Poppler for the PDF checks. Pytest runs serially by default. CI uses Ubuntu 24.04 for the pinned Playwright version.
