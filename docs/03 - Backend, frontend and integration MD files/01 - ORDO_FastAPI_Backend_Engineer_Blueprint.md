# ORDO FastAPI Backend Engineer Blueprint

**Artifact:** `ORDO_FastAPI_Backend_Engineer_Blueprint.md`\
**Project:** ORDO --- AI-powered GitHub Issue Intelligence Platform\
**Prepared:** 26 October 2026\
**Status:** Implementation manual; examples are provisional until
checked against the live repository.

> **Evidence limitation:** The prompt and ORDO planning material are
> available, but no live source repository, manifests, source files,
> lockfiles, or CI logs were available for inspection. This manual does
> not claim that routes, package interfaces, configuration, tests,
> Docker, or workflows already exist. Confirm every path and contract
> against the checked-out repository. Example code is provisional, not
> an approved API contract.

## How to use this manual

Proceed in order. Record observations, exact commands, test outcomes,
and open decisions. Do not overwrite existing work to make the
repository match examples. Labels: **Verified** = directly inspected;
**Approved** = accepted by Team Lead and relevant owners; **Proposed** =
example awaiting confirmation; **Blocked** = requires a
decision/interface.

# 1. Role Overview

## Objective

Build the HTTP application layer for ORDO. FastAPI exposes approved
product capabilities through stable contracts and orchestrates existing
domain packages; it must not reimplement ingestion, ML inference,
ranking, or retrieval algorithms owned elsewhere.

## Responsibilities

-   Inspect repository, requirements, existing routes, package
    interfaces, and CI before coding.
-   Turn approved requirements into route, request, response, error, and
    authorization contracts.
-   Implement app wiring, routing, validation, service orchestration,
    serialization, config, lifecycle, and API-level errors.
-   Integrate approved interfaces from `packages/data_ingestion/`,
    `packages/ml_engine/`, and `packages/code_retrieval/` only after
    inspecting their public interfaces.
-   Add deterministic unit, route, contract, and integration tests.
-   Keep OpenAPI documentation accurate.
-   Coordinate shared schemas, security decisions, and root/deployment
    changes with owners.
-   Report test evidence, limitations, and blockers honestly.

## Ownership boundaries

  ----------------------------------------------------------------------------
  Area                         Expected responsibility API engineer boundary
  ---------------------------- ----------------------- -----------------------
  `apps/api/`                  HTTP application and    Primary area if
                               orchestration           confirmed

  `packages/data_ingestion/`   GitHub collection,      Call public interface;
                               normalization,          do not silently rewrite
                               persistence/sync        

  `packages/ml_engine/`        Predictions and         Call approved
                               inference contracts     interface; do not
                                                       duplicate model logic

  `packages/code_retrieval/`   Search, ranking,        Call approved
                               indexing, retrieval/RAG interface; do not copy
                                                       algorithms

  `shared/`                    Shared                  Propose changes; obtain
                               schemas/contracts       approval

  `apps/web/`                  Dashboard/client        Agree request/response
                                                       needs; avoid UI-owned
                                                       changes

  `tests/`                     Shared tests            Follow established
                                                       layout and coordinate
                                                       fixtures

  `infra/`,                    Deployment/CI           Change only when
  `.github/workflows/`                                 assigned and approved

  Security/Privacy Reviewer    Threat model, security  Implement API controls
                               review, evidence        and coordinate risks
  ----------------------------------------------------------------------------

Ownership is a collaboration agreement, not automatic folder-level
enforcement through GitHub permissions.

## Deliverables

1.  Repository reconnaissance report.
2.  Approved endpoint inventory and contract references.
3.  Scoped API code and tests.
4.  Accurate OpenAPI docs and safe examples.
5.  Approved config/deployment changes only where needed.
6.  PR with exact test commands/results, security notes, limitations,
    and dependencies.
7.  Handover note distinguishing completed, verified, and blocked work.

## Definition of done

A successful Uvicorn startup is not enough. All mandatory contracts,
integrations, security requirements, tests, docs, CI, deployment
expectations, and handover items must be satisfied.

**Checkpoint:** \[ \] Scope approved \[ \] Owners clear \[ \] Existing
code inspected \[ \] Unknowns recorded.

# 2. Backend Architecture

## Proposed logical architecture --- verify against the repository

``` mermaid
flowchart TD
    A[Approved API Client / Dashboard] --> B[FastAPI Routes]
    B --> C[Validation and Authentication]
    C --> D[Application Services]
    D --> E[Code Retrieval Package]
    D --> F[ML Engine]
    D --> G[Data Ingestion / Approved Data Access]
    E --> H[Approved Shared Contracts]
    F --> H
    G --> H
    H --> I[Response Schema and Serialization]
    I --> J[HTTP Response]
    K[Configuration / Dependency Wiring] --> B
    K --> D
    L[Logging / Error Handling] --- B
    M[Tests] -. verify .-> B
```

This is a planning diagram, not proof that every component exists or
runs separately. ORDO planning describes a logical flow from GitHub
issue collection through shared contracts and approved storage to
ML/retrieval and the API. Confirm the actual storage and public
interfaces. Do not assume a database, identity provider, broker, or
separate service exists.

## Request lifecycle

``` mermaid
sequenceDiagram
    participant C as Client
    participant R as FastAPI Route
    participant V as Validation/Security
    participant S as Application Service
    participant P as Approved Package
    C->>R: HTTP request
    R->>V: Parse and validate
    alt Invalid or unauthorized
        V-->>C: Structured 4xx response
    else Valid and authorized
        V->>S: Validated values and trusted context
        S->>P: Documented package call
        P-->>S: Result or typed failure
        S-->>R: Public result or mapped error
        R-->>C: Schema-validated response
    end
```

-   **Entry point:** app instance/factory, routers, lifecycle, exception
    handlers.
-   **Routes:** HTTP method/path, dependencies, status codes, mapping to
    service calls.
-   **Schemas:** public request/response types and constraints; reuse
    authoritative shared models.
-   **Dependencies:** construct or provide services and request-scoped
    resources.
-   **Services:** orchestrate packages and translate domain outcomes;
    keep transport logic at the API boundary.
-   **Domain packages:** ingestion, ML, retrieval, ranking, and
    persistence.
-   **Configuration:** validate settings through the existing mechanism.
-   **Exceptions/logging/tests:** stable safe errors, useful
    non-sensitive telemetry, and contract verification.

## Validation and error flow

