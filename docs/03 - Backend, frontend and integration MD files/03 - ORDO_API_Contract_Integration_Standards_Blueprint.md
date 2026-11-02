# ORDO API Contract and Integration Standards Blueprint

**Project:** ORDO --- AI-Powered GitHub Issue Intelligence Platform\
**Artifact:** `ORDO_API_Contract_Integration_Standards_Blueprint.md`\
**Status:** Pre-repository design baseline\
**Prepared:** 27 October 2026\
**Audience:** Team Lead, Data Engineer, ML Engineer, Code Intelligence &
Retrieval Engineer, Backend Engineer, Frontend Engineer,
Security/Privacy Reviewer, DevOps/MLOps Engineer, QA Engineer

> **Evidence and status notice:** The ORDO repository has not yet been
> created. This document is therefore a pre-implementation contract
> proposal based on the available ORDO planning and role blueprints. It
> is not a repository audit. No routes, source-code interfaces,
> dependency versions, tests, OpenAPI documents, or Git state are
> claimed to exist or have been verified. All proposed contracts below
> require review and approval by the Team Lead and affected owners
> before implementation.

## Table of contents

1.  Executive Summary
2.  Project Context and Scope
3.  Repository Audit
4.  Integration Architecture
5.  Contract Inventory
6.  Shared Data Contracts
7.  Canonical Issue Representation
8.  API Request and Response Contracts
9.  Error Contract
10. Search and Retrieval Contract
11. ML Input and Output Contract
12. Pagination and Filtering
13. Serialization Standards
14. Versioning and Compatibility
15. OpenAPI and API Documentation
16. Contract Testing
17. Mocking and Independent Development
18. Integration Configuration
19. Security and Privacy
20. Contract Change Management
21. Troubleshooting Handbook
22. Implementation Plan
23. Git and Pull Request Workflow
24. Risks and Unresolved Questions
25. Definition of Done
26. Appendix A --- Proposed Schema Examples
27. Appendix B --- Contract Change Request Template
28. Appendix C --- Pull Request Handover Checklist

------------------------------------------------------------------------

## 1. Executive Summary

ORDO is planned as an AI-powered GitHub Issue Intelligence platform. The
intended product flow is to collect authorized GitHub issue data,
normalize it, produce issue intelligence, retrieve relevant evidence,
and present results through a user interface.

The purpose of this blueprint is to prevent each engineer from
independently inventing incompatible field names, identifier types,
response shapes, errors, and assumptions. It establishes a proposed
contract-first workflow before code is written.

### Decisions recommended for Team Lead approval

1.  Keep one approved monorepo. Do not create competing repositories for
    the API, UI, ingestion, ML, or retrieval modules.
2.  Keep the Streamlit frontend communicating with the backend over
    HTTP/JSON. The frontend must not access the database or import
    backend/package internals at runtime.
3.  Treat ingestion, ML, and retrieval as independently owned
    components. The API orchestrates their approved interfaces; it does
    not reimplement their algorithms.
4.  Use Pydantic request/response models at the FastAPI boundary if the
    planned FastAPI + Pydantic stack is approved.
5.  Distinguish raw GitHub records, normalized issue records, ML
    predictions, retrieval evidence, and public API response objects.
6.  Do not interpret a retrieval relevance score as a probability, proof
    of a fix, or contributor availability. Do not call an ML score a
    probability unless the model's documented output supports that
    interpretation.
7.  Adopt one safe error envelope for public API errors, subject to
    frontend and security approval.
8.  Require contract tests and an impact review whenever a shared schema
    changes.
9.  Mark all route names and schemas in this document as **proposed**,
    not existing or approved.
10. Complete the repository audit only after the Team Lead creates the
    repository and the engineering team has access.

### Status vocabulary

-   **Verified:** directly inspected in the actual repository or
    executed test.
-   **Proposed:** design suggestion awaiting approval.
-   **Approved:** accepted by the Team Lead and affected owners.
-   **Blocked:** cannot be finalized until an owner or product decision
    is supplied.
-   **Not applicable:** explicitly reviewed and excluded from the
    project scope.

No item is marked Verified in this pre-repository document.

## 2. Project Context and Scope

### 2.1 Planned component responsibilities

  -----------------------------------------------------------------------------
  Component               Expected responsibility       Contract responsibility
  ----------------------- ----------------------------- -----------------------
  Data ingestion          Collect authorized GitHub     Publish normalized
                          issue data, handle upstream   issue input shape,
                          pagination, normalize         source metadata, sync
                          records, and manage approved  outcomes, and ingestion
                          persistence/synchronization   errors

  ML engine               Issue classification,         Publish a stable Python
                          explainable priority scoring, input/output interface,
                          long-open risk, historical    method/version
                          resolution-time estimation,   metadata, warnings, and
                          and validated prediction      failure semantics
                          output where approved         

  Code retrieval          Indexing,                     Publish retrieval
                          lexical/vector/hybrid search, request/result
                          ranking, related issue/code   structures, stable
                          evidence, and provenance      evidence identifiers,
                                                        score semantics, and
                                                        timeout/index errors

  FastAPI backend         Public HTTP API, validation,  Own public HTTP
                          orchestration, authorization  contracts and adapt
                          integration, serialization,   package contracts
                          and API-level errors          without leaking
                                                        internal
                                                        representations

  Streamlit frontend      Display API results, forms,   Consume documented HTTP
                          filters, errors, and          responses; never assume
                          progress/status states        undocumented fields

  Shared contracts        Common schemas only where     Changes require Team
                          multiple Python components    Lead and affected-owner
                          genuinely share a type        approval

  QA/testing              Unit, contract, API,          Maintain deterministic
                          integration, consumer, and    fixtures and report
                          compatibility testing         actual test results

  Security/privacy        Threat review, access-control Approve sensitive
                          requirements, data handling,  boundary decisions and
                          logging and retention review  test expectations

  DevOps/MLOps            Runtime configuration, CI/CD, Coordinate environment
                          packaging and deployment      and release contract
                                                        checks
  -----------------------------------------------------------------------------

This table describes planned ownership, not confirmed filesystem
permissions. Folder ownership alone does not enforce Git access control.

### 2.2 Scope exclusions unless approved

Do not automatically add a new schema registry, message broker,
microservice boundary, database, API version prefix, or additional ML
capability. Choose infrastructure only when product requirements and the
approved repository justify it.

## 3. Repository Audit

### 3.1 Current state

**Repository status:** Not created, according to the project owner.\
**Git status / branch / remotes:** Not available.\
**Source files, dependency manifests, tests, routers, and OpenAPI
schema:** Not available for inspection.\
**Observed contract mismatches:** None can be confirmed without
implementation evidence.\
**Tests executed for this blueprint:** None.\
**OpenAPI generated or validated:** No.

Do not fill these fields with guesses. Update them after the repository
exists.

### 3.2 First audit checklist

From the actual monorepo root, record:

``` bash
git status
git branch --show-current
git branch -a
git log -5 --oneline
git remote -v
```

Inspect the structure.

PowerShell:

``` powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\.git\\|\\.venv\\|\\__pycache__\\' } |
  Select-Object -ExpandProperty FullName
```

Then inspect, where present:

-   `README.md`, `pyproject.toml`, requirements/lock files and
    `.python-version`
-   `apps/api/`, `apps/web/`, `packages/data_ingestion/`,
    `packages/ml_engine/`, `packages/code_retrieval/`, `shared/`,
    `tests/`
-   Existing Pydantic models, FastAPI routers, exception handlers,
    settings and API clients
