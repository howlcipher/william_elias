# Targeted résumé validation

2026-11-17 local publication candidate. The October validation and its historical claim comparisons remain in Git at `55e429e`. The [career evidence reconciliation](career_evidence_reconciliation.md) governs the current candidate.

## Test Impact Assessment

| Observable change | Coverage and tier |
| --- | --- |
| Corrected professional technology, contribution, and rollout boundaries | Canonical factual contract tests check portal stack and shared implementation, distinct C# discovery and Python history tooling, prototype limitations, and stale-claim exclusions across recruiter surfaces. Superseded numerical assertions and older stack requirements were replaced with assertions about units, scope, and status. Duplicated historical metric checks were consolidated. HBK outcome checks remain explicit. |
| Three different résumé priorities and independent attribution | Variant selection contract tests check eligibility, order, and ID validation. Render integration tests check official titles, qualifications, selected achievements and projects, ATS order and keywords, annotations, page counts, and the new text-boundary assertion. Visual inspection complements bounding boxes for overlap and section flow. |
| LinkedIn draft and updated banner | The profile contract compares official title, canonical About, and selected accomplishments with software résumé text. Banner rendering tests require canonical title, tagline, and supporting line. Freshness integration builds each artifact in two isolated directories. |
| Card order, disclosures, and mobile access | Browser acceptance tests cover responsive and contrast themes, keyboard access, navigation, no-JavaScript operation, primary résumé placement, contact visibility, disclosure expansion, download contents, and the compatibility URL. Synthetic layout tests retain rendering coverage for optional metrics and context lines without restoring disputed figures. |

The smallest checks were data contracts and render tests. Artifact and browser acceptance were warranted because the canonical change crosses all generated outputs. No external publication or employer-system integration was exercised. Employer evidence and mail delivery are outside the local regression gate.

## Commands and results

Python 3.12.14, pinned dependencies, Poppler, and the pinned Chromium headless shell. Pytest ran serially with one browser worker. The open interactive Firefox session was left alone.

| Command or check | Result |
| --- | --- |
| `python -W error scripts/build_config.py`, `build_html.py`, `generate_resume_pdf.py`, `generate_linkedin_banner.py`, `generate_linkedin_profile.py` | Ran all five generators. |
| `PYTHONPATH=. pytest -q tests --ignore=tests/test_browser.py --ignore=tests/test_generated_artifacts.py -W error` | Staged failures exposed obsolete factual assertions and clipped project headings. After corrections, 315 passed in the fast gate. |
| `PYTHONPATH=. pytest -q tests/test_browser.py -W error` | 72 passed in the staged Chromium run. |
| `PYTHONPATH=. pytest -q tests/test_build_html.py tests/test_resume_variants.py tests/test_browser.py::test_mobile_resume_visible_without_opening_menu -W error` | 95 passed after the final banner and mobile assertions. |
| `PYTHONPATH=. pytest -q tests/ -W error` | Final full regression, 412 passed in 81.51 seconds. Zero failures or skips. |
| `pdfinfo`, `pdftotext`, `pdftoppm -r 85 -png` | All targeted résumés are two pages. Text extracts in order. All six pages inspected visually for clipping, overlap, and section breaks. |
| `cmp William_Elias_Resume.pdf William_Elias_Production_DevOps_Resume.pdf` | Identical bytes. |
| Generated HTML fragment and file scan, `curl --location` on public links | Local navigation and PDF targets resolved. The live portfolio, four existing PDF URLs, LinkedIn destination, and public project destinations returned HTTP 200. Live PDF contents reflect the currently published site. |
| `git diff --check` | Passed. |

The final regression includes all eleven generated artifacts and checks byte-for-byte equality across isolated builds. The public project tests, hosted CI, other browser engines, employer verification, and LinkedIn publishing were outside the executed checks.

## Second review

Re-read the candidate against the November audit leads and inspected extracted text, page renders, and the banner. The portal's shipping statement is limited to selected modules with shared contributions. The CLI remains a prototype. Discovery, history cleanup, and credential lifecycle are separate. The delivery narrative distinguishes inventory, build verification, dry runs, and actual deployment. Retained HBK outcomes carry owner-profile provenance. The independent project descriptions match inspected public source, with beta and experimental qualifiers where appropriate. Employer questions remain in the [evidence record](career_evidence_reconciliation.md).

## Git

The existing checkout started clean on `main` at `1bbf940`. After fetching, the work continued on `career-evidence-reconciliation` based on current upstream `55e429e`. The changes are local and uncommitted.