``` mermaid
flowchart TD
    A[Request] --> B{Route exists?}
    B -- No --> E[404]
    B -- Yes --> C[Parse and validate]
    C -- Invalid --> F[422 or approved validation format]
    C -- Valid --> D{Auth required?}
    D -- Required --> G{Identity and permission valid?}
    G -- No identity --> H[401]
    G -- Denied --> I[403 or approved 404 policy]
    G -- Allowed --> J[Service]
    D -- Not required --> J
    J --> K{Outcome}
    K -- Missing resource --> L[Documented not-found response]
    K -- Dependency unavailable --> M[503 or approved retryable response]
    K -- Unexpected failure --> N[Safe 500 and internal log]
    K -- Success --> O[Validate public output]
    O --> P[HTTP response]
```

**Checkpoint:** \[ \] Diagrams reflect actual architecture \[ \] No
hypothetical infrastructure presented as deployed \[ \] Ownership and
contracts documented.

# 3. Environment Setup

## Objective and prerequisites

Use the package manager, Python version, and lockfile the repository
already defines. Prerequisites: approved repository access, Git,
supported Python, required local dependencies, and test fixtures.
Ordinary unit tests should not require production credentials.

## Working directory

Start at the actual repository root; `ordo-monorepo/` is expected only
if verified.

## Inspect first

``` bash
git status --short
git branch --show-current
git branch -a
git log -5 --oneline
git remote -v
git ls-files
```

Windows CMD: `dir` and `tree /F`. PowerShell: `Get-ChildItem -Force` and
`Get-ChildItem -Recurse -File`. macOS/Linux:
`find . -maxdepth 4 -type f | sort`.

Do not print `.env` values or secrets. Check existence only,
e.g. PowerShell `Test-Path .env`.

## Identify interpreter and package manager

``` bash
python --version
python -m pip --version
```

Windows launcher, if installed: `py --list`. Inspect `pyproject.toml`,
lockfiles, requirements, README, and CI before choosing
pip/uv/Poetry/workspace commands.

If the project explicitly requires Python 3.12 and it is installed:

``` bat
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

macOS/Linux equivalent:

``` bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

If another version is specified, use that version. If missing, install
the approved interpreter or ask the Team Lead. Do not introduce a
competing package manager. Install dependencies using the exact
README/lockfile workflow; do not blindly run every package-manager
example.

## Environment and startup

Copy `.env.example` only if it exists and the README requires it. CMD:
`copy .env.example .env`; PowerShell: `Copy-Item .env.example .env`.
Never commit `.env`. If no example exists, confirm required settings
before creating one.

If reconnaissance confirms `apps/api/main.py` exposes `app`, a possible
command from root is:

``` bash
python -m uvicorn apps.api.main:app --reload
```

This import path is provisional; use the actual entry point. Stop with
`Ctrl+C`.

If pytest is confirmed:

``` bash
python -m pytest --collect-only
python -m pytest
```

  -----------------------------------------------------------------------
  Failure                 Diagnose                Resolution
  ----------------------- ----------------------- -----------------------
  Wrong Python            `python --version`;     Activate correct
                          Windows `where python`, environment
                          Unix `which python`     

  Import error            Check working directory Follow monorepo
                          and package setup       packaging; avoid
                                                  `sys.path` hacks

  Dependency conflict     Check Python/lockfile   Use approved
                                                  lockfile/interpreter

  Missing setting         Check safe config names Confirm
                          and docs                required/optional
                                                  status

  Port occupied           Identify process and    Do not kill unknown
                          approved port override  process

  Tests hit network       Test isolation          Override/mock external
                          incomplete              dependency
  -----------------------------------------------------------------------

**Checkpoint:** \[ \] Root/branch verified \[ \] Python correct \[ \]
Existing dependency workflow used \[ \] Secrets protected \[ \] Startup
and tests verified.

# 4. API Requirements and Contract Design

Derive the API from approved requirements, existing tests, shared
schemas, dashboard needs, and package-owner agreements. Where sources
disagree, log a decision request; do not silently choose.

The ORDO planning material identifies decisions such as repository
submission format, validation/errors, job IDs and lifecycle if
asynchronous, progress/partial-data warnings, result/evidence links,
pagination/filtering, auth, timeouts/retries, and safe fallback
behavior.

## Endpoint inventory template

  -----------------------------------------------------------------------------------------
  Category         Method/path    Status         Contract/dependency   Owner
  ---------------- -------------- -------------- --------------------- --------------------
  Liveness         Not confirmed  Proposed       Minimal process       Team Lead/API
                                                 status                

  Readiness        Not confirmed  Proposed       Mandatory             API/DevOps
                                                 dependencies only     

  Issue search     Not confirmed  Blocked until  Query, filters,       API/Retrieval/Data
                                  approved       pagination, result    
                                                 schema                

  Issue details    Not confirmed  Proposed       Stable issue identity API/Data
                                                 and metadata          

  ML insights      Not confirmed  Blocked until  Inputs, outputs,      API/ML
                                  ML contract    version/evidence if   
                                                 approved              

  Ingestion        Not confirmed  Do not expose  Auth, idempotency,    API/Data/Security
  trigger/status                  without        lifecycle if needed   
                                  approval                             
  -----------------------------------------------------------------------------------------

For every approved endpoint, record method/path, purpose, request
params/body, schema, validation, success/error statuses, auth and
resource access, pagination, timeouts, dependencies, owner,
compatibility, tests, and docs.

## Contract-change workflow

1.  Propose reason and scope.
2.  Identify producers, consumers, tests, and docs.
3.  Obtain owner approval for
    names/types/nullability/IDs/timestamps/compatibility.
4.  Update owning modules and contract tests.
5.  Update OpenAPI/client examples.
6.  Record and announce the decision.

**Checkpoint:** \[ \] Existing/approved/proposed/blocked separated \[ \]
Contracts approved \[ \] Owners named.

# 5. FastAPI Application Structure

Inspect before creating files. If no structure exists, propose the
smallest suitable structure and obtain approval.

``` text
ordo-monorepo/
├── apps/api/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── README.md
├── packages/
│   ├── data_ingestion/
│   ├── ml_engine/
│   └── code_retrieval/
├── shared/
│   ├── schemas/
│   └── contracts/
├── tests/
└── pyproject.toml
```

