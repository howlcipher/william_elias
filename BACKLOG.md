# Engineering Backlog — william_elias

Static, config-driven resume site (HTML/CSS/vanilla JS + a Python PDF generator). Deployed via GitHub Pages from `main`. No build step, no test suite, no CI as of this writing.

This file is maintained by the BACKLOG operation. IDs are stable and never renumbered. Completed items keep their ID and move to the Completed section with history preserved.

**Last full audit:** 2026-07-31

---

## 1. Critical Bugs

*(None currently open. REL-001 — content that never becomes visible under a real failure condition — was the closest thing to a critical defect; fixed 2026-08-01, see Completed section.)*

## 2. Reliability

## 3. Accessibility

## 4. Security
## 5. Data and Build Architecture


## 6. Testing and CI

## 7. Repository Maintenance

## 8. Portfolio Enhancements

### ENH-001 — Support optional per-project links without inventing URLs

**Type:** Enhancement
**Priority:** Low
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `config.js`, `script.js`, `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-05)

### Done note
Added optional `link` rendering to project cards in `script.js` (rendered using `getValidUrl` as a `.contact-pill`), and added schema validation for `proj.link` (if present) in `scripts/generate_resume_pdf.py`. No invented URLs were added; the fields are omitted when not supplied.

---

### ENH-004 — SEO meta tag generation lacks proper HTML attribute escaping

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `scripts/build_html.py`
**Status:** Done (2026-08-05)

### Done note
Replaced ad-hoc string formatting in `build_html.py` with `html.escape(..., quote=True)` to properly escape double quotes and angle brackets in SEO meta tag `content` attributes.
`build_html.py` replaces `<meta>` tag contents by directly inserting values like `page_title` and `tagline` into `content="..."` attributes using f-strings. It replaces `&` with `&amp;` for `page_title`, but doesn't properly escape double quotes (`"`) or angle brackets (`<`, `>`). If the owner's `name`, `title`, or `tagline` in `resume.json` ever contains double quotes, it will prematurely terminate the `content` attribute and break the HTML structure.

### Proposed work
Use a standard HTML escaping function (like `html.escape(..., quote=True)` from Python's standard library) when interpolating strings into `index.html` attributes in `build_html.py`, replacing the ad-hoc `.replace('&', '&amp;')`.

### Acceptance criteria
- Generated meta tag content attributes are properly HTML-escaped.
- Double quotes in `resume.json` strings do not break `index.html` syntax.

### Validation
- Manual: Add a double quote to `tagline` in `resume.json`, run `python scripts/build_html.py`, and inspect `index.html` to ensure it is escaped as `&quot;`.

### ENH-002 — Consider stronger project evidence (screenshots, demos, case studies)

**Type:** Enhancement
**Priority:** Low
**Effort:** L
**Risk:** Low
**Recommended mode:** Planning
**Recommended model tier:** Standard
**Dependencies:** ENH-001 (if links are part of the evidence)
**Affected files:** `config.js`, `index.html`, `style.css`, new asset files
**Status:** Blocked — needs owner input on what evidence exists/should be created (screenshots, demo recordings, written case studies)

### Problem

The Projects section (`config.js:120-142`) currently shows only text highlights and tags — no visual evidence (screenshots, architecture diagrams) or deeper case-study content for either project.

### Proposed work

This is a planning/scoping item pending owner direction on what supporting material exists or should be created. Once scoped, break into independently shippable sub-items (e.g., "add screenshot to AI Knowledge Library card," "add architecture diagram," "add expandable case-study detail") rather than one large content overhaul.

### Acceptance criteria

- N/A until scoped — this item's completion criterion is "owner direction gathered and follow-up items filed," matching the same pattern as ARCH-002.

### Validation

- N/A (planning item).

### Notes

Explicitly kept separate from bug fixes per operating instructions. Do not invent screenshots, metrics, or claims — this depends entirely on real material the owner provides.

---

## 9. Completed

### ARCH-009 — CI does not verify freshness of config.js and index.html

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** ARCH-006, ARCH-007
**Affected files:** `.github/workflows/ci.yml`
**Status:** Done (2026-08-04)

### Done note
Updated `.github/workflows/ci.yml` to run `python scripts/build_config.py` and `python scripts/build_html.py` before checking for uncommitted changes with `git diff --exit-code config.js index.html William_Elias_Resume.pdf`.

---

### MAINT-002 — README overstates drift-proofing and omits the real workflow

**Type:** Maintenance
**Priority:** Low
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** Loosely follows ARCH-002/ARCH-005/TEST-004 (README should describe the actual final workflow, not get rewritten repeatedly as those land)
**Affected files:** `README.md`
**Status:** Done (2026-08-04)

### Done note
Rewrote README.md to reflect the new architecture with `resume.json` as the single source of truth, explain the build steps, remove the overstated claim about drift-proofing, and provide a single end-to-end validation command.

---

### TEST-004 — No single documented local validation command

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** TEST-001, TEST-002, ARCH-003
**Affected files:** `README.md`
**Status:** Done (2026-08-04)

### Done note
Added an end-to-end local validation command sequence to `README.md` under "Local Development & Validation".

---

### ENH-003 — Add `requirements-dev.txt` for development dependencies

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `requirements-dev.txt`, `.github/workflows/ci.yml`
**Status:** Done (2026-08-04)

### Done note
Created `requirements-dev.txt` listing `pytest`, `playwright`, `fpdf2`, and `pypdf`. Updated `.github/workflows/ci.yml` to install dependencies from this file instead of a hardcoded list.

---

### ARCH-005 — PDF generation is not verified deterministic/current in CI

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** TEST-003 (this is effectively a specific check within that CI job)
**Affected files:** CI config (new), `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-04)

### Done note
Updated `scripts/generate_resume_pdf.py` to use a fixed `creation_date` making the PDF byte-for-byte deterministic. Added a step to `.github/workflows/ci.yml` that generates the PDF and checks for uncommitted changes using `git diff --exit-code`.

---

### ARCH-006 — Introduce `resume.json` and generate `config.js`

**Type:** Improvement
**Priority:** Medium
**Effort:** M
**Risk:** Medium
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `resume.json`, `scripts/build_config.py`, `config.js`
**Status:** Done (2026-08-04)

### Done note
Created `resume.json` from `config.js`, created `scripts/build_config.py`, regenerated `config.js`, and updated tests.

---

### ARCH-007 — Generate static SEO meta tags from `resume.json`

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** ARCH-006
**Affected files:** `scripts/build_html.py`, `index.html`
**Status:** Done (2026-08-04)

### Done note
Created `scripts/build_html.py` to inject SEO meta tags into `index.html` from `resume.json`.

---

### ARCH-008 — Point PDF generator at `resume.json`

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** ARCH-006
**Affected files:** `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-04)

### Done note
Updated `generate_resume_pdf.py` to read `resume.json` via json.loads, removed the dirty JS regex parsing, and cleaned up tests.

---

### ARCH-002 — Evaluate a canonical structured resume data source (`resume.json`)

**Type:** Improvement
**Priority:** Medium
**Effort:** L
**Risk:** Medium
**Recommended mode:** Planning
**Recommended model tier:** High reasoning
**Dependencies:** None
**Affected files:** New `resume.json` (or similar), `config.js`, `scripts/generate_resume_pdf.py`, potentially `index.html` (SEO meta tags), build tooling
**Status:** Done (2026-08-04)

### Done note
Evaluated canonical source approach. Decided to pursue it. Added ARCH-006, ARCH-007, and ARCH-008 to the backlog for implementation.

### Problem

Resume content currently exists redundantly across four places that can drift independently: `config.js` (the site's source of truth), `index.html`'s hardcoded Open Graph/SEO meta tags (`index.html:6-13`, duplicating name/title/description), `preview.jpg` (a static screenshot that needs manual regeneration whenever the visual resume changes), and `William_Elias_Resume.pdf` (generated from `config.js` via a fragile regex parser — ARCH-001). There is no single canonical data source that all four derive from mechanically.

### Proposed work

This is a planning/design item, not an implementation item — evaluate whether introducing a canonical `resume.json` (or equivalent) is worth the added build-step complexity for a static site that currently has none. If yes, scope it as a **sequence of small, independently shippable items** rather than one large refactor, e.g.:
- Introduce canonical resume schema (`resume.json` + a documented shape)
- Generate `config.js` from canonical data (or eliminate `config.js` in favor of the browser loading `resume.json` directly)
- Generate static SEO/OG meta tags from canonical data
- Point PDF generator at canonical data directly (resolves ARCH-001)
- Document the generated-file workflow (ties into MAINT-002)

Each sub-item should be filed as its own `ARCH-###` entry once this evaluation is complete and the approach is decided, with this item's outcome being "decision made + follow-up items filed," not a full implementation.

### Acceptance criteria

- A documented decision (in this backlog item's Notes, or a short ADR if the project's conventions call for one) on whether to pursue the canonical-source architecture, with pros/cons considered (build-step complexity added to a currently zero-build static site vs. drift risk eliminated).
- If pursued: follow-up items filed for each independently shippable step, each leaving the repo in a working, deployable state.
- If deferred: rationale recorded so this doesn't get silently re-litigated.

### Validation

- N/A (planning item) — validation is peer/owner review of the decision and resulting item breakdown.

### Notes

Per the operating instructions for this backlog, do not create one large "refactor everything" item — this item exists specifically to produce that breakdown, not to do the refactor itself. Static GitHub Pages compatibility must be preserved regardless of outcome — any generation step must run at commit/CI time, not require a server at request time.

---

---

### ARCH-004 — PDF output has no document metadata

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-04)