-   Ingestion output schema and identifier/timestamp behavior
-   ML predictor's real callable interface and serialized output
-   Retrieval API, result IDs, ranking semantics, provenance, and
    empty-index behavior
-   Existing authentication, authorization, CORS, request limits and
    logging
-   CI workflows, formatter/linter/type-check/test commands and branch
    policy

The directory names above are planning references. If the repository
differs, preserve the actual structure and ask the Team Lead before
restructuring it.

### 3.3 Audit evidence register

  -------------------------------------------------------------------------
  Audit item              Evidence to capture       Current status
  ----------------------- ------------------------- -----------------------
  Python version          `.python-version`,        Blocked --- repo absent
                          project metadata, CI      
                          runtime                   

  FastAPI/Pydantic        lock file or resolved     Blocked
  versions                environment               

  Public routes           router source and         Blocked
                          generated OpenAPI         

  Shared issue schema     source model and tests    Blocked

  Ingestion interface     public function/class and Blocked
                          output fixture            

  ML interface            predictor signature and   Blocked
                          output model              

  Retrieval interface     search signature and      Blocked
                          result model              

  UI expectations         API client and rendering  Blocked
                          code                      

  Error format            exception handlers and UI Blocked
                          parser                    

  Authentication          middleware/dependencies   Blocked
                          and tests                 

  CI contract checks      workflow files and actual Blocked
                          run                       

  Git baseline            command outputs above     Blocked
  -------------------------------------------------------------------------

## 4. Integration Architecture

### 4.1 Proposed logical flow

``` mermaid
flowchart TD
    GH[GitHub API / authorized repositories] --> ING[Data ingestion and normalization]
    ING --> STORE[(Approved persistence layer)]
    STORE --> API[FastAPI orchestration layer]
    API --> ML[ML engine: predictions]
    API --> RET[Code retrieval: evidence and candidates]
    API --> STORE
    API <-->|HTTP / JSON| WEB[Streamlit frontend]
    QA[Contract and integration tests] -. validates .-> ING
    QA -. validates .-> ML
    QA -. validates .-> RET
    QA -. validates .-> API
    QA -. validates .-> WEB
```

**Status:** Proposed architecture, not a verified runtime graph. The
exact persistence model and whether ingestion writes to a database,
files, or another store must be confirmed. ML and retrieval may be
invoked as Python interfaces rather than separate network services; do
not create HTTP calls between packages without a deployment requirement.

### 4.2 Boundary register

  -------------------------------------------------------------------------------------------------------
  Boundary       Producer →        Proposed      Contract required        Error/timeout     Owner(s)
                 Consumer          mechanism                              policy            
  -------------- ----------------- ------------- ------------------------ ----------------- -------------
  GitHub →       GitHub API →      HTTPS REST    Upstream payload/page    Handle rate       Data Engineer
  ingestion      ingestion                       metadata                 limits,           
                                                                          pagination,       
                                                                          network errors;   
                                                                          bounded retries   

  Ingestion →    ingestion →       Python        Canonical issue record + Validation errors Data
  normalized     approved          interface     source metadata          distinct from     Engineer;
  record/store   storage/API       and/or                                 storage failures  Team Lead for
                                   persistence                                              shared schema
                                   adapter                                                  

  Normalized     ingestion/store → Python call   Normalized issue input → Validate          Data + ML
  issue → ML     ML engine         initially,    prediction result        input/output;     Engineers
                                   unless                                 controlled        
                                   deployment                             fallback only if  
                                   needs                                  approved          
                                   otherwise                                                

  Query →        API/service →     Python call   Search request →         Index             Retrieval +
  retrieval      retrieval         initially,    evidence candidates      unavailable,      API Engineers
                                   unless                                 invalid query,    
                                   deployment                             timeout, partial  
                                   needs                                  result semantics  
                                   otherwise                                                

  API →          FastAPI → UI      HTTP/JSON     Public                   Timeouts, safe    API +
  Streamlit                                      request/response/error   error parsing,    Frontend
                                                 schemas                  bounded retry     Engineers
                                                                          only for          
                                                                          safe/idempotent   
                                                                          operations        

  Shared         shared package →  Python import Versioned model          Avoid circular    Team Lead +
  contract →     Python consumers                definitions              imports;          affected
  consumers                                                               coordinated       owners
                                                                          changes           

  CI → release   tests/workflows → CI commands   Test and schema          Failing checks    QA + DevOps +
  gate           PR                              validation outcomes      block merge per   owners
                                                                          approved policy   
  -------------------------------------------------------------------------------------------------------

### 4.3 Architectural invariants proposed for approval

-   Streamlit calls the public API; it does not read SQLite or import
    internal package modules.
-   API routers validate transport-level input and delegate business
    logic to services/adapters.
-   Ingestion owns source acquisition and normalization; ML owns
    prediction algorithms; retrieval owns indexing/ranking/evidence.
-   Internal component schemas may differ from public API schemas. The
    API performs explicit mapping.
-   Private issue bodies, access tokens, full prompts, and raw upstream
    responses must not be written to ordinary logs.
-   A missing optional ML or retrieval result must have documented
    behavior; never fabricate a result to satisfy the UI.

## 5. Contract Inventory

The following inventory is a **proposal register**. It is not an
inventory of existing code.

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  Contract   Producer     Consumer          Interface type       Input schema        Output schema      Error behavior       Owner         Status
  ID                                                                                                                                       
  ---------- ------------ ----------------- -------------------- ------------------- ------------------ -------------------- ------------- --------------
  C-01       GitHub API   Ingestion         External HTTPS API   Upstream GitHub     Upstream payload + Rate limit, auth,    Data Engineer Proposed;
                                                                 issue/page schema   paging metadata    network, malformed                 inspect
                                                                                                        response                           upstream use

  C-02       Ingestion    Normalized        Python/persistence   Raw issue + source  Canonical          Validation and       Data Engineer Proposed;
                          store/consumers                        context             normalized issue   persistence errors                 owner
                                                                                                        separated                          confirmation

  C-03       Normalized   ML engine         Python               Canonical issue     Prediction         Input/model/output   ML Engineer   Proposed;
             issue                                               input               result +           validation errors                  owner
             producer                                                                warnings/version                                      confirmation

  C-04       Querying     Retrieval package Python               Retrieval request   Evidence           Invalid query, empty Retrieval     Proposed;
             service                                                                 candidates +       index, timeout       Engineer      owner
                                                                                     provenance                                            confirmation

  C-05       API service  Streamlit         HTTP/JSON            Public API request  Public response    Stable API error     API Engineer  Proposed
                                                                 models              models             envelope                           

  C-06       API service  Data package      Python or repository Repository/issue    Defined            Typed package        Data + API    Blocked
                                            adapter              lookup or sync      result/job/issue   exceptions           Engineers     pending actual
                                                                 command             object                                                design

  C-07       API service  ML package        Python               Canonical issue or  Publicly mappable  Typed model          ML + API      Proposed
                                                                 approved feature    prediction result  exceptions           Engineers     
                                                                 view                                                                      

  C-08       API service  Retrieval package Python               Search request      Evidence candidate Typed retrieval      Retrieval +   Proposed
                                                                                     list               exceptions           API Engineers 

  C-09       Streamlit    API               HTTP/JSON consumer   Query/filter/page   Renderable         Network/HTTP/JSON    Frontend +    Proposed
             client                         contract             parameters          response or error  errors handled       API Engineers 
                                                                                                        separately                         

  C-10       CI           All changed       Test/schema          Code, fixtures,     Pass/fail evidence Fail merge gate      QA + DevOps   Proposed
                          components        validation           OpenAPI schema                         according to policy                
  -------------------------------------------------------------------------------------------------------------------------------------------------------