Illustrative only. Reuse existing names and layout.

  ----------------------------------------------------------------------------
  Path                         Responsibility          Action
  ---------------------------- ----------------------- -----------------------
  `apps/api/main.py`           App, router             Verify existing entry
                               registration, lifespan  point

  `apps/api/routes/`           HTTP routes             Reuse conventions

  `apps/api/schemas/`          API-only models         Reuse shared
                                                       authoritative schema

  `apps/api/services/`         Orchestration           Add only when useful

  `apps/api/dependencies.py`   Service/resource        Reuse DI pattern
                               injection               

  `apps/api/config.py`         Settings                Reuse current config

  `apps/api/exceptions.py`     Error mapping           Reuse current error
                                                       format

  `tests/api/` or actual       API tests               Follow repository
  equivalent                                           layout

  `docs/api/` or actual docs   Approved contracts      Verify ownership
  path                                                 
  ----------------------------------------------------------------------------

Keep HTTP behavior in API layer, domain behavior in the owner package.
Avoid circular imports, duplicated business logic, and abstractions with
no clear benefit. Root/shared changes need approval.

**Checkpoint:** \[ \] Actual paths and ownership recorded \[ \] Existing
conventions win \[ \] No neighboring package changed without approval.

# 6. Application Entry Point and Lifecycle

Confirm import path, router modules, settings, lifecycle resources, and
error handlers first. Avoid model loading or remote calls during module
import.

**Provisional example only**, for a new minimal API with no mandatory
external resources. Adapt rather than replace an existing app factory:

`apps/api/main.py`

``` python
from fastapi import FastAPI

app = FastAPI(
    title="ORDO API",
    description="API for the ORDO issue intelligence platform.",
    version="0.1.0",
)

# Register only approved routers after their contracts are implemented.
# from apps.api.routes.health import router as health_router
# app.include_router(health_router)
```

This creates the app object; it does not pretend product routes exist.
Activate router registration only after the real module and contract are
confirmed.

For lifespan resources, document constructor/cleanup, mandatory vs
optional status, startup failure, readiness behavior, worker copies, and
test injection. Do not report readiness as healthy if a mandatory
dependency is down.

**Verification:** use the confirmed server command; inspect registered
paths through OpenAPI and a local smoke test.

**Checkpoint:** \[ \] No import-time network calls \[ \] Approved
routers only \[ \] Startup/shutdown policy clear \[ \] Readiness
accurate.

# 7. Configuration and Environment Variables

Inspect existing settings classes, dotenv loading, variable names,
`.env.example`, deployment manifests, and tests. Do not add a second
settings library without approval.

  -------------------------------------------------------------------------------------------
  Setting           Required?       Secret?              Source/use           Validation
  ----------------- --------------- -------------------- -------------------- ---------------
  App environment   Usually         No                   Deployment/logging   Allowed names
                    optional                             policy               

  Log level         Usually         No                   Logging              Valid level
                    optional                                                  

  CORS origins      If browser CORS No,                  Deployment           Explicit origin
                    needed          security-sensitive                        list

  Retrieval/index   If required by  Depends              Retrieval adapter    Owner-defined
  config            package                                                   

  Model config      If ML feature   Depends              ML adapter           Owner-defined
                    required                                                  

  Credentials       Only if         Yes                  Secret manager/env   Never log
                    approved                                                  
                    auth/provider                                             
                    needs them                                                
  -------------------------------------------------------------------------------------------

A safe `.env.example` contains only confirmed settings and harmless
placeholders. Required values should fail clearly at startup; optional
values need safe defaults. Tests should override config without editing
a developer's real `.env`. Keep environments separate.

**Checkpoint:** \[ \] Existing config mechanism reused \[ \]
Required/optional documented \[ \] Missing required settings fail
clearly \[ \] Secrets excluded from code/logs \[ \] Tests isolate
settings.

# 8. Request and Response Schemas

Use the installed Pydantic version and established schema conventions.
Do not duplicate authoritative models from `shared/schemas/`, expose
internal ORM/model/vector objects, or invent public fields.

For each schema, define types, required/optional/null behavior,
defaults, constraints, unknown-field policy, stable IDs, UTC/timestamp
serialization, upstream/downstream compatibility, and public versus
internal fields.

Provisional pagination example, **only if offset pagination is
approved** and Pydantic v2 is installed:

``` python
from pydantic import BaseModel, ConfigDict, Field


class PageRequest(BaseModel):
    """Illustrative pagination input, not an approved ORDO contract."""

    model_config = ConfigDict(extra="forbid")

    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
```

This demonstrates bounds and rejecting unknown fields; it does not imply
ORDO should use offset rather than cursor pagination.

Test valid input, missing fields, invalid types, bounds, unknown fields,
empty strings, null vs missing, and serialization. Use timezone-aware
timestamps and agreed UTC policy.

**Checkpoint:** \[ \] Contract match \[ \] Shared schema reused \[ \]
Boundary tests \[ \] No internal metadata leak.

# 9. Health and Readiness Endpoints

Implement only if required. **Liveness** is a cheap process-level check;
**readiness** verifies that the app can serve intended requests and must
include every mandatory dependency in its approved policy. Liveness must
not perform expensive remote checks.

Provisional router if no equivalent exists and `/health/live` is
approved: `apps/api/routes/health.py`

``` python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health/live", summary="Check API process liveness")
def liveness() -> dict[str, str]:
    """Process-level check; do not call external dependencies here."""
    return {"status": "alive"}
```

Wire it only after confirming imports and approval:

``` python
from apps.api.routes.health import router as health_router

app.include_router(health_router)
```

This is not a readiness implementation. Do not label it `/ready`.
Readiness needs an agreed dependency list, bounded checks,
timeout/failure mapping, and tests.

Provisional test, if path and dependencies are confirmed:

``` python
from fastapi.testclient import TestClient
from apps.api.main import app


def test_liveness_returns_success() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
```

Run `python -m pytest tests/api/test_health.py -q` from root if pytest
and this layout are confirmed. This test has not been executed during
preparation of this manual.

**Checkpoint:** \[ \] Liveness cheap \[ \] Readiness policy accurate \[
\] Response/status documented \[ \] Healthy and unavailable cases
tested.

# 10. Implement the Search or Retrieval API

Expose retrieval only after the API owner and Code Retrieval Engineer
approve request/result contracts. Agree query, repository scope, issue
state/labels, top-k bounds, pagination, result IDs, score semantics,
evidence links, empty-result behavior, timeout, auth, and errors.
Confirm whether search covers issues, code, or both.