### Done note
Added pdf.set_title, pdf.set_author, and pdf.set_creator to the FPDF initialization in scripts/generate_resume_pdf.py.

### Problem

`ResumePDF.__init__` (`scripts/generate_resume_pdf.py:26-30`) never calls `set_title`/`set_author`/`set_subject`/`set_creator`. The generated PDF's document properties are whatever `fpdf2` defaults to (typically blank), so the file shows no title/author metadata in PDF viewers, browser tabs (when opened directly), or OS file previews.

### Proposed work

Call `pdf.set_title(...)`, `pdf.set_author(config["personal"]["name"])`, and similar metadata setters in `build()`, sourcing values from the already-loaded config.

### Acceptance criteria

- Generated PDF's document properties (visible via `pdf metadata`, most PDF viewers' "Document Properties," or `pdfinfo`) show a meaningful title and author.
- No change to visible PDF page content.

### Validation

- Run `python3 scripts/generate_resume_pdf.py` and inspect metadata with `pdfinfo William_Elias_Resume.pdf` or equivalent.

### Notes

Small, isolated, good "quick win" item.

---

### ARCH-003 — No schema validation for resume config data

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None (independent of ARCH-002 — useful whether or not a canonical source is introduced)
**Affected files:** `scripts/generate_resume_pdf.py`, possibly a new small validation script
**Status:** Done (2026-08-04)

### Done note
Implemented validate_config in scripts/generate_resume_pdf.py which checks that all required top-level fields are present, expected lists are arrays, and personal URLs have valid protocol schemas. Added corresponding tests.

### Problem

Neither the browser (`script.js`) nor the PDF generator (`scripts/generate_resume_pdf.py`) validates `config.js`/parsed-config data before using it. Missing fields, malformed arrays, or invalid URL values would currently fail unpredictably — a missing `achievements` array throws inside `.map()`, a malformed `linkedin` URL renders as a broken link with no warning, etc. There's no single point that catches these before they reach either output.

### Proposed work

Add a lightweight validation pass (Python, run as part of or before PDF generation) that checks required fields are present, arrays are actually arrays, and URL-shaped fields look like URLs, failing with a clear, specific error message before generation proceeds. This does not need a full schema library — plain Python assertions/checks are sufficient for this project's size and language preferences (Python preferred per project conventions).

### Acceptance criteria

- Running the validation against the current `config.js` passes cleanly.
- Running it against a deliberately broken copy (missing required field, non-array `achievements`, malformed URL) fails with a specific, actionable error message rather than an unrelated traceback.
- Validation is easy to invoke as a single documented command (ties into TEST-004).

### Validation

- Manual: run against current config (pass) and against 2-3 deliberately broken variants (each fails with a clear message).

### Notes

Worth doing regardless of the ARCH-002 canonical-source decision — the validation logic is cheap and useful either way, just potentially validates a different file shape depending on that outcome.

---

### ARCH-001 — PDF generator parses `config.js` with regex instead of a real data source