### 5.1 Gap analysis before code exists

  -----------------------------------------------------------------------
  Topic                   Proposed rule           Must be confirmed by
  ----------------------- ----------------------- -----------------------
  Canonical issue         Preserve upstream       Data Engineer + Team
  identifier              GitHub numeric ID as    Lead
                          integer internally;     
                          keep repository         
                          identity and issue      
                          number as distinct      
                          fields                  

  Repository identity     Use an unambiguous      Data Engineer
                          repository identifier;  
                          `owner/name` may be a   
                          display/lookup value    
                          but must not replace    
                          numeric IDs where IDs   
                          are required            

  Timestamps              ISO 8601 with timezone, Data Engineer + API
                          normalized to UTC       Engineer
                          internally              

  Nullable fields         Distinguish absent,     All producers/consumers
                          null and empty values   
                          intentionally           

  ML score semantics      Document method, range, ML Engineer
                          meaning and             
                          limitations; no         
                          probability claim       
                          without evidence        

  Retrieval scores        Document ranking method Retrieval Engineer
                          and scale; no           
                          probability or          
                          proof-of-fix            
                          interpretation          

  Error body              One public error        API + Security +
                          envelope; framework     Frontend
                          validation details      
                          mapped safely           

  Pagination              API pagination and      API + Data Engineers
                          GitHub upstream         
                          pagination remain       
                          separate                

  Authentication          Must be decided before  Team Lead + Security
                          any private repository  Reviewer
                          data is exposed         

  API version prefix      Do not add until team   Team Lead
                          chooses versioning      
                          strategy                

  Database fields         Use only fields         Data Engineer + Team
                          required by approved    Lead
                          requirements            
  -----------------------------------------------------------------------

## 6. Shared Data Contracts

### 6.1 Recommended representation

If FastAPI and Pydantic 2.x are confirmed in the created repository, use
Pydantic models at the HTTP boundary and a clearly owned normalized
internal model. Share Python model definitions only when multiple Python
packages need the same semantic type. The Streamlit client should
consume the HTTP schema, not import backend model classes.

Do not build a shared package simply because it appears in a reference
tree. First identify the actual imports and ownership boundary.

### 6.2 Proposed model families

-   `NormalizedIssue`: source identity, repository identity, issue
    number, title/body, state, labels, author/source metadata and
    timestamps that are actually needed.
-   `PredictionResult`: prediction task, output value, method/model
    version, rationale/evidence fields if produced, and
    warnings/uncertainty metadata.
-   `EvidenceItem`: stable source reference, kind, URI/path/line
    metadata when available, snippet only if safe and approved, ranking
    score with documented semantics.
-   `SearchRequest` and `SearchResponse`: query, supported
    scope/filters, bounded pagination and result metadata.
-   `ApiError`: stable machine-readable code, safe message, request ID
    if implemented, and safe optional details.
-   `PageMetadata`: only if the API actually uses page/size pagination
    and needs total/next-page metadata.

These names are proposals. The Team Lead should approve the
shared-schema location after checking the actual monorepo and ownership
plan.

### 6.3 Model design rules

1.  Validate external input at the boundary.
2.  Avoid duplicate definitions of the same semantic entity in multiple
    packages.
3.  Do not include every upstream GitHub field by default.
4.  Keep raw upstream payloads separate from normalized fields and
    derived predictions.
5.  Keep model-specific tensors, embeddings, and internal feature arrays
    out of public responses unless explicitly required.
6.  Make serialized values JSON-compatible.
7.  Define whether unknown fields are ignored, rejected, or preserved at
    each boundary; do not rely on accidental defaults.
8.  Add a contract test for every agreed required/nullable field.

## 7. Canonical Issue Representation

### 7.1 Proposed field table

  ------------------------------------------------------------------------------------------------------------
  Field                    Proposed type           Required?      Nullable? Source         Validation /
                                                                                           consumers
  ------------------------ ---------------- ---------------- -------------- -------------- -------------------
  `source`                 string/enum                   Yes             No Ingestion      Approved source
                                                                                           name, e.g. GitHub

  `github_issue_id`        integer            Yes for GitHub             No Upstream issue Preserve as
                                                      source                ID             integer; Data, ML,
                                                                                           API

  `repository_id`          integer or       Yes after source             No Upstream       Type must be
                           stable string              review                repository ID  settled before
                                                                                           implementation

  `repository_full_name`   string                    Yes for             No `owner/name`   Validate non-empty;
                                              display/lookup                               case rules to be
                                                                                           documented

  `issue_number`           positive integer              Yes             No Upstream issue Scoped to
                                                                            number         repository; do not
                                                                                           confuse with global
                                                                                           issue ID

  `title`                  string                        Yes             No Upstream issue Trim/length-limit
                                                                                           policy required

  `body`                   string                   Optional            Yes Upstream issue May be absent/null;
                                                                                           never log by
                                                                                           default

  `state`                  string/enum                   Yes             No Upstream issue Map supported
                                                                                           upstream states;
                                                                                           unknown values
                                                                                           handled explicitly

  `labels`                 list of strings      Yes, default             No Upstream issue Normalize label
                                                  empty list                               names; unknown
                                                                                           labels retained
                                                                                           unless policy says
                                                                                           otherwise

  `author_login`           string                   Optional            Yes Upstream issue Treat as external
                                                                                           metadata, not
                                                                                           verified identity

  `created_at`             timezone-aware                Yes             No Upstream issue Parse ISO 8601;
                           datetime                                                        normalize UTC
                                                                                           internally

  `updated_at`             timezone-aware           Yes when       Possibly Upstream issue Reject malformed
                           datetime                 provided                               timestamps or
                                                    upstream                               record a typed
                                                                                           data-quality issue

  `html_url`               URL string               Optional            Yes Upstream issue Validate
                                                                                           scheme/host; avoid
                                                                                           using untrusted URL
                                                                                           for server-side
                                                                                           fetches

  `closed_at`              timezone-aware           Optional            Yes Upstream issue Null for open
                           datetime                                                        issues; not a proxy
                                                                                           for resolution
                                                                                           quality

  `derived_features`       separate typed                 No            Yes Feature        Include only
                           object                                           pipeline       approved,
                                                                                           documented features
  ------------------------------------------------------------------------------------------------------------

This table is a starting proposal, not an approved schema. Data Engineer
must reconcile it with the actual ingestion output and the Team Lead
must resolve identifier type decisions before consumers implement
against it.

### 7.2 Data normalization behavior

-   Preserve the original source identifier and source URL when
    approved.
-   Do not silently convert an identifier from string to integer or vice
    versa across a public boundary.
-   Normalize timestamps to timezone-aware UTC values internally.
    Serialize API timestamps as ISO 8601 with `Z` or explicit UTC
    offset.
-   Missing `body` is not the same as an empty body unless the approved
    model explicitly normalizes both to `""`.
-   Empty labels should be `[]`, not `null`, when the contract says the
    field is a list.
-   Unknown upstream states or labels should produce a documented
    mapping/data-quality behavior, not a silent incorrect
    classification.
-   Store derived predictions separately from raw issue fields so that
    re-running a model does not rewrite source truth.
-   Never place unapproved real private issue content in fixtures.

## 8. API Request and Response Contracts

### 8.1 Proposed public endpoint candidates