Changed files
- `.github/workflows/ci.yml`
- `README.md`
- `William_Elias_Production_DevOps_Resume.pdf`
- `William_Elias_Resume.pdf`
- `William_Elias_Security_Automation_Resume.pdf`
- `William_Elias_Software_Platform_Resume.pdf`
- `assets/images/linkedin-banner.png`
- `change_log.md`
- `documentation/ARCHITECTURE.md`
- `documentation/portfolio_optimization_handoff.md`
- `documentation/targeted_resume_validation.md`
- `index.html`
- `preview.jpg`
- `resume.json`
- `resume_variants.json`
- `scripts/generate_linkedin_banner.py`
- `scripts/generate_resume_pdf.py`
- `style.css`
- `tests/test_artifact_first_layout.py`
- `tests/test_browser.py`
- `tests/test_build_html.py`
- `tests/test_factual_corrections.py`
- `tests/test_generated_artifacts.py`
- `tests/test_hiring_contract.py`
- `tests/test_pdf_skill_context.py`
- `tests/test_promotion.py`
- `tests/test_resume_content.py`
- `tests/test_resume_variants.py`
- `tests/test_seo_and_navigation.py`
- `documentation/career_evidence_reconciliation.md`
- `documentation/linkedin_profile.md`
- `scripts/generate_linkedin_profile.py`

### Open Source layout follow-up

`style.css` now places the existing nine project cards in three evenly sized desktop columns. Smaller viewports retain a single column and content-sized rows. No generated files require rebuilding for the stylesheet change.

The existing project link and responsive overflow checks still apply. They did not cover column counts or equal desktop card dimensions. The focused Chromium acceptance test adds those assertions at 1024 and 1440 pixels and verifies the mobile single-column layout at 390 pixels. The two desktop cases reproduced the imbalance before the fix. No test contracts were removed or weakened.

Focused browser regression passed 24 tests. Final serial `PYTHONPATH=. pytest -q tests/ -W error` passed 415 tests with zero failures or skips.

## Final career audit follow-up

Starting point `2ddb937`, clean `main`, with work on local branch `final-career-audit`. The agent requests contained public source excerpts and the proposed wording. No employer records were supplied to either reviewer. Review feedback was treated as editorial input.

| Finding | Claude | AGY | Codex assessment | Decision | Evidence |
| --- | --- | --- | --- | --- | --- |
| Shared portal and staged releases read too cautiously | Unavailable | Sharpen ownership and rollout verbs | Direct work can be stated with specific actions. Leadership and broader deployment need evidence. | MODIFY | `ach-internal-dotnet-app`, `ach-portal-controls`, `ach-cicd-validation` |
| Portal runtime might be a preview | Unavailable | Generalize or use .NET 8 | .NET 10 was released in November 2025. The owner-provided audit identifies this version. Employer deployment remains provisional. | REJECT | [Microsoft support policy](https://dotnet.microsoft.com/en-us/platform/support/policy), evidence ledger |
| Remove canceled migration from résumé | Unavailable | Feature completed discovery | Integrity checks and redacted reporting are in scope. Specific detection mechanisms and migration execution lack evidence. | ACCEPT | `highlight-discovery-boundary`, `program-security-remediation` |
| Change generic résumé to software | Unavailable | Remap compatibility alias | Existing recipients expect the production version. Change the site’s primary action while preserving the alias contract. | MODIFY | Variant listing and compatibility configuration |
| Move Python above incident diagnosis | Unavailable | Reorder software résumé and LinkedIn | Keep the requested order and sharpen Python's deliverables. Preserve diagnosis as the lead on Production & DevOps. | MODIFY | `ach-python-tooling`, software and production selections |
| Reduce repeated portal and rollout material | Unavailable | Replace related highlights | Keep nonduplicated details on module architecture and verification boundaries. Put capability statements in What I Build and evidence in Selected Work. | MODIFY | `whatIBuild`, `highlight-modular-architecture`, `highlight-rollout-validation` |
| Add HBK to LinkedIn | Unavailable | Generate full earlier career | Generate the relevant HBK entry from the same selection as the software résumé. Keep the figures owner-reported in the ledger. | MODIFY | `exp-hbk`, LinkedIn Earlier Experience |
| Confirm claims about production and security scope | Unavailable | Suggested stronger rollout phrasing | Release counts, leadership scope, completed restoration, and credential actions require approved evidence. | NEEDS EVIDENCE | Evidence ledger |

Claude Code's default model requested usage credits and the Sonnet initial attempt timed out. AGY completed the independent first round. Both agents received the consolidated candidate for one final adversarial round. Claude Sonnet and AGY both timed out without findings in that round. The candidate has Codex review and test evidence.

### Test impact and verification

The observable changes are the sole primary résumé action, targeted skills, completed-work discovery highlight, and canonical HBK block in the LinkedIn package. Browser acceptance continues to exercise all three résumé downloads through their supported entry points, plus project grid, navigation, contact, contrast, and keyboard behavior. The filename, alias, ownership, status, no-inflation, and artifact assertions still apply.

The new contracts check that security describes completed discovery and that LinkedIn carries canonical HBK achievements. Assertions about primary listing were updated for the requested single-primary hierarchy. The skills fallback fixture removes the variant tag override so it still reaches the fallback it is intended to test. Fast verification found project names in unselected PDFs when the shared attribution line named featured projects. Restoring attribution-only copy fixed the content, preserving the existing selection assertions. No new generator or dependencies were needed.

Five generators ran with Python 3.12 and `-W error`. The fast suite excluded browser and isolated artifact tests for staging and passed 320 tests after corrections. The final serial gate includes both suites. Poppler rendered the six pages for visual inspection. PDF HTTPS annotations returned HTTP 200 and the email annotation was syntax checked.
