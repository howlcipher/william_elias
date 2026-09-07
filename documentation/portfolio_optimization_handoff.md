# Portfolio optimization handoff

The inherited portfolio optimization is implemented. The website retains broad software, DevOps, automation, production, and security positioning; the PDF remains a selective two-page companion. This document separates inherited work from the final corrections and records evidence and practical limits.

## 1. Scope and inherited state

Started on `main` at `07ac83e`, with 15 modified files, three untracked additions, and nothing staged. `git worktree list` showed only this checkout. Preserved the inherited title, three-paragraph About, independent metrics, Engineering Impact, source-specific claim tests, conservative employment language, selected project pair, static template, metadata, and visual identity. The initial targeted reproduction returned 63 passes and the two reported failures: stale README metrics and a premature navigation assertion.

## 2. Positioning and content hierarchy

The headline remains “Software, DevOps & Automation Engineer.” Software and automation evidence leads; official employment titles remain unchanged. Website order is Hero → metrics → About → Engineering Impact → Professional Experience → Open Source → Core Expertise → Education → Contact. Earlier Experience stays within Professional Experience on the website and has a compact separate PDF section.

## 3. Metrics and evidence provenance

README now matches the canonical metrics: `~60` applications in delivery standardization scope, `100+` repositories credential-remediated, and `300+` unused legacy applications retired. The `300+` claim was already in committed `resume.json` at `07ac83e`. Each headline metric and PDF highlight names its own `sourceProgram`; tests retain that specific evidence relationship rather than searching the entire résumé for matching numbers.

## 4. Conservative claims

Retained 56 definitions across 28 applications, 27/28 verified builds, 25/28 dry-run deployment paths, and first deployment pending approval. The expanded delivery evidence explicitly says zero applications have deployed through the new framework. “Co-led” infrastructure/DR work and “Contributed” Application Insights proof-of-concept work remain qualified. No new employment accomplishments were introduced. Project, coursework, and proof-of-concept technologies do not imply production orchestration experience.

## 5. Expandable evidence and static rendering

Six Engineering Impact cards show outcomes with native `details` / `summary` disclosures for implementation and validation. Keyboard Enter/Space and no-JavaScript operation are verified. The inherited HTML template is `scripts/site_template.html`; `index.html` is output. The inherited section-order-aware navigation remains intact. No frontend framework, architecture migration, or SEO rebuild was introduced.

## 6. PDF experience qualifiers

Added optional `skills[].pdfContext`, validated as a non-empty string when present. It renders in 10-point italic text immediately beside its category before the tags. Current qualifiers are “Internal tools & projects” for AI-Enabled Engineering and “Projects & container-host proof of concept” for Additional Hands-On Technologies. The existing `GitHub Actions (projects)` tag remains. Omitted fields preserve the unqualified category format. Tests cover omission, valid rendering, invalid types/empty values, the current qualifiers, and pagination.

## 7. PDF pagination and visual inspection

Artifact: [`William_Elias_Resume.pdf`](../William_Elias_Resume.pdf).

Regenerated with the inherited whole-section keep-together calculation. Both pages were rendered at 1.6× and visually reviewed. Exactly two Letter pages remain. All three engineering highlights and their bullets/technology lines stay together at the top of page two, followed by HowlPlane and Baseball Optimizer, earlier employment, and education. Professional summary, current employment, and all included expertise categories remain on page one.

No clipping, overlapping text, broken wrapping, misaligned dates, or orphaned highlight headings were found. Body text and bullets remain 10 points; small supporting typography is 9–9.5 points. Paragraphs and bullets are left-aligned, and qualifications wrap legibly. Content occupies approximately y=21–656 points on page one and y=33–618 on page two, leaving about 136 and 174 points of bottom whitespace respectively. This whitespace is accepted to preserve the two-page structure and grouped highlights. Six link annotations are inside the page bounds: email, LinkedIn, GitHub, portfolio, and both selected repositories. The PDF is text-extractable; a tagged-PDF accessibility audit was not performed.

## 8. Generated artifacts and repeatability

