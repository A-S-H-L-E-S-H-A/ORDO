# ORDO Project Requirements and Scope Blueprint

**Project:** ORDO — AI-powered GitHub Issue Intelligence Platform  
**Document:** `docs/implementation/ORDO_Project_Requirements_and_Scope_Blueprint.md`  
**Status:** Draft for project-owner review; not an approved baseline  
**Date:** 2026-10-27  
**Repository status:** The user has stated that the repository has not yet been created. No application code, tests, or deployments were inspected or verified.

> **Evidence rule:** This document distinguishes project intent from confirmed commitments. The existing role-specific manuals in the user's Library are planning artifacts, not proof of implementation or project-owner approval. Any feature or technology marked Proposed or Awaiting approval must not be treated as committed scope.

## Table of Contents
1. [Purpose and Status](#1-purpose-and-status)
2. [Product Overview](#2-product-overview)
3. [Problem Statement and Goals](#3-problem-statement-and-goals)
4. [Stakeholders and User Roles](#4-stakeholders-and-user-roles)
5. [Functional Requirements](#5-functional-requirements)
6. [User Workflows](#6-user-workflows)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Data and GitHub Integration](#8-data-and-github-integration)
9. [AI and ML Requirements](#9-ai-and-ml-requirements)
10. [Code Retrieval Requirements](#10-code-retrieval-requirements)
11. [API and Frontend Requirements](#11-api-and-frontend-requirements)
12. [Security and Privacy](#12-security-and-privacy)
13. [Scope Boundaries](#13-scope-boundaries)
14. [Acceptance Criteria](#14-acceptance-criteria)
15. [Definition of Done](#15-definition-of-done)
16. [Risks and Dependencies](#16-risks-and-dependencies)
17. [Traceability Matrix](#17-traceability-matrix)
18. [Proposed Implementation Phases](#18-proposed-implementation-phases)
19. [Assumptions and Open Questions](#19-assumptions-and-open-questions)
20. [Approval and Change History](#20-approval-and-change-history)

## 1. Purpose and Status

This document is the product-level source of truth proposed for ORDO scope. It defines the user problem, candidate capabilities, testable requirements, acceptance approach, and decisions that must be approved before implementation. It does not replace specialist manuals.

### Status vocabulary
- **Confirmed:** explicitly established by available project information.
- **Proposed:** reasonable candidate requiring approval.
- **Awaiting approval:** a decision is required before dependent implementation.
- **Not verified:** no implementation evidence is available.

The only confirmed product-level fact is that ORDO is intended to be an AI-powered GitHub Issue Intelligence Platform. FastAPI, Streamlit, GitHub issue ingestion, ML, code retrieval, and storage are repeated in planning manuals, but the exact initial-release scope and technical choices still require approval.

## 2. Product Overview

ORDO is intended to help a developer or repository maintainer make sense of GitHub issues more efficiently than a basic issue list. The planned concept combines repository issue data with analysis and, if approved, relevant source-code context. A proposed implementation uses a FastAPI service and a Streamlit dashboard.

### Candidate capabilities

| Capability | Current status | Approval needed |
|---|---|---|
| Retrieve issues from a user-selected GitHub repository | Proposed | Supported repository types, authentication, issue/PR inclusion |
| Normalize issue records into a stable internal representation | Proposed | Canonical fields and update semantics |
| Display issue lists and basic details | Proposed | Filters, sorting, pagination |
| Classify or categorize issues | Proposed | Taxonomy, model approach, quality threshold |
| Similarity or duplicate-issue suggestions | Proposed | Definition of duplicate, evaluation set, UI behavior |
| Prioritization support | Proposed | Signals and explanation; must not silently close or modify issues |
| Retrieve related source-code context | Proposed | Repository indexing and permission boundaries |
| AI-generated summaries or recommendations | Proposed | Model/provider, privacy, evidence and human review |
| FastAPI backend | Repeated planned architecture | API contract approval |
| Streamlit dashboard | Repeated planned architecture | Page and interaction approval |
| Persistent storage | Undecided | Need, data lifecycle, technology |
| Vector database / external cache / background queue | Undecided | Must be justified by workload; not assumed |

## 3. Problem Statement and Goals

### Problem
Issue trackers can contain large numbers of reports with overlapping descriptions, inconsistent labels, incomplete reproduction steps, and links to source code. A plain listing exposes the records but may not help a user identify themes, possible duplicates, or relevant code.

### Intended users (proposed)
- **Repository maintainer:** triages incoming issues and reviews categories or candidate duplicates.
- **Developer/contributor:** investigates an issue and searches for relevant source-code context.
- **Project owner/operator:** configures the application and reviews its operational health, if such controls are approved.

No separate login, organization administration, multi-tenancy, or team-management feature is assumed.

### Product goals
1. Reduce the effort required to find and understand relevant issues.
2. Present issue analysis as decision support, with source evidence and uncertainty visible.
3. Preserve the original GitHub issue as the authoritative source.
4. Keep the application testable, observable, secure, and maintainable.
5. Avoid unapproved write actions to GitHub.

### Success measures to approve
| Measure | Measurement approach | Target |
|---|---|---|
| Issue ingestion correctness | Compare normalized records with a controlled GitHub fixture | To be approved |
| Classification quality, if included | Labelled evaluation set; precision/recall/F1 as appropriate | To be approved |
| Similarity usefulness, if included | Human-labelled pairs; precision@k/recall@k | To be approved |
| Code retrieval relevance, if included | Curated issue-to-code queries; ranking evaluation and human review | To be approved |
| API and dashboard latency | Representative workload measurements | To be approved |
| Failure transparency | Tests for rate limits, invalid input, empty results, network failure | All specified failure paths handled |
| Setup reproducibility | Clean-environment setup instructions executed by a new developer | To be verified |

Do not report numeric success targets until approved and measured.

## 4. Stakeholders and User Roles

| Role | Needs | Authority / boundary |
|---|---|---|
| Project owner / approver | Scope, risk, acceptance, release decisions | Approves unresolved product and technology decisions |
| Project Lead / Technical Coordinator | Dependency, contracts, ownership, gates | Coordinates; does not unilaterally approve product scope unless delegated |
| Repository maintainer | Issue triage and understandable results | GitHub remains source of truth |
| Developer/contributor | Relevant issue and code context | Can inspect suggestions; no automatic consequential action |
| Engineering roles | Stable contracts and clear boundaries | Own assigned modules as defined in specialist manuals |
| Security reviewer | Secret handling, private data, threat boundaries | Reviews security design and findings |

## 5. Functional Requirements

Priority uses **P0** (required for a minimal approved release), **P1** (important candidate), and **P2** (future candidate). Priorities are proposed until scope approval. Requirements are stable identifiers and should not be reused.

### GitHub integration and ingestion

#### FR-001 — Validate repository reference
- **Status:** Proposed; **Priority:** P0 candidate.
- **Actor:** User / backend.
- **Preconditions:** Application configuration is valid.
- **Behavior:** Validate repository owner/name or approved repository reference before making external requests.
- **Inputs:** Repository reference.
- **Outputs:** Validated repository identity or a safe validation error.
- **Errors:** Empty/malformed reference, unsupported URL, unavailable repository.
- **Acceptance:** Invalid references are rejected before external calls; errors do not expose credentials.
- **Dependencies:** API contract, security review.
- **Verification:** Unit and API validation tests.

#### FR-002 — Retrieve issues using GitHub API
- **Status:** Proposed; **Priority:** P0 candidate.
- **Actor:** Ingestion service.
- **Preconditions:** Repository reference is valid; configured credentials, if needed, are available.
- **Behavior:** Retrieve only approved issue fields, handle pagination, timeouts, rate limits, and external API errors.
- **Inputs:** Repository reference and approved filters.
- **Outputs:** Source records or a typed failure/partial-result report.
- **Errors:** Authentication/authorization failure, 404, rate limit, network timeout, malformed response.
- **Acceptance:** Pagination is tested; failures are distinguishable; secrets are never included in logs.
- **Dependencies:** GitHub integration decision, canonical data contract.
- **Verification:** Mocked HTTP tests and controlled opt-in integration test.

#### FR-003 — Normalize and validate issue records
- **Status:** Proposed; **Priority:** P0 candidate.
- **Actor:** Data ingestion.
- **Behavior:** Map approved source fields into canonical models; validate types and timestamps; preserve source identifiers.
- **Inputs:** GitHub response records.
- **Outputs:** Valid normalized records plus explicit validation diagnostics.
- **Errors:** Missing required identifiers, malformed timestamps, unexpected types.
- **Acceptance:** Valid fixtures normalize deterministically; invalid records do not silently appear as valid.
- **Dependencies:** Shared schema, DATA requirements.
- **Verification:** Unit and fixture tests.

#### FR-004 — Handle repeated retrieval safely
- **Status:** Awaiting approval; **Priority:** P0 if persistence/incremental sync is approved.
- **Actor:** Ingestion/storage.
- **Behavior:** Re-fetching the same issue must not create duplicate logical records; update policy must be explicit.
- **Inputs:** Existing and newly retrieved source records.
- **Outputs:** Insert/update/no-op result or typed failure.
- **Acceptance:** Idempotency behavior is demonstrated with repeated and changed fixtures.
- **Dependencies:** Storage decision and schema.
- **Verification:** Storage integration tests.

### Issue presentation and analysis

#### FR-005 — Display issue results
- **Status:** Proposed; **Priority:** P0 candidate.
- **Actor:** Repository maintainer / developer.
- **Behavior:** Display issue title, number, state, labels, timestamps, and links only where approved and available.
- **Inputs:** Valid API response.
- **Outputs:** Readable issue list/details.
- **Errors:** Empty results, loading, API failure, partial data.
- **Acceptance:** UI distinguishes loading, empty, success, and failure states; missing optional fields do not crash the view.
- **Dependencies:** API response contract, frontend.
- **Verification:** UI smoke tests and API-client tests.

#### FR-006 — Provide issue categorization
- **Status:** Awaiting approval; **Priority:** P1 candidate.
- **Actor:** ML engine.
- **Behavior:** Generate category labels only after taxonomy, model, and evaluation criteria are approved.
- **Inputs:** Approved issue text/metadata.
- **Outputs:** Category and confidence/evidence fields according to shared schema.
- **Errors:** Empty text, unsupported input, model unavailable.
- **Acceptance:** Output schema is stable; model failures are explicit; evaluation results meet approved targets.
- **Dependencies:** ML design, labelled evaluation set, privacy review.
- **Verification:** Model evaluation tests.

#### FR-007 — Suggest similar or duplicate issues
- **Status:** Awaiting approval; **Priority:** P1 candidate.
- **Actor:** ML/retrieval engine.
- **Behavior:** Return candidate related issues with relevance signals; do not automatically close, merge, or modify issues.
- **Inputs:** Issue text and candidate corpus.
- **Outputs:** Ranked candidates and explainable references.
- **Errors:** No candidates, stale index, retrieval unavailable.
- **Acceptance:** Empty/no-match state is clear; relevance is evaluated against a curated dataset.
- **Dependencies:** Definition of similarity, retrieval strategy, data scope.
- **Verification:** Ranking evaluation and negative tests.

#### FR-008 — Retrieve relevant code context
- **Status:** Awaiting approval; **Priority:** P1 candidate.
- **Actor:** Code retrieval engine.
- **Behavior:** Link issue context to scoped candidate files/snippets with repository/path/commit metadata where available.
- **Inputs:** Issue and repository context.
- **Outputs:** Ranked code references, or an explicit no-match/unavailable state.
- **Errors:** Repository inaccessible, incomplete checkout/index, oversized repository, rate limit.
- **Acceptance:** Results remain within authorized repository scope; source references are traceable; failure is not misrepresented as no match.
- **Dependencies:** Retrieval architecture, access policy, evaluation set.
- **Verification:** Retrieval relevance and permission tests.

#### FR-009 — Show analysis provenance
- **Status:** Proposed; **Priority:** P1 candidate.
- **Actor:** User.
- **Behavior:** Where analysis is shown, distinguish GitHub source fields from derived model output and expose limitations/provenance appropriate to the feature.
- **Acceptance:** UI does not present predictions as authoritative source facts; unavailable confidence/evidence is not fabricated.
- **Dependencies:** ML/retrieval contracts.
- **Verification:** UI review and contract tests.

### API, configuration, and operations

#### FR-010 — Expose approved capabilities through FastAPI
- **Status:** Proposed (FastAPI is repeatedly planned); **Priority:** P0 candidate.
- **Actor:** Streamlit client / API consumer.
- **Behavior:** Provide documented, validated operations based on the separately approved API contract.
- **Acceptance:** Routes, schemas, status codes, and error shapes match the API contract; no paths are invented in this requirements document.
- **Dependencies:** API Contract and Integration Standards manual.
- **Verification:** Contract and API tests.

#### FR-011 — Provide Streamlit dashboard
- **Status:** Proposed (Streamlit is repeatedly planned); **Priority:** P0 candidate.
- **Actor:** Repository maintainer / developer.
- **Behavior:** Offer repository selection/configuration and result exploration only to the extent approved.
- **Acceptance:** Handles loading, empty, retryable error, and invalid-input states; UI never exposes secrets.
- **Dependencies:** API client and API contract.
- **Verification:** Smoke tests and workflow review.

#### FR-012 — Validate application configuration
- **Status:** Proposed; **Priority:** P0 candidate.
- **Actor:** Application startup.
- **Behavior:** Validate required configuration at startup and explain missing variable names without printing secret values.
- **Acceptance:** Missing required configuration fails clearly; optional features can be disabled only if designed to be optional.
- **Dependencies:** architecture/configuration decision.
- **Verification:** Startup tests with isolated environment variables.

#### FR-013 — Expose operational health
- **Status:** Proposed; **Priority:** P1 candidate.
- **Actor:** Operator / deployment system.
- **Behavior:** Provide appropriate health/readiness checks and structured diagnostics without leaking internals.
- **Acceptance:** Health semantics distinguish process availability from dependency readiness where needed.
- **Dependencies:** operational design.
- **Verification:** API tests and controlled-failure tests.

## 6. User Workflows

### WF-001: Open dashboard and retrieve issues
1. User opens Streamlit.
2. UI validates required configuration and backend connectivity.
3. User supplies/selects an approved repository reference.
4. Backend validates the request and calls the ingestion service.
5. Ingestion handles pagination and normalizes records.
6. Backend returns contract-compliant results.
7. UI displays records or an actionable empty/error state.
- **Failure paths:** invalid repository, GitHub access denied, rate limit, timeout, no issues, backend unavailable.
- **Requirements:** FR-001, FR-002, FR-003, FR-005, FR-010, FR-011, FR-012.

### WF-002: Explore ML analysis (only if approved)
1. User selects an issue or requests analysis.
2. Backend invokes the ML service through the agreed interface.
3. ML validates inputs and returns a typed result.
4. UI labels the result as derived analysis and displays provenance/limitations.
- **Failure paths:** model unavailable, unsupported input, no prediction, evaluation limitations.
- **Requirements:** FR-006, FR-009.

### WF-003: Explore related issue or code context (only if approved)
1. User opens an issue.
2. Retrieval service searches only the authorized, configured corpus.
3. Service returns ranked candidates with references or an explicit unavailable/no-match response.
4. UI renders links and snippets only where allowed.
- **Failure paths:** inaccessible repository, stale/incomplete index, no match, retrieval failure.
- **Requirements:** FR-007, FR-008, FR-009.

## 7. Non-Functional Requirements

| ID | Requirement | Acceptance / measurement | Status |
|---|---|---|---|
| NFR-001 | Performance | Define representative repository sizes and concurrency, then approve latency targets before release | Awaiting approval |
| NFR-002 | Reliability | External failures, timeouts, and partial ingestion are explicit and recoverable where safe | Proposed |
| NFR-003 | Scalability | Measure actual issue counts, repository sizes, and concurrency before adding infrastructure | Proposed |
| NFR-004 | Maintainability | Separate API, ingestion, storage, ML, retrieval, and UI responsibilities; avoid circular imports | Proposed |
| NFR-005 | Usability/accessibility | Keyboard-usable controls, readable errors, stable navigation, clear result provenance | Proposed |
| NFR-006 | Observability | Structured logs and diagnostics; no secrets or full sensitive payloads by default | Proposed |
| NFR-007 | Testability | Unit tests do not require live GitHub credentials; integration tests are opt-in/controlled | Proposed |
| NFR-008 | Configuration | Environment-specific configuration; safe example file; startup validation | Proposed |
| NFR-009 | Compatibility | Pin and test supported Python/package versions after architecture approval | Awaiting approval |
| NFR-010 | Data integrity | Source IDs, UTC timestamp conventions, validation, duplicate policy defined | Proposed |
| NFR-011 | Security/privacy | Least privilege, secret redaction, data minimization, safe errors, reviewed retention | Proposed |
| NFR-012 | Reproducibility | Clean setup and baseline checks documented and executed before release | Proposed |

Numeric targets for latency, throughput, availability, recovery, and model quality remain decisions; do not fabricate values.

## 8. Data and GitHub Integration

| Data category | Purpose | Source/format | Validation | Storage/retention | Sensitivity |
|---|---|---|---|---|---|
| Repository identity | Scope issue retrieval | GitHub owner/name or canonical URL | Parse and normalize | Persist only if approved | Low to moderate |
| Issue identity | Stable source reference | GitHub repository-scoped issue number and source ID/URL | Do not treat issue number as globally unique | Define uniqueness across repository | Moderate |
| Title/body | Display and analysis | GitHub text fields | Bound size; tolerate missing body | Minimize and set retention if persisted | May contain sensitive content |
| State/labels | Filter and classify | GitHub structured fields | Validate allowed types; preserve unknown labels safely | Per approved storage design | Low to moderate |
| Timestamps | Sorting and freshness | GitHub timestamps | Parse timezone-aware; normalize UTC | Define update policy | Low |
| Code context | Issue investigation | Repository files/snippets | Track path and source revision | Persist/index only if approved | Can be confidential |
| Derived ML output | Decision support | Internal model output | Validate schema and provenance | Version and invalidate if stored | Depends on inputs |

### Integration behavior
- Use GitHub API pagination rather than assuming one response contains all records.
- Set explicit timeouts.
- Respect rate-limit headers and retry-after guidance; use bounded retries with backoff for transient errors.
- Do not blindly retry non-idempotent operations. The initial design should be read-only unless write actions are separately approved.
- Distinguish authentication failure, permission denial, missing repository, rate limit, transient network failure, and invalid response.
- Tests use mocked HTTP responses and synthetic fixtures; live integration tests require explicit configuration.
- Decide whether pull requests are included in addition to issues. GitHub's issue endpoints may represent pull requests as issue-like records, so filtering must be explicit.

## 9. AI and ML Requirements

ML features are optional until approved. For each feature, define:
- Input fields and size limits.
- Output schema and failure behavior.
- Human-review expectations.
- Baseline and evaluation dataset.
- Metrics and acceptance threshold approved by the project owner.
- Model/provider, inference location, resource needs, and privacy implications.
- Version/provenance metadata if outputs are persisted.
- Reproducibility and regression strategy.

Do not select an algorithm, LLM provider, embedding model, or vector store in this document. Candidate features are classification, similarity/duplicate suggestions, prioritization support, and summaries. Any priority score must be advisory unless the product owner explicitly approves another behavior. Do not fabricate confidence values.

## 10. Code Retrieval Requirements

Code retrieval is a proposed capability, not yet a final commitment. The design must establish:
- Which repositories and branches/commits are in scope.
- How repository access is authorized.
- Whether indexing is full or incremental.
- How files are filtered, chunked, and represented.
- How results cite repository, path, and revision.
- How stale indexes and inaccessible files are represented.
- What happens when no relevant result is found.
- How relevance is evaluated and what threshold is accepted.
- Whether source text can be persisted and for how long.

Implementation mechanism (keyword, embeddings, hybrid retrieval, vector database, or another approach) remains open pending architecture review and evaluation.

## 11. API and Frontend Requirements

### FastAPI backend
- Own public HTTP routing, request validation, response serialization, error mapping, and API documentation.
- Delegate ingestion, storage, ML, and retrieval to their owning services.
- Use the API Contract and Integration Standards manual as the source of truth for paths and schemas.
- Never expose stack traces, tokens, filesystem paths, or raw sensitive payloads in public errors.

### Streamlit dashboard
- Own page layout, user input, session state, display, and user-facing error states.
- Call the backend through a single approved API client pattern.
- Do not duplicate business logic or query storage directly.
- Show loading, empty, success, partial-result, and failure states as applicable.
- Do not assume authentication or user accounts until approved.

## 12. Security and Privacy

| ID | Requirement | Acceptance | Status |
|---|---|---|---|
| SEC-001 | Secrets stay outside source control | `.env` ignored; only placeholders in `.env.example`; secret scan/review | Proposed |
| SEC-002 | Least-privilege GitHub access | Document token/app permissions; read-only access unless writes approved | Awaiting approval |
| SEC-003 | Validate untrusted inputs | Repository refs, query params, external payloads validated | Proposed |
| SEC-004 | Redact secrets | Logs/errors omit tokens and authorization headers | Proposed |
| SEC-005 | Minimize retained content | Persist only approved fields; retention/deletion policy documented | Awaiting approval |
| SEC-006 | Respect private repository boundaries | No cross-repository leakage; test access-denied paths | Awaiting approval |
| SEC-007 | Safe error responses | No stack traces or internal details in production responses | Proposed |
| SEC-008 | Dependency security | Supported dependency scanning and remediation process | Proposed |
| SEC-009 | Secure deployment configuration | No credentials in committed config; access controls reviewed | Proposed |

Security reviewer must assess private repository content, logs, retention, model-provider data handling, dependency risks, and deployment secret management. No regulatory compliance claim is made.

## 13. Scope Boundaries

### In scope — proposed initial baseline
- Repository reference validation.
- Read-only GitHub issue retrieval and normalization.
- Basic issue display through the planned API and Streamlit interface.
- Explicit loading/empty/error states.
- Configuration validation, safe logging, and automated tests.
- Clear documentation and reproducible local setup.

This baseline still requires project-owner approval.

### Out of scope — not currently approved
- Automatic issue closure, labelling, assignment, or commenting.
- Automatic code changes or pull-request creation.
- Multi-tenant SaaS administration.
- Billing, user management, and organization-wide analytics.
- Guaranteed AI correctness or autonomous triage.
- Production deployment to a specific cloud provider before approval.

These are not permanent exclusions; they are not part of the current approved baseline because no approval evidence is available.

### Future enhancements — candidates
- Duplicate detection and issue clustering.
- Prioritization and summaries.
- Code context retrieval.
- Webhooks and incremental synchronization.
- Background jobs, external cache, vector database, centralized telemetry.
- Team analytics and integrations beyond GitHub.

## 14. Acceptance Criteria

Project acceptance requires:
1. Project owner approves initial scope and open decisions.
2. Valid repository input retrieves the approved issue fields through a controlled test.
3. Pagination and common GitHub failure scenarios are covered by automated tests.
4. Normalization is deterministic and invalid records are handled explicitly.
5. UI presents success, empty, loading, and error states.
6. API contract tests pass and documentation matches actual endpoints.
7. Secrets are not committed or emitted in logs/errors.
8. Tests run without production credentials.
9. Any approved ML/retrieval feature meets its separately approved evaluation criteria.
10. Setup, troubleshooting, configuration, and limitations are documented.
11. End-to-end validation is run and actual results are recorded.
12. No critical/high security finding is silently ignored.

Items dependent on implementation are **not verified** at document creation.

## 15. Definition of Done

A requirement is complete only when its acceptance criteria are linked to evidence: code review, automated test, evaluation report, or verified manual procedure. Code written alone is not proof of completion.

- Functional and negative paths tested.
- Shared contracts match API and package implementations.
- Data integrity and idempotency tested where storage exists.
- ML/retrieval quality measured where those features are approved.
- Security review completed and findings resolved or explicitly accepted.
- Configuration and secrets safe.
- Observability adequate to diagnose supported failures.
- Clean setup and release checks documented and verified.
- Known limitations and residual risks accepted by an authorized owner.

## 16. Risks and Dependencies

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-001 | GitHub rate limits interrupt ingestion | Medium | High | Pagination, bounded retry/backoff, user-facing diagnostics | Data Engineer | Open |
| R-002 | Ambiguous initial scope causes rework | High | High | Approve scope before implementation | Project Lead / owner | Open |
| R-003 | Inconsistent schemas across modules | Medium | High | Single shared-contract owner and contract tests | API/Integration | Open |
| R-004 | Model outputs are unreliable | Medium | High | Baselines, labelled evaluation, human oversight | ML Engineer | Open |
| R-005 | Retrieval exposes or returns irrelevant code | Medium | High | Scope filters, permission tests, relevance evaluation | Retrieval/Security | Open |
| R-006 | Sensitive issue text leaks into logs/provider | Medium | High | Minimize payloads, redact logs, review provider handling | Security | Open |
| R-007 | Unnecessary infrastructure increases complexity | Medium | Medium | Measure workload; approve infrastructure via ADR | Architect | Open |
| R-008 | Local storage does not support deployment needs | Medium | Medium | Document concurrency/backup limits; validate target | Storage/DevOps | Open |
| R-009 | No verified repository or tests exist yet | Confirmed planning gap | High | Bootstrap only after decisions; record actual checks | Project Lead | Open |

### Dependency chain
Scope approval → architecture and shared contracts → repository/environment → storage and ingestion interfaces → ingestion/storage → ML and retrieval (if approved) → backend → frontend → integration → security/QA/performance → deployment → handover.

## 17. Traceability Matrix

| Requirement | Feature | Owner | Manual | Verification | Status |
|---|---|---|---|---|---|
| FR-001/002 | Repository validation and GitHub retrieval | Data Engineer | `ORDO_Data_Engineer_Blueprint.md` | HTTP mocks + controlled integration | Proposed |
| FR-003/004 | Normalization and idempotency | Data + Storage | `ORDO_Database_Data_Storage_Engineer_Blueprint.md` | Fixture/storage tests | Proposed |
| FR-005 | Issue display | Frontend | `ORDO_Streamlit_Frontend_Engineer_Blueprint.md` | UI smoke tests | Proposed |
| FR-006/007 | Classification/similarity | ML | `ORDO_ML_Engineer_Blueprint.md` | Evaluation suite | Awaiting approval |
| FR-008 | Code context | Retrieval | `ORDO_Code_Retrieval_Engineer_Blueprint.md` | Relevance/access tests | Awaiting approval |
| FR-010 | Public API | Backend/API owner | `ORDO_FastAPI_Backend_Engineer_Blueprint.md`; `ORDO_API_Contract_Integration_Standards_Blueprint.md` | Contract/API tests | Proposed |
| FR-011/012 | Dashboard/config | Frontend/Platform | Frontend + DevOps manuals | Smoke/startup tests | Proposed |
| NFR-001/002 | Performance/reliability | Performance Engineer | `ORDO_Performance_Reliability_Engineer_Blueprint.md` | Workload/failure tests | Targets awaiting approval |
| SEC-001–009 | Security/privacy | Security reviewer | `ORDO_Security_Privacy_Reviewer_Blueprint.md` | Security tests/review | Proposed |
| NFR-006 | Observability | Observability Engineer | `ORDO_Monitoring_Logging_Observability_Blueprint.md` | Controlled-failure checks | Proposed |
| Release DoD | CI/deployment/docs | DevOps/Release/Docs | Corresponding manuals | Pipeline + release checklist | Not verified |

## 18. Proposed Implementation Phases

1. **Requirements confirmation:** approve P0 scope, metrics, data/privacy boundaries.
2. **Architecture and interface decisions:** approve component boundaries, API contract, storage, ML/retrieval choices.
3. **Repository/environment setup:** create approved monorepo, runtime and tooling, safe configuration.
4. **Shared contracts and data design:** canonical issue models, error format, service interfaces.
5. **Ingestion and storage:** implement read-only ingestion; storage only if approved.
6. **ML and code retrieval:** parallelize only after data and interface contracts are stable; optional features can be deferred.
7. **Backend:** implement approved API and service orchestration.
8. **Frontend:** build against the stable API contract.
9. **Integration:** exercise end-to-end workflows.
10. **Security and quality:** remediate findings, regression tests, evaluate performance.
11. **Deployment and release:** only after target and secrets are approved.
12. **Operational handover:** documentation, known limitations, ownership and recovery guidance.

Independent tasks such as documentation templates, fixture preparation, and threat modelling can proceed in parallel. Schema/API consumers must wait for the relevant contracts.

## 19. Assumptions and Open Questions

| ID | Question | Why it matters | Required approver |
|---|---|---|---|
| OQ-001 | What exact capabilities define the first release? | Determines scope and phase gates | Project owner |
| OQ-002 | Public repositories only, or private repositories too? | Permissions, secrets, privacy | Owner + Security |
| OQ-003 | Issues only, or include pull requests? | API semantics and filters | Product owner |
| OQ-004 | Is persistence required for first release? | Database, retention, sync | Architect + owner |
| OQ-005 | Which ML feature, if any, is P0? | Model, evaluation and resources | Product owner |
| OQ-006 | Is code retrieval required for first release? | Indexing, storage and permissions | Product owner |
| OQ-007 | Which authentication model is required? | API and UI access control | Security + owner |
| OQ-008 | What deployment target and workload are expected? | Performance, operations and cost | Owner/DevOps |
| OQ-009 | What are acceptable latency and quality targets? | Release acceptance | Owner + engineering |
| OQ-010 | What are retention, deletion, RPO and RTO requirements? | Storage and operations | Owner + Security/Storage |

## 20. Approval and Change History

| Version | Date | Change | Status |
|---|---|---|---|
| 0.1 | 2026-10-27 | Initial requirements baseline generated from available ORDO planning context | Draft; approval pending |

### Approval checklist
- [ ] Initial-release scope approved.
- [ ] Repository access model approved.
- [ ] Storage and retention decision approved.
- [ ] ML/retrieval scope approved or explicitly deferred.
- [ ] API contract and architecture approved.
- [ ] Success metrics and performance targets approved.
- [ ] Security/privacy review completed.
