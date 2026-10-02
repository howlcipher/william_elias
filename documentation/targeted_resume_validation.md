# Targeted résumé variants — validation and factual-drift review

Date: 2026-10-02. Branch: `feat/targeted-resume-variants`. Base: `main` at `6652b70`.

## What changed

The model is now **one person → one canonical evidence base (`resume.json`) → one broad website → two targeted résumé views (`resume_variants.json`)**.

* The website headline is **Software & Automation Engineer**, supporting line **Developer Tooling • Platform Engineering • CI/CD • Production Engineering**.
* `William_Elias_Software_Platform_Resume.pdf` — "Software & Automation Engineer"; supporting line "Developer Tooling | Platform Engineering | Python | Go | C#/.NET | CI/CD".
* `William_Elias_Production_DevOps_Resume.pdf` — "Production & DevOps Automation Engineer"; supporting line "CI/CD | Azure DevOps | Automation | Reliability | Python | Production Systems".
* `William_Elias_Resume.pdf` — byte-for-byte copy of the Production & DevOps PDF (`compatibility` in `resume_variants.json`), so existing links keep working without a third résumé.

These headlines are résumé positioning labels shown above the experience. Every job title in Professional Experience and Earlier Experience is unchanged, and the JSON-LD `jobTitle` is now the official current title, **Production Support Engineer**. Previously, JSON-LD reported the positioning headline as `jobTitle`.

## Factual-drift review

Wording that was only selected or reordered by a variant has no entry. Every experience achievement, program card, project highlight, earlier-experience summary, education entry, skill tag, and qualifier (`pdfContext`) is unchanged; only IDs were added.

### Changed or new professional wording