No endpoint below is verified or approved. The Team Lead must choose
product scope before implementation.

  -----------------------------------------------------------------------------------------------------------------------------------
  Method + path (proposed)                           Purpose                 Request        Response          Status/error
                                                                                                              considerations
  -------------------------------------------------- ----------------------- -------------- ----------------- -----------------------
  `GET /health`                                      Process liveness        None           Minimal status    `200` when process is
                                                                                            object            alive; do not use as
                                                                                                              proof all dependencies
                                                                                                              are ready

  `GET /ready`                                       Optional dependency     None           Readiness status  Only add if
                                                     readiness                              per approved      deployment/operations
                                                                                            policy            need it; avoid exposing
                                                                                                              sensitive dependency
                                                                                                              details

  `GET /api/v1/repositories`                         List                    Bounded        Repository page   Auth and repository
                                                     configured/authorized   page/filter                      authorization must be
                                                     repositories            parameters                       defined

  `POST /api/v1/repositories/{repository_id}/sync`   Request ingestion/sync  Approved sync  Job/status object Decide async vs sync
                                                                             options        or synchronous    before coding; protect
                                                                                            result            against repeated
                                                                                                              expensive requests

  `GET /api/v1/issues`                               Search/list normalized  Repository     Issue page        Enforce authorization
                                                     issues                  scope,                           and bounded page size
                                                                             filters,                         
                                                                             pagination                       

  `GET /api/v1/issues/{issue_id}`                    Retrieve issue details  Stable issue   Issue detail      Define global ID vs
                                                                             identifier                       repository + issue
                                                                                                              number

  `POST /api/v1/search`                              Retrieve related        Search request Evidence/search   Timeout, empty index,
                                                     issues/code evidence                   response          partial failure
                                                                                                              behavior

  `GET /api/v1/jobs/{job_id}`                        Optional sync/analysis  Job identifier Job status        Add only if async jobs
                                                     job status                                               are selected
  -----------------------------------------------------------------------------------------------------------------------------------

Do not implement all candidates automatically. The route list must be
aligned with the product requirements and approved by the Team Lead.

### 8.2 Public API principles

-   Use explicit request and response models.
-   Document successful and error status codes.
-   Define authentication and authorization per route before private
    data is exposed.
-   Use HTTP status codes consistently; do not return `200` for failed
    operations.
-   Use bounded timeouts and resource limits.
-   Do not expose internal filesystem paths, raw model objects, private
    code, access tokens, stack traces, or raw upstream error bodies.
-   Keep public response models stable even when internal packages
    change.
-   Do not promise a synchronous result for ingestion or retrieval work
    until latency and resource constraints are measured.

### 8.3 Proposed search request example

This example is provisional. `repository_ids`, filters and pagination
semantics need owner approval.

``` json
{
  "query": "login fails after password reset",
  "repository_ids": [12345],
  "filters": {
    "state": ["open", "closed"],
    "labels": ["bug"]
  },
  "page": 1,
  "page_size": 10
}
```

### 8.4 Proposed search response example

``` json
{
  "items": [
    {
      "result_id": "example-result-1",
      "kind": "issue",
      "title": "Password reset redirects incorrectly",
      "source_url": "https://github.com/example/project/issues/42",
      "score": 0.73,
      "score_method": "hybrid_rank_v1",
      "evidence": []
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": null
}
```

The score `0.73` is illustrative only. Do not ship a numeric score until
the Retrieval Engineer defines its range, ranking meaning, normalization
and comparability. `total: null` is only acceptable if the approved
pagination contract explicitly permits unknown totals; otherwise omit it
or return a known total consistently.

## 9. Error Contract

### 9.1 Proposed public error envelope

``` json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request is invalid.",
    "request_id": "example-request-id",
    "details": {}
  }
}
```

This is a proposed public format. FastAPI's default validation error
body must not be assumed to match it. The API Engineer must implement
and test an approved mapping.

### 9.2 Proposed status mapping

  ------------------------------------------------------------------------
  HTTP status             Meaning                  Retry?
  ----------------------- ------------------------ -----------------------
  `400`                   Malformed request or     No, until corrected
                          invalid query semantics  

  `401`                   Missing/invalid          No, until credentials
                          authentication, if auth  are corrected
                          is enabled               

  `403`                   Authenticated caller     No
                          lacks permission         

  `404`                   Resource not found or    No
                          deliberately concealed   
                          by security policy       

  `409`                   Conflicting state or     Depends on documented
                          duplicate/incompatible   operation
                          operation                

  `422`                   Request schema           No, until corrected
                          validation failure, if   
                          this mapping is adopted  

  `429`                   Rate limit               Retry only after the
                                                   documented delay

  `502`                   Upstream dependency      Sometimes, bounded
                          returned an              retry for safe
                          invalid/failing response operations

  `503`                   Required dependency      Sometimes, bounded
                          temporarily unavailable  retry

  `504`                   Dependency or operation  Depends on idempotency
                          timeout                  and operation status

  `500`                   Unexpected internal      Retry only when safe
                          failure                  and policy permits
  ------------------------------------------------------------------------

Avoid exposing stack traces and raw upstream response bodies. The exact
use of `400` versus `422` and whether `request_id` exists must be made
consistent across API handlers and the UI client.

### 9.3 Logging policy

-   Log one structured failure at the layer that owns the actionable
    error; avoid logging the same exception repeatedly at every layer.
-   Include request/correlation IDs only if middleware and propagation
    are implemented.
-   Never log tokens, full private issue bodies, secrets, or unapproved
    source snippets.
-   Keep diagnostic details safe and bounded.
-   Record retryability in internal exception semantics or documented
    status behavior, not by making the UI parse English error messages.

### 9.4 Frontend error handling

The Streamlit client should distinguish: 1. Connection failure / timeout
(no valid HTTP response). 2. Non-success HTTP status with valid error
JSON. 3. Non-success response with malformed or unexpected JSON. 4.
Successful status with an invalid response shape. 5. A valid response
with an empty `items` list.

Each state needs a safe user-facing message. Do not display stack traces
or raw exception dumps to end users.

## 10. Search and Retrieval Contract

### 10.1 Proposed request fields

-   `query`: required non-empty text, with an approved maximum length.
-   `repository_ids` or repository scope: optional only if
    cross-repository search is authorized and supported.
-   `filters`: only filters the retrieval engine actually implements.
-   `page` / `page_size` or cursor: choose one based on the retrieval
    engine and API workload.
-   `include_evidence`: include only if evidence is optional and the
    performance/privacy impact is understood.

### 10.2 Proposed result fields

-   Stable `result_id`
-   `kind` (for example, issue, code file, pull request) only for
    supported result types
-   Source/repository identity
-   Display title
-   Link or path where valid
-   Line range only when supported by actual indexed evidence
-   Score and `score_method` with documented semantics
-   Evidence/provenance metadata
-   Optional warnings for partial results

Do not fabricate source URLs, paths, commit SHAs, line ranges, pull
requests, fixes or contributor availability. Evidence must trace to
indexed/source data.

### 10.3 Required edge-case semantics

Retrieval owner must define: - Empty query behavior. - Empty index /
index not yet built. - No results. - Invalid filter. - Unsupported
repository scope. - Index version mismatch. - Timeout. - Partial results
if one retrieval backend fails. - Deduplication and stable ordering. -
Whether scores can be compared between queries or model/index versions.

The retrieval score must not be called a duplicate probability or proof
of a fix unless an independently validated, explicitly defined model
establishes that interpretation.

## 11. ML Input and Output Contract

### 11.1 Proposed interface boundary

