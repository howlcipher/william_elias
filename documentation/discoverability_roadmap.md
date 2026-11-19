# Discoverability & Identity Network Roadmap

This roadmap documents the implementation milestones to make William Elias and his verified engineering work discoverable, accurately represented, and easily verifiable across his portfolio, GitHub, LinkedIn, traditional search engines, and AI-powered search engines.

---

## Milestone Summary

| Milestone | Goal | Status |
|---|---|---|
| **D0** | Existing work reconciliation and baseline | **COMPLETE** |
| **D1** | Portfolio architectural and evidence refinements | **COMPLETE** |
| **D2** | Portfolio SEO and structured data | **COMPLETE** |
| **D3** | Three-property professional identity consistency | **COMPLETE** |
| **D4** | GitHub developer-profile discoverability | **COMPLETE** |
| **D5** | LinkedIn recruiter discoverability | **COMPLETE** |
| **D6** | Machine-readable career profile | **COMPLETE** |
| **D7** | AI-search and traditional search verification | **COMPLETE** |
| **D8** | Visual, factual, accessibility, and release audit | **COMPLETE** |

---

## Detailed Milestones

### Milestone D0: Existing Work Reconciliation & Baseline

- **Objective:** Establish the verified baseline state of the repository, confirm 415 passing tests, record existing SEO and structured data, capture full-page baseline screenshots across all four appearance themes, and execute live search baseline queries.
- **Tasks:**
  - [x] Verify current branch (`feat/discoverability-and-identity-network`) and clean base commit (`9025405`).
  - [x] Execute full test suite (342 non-browser + 73 browser = 415 passed).
  - [x] Record existing JSON-LD, metadata, robots, and sitemap configuration.
  - [x] Capture baseline full-page screenshots in all four themes (`dark`, `light`, `contrast-dark`, `contrast-light`) at desktop (1440px) and mobile (390px) viewports in `documentation/screenshots/baseline/`.
  - [x] Execute live baseline search queries across traditional and AI search (Google, Bing, search APIs).
- **Acceptance Criteria:** Baseline tests pass (415/415), screenshots captured, initial discoverability observations recorded.
- **Status:** **COMPLETE**

---

### Milestone D1: Portfolio Architectural & Evidence Refinements

- **Objective:** Add technical diagrams and evidence indexing to the portfolio to visually communicate verified architecture and simplify technical inspection for engineering hiring managers.
- **Tasks:**
  - [x] Implement an accurate, accessible SVG deployment safeguards architecture diagram illustrating verified preflight drift checks, artifact verification, and server-specific file protections.
  - [x] Implement an accurate, accessible SVG Howl ecosystem architecture diagram detailing the relationship between HowlPlane (control plane/orchestrator), HowlProof (verification engine), and HowlFrame (compiler toolchain & bytecode VM).
  - [x] Add a public independent engineering evidence index connecting repositories, supported capabilities, commit citations, and reproducible test suites.
  - [x] Reinforce the visual and semantic distinction between production-deployed deliverables and exploratory prototypes with Chicago Cubs themed status badges.
- **Dependencies:** D0 baseline.
- **Acceptance Criteria:** Diagrams use semantic, accessible SVG with Cubs palette tokens (`--blue`, `--red`, `--ink`, `--line`), pass contrast checks, render responsively down to 320px, and contain no fictional systems or confidential topology.
- **Status:** **COMPLETE**

---

### Milestone D2: Portfolio SEO & Structured Data

- **Objective:** Ensure maximum crawlability, indexability, and semantic clarity for Googlebot, Bingbot, OAI-SearchBot, and other search engines.
- **Tasks:**
  - [x] Audit origin-level `howlcipher.github.io/robots.txt` (404) vs. project-level `howlcipher.github.io/william_elias/robots.txt` (200), documenting crawler behavior under RFC 9309.
  - [x] Audit and enhance `Person` and `ProfilePage` JSON-LD structured data with stable `@id`, unambiguous `sameAs` links, official job title, `worksFor`, `alumniOf`, and target role competencies.
  - [x] Validate Open Graph, Twitter Cards, canonical URL, sitemap XML, and meta descriptions.
  - [x] Verify heading hierarchy (H1 -> H2 -> H3) and crawlable HTML text accessibility.
  - [x] Document free Search Console and Bing Webmaster Tools verification procedures in search visibility report.
- **Dependencies:** D1 structural additions.
- **Acceptance Criteria:** Structured data parses without errors in schema validators, `Person.jobTitle` matches official title, `sameAs` points to verified profiles, and crawler policies are documented.
- **Status:** **COMPLETE**

---

### Milestone D3: Three-Property Professional Identity Consistency