``` mermaid
flowchart TD
    A[Approved search request] --> B[Validate query and filters]
    B --> C{Auth required?}
    C -- Yes --> D[Authorize repository scope]
    C -- No --> E[Application service]
    D -->|Denied| F[401/403]
    D -->|Allowed| E
    E --> G[Approved retrieval adapter]
    G --> H{Outcome}
    H -->|Matches| I[Map public result schema]
    H -->|Empty| J[Documented empty result]
    H -->|Unavailable/timeout| K[Approved retryable error]
    H -->|Unexpected| L[Safe 500 + internal log]
    I --> M[HTTP response]
    J --> M
```

Implementation sequence: inspect package source/tests; confirm
constructor, input/output, exceptions, lifecycle and sync/async
behavior; approve shared schema and auth; add an API adapter only if
useful; validate and authorize; invoke bounded search; map output;
translate errors; test success, empty results, invalid filters, timeout,
dependency failure, and access control.

A complete production search route cannot be responsibly supplied until
the actual retrieval interface is known. Inventing a `search()`
method/result object would create a false contract.

**Checkpoint:** \[ \] Interface inspected \[ \] Contracts approved \[ \]
Repository auth enforced \[ \] Failure semantics tested.

# 11. Integration With the Code Retrieval Package

Inspect package exports, README, types, tests, config, index lifecycle,
exceptions, and dependencies. Record:

-   Constructor/factory and settings.
-   Search method and sync/async signature.
-   Input and result schema; score semantics and evidence.
-   Known exceptions and timeout behavior.
-   Index initialization/availability/cleanup.
-   Blocking I/O/CPU work and thread safety.
-   Authorization expectations and private-index isolation.

Do not call long blocking work directly on an async event loop. Use
native async calls when documented; use the repository's
threadpool/offloading pattern only for appropriate blocking I/O;
coordinate CPU-heavy inference/indexing and concurrency with the owner.
Do not blindly wrap async calls in a threadpool.

Use deterministic contract fixtures for unit tests and a separate
integration test for a real local index. No live GitHub credentials or
production index should be needed for unit tests. If no stable public
interface exists, document the blocker and ask the Code Retrieval
Engineer to provide one. Do not modify their package without approval.

**Checkpoint:** \[ \] Public interface documented \[ \]
Execution/lifecycle understood \[ \] Authorization boundary explicit \[
\] Isolated tests \[ \] Integration test when available.

# 12. Integration With the ML Engine

Expose ML features only when approved and use the ML Engineer's public
interface. Confirm input schema, output fields, model/version metadata,
uncertainty semantics, features, exceptions, latency/resource
expectations, initialization, concurrency, and local/remote hosting. Do
not assume hosting mode.

``` mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as Service
    participant M as Approved ML Interface
    C->>A: Validated request
    A->>S: Authorized context
    S->>M: Contract-defined input
    M-->>S: Prediction and approved metadata
    S->>S: Validate/map public output
    S-->>A: Public result
    A-->>C: Documented response
```

Validate input, invoke the approved function, validate output, apply
bounded timeout/concurrency, map known failures, log timing/outcome
without full private bodies, and test invalid input, success, timeout,
unavailable model, malformed output, and version metadata. Predictions
are advisory. Never fabricate scores or silently use an unapproved
fallback.

**Checkpoint:** \[ \] Interface approved \[ \] Model logic stays in ML
package \[ \] Output validated/advisory \[ \] Failures tested \[ \] No
fake fallback.

# 13. Integration With Data Ingestion

Determine whether ingestion is triggered by the API, scheduled, or run
separately. Do not expose ingestion routes by default.

Ask the Data Engineer/Team Lead about canonical repository URL/identity,
allowed URL patterns and redirects, GitHub scopes, pagination/rate
limits/retries, sync vs async, job IDs/statuses, idempotency,
partial-data warnings, private repository authorization, and retention.

If an endpoint is approved, validate and authorize before calling the
package; keep the route thin; use documented response/job contract;
apply rate/size/time limits; and define duplicate submission behavior.
Long-running work should not be disguised as a fast synchronous request.
Durable queues require explicit architecture approval.

User-supplied repository URLs are untrusted. Use a maintained URL
parser, exact host/path allowlist, controlled redirects,
destination/network policy at connection time, timeouts, response-size
limits, and tests proving rejected URLs cause no outbound request.
Parsing alone does not fully prevent SSRF.

**Checkpoint:** \[ \] Trigger mode confirmed \[ \] Route approved \[ \]
Auth/SSRF/retry/idempotency agreed \[ \] Long-running lifecycle
documented \[ \] Privacy/retention reviewed.

# 14. Application Service Layer

Services coordinate packages without duplicating domain logic. For each
service, document responsibility, typed inputs/outputs, dependencies,
exceptions, public interface, timeout, logging/privacy, and tests. Add a
wrapper only when it improves orchestration, testability, or contract
translation.

Use the existing dependency-injection pattern. Routes should obtain
services through dependency providers; tests should override providers
with deterministic fakes. A test fake must not become a production
fallback.

Sequence: define contract test; inject clients; validate/map package
results; authorize before protected data returns; handle known failures;
keep HTTP status mapping at the API boundary unless the existing design
says otherwise.

**Checkpoint:** \[ \] Clear service purpose \[ \] Injectable
dependencies \[ \] No duplicated domain logic \[ \] Typed failure
mapping \[ \] Unit tests without external services.

# 15. Error Handling and HTTP Status Codes

  -----------------------------------------------------------------------
  Code                                Appropriate use
  ----------------------------------- -----------------------------------
  `200`                               Successful read/search with body

  `201`                               Resource created

  `204`                               Success with no body

  `400`                               Malformed request or application
                                      rule failure

  `401`                               Missing/invalid auth when required

  `403`                               Authenticated but not permitted

  `404`                               Missing resource or approved
                                      anti-enumeration behavior

  `409`                               State/idempotency conflict

  `422`                               Schema/field validation failure,
                                      consistent with FastAPI behavior

  `429`                               Enforced rate limit exceeded

  `500`                               Unexpected server failure

  `503`                               Mandatory dependency unavailable
  -----------------------------------------------------------------------

Use only codes that match endpoint semantics. Map validation errors
safely; distinguish missing from inaccessible resources per policy;
translate dependency timeouts/unavailability; never return raw exception
text. Unexpected errors should be logged internally with
request/correlation ID and returned as a generic public error.