All three generators ran under Python 3.12.14 using `requirements-dev.txt`: pytest 9.0.3, Playwright 1.60.0, pytest-playwright 0.8.0, fpdf2 2.8.7, pypdf 6.14.2, and Pillow 12.3.0. Six outputs are checked: `config.js`, `index.html`, `robots.txt`, `sitemap.xml`, `preview.jpg`, and the PDF.

New tests construct two separate temporary directories containing only canonical JSON, generator scripts, source HTML template, and assets. They run each CLI with warnings treated as errors, compare both independent builds byte-for-byte, and compare every output to the checked-in copy. Root outputs are never overwritten by those tests. PDF creation time remains fixed and compression remains disabled. Social-preview rendering uses Pillow's bundled font rather than a machine-specific font file. The 1200 × 630 preview was visually inspected for text wrapping, portrait alignment, and preserved identity.

## 9. Navigation and browser contracts

Replaced fixed navigation sleeps with bounded checks of the requested scroll destination and `aria-current` state. Tests wait for fonts before scrolling, since late font metrics can move the target. The check clamps the desired position to the document's scrollable range. Existing active-state, underline, logo-return, and résumé-not-active assertions remain; smooth scrolling is unchanged.

Browser coverage now includes all six actual navigation links on desktop and mobile, menu closure, Escape/focus return, keyboard theme and contrast controls, native evidence disclosure, no-JavaScript content/disclosure, four real PDF downloads compared byte-for-byte, and all six project popup destinations. Project popup tests stub the destination response; separate live verification checks availability.

## 10. Visual and accessibility review

Captured all 20 width/theme combinations: 320, 390, 810, 1024, and 1440 pixels, each in dark, light, dark contrast, and light contrast. Fresh viewport, full-page, section, expanded-evidence, focus, and PDF images total 78 files. All 20 website captures report zero horizontal overflow, broken images, and uncaught page errors. Reviewed the responsive hero layouts, desktop/mobile text hierarchy, card alignment, tag wrapping, employment chronology, contact actions, expanded evidence, and visible keyboard focus.

The review found a small dark-mode role title at 3.87:1 contrast. Added a dedicated `--red-text` token (`#ff6060` in dark mode), preserving the existing decorative red accents and other theme colors. A browser regression asserts at least 4.5:1 for the mobile title in every theme. This is targeted accessibility verification, not a claim of comprehensive WCAG certification or screen-reader testing.

## 11. Verification environment and results

Final gate: **202 tests passed in 54.00 seconds**, with zero failures and Python warnings treated as errors. All three generators, both lint checks, and `git diff --check` exited successfully. Freshness and independent repeat-generation checks passed for all six generated artifacts.

See the companion [evidence manifest](portfolio_optimization_evidence.json) for final commands/results, output hashes, page/link geometry, screenshot hashes, and live destination records.

The inherited `venv_ci` uses Python 3.14 and newer pytest/Playwright, so it was not used for the final gate. An isolated Python 3.12.14 environment was created at `/tmp/portfolio-ci`. This host is Ubuntu 26.04; pinned Playwright 1.60.0 rejects that host name during browser installation. Local browser commands therefore use `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64` with the matching Chromium build. Installation reports the unsupported-host fallback. The final test gate treats Python warnings as errors. This verifies Python 3.12 compatibility locally; no remote GitHub Actions execution or exact GitHub runner OS parity is claimed.

There is no configured repository flake8 job. Local flake8 checked all changed Python files with inherited long-line style retained via `--extend-ignore E501`, and both new test modules also passed default flake8. Cleaned spacing and unused imports in touched files. No runtime dependency versions were changed beyond the inherited explicit Pillow pin. Direct dependencies are pinned; transitive dependencies and platform-native libraries are not fully locked.

## 12. External destination checks

Live HTTP GET checks on 2026-09-07 reached the six project repositories, GitHub profile, source repository, live portfolio, and published PDF with expected content. No destination was confirmed broken. LinkedIn returned HTTP 200 with the title “Checking your browser - reCAPTCHA”; the profile content cannot be verified by this automated check. Web browsing also produced cache/fetch failures for some URLs that direct HTTP requests subsequently reached; these were not treated as broken links.

The published PDF was checked for availability only and predates this local commit. No email was sent, and no mail client was launched. GitHub repository “About” metadata still describes “Senior DevOps / Platform Engineer”; updating that external repository setting is deferred. Local résumé metadata uses the intended broader positioning.

