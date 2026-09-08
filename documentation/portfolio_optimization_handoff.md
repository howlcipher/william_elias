# Portfolio factual-correction handoff

This is the current-state handoff for the final factual correction and skills reconciliation. William's direct confirmation supersedes the earlier portfolio wording and tests. The errors were in the portfolio's description of his work, not evidence that the underlying work was incorrect. Previous commits remain in Git history.

## Reconciled starting state

Started from clean, synchronized `main` at `0ef518a`, after fetching origin. Previous polish PR #9 was already merged. The prior design, native Engineering Impact disclosures, static HTML template, two-page PDF generator, and broad GitHub description/topics were present. No unrelated local changes existed. Work uses `fix/resume-factual-corrections`.

`resume.json` remains the canonical professional-content source. The headline remains **Software, DevOps & Automation Engineer**, supported by **Software • Automation • Delivery • Production Reliability**. AI remains one part of that identity. The About section retains three concise paragraphs and the existing layout and section order.

## Directly confirmed corrections

| Area | Incorrect previous wording | Correct current content |
| --- | --- | --- |
| Security work | .NET 8/C# utility, Azure Key Vault migration, integrity-verified rollback, Managed Identity, xUnit, 62 automated tests, migration-path self-review | Python scans of source code and Git history; BFG Repo-Cleaner history cleanup across 100+ repositories, completed; measured 2,832 files / 67 distinct secrets / approximately 25 seconds. No automated tests for this tool. |
| Security technologies | C#, Azure Key Vault, Managed Identity, xUnit, Python, PowerShell | Python, Git, BFG Repo-Cleaner, Credential Remediation, Git History Remediation; compact PDF line: Python, Git, BFG Repo-Cleaner. |
| Internal portal | Razor Pages, xUnit, 156 automated tests, FastAPI in the portal technology list | .NET 8 Blazor Web App using Interactive Server; per-module policies, database-backed workflows, permanently retained SOX audit trail, DBA approve-only scripts, live-object diffing, pre-CAB visibility, service-desk request tracking. |
| Portal technologies | ASP.NET Core 8, Razor Pages, C#, SQL Server, SQLite, xUnit, FastAPI | C#, .NET 8, Blazor, ASP.NET Core, SQL Server, SQLite. FastAPI remains on separate professional dashboards/tooling. |
| Identity | Unsupported Azure identity/security tools | Auth0, OAuth/OIDC, IAM and authentication troubleshooting; no expanded identity architecture ownership. |
| Employment | Hyphenated descriptor and current role marked Remote | Production Support Engineer **\|** DevOps & Automation; Auburn Hills, MI · Hybrid. The first part is the official title, the second a résumé descriptor. U.S. remote availability remains the next-role preference. |
| Delivery | First-deployment/approval, zero-deployment, go/no-go adoption commentary | Durable scope, implementation, and validation evidence without a current deployment count. |

Preserved delivery evidence: ~60-application .NET estate; 56 definitions across 28 applications; 27/28 builds verified; 25/28 deployment paths dry-run validated; six latent delivery defects discovered during validation; repository-to-server inventory, reusable definition/template automation, artifact checks, and environment-readiness guardrails. The inherited detailed evidence also supports 157 definitions organized and 95 legacy definitions inventoried/classified, kept distinct from the 56 created definitions. These private-work facts use William's supplied authority and existing detailed evidence, not an independent employer audit.

Preserved qualified shared ownership for observability and infrastructure/DR, 300+ application retirements, weekly releases, migrations, operational troubleshooting, and AI-assisted knowledge/incident tooling with human-review safeguards.

## Skills reconciliation

Ten website groups become eight: Software & Backend; DevOps & Delivery; Automation; Production & Reliability; Infrastructure & Application Operations; Security & Identity; AI-Enabled Engineering; Additional Technical Foundations.

Web Development is merged into Software & Backend, which now contains Python, FastAPI, C#, .NET, Blazor, ASP.NET Core, SQL Server, REST APIs, SQLite, JavaScript, HTML, and CSS. The explicit eight-tag PDF selection ends at REST APIs. Optional `skills[].pdfTags` must be a non-empty unique subset of website tags; absent fields retain the existing six-tag default. This small generator extension avoids expanding every PDF skill group just to accommodate software skills.

Additional Hands-On Technologies is removed. Docker/Compose remains on the legitimate Baseball Optimizer project; the detailed delivery evidence retains its explicitly qualified WSL2/Rancher Desktop proof of concept. No top-level container/Helm proficiency is implied.

Additional Programming Foundations becomes **Additional Technical Foundations**, website-only: Java, Kotlin, Android Development, Digital Forensics, FTK Imager, EnCase, Wireshark. Visible context explicitly identifies coursework and academic/project experience, not professional production ownership. No professional forensics employment is claimed. GitHub Actions remains project-scoped, Go is explicitly project-scoped in both website and PDF context, and AI remains qualified as internal tools/projects.