The ML Engineer should expose a stable Python interface for normalized
issue input and validated prediction output. Exact function/class names
must be confirmed by the ML owner; `Predictor.predict(issue)` is a
candidate name, not an existing symbol.

### 11.2 Proposed output content

For each implemented prediction task, return only supported values and
metadata, such as: - Task name and prediction value. - Method/model
identifier or version where available. - Rationale or feature
explanation if the method can provide it. - Warnings or uncertainty
state. - Training/evaluation provenance in model documentation, not
necessarily every public response.

Do not require every possible task (classification, priority, long-open
risk, resolution-time estimate) if the Team Lead has not approved all of
them.

### 11.3 ML contract rules

-   Separate internal model outputs from public API response objects.
-   Do not label a score as probability/confidence unless its semantics
    are validated and documented.
-   Define behavior for missing title/body, unknown labels, empty input,
    model loading failure and unexpected model output.
-   Document the minimum data requirements and any fallback behavior.
-   Keep inference local/offline where the approved design requires it;
    do not add external API calls without review.
-   Record model/version changes that alter output meaning and
    coordinate with API/UI consumers.
-   The API owner decides how typed ML errors map to HTTP responses; the
    ML package must not independently dictate public HTTP status codes.

## 12. Pagination and Filtering

Do not force one pagination mechanism on every interface.

  -----------------------------------------------------------------------
  Interface                           Proposed pagination
  ----------------------------------- -----------------------------------
  GitHub ingestion                    Follow upstream API pagination
                                      semantics and rate limits

  Public issue listing                Page/size or cursor, selected after
                                      expected dataset size and sorting
                                      needs are understood

  Retrieval engine                    Use the method supported
                                      efficiently by the underlying index

  Internal ML batch processing        Bounded batches; not public API
                                      pagination

  Long-running sync/analysis          Consider a job resource only if
                                      async work is approved
  -----------------------------------------------------------------------

For every paginated public endpoint, define: - Default and maximum page
size. - Whether total count is known, omitted, or nullable. - Empty page
behavior. - Stable ordering and tie-breaker. - Interaction between
filters, sorting and paging. - Invalid page/size behavior. - Whether
page numbers start at 1 or offsets start at 0. - Whether concurrent data
changes can shift results.

Do not fetch all upstream pages into memory by default. Bound page
counts, response sizes and retries. Public API pagination and GitHub
ingestion pagination are separate contracts.

## 13. Serialization Standards

### 13.1 Proposed conventions

-   **Identifiers:** preserve source types. Distinguish upstream global
    issue ID, repository ID and repository-local issue number.
-   **Timestamps:** timezone-aware values internally; ISO 8601 with UTC
    marker/offset over HTTP.
-   **Enums:** stable string values; additions can still break
    exhaustive consumers, so notify owners.
-   **Nullability:** required-but-nullable is different from
    optional/omitted. Specify each field explicitly.
-   **Lists:** use `[]` for known empty collections; do not alternate
    between `null` and `[]`.
-   **Numbers:** document units, bounds and score semantics; reject
    non-finite values in JSON outputs.
-   **Unicode:** preserve Unicode text; do not assume issue bodies are
    ASCII.
-   **Unknown fields:** define policy for each boundary. Do not rely on
    implicit Pydantic defaults without tests.
-   **URLs:** validate and treat as untrusted. Server-side fetches
    require SSRF protections.
-   **JSON:** only JSON-compatible public values; no Python objects,
    tensors, NaN/Infinity or raw exception objects.

### 13.2 Timestamp examples

Accept and normalize valid timezone-aware ISO 8601 timestamps, such as:

``` text
2026-10-27T04:15:30Z
2026-10-27T09:45:30+05:30
```

These examples represent the same instant. Do not interpret naive
timestamps as UTC without an explicit source-specific rule.

### 13.3 Compatibility-sensitive examples

-   Renaming `repository_id` to `repo_id` is a breaking change.
-   Changing an ID from integer to string may break equality, database
    lookups and frontend assumptions.
-   Changing `evidence: []` to `evidence: null` can break renderers.
-   Adding a new enum value can break clients that assume a closed set.
-   Replacing a numeric ranking score with a normalized score requires
    explicit semantic/version documentation.

## 14. Versioning and Compatibility

### 14.1 Initial policy proposal

For a new project, agree on the public API path strategy before
implementation. A path prefix such as `/api/v1` is a proposal seen in
some route candidates above, not an approved requirement. Do not mix
prefixed and unprefixed routes accidentally.

For Python package interfaces, use coordinated changes and
release/version rules appropriate to the actual packaging model. A new
schema registry is not required by default.

### 14.2 Change classification

  -------------------------------------------------------------------------------
  Change            Risk              Required checks         Approval
  ----------------- ----------------- ----------------------- -------------------
  Add optional      Usually low, but  Producer, API schema    API owner +
  response field    check strict      and consumer tests      affected consumers
                    clients                                   

  Add required      Breaking          Migration and           Team Lead +
  request field                       compatibility tests     producer/consumer
                                                              owners

  Rename/remove     Breaking          Consumer search,        Team Lead + all
  field                               migration plan, tests   affected owners

  Change identifier High              Database, equality,     Data + API + UI +
  type                                serialization, API/UI   Team Lead
                                      tests                   

  Change            Medium/high       Schema and consumer     Producer + consumer
  null/omission                       rendering tests         owners
  behavior                                                    

  Add enum value    Medium            Unknown-value behavior  Owning component +
                                      and client tests        consumers

  Change score      High              Evaluation, docs, UI    ML/Retrieval
  semantics                           labels, version         owner + API/UI
                                      metadata                owners

  Change error      High              All frontend/error      API + Frontend +
  envelope                            consumer tests          Security

  Change pagination High              API,                    API + relevant
  semantics                           ingestion/retrieval, UI package owners
                                      tests                   

  Add/remove        Medium/high       OpenAPI diff, auth      Team Lead + API +
  endpoint                            review,                 consumers
                                      migration/deprecation   
                                      plan                    

  Change internal   Depends on        Package consumer tests  Package owner +
  Python signature  callers           and import scan         consumers
  -------------------------------------------------------------------------------

### 14.3 Deprecation process

1.  Record the problem, affected consumers and replacement.
2.  Obtain approval before changing the contract.
3.  Add the new behavior without removing the old one when feasible.
4.  Document migration steps and a removal date/criteria.
5.  Notify consumers and update tests/examples.
6.  Measure/confirm that supported consumers have migrated.
7.  Remove the deprecated behavior only after approval.
8.  Include rollback instructions in the PR.

Because the repository does not yet exist, no current versioning or
deprecation policy can be reported as established.

## 15. OpenAPI and API Documentation

After FastAPI is implemented, inspect its actual application entry point
and OpenAPI settings. If the app exposes standard FastAPI docs, common
local URLs are `/docs`, `/redoc`, and `/openapi.json`; verify them
against the configured application rather than assuming they exist.

Example commands after the app entry point is known:

``` bash
# Run from the repository root after replacing the module path
# with the actual approved FastAPI application import.
python -m uvicorn <actual_module>:app --reload
```

When an application entry point is confirmed, export the schema using
the actual module:

``` bash
python -c "import json; from <actual_module> import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json
```

The placeholder `<actual_module>` must be replaced; this command has not
been run. Do not commit an OpenAPI snapshot unless the team agrees to
maintain it.

Validation policy: - Every public route must declare request/response
models where applicable. - Review generated OpenAPI for status codes,
authentication, optional fields and descriptions. - Validate example
payloads against the implemented schema. - Compare OpenAPI changes in PR
review when public contracts change. - Record exact command and result;
do not mark validation passed without execution.