Proposed envelope, only if approved:

``` json
{
  "error": {
    "code": "DEPENDENCY_UNAVAILABLE",
    "message": "The requested capability is temporarily unavailable.",
    "request_id": "server-generated-correlation-id"
  }
}
```

Test invalid input, not-found, denied access, timeout, dependency
unavailable, and unexpected exceptions. Assert that public bodies do not
expose stack traces, file paths, secrets, or private issue text.

**Checkpoint:** \[ \] Error format approved \[ \] Status semantics
correct \[ \] Safe public messages \[ \] Useful private diagnostics.

# 16. Authentication and Authorization

First decide with Team Lead and Security/Privacy Reviewer whether the
API is public, internal, or authenticated. Do not invent provider, token
format, signing key, roles, or scopes.

If auth is required: reuse the approved mechanism; validate
signature/issuer/audience/expiry as applicable; extract identity only
after validation; enforce repository-level authorization for every
protected operation; return consistent 401/403 (or approved 404
anti-enumeration); protect secrets; test missing, invalid, expired,
wrong-audience, insufficient-permission, cross-repository, and allowed
cases.

Never fake authentication by accepting any non-empty Authorization
header.

``` mermaid
flowchart TD
    A[Protected request] --> B{Credentials supplied?}
    B -- No --> C[401]
    B -- Yes --> D[Verify approved mechanism]
    D -- Invalid/expired --> E[401]
    D -- Valid --> F[Resolve identity and permissions]
    F --> G{Allowed for resource?}
    G -- No --> H[403 or approved 404]
    G -- Yes --> I[Invoke service with trusted context]
```

**Checkpoint:** \[ \] Requirement decided \[ \] Existing auth reused \[
\] Resource access enforced \[ \] Positive/negative tests \[ \] No fake
checks/secrets.

# 17. CORS, Rate Limiting, and Request Protection

Apply only the controls required by the deployment and threat model.

-   **CORS:** if browser clients need cross-origin access, allow
    explicit approved origins/methods/headers. Avoid wildcard origins
    with credentials. CORS is not auth.
-   **Bounds:** cap query length, result count, pagination, filter/label
    count, and request size at the appropriate layer.
-   **Timeouts:** bound remote calls and expensive package operations.
-   **Rate limiting:** protect endpoints consuming CPU, inference time,
    GitHub quota, or index resources.
-   **Untrusted input:** validate repository URLs and user-controlled
    filters.
-   **Distributed deployment:** an in-memory limiter does not coordinate
    multiple workers/replicas; shared enforcement needs shared state or
    an upstream gateway.

Test maximum and over-limit values, disallowed origins, rate limits
where implemented, and timeout behavior. Record which layer enforces
each control.

**Checkpoint:** \[ \] CORS only when needed \[ \] Explicit production
origins \[ \] Resource bounds \[ \] Rate-limit claims match topology \[
\] Tests exist.

# 18. Logging and Observability

Log startup/shutdown, route template, method/status/duration, request ID
when supported, dependency name/duration/outcome, validation/auth
category, and internal exception details in restricted logs. Avoid
logging API keys, Authorization headers, JWTs, `.env` values, private
issue bodies, sensitive prompt text, and unredacted URLs with sensitive
query parameters.

To diagnose a request: reproduce with request ID/time; locate request
log; check status/duration/dependency; inspect protected internal
traceback; reproduce with service test; fix and add regression test;
verify public response remains safe. Reuse existing logging format; add
structured logging/metrics only if approved.

**Checkpoint:** \[ \] Failure/duration visibility \[ \] Sensitive data
omitted \[ \] Correlation IDs consistent if enabled \[ \] App vs
dependency failures distinguishable.

# 19. Asynchronous Operations and Background Tasks

Choose execution model based on real package behavior. `async def` is
useful when awaiting non-blocking async operations; long blocking work
must not run on the event loop. CPU-heavy inference/indexing needs
owner-approved worker/concurrency design. Apply timeouts and verify
thread safety of shared clients.

FastAPI background tasks are in-process, not a durable queue; work may
be lost on restart and lacks durable retries/status by default. Use only
for short work where those semantics are acceptable. If durable
ingestion/analysis jobs are required, approve queue/job architecture,
IDs/statuses, retries, idempotency, persistence, and failure handling.
Do not add Celery/Redis/brokers without approval.

**Checkpoint:** \[ \] Blocking/async work identified \[ \]
Timeouts/concurrency documented \[ \] Durability accurately described \[
\] Long jobs have approved design.

# 20. Testing Strategy

  -----------------------------------------------------------------------
  Level                   Purpose                 External dependencies
  ----------------------- ----------------------- -----------------------
  Schema/unit             Constraints and pure    None
                          transformations         

  Service unit            Orchestration and error Injected fakes
                          mapping                 

  Route                   HTTP status,            Local app
                          validation, schema, DI  
                          overrides               

  Contract                API/package agreement   Fixtures or owner test
                                                  doubles

  Integration             Real                    Explicitly provisioned
                          package/index/storage   local resources

  End-to-end              Client-to-API workflow  Test environment

  Security                Auth, isolation, SSRF,  Isolated fixtures
                          limits, safe errors     
  -----------------------------------------------------------------------

Every approved endpoint needs tests for success, invalid/missing fields,
bounds, empty/not-found behavior, timeout/unavailable dependency,
unexpected failure, authorization, pagination/filtering, serialization,
and no sensitive leakage as applicable. Unit tests should not require
live GitHub credentials, paid APIs, or network unless clearly labeled
external integration tests.

If pytest is confirmed:

``` bash
python -m pytest tests/api/test_health.py -q
python -m pytest tests/api/test_health.py::test_liveness_returns_success -q
python -m pytest tests/api -q
python -m pytest
python -m pytest --cov=apps.api --cov-report=term-missing
```

Coverage command requires pytest-cov and the confirmed package path. Do
not report coverage unless run. Do not mask defects with broad skips or
swallowed exceptions.

``` mermaid
flowchart TD
    A[Inspect test config] --> B[Run baseline]
    B --> C[Schema/unit tests]
    C --> D[Route and DI tests]
    D --> E[Contract/integration tests]
    E --> F[Run relevant suite]
    F --> G{Pass?}
    G -- No --> H[Diagnose, fix, add regression test]
    H --> F
    G -- Yes --> I[Run full required CI checks]
    I --> J[Record commands and results]
```