## Open-source verification and final wording

Read-only shallow clones of current GitHub default branches were inspected. No changes or test executions were made in those external repositories; the review verifies implementation/test presence, not test success or adoption.

**HowlPlane — AI Engineering Control Plane**, inspected at `e937d61d7168bda1d697a0d3ac81d36fb2813988`:

- Built a Python/Go engineering control plane that routes work across coding agents, reconciles independent reviews, and runs deterministic verification.
- Added durable evidence recording and human-controlled authority boundaries for consequential actions, with shared project context and CI/security checks.

Evidence: `src/control_plane/router.py`, `reconciliation.py`, `verification.py`, `evidence_ledger.py`, `authority_envelope.py`, `human_boundary.py`; Go entrypoint/command layer in `cmd/howlplane/main.go` and `pkg/cli/command.go`; `.agents/` shared context; `.github/workflows/test.yml` and `codeql.yml`. No origin story, production adoption, unsupervised autonomy, or model-training claim is made.

**RedrawUS — Geospatial Analysis & Visualization Platform**, inspected at `430129098b3f1e1192eae51bcc8f0ac4f26af3af`:

- Built a multi-state geospatial analysis platform with Python/R data pipelines and an interactive JavaScript map, persistent browser caching, and Web Workers.
- Processes geographic datasets with GeoPandas, Shapely, and GerryChain; includes pytest, Vitest, and Playwright tests for data processing and application behavior.

Evidence: `pipeline/generate_maps.py`, `pipeline/run_pipeline.R`, `requirements.txt`, `src/DataService.js`, `src/MapController.js`, `src/worker.js`, `package.json`, `tests/python/test_data_processor.py`, `tests/js/DataService.test.js`, and `tests/e2e/dashboard.spec.js`. Vite and Leaflet are present; browser caching uses localforage. The source includes procedural/synthetic fallbacks, so no universal real-data accuracy or scale claim is inferred. `.github/workflows/ci.yml` runs SEO checks and `deploy.yml` builds/tests/deploys Pages; the résumé does not imply that CI runs every named test framework.

The general PDF selects **HowlPlane + RedrawUS**. Baseball Optimizer remains on the broader website. The three PDF highlights are Internal Tools & Developer Enablement, Security & Credential Remediation, and Production Reliability & Observability.

## Generated artifacts and validation

The normal three-generator process produces `config.js`, `index.html`, `robots.txt`, `sitemap.xml`, `preview.jpg`, and `William_Elias_Resume.pdf`. Generated content is never manually patched. SEO/JSON-LD removes the unsupported security term and adds Blazor/Auth0/OAuth/OpenID Connect/IAM while preserving the headline, curated existing metadata, and social preview identity. Robots, sitemap, and preview are regenerated but have no expected visual/content change.

Reproduce with Python 3.12 and `requirements-dev.txt`:

```bash
python scripts/build_config.py
python scripts/build_html.py
python scripts/generate_resume_pdf.py
PYTHONPATH=. pytest tests/ -W error -q
```

The pinned local environment is `/tmp/portfolio-ci`; local Chromium uses `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64` on this Ubuntu 26.04 host. The repository CI uses Python 3.12 and checks generated freshness. Local flake8 follows the existing long-line convention (`--extend-ignore E501`). New factual contracts first reproduced 12 failures against the old content. Old false assertions were replaced with semantic correctness checks; no useful coverage was discarded to retain false claims.

Current artifact hashes, PDF geometry/link evidence, screenshot records, and final validation results are in [the evidence manifest](portfolio_optimization_evidence.json). Capture files are retained outside Git in `/run/media/system/tallgeese/dev/william_elias_evidence/factual-corrections/`; they are local evidence, not assets included in a fresh clone.

## Visual and publication review

Both PDF pages are rendered for inspection. The PDF retains 10-point body text and two Letter pages, with all three engineering highlights grouped on page two. Browser review covers 320, 390, 810, 1024, and 1440 pixels in dark, light, dark contrast, and light contrast modes, plus native disclosure expansion and keyboard operation. Final measured results are recorded in the evidence manifest.

GitHub repository description and all 15 topics already match the intended broad identity; no metadata churn is needed. Pages serves `main` at `https://howlcipher.github.io/william_elias/`. User authorization covers signed commit, push, PR, merge after successful checks, branch deletion, and published site/PDF verification. Publication identifiers and final deployment results are reported with task completion rather than embedding a self-referential commit hash here.

This is the completed canonical general content after the publication gate. Future content work should follow new real experience or a target-specific role. No further general résumé rewrite is pending. Professional implementation was not independently audited with the employer; additional browser engines, screen readers, and a tagged-PDF accessibility audit are outside this verification scope.