## 16. Contract Testing

### 16.1 Test layers

1.  **Model/unit tests:** required fields, nullability, invalid types,
    timestamps, serialization.
2.  **Component contract tests:** ingestion output, ML output, retrieval
    results conform to their agreed interfaces.
3.  **API tests:** status codes, request validation, response shape and
    error envelope.
4.  **Consumer tests:** Streamlit handles success, empty results,
    malformed JSON, HTTP errors and network failures.
5.  **Integration tests:** approved data flow across actual package
    boundaries.
6.  **Compatibility tests:** approved old/new examples remain valid
    during migration.
7.  **Security tests:** unauthorized access, oversized input, unsafe
    URLs and sensitive error/log behavior as applicable.

### 16.2 Proposed initial test layout

Adapt to the repository's actual structure:

``` text
tests/
  contracts/
    test_issue_contract.py
    test_search_contract.py
    test_error_contract.py
  integration/
    test_issue_to_api_flow.py
    test_search_to_ui_contract.py
```

Package owners should also maintain tests inside their owned packages if
that is the agreed layout. Do not create duplicate test files solely to
match this example.

### 16.3 Proposed schema tests

The following example uses Pydantic 2.x and is only suitable if the
repository confirms Pydantic 2.x. It illustrates the intended validation
behavior, not an already-existing model.

``` python
# Example only: tests/contracts/test_issue_contract.py
from datetime import datetime, timezone

import pytest
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ProposedIssueContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    github_issue_id: int = Field(gt=0)
    repository_full_name: str = Field(min_length=1)
    issue_number: int = Field(gt=0)
    title: str = Field(min_length=1)
    body: str | None = None
    labels: list[str] = Field(default_factory=list)
    created_at: datetime


def test_valid_issue_serializes_with_timezone():
    issue = ProposedIssueContract(
        github_issue_id=101,
        repository_full_name="example/project",
        issue_number=7,
        title="Example issue",
        body=None,
        labels=[],
        created_at=datetime(2026, 10, 27, tzinfo=timezone.utc),
    )
    data = issue.model_dump(mode="json")
    assert data["github_issue_id"] == 101
    assert data["body"] is None
    assert data["labels"] == []
    assert data["created_at"].endswith("Z")


def test_invalid_identifier_is_rejected():
    with pytest.raises(ValidationError):
        ProposedIssueContract(
            github_issue_id=0,
            repository_full_name="example/project",
            issue_number=7,
            title="Example issue",
            created_at=datetime(2026, 10, 27, tzinfo=timezone.utc),
        )


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        ProposedIssueContract(
            github_issue_id=101,
            repository_full_name="example/project",
            issue_number=7,
            title="Example issue",
            created_at=datetime(2026, 10, 27, tzinfo=timezone.utc),
            surprise="not in the contract",
        )
```

Expected outcome after dependencies and the test file are installed in
the real repository: all three tests pass. They have not been executed.
`model_dump(mode="json")` and the expected UTC `Z` serialization must be
checked against the selected Pydantic version and serializer
configuration.

### 16.4 API test acceptance

Use the repository's existing test runner and FastAPI testing pattern.
For each implemented endpoint, test: - Valid request and expected
success status. - Missing required fields and invalid types. - Unknown
IDs and unauthorized access. - Empty result sets. - Upstream timeout or
unavailable dependency. - Error response envelope and safe details. -
Response model serialization. - Pagination bounds and deterministic
ordering.

Mocks are useful for unit tests, but critical cross-component
integration must also be tested with real package implementations or
controlled local fakes that conform to the approved contract.

## 17. Mocking and Independent Development

-   Unit mocks test a small component in isolation.
-   Fake implementations provide deterministic behavior for consumers
    while a dependency is still being built.
-   Fixtures should be minimal, synthetic, stable and free of secrets.
-   Local stub servers are appropriate when an HTTP consumer needs a
    dependency before the real service is available.
-   Recorded fixtures must be sanitized and approved for use.
-   Test containers are optional; introduce them only if infrastructure
    and CI support them.
-   Every fake must be based on an approved schema and should fail
    clearly when a required field is missing.
-   Do not let the mock become the only definition of the contract; the
    approved schema and contract tests are authoritative.
-   Mark tests requiring GitHub credentials, private repositories, model
    artifacts, or an index so that offline tests can run separately.

## 18. Integration Configuration

### 18.1 Decisions required after repository creation

Confirm: - Supported Python version from project metadata and CI. -
Package manager and lockfile policy. - Actual FastAPI/Pydantic
versions. - Shared package import convention. - API base URL and
frontend configuration variable. - Database and migration approach, if
persistence is approved. - Ingestion token handling and rate-limit
configuration. - ML artifact location and model-loading policy. -
Retrieval index path/version and rebuild procedure. - Timeouts and retry
limits. - Local ports and startup order. - Test, lint, format,
type-check and security commands.

Planning blueprints may reference Python 3.12+, FastAPI, Pydantic 2.x,
SQLite/SQLAlchemy, Streamlit, Pytest and HTTPX. These remain proposed
until the Team Lead approves a coherent dependency set and the
repository lock/configuration confirms it.

### 18.2 Configuration rules

-   Read secrets from environment variables or an approved secret
    manager.
-   Commit a sanitized `.env.example`, never a populated `.env`.
-   Validate required settings at startup and fail with a safe,
    actionable message.
-   Do not place credentials in frontend source, URL query parameters,
    test fixtures or logs.
-   Keep service URLs, timeouts, page-size limits and model/index
    locations configurable where appropriate.
-   Avoid adding duplicate dependency declarations across root and
    subpackages without a clear packaging policy.
-   Avoid circular imports by keeping shared contracts independent of
    API/router modules.

## 19. Security and Privacy

Before exposing private repository data, Security/Privacy and the Team
Lead must decide: - Authentication mechanism and authorization model. -
Repository-level access checks. - Token scopes and rotation. - Request
and body size limits. - Rate limiting and expensive-operation
controls. - CORS origins for the actual deployment. - Logging/redaction
policy and retention. - Whether issue body snippets or source-code
evidence may be returned to the UI. - Whether any external model/service
may receive issue or code content. - SSRF protections for URLs and
source references. - Dependency and model artifact trust.

Input validation does not replace authorization. A valid repository ID
is not proof that the caller can access that repository.

Treat issue text, labels, URLs, code snippets and upstream error
messages as untrusted data. Do not let issue contents become privileged
instructions to an AI model. Do not send private source content to a
third-party service without explicit approval. Keep error messages
useful but non-sensitive.

## 20. Contract Change Management

Every proposed change must include:

1.  Problem statement.
2.  Current contract and evidence, or "not yet implemented".
3.  Proposed contract.
4.  Reason for change.
5.  Producer impact.
6.  Consumer impact.
7.  Compatibility classification.
8.  Migration plan.
9.  Required tests.
10. Documentation updates.
11. Required approvals.
12. Rollback/recovery plan.

Required reviewers depend on the change but normally include the owning
producer, every affected consumer, and the Team Lead for shared/public
contracts. Security-sensitive changes require the Security/Privacy
Reviewer. Root configuration and CI/deployment changes require
coordination with DevOps/MLOps.

Do not merge a shared contract change until names, types, nullability,
serialization, error behavior and consumer expectations are agreed.

## 21. Troubleshooting Handbook

