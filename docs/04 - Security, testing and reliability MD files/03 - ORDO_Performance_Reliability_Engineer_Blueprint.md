# ORDO Performance & Reliability Engineer Blueprint

**Artifact:** `ORDO_Performance_Reliability_Engineer_Blueprint.md`\
**Project:** ORDO --- AI-Powered GitHub Issue Intelligence Platform\
**Role:** Performance and Reliability Engineer\
**Status:** Initial implementation manual; repository-specific audit and
benchmark results are **pending**\
**Last updated:** 2026-10-27

> **Important scope note:** The project owner has indicated that the
> ORDO repository has not yet been created. Therefore, this document
> does not claim that any source files, endpoints, dependencies, tests,
> or infrastructure have been inspected or executed. Paths and code
> below are either (a) commands to run after the repository exists, or
> (b) proposed examples to adapt after the owning engineer confirms the
> real implementation. Do not treat example paths, endpoint names,
> thresholds, or code as verified facts about ORDO.

## Table of contents

1.  [Executive Summary](#1-executive-summary)
2.  [Project Context and Scope](#2-project-context-and-scope)
3.  [Repository Audit](#3-repository-audit)
4.  [Component Ownership and
    Dependencies](#4-component-ownership-and-dependencies)
5.  [Performance and Reliability
    Baseline](#5-performance-and-reliability-baseline)
6.  [Performance Objectives and Acceptance
    Criteria](#6-performance-objectives-and-acceptance-criteria)
7.  [Profiling Tools and Procedures](#7-profiling-tools-and-procedures)
8.  [FastAPI Performance](#8-fastapi-performance)
9.  [Data Ingestion Performance](#9-data-ingestion-performance)
10. [ML Performance](#10-ml-performance)
11. [Code Retrieval Performance](#11-code-retrieval-performance)
12. [Streamlit Responsiveness](#12-streamlit-responsiveness)
13. [Caching Strategy](#13-caching-strategy)
14. [Reliability and Failure Modes](#14-reliability-and-failure-modes)
15. [Timeouts, Retries, and
    Resilience](#15-timeouts-retries-and-resilience)
16. [Resource Management and
    Concurrency](#16-resource-management-and-concurrency)
17. [Observability and Diagnostics](#17-observability-and-diagnostics)
18. [Health Checks and Readiness](#18-health-checks-and-readiness)
19. [Load, Stress, and Soak Testing](#19-load-stress-and-soak-testing)
20. [Performance Regression Testing](#20-performance-regression-testing)
21. [Capacity Planning](#21-capacity-planning)
22. [Security and Privacy](#22-security-and-privacy)
23. [Implementation Plan](#23-implementation-plan)
24. [Testing and Verification](#24-testing-and-verification)
25. [Troubleshooting Handbook](#25-troubleshooting-handbook)
26. [Git Workflow and Pull Request](#26-git-workflow-and-pull-request)
27. [Risks and Unresolved Questions](#27-risks-and-unresolved-questions)
28. [Operational Handover](#28-operational-handover)
29. [Definition of Done](#29-definition-of-done)

------------------------------------------------------------------------

## 1. Executive Summary

The Performance and Reliability Engineer is responsible for measuring
ORDO before optimizing it, identifying bottlenecks with evidence,
improving reliability without breaking contracts, and proving the effect
of changes through repeatable tests.

Because the repository does not yet exist, the current status is:

-   **Repository audit:** blocked until the initial repository is
    created and accessible.
-   **Baseline measurements:** not measured.
-   **Verified bottlenecks:** none established.
-   **Code changes:** none implemented by this document.
-   **Performance targets:** provisional proposals only; Project Lead
    approval required.
-   **Next action:** create/obtain the repository, record its initial
    Git state, and complete the audit in Section 3 before proposing
    implementation changes.

Do not use benchmark values in a report or pull request until the
command has actually been run and its raw output retained. The code
examples in this manual are templates, not evidence of current ORDO
behavior.

## 2. Project Context and Scope

ORDO is intended to be an AI-powered GitHub issue intelligence platform.
Candidate components described in the project brief include:

-   GitHub issue ingestion and normalization.
-   Machine-learning inference, if implemented.
-   Code retrieval and ranking, if implemented.
-   FastAPI backend.
-   Streamlit frontend.
-   Persistence or caching, if implemented.
-   Docker and CI/CD, if configured.

The repository must establish which components actually exist, how they
communicate, and which are required for a successful user request. Do
not assume a database, Redis, Celery, vector database, cloud provider,
GPU, or distributed worker system.

### In scope

-   Reproducible performance measurement and profiling.
-   API, ingestion, ML, retrieval, and frontend performance reviews
    where those components exist.
-   Failure behavior, bounded retries, timeouts, resource lifecycle, and
    graceful shutdown.
-   Tests and benchmark procedures.
-   Minimal useful observability.
-   Security/privacy checks related to performance work.
-   Rollback, pull-request, and operational handover documentation.

### Out of scope without approval

-   Changing public API contracts.
-   Changing authentication, authorization, data retention, or privacy
    policy.
-   Replacing the architecture or adding infrastructure merely for
    convenience.
-   Optimizing code owned by another role without that owner's review.
-   Running stress tests against production or consuming real GitHub API
    quota without explicit authorization.

## 3. Repository Audit

### 3.1 Gate: repository availability

The project owner has reported that the repository is not yet created.
Until it exists, record the audit as **Blocked --- repository
unavailable**, not "passed."

When a repository is created, open a terminal at its root and run:

``` bash
git status
git branch --show-current
git remote -v
git log -1 --oneline
```

Save the outputs in the engineering ticket or an approved audit note.
Redact any sensitive remote URL information before sharing logs.

### 3.2 Inventory commands

Run these from the repository root. Commands that find no matches should
be recorded as "not found," not used to infer that a component
definitely does not exist.

**Windows PowerShell:**

``` powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\(\.git|\.venv|venv|node_modules|__pycache__)\\' } |
  Select-Object -ExpandProperty FullName

Get-ChildItem -Recurse -File -Include pyproject.toml,requirements*.txt,poetry.lock,uv.lock,Pipfile,environment.yml
Get-ChildItem -Recurse -File -Include Dockerfile,compose.yaml,docker-compose.yml,*.yml,*.yaml
Get-ChildItem -Recurse -File -Include test_*.py,*_test.py,pytest.ini,tox.ini
```

**Cross-platform Git and Python checks:**

``` bash
python --version
python -m pip --version
git status --short
git branch --show-current
git remote -v
```

Do not install or upgrade dependencies during the initial audit. First
record the existing dependency-management method and lock files.

### 3.3 Audit checklist

Record **Finding**, **Evidence**, **Owner**, **Risk**, and **Follow-up**
for every row.

  ---------------------------------------------------------------------------------------------
  Area                   Inspect                            Evidence to       Status now
                                                            capture           
  ---------------------- ---------------------------------- ----------------- -----------------
  Runtime/dependencies   Python version, package manifest,  Manifest paths    Blocked
                         lock file                          and versions      

  Entry points           FastAPI app, Streamlit entry       Exact paths and   Blocked
                         point, CLI scripts                 launch commands   

  API lifecycle          Routers, middleware, dependencies, Files, handler    Blocked
                         startup/shutdown                   names, blocking   
                                                            calls             

  Ingestion              GitHub client, pagination,         Code path,        Blocked
                         retries, normalization             timeouts, quota   
                                                            handling          

  ML                     Model loading, preprocessing,      Artifact paths,   Blocked
                         inference                          load lifecycle,   
                                                            metrics           

  Retrieval              Index build, query, ranking,       Implementation    Blocked
                         serialization                      and index         
                                                            lifecycle         

  Persistence/cache      Database, cache, connection        Config and        Blocked
                         lifecycle if present               query/cache paths 

  Frontend               Streamlit state, reruns, API calls Exact             Blocked
                                                            pages/functions   
                                                            and repeated work 

  Reliability            Exceptions, timeouts, health       Code and tests    Blocked
                         endpoints                                            

  Observability          Logs, metrics, correlation IDs     Configuration and Blocked
                                                            example output    

  Deployment             Docker, CI/CD, resource limits     Files and         Blocked
                                                            pipeline          
                                                            configuration     

  Testing                Unit/integration/e2e/performance   Commands,         Blocked
                         tests                              duration, gaps    
  ---------------------------------------------------------------------------------------------

### 3.4 Performance-sensitive operation register

Create `docs/performance/operation-register.md` only if the team
approves this location. Initially list candidates, then replace them
with verified functions and file paths.

  --------------------------------------------------------------------------------------------------------------
  Operation                  Component            Input size External         Timing method    Evidence/status
                             owner                           dependency                        
  -------------------------- ----------- ------------------- ---------------- ---------------- -----------------
  GitHub issue fetch         Data                 To measure GitHub API       Per-request      Not audited
                             Engineer                                         timer            

  Normalization/validation   Data                 To measure None assumed     `perf_counter`   Not audited
                             Engineer                                                          

  ML inference               ML                   To measure Model/runtime    Warm/cold timing Not audited
                             Engineer,                                                         
                             if present                                                        

  Retrieval/index query      Retrieval            To measure Index/storage,   Query timer      Not audited
                             Engineer,                       if any                            
                             if present                                                        

  API request lifecycle      Backend       Payload-dependent Internal         HTTP benchmark   Not audited
                             Engineer                        dependencies                      

  Streamlit end-to-end       Frontend       Result-dependent FastAPI          Browser/user     Not audited
  search                     Engineer                                         timing           
  --------------------------------------------------------------------------------------------------------------

### 3.5 Repository audit output

The audit is complete only when it contains: 1. Exact repository commit
and branch. 2. Verified runtime and dependency-management approach. 3. A
component/dependency diagram based on actual files. 4. Exact entry
points and launch commands. 5. Existing tests and their current result.
6. A list of unknowns with a named owner and due date.

## 4. Component Ownership and Dependencies

Use the role boundaries in the ORDO project brief unless the Project
Lead records a different decision.

  -----------------------------------------------------------------------------
  Work area                    Primary owner           Required
                                                       reviewers/coordination
  ---------------------------- ----------------------- ------------------------
  GitHub ingestion and data    Data Engineer           Performance Engineer;
  transformations                                      Security Reviewer for
                                                       data exposure

  Model training/inference     ML Engineer             Performance Engineer;
                                                       Project Lead for quality
                                                       thresholds

  Retrieval/indexing/ranking   Code Retrieval Engineer Performance Engineer; QA
                                                       Engineer

  API handlers/contracts       FastAPI Backend         Performance Engineer;
                               Engineer                Project Lead for
                                                       contract changes

  Streamlit pages/session      Streamlit Frontend      Performance Engineer;
  state                        Engineer                Backend Engineer

  CI/CD, containers,           DevOps Engineer         Performance Engineer;
  deployment                                           Security Reviewer

  Test strategy and quality    QA Engineer             Component owners and
  gates                                                Performance Engineer

  Security/privacy review      Security and Privacy    Relevant component owner
                               Reviewer                

  Cross-team scope/contracts   Project Lead            Affected owners
  -----------------------------------------------------------------------------

The Performance Engineer should diagnose and propose changes, but must
not silently take ownership of another team's implementation. Any
shared-contract or architecture change requires Project Lead approval.

### Dependency map template

Populate only after repository inspection:

``` text
Streamlit UI
    -> FastAPI endpoint(s)
        -> [verified service/function]
            -> [GitHub API / ML / retrieval / persistence, if present]
```

Mark each edge as synchronous, asynchronous, or unknown, and record
timeout and failure propagation behavior.

## 5. Performance and Reliability Baseline

### 5.1 Baseline rules

-   Use a local or explicitly approved staging environment.
-   Prefer synthetic or sanitized data.
-   Fix the code commit, configuration, Python version, dependencies,
    and test data.
-   Warm up the application before measuring steady-state behavior;
    separately measure cold start.
-   Record concurrency, ramp-up, duration, number of requests, and
    machine resource limits.
-   Measure the same workload before and after a change.
-   Keep raw outputs in an approved location, excluding secrets and
    private issue content.
-   Never turn an unmeasured value into a reported baseline.

### 5.2 Required environment record

``` text
Git commit:
Branch:
OS/version:
CPU:
RAM:
Python:
Dependency lock/manifest:
Run command:
Configuration profile (no secrets):
Dataset description and row/issue count:
Cold-start procedure:
Warm-up duration:
Measured duration:
Concurrency/users:
Request mix:
Resource limits:
Date/time and operator:
Raw output location:
Known confounders:
```

### 5.3 Benchmark table

Fill this table only with actual measurements. Use `Not measured` until
a run is completed.

  ----------------------------------------------------------------------------------
  Workflow              Baseline           Target Method                Status
  ------------- ---------------- ---------------- --------------------- ------------
  API cold          Not measured       To approve Timed process startup Pending
  startup                                                               

  Lightweight       Not measured       To approve HTTP benchmark        Pending
  API request                                                           

  Search API        Not measured       To approve Representative        Pending
  request                                         request set           

  Retrieval         Not measured       To approve Component benchmark   Pending
  query                                                                 

  ML inference      Not measured       To approve Cold and warm         Pending
  (if present)                                    inference             

  Bounded           Not measured       To approve Fixed synthetic       Pending
  ingestion                                       fixture               

  End-to-end UI     Not measured       To approve Browser/manual trace  Pending
  search                                                                

  Dependency        Not measured  Correct bounded Failure injection     Pending
  unavailable                             failure                       

  Peak process      Not measured       To approve OS                    Pending
  memory                                          metrics/tracemalloc   
  ----------------------------------------------------------------------------------

### 5.4 Safe baseline sequence

1.  Run the existing unit tests without modifying code.
2.  Start each service using its documented command.
3.  Measure cold startup three times and report all runs plus median; do
    not hide outliers.
4.  Run a small warm-up workload.
5.  Measure a fixed request set at low concurrency.
6.  Repeat at expected local concurrency only after confirming the
    endpoint and data are safe.
7.  Capture CPU and memory before, during, and after the workload.
8.  Save exact commands and raw outputs.
9.  Repeat the baseline at least once to estimate run-to-run variation.

## 6. Performance Objectives and Acceptance Criteria

The Project Lead must approve objectives after workload and deployment
constraints are known. Until then, all targets are provisional.

Suggested initial **measurement gates**, not claims about current
performance:

-   Correctness: no changed result semantics or API contract without
    approval.
-   Error behavior: expected dependency failures return bounded,
    documented errors rather than false success.
-   Performance: compare median and p95 under identical conditions; use
    a relative improvement target only where a measurable bottleneck
    exists.
-   Memory: no unexplained sustained growth across a bounded soak run.
-   Reliability: no unhandled exceptions or resource leaks in the agreed
    failure tests.
-   Quality: retrieval relevance and ML quality must remain within
    owner-approved limits.
-   CI: functional tests must pass; timing gates should be added only
    after stable baselines exist.

Avoid choosing arbitrary universal latency numbers before the endpoint
mix, hardware, data size, and deployment context are known.

## 7. Profiling Tools and Procedures

Use existing tools first. Add dependencies only when they answer a
concrete question.

### 7.1 `time.perf_counter()` --- focused stage timing

Use for elapsed wall-clock time around a known operation. It is
low-overhead and suitable for a first breakdown.

``` python
from time import perf_counter

started = perf_counter()
result = operation_under_test()
elapsed_seconds = perf_counter() - started
print(f"operation_seconds={elapsed_seconds:.6f}")
```

Replace `operation_under_test()` with a real function found during the
audit. Do not commit this placeholder as runnable application code.

### 7.2 `cProfile` --- Python call-level profile

From the repository root, run against a verified script or module:

``` bash
python -m cProfile -o profile.out path/to/verified_benchmark.py
python -c "import pstats; pstats.Stats('profile.out').strip_dirs().sort_stats('cumtime').print_stats(40)"
```

The path is intentionally a placeholder. Use a fixed input and avoid
profiling a production workload. Inspect cumulative time first, then
call counts and self time. High cumulative time can be due to a slow
child call; it does not automatically mean the parent function itself
needs optimization.

### 7.3 `tracemalloc` --- Python allocation comparison

Create a temporary, untracked diagnostic script or approved test around
a representative operation:

``` python
import tracemalloc

tracemalloc.start()
# Run the bounded operation under investigation here.
current_bytes, peak_bytes = tracemalloc.get_traced_memory()
print(f"current_bytes={current_bytes}")
print(f"peak_bytes={peak_bytes}")
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:20]:
    print(stat)
tracemalloc.stop()
```

`tracemalloc` reports Python-tracked allocations, not all
native-library, model, GPU, or operating-system memory. Pair it with
OS/process memory metrics when relevant.

### 7.4 `py-spy` --- sampling a running process

Use only if installation is permitted and the process can be profiled
safely. Install it in the approved development environment, then use its
documented command for the current platform. Sampling helps locate hot
stacks without instrumenting every call. Do not attach to production
without authorization.

### 7.5 HTTP load test

Use an existing tool if present. If none exists, the following Locust
example can be introduced only after confirming that `/health` is a
real, safe endpoint and the local API is running.

`tests/performance/locustfile.py` (proposed example; do not add until
the route is verified):

``` python
from locust import HttpUser, between, task

class OrdoReadOnlyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        # Replace with a verified read-only endpoint.
        with self.client.get("/health", name="GET /health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
```

Example bounded local command after endpoint verification:

``` bash
locust -f tests/performance/locustfile.py --host http://127.0.0.1:8000 \
  --users 5 --spawn-rate 1 --run-time 2m --headless
```

This example intentionally tests only a read-only health route. Do not
point it at production or an external service. Do not use an ingestion
endpoint as a load-test task unless it is specifically designed for
safe, bounded testing.

### 7.6 Profiling workflow

1.  Reproduce a slow workflow with a fixed input.
2.  Record wall time and relevant resource usage.
3.  Profile the same workload.
4.  Identify the highest-impact verified call path.
5.  Form one testable hypothesis.
6.  Change one concern at a time.
7.  Run correctness tests.
8.  Repeat the exact benchmark and compare results.
9.  Record trade-offs and run-to-run variation.
10. Revert if improvement is not repeatable or correctness degrades.

## 8. FastAPI Performance

**Audit first:** locate the actual `FastAPI()` construction, routers,
middleware, dependency functions, startup/shutdown hooks, and request
handlers. No endpoint names or source paths are known yet.

### Inspection questions

-   Does an `async def` handler call blocking network, file, database,
    or model code?
-   Are HTTP clients or models recreated on every request?
-   Are external calls given explicit connect/read/total timeouts?
-   Is concurrency bounded for expensive operations?
-   Are response payloads unnecessarily large?
-   Is work repeated across dependency layers?
-   Are exceptions mapped to correct HTTP responses?
-   Are resources closed during shutdown?
-   Are request and correlation IDs available without logging sensitive
    payloads?

### Change: remove verified repeated initialization

**Problem:** only valid if profiling or code inspection proves a
client/model is repeatedly created on a hot path.\
**Evidence:** record constructor call counts, timing, and the exact
file/function.\
**Affected files:** unknown until repository exists.\
**Implementation:** prefer the existing application lifespan/resource
pattern; initialize reusable clients once per process when safe, and
close them at shutdown. Do not copy a generic lifespan implementation
into the app until current framework versions and ownership conventions
are confirmed.\
**Compatibility:** verify startup failure behavior, client
thread-safety, and model lifecycle.\
**Verification:** unit-test initialization count, test shutdown cleanup,
run API integration tests, and compare cold/warm latency.\
**Rollback:** revert the focused patch if lifecycle or concurrency tests
fail.\
**Approval:** FastAPI Backend Engineer; Project Lead if contracts
change.

### Blocking versus async work

-   Use async I/O only when the dependency library actually supports it.
-   Do not label CPU-bound model inference as async and assume it
    becomes faster.
-   For blocking I/O in an async handler, select an appropriate bounded
    thread/offload strategy after measuring.
-   For CPU-bound work, evaluate process isolation or controlled worker
    execution only if evidence and architecture justify it.
-   Never create unbounded tasks or threads in response to arbitrary
    user traffic.

### API response checks

For each expensive endpoint, measure request parsing, dependency setup,
external calls, core computation, serialization, and total latency
separately where practical. Preserve status codes, response schemas,
ordering, and error semantics unless an approved contract change is
made.

## 9. Data Ingestion Performance

Audit the real GitHub client and ingestion pipeline before modifying it.

### Required checks

-   Pagination termination and page-size behavior.
-   Connection reuse and explicit timeouts.
-   GitHub rate-limit headers and reset times.
-   Retry classification and bounded total retry duration.
-   Duplicate issue handling and idempotency.
-   Repeated parsing/normalization.
-   Memory use for large result sets.
-   Incremental ingestion and checkpoint support.
-   Recovery from interruption or partially completed runs.
-   Quota consumption for the bounded benchmark.

### Retry policy principles

Retry only transient failures (for example, selected network errors, 429
responses, and selected 5xx responses) when the API's guidance supports
it. Do not retry authentication failures, invalid requests, or
permission failures indefinitely. Respect `Retry-After` and
service-specific rate-limit guidance. Use capped exponential backoff
with jitter and a maximum total time budget.

Do not implement checkpointing without defining its consistency model:
when is a record considered committed, how are duplicates detected, and
how is an interrupted page/job resumed?

### Bounded ingestion benchmark

Use a sanitized fixture or mock GitHub client that returns a fixed
number of pages. Record: - number of synthetic issues, - page count, -
transformations executed, - elapsed time, - issues/second, - peak
memory, - retry count, - duplicate count, - failures and recovery
result.

Never benchmark by fetching an unbounded repository history or by
intentionally exhausting real API quotas.

## 10. ML Performance

This section applies only if the audit confirms an ML model in ORDO.

Separate **training-time** concerns from **inference-time** concerns.
Measure model artifact loading, preprocessing, warm-up, per-item
inference, batching, post-processing, and memory independently.

Check for: - Model loaded once per request instead of a controlled
lifecycle. - Repeated tokenization or preprocessing. - Unnecessary
conversions/copies. - Batch sizes that exceed memory or hurt tail
latency. - Unbounded concurrent inference. - Cold-start and warm-start
differences. - Artifact/version mismatch. - Reproducibility and approved
quality metrics.

Do not change preprocessing semantics, thresholds, model versions, or
output schemas merely to reduce latency. The ML Engineer must define
quality checks and acceptable tolerances. If no metric or quality
threshold exists, request one from the ML Engineer and Project Lead
before accepting an optimization.

**Acceptance:** correctness tests pass; quality metrics remain within
approved limits; warm and cold timing are separately reported; memory
behavior is measured under the expected concurrency.

## 11. Code Retrieval Performance

This section applies only if the repository contains a
retrieval/indexing subsystem.

Measure indexing and query paths separately. Track: - Index build time
and source corpus size. - Whether indexes rebuild on every request or
process start. - Query preprocessing time. - Candidate count and ranking
time. - Embedding generation time if applicable. - Serialization time
and response size. - Memory/storage footprint. - Retrieval relevance
using the project's actual evaluation set.

Do not switch search technology, add a vector database, or cache results
before the current implementation and workload justify it. An
optimization is not acceptable if relevance degrades beyond the agreed
threshold.

For index lifecycle changes, document versioning, invalidation, rebuild,
corruption recovery, and compatibility with existing persisted
artifacts. The Code Retrieval Engineer owns implementation approval.

## 12. Streamlit Responsiveness

Inspect the actual UI entry point and pages. Identify expensive work
executed on every rerun, repeated API calls, repeated model/data
loading, unnecessary result rendering, and session-state misuse.

### Cache decision rules

-   `st.cache_data`: suitable for reusable serializable data when the
    cache key captures all relevant inputs and the data can safely be
    shared.
-   `st.cache_resource`: suitable for reusable resources such as a
    thread-safe client or model, with explicit lifecycle and concurrency
    considerations.
-   Do not cache authentication-dependent or sensitive results in a
    shared context unless isolation is proven.
-   Document cache key inputs, TTL, invalidation, memory behavior, and
    stale-data behavior.
-   Do not cache a result merely because it is expensive; first
    establish whether repeated execution is unnecessary and whether
    sharing is safe.

### UI acceptance

-   The frontend displays a clear loading state for long operations.
-   Backend failures produce actionable, non-sensitive feedback.
-   A failed API call does not masquerade as an empty successful result.
-   Session state does not leak one user's data into another session.
-   API calls are not duplicated by avoidable reruns.
-   Result limits/pagination are used where supported by the existing
    API contract.

The Streamlit Frontend Engineer owns UI changes.

## 13. Caching Strategy

No cache technology is assumed to exist.

Before adding or changing a cache, document:

  -----------------------------------------------------------------------
  Field                               Required decision
  ----------------------------------- -----------------------------------
  Purpose                             Which measured repeated work does
                                      it avoid?

  Key                                 Which parameters, identity,
                                      version, and filters affect the
                                      result?

  Value                               What is stored, and is it safe to
                                      share?

  Expiration                          Is there a TTL or version-based
                                      invalidation?

  Invalidation                        What event makes the value stale?

  Size                                How are memory/storage limits
                                      enforced?

  Concurrency                         Can simultaneous misses cause
                                      duplicate expensive work?

  Failure                             Does cache failure safely fall back
                                      to the source?

  Privacy                             Could one user receive another
                                      user's or private issue's data?

  Measurement                         What are hit rate, miss latency,
                                      and memory costs?
  -----------------------------------------------------------------------

Compare cache hit and miss behavior under the same workload. Include a
way to disable or clear the cache in tests if the implementation
supports it. Do not introduce Redis or another external service without
a measured need, operational plan, and owner approval.

## 14. Reliability and Failure Modes

Complete this matrix after the real architecture is known. The rows
below are candidate scenarios from the project brief, not confirmation
that every dependency exists.

  --------------------------------------------------------------------------------------------------------------
  Failure mode     Detection            User impact        Desired recovery     Test             Owner
  ---------------- -------------------- ------------------ -------------------- ---------------- ---------------
  GitHub API       Timeout/connection   Ingestion/search   Bounded failure,     Mock network     Data Engineer
  outage           error                may be unavailable preserve prior valid failure          
                                        or stale           data where                            
                                                           applicable                            

  GitHub rate      HTTP 429/headers     Delayed ingestion  Respect              Mock 429 and     Data Engineer
  limit                                                    reset/Retry-After;   reset            
                                                           stop within budget                    

  Invalid upstream Schema/validation    One operation may  Reject safely; log   Malformed        Data Engineer
  response         error                fail               sanitized category   fixture          

  Missing          Startup validation   Service cannot     Fail fast with safe  Remove required  Component owner
  configuration                         start correctly    actionable message   test setting     

  Model            Exception/health     ML feature         Fail clearly or      Mock             ML Engineer
  load/inference   signal               unavailable        approved fallback    load/inference   
  failure                                                                       error            

  Retrieval index  Open/query failure   Search unavailable Clear failure;       Temporary        Retrieval
  absent/corrupt                        or incomplete      approved rebuild     invalid test     Engineer
                                                           procedure            index            

  Database         Connection/query     Data-dependent     Bounded timeout and  Test-only        Backend/Data
  unavailable, if  error                feature fails      safe error           unavailable      owner
  used                                                                          service          

  Frontend cannot  HTTP/network failure Search/action      Show retryable       Point test UI at Frontend
  reach API                             fails              message; no false    stopped local    Engineer
                                                           success              API              

  Memory pressure  OS/container metrics Slowdown or        Bound work and data; Small controlled Performance +
                                        process            document             load test        DevOps
                                        termination        restart/recovery                      

  Partial          Job/checkpoint state Missing or         Idempotent resume or Interrupt mock   Data Engineer
  ingestion                             duplicate records  explicit restart     job              

  Unexpected       Structured error log Request fails      Correct 5xx; no      Inject           Component owner
  exception                                                secret/traceback     controlled       
                                                           leak to user         exception        
  --------------------------------------------------------------------------------------------------------------

Failure injection must run only in local/test environments with
disposable data. Never kill production dependencies or corrupt a real
index as an experiment.

## 15. Timeouts, Retries, and Resilience

For every external call, record:

  ---------------------------------------------------------------------------------------------------------
  Operation   Connect timeout     Read/total   Retryable cases         Attempts/budget   Final behavior
                                  timeout                                                
  ----------- ------------------- ------------ ----------------------- ----------------- ------------------
  GitHub API  To set from         To set       Transient/network,      Bounded and       Explicit
  request     client/deployment                selected 5xx/429 per    approved          failure/status
              needs                            API guidance                              

  Frontend →  To set              To set       Usually avoid blind     Based on          Clear UI error
  FastAPI                                      retries for             operation         
                                               non-idempotent actions  idempotency       

  Internal    Based on measured   Based on     Do not retry            Bounded           Feature-specific
  model call  inference and user  measured     deterministic failures                    error
              SLO                 inference    blindly                                   

  Database    Based on driver     Based on     Driver/error-specific   Bounded           Safe failure
  call, if                        query budget                                           
  present                                                                                
  ---------------------------------------------------------------------------------------------------------

Values must be chosen after the owner identifies the client library and
latency requirements. Avoid retry multiplication: if the UI retries
three times, the API retries three times, and a client retries three
times, one user action may amplify into many upstream calls.

A circuit breaker is not a default requirement. Consider one only when
repeated calls to a failing dependency cause resource exhaustion or
cascading latency. Document states, thresholds, half-open behavior,
metrics, and tests before implementing it.

## 16. Resource Management and Concurrency

Audit lifecycle and bounds for HTTP clients, database connections (if
present), file handles, model resources, thread/process pools,
background tasks, temporary files, in-memory datasets, and concurrent
ingestion jobs.

Checklist: - Reuse long-lived clients where safe; close them at
shutdown. - Bound expensive concurrent operations. - Limit request and
dataset sizes. - Avoid unbounded in-memory accumulation. - Ensure
temporary files are removed after success and failure. - Avoid shared
mutable state unless synchronization semantics are clear. - Test
shutdown while a bounded local operation is active. - Define what
happens when ingestion is interrupted. - Do not add a task queue or
distributed workers without an approved requirement.

### Resource lifecycle template

``` text
Process startup
  -> validate configuration
  -> initialize required resources once
  -> mark ready when required resources are usable
  -> serve bounded requests
  -> stop accepting new work on shutdown
  -> finish/cancel in-flight work according to policy
  -> close clients/connections/files
  -> exit
```

Adapt this sequence to the actual application lifecycle; it is a design
checklist, not a verified current flow.

## 17. Observability and Diagnostics

Start with logs and measurements that answer specific operational
questions. Add a monitoring platform only when deployment needs justify
it.

### Minimal useful measurements

-   Request count, latency distribution, and error count.
-   External dependency duration and error category.
-   Ingestion duration, processed count, retries, and failures.
-   Retrieval latency and candidate count, if applicable.
-   ML load/inference duration and failures, if applicable.
-   Process CPU and memory.
-   Cache hit/miss and eviction behavior, if applicable.
-   Startup duration and readiness state.

### Structured log fields

Use fields supported by the application: `timestamp`, `severity`,
`component`, `operation`, `request_id` or correlation ID if implemented,
`duration_ms`, `outcome`, and `error_category`.

Never log access tokens, authorization headers, passwords, private issue
contents, or unnecessary personal data. Prefer counts and sanitized
error categories over full payloads.

### Trace a slow request

1.  Record a request/correlation ID if the architecture supports it.
2.  Capture frontend request start/end and HTTP status.
3.  Match the request in API logs.
4.  Compare handler total time with individual dependency durations.
5.  Inspect the relevant component profile or timer.
6.  Check CPU, memory, connection saturation, and upstream errors for
    the same interval.
7.  Reproduce with a fixed safe input.
8.  Change one cause at a time and rerun the benchmark.

Do not expose a metrics or diagnostic endpoint publicly without
access-control and deployment review.

## 18. Health Checks and Readiness

First inspect whether health endpoints already exist. Avoid duplicate
endpoints with conflicting semantics.

-   **Liveness:** process is running and responsive; should not fail
    solely because an optional external service is down.
-   **Readiness:** the process can handle its intended workload.
-   **Dependency status:** status of required dependencies, reported
    separately where practical.

Decide which dependencies are essential and which features can degrade
gracefully. A health endpoint should be cheap, bounded, and safe; it
must not trigger a full ingestion, model reload, or index rebuild.

If the Backend Engineer approves new endpoints, add tests for healthy
state, required dependency unavailable, and optional dependency
unavailable. Do not publish implementation code for a route until the
current app structure and API contract are known.

## 19. Load, Stress, and Soak Testing

All load testing must be performed against local or explicitly
authorized staging services. Never run stress tests against production
without explicit authorization.

  -------------------------------------------------------------------------
  Test type         Purpose           Initial safe        Main measurements
                                      approach            
  ----------------- ----------------- ------------------- -----------------
  Load              Expected normal   Small bounded users p50/p95/p99,
                    usage             and fixed request   throughput,
                                      mix                 errors

  Stress            Find limits       Increase in small   Failure point,
                    beyond normal     steps with stop     saturation,
                    load              conditions          recovery

  Spike             Sudden traffic    Controlled          Queueing,
                    change            step-up/step-down   timeouts,
                                                          recovery

  Soak              Sustained         Low bounded traffic Memory trend,
                    resource behavior over a longer       error trend,
                                      window              latency drift

  Concurrency       Race/resource     Simultaneous safe   Duplicate work,
                    correctness       requests            state corruption,
                                                          errors
  -------------------------------------------------------------------------

### Test plan template

For every run record: - endpoint/workflow and whether it is read-only, -
environment and commit, - dataset and payload size, - users/concurrency
and ramp-up, - warm-up and measured duration, - request distribution, -
response codes and error rate, - p50/p95/p99 latency and throughput, -
CPU/memory and relevant dependency metrics, - safety stop conditions, -
cleanup and raw output location.

### Stop conditions

Stop the test if unexpected writes occur, real API quotas are being
consumed, error rates rise sharply, memory approaches the environment
limit, the service becomes unresponsive, or the target is not the
intended local/staging host. Keep a human operator present for stress
and failure-injection runs.

## 20. Performance Regression Testing

Do not add brittle timing assertions to ordinary unit tests before a
stable baseline exists.

Recommended tiers: - **Unit tests:** correctness and bounded behavior,
no strict wall-clock thresholds unless the operation is deterministic
and tiny. - **Integration tests:** API/contract correctness, timeout
handling, resource cleanup. - **Scheduled/manual benchmarks:**
representative latency, throughput, memory, ingestion, retrieval, and
inference. - **CI performance check:** only after stable runner
conditions and repeatable baselines are established.

Record baseline commit, command, environment, dataset, run count,
summary statistics, and raw output. Compare before/after results under
identical conditions. Define release-blocking regression thresholds with
the Project Lead and QA Engineer; use relative change and noise bounds
rather than a single universal latency limit.

A regression guard is **not implemented** until a CI job or documented
repeatable process has been added and verified.

## 21. Capacity Planning

No production traffic, hardware, or deployment limits are currently
verified. Do not estimate production capacity until these inputs are
collected.

  ----------------------------------------------------------------------------
  Input               Value             Source               Confidence /
                                                             follow-up
  ------------------- ----------------- -------------------- -----------------
  Typical and peak    Unknown           Product/deployment   Required
  requests/second                       owner                

  Concurrent users    Unknown           Product owner        Required

  Dataset size and    Unknown           Data Engineer        Required
  growth                                                     

  Model               Unknown / if      ML Engineer          Required
  memory/runtime      applicable                             

  Retrieval index     Unknown / if      Retrieval Engineer   Required
  size                applicable                             

  GitHub quota        Unknown           Data Engineer        Required
  profile                                                    

  CPU/RAM/container   Unknown           DevOps Engineer      Required
  limits                                                     

  Connection limits   Unknown / if      Backend/DevOps       Required
                      applicable                             
  ----------------------------------------------------------------------------

Diagnose likely bottlenecks using evidence: - **CPU:** sustained high
CPU and profiles showing compute-heavy stacks. - **Memory:** rising
process RSS, allocation snapshots, large resident model/index, or OOM
events. - **Disk:** high I/O wait or slow reads/writes correlated with
latency. - **Network:** time spent waiting on remote calls, retransmits,
or high dependency latency. - **Upstream:** latency/error spikes
correlated with GitHub or another dependency. - **Lock/contention:**
latency grows with concurrency while CPU is not saturated and stacks
show waiting.

Do not recommend larger infrastructure until the bottleneck and workload
have been measured.

## 22. Security and Privacy

Performance work must preserve security controls.

Review: - Request and upload size limits. - Bounded concurrency and
expensive unauthenticated paths. - Sensitive fields in logs and
benchmark output. - Shared cache isolation. - Large response payloads. -
Secrets in test scripts or command history. - Production/private issue
data copied into local test fixtures. - Load-test credentials committed
to Git. - Diagnostic and metrics endpoints exposed without controls.

Use synthetic or approved sanitized data. Coordinate security-sensitive
changes with the Security and Privacy Reviewer. Do not change
authentication, authorization, access-control, or retention behavior
without explicit review and approval.

## 23. Implementation Plan

Follow this order. Each stage requires evidence and a completion record.

  -------------------------------------------------------------------------------------
  Stage                   Actions               Output/evidence       Completion gate
  ----------------------- --------------------- --------------------- -----------------
  1\. Audit and ownership Obtain repo; record   Audit table,          Actual paths and
                          Git/runtime; map      ownership map         owners identified
                          actual components                           

  2\. Baseline            Fixed workload,       Baseline report       Reproducible or
                          environment record,                         blocker
                          raw results                                 documented

  3\. Profile             Profile               Profiles and timing   Hot path
                          representative slow   breakdown             supported by
                          workflows                                   evidence

  4\. Rank bottlenecks    Score impact,         Prioritized register  Top issue has
                          confidence, effort,                         owner and
                          risk                                        hypothesis

  5\. Approve objectives  Propose provisional   Project Lead decision Thresholds
                          SLOs and quality                            approved or open
                          bounds                                      

  6\. Fix bottleneck      One narrow patch by   Diff, tests,          Correctness and
                          owning engineer       benchmark             benefit verified

  7\. Resilience          Audit                 Policy table and      Bounded behavior
                          timeout/retry/error   failure tests         verified
                          policies                                    

  8\.                     Inspect lifecycle and Lifecycle notes and   No known
  Resources/concurrency   bounds                tests                 unbounded path
                                                                      left unexplained

  9\.                     Add only useful       Logs/metrics/health   No sensitive
  Observability/health    approved signals      tests                 data; signals
                                                                      actionable

  10\. Regression tests   Select stable tests   Test commands/CI      Tests repeat
                          and benchmark cadence change if approved    reliably

  11\. Repeat benchmarks  Run same workload and Before/after report   Results include
                          environment                                 variance and
                                                                      errors

  12\. Review             Correctness,          Review approvals      Required owners
                          security, privacy,                          approve
                          contracts                                   

  13\.                    Document config and   Rollback steps        Recovery
  Rollback/deployment     rollback                                    procedure
                                                                      reviewed

  14\. PR/handover        Summarize evidence    PR description,       Project Lead
                          and unresolved risks  runbook               accepts handover
  -------------------------------------------------------------------------------------

### Bottleneck register template

  ----------------------------------------------------------------------------------------------------------
  ID         Finding       Evidence     Impact    Confidence   Effort    Risk      Owner   Priority/status
  ---------- ------------- ------------ --------- ------------ --------- --------- ------- -----------------
  PERF-001   Not           Repository   Unknown   None         Unknown   Unknown   TBD     Blocked
             established   not                                                             
                           available                                                       

  ----------------------------------------------------------------------------------------------------------

Do not fill this with guessed problems. Promote an item only after code
inspection or measurement confirms it.

## 24. Testing and Verification

Use the repository's actual test conventions once available. Do not
assume pytest, a test folder, or a particular command until the manifest
and existing CI are inspected.

For every change, record:

1.  Behavior protected.
2.  Exact test file(s).
3.  Test implementation or bounded patch.
4.  Command and working directory.
5.  Expected result.
6.  Actual result and captured output.
7.  Failure diagnosis.
8.  Compatibility risk.
9.  Benchmark comparison.
10. Rollback condition.

### Verification matrix

  -----------------------------------------------------------------------
  Change type                         Minimum verification
  ----------------------------------- -----------------------------------
  API hot-path change                 Unit + API integration + contract
                                      test + before/after benchmark

  Ingestion change                    Pagination/retry/idempotency
                                      tests + bounded mock benchmark

  ML change                           Output parity/quality metric +
                                      cold/warm latency + memory

  Retrieval change                    Relevance tests + query latency +
                                      index lifecycle tests

  Streamlit change                    UI/API failure state + rerun/cache
                                      behavior + manual end-to-end test

  Cache change                        Hit/miss parity + invalidation +
                                      concurrency/privacy tests

  Timeout/retry change                Deterministic simulated failure +
                                      total time-budget assertion

  Resource lifecycle change           Init count + cleanup on
                                      success/failure + shutdown test

  CI/deployment change                Pipeline validation + local/staging
                                      smoke test + rollback check
  -----------------------------------------------------------------------

Never claim a test passed unless it was run. Report skipped tests and
reasons explicitly.

## 25. Troubleshooting Handbook

The commands below are diagnostic starting points; adapt them to the
actual runtime and scripts. Example output is not represented as
observed ORDO output.

### 25.1 Slow API responses

1.  **Symptoms:** high p95/p99 or long UI wait.
2.  **Likely causes:** slow dependency, blocking I/O, repeated
    preprocessing, serialization, contention.
3.  **Diagnosis:** compare total HTTP latency with per-stage timers; run
    `cProfile` on a fixed safe workflow; inspect upstream latency.
4.  **Interpretation:** if most time is in a remote call, local
    micro-optimization will have limited benefit.
5.  **Safe correction:** fix the measured stage only; set bounded
    timeouts where missing and approved.
6.  **Verify:** repeat identical workload and compare latency
    distribution and error rate.
7.  **Escalate:** Backend Engineer for handler/contracts; component
    owner for ingestion, ML, or retrieval.

### 25.2 High CPU

1.  **Symptoms:** sustained CPU saturation and throughput flattening.
2.  **Likely causes:** CPU-heavy ranking/preprocessing, repeated
    parsing, inefficient loops, excess concurrent work.
3.  **Diagnosis:** OS process metrics plus `cProfile` or approved
    sampling profiler.
4.  **Interpretation:** focus on cumulative time and call counts;
    confirm the workload is representative.
5.  **Safe correction:** reduce verified repeated work or bound
    concurrency; avoid premature multiprocessing.
6.  **Verify:** same workload, CPU time, throughput, p95, and
    correctness.
7.  **Escalate:** owner of the hot function; DevOps if limits differ
    between local and deployment.

### 25.3 Excessive or growing memory

1.  **Symptoms:** high RSS, OOM, or memory rising across repeated
    operations.
2.  **Likely causes:** retained datasets/results, index/model size,
    unbounded cache, leaked references, native allocations.
3.  **Diagnosis:** process RSS over time plus `tracemalloc`; note that
    Python allocation tracking misses some native memory.
4.  **Interpretation:** compare snapshots and whether memory falls after
    references are released; distinguish a one-time model load from
    growth per request.
5.  **Safe correction:** bound datasets/cache/concurrency or fix
    retention only after identifying the allocation path.
6.  **Verify:** repeat a bounded soak run and compare memory trend.
7.  **Escalate:** ML/Retrieval owner for model/index; DevOps for
    container limits.

### 25.4 Slow ingestion or GitHub rate limiting

1.  **Symptoms:** low issues/second, repeated 429s, long waits.
2.  **Likely causes:** pagination inefficiency, quota limits, repeated
    requests, no connection reuse, retries without budget.
3.  **Diagnosis:** log page count, request duration, status category,
    rate-limit metadata, retry count; never log tokens or full private
    issue content.
4.  **Interpretation:** distinguish upstream throttling from local
    transformation cost.
5.  **Safe correction:** use bounded retries, respect API guidance,
    reuse clients, and benchmark transformations with a mock client.
6.  **Verify:** fixed fixture and separately authorized small upstream
    smoke test if needed.
7.  **Escalate:** Data Engineer; Security Reviewer if logging/data
    handling is implicated.

### 25.5 Repeated timeouts

1.  **Symptoms:** requests hang or timeout at multiple layers.
2.  **Likely causes:** missing timeout, retry multiplication, saturated
    pool, slow upstream, network failure.
3.  **Diagnosis:** record stage timings and total elapsed time; inspect
    retry counts and pool utilization.
4.  **Interpretation:** total duration should be bounded by the designed
    budget, not multiplied unpredictably by nested retries.
5.  **Safe correction:** establish per-operation budgets and retry
    ownership.
6.  **Verify:** inject a deterministic test timeout and assert bounded
    completion.
7.  **Escalate:** owner of the client or dependency; DevOps for
    network/deployment conditions.

### 25.6 Slow ML inference

1.  **Symptoms:** cold requests slow or latency rises with concurrency.
2.  **Likely causes:** repeated model loading, preprocessing, poor batch
    size, CPU contention, memory pressure.
3.  **Diagnosis:** separately time load, warm-up, preprocess, inference,
    and postprocess.
4.  **Interpretation:** compare cold and warm results; validate the
    model is not reloaded per request.
5.  **Safe correction:** only change lifecycle/batching after measuring
    and defining quality limits.
6.  **Verify:** output/quality parity, latency, memory, and concurrency.
7.  **Escalate:** ML Engineer.

### 25.7 Slow retrieval

1.  **Symptoms:** retrieval endpoint dominates end-to-end latency.
2.  **Likely causes:** repeated index build, embedding generation, too
    many candidates, ranking, serialization.
3.  **Diagnosis:** separate index startup, query preprocessing,
    candidate search, ranking, and response construction.
4.  **Interpretation:** measure relevance separately from latency.
5.  **Safe correction:** optimize the measured stage without changing
    result semantics silently.
6.  **Verify:** approved relevance suite and repeatable latency
    benchmark.
7.  **Escalate:** Code Retrieval Engineer.

### 25.8 High Streamlit rerun cost

1.  **Symptoms:** UI appears to reload, repeats API calls, or reloads
    models/data.
2.  **Likely causes:** expensive top-level work, state misuse, unsafe
    cache scope, duplicate UI/backend logic.
3.  **Diagnosis:** inspect rerun paths, count API calls, and time UI
    stages.
4.  **Interpretation:** distinguish a normal Streamlit rerun from
    genuinely duplicated external work.
5.  **Safe correction:** use session state/cache only with correct
    keying, invalidation, and privacy semantics.
6.  **Verify:** same user action makes the expected number of calls;
    errors remain visible.
7.  **Escalate:** Streamlit Frontend Engineer.

### 25.9 Cache inconsistency

1.  **Symptoms:** stale or cross-context results.
2.  **Likely causes:** incomplete key, wrong TTL, missing invalidation,
    shared user-specific data.
3.  **Diagnosis:** test each key input and compare cache hit with fresh
    source result.
4.  **Interpretation:** correctness/privacy defects outrank latency
    benefit.
5.  **Safe correction:** fix key/isolation/invalidation or disable the
    cache.
6.  **Verify:** hit/miss parity, stale-data test, concurrent-user
    isolation test.
7.  **Escalate:** cache owner and Security Reviewer where user data is
    involved.

### 25.10 Database latency (only if a database exists)

1.  **Symptoms:** query spans dominate endpoint latency.
2.  **Likely causes:** repeated queries, missing indexes, connection
    pool exhaustion, large result sets.
3.  **Diagnosis:** use the database's approved query timing and
    explain-plan tooling; do not expose credentials.
4.  **Interpretation:** verify actual query count and query plan before
    adding indexes.
5.  **Safe correction:** owner-reviewed query/index change with
    migration and rollback.
6.  **Verify:** correctness, query latency, concurrency, and migration
    rollback.
7.  **Escalate:** database/backend owner.

### 25.11 Concurrency failures

1.  **Symptoms:** duplicate jobs, corrupted state, intermittent
    exceptions, inconsistent results.
2.  **Likely causes:** shared mutable state, unbounded jobs,
    non-idempotent operations, unsafe clients.
3.  **Diagnosis:** bounded concurrent test with deterministic fixtures
    and request/job IDs.
4.  **Interpretation:** reproduce before changing locking or execution
    model.
5.  **Safe correction:** enforce bounds and idempotency or
    synchronization appropriate to the actual design.
6.  **Verify:** repeat concurrency test and inspect resource cleanup.
7.  **Escalate:** owning component engineer and Project Lead for
    architectural changes.

### 25.12 Unstable load tests or local/CI differences

1.  **Symptoms:** noisy p95 or intermittent benchmark failure.
2.  **Likely causes:** shared runner load, different dependency
    versions, cold caches, inconsistent data, background processes.
3.  **Diagnosis:** compare environment records, repeat runs, separate
    warm-up from measurement, inspect resource contention.
4.  **Interpretation:** do not treat small differences within run-to-run
    noise as real improvement.
5.  **Safe correction:** pin test inputs/environment and use scheduled
    benchmarks for noisy metrics.
6.  **Verify:** repeated runs show a consistent effect.
7.  **Escalate:** QA for test design; DevOps for runner/environment
    differences.

### 25.13 Regression after optimization

1.  **Symptoms:** lower latency but changed results, increased errors,
    or memory growth.
2.  **Likely causes:** semantic change, stale cache, concurrency bug,
    hidden retries, reduced retrieval/model quality.
3.  **Diagnosis:** compare API outputs, quality metrics, logs, resource
    use, and benchmark configuration.
4.  **Interpretation:** a speedup is not accepted if correctness,
    privacy, reliability, or approved quality regresses.
5.  **Safe correction:** disable/revert the focused patch; preserve
    diagnostic evidence.
6.  **Verify:** baseline behavior restored and regression test added.
7.  **Escalate:** component owner, QA, Security Reviewer, or Project
    Lead according to the failure.

## 26. Git Workflow and Pull Request

Before edits:

``` bash
git status
git branch --show-current
git remote -v
```

Confirm branch/PR conventions with the Project Lead. Do not assume the
target branch is `main` or `develop`.

After edits:

``` bash
git diff --check
git status
git diff
```

Then run relevant tests and benchmarks. Inspect the diff for unrelated
changes, generated profiles, credentials, private data, and large
artifacts. Keep raw benchmark output only in an approved location.

### Pull request template

``` markdown
## Problem and evidence
- Verified issue:
- Evidence/profile:
- Baseline commit/environment:

## Change
- Files changed:
- Behavior changed:
- API/contract impact:

## Measurements
- Before:
- After:
- Run count and variance:
- Workload/configuration:

## Verification
- Tests executed:
- Benchmarks executed:
- Failures/skipped checks and reasons:

## Resource, security, and privacy impact
- CPU/memory/dependency effects:
- Sensitive data/logging review:
- Required approvals:

## Rollback
- Revert/configuration steps:
- Rollback trigger:

## Limitations and follow-up
- Open questions:
- Owner:
```

Use a commit message such as
`perf: reduce repeated retrieval preprocessing` only if it matches team
conventions and the change really does that.

## 27. Risks and Unresolved Questions

  -------------------------------------------------------------------------------
  Question            Why it matters          Required owner    Status
  ------------------- ----------------------- ----------------- -----------------
  Where is the        Required for audit and  Project Lead      Open
  repository and what exact paths                               
  is its initial                                                
  commit?                                                       

  Which               Reproducible runs       Backend/DevOps    Open
  Python/dependency                                             
  manager is                                                    
  selected?                                                     

  Which components    Avoid false assumptions Project Lead +    Open
  are actually                                component owners  
  implemented?                                                  

  What are the        Prevent compatibility   Backend           Open
  supported API       breaks                  Engineer +        
  contracts?                                  Project Lead      

  What workloads and  Meaningful SLOs and     Product/Project   Open
  concurrency are     capacity                Lead              
  expected?                                                     

  Which quality       Prevent quality         ML/Retrieval      Open
  metrics protect     regressions             Engineer          
  ML/retrieval                                                  
  behavior?                                                     

  Which data can be   Privacy and             Security          Open
  used for tests?     repeatability           Reviewer/Data     
                                              Engineer          

  What is the         Safe load/failure       DevOps            Open
  approved staging    testing                                   
  environment?                                                  

  What branch and PR  Safe collaboration      Project Lead      Open
  rules apply?                                                  

  Which dependencies  Readiness/degradation   Component owners  Open
  are essential       design                                    
  versus optional?                                              
  -------------------------------------------------------------------------------

### Risk register

  ----------------------------------------------------------------------------
  Risk                    Mitigation                   Owner
  ----------------------- ---------------------------- -----------------------
  Optimizing before       Make audit a hard gate       Performance Engineer
  repository audit                                     

  Invented baseline or    Keep `Not measured`; require Performance Engineer +
  target                  raw evidence                 QA

  Cross-team code changes Require owning engineer      Project Lead
                          review                       

  Load test consumes real Local mock/staging, bounded  Performance Engineer +
  quota or writes data    workload, stop conditions    Data Engineer

  Speedup changes         Owner-approved quality suite ML/Retrieval Engineer
  retrieval/model quality                              

  Cache leaks/stale data  Key/invalidation/isolation   Component owner +
                          tests                        Security Reviewer

  Retry amplification     One explicit retry budget    Backend/Data owner
                          per dependency path          

  Monitoring exposes      Sanitization and access      Security Reviewer
  sensitive data          review                       
  ----------------------------------------------------------------------------

## 28. Operational Handover

Before handover, provide: - Repository commit and branch tested. -
Current component/dependency map. - Baseline environment and raw
benchmark locations. - Approved SLOs and quality thresholds, or
explicitly unresolved approvals. - Changes merged/released and
associated PRs. - Before/after measurements and their limitations. -
Test commands and actual outcomes. - Known failure modes and recovery
steps. - Resource limits and capacity assumptions. - Logging/metrics
locations and privacy review. - Rollback procedure and trigger. -
Outstanding risks, owners, and due dates. - Next benchmark/review date
if agreed.

### Handover checklist

-   [ ] Repository audit complete with exact paths.
-   [ ] Baseline is reproducible or measurement blocker is explicit.
-   [ ] No fabricated measurements or test results.
-   [ ] Each accepted optimization has correctness and performance
    evidence.
-   [ ] Failure behavior is bounded and tested where feasible.
-   [ ] Security/privacy review is recorded.
-   [ ] Rollback procedure has been reviewed.
-   [ ] Component owners and Project Lead have approved required
    changes.
-   [ ] Operational owner knows how to diagnose common failures.

## 29. Definition of Done

The performance/reliability work is complete only when:

-   [ ] The actual repository has been audited.
-   [ ] Performance-sensitive workflows and owners are identified.
-   [ ] A reproducible baseline exists, or inability to measure is
    documented.
-   [ ] Profiling procedures are reproducible.
-   [ ] Bottlenecks are backed by code evidence or measurements.
-   [ ] Proposed code changes are repository-specific and
    owner-approved.
-   [ ] Correctness/regression tests are provided and their actual
    results recorded.
-   [ ] Reliability and failure behavior are documented.
-   [ ] Load tests use bounded, repeatable, authorized workloads.
-   [ ] Before/after measurements are reported only when collected.
-   [ ] Security/privacy implications are reviewed.
-   [ ] Rollback instructions are available.
-   [ ] Required approvals are recorded.
-   [ ] Unresolved risks and dependencies have owners.
-   [ ] PR summary and operational handover are ready.

------------------------------------------------------------------------

## Appendix A --- First-session command sequence

Run only after the repository has been created and cloned:

``` bash
# 1. Enter the repository root.
git status
git branch --show-current
git remote -v
git log -1 --oneline

# 2. Record runtime and package tooling.
python --version
python -m pip --version

# 3. Inspect tracked files and manifests.
git ls-files
```

Then use the existing project documentation to run its tests. Do not
guess a test command before inspecting the manifest and CI
configuration.

## Appendix B --- Evidence discipline

Use these status labels consistently:

-   **Verified:** directly confirmed in the repository or by an executed
    test/measurement.
-   **Measured:** a numeric result was collected with the
    workload/environment recorded.
-   **Proposed:** suggested implementation not yet applied.
-   **Pending approval:** requires the named owner or Project Lead.
-   **Not measured:** procedure exists but has not been run.
-   **Blocked:** required repository, environment, data, or access is
    unavailable.
-   **Not applicable:** repository evidence confirms the component does
    not exist or the scenario does not apply.

Do not change a status label without new evidence.