| Canonical ID / field | Old wording | New wording | Evidence reference / reason |
|---|---|---|---|
| `personal.title` (website headline) | DevOps, Software & Production Engineer | Software & Automation Engineer | Positioning label requested for the broad profile; not a job title. Not used as `jobTitle`. |
| `personal.supporting` | Python • C#/.NET • Go • Azure DevOps • CI/CD • REST APIs | Developer Tooling • Platform Engineering • CI/CD • Production Engineering | Domains already in canonical content: Developer Tooling skill tag and program names, Platform Engineering (prior `knowsAbout` and target roles), CI/CD program, Production Engineering (prior target roles). No new experience. |
| `personal.pdfSupporting` | Python • … • ASP.NET Core | *(removed)* | Replaced by the per-variant `supporting` presentation line. |
| `summary` (single résumé summary) | DevOps, Software and Production Engineer with 10+ years … AI-enabled engineering with human review. | *(retired)*; replaced by the `positioningStatements` below | Factual summary prose now traces to evidence IDs. |
| `summary-software-opening` | (new) | Software and automation engineer with 10+ years across software delivery, production operations, infrastructure, and networking, building developer tools, internal applications, and delivery automation. | Same tenure/domain phrase as the retired summary; `exp-stellantis`, `exp-hbk`, `exp-trendset` (Sep 2015 start), `program-deployment-tooling`, `program-internal-software`, `program-python-productivity`. |
| `summary-build-tools` | (new) | Builds a Go self-service deployment CLI, Python/FastAPI dashboards and Azure DevOps REST automation, and a C#/.NET Blazor internal production-support application. | `program-deployment-tooling`, `program-python-productivity`, `program-internal-software`. Azure DevOps REST is attached only to the CLI and Python tools, not the Blazor portal. |
| `summary-delivery-enablement` | (new) | Turns CI/CD standardization, credential remediation, and recurring production-support work into reusable pipeline templates, CLI tooling, and scheduled automation. | `program-cicd-release` (reusable pipeline templates), `program-security-remediation`, `program-python-productivity` (reusable operations CLI, scheduled reporting, recurring workflows). No outcome/adoption claim. |
| `summary-security-depth` | (new) | Adds security depth through credential-remediation tooling, OAuth/OIDC/JWT work, Auth0 identity troubleshooting, and in-progress M.S. Cyber Defense studies. | `program-security-remediation`, `program-oauth-integration`, `skill-security-identity`, `edu-ms-cyber-defense` ("In Progress" preserved). |
| `summary-production-opening` | (new) | Production and DevOps automation engineer with 10+ years across production operations, software delivery, infrastructure, and networking. | `exp-stellantis`, `exp-hbk`, `exp-trendset`. |
| `summary-cicd-delivery` | (new) | Builds Azure DevOps CI/CD standardization, reusable pipeline templates, release tracking, and Go and Python deployment and operations automation. | `program-cicd-release`, `program-production-reliability` (release tracking), `program-deployment-tooling`, `program-python-productivity`. |
| `summary-production-reliability` | (new) | Troubleshoots production API/integration, database, configuration, and infrastructure issues with Azure Monitor, Application Insights, KQL, structured logging, incident triage, and RCA. | `program-production-reliability` details; `skill-production-reliability` tags. |
| `summary-security-infrastructure` | (new) | Adds credential remediation, Auth0/OAuth/OIDC troubleshooting, and a Windows Server, IIS, Active Directory, SQL Server, and network infrastructure background. | `program-security-remediation`, `skill-security-identity`, `skill-infrastructure-operations`, `exp-trendset`, `exp-project-worldwide`. "Background", not ownership. |
| `highlight-cicd-release` | Directed a CI/CD standardization program … with build validation and representative deployment-path dry runs. | *(removed)* | Duplicated the experience bullet; the claim remains in `ach-cicd-standardization` and the program card. |
| `highlight-internal-software` → `highlight-portal-change-safety` | Built and maintain an internal .NET 8 Blazor Web App … audit history, live diffing, and service-desk tracking. | Change-safety features in the modular .NET 8 Blazor Web App include DBA approve-only deployment scripts, live configuration/object diffing for pre-CAB and pre-deployment review, per-module access policies, and retained audit history; integrated service-desk request tracking keeps operational workflows traceable. | `program-internal-software` bullets/details. SOX wording deliberately omitted (the handoff forbids a formal SOX compliance claim). |
| `highlight-python-productivity` → `highlight-python-workflow-tools` | Built a suite of Python developer and operations tools spanning API automation, … recurring support workflows. | Sole-authored Python tools parse failed integration payloads into a structured DBA-approval queue, run scheduled query-to-email reports, and summarize processing errors embedded in XML integration logs; repository-discovery and Git-history remediation tooling supports single-repository and whole-project modes with interchangeable rewrite engines. | `program-python-productivity` details. "Sole-authored" is applied only to the three tools the details call sole-authored. |
| `highlight-deployment-tooling` | (new) | Guided setup and project initialization/scaffolding generate pipeline configuration; Azure DevOps REST integration drives build, push, deploy, rollback, status, and audit; host auditing, fail-fast deployment-path validation, container-lifecycle integration, and automated post-deployment verification are built in. | `program-deployment-tooling` bullets/details. No adoption, user-count, or "Internal Developer Platform" claim. |
| `highlight-production-reliability` | (new) | Troubleshoot production application issues as the primary responsibility, across API/integration, database, configuration, and infrastructure problems, using Azure Monitor, Application Insights, KQL, and structured logging; support data-migration and infrastructure-migration efforts, including scripted data moves and DR-related database migration work. | `program-production-reliability` details, near-verbatim; "support" qualifier kept. |
| `highlight-infrastructure-investigation` | (new) | Investigated server/container migration paths and audited disaster-recovery pipeline definitions to identify broken or obsolete deployment paths and support remediation planning, working across OS configuration, IIS, Active Directory, firewall rules, databases, and load balancers; designed a zero-disk-secret Blazor Web App container migration proof of concept. | `program-infrastructure-modernization`; "investigated", "audited", and "proof of concept" kept. No completed migration or cutover. |
| JSON-LD `jobTitle` | DevOps, Software & Production Engineer | Production Support Engineer | Official employer-issued title (`experience[exp-stellantis].officialTitle`). Correction toward truth. |
| JSON-LD `description` | Building Software, Automating Work & Delivering Reliable Systems | Software and automation engineer who builds developer tools, internal software, CI/CD and delivery automation, and production engineering systems that make software easier to build, ship, secure, troubleshoot, and operate. | Positioning text (`seo.personDescription`); mirrors the prior About wording "easier to build, ship, secure, troubleshoot, and operate". |
| `seo.knowsAbout` | … Git, IAM … | Removed Git, IAM; added Developer Productivity, Developer Experience (DevEx), Internal Tools, Infrastructure Automation, Production Reliability, DevSecOps | Topic keywords already present as prior target roles (contact copy) or canonical program/skill names. Git and IAM stay in visible skills. |
| `seo.siteName`, `description`, `socialDescription` | DevOps, Software and Production Engineer … | Software & Automation Engineer: Developer Tooling, Platform Engineering, Azure DevOps CI/CD, Production Engineering, Python, Go and C#/.NET. (and similar social copy) | Metadata positioning only. |
| `about` (3 paragraphs) | I work where software engineering, DevOps, and production operations overlap … | I am a software and automation engineer … (same recent-work list, reordered to lead with the Go self-service deployment CLI; target roles reordered; adds "My in-progress M.S. in Cyber Defense adds security depth") | Same facts. M.S. kept as "in-progress". |
| `personal.contactCopy` | Open to U.S. fully remote DevOps, … roles. | Open to U.S. fully remote roles in software engineering for developer tooling, internal platforms, and automation; developer productivity and developer experience (DevEx); … | Desired-role language, not experience claims. |

### Explicit inflation review

