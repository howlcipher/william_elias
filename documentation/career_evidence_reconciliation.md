# Career evidence reconciliation

Review date 2026-11-17. The November audit summaries support provisional descriptions and are not primary employer records. Scope labels below describe the evidence available for this review. Canonical IDs refer to `resume.json`.

## Professional and education claims

| Claim | Basis and confidence | Status and publication boundary |
| --- | --- | --- |
| Current role, promotion, tenure (`exp-stellantis`) | Owner confirmation, high | Verified as stated by owner. Preserve the official title and dates. |
| Shared internal operations portal and controls (`ach-internal-dotnet-app`, `ach-portal-controls`) | Owner brief and audit summaries, medium | Provisional. Selected workflows run in production; development and QA work remain distinct. Confirm stack, release scope, and personal contribution. Exclude internal topology and retired features. |
| Azure DevOps templates, rollout and preflight checks (`ach-cicd-standardization`, `ach-cicd-validation`) | Owner profile for broad CI/CD work and audit summaries for specifics, medium | Qualified. Inventory, configured pipelines, builds, dry runs, and production deployments are distinct. Deployment figures and estate-wide completion remain excluded. |
| Python reporting, APIs, and diagnostics (`ach-python-tooling`, `ach-release-kql`) | Owner profile and audit summaries, medium | Qualified. One FastAPI integration is reported. No usage or performance figures. |
| Production diagnosis and source-reference corrections (`ach-production-remediation`) | Audit summaries, medium | Provisional. Describe the intervention at a high level. Restoration timing and outcome remain unverified. |
| Configuration discovery in C#/.NET and Python Git-history tooling (`ach-secrets-discovery`, `ach-git-history-tooling`) | Audit summaries, medium | Provisional. The migration proposal was not executed. Credential lifecycle actions and cleanup counts remain unverified and excluded. Confirm disclosure permission for the tool descriptions. |
| Deployment CLI and infrastructure investigations | Audit summaries, medium | Provisional. Prototype capabilities and completed production releases are distinct. |
| AI-assisted development practices (`about`) | Owner brief, medium | Qualified. Describe working practices and human review without claiming individual authorship or universal enforcement. |
| Prior employment and education | Owner profile and employment record, high for roles and education status | Qualified. Preserve official dates and degree status. HBK impact figures are owner-reported; underlying measurements were unavailable. |

## Independent work

These are AI-assisted independent projects. Verification below covers public implementation evidence at the inspected revisions. It does not establish employer adoption, commercial deployment, or current test results.

| Project and status | Public evidence reviewed | Classification and confidence | Where shown |
| --- | --- | --- | --- |
| HowlPlane, agent orchestration with policy checks, run records, and approval flows | [README and source tree](https://github.com/howlcipher/howlplane/tree/03868872a78f2bb16af090dffccd97471e7eb3af), approval lifecycle tests and control-plane policy source | VERIFIED_WITH_QUALIFICATION, high for code scope | Website, software and production PDFs, LinkedIn Featured |
| HowlProof, advisory local verification beta | [README and source tree](https://github.com/howlcipher/howlproof/tree/3b3e4eea407e5069f1b0b0be14ff7321b69bd77c), evidence bundle, verdict and replay modules. Replay applies to supported findings. | VERIFIED_WITH_QUALIFICATION, high | Website, software and security PDFs, LinkedIn Featured |
| HowlFrame, experimental Go compiler and capability-bounded runtime | [README and source tree](https://github.com/howlcipher/howlframe/tree/9c739c9db6ca708555352d3613ff3435afcc4006), compiler, VM and WasmGC backend | VERIFIED_WITH_QUALIFICATION, high | Website |
| HowlDream, experimental comparison and validation of AI proposals | [README and source tree](https://github.com/howlcipher/howldream/tree/9724147e8b914edc6765df5888bc75395c97b22b), engine and evidence modules | VERIFIED_WITH_QUALIFICATION, high | Website |
| HowlWriter, linting, provenance, and citation workflow | [README and source tree](https://github.com/howlcipher/howlwriter/tree/81480cac6201ffcdf37da1786ed8e634af6a964b), linting and citation verification modules | VERIFIED_WITH_QUALIFICATION, high | Website |
| Password Arena, local synthetic password-strength simulator | [README and source tree](https://github.com/howlcipher/password_arena/tree/029dae795979187087069b7bcc631449c86f7907), evaluation engine and information policy source | VERIFIED_WITH_QUALIFICATION, high | Website, security PDF |
| AI Router local alpha, Baseball Optimizer Rust/Axum backend and RedrawUS geospatial pipeline | Public trees and project docs at [AI Router](https://github.com/howlcipher/ai_router/tree/82e202f), [Baseball Optimizer](https://github.com/howlcipher/baseball_optimizer/tree/a81cd88), and [RedrawUS](https://github.com/howlcipher/redistricting-map/tree/4301290) | VERIFIED_WITH_QUALIFICATION, medium | Website |

## Review before publication

Confirm employer disclosure clearance for portal and delivery claims, security tooling, and incident descriptions. If stronger ownership or outcomes are needed, obtain sanitized contribution and release evidence that can support those claims. Confirm the HBK measurement basis before increasing precision.