## 13. Five hiring perspectives

The inherited plan did not supply the original five labels. A clarification was offered; this report uses the five disciplines named by the plan. These are evidence-based perspectives applied by one agent, not feedback from five actual recruiters or independent reviewers. Professional claims are checked against repository source consistency, not independently verified with employers.

| Perspective | Concrete evidence visible to the reader | Assessment and limit |
| --- | --- | --- |
| Software/backend hiring manager | Python/FastAPI dashboards; modular ASP.NET Core support portal; SQL Server, per-module policies, audit trail, and 156 tests; Baseball Optimizer's Rust/Axum/SQLite API | Software-building evidence appears before skill inventory and on both PDF pages. Private employer implementation was not independently audited. |
| Automation/developer-productivity recruiter | Python/PowerShell workflow tools; retirement of 300+ applications; HBK processing reduction and monthly hours saved; HowlPlane task routing and verification | Demonstrates operational automation plus reusable engineering tooling. Professional outcomes and independent projects stay distinguishable. |
| DevOps/platform hiring manager | ~60-application scope; 56 definitions across 28 applications; 27/28 builds and 25/28 dry-run paths; six defects caught before rollout | Detailed validation supports delivery engineering breadth. First production deployment through the new framework remains pending; no production Kubernetes claim. |
| Production/SRE hiring manager | Weekly releases, database migrations, incident triage, OAuth/IAM and networking diagnostics; Application Insights, KQL, structured logging; co-led DR/cutover work | Shows production operations grounded in applications and infrastructure. “Contributed” and “co-led” preserve shared ownership; no new SLO or scale claims. |
| Security-focused hiring manager | 100+ repositories credential-remediated; Git-history cleanup; Key Vault migration and integrity-verified rollback with 62 tests; credential/PII/provenance/human-review safeguards | Security is demonstrated within software and production work. Proof-of-concept and internal AI tooling remain qualified; no unsupported security-leadership claims. |

## 14. Durable evidence and reproduction

Tracked manifest: `documentation/portfolio_optimization_evidence.json`. Full local evidence and capture script: `/run/media/system/tallgeese/dev/william_elias_evidence/2026-09-07/`. The screenshot binaries remain outside the Git repository to avoid adding approximately 28 MB of review images; the committed hashes make them identifiable. They are durable on this machine but are not included in a fresh clone.

Reproduce the normal CI gate from the repository root using a Python 3.12 environment:

```bash
pip install -r requirements-dev.txt
playwright install chromium --with-deps
python scripts/build_config.py
python scripts/build_html.py
python scripts/generate_resume_pdf.py
PYTHONPATH=. pytest tests/ -W error -q
```

On this Ubuntu 26.04 host only, prefix Playwright installation/testing/capture with `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64`. Screenshot capture uses reduced motion to stabilize static images; navigation regression tests use normal smooth scrolling. Detailed section captures use an enlarged viewport height to avoid placing the fixed navigation bar across the captured element; the 20 full-page and hero captures use the normal 900-pixel viewport height.

## 15. Documentation, limitations, and deferred work

README documents the metrics, source template, social preview, Engineering Impact, field semantics, generation, and verification workflow. `change_log.md` records inherited improvements and finishing fixes. The inherited canonical URL, metadata, ProfilePage/Person graph, `sameAs`, curated `knowsAbout`, and nested WebSite data remain unchanged in this finishing pass.

Deferred: push/deployment; changing external GitHub About metadata; manually verifying LinkedIn past its challenge; Firefox/WebKit and real-device/screen-reader testing; actual recruiter feedback; transitive dependency locking and cross-platform byte equivalence beyond the tested environment. Auxiliary LinkedIn-banner generation is outside the requested three-generator build. No new accomplishments, architecture migration, or SEO rebuild are pending as part of this scope.

## 16. Commit and publication boundary

The intended changes are committed together with an SSH-signed conventional commit using the existing local signing key. Signature verification and clean-tree results are reported in the completion response and local `commit-verification.txt`. The commit containing this handoff can also be found with `git log -1 --format='%H %s' -- documentation/portfolio_optimization_handoff.md`. The handoff does not embed its own commit hash, which would change that hash. No push or deployment is authorized by this task.