| Risk | Result |
|---|---|
| Proof of concept → production | Container work remains "proof of concept" in the PDF highlight and program card. |
| Investigation → completed migration | Server/container migration and DR work remain "investigated" / "audited" / "support remediation planning". No cutover or zero-downtime claim (banned-term tests run on both PDFs). |
| Azure DevOps → Azure cloud | No Azure cloud, AKS, Terraform, Kubernetes, AWS, or GCP claim; tested on both PDFs. Azure Monitor and Application Insights appear only as diagnostics tools. |
| Project → professional | HowlPlane and HowlFrame appear only under "Selected Open-Source Engineering". Website-only Additional Technical Foundations (academic) cannot be selected by a variant. GitHub Actions stays "(projects)". |
| Academic → professional | M.S. Cyber Defense stays "In Progress"; CCNA stays "Previously Held"; both asserted in both PDFs. |
| Shared → sole ownership | "Sole-authored" appears only where the canonical details already say so. No team-lead or ownership language was added. |
| Dry-run → production deployment | "dry-run validated representative deployment paths for 25 of 28" and "remaining checks blocked" are asserted in both PDFs. |
| Changed metrics | None. Tests assert the canonical metric strings, require every number in either PDF to exist in `resume.json`, forbid digits in the variant file, and trace statement/highlight numbers to their evidence. |
| Dropped qualifiers | `pdfContext` qualifiers are canonical and always rendered with a selected category. |
| Fabricated historical titles | None. All role titles render verbatim. The PDF headlines are positioning labels, and JSON-LD uses the official title. |

No professional-experience claims were intentionally upgraded, invented, or converted from project, proof-of-concept, academic, or investigative work into professional production ownership.

### Ambiguities intentionally left unchanged

* **"Directed a CI/CD standardization program"**: the existing verb was kept verbatim. The evidence describes building the inventory, verification, templates, and definitions; earlier documentation mentions preserving "co-led"/"contributed" qualifiers generally. The verb was neither strengthened nor softened here; William should confirm it if the program had a different formal lead.
* **"Self-service" deployment CLI**: canonical wording kept. The evidence does not document adoption or user counts, so none is claimed, and the CLI is not called an Internal Developer Platform.
* **"10+ years"**: unchanged from the prior summary. It spans Sep 2015 to present and includes the networking roles; the text says "across software delivery, production operations, infrastructure, and networking".
* **"Platform Engineering" / "Infrastructure Automation"**: used only as domain/target-role terms (supporting line, metadata, contact copy), as before. They are not presented as a held role or IaC ownership.

## Verification (2026-10-02)

Environment: Python 3.12.3 with pinned `requirements-dev.txt` (fpdf2 2.8.7, pypdf 6.14.2, Pillow 12.3.0, Playwright 1.60.0), Chromium headless shell, poppler 24.02 `pdftotext`/`pdftoppm`.

| Check | Result |
|---|---|
| Baseline suite on `main` (`6652b70`) | 232 passed |
| Final suite `PYTHONPATH=. pytest tests/ -W error` | 356 passed, 0 skipped, 0 failed |
| Page counts (pypdf, automated) | Software & Platform 2, Production & DevOps 2, legacy alias 2 |
| Legacy alias | `cmp` identical to the Production & DevOps PDF; tested to follow `compatibility.variant` |
| Determinism | Eight artifacts built in two independent temp directories are byte-identical to each other and to the checked-in files; independent per-variant rebuilds are identical |
| ATS (`pdftotext`) | Both PDFs: sections extract in order (Summary → Experience → Core Expertise → Highlights → Open Source → Earlier Experience → Education), contact details/URLs extractable, every selected achievement extracts verbatim, no U+FFFD or `(cid:` glyphs, "Brüel & Kjær" intact, variant keyword sets present, no images |
| Website | Both résumé links in hero, mobile menu, and CTA; navbar "Resumes" jumps to `#resume-downloads`; each download is byte-identical to its file; legacy URL served; the site no longer links the ambiguous single PDF |
| Responsive / accessibility | 20 captures (320, 390, 810, 1024, 1440 × dark, light, contrast-dark, contrast-light): no horizontal overflow, no page errors, smallest résumé control 44 px, navbar control 44 px, stacked at ≤ 620 px; keyboard Tab reaches both hero résumé links with a visible 3 px outline; plain anchors, no hover dependency; existing scroll-spy, mobile menu, theme, and no-JS tests pass |
| SEO | JSON-LD parses; `jobTitle` = Production Support Engineer; positioning terms in `description` and `knowsAbout`; meta description 155 chars |
| PDF visual inspection | All four targeted-PDF pages rendered with `pdftoppm -r 100` and inspected: no clipping, overlap, page-three spill, orphaned headings, or split skill lines; 10 pt body text retained; links/URLs intact. Alias proven identical, so not rendered separately. |

Rendered pages and screenshots were kept as local session artifacts and are not committed, following repository convention.