These are diagnostic scenarios, not observed ORDO failures. Run commands
from the actual repository root and adapt module names to the real
layout.

  ------------------------------------------------------------------------------------------------------
  Symptom            Diagnostic     Likely cause            Safe remediation        Owner
                     action                                                         
  ------------------ -------------- ----------------------- ----------------------- --------------------
  API rejects a      Inspect HTTP   Field                   Fix producer or         API + consumer owner
  valid-looking      status/body;   name/type/nullability   consumer after          
  request            compare        mismatch                identifying the         
                     payload with                           approved schema; do not 
                     OpenAPI; run                           disable validation      
                     schema tests                           blindly                 

  UI expects a       Inspect        UI relied on            Agree whether field     API + Frontend
  missing field      sanitized      undocumented field or   belongs in public       
                     response and   API mapper omitted it   contract; update        
                     model/schema                           schema, producer,       
                                                            consumer and tests      
                                                            together                

  ID lookup fails    Compare types  Issue number confused   Preserve distinct       Data + API
                     and source of  with global issue ID;   identifiers and migrate 
                     each ID        string/int mismatch     consumers deliberately  

  Timestamp parsing  Inspect raw    Naive/invalid timestamp Add source-specific     Data + API
  fails              sanitized      or inconsistent         parsing/validation and  
                     timestamp      serialization           tests; do not silently  
                     format and                             assume UTC              
                     timezone                                                       

  `null` crashes UI  Check schema   Required-but-nullable   Standardize optionality API + Frontend
                     and serialized versus omitted          and null behavior; add  
                     payload        semantics unclear       UI empty/null tests     

  Unexpected HTTP    Capture        Handler mapping         Align handler and API   API
  status             status,        inconsistent with       tests; do not retry all 
                     request ID and policy                  failures                
                     safe error                                                     
                     code                                                           

  Error formats      Compare        Framework default       Map errors at API       API + Security
  differ             validation,    bypasses common handler boundary and test each  
                     domain and                             category                
                     upstream error                                                 
                     responses                                                      

  ML output invalid  Validate       Producer changed output Fail with typed         ML + API
                     against ML     or data missing         internal error or       
                     contract;                              approved fallback;      
                     inspect model                          never invent            
                     version and                            predictions             
                     safe                                                           
                     diagnostics                                                    

  Retrieval result   Inspect index  Index unavailable,      Return documented       Retrieval + API
  has no evidence    state, result  missing metadata or     warning/empty/partial   
                     type and       contract drift          behavior; never         
                     provenance                             fabricate provenance    

  Pagination         Re-run with    Unstable ordering,      Define stable           API/Data/Retrieval
  duplicates/skips   stable sort    wrong page base or data tie-breaker and test    
  results            and boundary   changing during         page boundaries         
                     fixtures       traversal                                       

  JSON serialization Check for      Internal object leaked  Explicitly map to       Producer + API
  fails              datetime,      into public response    JSON-safe schema;       
                     tensor,                                reject non-finite       
                     NaN/Infinity                           numbers                 
                     or custom                                                      
                     objects                                                        

  Circular import    Inspect import Shared model imports    Move only genuinely     Package owners
                     graph and      API/router              shared types to an      
                     minimal import implementation          approved                
                     traceback                              dependency-neutral      
                                                            module                  

  Dependency         Inspect        Incompatible dependency Resolve through         DevOps + affected
  conflict           lockfile,      ranges or duplicated    approved package        owner
                     Python runtime declarations            manager and CI; avoid   
                     and package                            ad-hoc global installs  
                     metadata                                                       

  OpenAPI differs    Regenerate     Route/schema changed    Update source           API
  from docs          schema from    without                 models/docs and rerun   
                     actual app and documentation/test      schema checks           
                     compare        update                                          

  Contract tests     Review diff    Breaking change,        Decide whether contract Producer + consumer
  fail after change  and failing    outdated fixture or     or implementation is    
                     fixture        accidental              wrong; update only      
                                    implementation          after owner approval    
                                    regression                                      

  Service cannot     Check          Incorrect env var,      Fix configuration and   API + DevOps
  connect            configured     service not started or  verify readiness; never 
                     URL, port,     network issue           paste secrets into logs 
                     process,                                                       
                     timeout and                                                    
                     sanitized logs                                                 
  ------------------------------------------------------------------------------------------------------

Useful initial commands after the environment is set up:

``` bash
python --version
python -m pip --version
python -m pytest
git status --short
git diff --check
```

These commands are examples; use the actual project's approved
environment and test commands.

## 22. Implementation Plan

### Phase 0 --- Team Lead establishes the repository

-   Create the approved monorepo and grant the team access.
-   Confirm branch policy and protected branch.
-   Approve initial layout and root dependency strategy.
-   Preserve the project requirements and role ownership boundaries.
-   Add repository instructions and a basic README.

**Exit gate:** engineers can clone the same repository and identify the
approved base branch.

### Phase 1 --- Repository reconnaissance

-   Every engineer inspects the existing structure and assigned area.
-   Record dependency versions and test commands.
-   Identify existing models, outputs and public functions.
-   Do not overwrite work to match a reference blueprint.

**Exit gate:** API Contract Engineer publishes an evidence-based
repository audit.

### Phase 2 --- Contract workshop

-   Data Engineer presents normalized issue output and source semantics.
-   ML Engineer presents input/output and prediction semantics.
-   Retrieval Engineer presents request/result and evidence provenance.
-   API Engineer presents proposed public endpoints and error behavior.
-   Frontend Engineer confirms render needs and failure states.
-   Security Reviewer confirms auth, private-data and logging
    constraints.
-   Team Lead resolves disagreements.

**Exit gate:** named owners approve the first contract set.

### Phase 3 --- Contract-first scaffolding

-   Add only approved shared schemas and examples.
-   Add schema tests and minimal synthetic fixtures.
-   Generate OpenAPI from implemented routes once they exist.
-   Add CI checks for contract tests.

**Exit gate:** agreed schemas can be imported/validated and tests run in
the project environment.

### Phase 4 --- Component implementation

-   Each engineer works within the assigned ownership boundary.
-   Use approved fakes where dependencies are incomplete.
-   Coordinate all shared/root changes by PR.
-   Add unit and component contract tests.

**Exit gate:** each component passes its own agreed tests.

### Phase 5 --- Integration

-   Connect ingestion, normalized storage, ML and retrieval through
    approved interfaces.
-   Connect Streamlit to FastAPI over HTTP.
-   Test empty results, malformed input, unavailable dependencies and
    authorization.
-   Record latency and resource limits before deciding sync versus async
    behavior.

**Exit gate:** critical end-to-end flows pass with actual components or
explicitly identified controlled test doubles.

### Phase 6 --- Compatibility, security and release readiness

-   Review OpenAPI changes and all shared contract changes.
-   Run full required tests, formatting, lint/type/security checks and
    deployment checks.
-   Complete privacy/security review and migration documentation.
-   Record actual test outcomes and known limitations.

**Exit gate:** Team Lead and required owners approve release readiness;
no checklist is marked complete without evidence.

## 23. Git and Pull Request Workflow

Use the actual repository policy. Do not assume the branch is named
`develop`.

Before changes:

``` bash
git status
git branch --show-current
git branch -a
git remote -v
```

After changes:

``` bash
git diff --check
git status
git diff
```

Suggested PR description:

``` markdown
## Summary
- Problem and intended behavior:

## Contract changes
- Contract IDs:
- Current behavior/evidence:
- Proposed/approved behavior:
- Compatibility classification:

## Affected components
- Producers:
- Consumers:
- Shared files:

## Tests
- Commands executed:
- Actual results:
- Tests not run and why:

## Security/privacy
- Authorization and sensitive-data impact:
- Logging/redaction:
- Review status:

## Migration and rollback
- Consumer updates:
- Rollback/recovery:

## Approvals
- Team Lead:
- Producer owner:
- Consumer owners:
- Security/DevOps review where required:

## Limitations
- Unresolved decisions:
- Known risks:
```

