# William Elias — Search Engine & AI-Search Visibility Report

**Date:** November 19, 2026  
**Status:** COMPLETE (Milestone D7)  
**Lead Auditor:** AGY (Technical SEO, AI Discoverability & Evidence Auditor)  
**Subject:** Discoverability of William Elias across Web Search (Google, Bing), AI Search (ChatGPT Search, Copilot, Perplexity), and Recruiter Sourcing

---

## 1. Executive Summary

This report establishes the baseline visibility, technical search engine optimization (SEO), and AI-search discoverability posture for William Elias and his verified engineering work.

### Key Discoverability Findings:
1. **Entity Collision with Prominent Namesakes:** Generic branded searches such as `"William Elias software engineer"` or `"William Elias engineer"` are heavily diluted by medical researchers (notably Dr. W. Jeff Elias, neurosurgery pioneer at UVA Health) and national laboratory directors.
2. **Handle-Bound Search Strength:** Searches coupling William's name with his technical handle (`"William Elias howlcipher"`) or independent project (`"William Elias HowlPlane"`) index with 100% precision directly to his GitHub repositories and Go package documentation (`pkg.go.dev`).
3. **AI Search Engine Readiness:** By implementing an advisory `llms.txt` file and structured `candidate-profile.json`, William's portfolio provides a standardized, machine-readable reference for generative AI search engines (ChatGPT Search, Perplexity, Microsoft Copilot), communicating explicit entity disambiguation directives and verified technical scope boundaries.
4. **RFC 9309 Crawler Compliance:** GitHub Pages root crawler behavior was formally audited. The root `https://howlcipher.github.io/robots.txt` 404 response is confirmed non-blocking under RFC 9309, while the repository-level `https://howlcipher.github.io/william_elias/robots.txt` returns HTTP 200 with complete crawl permission and sitemap reference.
5. **Implementation Scope Distinction:** Portfolio code, structured JSON-LD, `candidate-profile.json`, `llms.txt`, SVG diagrams, and automated test suites represent completed, committed repository deliverables. External profile updates (creating the `howlcipher/howlcipher` GitHub profile README, applying LinkedIn profile changes, and verifying Google/Bing Webmaster tools) remain unapplied recommendations awaiting manual owner action.

---

## 2. Branded Query Baseline Benchmark

A benchmark was conducted across public web search indices and search APIs on November 19, 2026:

| Query String | Top Search Results | Entity Disambiguation Result | Visibility Assessment |
| :--- | :--- | :--- | :--- |
| `"William Elias software engineer"` | UVA Neurosurgery faculty, LinkedIn profiles of non-target engineers, general directories | Mixed / Collision with academic namesakes | Low direct visibility without handle qualification |
| `"William Elias GitHub howlcipher"` | `github.com/howlcipher`, `github.com/howlcipher/howlplane`, `pkg.go.dev/github.com/howlcipher/howlframe` | 100% Accurate (Direct to William's engineering work) | High precision; primary entry point for technical verification |
| `"William Elias HowlPlane"` | `github.com/howlcipher/howlplane`, HowlPlane architectural documentation | 100% Accurate (Identifies William as author/maintainer) | High precision; strong association with multi-agent platform |
| `"Wyl Elias LinkedIn"` | `linkedin.com/in/wylelias` | 100% Accurate (Direct to William's professional profile) | High precision; vanity slug provides instant match |
| `site:howlcipher.github.io/william_elias/` | Canonical portfolio homepage, target resume URLs | 100% Accurate (Direct indexation) | Clean indexation; no indexing blocks or canonical conflicts |

---

## 3. Specialist Role Searches & Discoverability Optimization

Recruiters and hiring managers rarely search by candidate name alone; they search for specific skill intersections and role titles. Below is the discovery matrix across the 5 target role families:

### 3.1 Role Family Alignment & Keyword Indexing

| Target Role Family | Primary Discovery Keywords | Portfolio Evidence Surface | Structured Metadata Signals |
| :--- | :--- | :--- | :--- |
| **Developer Productivity Engineer** | `Developer Productivity`, `CI/CD Automation`, `Preflight Validation`, `Drift Detection`, `Azure DevOps` | Preflight checks diagram, CI/CD case study, verification disclosures | `knowsAbout: Developer Productivity, CI/CD, Azure DevOps` |
| **Software Engineer — Internal Tools** | `Internal Tools`, `ASP.NET Core`, `Razor Pages`, `C#`, `SQL Server`, `Operational Tooling` | Operational portal case study, What I Build card, architecture breakdown | `knowsAbout: Internal Tools, ASP.NET Core, Razor Pages, C#` |
| **Platform Software Engineer** | `Platform Engineering`, `Developer Tooling`, `Multi-Agent Architecture`, `Evidence Sandbox`, `HowlPlane` | Howl Ecosystem diagram, HowlPlane / HowlProof / HowlFrame cards | `knowsAbout: Systems Architecture, Multi-Agent Platforms` |
| **Security Automation Engineer** | `Security Automation`, `Secrets Discovery`, `Git-History Tooling`, `zxcvbn`, `Password Arena` | Secrets discovery case study, Password Arena card | `knowsAbout: Security Automation, Secrets Discovery` |
| **Production Engineer (Automation)** | `Production Reliability`, `Incident Triage`, `Telemetry`, `Server File Safeguards`, `Python Scripting` | Production reliability case study, Python productivity card | `knowsAbout: Production Reliability, Incident Triage, Telemetry` |

---

## 4. AI Search Engines & LLM Retrieval Evaluation

AI search engines (Perplexity, ChatGPT Search, Microsoft Copilot) synthesize answers rather than merely returning blue links. To ensure William Elias is represented accurately, the following mechanisms are deployed:

### 4.1 The Role of `llms.txt`
Modern LLM web crawlers (such as `GPTBot`, `PerplexityBot`, `Claude-Web`) seek structured, high-signal Markdown summaries adhering to the `llms.txt` standard. William's portfolio publishes `/llms.txt` containing:
- Direct entity disambiguation directives to distinguish him from medical namesakes.
- Clarification that his official title is **Senior Production Support Engineer** at Stellantis Financial Services US, while his technical positioning is **Software & Automation Engineer**.
- Explicit breakdown of verified skills, independent repositories, and target role alignments.
- Strict factual boundaries preventing unsupported claims (e.g., forbidding claims of AWS/Kubernetes adoption, automated production rollback, or enterprise secret rotation).
- *Advisory Scope:* While `llms.txt` provides structured grounding, it provides no guarantee that external AI search engines will crawl it, index it, or eliminate hallucinations.

### 4.2 Machine-Readable Candidate Profile (`candidate-profile.json`)
Applicant Tracking Systems (ATS) and AI talent platforms increasingly ingest structured JSON profiles. William's portfolio provides a validated, machine-readable JSON profile linked via:
```html
<link rel="alternate" type="application/json" title="Candidate Profile (JSON)" href="candidate-profile.json">
```
This provides standardized semantic structure for programmatic ingestion (subject to individual ATS parsing capabilities).

---

## 5. Technical Discovery & Crawler Infrastructure Audit

### 5.1 Root vs. Project `robots.txt` Analysis (RFC 9309)
- **Root URL:** `https://howlcipher.github.io/robots.txt`
  - *Response:* HTTP 404 (Not Found).
  - *Crawler Behavior:* Under Section 2.3.1.2 of RFC 9309 ("Robots Exclusion Protocol"), an HTTP 4xx response indicates that no crawler restrictions exist for the host. Crawlers treat this as **Allow All**.
- **Project URL:** `https://howlcipher.github.io/william_elias/robots.txt`
  - *Response:* HTTP 200 (OK).
  - *Content:* Explicitly declares `User-agent: *`, `Allow: /`, and references `Sitemap: https://howlcipher.github.io/william_elias/sitemap.xml`.
  - *Status:* 100% compliant and fully verified by automated tests.

### 5.2 Structured Data (Schema.org JSON-LD)
The portfolio `<head>` embeds a fully verified JSON-LD script block containing:
- `@type: "ProfilePage"`
- `mainEntity: Person`
- `jobTitle: "Senior Production Support Engineer"` (Preserving official employer title)
- `description`: Grounded in Software & Automation Engineering capabilities.
- `worksFor`: Organization "Stellantis Financial Services US".
- `alumniOf`: Dakota State University, Colorado State University Global Campus, Rochester College.
- `sameAs`: Explicit bidirectional links to `https://github.com/howlcipher` and `https://linkedin.com/in/wylelias`.
- `knowsAbout`: Curated list of 17 core competencies (no keyword stuffing, length < 30).

---

## 6. Search Console & Webmaster Runbook

To accelerate indexation and monitor search performance, execute the following steps:

### 6.1 Google Search Console Setup
1. Log in to [Google Search Console](https://search.google.com/search-console).
2. Add a new Property using the **URL prefix** method:
   `https://howlcipher.github.io/william_elias/`
3. Verification Method: Select **HTML tag** or **GitHub Pages domain verification**.
4. Submit Sitemap: Navigate to **Sitemaps** and submit:
   `https://howlcipher.github.io/william_elias/sitemap.xml`
5. Request Indexing: In the URL Inspection tool, enter `https://howlcipher.github.io/william_elias/` and click **Request Indexing**.

### 6.2 Bing Webmaster Tools Setup
1. Log in to [Bing Webmaster Tools](https://www.bing.com/webmasters).
2. Import verified property from Google Search Console (one-click integration), or add URL prefix manually.
3. Submit Sitemap: Enter `https://howlcipher.github.io/william_elias/sitemap.xml`.
4. URL Submission: Submit the homepage URL and the three resume PDF URLs for instant indexing.

### 6.3 Maintenance & Re-indexing Cadence
- After any new release or significant resume update, re-run URL inspection in Search Console to request a fresh crawl.
- Sitemaps are automatically maintained by `scripts/build_html.py` during builds.