- **Objective:** Create a unified, cross-reinforcing professional identity network between Portfolio, GitHub, and LinkedIn.
- **Tasks:**
  - [x] Conduct a detailed identity mapping audit (name, aliases/handles, official title, target positioning, core skills, employment history, project identities, contact methods) in `documentation/identity_network_audit.md`.
  - [x] Address search-entity disambiguation (distinguishing William Elias from neurosurgery and national lab namesakes).
  - [x] Verify bidirectional navigational cross-links across all three properties.
  - [x] Document exact owner instructions for manual LinkedIn updates.
- **Dependencies:** D0 baseline, D2 structured data.
- **Acceptance Criteria:** Cross-links resolve accurately; identical core facts are communicated across all three surfaces.
- **Status:** **COMPLETE**

---

### Milestone D4: GitHub Developer-Profile Discoverability

- **Objective:** Maximize technical credibility and discoverability on GitHub (`howlcipher`).
- **Tasks:**
  - [x] Design and produce the complete GitHub profile repository README (`howlcipher/README.md`) to serve as a technical gateway linking to the portfolio and key platforms in `documentation/github_profile_recommendations.md`.
  - [x] Audit repository About descriptions, topics, and homepage links across `william_elias`, `howlplane`, `howlproof`, `howlframe`, `howldream`, and `password_arena`.
  - [x] Prepare exact configuration recommendations for GitHub pinned repositories and profile bio.
- **Dependencies:** D3 identity audit.
- **Acceptance Criteria:** Ready-to-commit `howlcipher/README.md` and repository metadata checklist prepared with accurate, verified technical language.
- **Status:** **COMPLETE**

---

### Milestone D5: LinkedIn Recruiter Discoverability

- **Objective:** Optimize LinkedIn profile for recruiter search visibility across the five target role families while preserving official titles.
- **Tasks:**
  - [x] Review current live LinkedIn profile against `documentation/linkedin_profile.md`.
  - [x] Align headline, About, Experience, Skills ordering, and Featured links.
  - [x] Formulate exact copy and step-by-step checklist for owner-controlled updates in `scripts/generate_linkedin_profile.py` and `documentation/linkedin_profile.md`.
  - [x] Ensure official title (**Senior Production Support Engineer**) is preserved while target keywords (Developer Productivity, Internal Tools, Platform Software, Security Automation) are highlighted.
- **Dependencies:** D3 identity audit.
- **Acceptance Criteria:** LinkedIn package is complete, ready for manual application, and strictly aligned with canonical evidence.
- **Status:** **COMPLETE**

---

### Milestone D6: Machine-Readable Career Profile

- **Objective:** Provide a lightweight, standardized, machine-readable export (`candidate-profile.json` and `llms.txt`) generated deterministically from canonical facts for AI engines, scrapers, and recruiter parsers.
- **Tasks:**
  - [x] Create `candidate-profile.json` generator based on `resume.json`.
  - [x] Evaluate and generate a clean, factual `llms.txt` documenting the portfolio, public projects, verified experience, and AI search guidance.
  - [x] Validate exports against visible site content and ensure zero exposure of private or confidential data.
- **Dependencies:** D1 portfolio content, D2 SEO.
- **Acceptance Criteria:** JSON schema validates, files build automatically during `build_html.py`, and contents contain only public, verified facts.
- **Status:** **COMPLETE**

---

### Milestone D7: AI-Search & Traditional Search Verification

- **Objective:** Benchmark and analyze how William Elias appears across traditional search engines (Google, Bing) and AI search engines (ChatGPT Search, Microsoft Copilot, Perplexity).
- **Tasks:**
  - [x] Execute branded queries and evaluate entity disambiguation.
  - [x] Execute targeted professional queries and evaluate technical keyword relevance.
  - [x] Analyze citations, factual accuracy, hallucination risks, and source provenance in `documentation/search_visibility_report.md`.
  - [x] Record comparative findings and strategic recommendations.
- **Dependencies:** D0 baseline queries, D2 SEO, D3 cross-links.
- **Acceptance Criteria:** Structured test logs recorded with dates, queries, platforms, observations, and limitations.
- **Status:** **COMPLETE**

---

### Milestone D8: Visual, Factual, Accessibility & Release Audit

- **Objective:** Perform end-to-end regression validation, accessibility verification, and release preparation.
- **Tasks:**
  - [x] Capture post-implementation screenshots across all four themes and two viewports in `documentation/screenshots/final/`.
  - [x] Validate WCAG AA contrast compliance, keyboard focus, and screen-reader accessibility.
  - [x] Verify 100% test pass on pytest suite (419 tests) and all generated files.
  - [x] Prepare clean release documentation with clear commit history.
- **Dependencies:** D1 through D7.
- **Acceptance Criteria:** Zero test regressions, zero broken links, perfect contrast across 4 themes, all artifacts fresh and byte-identical where required.
- **Status:** **COMPLETE**