**Checkpoint:** \[ \] Real contracts tested \[ \] Unit tests isolated \[
\] Failure/security paths covered \[ \] Relevant and full suites run
honestly.

# 21. API Documentation

Verify whether `/docs`, `/redoc`, and `/openapi.json` are enabled or
customized. For each endpoint document summary, purpose, request
schema/examples, response schema/status, errors, auth/permissions,
pagination/filter semantics, timeout/partial-result behavior, and safe
examples. Examples must match approved endpoints; do not publish
invented `/search` contracts.

Start the confirmed app, inspect configured docs, verify all
routes/schemas/statuses/auth requirements, and add OpenAPI-generation
tests if the project supports them. No real credentials or private data
in examples.

**Checkpoint:** \[ \] Docs match actual behavior \[ \] Examples safe \[
\] Errors/auth documented \[ \] Custom paths recorded.

# 22. Performance and Reliability

Measure before optimizing. Record environment and method for API latency
(median/tail percentiles), retrieval latency, model inference, startup,
memory, concurrency, timeout/error rate, and throughput. Do not invent
latency targets. Ask Team Lead/product owner to approve SLOs, load
profile, query limits, and acceptable failure behavior.

Use bounded timeouts; retry only when safe; never retry non-idempotent
actions without contract; observe external calls/model work; use
graceful fallback only if approved and labeled. Consider caching,
pooling, batching, and concurrency after measuring and defining
freshness/access rules.

**Checkpoint:** \[ \] Baseline measured \[ \] SLOs approved or open \[
\] Retry/fallback safe \[ \] Optimization has before/after evidence.

# 23. Security and Privacy

## Checklist

-   [ ] Secrets externalized and not committed.
-   [ ] Auth matches approved identity design.
-   [ ] Resource-level authorization protects private
    repositories/issues.
-   [ ] User URLs have allowlist and SSRF controls.
-   [ ] Input/resource-intensive filters are bounded.
-   [ ] Errors do not leak stack traces, paths, secrets, or private
    records.
-   [ ] CORS is explicit; rate/request limits are placed correctly.
-   [ ] Logs exclude credentials and private bodies.
-   [ ] Dependencies/lockfiles are checked by approved process.
-   [ ] Environment separation and secure defaults documented.
-   [ ] Retention/deletion expectations clear.
-   [ ] Retrieval cannot leak across users/repositories.
-   [ ] AI/RAG content is treated as untrusted if such features exist.

Responsibilities: API owns request validation, HTTP authorization
enforcement, safe errors, request bounds, and API logging; ingestion
owns collection/fetching/provider scopes; retrieval owns index access
isolation; ML owns inference/output validation; web owns safe rendering;
DevOps owns TLS/network/secrets/container controls; Security Reviewer
owns threat model/review; Team Lead owns architecture and risk
acceptance.

Issue bodies, comments, PR text, code, and retrieved documents are
untrusted. Model instructions must not be overridden by retrieved
content; authorization remains deterministic and server-side. Input
validation alone is not proof of security.

**Checkpoint:** \[ \] Threat model matches actual data flow \[ \]
Controls assigned \[ \] Private access enforced \[ \] Findings tracked
\[ \] Claims supported by evidence.

# 24. Docker and Deployment Integration

Inspect existing Dockerfile, Compose, `infra/`, manifests, health
checks, CI image build, environment injection, port, and shutdown
policy. Do not replace existing infrastructure or add a database to
match an example.

If containerization is approved, verify build context and monorepo
package inclusion, lockfile-based dependencies, correct app command,
non-root execution where policy supports it, runtime-only secrets,
correct port, health check semantics, graceful shutdown, logs, and
service dependencies.

``` mermaid
flowchart TD
    A[Approved code] --> B[Local tests/static checks]
    B --> C[PR review and CI]
    C --> D{Checks pass?}
    D -- No --> E[Fix and rerun]
    E --> B
    D -- Yes --> F[Existing container build]
    F --> G[Smoke test approved environment]
    G --> H[Verify health/readiness/logs]
    H --> I[Approved deployment process]
```

Run only repository-documented build/Compose commands. Record image tag,
configuration version, and test environment. Local startup does not
prove deployment success.

**Checkpoint:** \[ \] Existing workflow reused \[ \] Command/port
verified \[ \] No image-baked secrets \[ \] Health checks correct \[ \]
Build/smoke tests passed.

# 25. CI, Formatting, and Static Checks

Inspect `.github/workflows/`, manifests, README,
formatter/linter/type-check/security configs, and CI job names. Record
actual commands and Python version. Do not assume Ruff, Black, mypy,
Bandit, or any tool is installed.

  ---------------------------------------------------------------------------
  Check                 Actual command    Owner             Required?
  --------------------- ----------------- ----------------- -----------------
  Unit/API tests        Read from         API/QA            Confirm
                        workflow                            

  Formatter             Read from         API/Team Lead     Confirm
                        config/CI                           

  Linter                Read from         API/Team Lead     Confirm
                        config/CI                           

  Type checker          If configured     API/Team Lead     Confirm

  Dependency/security   If configured     Security/DevOps   Confirm
  scan                                                      

  Container build       If configured     DevOps            Confirm

  Contract/OpenAPI      Existing or       API/Team Lead     Confirm
  check                 approved                            
  ---------------------------------------------------------------------------

If a check is missing, propose the smallest change to the responsible
owner. To diagnose CI: read the complete job log; reproduce with the
same interpreter/command; fix the cause; add regression coverage; rerun.
Never weaken checks to make a pipeline green.

**Checkpoint:** \[ \] Local commands match CI \[ \] Checks not weakened
\[ \] Workflow owner approved changes \[ \] Results recorded.