Do not claim tests passed unless executed. Do not commit `.env`,
credentials, private issue content, local indexes, model weights, or
unrelated files. Stage explicit paths and inspect the staged diff before
committing.

## 24. Risks and Unresolved Questions

The following questions block final approval of the contract baseline.

  -----------------------------------------------------------------------
  Question                Why it matters          Responsible
                                                  decision-maker
  ----------------------- ----------------------- -----------------------
  What exact product      Determines which routes Team Lead / Product
  workflows are in the    and schemas are         owner
  first release?          necessary               

  What is the canonical   Prevents ID collisions  Data Engineer + Team
  repository and issue    and conversion bugs     Lead
  identifier strategy?                            

  What does ingestion     Defines ML, retrieval   Data Engineer
  actually emit and       and API input contracts 
  persist?                                        

  Which ML tasks are in   Prevents speculative    ML Engineer + Team Lead
  MVP and what are their  endpoints and score     
  exact outputs?          mislabeling             

  Which retrieval result  Determines evidence     Retrieval Engineer
  types are supported?    schema and frontend     
                          rendering               

  What does the retrieval Prevents false          Retrieval Engineer
  score mean and is it    confidence claims       
  comparable?                                     

  Is sync work            Affects timeouts,       Team Lead + API + Data
  synchronous or          response model and UI   
  represented as jobs?    states                  

  Which database/storage  Affects persistence     Team Lead + Data/DevOps
  design is approved?     contracts and           
                          migrations              

  What auth and           Essential before        Team Lead + Security
  repository              private repository      
  authorization model is  access                  
  required?                                       

  What API versioning     Affects path design and Team Lead + API
  strategy is approved?   compatibility policy    

  What are supported      Required for code       DevOps + Team Lead
  Python/dependency       examples, model APIs    
  versions?               and CI                  

  Are external LLM/model  Privacy, cost and       Security/Privacy + Team
  services allowed to     security implications   Lead
  receive issue/code                              
  content?                                        

  How long are issue      Privacy and operational Team Lead + Security +
  content, logs and       design                  Data
  derived outputs                                 
  retained?                                       

  Which branch and PR     Avoids incorrect Git    Team Lead / repository
  rules are active?       workflow assumptions    admin
  -----------------------------------------------------------------------

Until these decisions are answered, examples in this manual remain
proposals.

## 25. Definition of Done

### Pre-repository planning completion

-   [x] A pre-repository status and evidence limitation are explicitly
    documented.
-   [x] Proposed ownership boundaries and logical integration flow are
    described.
-   [x] Proposed contract inventory and gap/decision register exist.
-   [x] Proposed serialization, error, versioning and change-management
    rules are documented.
-   [x] Repository-dependent work is explicitly marked blocked.
-   [x] Proposed example schemas and test examples are labeled as
    unexecuted.

### Must remain incomplete until repository creation and verification

-   [ ] Actual repository structure and Git state audited.
-   [ ] Python, FastAPI, Pydantic and other dependency versions
    verified.
-   [ ] Existing public endpoints and internal interfaces inventoried.
-   [ ] Evidence-based contract mismatches recorded.
-   [ ] Contract decisions approved by Team Lead and affected owners.
-   [ ] Models integrated into actual source tree.
-   [ ] Contract, API, consumer and integration tests executed.
-   [ ] OpenAPI generated and reviewed.
-   [ ] Security/privacy controls tested.
-   [ ] CI results, PR summary and handover completed.

The pre-repository blueprint is not equivalent to implementation
completion.

## 26. Appendix A --- Proposed Schema Examples

These snippets are illustrative and must be reconciled with approved
requirements and installed dependency versions.

### A.1 Proposed issue schema (Pydantic 2.x)

``` python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class NormalizedIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = "github"
    github_issue_id: int = Field(gt=0)
    repository_full_name: str = Field(min_length=1)
    issue_number: int = Field(gt=0)
    title: str = Field(min_length=1)
    body: str | None = None
    state: str = Field(min_length=1)
    labels: list[str] = Field(default_factory=list)
    author_login: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    closed_at: datetime | None = None
    html_url: HttpUrl | None = None
```

Before adopting this model, decide whether `repository_id` is required,
which `state` values are supported, how timezone normalization is
enforced, whether unknown fields should be rejected, and whether
`HttpUrl` serialization matches the public contract. This model is not a
substitute for source-specific normalization.

### A.2 Proposed error schema

``` python
from pydantic import BaseModel, ConfigDict


class ErrorBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    request_id: str | None = None
    details: dict[str, object] | None = None


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: ErrorBody
```

The API owner must decide whether `details` is omitted or null when
empty and ensure details never contain secrets, stack traces, private
source data or raw upstream responses.

### A.3 Proposed retrieval response concept

Do not finalize a concrete `score: float` contract until the Retrieval
Engineer documents the scoring method, allowed range, tie behavior, and
meaning. Evidence should carry provenance fields only when they can be
backed by indexed source data.

## 27. Appendix B --- Contract Change Request Template

``` markdown
# Contract Change Request

- Change ID:
- Requester / date:
- Owning producer:
- Affected consumers:
- Team Lead:

## 1. Problem statement

## 2. Current contract
- Evidence/source file or “not implemented”:
- Current example:

## 3. Proposed contract
- Schema/path/signature:
- Required and optional fields:
- Nullability and serialization:
- Error behavior:

## 4. Reason for change

## 5. Producer impact

## 6. Consumer impact
- API:
- Frontend:
- Ingestion:
- ML:
- Retrieval:
- Storage/CI/deployment:

## 7. Compatibility classification

## 8. Migration plan

## 9. Required tests

## 10. Documentation/OpenAPI updates

## 11. Security/privacy review

## 12. Owner approvals

## 13. Rollback or recovery plan

## 14. Verification results
- Exact commands:
- Actual outcomes:
```

## 28. Appendix C --- Pull Request Handover Checklist

-   [ ] Contract change is linked to an approved requirement/decision.
-   [ ] Producer and every affected consumer are identified.
-   [ ] Required/optional/null semantics are explicit.
-   [ ] Identifier and timestamp types are consistent.
-   [ ] Error codes, HTTP statuses and retry behavior are documented.
-   [ ] Retrieval score and ML output semantics are not overstated.
-   [ ] Empty results and dependency failures have defined behavior.
-   [ ] Unit and contract tests cover the schema.
-   [ ] Integration tests cover critical boundaries.
-   [ ] Streamlit can render success, empty, and error responses.
-   [ ] OpenAPI matches the implemented routes and models.
-   [ ] Authentication and repository authorization have been reviewed.
-   [ ] Logs and fixtures contain no secrets or unapproved private
    content.
-   [ ] `git diff --check` passes and only intended files are included.
-   [ ] Actual test commands and outcomes are recorded.
-   [ ] Required owners and Team Lead have approved.
-   [ ] Migration, known limitations and rollback are documented.

------------------------------------------------------------------------

**Final handover note:** Save this document at the root of the approved
ORDO monorepo as `ORDO_API_Contract_Integration_Standards_Blueprint.md`
when the repository is created. Until then, keep it as the
pre-repository planning artifact. Once code exists, replace provisional
examples with evidence from source files, approve contracts with owners,
and record real test results.
