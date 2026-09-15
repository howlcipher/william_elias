# Portfolio positioning and evidence handoff

## Current recruiter-facing identity

**DevOps, Software & Production Engineer**

Supporting line: **Python • C#/.NET • Go • Azure DevOps • CI/CD • REST APIs**

William builds software and automation for delivery, production reliability, developer tooling, security, and operational problems. The portfolio targets U.S. fully remote DevOps, Azure DevOps, Production Engineering, internal-tools/automation/backend software engineering, infrastructure automation, developer productivity, platform engineering, and security automation / DevSecOps roles. Security Automation and AI-Enabled Engineering are supporting differentiators, not primary career identities.

## Evidence boundaries preserved

`resume.json` is the canonical content source. Regenerate all public artifacts with the scripts in `scripts/`; do not use generated assets as sources.

* CI/CD scope remains 60 repositories and 104 applications. Durable evidence includes 56 Azure DevOps build/release definitions across 28 standardized application repositories, 27/28 build validation, 25/28 representative deployment-path dry runs, and 109 existing definitions reviewed/classified (95 legacy and 14 aligned). Do not publish changing rollout or adoption status.
* The production-support portal is a .NET 8 Blazor Web App with Interactive Server, C#, ASP.NET Core, SQL Server, and SQLite. It has per-module access policies, database-backed workflows, retained SOX/audit history where supported, DBA approve-only deployment scripts, live configuration/object diffing, pre-change/pre-CAB visibility, and service-desk tracking. It is not Razor Pages.
* FastAPI is professional experience for separate internal dashboards and operational tooling; do not attach it to the Blazor portal.
* Security evidence is Python source-code and Git-history scanning, BFG Repo-Cleaner remediation across 100+ repositories, and complete remediation records. A measured scan processed 2,832 files and identified 67 distinct exposed secrets in approximately 25 seconds. Do not claim Azure Key Vault, Managed Identity, Azure SDK, .NET/C#, or automated tests for this tooling.
* Auth0, OAuth/OIDC, IAM, authentication/identity troubleshooting, PII safeguards, and audit controls are supported security/identity content. Do not inflate this to Azure identity architecture ownership.
* Python remains central through FastAPI dashboards, developer and operations tooling, Azure DevOps REST API automation, payload triage, scheduled reporting, integration-log parsing, engineering search, RCA, operations CLI work, and recurring production-support workflows.
* The reusable 22-query KQL library is authored and maintained for internal monitoring and troubleshooting automation. Release tracking is maintained for a recurring, roughly weekly cadence, with direct deployment participation.

## Explicit exclusions

Do not assert: Razor Pages for the portal; Azure Key Vault, Managed Identity, Azure SDK, .NET/C#, xUnit, 62 automated tests, or 156 automated tests for the corrected systems; formal SOX compliance; sole authorship of 300+ retirements; leading weekly production releases; unqualified migrations; Python apps hosted on IIS; vendor-report conversion; a completed DR cutover; a zero-downtime production-server migration; or Azure identity architecture ownership.

## Artifact and validation workflow

```bash
python3 scripts/build_config.py
python3 scripts/build_html.py
python3 scripts/generate_resume_pdf.py
PYTHONPATH=. pytest tests/ -W error
git diff --check
```

The test suite verifies generated-artifact freshness and repeatability, the eight-card Engineering Impact order, the portal/Blazor separation, CI/CD metric scope, the 67-secret and 22-query claims, stale-claim exclusions, metadata, and browser accessibility/responsive behavior. Before publication, visually inspect the two-page PDF and the site at 320, 390, 810, 1024, and 1440 pixels in dark, light, and both contrast modes.