# 26. Troubleshooting Guide

  ------------------------------------------------------------------------------------------------------------------------------------
  Problem                     Possible cause             Diagnostic step                                   Resolution
  --------------------------- -------------------------- ------------------------------------------------- ---------------------------
  Server fails to start       Import/dependency/config   Read full traceback; verify interpreter and cwd   Correct
                              error                                                                        import/dependency/setting

  Endpoint 404                Router not registered or   Inspect OpenAPI and router inclusion              Correct after contract
                              path mismatch                                                                check

  Request 422                 Schema/type validation     Inspect validation response safely                Correct request/schema per
                              failed                                                                       contract

  Search 500                  Retrieval/service failure  Correlate logs and reproduce service test         Fix cause and map known
                                                                                                           failures

  Readiness fails             Mandatory dependency       Inspect readiness checks and dependency health    Restore dependency or
                              unavailable                                                                  correct policy

  Local tests pass, CI fails  Environment mismatch/test  Compare versions, env vars, logs                  Make setup and fixtures
                              leakage                                                                      deterministic

  Import fails                Wrong cwd/package          Inspect packaging and imports                     Follow established install
                              installation                                                                 workflow

  `No module named fastapi`   Wrong interpreter          `python -m pip show fastapi`;                     Activate correct
                                                         `python -c "import sys; print(sys.executable)"`   env/install approved deps

  Port occupied               Existing process           Windows `netstat -ano | findstr :8000`; Unix      Identify process or use
                                                         `lsof -i :8000`                                   approved port

  Browser CORS failure        Origin/method/header       Inspect network details and server logs           Explicitly configure
                              mismatch or other request                                                    approved origin; CORS is
                              failure                                                                      not auth

  Timeout                     Slow dependency/unbounded  Compare route/dependency timings                  Bound work and set approved
                              query                                                                        timeouts

  Empty results               Index absent, stale data,  Verify readiness and known fixture                Fix index/data/filter;
                              filters too strict                                                           never fabricate result

  Serialization error         Package output differs     Contract-test actual result                       Explicit mapping and
                              from schema                                                                  validation

  Secret in logs              Sensitive log context      Inspect logger and synthetic-secret tests         Redact/remove; rotate real
                                                                                                           leak; add regression test

  Merge conflict              Overlapping work/base      `git status`, inspect conflict markers            Resolve with owners and
                              advanced                                                                     rerun tests

  Contract unclear            Missing owner decision     Review approved docs/schemas                      Mark blocked and request
                                                                                                           decision
  ------------------------------------------------------------------------------------------------------------------------------------

Safe diagnostics from root:

``` bash
git status --short
git diff --check
python --version
python -m pip --version
python -m pytest --collect-only
```

**Checkpoint:** \[ \] Root cause evidence captured \[ \] Fix tested \[
\] Regression test added where appropriate.

# 27. Final Verification Checklist

## Requirements and code

-   [ ] Requirements/acceptance criteria approved.
-   [ ] Existing routes/contracts inspected.
-   [ ] Public schemas match shared/package interfaces.
-   [ ] No unapproved endpoint/infrastructure.
-   [ ] Routes orchestrate; domain logic stays with package owners.
-   [ ] Config validated; no secrets committed.
-   [ ] Health/readiness correct if required.
-   [ ] Retrieval/ML/ingestion integration works if required.
-   [ ] Auth/access controls work if required.
-   [ ] Errors consistent and safe; logs non-sensitive.
-   [ ] Timeouts/limits/concurrency appropriate.
-   [ ] OpenAPI/docs match behavior.
-   [ ] Docker/deployment works if required.

Run from root, adapting to actual project:

``` bash
git status --short
git diff --check
git diff --stat
git diff
```

If pytest and these paths are confirmed:

``` bash
python -m pytest tests/api -q
python -m pytest
```

Run the actual formatter/linter/type/security/container commands from
CI. Review staged files before commit:

``` bash
git status --short
git diff --cached --check
git diff --cached
```

Ensure `.env`, credentials, generated indexes, model weights, local
datasets, and unrelated files are not staged.

## Branch/handover

-   [ ] Feature branch based on approved base.
-   [ ] Intended files only.
-   [ ] Relevant/full required checks run and recorded.
-   [ ] PR accurately reports results.
-   [ ] Cross-team dependencies documented.
-   [ ] No unsupported production-readiness claim.

# 28. Pull Request and Team Handover

## Git workflow

Proposed branch: `feature/api/fastapi-backend`, unless the repo
convention differs. Confirm the base branch with Team Lead; use
`develop` only if approved.

``` bash
git status --short
git fetch origin
git branch -a
```

After confirming `<TEAM_APPROVED_BASE_BRANCH>` and safe working tree:

``` bash
git switch <TEAM_APPROVED_BASE_BRANCH>
git pull --ff-only origin <TEAM_APPROVED_BASE_BRANCH>
git switch -c feature/api/fastapi-backend
```

If branch already exists, inspect it. Never discard uncommitted work.
Review and stage only exact paths:

``` bash
git diff --check
git status --short
git diff
git add <APPROVED_API_FILES>
git diff --cached --check
git diff --cached
git commit -m "feat(api): implement ORDO backend endpoints"
git push -u origin feature/api/fastapi-backend
```

Replace placeholders with real paths/branch names. Do not stage the
entire repo indiscriminately. Follow repository merge/rebase policy and
resolve conflicts with affected owners.

## PR template

**Proposed title:** `feat(api): implement ORDO backend endpoints`

``` markdown
## Summary
- What changed and why?

## Requirements and contracts
- Requirement/decision references:
- Contract approvers:
- Compatibility impact:

## Implemented endpoints
- Method + path:
- Purpose:
- Authentication/authorization:

## Files changed
- API:
- Tests:
- Docs/config/deployment:

## Tests executed
- [ ] Unit/schema
- [ ] Route
- [ ] Contract/integration (identify external dependencies)
- [ ] Full required suite
- [ ] Formatting/lint/type/security
- Exact commands and actual outcomes:

## Security and privacy
- Access control:
- URL/SSRF/rate/size controls:
- Logging/retention:
- Security review status:

## Configuration and deployment
- Environment variables:
- Docker/CI/deployment implications:
- Rollback considerations:

## Limitations and outstanding dependencies
- Blocked contracts:
- Cross-team work:
- Unverified assumptions:

## Reviewer checklist
- [ ] Contract approved
- [ ] No secrets/private data committed
- [ ] Errors/logs safe
- [ ] Tests/docs match implementation
- [ ] Ownership boundaries respected
```

Remove non-applicable items but never mark an item complete without
evidence.

## Team handover

-   **Code Retrieval Engineer:** exact adapter interface, request/result
    schema, exceptions, timeouts, fixtures.
-   **ML Engineer:** inference input/output, model/version metadata,
    latency/failure expectations, approved fallback.
-   **Data Engineer:** canonical issue records, IDs/timestamps,
    ingestion state, private-repository scope.
-   **Web Engineer:** verified OpenAPI URL, safe request/response
    examples, paging/errors/auth.
