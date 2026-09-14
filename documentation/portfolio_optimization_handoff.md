# Portfolio positioning and evidence handoff

## Current recruiter-facing identity

**DevOps, Software & Production Engineer**

Supporting line: **Python • C#/.NET • Go • Azure DevOps • CI/CD • REST APIs**

William builds software and automation for delivery, production reliability, developer tooling, security, and operational problems. The portfolio targets U.S. fully remote DevOps, Azure DevOps, Production Engineering, internal-tools/automation/backend software engineering, infrastructure automation, developer productivity, platform engineering, and security automation / DevSecOps roles. Security Automation and AI-Enabled Engineering are supporting differentiators, not primary career identities.

## Evidence boundaries preserved

`resume.json` is the canonical content source. Regenerate all public artifacts with the scripts in `scripts/`; do not use generated assets as sources.

* CI/CD scope remains 60 repositories and 104 applications. Standardized rollout is complete for 28 repositories, with 56 Azure DevOps build/release definitions across those 28. Build validation was 27/28; representative deployment-path dry runs were 25/28. The separate review of existing definitions found 95 legacy definitions out of 109 reviewed.
* The production-support portal is ASP.NET Core on .NET 8 with Razor Pages, SQL Server and SQLite, role-gated workflows, audit logging, live configuration diffing, pre-change-review visibility, and service-desk integration. It is not Blazor.
* The separate Blazor Web App is a container-deployment proof of concept using Interactive Server. Do not combine it with the production-support portal.
* Security evidence is credential discovery/classification, Git-history remediation, Azure Key Vault migration support, and the scoped OAuth 2.1 resource-server work. Credential findings were reduced from 866 to 67 distinct exposed secrets; the Key Vault migration remains ongoing.
* Python remains central through developer and operations tooling, Azure DevOps REST API automation, payload triage, scheduled reporting, integration-log parsing, engineering search, RCA, operations CLI work, and recurring production-support workflows.
* The reusable 22-query KQL library is authored and maintained for internal monitoring and troubleshooting automation. Release tracking is maintained for a recurring, roughly weekly cadence, with direct deployment participation.

## Explicit exclusions

Do not assert: credential remediation across 100+ repositories; 157 definitions; six latent defects; FastAPI dashboards; Auth0 troubleshooting; Application Insights adoption claims; a Blazor production-support portal; formal SOX compliance; sole authorship of 300+ retirements; leading weekly production releases; unqualified migrations; Python apps hosted on IIS; vendor-report conversion; a completed DR cutover; a zero-downtime production-server migration; or a completed organization-wide Key Vault migration.

## Artifact and validation workflow

```bash
python3 scripts/build_config.py
python3 scripts/build_html.py
python3 scripts/generate_resume_pdf.py
PYTHONPATH=. pytest tests/ -W error
git diff --check
```

The test suite verifies generated-artifact freshness and repeatability, the eight-card Engineering Impact order, the portal/Blazor separation, CI/CD metric scope, the 67-secret and 22-query claims, stale-claim exclusions, metadata, and browser accessibility/responsive behavior. Before publication, visually inspect the two-page PDF and the site at 320, 390, 810, 1024, and 1440 pixels in dark, light, and both contrast modes.