**Type:** Improvement
**Priority:** Medium
**Effort:** M
**Risk:** Medium
**Recommended mode:** Coding
**Recommended model tier:** High reasoning
**Dependencies:** None (but see ARCH-002, which would obsolete this approach)
**Affected files:** `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-04)

### Done note
Implemented the stopgap fix: wrapped `json.loads` in a `try...except` block in `load_config()` to fail loudly with a clear, specific error message explaining the regex parsing failure and its likely cause (complex JS-only syntax).

### Problem

`load_config()` (`scripts/generate_resume_pdf.py:17-23`) parses the JS module by string-splitting on `=`, stripping a trailing `;`, and using two regexes to coerce unquoted object keys and trailing commas into valid JSON before `json.loads`. This works today because `config.js`'s object literal happens to stay close to JSON syntax, but it's fragile: any future use of JS-only syntax in `config.js` (template literals, comments, single-quoted strings, computed properties, trailing function calls) will silently break or misparse the PDF generator with no clear error message pointing at the cause.

### Proposed work

This is directly superseded by introducing a canonical structured data source (ARCH-002/ARCH-003) — if that work proceeds, this item's proper resolution is "PDF generator reads `resume.json` directly," which is trivial once that source exists. If the canonical-source work is deferred, harden the current regex parser with clearer error handling (fail loudly with a specific message when `json.loads` fails, rather than an opaque `JSONDecodeError`) as a stopgap.

### Acceptance criteria

- Either: PDF generator reads from a canonical JSON/structured source with no regex-based JS parsing (preferred, depends on ARCH-002/003), or: parse failures produce a clear, actionable error message identifying the likely cause.
- Existing PDF output is unchanged for the current `config.js` content.

### Validation

- Manual: run `python3 scripts/generate_resume_pdf.py`, confirm output PDF matches current tracked `William_Elias_Resume.pdf` content.
- Manual: intentionally introduce a JS-only construct (e.g. a template literal) into a scratch copy of `config.js` and confirm the parser either handles it or fails with a clear message rather than a cryptic traceback.

### Notes

Don't implement this independently of the ARCH-002/003 decision — check whether the canonical-source work is planned before investing effort in hardening the regex approach, since it may be thrown away.

---

### TEST-002 — No automated tests for the PDF generator

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** New test file (e.g. `scripts/test_generate_resume_pdf.py`), `scripts/generate_resume_pdf.py`
**Status:** Done (2026-08-04)

### Done note
Implemented pytest-based unit tests for load_config() and layout calculations. Tests pass and integrate with CI.

### Problem

`scripts/generate_resume_pdf.py` has no tests. `load_config()`'s regex-based parsing (ARCH-001) and the `keep_together`/`bullet_height` orphan-prevention logic are exactly the kind of fragile-but-important logic that benefits from unit coverage, since failures would otherwise only surface as visually broken PDF output discovered by manual inspection.

### Proposed work

Add `pytest`-based unit tests (Python preferred per project conventions) for `load_config()` against representative `config.js`-shaped input, and for `bullet_height`/`keep_together` page-break behavior. Full visual PDF diffing is out of scope — focus on the parsing and layout-calculation logic that's most likely to silently break.

### Acceptance criteria

- Tests exist and pass for `load_config()` parsing at least one realistic sample.
- Tests exist for orphan-prevention logic (`bullet_height` returns expected line counts for known input).
- Tests runnable via a single documented command.

### Validation

- Run `pytest scripts/` (or equivalent), confirm all pass.

### Notes

Smaller and more contained than TEST-001 — good candidate to do first if sequencing tests before browser-behavior tests is preferred.

---

### TEST-003 — No CI pipeline

**Type:** Improvement
**Priority:** High
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** TEST-001 and/or TEST-002 (needs something to run — can start with whichever test suite lands first)
**Affected files:** New `.github/workflows/*.yml`
**Status:** Done (2026-08-04)

### Problem

There is no `.github/workflows` directory and no CI configuration at all. Nothing runs automatically on push or PR — no linting, no tests (none exist yet), no generated-file freshness check. GitHub Pages deployment for this repo appears to be classic branch-based Pages (serving directly from `main`, not an Actions-based deploy — no workflow file exists to do otherwise), so CI here is purely a verification gate, not a deployment mechanism.

### Proposed work

Add a GitHub Actions workflow that runs on push/PR: the test suite(s) from TEST-001/TEST-002 once they exist, and (once available) the PDF-freshness check from ARCH-005. Explicitly scope the workflow to verification only — it must not deploy, push commits, or otherwise mutate the repository, per repository constraints.

### Acceptance criteria

- A workflow file exists and runs on push/PR to `main`.
- The workflow fails when tests fail and passes when they succeed (verify with an intentionally broken test).
- The workflow performs no writes back to the repository (no auto-commits, no deploy step).

### Validation

- Push a branch with an intentionally failing test (or open a draft PR), confirm the workflow fails; fix it, confirm it passes.

### Notes

Marked Blocked until at least one of TEST-001/TEST-002 exists to give the pipeline something to run — implementing CI with nothing to check would be low-value. Recommended order: TEST-002 (smaller) → TEST-003 (CI running that) → TEST-001 (expand coverage) → ARCH-005 (add PDF-freshness check to the now-existing pipeline).

**Done note (2026-08-04):** Implemented GitHub Actions CI workflow in `.github/workflows/ci.yml` that runs the headless browser tests using pytest and playwright on push/PR to `main`.

---
### MAINT-001 — Tracked `.directory` desktop metadata file, no `.gitignore`

**Type:** Maintenance
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `.directory` (remove), new `.gitignore`
**Status:** Done (2026-08-04)

### Problem

`.directory` (`[Desktop Entry]\nIcon=folder-important`) is tracked in the repository — this is KDE/Dolphin desktop-environment metadata, not project content, and shouldn't be version-controlled. There is also no `.gitignore` at all, so any future local editor/OS artifacts (`.DS_Store`, `__pycache__/`, editor swap files, etc.) risk being accidentally committed.

### Proposed work

`git rm .directory` and add a `.gitignore` covering common OS metadata (`.directory`, `.DS_Store`), Python artifacts (`__pycache__/`, `*.pyc`), and common editor swap files.

### Acceptance criteria

- `.directory` is removed from the repository.
- A `.gitignore` exists covering the categories above.
- No project-relevant tracked files are accidentally ignored (verify `git status` shows nothing unexpected after adding `.gitignore`).

### Validation

- `git status` after the change shows `.directory` removed and no unintended untracked/ignored files.

### Notes

Trivial, zero-risk — good first/quick item.

**Done note (2026-08-04):** Created `.gitignore` ignoring common files and `__pycache__`. Untracked `tests/__pycache__` and removed tracked `.directory`.

---

### TEST-001 — No automated regression tests for browser behavior

**Type:** Improvement
**Priority:** High
**Effort:** M
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None (but naturally exercises REL-001, REL-002, REL-005, A11Y-001 — best done after or alongside those fixes so tests capture the corrected behavior)
**Affected files:** New test files (e.g. under a `tests/` directory), `script.js`
**Status:** Done (2026-08-04)

### Problem

There is no test framework, test file, or automated check for any of `script.js`'s browser-side behavior — storage fault-tolerance, `IntersectionObserver` fallback, malformed API response handling, or mobile-menu keyboard behavior. Every one of the reliability/accessibility bugs above was found by manual code reading, not by a failing test, and any future regression would similarly go unnoticed until manually discovered.

### Proposed work

Add a lightweight test suite covering, at minimum: `formatRelativeTime`/`renderLastSynced` output for known inputs, storage-failure fallback behavior (REL-002), malformed API response handling (REL-005), `IntersectionObserver`-unavailable fallback (REL-001), and mobile-menu open/close/Escape behavior (A11Y-001). Given the project's static/vanilla-JS nature and stated dependency-sprawl aversion, prefer a minimal-dependency approach — a small headless-browser test runner (e.g. Playwright or a lighter alternative) is reasonable since this is dev-only tooling that doesn't touch the shipped site, but keep the choice deliberate and documented rather than defaulting to a heavy framework.

### Acceptance criteria

- Test suite runs via a single documented command (ties into TEST-004).
- Tests cover each of the specific behaviors listed above.
- Tests fail (before the corresponding fix) and pass (after) for at least REL-001, REL-002, and REL-005, demonstrating they actually catch the bugs they're meant to guard.
- Test tooling is dev-only — no impact on the shipped static site or its dependency footprint.

### Validation

- Run the test suite locally; confirm pass/fail status matches expectations against both the pre-fix and post-fix code (can be verified via git stash/checkout during test-writing).

### Notes

This is naturally sequenced after the reliability/accessibility bug fixes it's meant to cover, so the tests encode correct behavior rather than the current buggy behavior — but could also be written test-first (red/green) alongside each fix if preferred at implementation time.

**Done note (2026-08-04):** Implemented a Python `pytest` and `playwright` based headless test suite in `tests/test_browser.py` that verifies the JS browser behaviors without adding heavy JS dependencies like NPM.

---

### SEC-004 — Config-driven sections still render via unescaped `innerHTML`

**Type:** Improvement
**Priority:** Low
**Effort:** M
**Risk:** Medium
**Recommended mode:** Coding
**Recommended model tier:** High reasoning
**Dependencies:** None
**Affected files:** `script.js`
**Status:** Done (2026-08-04)

### Problem

Filed as the deferred half of SEC-001, which was scoped down to the last-synced widget only (see SEC-001's Done note, 2026-08-01). `script.js` still builds the hero (`script.js:22-34`), summary (`script.js:39`), skills (`script.js:44-53`), experience (`script.js:57-72`), projects (`script.js:74-87`), and education (`script.js:90-98`) sections via template-literal `innerHTML` assignment. All of this data currently comes from the static, owner-controlled `config.js`, so the practical exploit risk is low today (defense-in-depth, not an active vulnerability) — but it sets a pattern that would become actively dangerous if `config.js` were ever replaced by a fetched/CMS-driven source (see ARCH-002), and achievements/highlights/tags are exactly the kind of free-text fields a future content source might not fully control.

### Proposed work

Replace `innerHTML` template interpolation with `textContent` assignment and explicit DOM construction (`createElement`/`appendChild`/`textContent`) across the six sections listed above. This is a genuine refactor of `script.js`'s rendering, not a one-line fix — don't attempt it as a single diff; split it per-section (hero, skills, experience, projects, education, summary) and verify each section's visual output against the live site before moving to the next, since template literals currently also encode structural markup (wrapper `div`s, icon `i` tags, conditional contact-pill links) that has to be reconstructed correctly, not just the text nodes.

### Acceptance criteria

- None of the six sections use `innerHTML` with interpolated `config.js` values; equivalent output is built via `textContent`/DOM APIs.
- Visual output is pixel-identical to before for the current `config.js` content (this is the main risk: the current template literals encode a fair amount of conditional structure — e.g. the hero's contact pills only render if the corresponding config field is truthy — that must be preserved exactly).
- No regression to any interactive behavior tied to this markup (fade-in observer targets, `.timeline-dot`, `.skill-tags`, etc. — verify class names and structure are unchanged, not just visible text).

### Validation

- Manual: visually diff every section before/after against the live site.
- Automated: see TEST-001 — this item is a strong candidate to pair with automated regression tests precisely because "visually identical" is hard to eyeball-verify across six sections reliably by hand.

### Notes

Larger and lower-urgency than the last-synced fix (SEC-001) it was split from — the data source here is static and owner-controlled, so this is genuinely optional hardening, not an active-risk fix. Good candidate to sequence alongside or after TEST-001 exists, so the refactor has an automated safety net rather than relying purely on manual visual diffing across six sections.

**Done note (2026-08-04):** Refactored config-driven rendering in `script.js` to construct DOM nodes explicitly using `document.createElement`, `textContent`, and `appendChild`.

---

### SEC-005 — Config-driven link `href` values aren't protocol-validated

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** SEC-004 (natural to fix together at the same call site, though not strictly required — this is a small independent addition)
**Affected files:** `script.js`
**Status:** Done (2026-08-04)

### Problem

Filed as the deferred half of SEC-002, which was scoped down to the last-synced widget's `url` only (see SEC-002's Done note, 2026-08-01). `config.personal.linkedin`, `.github`, `.resumePdf`, and `.sourceRepo` (`script.js:27-32`, inside the hero template literal) are still written directly into `href` attributes with no protocol check. These are owner-controlled config values today, so practical risk is low — this is cheap defense-in-depth, not an active vulnerability.

### Proposed work

Add a small helper that validates a URL string starts with `http://`/`https://` (for `linkedin`/`github`/`sourceRepo`) or is a same-origin relative path (for `resumePdf`, which is a local file like `William_Elias_Resume.pdf`, not an absolute URL) before using it as an `href`; skip rendering the link entirely if validation fails, matching the pattern already established for the last-synced widget in SEC-002.

### Acceptance criteria

- A config value with a non-http(s)/non-relative protocol (e.g. `javascript:...`) does not get rendered as a clickable `href`.
- Normal `https://` links and the local `resumePdf` relative path are both unaffected.

### Validation

- Manual: temporarily set a config link value to `javascript:alert(1)`, confirm it's not rendered as an active link after the fix.

### Notes

Small and cheap on its own, but touches the same hero template literal SEC-004 refactors — sequence together if both are being done, otherwise this can be done standalone since it doesn't require the full `innerHTML`→DOM-API rewrite (a href-validation check works the same whether the surrounding markup is built via `innerHTML` or `createElement`).

**Done note (2026-08-04):** Added `getValidUrl` helper function in `script.js` and wrapped url variables with it before assigning them to href or src.

---
### REL-001 — `.fade-in` sections can stay permanently invisible without `IntersectionObserver`

**Type:** Bug
**Priority:** High
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `script.js`, `style.css`
**Status:** Done (2026-08-01)

### Problem

`.fade-in` elements (`style.css:564`) start at `opacity: 0` and rely entirely on `script.js:102-114` calling `IntersectionObserver` to add `.visible`. There is no `typeof IntersectionObserver === 'undefined'` guard and no `<noscript>` fallback. On any browser/environment where `IntersectionObserver` is unsupported or blocked (older browsers, some in-app webviews, aggressive privacy tools), every major section of the page — hero, about, skills, experience, projects, education — remains invisible forever with no way for the visitor to know content exists.

### Proposed work

Add a feature-detection fallback: if `IntersectionObserver` is unavailable, immediately add `.visible` to all `.fade-in` elements (or skip the class-toggling animation entirely) instead of leaving them hidden. Keep the fallback minimal — no polyfill needed, just a graceful degrade to "visible, no animation."

### Acceptance criteria

- With `IntersectionObserver` deleted/stubbed out in devtools before page load, all `.fade-in` sections are visible without scrolling interaction.
- Normal (supported) behavior is unchanged — sections still fade in on scroll.
- `prefers-reduced-motion` behavior (`style.css:112-134`) continues to work.

### Validation

- Manual: in browser devtools console before navigation, run `delete window.IntersectionObserver` via a pre-load snippet or a local test harness, reload, confirm content is visible.
- Manual: normal load, confirm fade-in animation still occurs on scroll.

### Notes

Sequencing: do this first — it's the only bug where content can become literally unreachable, and the fix is small and isolated.

**Done note (2026-08-01):** Wrapped the observer setup in `typeof IntersectionObserver === 'undefined'` (`script.js:96`); when unsupported, `.fade-in` elements get `.visible` added immediately instead of staying at `opacity: 0`. Verified via a Node harness transcribing the exact branch logic against a mocked DOM (no `IntersectionObserver` global vs. present) — both paths correctly mark all `.fade-in` elements visible. A real browser/devtools check wasn't available in this environment (no Chrome extension connected, no local Chromium/Playwright); a manual devtools spot-check per the item's Validation section is still recommended before/at next deploy.

---

### REL-002 — Theme/colorblind/last-synced `localStorage` calls are not fault-tolerant

**Type:** Bug
**Priority:** High
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `script.js`
**Status:** Done (2026-08-01)

### Problem

`script.js` reads `localStorage` safely in one place (`initLastSynced`'s cache read, wrapped in try/catch) but calls `localStorage.setItem` unguarded in five places: theme toggle, colorblind toggle, and the last-synced cache write. In Safari private browsing (older versions), storage-quota-exceeded scenarios, or environments where storage access is blocked by policy, `setItem` throws. Each throw aborted the rest of that function — in `enableColorblindMode()`, skipping the icon update; in `initLastSynced()`'s success path, discarding a successful API response and leaving the footer widget unrendered.

### Proposed work

Wrap each `localStorage.setItem`/`getItem` call in try/catch, centralized through a small helper (`safeStorage.get(key)` / `safeStorage.set(key, value)`) that swallows exceptions and returns a sentinel. Ensure the surrounding UI update (icon swap, `renderLastSynced` call) still executes even when persistence fails.

### Acceptance criteria

- Stubbing `localStorage.setItem` to throw does not prevent the theme icon, colorblind indicator, or last-synced widget from updating.
- Stubbing `localStorage.getItem` to throw does not throw an uncaught exception during initial load.
- No regression to normal (storage-available) behavior.

### Validation

- Manual: override `localStorage.setItem`/`getItem` in devtools console to throw, reload and interact with theme/colorblind toggles, confirm no uncaught errors in console and UI still updates.
- Automated: see TEST-001.

### Notes

**Done note (2026-08-01):** Added top-level `safeStorageGet(key)`/`safeStorageSet(key, value)` helpers (`script.js:1-14`) that swallow storage exceptions, and replaced all nine unguarded `localStorage.getItem`/`setItem` call sites (theme toggle, colorblind toggle, `enableColorblindMode`, `initLastSynced`'s cache write) with calls to the helpers. The pre-existing try/catch-wrapped cache read in `initLastSynced` was left as-is. Implementation was delegated to `gpt-oss-120b-medium` via agy; the first pass defined the helpers *inside* the `DOMContentLoaded` closure, which made them invisible to `initLastSynced()` (a top-level function called from inside that closure but not lexically nested in it) — this would have thrown `ReferenceError: safeStorageSet is not defined` on every successful fetch, silently caught by the promise chain's `.catch()`, reintroducing the exact "successful API response discarded" bug this item exists to fix. Caught by reviewing the diff before trusting it (per repo convention) and fixed by moving both helpers to module scope. Verified with a Node `vm`-context harness (mocked `document`/`localStorage`/`fetch`) confirming the last-synced widget still renders when `localStorage.getItem`/`setItem` throw, and that normal (non-throwing) storage behavior is unaffected.

---

### REL-006 — Fixed navbar can hide section headings on anchor navigation

**Type:** Bug
**Priority:** Medium
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `style.css`
**Status:** Done (2026-08-01)

### Problem

`.navbar` is `position: fixed` (`style.css:156-166`) and `html { scroll-behavior: smooth }` is set (`style.css:76-78`). The hero has `padding-top: 140px` to clear the navbar on initial load, but `.section` (`style.css:376-378`) has no `scroll-margin-top`. Clicking a nav link (`#about`, `#skills`, `#experience`, `#projects`, `#education`) scrolls the target heading to the very top of the viewport, where it's obscured by the fixed, blurred navbar.

### Proposed work

Add `scroll-margin-top` to `.section` (and/or the section headings) sized to clear the navbar's rendered height, so anchor-jumped headings land visibly below the nav bar.

### Acceptance criteria

- Clicking each desktop nav link and each mobile nav link scrolls its target section's heading fully into view, not underneath the navbar.
- No visual regression to section spacing when reached via normal scrolling (non-anchor navigation).

### Validation

- Manual: click each nav link at desktop and mobile viewport widths, confirm the heading is visible below the navbar with reasonable spacing.

### Notes

Small, isolated CSS fix — good candidate for a first small implementation task alongside REL-001/REL-002.

**Done note (2026-08-01):** Added `scroll-margin-top: 140px` to `.section` (`style.css:378`) matching the desktop hero's `padding-top`, and `scroll-margin-top: 100px` to a `.section` override inside the existing `@media (max-width: 768px)` block (`style.css:604`) matching the mobile hero's `padding-top`. No other selectors touched; `padding` on `.section` unchanged. Implementation delegated to `gemini-3.5-flash-low` via agy, which hit an account-wide Gemini quota (unrelated to this task, resets in ~66h); re-delegated to `gpt-oss-120b-medium`, which produced the correct minimal diff on the first attempt. Verified via `git diff` against disk (brace-balance and region checks) rather than trusting the delegate's self-reported diff. No local Chromium/Playwright/browser tool was available in this environment to do the manual click-through in the item's Validation section — that spot-check (each desktop/mobile nav link scrolls its heading fully clear of the navbar) is still recommended before/at next deploy, same caveat as REL-001.

---

### A11Y-005 — Primary blue fails contrast (2.79:1) against dark colorblind-mode background

**Type:** Bug
**Priority:** High
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `style.css`
**Status:** Done (2026-08-01)

### Problem

Measured directly: `--primary: #005ab5` against `[data-theme="colorblind"].dark-mode-colorblind`'s `--bg-main: #121212` yields **2.79:1** contrast, and against `--bg-card: #1e1e1e` yields **2.48:1**. Both fail WCAG AA even at the most lenient applicable threshold (3:1 for large text / UI components), let alone the 4.5:1 normal-text threshold. `--primary` is used for `.section-title` (large text — still fails at 2.79:1), link/icon hover states, and the `:focus-visible` outline color (non-text UI contrast, 3:1 required — fails). This is exactly the mode meant to serve low-vision and colorblind users, so the failure is highest-impact where it's least acceptable.

Separately, `--accent: #d55e00` on the same dark colorblind background measures 4.84:1 (passes normal text) but only 4.31:1 against the card background (still passes 4.5:1? — 4.31 fails 4.5:1 marginally for normal-size text; passes for large text at 3:1). `.timeline-date` and `.project-subtitle` use `--accent` at 0.9rem, which is normal-size text requiring 4.5:1 — this is a smaller, secondary finding worth including in the same fix pass.

Light colorblind mode was also checked and passes: primary 6.71:1, accent 3.87:1 on `#ffffff` (accent is used only for large/secondary text there, so 3.87:1 is acceptable for that usage but worth a final check once the dark-mode value changes).

### Proposed work

Darken/adjust `--primary` (and re-check `--accent`) specifically within `[data-theme="colorblind"].dark-mode-colorblind` so both meet at least 4.5:1 against `--bg-main` and `--bg-card` for any normal-text usage, and at least 3:1 for large-text/UI-component usage (focus outlines, icon hover). Keep the light colorblind-mode values as-is since they already pass. Re-verify with computed contrast ratios, not visual inspection alone.

### Acceptance criteria

- `--primary` and `--accent` (as used for text, focus outlines, and UI-component color in dark colorblind mode) meet WCAG AA contrast thresholds for their actual usage (4.5:1 normal text, 3:1 large text/UI components) against both `--bg-main` and `--bg-card` in `[data-theme="colorblind"].dark-mode-colorblind`.
- Light colorblind mode is unaffected (already passes).
- The colorblind-safe blue/orange hue pairing is preserved (don't reintroduce a red/green pair).

### Validation

- Automated: recompute WCAG contrast ratios for the new hex values against both backgrounds (same method used to find this issue) and confirm all pass their applicable threshold.
- Manual: visually confirm the dark colorblind theme still reads as high-contrast and the blue/orange distinction remains clear.

### Notes

This is a measured, confirmed failure (not a hypothesis) — contrast ratios computed directly from the CSS custom property values in `style.css:11-19,40-68`. Sequence this early; it's a real accessibility defect in a mode specifically built for accessibility.

**Done note (2026-08-01):** Re-evaluation before implementing surfaced a conflict the original Proposed work didn't account for: `--primary` is used both as *text/outline color* (needs to be light against the dark backgrounds) and as a *background under white text* at two sites (`.skip-link`, `.contact-pill:hover`, both `background: var(--primary); color: #ffffff;`) — lightening `--primary` directly would have fixed the reported failure while silently breaking those white-on-button pairs (dropping them from 6.71:1 to as low as ~3.2:1, itself a new AA failure). Resolved by introducing a `--primary-text` custom property (`style.css:13`, defined once at `:root` as `var(--primary)` so every theme's behavior is unchanged by default) used only at the 5 text/outline call sites (`style.css:106` focus-visible outline, `:204` nav-link hover, `:227` icon-btn hover, `:312` hero heading, `:387` section-title), while the 2 background call sites keep `var(--primary)` untouched. Only `[data-theme="colorblind"].dark-mode-colorblind` overrides `--primary-text` (to `#1c8dff`, 5.62:1/5.00:1 against bg-main/bg-card) and `--accent` (to `#e96700`, 5.71:1/5.08:1) — `--accent` had no equivalent background-usage conflict (grepped every `var(--accent)` site: all `color`/`border-color`, no background+white-text pairing) so it was overridden directly rather than split. Light colorblind mode and all non-colorblind themes are untouched (they don't define `--primary-text` or override `--accent` in dark mode, so they keep exactly their prior computed values). Contrast ratios computed with a WCAG relative-luminance/contrast-ratio Python script (standard sRGB-linearization formula), not visual inspection, and re-verified after the delegate's edit against the actual file on disk. Implementation delegated to `gpt-oss-120b-medium` via agy with the exact hex values, line-level context, and an explicit instruction not to blind-replace `var(--primary)` (to avoid catching the 2 background sites); the delegate's diff matched the spec exactly on the first attempt, confirmed via `git diff` against disk. No local Chromium/Playwright/browser tool was available to do the manual "still reads as high-contrast, blue/orange distinction clear" visual check in this environment — recommended before/at next deploy, same caveat as REL-001/REL-006.

---

### A11Y-001 — Mobile menu button lacks `aria-expanded`/`aria-controls`, no Escape handling, no focus return

**Type:** Bug
**Priority:** High
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `index.html`, `script.js`
**Status:** Done (2026-08-01)

### Problem

`.mobile-menu-btn` (`index.html:45-47`) has only `aria-label`; it has no `aria-expanded` or `aria-controls`, so screen reader users get no indication the button is a disclosure toggle or what state it's in. `script.js:121-141` toggles the `.active` class and swaps the icon but never sets `aria-expanded`. There is also no `keydown` handler for Escape to close the menu, and no focus management — closing the menu (by link click) doesn't return focus to the toggle button, and there's no way to close via keyboard without tabbing through every link.

### Proposed work

- Add `aria-expanded="false"` (toggled true/false) and `aria-controls="<mobile-nav-id>"` to `.mobile-menu-btn`; give `.mobile-nav` a matching `id`.
- Add an Escape `keydown` handler that closes the menu when open and returns focus to `.mobile-menu-btn`.
- On link-click close (existing behavior at `script.js:135-140`), keep it, but ensure `aria-expanded` is set to `false` at the same time.

### Acceptance criteria

- `aria-expanded` on `.mobile-menu-btn` accurately reflects open/closed state at every transition (button click, link click, Escape).
- `aria-controls` references the mobile nav's `id`.
- Pressing Escape while the mobile menu is open closes it and moves focus back to `.mobile-menu-btn`.
- No regression to existing click-to-open/close and icon-swap behavior.

### Validation

- Manual: keyboard-only walkthrough — Tab to menu button, Enter to open, verify `aria-expanded="true"` in devtools, Escape to close, verify focus returns to the button.
- Manual: screen reader spot check (VoiceOver or NVDA) confirms the button announces as a toggle with current state.

### Notes

Combine with A11Y-002 (semantic exposure while closed) since both touch the same markup and script.

**Done note (2026-08-01):** Added `aria-expanded="false"` and `aria-controls="mobile-nav"` to `.mobile-menu-btn` (`index.html:45`) and `id="mobile-nav"` to `.mobile-nav` (`index.html:53`, also covers A11Y-002 below). In `script.js`, extracted a `closeMobileMenu()` helper (`script.js:142-147`) used by both the existing link-click-close path and a new `keydown` listener for Escape that closes the menu and calls `mobileMenuBtn.focus()` to return focus (`script.js:176-181`). The click-toggle handler now sets `aria-expanded`/`aria-hidden` to match the new open/closed state on every transition. Implementation delegated to `gpt-oss-120b-medium` via agy in a single combined brief covering both A11Y-001 and A11Y-002; verified against the actual file diff on disk (not the delegate's truncated self-summary), plus `node --check script.js` and an HTML tag-balance sanity check. No local browser/screen-reader tool was available in this environment to do the manual keyboard/AT walkthrough in the Validation section — recommended before/at next deploy, same caveat as prior items.

---

### A11Y-002 — Verify closed mobile-menu content is fully inert (not just visually hidden)

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** A11Y-001
**Affected files:** `style.css`, `index.html`
**Status:** Done (2026-08-01)

### Problem

`.mobile-nav` is hidden when closed via `visibility: hidden` plus `transform`/`opacity` (`style.css:239-257`), which in modern browsers does remove it from the tab order and, generally, the accessibility tree. This is better than `display` toggling alone would suggest, but it hasn't been verified against the project's actual assistive-technology/browser support matrix, and relying on `visibility: hidden` alone (without a redundant `aria-hidden` or the `inert` attribute) is a known source of inconsistent AT behavior across older browser/AT combinations.

### Proposed work

Add `aria-hidden="true"` (toggled alongside `.active`/`aria-expanded` in the same script.js code path from A11Y-001) or the `inert` attribute to `.mobile-nav` while closed, as defense-in-depth on top of the existing `visibility: hidden`.

### Acceptance criteria

- With the menu closed, mobile nav links are confirmed unreachable via Tab and not announced by a screen reader.
- With the menu open, links are reachable and announced normally.

### Validation

- Manual: keyboard Tab-through with menu closed confirms mobile links are skipped.
- Manual: screen reader spot check with menu closed confirms links are not announced.

### Notes

Lower priority than A11Y-001 since `visibility: hidden` already provides most of the needed behavior in current browsers — this is a verification + defense-in-depth item, not a confirmed active bug.

**Done note (2026-08-01):** Implemented together with A11Y-001 (see that item's Done note for the full diff) since both touch the same markup/script code path as anticipated. `aria-hidden="true"`/`"false"` on `.mobile-nav` is now toggled in `script.js` alongside `aria-expanded`, in addition to the pre-existing `visibility: hidden` CSS. Actual affected files ended up being `index.html` and `script.js` only — `style.css` (listed above) wasn't touched since the existing `visibility`/`transform`/`opacity` hiding was left as-is; `aria-hidden` is a defense-in-depth attribute toggle, not a CSS change.

---

### A11Y-003 — Theme and colorblind toggle buttons don't expose pressed state programmatically

**Type:** Bug
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `index.html`, `script.js`, `style.css`
**Status:** Done (2026-08-01)

### Problem

`#theme-toggle` and `#colorblind-toggle` (`index.html:37-42`) communicate state only through icon glyph changes (`fa-sun`/`fa-moon`, `script.js:230-238`) and, for colorblind mode, an inline `style.color` set directly in JS (`script.js:207, 226`). Neither button has `aria-pressed`, so screen reader users have no way to know whether dark/light or colorblind mode is currently active. The inline-style-only indicator for colorblind state is also fragile — it bypasses the theme system's CSS custom properties and won't respond to theme changes made another way.

### Proposed work

Add `aria-pressed` (or `aria-checked` if treated as a switch) to both buttons, updated at every state transition. Replace the inline `style.color` colorblind indicator with a CSS class (e.g. `.icon-btn.active`) styled via `style.css` using `var(--primary)`, toggled in `script.js` instead of setting `style.color` directly.

### Acceptance criteria

- `aria-pressed` on both buttons accurately reflects current state after every toggle and after initial load (including when state is restored from `localStorage` or OS preference).
- Colorblind-active visual indicator is applied via a CSS class, not an inline style.
- No visual regression to the existing active-state color indicator.

### Validation

- Manual: toggle each control, inspect `aria-pressed` in devtools at each state.
- Manual: screen reader spot check confirms toggle state is announced.

### Notes

Small, contained change. Independent of A11Y-001/002 (different controls) — can be done in parallel by a different work session if desired, but no hard dependency either way.

**Done note (2026-08-01):** Added `aria-pressed` to both `#theme-toggle` and `#colorblind-toggle` (`index.html:37,40`), defaulting to `true`/`false` respectively to match this site's actual defaults (dark theme, colorblind off) and kept in sync at every transition: `updateThemeIcon()` now sets `theme-toggle`'s `aria-pressed` from the theme argument it already receives (`script.js:280`), and both branches of the colorblind click handler plus `enableColorblindMode()` set `colorblind-toggle`'s `aria-pressed` (`script.js:245-246,264-267`). Replaced the inline `style.color` indicator with an `.icon-btn.active` CSS class (`style.css:232-234`), toggled via `classList` instead of direct style writes. One correction made during re-evaluation: the original Proposed work said to style the active class "using `var(--primary)`", but that predates A11Y-005's fix splitting `--primary` (background-safe) from `--primary-text` (text-safe) — using `var(--primary)` here would have reintroduced the exact dark-colorblind-mode text-contrast failure A11Y-005 just fixed, since this is icon *color* (text-role), not a background. Used `var(--primary-text)` instead, matching the adjacent `.icon-btn:hover` rule. Implementation delegated to `gpt-oss-120b-medium` via agy; verified against the actual file diff on disk (the delegate's own summary this time didn't include the diff text at all, just a description — per repo convention, never trust a delegate's self-report without checking disk). Sanity-checked with `node --check script.js`, brace-balance, and button-tag-balance. No local browser/screen-reader tool was available in this environment to do the manual devtools/AT walkthrough in the Validation section — recommended before/at next deploy, same caveat as prior items.

---

### A11Y-004 — Heading hierarchy skips from `h1` to `h3`

**Type:** Bug
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `index.html`, `script.js`, `style.css`
**Status:** Done (2026-08-01)

### Problem

The hero renders an `h1` (config-driven, `script.js:7`) and an `h2.subtitle` (`script.js:8`), but every section title (`index.html:71,78,85,92,99`) is an `h3.section-title`, and content within sections (skill categories, timeline items, project cards, education cards) uses `h4`/`h5`. There is no `h2` used for the top-level section headings ("Professional Summary," "Core Skills," etc.) — the hierarchy jumps `h1` → (hero `h2`) → `h3` for sections not nested under the hero `h2`, which is itself questionable since the hero `h2` (job title) and the section `h3`s aren't actually in a parent-child relationship.

### Proposed work

Restructure so section titles (`index.html:71,78,85,92,99`) use `h2`, and demote nested headings one level accordingly (skill-category/timeline/project/education headings move from `h4`→ appropriate level, currently-`h5` company/school lines adjust to match). Update `style.css` selectors and any element-specific styling tied to the old tag names.

### Acceptance criteria

- Heading levels increase by exactly one at each nesting step with no skipped levels, verified with a browser accessibility tree inspector or automated heading-outline check.
- Visual appearance is unchanged (font size/weight styled by class, not by relying on the tag's default UA styling).

### Validation

- Manual: browser devtools Accessibility panel heading outline, or a headings-list browser extension, confirms a clean h1→h2→h3(→h4) outline with no gaps.
- Visual diff: confirm no unintended styling change from swapping tag names (styles are class-driven, so this should be a non-issue, but verify).

### Notes

Purely structural/markup — no resume content changes required, just tag names and matching CSS selectors.

**Done note (2026-08-01):** Promoted the 5 section titles h3→h2 (`index.html:71,78,85,92,99`, `.section-title` is class-styled so no CSS change needed there). Demoted the nested headings one level in `script.js`'s template literals: `skill.category`, `job.title`, `proj.name`, `edu.degree` all h4→h3, and the single h5 (`job.company`/location line) →h4 (`script.js:47,62-63,76,94`). Updated the matching tag-descendant selectors in `style.css` (`.skill-category h4`→`h3`, `.timeline-content h4`→`h3`, `.timeline-content h5`→`h4`, `.project-card h4`→`h3`). Found one pre-existing gap while doing this: `edu.degree`'s heading had no dedicated CSS rule at all (no `.edu-info h4` existed), so it was rendering at the browser's UA-default h4 size; promoting it to h3 would have silently picked up the larger UA-default h3 size instead, a real visual regression the item's own acceptance criteria calls out. Added `.edu-info h3 { font-size: 1em; }` (`style.css:541-543`) to pin it back to its prior effective size. Final outline: h1 → h2 (hero subtitle, sibling) / h2 (section titles) → h3 (category/job-title/project-name/degree) → h4 (company/location line) — no skipped levels. Implementation delegated to `gpt-oss-120b-medium` via agy in two parts: the first call hit a transient network error mid-run but had already completed the index.html edit correctly before failing (git status showed a partial diff, not a clean revert) — verified that partial diff against disk before re-delegating just the remaining script.js/style.css changes in a follow-up brief that explicitly excluded index.html, rather than re-running the full original brief and risking a double-edit. Verified all three files against disk diffs (not the delegate's prose summaries, which again didn't include actual diff text) plus `node --check script.js`, brace-balance, and a full heading-tag grep across both files to confirm the final outline. No local browser/AT tool was available in this environment for the manual accessibility-tree/visual-diff check in the Validation section — recommended before/at next deploy, same caveat as prior items.

---

### REL-003 — Last-synced repo/branch are hardcoded and duplicate `config.js.sourceRepo`

**Type:** Improvement
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `script.js`, `config.js`
**Status:** Done (2026-08-01)

### Problem

`initLastSynced()` hardcodes `https://api.github.com/repos/howlcipher/william_elias/commits/main` (`script.js:278`), duplicating the repo identity already present in `config.js.personal.sourceRepo` (`config.js:11`) and the branch name implicitly assumed to be `main`. If the repo is ever renamed/forked or the default branch changes, this must be updated in two places (and the README's deploy instructions imply `main` is significant — see MAINT-002).

### Proposed work

Derive the GitHub API URL from `config.personal.sourceRepo` (parse owner/repo out of the GitHub URL) plus a single configurable branch value (add e.g. `config.personal.sourceBranch = "main"` or a small constant near the top of `script.js`). Keep the parsing simple — this doesn't need a general-purpose URL parser, just a `sourceRepo.replace('https://github.com/', '')` style extraction with a sanity check.

### Acceptance criteria

- Repo owner/name is sourced from `config.js`, not duplicated as a literal in `script.js`.
- Branch is a single named constant/config value, not inlined in the fetch URL string.
- Widget behavior (rendering, caching, relative time) is unchanged for the current repo/branch.

### Validation

- Manual: load the page, confirm the last-synced widget still renders the correct commit.
- Manual: temporarily point the derived URL at a different fork/branch to confirm the value is actually being read from config, not hardcoded.

### Notes

Low urgency on its own, but do this before/alongside REL-004 (cache key) since both touch the same function and repo/branch identity feeds the cache key.

**Done note (2026-08-01):** Implemented together with REL-004 (single function rewrite covers both). Added `config.personal.sourceBranch: "main"` (`config.js:11-12`). `initLastSynced()` (`script.js:302-349`) now derives `ownerRepo` from `config.personal.sourceRepo` via `.replace('https://github.com/', '')` plus a `/^[^/]+\/[^/]+$/` sanity check (bails out silently, same as a fetch failure, if `sourceRepo` is missing or malformed) and reads `branch` from `config.personal.sourceBranch` (falling back to `'main'` if unset), then builds both the fetch URL and the cache key from those. Verified the extraction produces byte-identical values to the old hardcoded ones for the current config (`howlcipher/william_elias`, `main`) via a standalone Node check, so current behavior is unchanged. Implementation delegated to `gpt-oss-120b-medium` via agy; this delegation had a real defect caught only by checking the actual file on disk: the model's diff summary claimed a full function replacement, but it had only *inserted* the new function body without deleting the old one, leaving the new function's closing `}` immediately followed by ~40 lines of the old function's body as dangling top-level statements — a `SyntaxError: Unexpected token '}'` that `node --check script.js` caught immediately. Fixed by deleting the leftover dead code directly (a small, unambiguous removal, not worth a full re-delegation). This is the same class of failure the repo's own delegation protocol warns about (self-reported diffs that don't match reality) — `node --check` is now a standing habit for every JS delegation in this repo, not just a one-off.

---

### REL-004 — Last-synced cache key doesn't include repo/branch identity

**Type:** Bug
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** REL-003 (do together or REL-004 first, either order is fine — REL-003 is what makes this matter)
**Affected files:** `script.js`
**Status:** Done (2026-08-01)

### Problem

`CACHE_KEY = 'we_last_synced'` (`script.js:260`) is a fixed string with no repo/branch component. This is harmless today (one hardcoded repo/branch), but once REL-003 makes the repo/branch configurable, a stale cached value from a previous repo/branch could be served under the same key after a config change, showing the wrong commit until the 10-minute TTL expires.

### Proposed work

Include the derived owner/repo/branch in the cache key (e.g. `` `we_last_synced:${owner}/${repo}:${branch}` ``) so a config change invalidates old cache entries automatically.

### Acceptance criteria

- Changing the configured repo or branch does not surface a stale cached commit from the old identity.
- Existing cache behavior (10-minute TTL, graceful fallback to cache on fetch failure) is unchanged.

### Validation

- Manual: populate cache for one repo/branch, change the configured value, reload, confirm a fresh fetch occurs rather than serving stale cached data.

### Notes

Trivial fix; sequence right after REL-003 so there's something for the key to disambiguate.

**Done note (2026-08-01):** See REL-003's Done note — implemented together as one function rewrite. `CACHE_KEY` is now `` `we_last_synced:${ownerRepo}:${branch}` `` (`script.js:308`), so a repo or branch config change no longer risks serving a stale cached commit from the old identity under the same key. Existing TTL (10 min) and cache-fallback-on-fetch-failure behavior are both untouched.

---

### REL-005 — Last-synced API response is cached and rendered without validation

**Type:** Bug
**Priority:** Medium
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** None
**Affected files:** `script.js`
**Status:** Done (2026-08-01)

### Problem

`initLastSynced()`'s fetch handler (`script.js:287-293`) takes `data.sha`, `data.commit.author.date`, and `data.html_url` directly from the parsed JSON response and both caches them and passes them to `renderLastSynced`, which interpolates them into `innerHTML` (`script.js:256`, see SEC-001) without checking they exist or are well-formed. If GitHub's API response shape changes, returns an error body with a 200 (unlikely but not impossible), or `res.json()` succeeds on something unexpected, `sha.slice(0,7)` at `script.js:255` can throw on `undefined`, or a malformed `date` can produce `Invalid Date` / `NaN` output from `formatRelativeTime`.

### Proposed work

Validate the shape of the response (string `sha`, parseable `commit.author.date`, string `html_url` matching an expected `https://github.com/...` pattern) before caching or rendering. On validation failure, treat it the same as a fetch failure — fall back to cache if present, otherwise render nothing.

### Acceptance criteria

- A mocked API response missing `sha`/`commit.author.date`/`html_url` does not throw an uncaught exception and does not render broken/`NaN`/`undefined` content.
- A malformed response is not written to `localStorage` cache.
- Normal successful responses render exactly as before.

### Validation

- Manual: mock `fetch` to resolve with a response missing expected fields, reload, confirm no console errors and no garbled footer text.
- Automated: see TEST-001.

### Notes

Ties directly into SEC-001 (unsafe `innerHTML` interpolation of this same data) — consider implementing both together since the safe-rendering rewrite naturally forces validation at the same call site.

**Done note (2026-08-01):** Implemented together with SEC-001's last-synced portion and SEC-002's last-synced portion (one combined delegation, since all three touch the same two functions). Added `validateLastSyncedData(data)` (`script.js:295-304`), called from `initLastSynced()`'s fetch success handler: checks `sha` is a non-empty string, `commit.author.date` parses to a valid `Date`, and `html_url` is a string matching `/^https:\/\/github\.com\//`. On failure it returns `null`, which makes the caller `throw`, routing through the *existing* `.catch()` fallback (cache-if-present, else render nothing) instead of adding new branching — same behavior REL-005 asked for. Verified with a Node `vm`-context harness (mocked `document`/`localStorage`/`fetch`, same technique used for REL-002) across four scenarios: a valid response (renders + caches correctly), a response missing `sha` (no throw, empty render, nothing cached), an `<img src=x onerror=alert(1)>`-style payload in `sha` (renders as inert text via `textContent`, confirmed by inspecting the actual diff uses `createElement`/`textContent`, never `innerHTML`), and a `javascript:` URL in `html_url` (rejected by the `https://github.com/` prefix check before it ever reaches render or cache). Implementation delegated to `claude-sonnet-4-6` via agy (escalated above the usual `gpt-oss-120b-medium` tier given this item's own "High reasoning" recommendation and that it's security-sensitive rendering code) — this delegation was clean on the first attempt, unlike the prior REL-003/004 delegation, but was still verified against the actual disk diff and `node --check` rather than trusted from its prose summary, per standing practice in this repo.

---

### SEC-001 — Resume and API data rendered via unescaped `innerHTML` throughout

**Type:** Improvement
**Priority:** Medium
**Effort:** M
**Risk:** Medium
**Recommended mode:** Coding
**Recommended model tier:** High reasoning
**Affected files:** `script.js`
**Dependencies:** REL-005 (validation work overlaps the same call site)
**Status:** Done (2026-08-01) — scoped to the last-synced widget only; config.js-driven sections filed as SEC-004

### Problem

`script.js` builds DOM content via template-literal `innerHTML` assignment in ~7 places: hero (`script.js:6-18`), summary (`script.js:23`), skills (`script.js:28-36`), experience (`script.js:41-53`), projects (`script.js:58-68`), education (`script.js:74-82`), and the last-synced widget (`script.js:256`). The `config.js` values are static and owner-controlled, so the practical risk there is low (defense-in-depth, not an active exploit path) — but the last-synced widget interpolates `sha`, `date`-derived text, and `url` **sourced from a live network response (GitHub's API)** directly into `innerHTML` with no escaping (`script.js:256`). While GitHub's API is trusted today, this is the one spot where externally-sourced data reaches `innerHTML` unescaped, and it sets a pattern that would be actively dangerous if `config.js` ever became less static (e.g., fetched from a CMS) or if the API response shape assumption in REL-005 is ever violated.

### Proposed work

Replace `innerHTML` template interpolation with `textContent` assignment and explicit DOM construction (`createElement` + `setAttribute`/`textContent`) at least for the last-synced widget, since that's the only genuinely externally-sourced data. Extend the same pattern to the `config.js`-driven renderers where practical, prioritizing anywhere user-facing text is interpolated (achievements, highlights, tags) over purely structural markup. This is a meaningful refactor of `script.js`'s rendering — don't rewrite it in one giant diff; consider splitting by section (hero, skills, experience, projects, education, last-synced) if done incrementally.

### Acceptance criteria

- The last-synced widget no longer interpolates API-sourced strings into `innerHTML`; equivalent output is built via `textContent`/DOM APIs.
- Config-driven sections render identically to before (no visual regression).
- No behavior change to links (`href`, `target`, `rel` attributes preserved, see SEC-002).

### Validation

- Manual: visually diff every section before/after against the live site to confirm no rendering regression.
- Manual: mock the last-synced fetch to return a value containing `<img src=x onerror=alert(1)>` in `html_url` or `sha`, confirm it renders as inert text, not executed markup, both before-fix (to confirm the risk) and after-fix (to confirm the mitigation).

### Notes

This is the largest single refactor in the backlog short of the resume.json architecture work — size it as M and expect it may be worth splitting into per-section sub-items if it proves larger in practice. The `config.js` half of this item is lower urgency than the last-synced half; if scoping down, prioritize the last-synced widget alone and file the `config.js` portion as a separate follow-up.

**Done note (2026-08-01):** Scoped down exactly as this item's own Notes suggested: implemented the last-synced widget portion only (see REL-005's Done note for the full diff — `renderLastSynced()` now builds DOM via `createElement`/`textContent`/`append`, no `innerHTML`). Confirmed via the verification harness that an XSS-style payload in API-sourced `sha` renders as inert text, not executed markup. The `config.js`-driven sections (hero, summary, skills, experience, projects, education — still using `innerHTML` template interpolation, `script.js:22,39,44,57,74,90`) are unchanged; that data remains owner-controlled/static so the practical risk stays low, but the refactor itself is filed as **SEC-004** below rather than done here, per this item's own scoping guidance.

---

### SEC-002 — Dynamic link `href` values aren't protocol-validated

**Type:** Improvement
**Priority:** Low
**Effort:** S
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Standard
**Dependencies:** SEC-001 (natural to fix together at the same call sites)
**Affected files:** `script.js`
**Status:** Done (2026-08-01) — scoped to the last-synced widget's `url` only; config.js-driven links filed as SEC-005

### Problem

`config.personal.linkedin`, `.github`, `.resumePdf`, `.sourceRepo` (`script.js:13-16`) and the last-synced `url` (`script.js:256`) are all written directly into `href` attributes with no check that they're `http(s)` URLs. Today all values are owner-controlled or come from GitHub's API, so this is low practical risk, but it's an easy, cheap check to add as defense-in-depth (e.g. against a future config value accidentally containing a `javascript:` URL).

### Proposed work

Add a small helper that validates a URL string starts with `http://` or `https://` (or is a `mailto:`/`tel:` where expected) before using it as an `href`, skipping/omitting the link if it fails validation rather than rendering a dangerous `href`.

### Acceptance criteria

- A config value or API value with a non-http(s) protocol (e.g. `javascript:...`) does not get rendered as a clickable `href`.
- Normal `https://` links are unaffected.

### Validation

- Manual: temporarily set a config link value to `javascript:alert(1)`, confirm it's not rendered as an active link after the fix.

### Notes

Bundle with SEC-001 since both touch the same rendering call sites.

**Done note (2026-08-01):** Implemented for the last-synced widget's `url` only, together with REL-005/SEC-001 (see REL-005's Done note for the full diff and verification). `renderLastSynced()` now only sets `href`/`target`/`rel` on the commit link if `url` matches `/^https:\/\//`; a mocked `javascript:alert(1)` value was confirmed rejected before it ever reaches the DOM (caught earlier, at `validateLastSyncedData`'s stricter `https://github.com/` prefix check, but the render-time `/^https:\/\//` guard is a deliberate second layer independent of that — see REL-005's Done note for why both are kept). The `config.js`-driven links (`linkedin`, `github`, `resumePdf`, `sourceRepo` — `script.js:27-32`) are unchanged and filed as **SEC-005** below, per this item's dependency on SEC-001 which was also scoped down.

---

### SEC-003 — Font Awesome stylesheet loaded from CDN without Subresource Integrity

**Type:** Improvement
**Priority:** Low
**Effort:** XS
**Risk:** Low
**Recommended mode:** Coding
**Recommended model tier:** Lightweight
**Dependencies:** None
**Affected files:** `index.html`
**Status:** Done (2026-08-01)

### Problem

`index.html:18` loads `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css` with no `integrity` or `crossorigin` attribute. If cdnjs were ever compromised or the specific asset tampered with, the site would load and execute (well, apply as CSS — lower severity than a JS CDN, but still) unverified third-party content. Google Fonts links (`index.html:15-17`) are lower risk (no SRI support for cross-origin CSS at a dynamically-generated URL, which is normal/expected for Google Fonts) and are not in scope here.

### Proposed work

Add an `integrity` (SRI hash) and `crossorigin="anonymous"` attribute to the Font Awesome `<link>` tag, pinned to the specific 6.4.0 version already in use. cdnjs publishes SRI hashes alongside each asset version.

### Acceptance criteria

- Font Awesome stylesheet link includes a correct `integrity` hash matching the pinned 6.4.0 asset and `crossorigin="anonymous"`.
- Icons continue to render correctly (SRI mismatch would block the stylesheet entirely, so this is self-verifying).

### Validation

- Manual: load the page after the change, confirm icons still render and no console error about SRI mismatch/blocked resource.

### Notes

Cheapest item in the backlog — good candidate to bundle into any other small maintenance pass.

**Done note (2026-08-01):** Added `integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw=="` and `crossorigin="anonymous"` to the Font Awesome `<link>` (`index.html:18`). Applied this one directly rather than delegating — it's a single well-defined attribute addition with no logic to get wrong, and getting the hash *right* mattered more than saving a delegation round-trip. Didn't trust a third-party SRI listing site: downloaded the actual `all.min.css` 6.4.0 asset from cdnjs directly, computed its SHA-512 locally with `openssl dgst`, and cross-checked that against cdnjs's own API (`api.cdnjs.com/libraries/font-awesome/6.4.0?fields=sri`) — both independent computations matched byte-for-byte. No local browser was available to do the manual "icons still render, no SRI-mismatch console error" check in the Validation section (this one actually matters more than most of the "no browser available" caveats elsewhere in this file, since a hash typo here would silently block every icon on the site) — strongly recommended before/at next deploy.

---

## Recommended Sequencing

Dependency-aware order, following the general sequence in the operating instructions:

1. ~~**REL-001** — IntersectionObserver fallback (prevents invisible content)~~ — Done (2026-08-01)
2. ~~**REL-002** — storage fault tolerance~~ — Done (2026-08-01)
3. ~~**REL-006** — anchor scroll-margin fix~~ — Done (2026-08-01)
4. ~~**A11Y-005** — dark colorblind contrast fix (measured, confirmed failure)~~ — Done (2026-08-01)
5. ~~**A11Y-001** + **A11Y-002** — mobile menu keyboard/ARIA behavior~~ — Done (2026-08-01)
6. ~~**A11Y-003** — toggle button state exposure~~ — Done (2026-08-01)
7. ~~**A11Y-004** — heading hierarchy~~ — Done (2026-08-01)
8. ~~**REL-003** → **REL-004** — last-synced repo/branch config-driven, then cache key~~ — Done (2026-08-01)
9. ~~**REL-005** + **SEC-001** (last-synced portion) + **SEC-002** — safe rendering and validation for the last-synced widget together~~ — Done (2026-08-01); config.js-wide portions filed as **SEC-004**/**SEC-005**
10. ~~**SEC-003** — Font Awesome SRI (cheap, anytime)~~ — Done (2026-08-01)
10a. **SEC-004** → **SEC-005** — config.js-wide safe rendering and href validation, deferred from item 9 (filed 2026-08-01; lower urgency, data is owner-controlled — good candidate to pair with TEST-001 once it exists)
11. **MAINT-001** — remove `.directory`, add `.gitignore` (cheap, anytime)
12. **TEST-002** → **TEST-003** → **TEST-001** — PDF tests, then CI, then browser-behavior tests
13. **ARCH-003** — config validation
14. **ARCH-002** — canonical resume-data decision (planning), spawning its own follow-up items if pursued
15. **ARCH-001** — PDF parser hardening (only if ARCH-002 is deferred; otherwise resolved by ARCH-002's follow-ups)
16. **ARCH-004** — PDF metadata (anytime, cheap)
17. ~~**ARCH-005** — PDF freshness check in CI~~ — Done (2026-08-04)
18. **TEST-004** — document validation command (after the above testing items land)
19. **MAINT-002** — README accuracy pass (do a lightweight pass early for the overstated claim; full pass after ARCH-005/TEST-004)
20. **ENH-001**, **ENH-002** — portfolio enhancements, whenever owner input/priority allows

SEC-001's `config.js`-wide portion is the largest true refactor in this list; treat it as the one item most likely to warrant further sub-splitting at implementation time.