-   **Security/Privacy Reviewer:** route inventory, auth tests, URL
    protections, logging, retention, open risks.
-   **Team Lead:** decisions, changed files, test evidence, deployment
    implications, blockers.
-   **QA Engineer:** deterministic fixtures, expected statuses,
    regression cases, external-test requirements.
-   **DevOps/MLOps Engineer:** health checks, env injection, container
    command/port, workers, logs, CI changes.

Separate completed, verified, approved-but-unimplemented, and blocked
work.

``` mermaid
flowchart TD
    A[Confirm base branch and clean tree] --> B[Create feature branch]
    B --> C[Scoped implementation]
    C --> D[Tests and static checks]
    D --> E[Review diff and staged files]
    E --> F[Commit and push]
    F --> G[Open PR with evidence]
    G --> H[Owner review and CI]
    H --> I{Approved and checks pass?}
    I -- No --> J[Address feedback and rerun]
    J --> D
    I -- Yes --> K[Merge under repo policy]
    K --> L[Handover and record remaining work]
```

# 29. Definition of Done

Mark assigned work complete only when all applicable items are
satisfied.

## Requirements and contracts

-   [ ] Requirements/acceptance criteria traceable.
-   [ ] Existing/new endpoints distinguished.
-   [ ] Request, response, error, pagination, and auth contracts
    approved.
-   [ ] Shared changes approved by affected owners.
-   [ ] Unknowns have an owner and next action.

## Implementation

-   [ ] App starts using documented command.
-   [ ] Routers/dependencies registered correctly.
-   [ ] Configuration validated and secrets externalized.
-   [ ] Schemas match approved contracts.
-   [ ] Routes do not duplicate domain logic.
-   [ ] Resources initialize/close correctly.
-   [ ] Readiness accurately reflects mandatory dependencies if
    required.
-   [ ] Required retrieval/ML/ingestion integrations work.
-   [ ] Known failures map safely.
-   [ ] Timeouts, request bounds, and concurrency addressed.

## Security/privacy

-   [ ] Auth/resource authorization implemented if required.
-   [ ] Private repository access enforced.
-   [ ] URL/filter protections appropriate.
-   [ ] Logs/errors avoid secrets/private content.
-   [ ] Security findings resolved or accepted by authorized owner.
-   [ ] Retention/privacy assumptions documented.

## Quality/docs

-   [ ] Relevant unit/schema/route/contract/integration tests pass.
-   [ ] Full required suite and CI checks pass.
-   [ ] Unit tests do not require live credentials by default.
-   [ ] OpenAPI matches behavior.
-   [ ] Performance claims measured.
-   [ ] Deployment compatibility verified if applicable.
-   [ ] Operational notes updated.

## Git/handover

-   [ ] Approved base and feature branch used.
-   [ ] Only intended files committed.
-   [ ] No secrets/generated indexes/model artifacts/unrelated changes.
-   [ ] PR accurately describes implementation and evidence.
-   [ ] Cross-team dependencies documented and communicated.
-   [ ] No mandatory endpoint, security requirement, contract, test, or
    approval remains unresolved.

**Completion rule:** If any mandatory endpoint, security requirement,
package contract, test, or approval is unresolved, report the work as
**blocked** or **partially complete**, name the owner, and state the
next action. A successful local startup is not production-readiness
evidence.

------------------------------------------------------------------------

## Appendix A --- Repository reconnaissance report

  --------------------------------------------------------------------------------------------
  Item                     Observed value    Evidence/command               Status/follow-up
  ------------------------ ----------------- ------------------------------ ------------------
  Repository root                            `pwd` / listing                

  Branch and worktree                        `git branch --show-current`,   
                                             `git status --short`           

  Approved base branch                       Team Lead/docs                 

  Python/package manager                     Manifest/CI                    

  FastAPI/Pydantic                           Manifest/active environment    
  versions                                                                  

  Entry point/routes                         Source/OpenAPI                 

  Shared schemas                             `shared/` or existing package  

  Retrieval/ML/ingestion                     Package source/tests           
  interfaces                                                                

  Authentication                             Source/config/docs             

  Test/lint/format tools                     Manifest/CI                    

  Docker/deployment                          Dockerfile/Compose/infra       

  CI workflows                               `.github/workflows/`           

  Missing decisions                          Decision log                   
  --------------------------------------------------------------------------------------------

## Appendix B --- Safe inspection commands

``` bash
git status --short
git branch --show-current
git branch -a
git log -5 --oneline
git remote -v
git ls-files
git diff --check
git diff --stat
```

PowerShell configuration-file discovery without printing secrets:

``` powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File -Include pyproject.toml,requirements.txt,uv.lock,poetry.lock,pytest.ini,ruff.toml,mypy.ini,Dockerfile,docker-compose.yml
```

macOS/Linux:

``` bash
find . -maxdepth 5 -type f \( -name 'pyproject.toml' -o -name 'requirements.txt' -o -name 'uv.lock' -o -name 'poetry.lock' -o -name 'pytest.ini' -o -name 'ruff.toml' -o -name 'mypy.ini' -o -name 'Dockerfile' -o -name 'docker-compose.yml' \) -print
```

## Appendix C --- Contract decision log

  ----------------------------------------------------------------------------------------
  ID          Question         Decision/rationale   Owner(s)      Date        Tests/docs
                                                                              affected
  ----------- ---------------- -------------------- ------------- ----------- ------------
  API-001     Search                                API +                     
              request/result                        Retrieval +               
              contract                              TL                        

  API-002     Private                               Security + TL             
              repository                                                      
              authorization                                                   

  API-003     Job lifecycle if                      API + Data +              
              async                                 TL                        

  API-004     Error envelope                        API + Web +               
                                                    TL                        

  API-005     Readiness                             API +                     
              dependencies                          DevOps + TL               

  API-006     Performance                           TL + product              
              objectives                            owner                     
  ----------------------------------------------------------------------------------------

## Appendix D --- Implementation status handover

-   **Completed and verified:**
-   **Approved but not implemented:**
-   **Blocked by contract/decision:**
-   **Tests (exact commands and results):**
-   **CI status:**
-   **Security review status:**
-   **Deployment verification:**
-   **Known limitations:**
-   **Owners and next actions:**

------------------------------------------------------------------------

**End of manual.** This is an implementation guide, not evidence that
the repository has been inspected or that example code, tests, CI
checks, or deployment have passed. Verify all proposed details against
the actual ORDO monorepo before implementation.
