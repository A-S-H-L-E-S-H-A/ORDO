# ORDO Code Retrieval Engineer Blueprint

**Deliverable:** `ORDO_Code_Retrieval_Engineer_Blueprint.md`\
**Project:** ORDO --- AI-powered GitHub Issue Intelligence Platform\
**Status:** Repository-specific decisions remain unverified until the
engineer inspects the actual repository.

> **Repository limitation:** This blueprint was prepared from the
> uploaded role prompt. No ORDO source-code checkout, repository URL,
> schemas, dependency manifests, or CI files were supplied. It therefore
> does not claim that example files, branches, interfaces, dependencies,
> or features already exist. All illustrative designs must be checked
> against the actual repository. The included lexical-search example is
> a reference implementation, not an instruction to replace an existing
> search system.

## How to use this manual

Follow the sections in order. Inspect first, agree on contracts second,
and implement only after confirming the target and strategy. Labels
mean:

-   **Confirmed from role brief:** required responsibilities and
    ownership boundaries.
-   **Must inspect:** verify in the repository.
-   **Proposed:** a design requiring approval.
-   **Illustrative:** an example, not a claim about current ORDO
    behavior.
-   **Blocked decision:** stop and ask the named owner before
    proceeding.

# Section 1 --- Role Overview

## Purpose

The Code Retrieval Engineer builds the retrieval layer that finds
relevant ORDO records for a user query. The retrieval target may be
GitHub issues, source files, documentation, or a combination; the title
"Code Retrieval" does not settle this question. Confirm it from
requirements and actual code.

Example queries include "login fails after token refresh," "database
connection timeout," or "open issues labelled bug in repository X."
Results should be relevant, stable, consistently ranked, and limited to
data the caller is allowed to access.

## Expected deliverables

1.  Repository inspection report and open-decision list.
2.  Approved input/output contract and retrieval strategy.
3.  Retrieval implementation in the existing/approved package.
4.  Mapping/index lifecycle code only if required.
5.  Unit, contract, integration, and regression tests appropriate to the
    implementation.
6.  Relevance evaluation data and script if required.
7.  Integration notes for ingestion, ML, API, UI, and security owners.
8.  Updated documentation.
9.  Focused feature branch, commits, pull request, and handover report.

## Ownership boundaries

  -------------------------------------------------------------------------
  Owner                   Coordinate on           Do not change without
                                                  approval
  ----------------------- ----------------------- -------------------------
  Team Lead               Architecture,           Root config, shared
                          acceptance criteria,    schemas, architecture
                          base branch, shared     
                          contracts               

  Data Engineer           Authoritative record    Ingestion/normalization
                          schema, IDs,            code
                          update/delete semantics 

  ML Engineer             Approved embedding      Model loading/training
                          interface,              implementation
                          model/version,          
                          dimensions              

  API Engineer            Request/response        FastAPI routes and
                          contracts, errors,      API-owned schemas
                          dependency injection    

  Web Engineer            UI consumption path and Streamlit/frontend
                          result fields           implementation

  Security/Privacy        Access, retention,      Organization security
  Reviewer                logging, private data   policy
                          handling                

  DevOps/MLOps            Runtime, CI,            CI/deployment files
                          deployment, index       outside approved scope
                          persistence             
  -------------------------------------------------------------------------

## Definition of done --- overview

The work is complete only when the agreed behavior is implemented,
relevant tests and evaluation are run, integration contracts are
compatible, docs match the code, security/privacy checks are addressed,
the PR is reviewable, and unresolved dependencies are handed over.
Passing unit tests alone does not prove production readiness.

**Checkpoint:** State the retrieval target, caller, public interface,
access restrictions, and expected result fields before implementation
begins.

# Section 2 --- Architecture and Data Flow

The role brief describes ingestion, normalization, ML, retrieval,
FastAPI, Streamlit, testing, CI/CD, and security as possible platform
capabilities---not proof that each exists today.

## Proposed retrieval flow

``` mermaid
flowchart TD
    A[GitHub Issues or approved source] --> B[Existing ingestion pipeline]
    B --> C[Normalized records]
    C --> D{Separate index required?}
    D -- No --> E[Existing lookup/store]
    D -- Yes --> F[Retrieval index]
    U[User query] --> Q[Validate and process query]
    Q --> R[Retrieval strategy]
    E --> R
    F --> R
    R --> K[Filter and rank]
    K --> O[Stable retrieval results]
    O --> API[Approved API/application consumer]
```

-   **Ingestion:** owned upstream; provides records using an agreed
    schema.
-   **Normalized records:** authoritative data and stable IDs.
-   **Index decision:** exact lookup may not require a separate index.
-   **Query processing:** validates inputs and applies safe, approved
    normalization.
-   **Retrieval strategy:** exact, lexical/BM25, semantic, hybrid, or
    another approved method.
-   **Filtering/ranking:** applies filters and deterministic
    tie-breaking.
-   **Consumer:** invokes a stable package interface; HTTP and UI
    behavior remain in their layers.

## Proposed package interaction

``` mermaid
flowchart LR
    ING[Data ingestion owner] -->|normalized records| RET[Retrieval package]
    ML[ML owner] -. optional approved embeddings .-> RET
    CONTRACTS[Shared contracts] <--> RET
    API[FastAPI/API owner] -->|public interface| RET
    API --> UI[UI consumer]
```

This is proposed, not a verified diagram of the current repository.
Remove or rename components to match the actual source tree.

## Inspection report template

``` markdown
# Retrieval Repository Inspection
- Date / engineer:
- Repository root:
- Active branch:
- Approved base branch and evidence:
- Python version / package manager:
- Test framework / formatter / linter:
- Existing retrieval implementation:
- Authoritative record schema and stable ID:
- Embedding interface (if any):
- API request/response contract:
- CI workflow:
- Baseline test result:
- Files expected to change:
- Files out of scope:
- Open decisions, owners, and dates:
```

# Section 3 --- Development Environment Setup

## Inspect before installing

Run commands from the repository root.

``` bash
git status --short
git branch --show-current
git branch -a
git log -5 --oneline
git remote -v
```

These commands reveal uncommitted changes, active/local/remote branches,
recent history, and configured remotes. Do not discard local changes. Do
not publish private remote URLs.

Directory inspection:

Windows CMD:

``` bat
dir
tree /F
```

PowerShell:

``` powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\(\.git|\.venv|venv|node_modules)\\' } |
  Select-Object -ExpandProperty FullName
```

macOS/Linux:

``` bash
find . -maxdepth 3 -type f -not -path './.git/*' -not -path './.venv/*' | sort
```

Inspect any existing `README.md`, `pyproject.toml`, lockfiles,
`requirements.txt`, `.gitignore`, `docs/`, `packages/data_ingestion/`,
`packages/ml_engine/`, `packages/code_retrieval/`, `apps/api/`,
`tests/`, `.github/workflows/`, configuration, schemas, and
search/embedding code. Do not dump `.env` contents or private data into
logs.

## Verify Python and environment

Windows:

``` bat
py --version
py -0p
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python --version
```

PowerShell:

``` powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python --version
```

macOS/Linux:

``` bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python --version
```

Use the Python version required by repository metadata/CI. If the
project does not use a virtual environment, follow its documented
practice. If PowerShell blocks activation, follow team policy or invoke
the venv interpreter directly; do not weaken machine-wide policy without
approval.

Install dependencies only through the repository's established package
manager. Examples---not universal instructions:

``` bash
python -m pip install -r requirements.txt
# or, if the repository documents editable installation:
python -m pip install -e .
```

If it uses Poetry, uv, PDM, or another tool, use the locked workflow
already documented. Do not install new search libraries until strategy
and dependency approval.

Run the documented baseline tests before editing. If pytest is
confirmed:

``` bash
python -m pytest
```

Record actual results and pre-existing failures. If setup fails, verify
interpreter, lockfile, and CI instructions before changing versions.

**Checkpoint:** approved runtime and dependencies are installed;
baseline tests have been run; existing failures are recorded.

# Section 4 --- Retrieval Requirements and Contracts

Before coding, answer:

1.  What is searchable: issues, code, docs, or a combination?
2.  Is search scoped by repository, organization, or caller permission?
3.  Which schema is authoritative, and what is the stable ID?
4.  Which fields are searchable text versus metadata?
5.  Which filters, sorting, pagination, and top-k limits are required?
6.  Are snippets or full content returned?
7.  What happens for empty/invalid queries and no matches?
8.  What are the score semantics and tie-breaking rules?
9.  What latency, scale, refresh, and resource constraints are
    documented?
10. How are updates, duplicates, and deletions represented?
11. Who owns API error mapping and authorization?
12. Is semantic search required, and is an approved embedding interface
    available?

Illustrative result contract only:

``` python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class RetrievalResult:
    document_id: str
    score: float
    content: str
    metadata: dict[str, Any]
```

If the repository already uses Pydantic, `TypedDict`, dataclasses, or
shared schemas, follow that convention. Do not create a competing
contract.

## Contract review checklist

-   [ ] Retrieval target and use cases agreed.
-   [ ] Authoritative schema and stable ID confirmed.
-   [ ] Searchable fields and metadata agreed.
-   [ ] Filters and access-control contract agreed.
-   [ ] Result fields, score semantics, and ordering agreed.
-   [ ] Empty result, invalid input, and error behavior agreed.
-   [ ] Update/delete and duplicate semantics agreed.
-   [ ] Embedding dependency approved if needed.
-   [ ] Latency/top-k/pagination constraints documented.
-   [ ] Acceptance thresholds assigned to an owner.

Ask the Data Engineer about source records, the ML Engineer about
embeddings, and the API Engineer about public request/response behavior.
The Team Lead resolves conflicts. Do not invent field names or model
interfaces.

# Section 5 --- Retrieval Strategy Selection

  --------------------------------------------------------------------------------------------------
  Strategy         Use when                 Advantages     Limitations/dependencies   Evaluation
  ---------------- ------------------------ -------------- -------------------------- --------------
  Exact/metadata   IDs, repository, state,  Simple and     No paraphrase              Exact
  lookup           labels                   precise        understanding              correctness,
                                                                                      latency

  Lexical search   Known keywords and error Transparent    Misses                     Precision@k,
                   text                     and            synonyms/paraphrases       Recall@k, MRR
                                            inexpensive                               

  BM25             Larger keyword-search    Term rarity    Requires                   Precision@k,
                   corpus                   and document   implementation/library and MRR, NDCG@k
                                            length affect  tokenization decisions     
                                            ranking                                   

  Semantic vector  Paraphrases/conceptual   Finds meaning  Approved embedding model   Recall@k, MRR,
  search           similarity               without exact  and vector index required  NDCG@k
                                            words                                     

  Hybrid           Exact terms and          Balances       More complexity; score     Compare on
                   paraphrases both matter  lexical and    scales differ              same labelled
                                            semantic                                  queries
                                            strengths                                 

  Reranking        Candidate set is good    Can improve    Adds latency/cost; cannot  NDCG/MRR plus
                   but order needs          top-result     recover missing candidates latency
                   improvement              order                                     
  --------------------------------------------------------------------------------------------------

``` mermaid
flowchart TD
    A[Confirm requirements] --> B{Only IDs/metadata?}
    B -- Yes --> C[Existing lookup]
    B -- No --> D{Keyword matching sufficient?}
    D -- Yes --> E[Lexical or BM25 baseline]
    D -- No --> F{Approved embedding interface?}
    F -- No --> G[Block semantic work; agree interface]
    F -- Yes --> H{Need exact terms and paraphrases?}
    H -- No --> I[Semantic retrieval if justified]
    H -- Yes --> J[Evaluate hybrid]
    C --> K[Measure relevance and latency]
    E --> K
    I --> K
    J --> K
```

Do not introduce a hosted vector database, paid API, heavy dependency,
or every strategy by default. Choose the simplest approach that meets
the requirements. If unclear, record a blocked decision and ask the Team
Lead.

Decision record:

``` markdown
- Retrieval target:
- Chosen strategy and alternatives:
- Rationale:
- Approved dependencies:
- Index/persistence and update behavior:
- Evaluation dataset and metrics:
- Privacy/access implications:
- Approver/date:
- Deferred options:
```

# Section 6 --- Package Structure and Implementation Plan

Use actual package boundaries. This possible tree is illustrative:

``` text
packages/code_retrieval/
  __init__.py
  schemas.py             # only if new contract is approved
  query_processor.py     # if needed
  document_mapper.py     # if needed
  index_manager.py       # only if a separate index is required
  lexical_search.py      # only if lexical search is selected
  retriever.py           # public orchestration interface
tests/code_retrieval/
  test_query_processor.py
  test_document_mapper.py
  test_index_manager.py
  test_lexical_search.py
  test_retriever.py
docs/
  code-retrieval.md      # actual approved docs location
```

  ---------------------------------------------------------------------------------------
  Candidate file         Responsibility               Inputs/outputs    Status
  ---------------------- ---------------------------- ----------------- -----------------
  `schemas.py`           Approved query/result types  Contract types    Must inspect;
                                                                        avoid duplication

  `query_processor.py`   Query validation             Raw query →       New only if
                                                      validated query   needed

  `document_mapper.py`   Source mapping               Source record →   Blocked until
                                                      retrieval         schema known
                                                      document          

  `index_manager.py`     Build/update/delete/reload   Documents ↔ index Only if index
                                                                        required

  `lexical_search.py`    Lexical candidate scoring    Query + docs →    Only if strategy
                                                      ranked hits       selected

  `retriever.py`         Stable public API            Query/options →   Follow existing
                                                      results           architecture

  Tests/docs             Verify and explain behavior  Real implemented  Add to existing
                                                      contract          conventions
  ---------------------------------------------------------------------------------------

``` mermaid
flowchart TD
    SC[Approved schemas] --> Q[Query processing]
    SC --> DM[Document mapping]
    Q --> R[Retrieval strategy]
    DM --> IX[Index, if needed]
    IX --> R
    R --> RK[Filters and ranking]
    RK --> P[Public retrieval interface]
    P --> API[API/application consumer]
```

Avoid circular imports and duplicated model-loading logic. Do not create
empty modules to match an example tree.

# Section 7 --- Implement Query Validation and Processing

Rules: validate input type, reject or explicitly handle whitespace-only
queries, cap query length/top-k, preserve Unicode, avoid destructive
normalization, validate filter keys/types, and parameterize any
database/search expressions. Do not silently turn invalid filters into
broad searches. Keep HTTP status mapping in the API layer when that is
the existing convention.

## Complete illustrative implementation

**File:** `packages/code_retrieval/query_processor.py`\
**Status:** reference code only; adapt imports and conventions to the
repository.

``` python
from __future__ import annotations

from dataclasses import dataclass


class InvalidQueryError(ValueError):
    """Raised when a retrieval query is invalid."""


@dataclass(frozen=True)
class ProcessedQuery:
    original: str
    normalized: str
    tokens: tuple[str, ...]


def process_query(query: str, *, max_length: int = 500) -> ProcessedQuery:
    if not isinstance(query, str):
        raise InvalidQueryError("query must be a string")
    if not isinstance(max_length, int) or isinstance(max_length, bool) or max_length < 1:
        raise ValueError("max_length must be a positive integer")

    normalized = query.strip()
    if not normalized:
        raise InvalidQueryError("query must not be empty")
    if len(normalized) > max_length:
        raise InvalidQueryError(f"query exceeds the {max_length}-character limit")

    tokens = tuple(token.casefold() for token in normalized.split() if token)
    if not tokens:
        raise InvalidQueryError("query must contain a searchable token")

    return ProcessedQuery(query, normalized, tokens)
```

`strip()` removes edge whitespace; `casefold()` supports Unicode-aware
case-insensitive matching. The whitespace tokenizer is intentionally
simple and may not suit every language or corpus. Change normalization
only with relevance/regression tests.

**Tests:** `tests/code_retrieval/test_query_processor.py`

``` python
import pytest
from packages.code_retrieval.query_processor import InvalidQueryError, process_query


def test_valid_query_preserves_punctuation():
    result = process_query("  Login fails: HTTP-401  ")
    assert result.normalized == "Login fails: HTTP-401"
    assert result.tokens == ("login", "fails:", "http-401")


@pytest.mark.parametrize("query", ["", " ", "\t\n"])
def test_empty_query_rejected(query):
    with pytest.raises(InvalidQueryError):
        process_query(query)


def test_non_string_rejected():
    with pytest.raises(InvalidQueryError):
        process_query(None)  # type: ignore[arg-type]


def test_length_limit():
    with pytest.raises(InvalidQueryError, match="exceeds"):
        process_query("abcdef", max_length=5)


def test_invalid_max_length():
    with pytest.raises(ValueError, match="max_length"):
        process_query("hello", max_length=0)


def test_unicode_preserved():
    assert process_query("café 登录").tokens == ("café", "登录")
```

Run if pytest is the project runner:

``` bash
python -m pytest tests/code_retrieval/test_query_processor.py
```

If imports fail, inspect package configuration and neighboring tests
rather than adding unexplained path hacks.

**Checkpoint:** Validation rules match the agreed contract and tests
cover normal, empty, malformed, Unicode, and boundary inputs.

# Section 8 --- Implement the Document or Issue Mapping Layer

Do not implement a mapper until the authoritative source schema is
available. Potential fields include stable ID, repository identity,
title, body, labels, state, timestamps, and source URL; none should be
claimed as present without evidence.

Create a mapping table:

  ---------------------------------------------------------------------------------
  Source field              Searchable?       Metadata?         Missing-value rule
  ------------------------- ----------------- ----------------- -------------------
  Stable ID                 Usually no        Yes               Reject/quarantine
                                                                if absent, per
                                                                contract

  Title/body                Usually yes if    Optional          Schema-approved
                            supplied                            null/empty behavior

  Repository identity       Sometimes         Yes               Required if
                                                                scope/access
                                                                filtering needs it

  Labels/state/timestamps   Usually metadata  Yes               Preserve source
                                                                semantics

  URL                       Usually no        Yes if consumers  Do not synthesize
                                              need it           unverified URLs
  ---------------------------------------------------------------------------------

Preserve stable IDs; never derive IDs from titles or list positions.
Define duplicate, update, and deletion behavior with the Data Engineer.
Keep only approved fields, preserve access-control metadata, and avoid
unnecessary copies of private issue bodies.

**Blocked dependency:** request the actual record model/schema, one
sanitized example, stable-ID semantics, null rules, update/delete
signals, and fields approved for indexing/retention. Then implement a
typed mapper with tests for missing fields, Unicode, duplicate IDs, and
updates. A guessed generic dictionary mapper is not a substitute for a
missing contract.

# Section 9 --- Implement the Index Lifecycle

A separate index is not automatic. Exact lookup may use an existing
store; an in-memory index may be suitable for tests or a small
prototype; local persistent or external indexing needs a justified
operational requirement.

  -----------------------------------------------------------------------
  Type                    Suitable when           Main concerns
  ----------------------- ----------------------- -----------------------
  No separate index       Existing store meets    Query capability and
                          requirements            load

  In-memory               Small/temporary corpus  Startup rebuild, RAM,
                                                  worker duplication

  Local persistent        Local durable state     Permissions,
                          needed                  corruption, versioning,
                                                  backup

  External service        Scale/operations        Cost, network,
                          justify it              security, deployment
                                                  burden
  -----------------------------------------------------------------------

If indexing is selected, define initial build, incremental upsert,
duplicate prevention, replacement, deletion/stale cleanup,
persistence/reload, version compatibility, interrupted-build recovery,
atomic publication, and rebuild/rollback.

``` mermaid
flowchart TD
    A[Authoritative records] --> B[Validate schema and IDs]
    B --> C[Build staging index]
    C --> D{Validation succeeds?}
    D -- No --> E[Abort; retain prior usable index]
    D -- Yes --> F[Publish version]
    F --> G[Load and search]
    H[Update] --> C
    I[Deletion] --> J[Remove/mark stale per contract]
    J --> C
    K[Schema/model change] --> L[Approved rebuild]
    L --> C
```

This is conceptual. Verify the chosen library's atomicity and
multi-process guarantees. Test build, reload, repeated upsert, deletion,
interrupted build, and schema/model version mismatch using temporary
data.

# Section 10 --- Implement Lexical Retrieval, If Required

The following complete example is a small in-memory lexical baseline. It
is not BM25, not persistent, and not a recommendation to replace an
existing search library. Use only if the strategy decision approves it.

**File:** `packages/code_retrieval/lexical_search.py`

``` python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from packages.code_retrieval.query_processor import process_query


@dataclass(frozen=True)
class SearchDocument:
    document_id: str
    content: str
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    score: float
    content: str
    metadata: Mapping[str, Any]


class InvalidSearchParameter(ValueError):
    pass


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.casefold() for token in text.split() if token)


class LexicalRetriever:
    """Simple term-frequency scorer with deterministic ID tie-breaking."""

    def __init__(self, documents: Iterable[SearchDocument]) -> None:
        by_id: dict[str, SearchDocument] = {}
        for document in documents:
            if not isinstance(document.document_id, str) or not document.document_id:
                raise ValueError("document_id must be a non-empty string")
            if document.document_id in by_id:
                raise ValueError(f"duplicate document_id: {document.document_id}")
            if not isinstance(document.content, str):
                raise ValueError("document content must be a string")
            by_id[document.document_id] = document
        self._documents = tuple(by_id[key] for key in sorted(by_id))
        self._tokens = {
            document.document_id: _tokens(document.content)
            for document in self._documents
        }

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> list[SearchHit]:
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
            raise InvalidSearchParameter("top_k must be a positive integer")
        query_terms = set(process_query(query).tokens)
        filters = filters or {}
        hits: list[SearchHit] = []

        for document in self._documents:
            if not all(document.metadata.get(key) == value
                       for key, value in filters.items()):
                continue
            terms = self._tokens[document.document_id]
            score = float(sum(terms.count(term) for term in query_terms))
            if score > 0:
                hits.append(SearchHit(
                    document.document_id, score, document.content, document.metadata
                ))

        hits.sort(key=lambda hit: (-hit.score, hit.document_id))
        return hits[:top_k]
```

Limitations: whitespace tokenization means punctuation can affect
matches; the score is not BM25 or a probability; filters are exact
equality and not an authorization system; documents remain in memory;
the example returns full content instead of snippets; no phrase search,
stemming, typo tolerance, field weighting, or semantic similarity is
provided.

**Tests:** `tests/code_retrieval/test_lexical_search.py`

``` python
import pytest
from packages.code_retrieval.lexical_search import LexicalRetriever, SearchDocument


@pytest.fixture
def retriever():
    return LexicalRetriever([
        SearchDocument("ISSUE-2", "login token refresh fails",
                       {"state": "open", "repository": "org/app"}),
        SearchDocument("ISSUE-1", "database connection timeout",
                       {"state": "open", "repository": "org/api"}),
        SearchDocument("ISSUE-3", "CSV import drops empty values",
                       {"state": "closed", "repository": "org/app"}),
    ])


def test_known_terms_match(retriever):
    assert retriever.search("database connection timeout")[0].document_id == "ISSUE-1"


def test_body_term_match(retriever):
    assert [x.document_id for x in retriever.search("refresh")] == ["ISSUE-2"]


def test_no_match_is_empty(retriever):
    assert retriever.search("unrelatedxyz") == []


def test_filter(retriever):
    hits = retriever.search("login", filters={"repository": "org/app"})
    assert [x.document_id for x in hits] == ["ISSUE-2"]


def test_top_k(retriever):
    assert len(retriever.search("login token timeout", top_k=1)) == 1


@pytest.mark.parametrize("top_k", [0, -1, True, 1.5])
def test_invalid_top_k(retriever, top_k):
    with pytest.raises(ValueError, match="top_k"):
        retriever.search("login", top_k=top_k)


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        LexicalRetriever([
            SearchDocument("x", "first", {}),
            SearchDocument("x", "second", {}),
        ])


def test_ties_are_stable():
    retriever = LexicalRetriever([
        SearchDocument("b", "timeout issue", {}),
        SearchDocument("a", "timeout issue", {}),
    ])
    assert [x.document_id for x in retriever.search("timeout")] == ["a", "b"]
```

Illustrative ranking for query `login token`: a document containing both
terms scores 2; documents containing only one term score 1; no-match
documents are excluded. Ties sort by stable ID. This is deterministic
behavior, not a claim of optimal relevance.

Run:

``` bash
python -m pytest tests/code_retrieval/test_lexical_search.py
```

Add tests for exact title/body mapping, duplicate records, metadata
filters, no matches, ties, and invalid top-k. The shown fixture has one
content field; add separate title/body weighting only if the actual
contract requires it.

# Section 11 --- Implement Semantic Retrieval, If Required

Semantic search is blocked until the ML Engineer provides the approved
embedding interface, model/version, input limits, output dimension/type,
normalization, batch behavior, lifecycle, and failure semantics. Do not
invent a model name, download a large model, or add a paid provider.

``` mermaid
flowchart LR
    D[Normalized records] --> P[Approved document text preparation]
    P --> E[Approved embedding interface]
    E --> V[Vectors linked to stable IDs]
    Q[User query] --> QP[Validate query]
    QP --> QE[Same approved embedding interface]
    QE --> S[Similarity/candidate search]
    V --> S
    S --> F[Approved filters/access scope]
    F --> R[Ranked results]
```

Checks to implement once the interface exists:

-   Query and document vectors use compatible model versions and
    preprocessing.
-   Dimensions and dtype are validated.
-   Cosine similarity uses normalized vectors or divides by norms
    correctly.
-   Zero/non-finite vectors are handled.
-   Stable IDs are stored alongside vectors.
-   Model/index failures are explicit.
-   Access restrictions are applied before results are exposed.
-   Unit tests mock the embedding interface; live services are opt-in
    integration tests.

**Checkpoint:** No semantic implementation should be merged until the
embedding contract and index strategy are approved.

# Section 12 --- Implement Hybrid Retrieval and Reranking, If Required

Use hybrid search only if relevance evaluation shows that the approved
baseline misses important use cases. A conceptual pipeline:

``` mermaid
flowchart TD
    Q[Validated query] --> L[Lexical candidates]
    Q --> S[Semantic candidates]
    L --> U[Union and deduplicate by stable ID]
    S --> U
    U --> F[Approved filters and access scope]
    F --> C[Rank fusion]
    C --> R{Reranker justified?}
    R -- No --> O[Top-k results]
    R -- Yes --> RR[Approved reranker]
    RR --> O
```

Raw lexical and semantic scores may not share a scale. Rank-based fusion
(e.g., reciprocal-rank fusion) avoids direct score-scale comparison but
discards some score magnitude. Normalized-score fusion requires a
documented normalization method and evaluation-tuned weights. Reranking
adds latency and cannot recover candidates omitted by both retrieval
paths.

No actual embedding/search interfaces or fusion weights are supplied, so
a project-specific hybrid implementation would be fabricated. Establish
lexical-only and/or semantic-only baselines first. If hybrid is
approved, test duplicate candidate removal, deterministic fusion,
filters, top-k, missing/non-finite scores, reranker failures, and
compare all strategies on the same labelled query set.

# Section 13 --- Implement the Public Retrieval Interface

Document the actual function/class name, import path, constructor,
query/filter/top-k arguments, result schema, score semantics, error
behavior, configuration, dependency injection, and lifecycle. Keep
retrieval independently testable from FastAPI and Streamlit.

Illustrative usage matching Section 10 only:

``` python
from packages.code_retrieval.lexical_search import LexicalRetriever, SearchDocument

retriever = LexicalRetriever([
    SearchDocument(
        document_id="ISSUE-42",
        content="Login fails after token refresh",
        metadata={"repository": "org/example", "state": "open"},
    ),
])
results = retriever.search(
    "token refresh", top_k=5, filters={"repository": "org/example"}
)
for result in results:
    print(result.document_id, result.score)
```

Do not print private issue content in production logs. Replace the
import path with the real package interface.

Interface checklist: - \[ \] API consumer imports only public symbols. -
\[ \] Return schema and score semantics are documented. - \[ \] Filters
and top-k are validated. - \[ \] Error behavior is stable. - \[ \] No
HTTP/UI dependencies leak into retrieval. - \[ \] API owner reviewed the
contract. - \[ \] Contract tests verify fields and types.

# Section 14 --- Error Handling, Configuration, and Logging

  -----------------------------------------------------------------------
  Failure                 Retrieval behavior      Consumer behavior
  ----------------------- ----------------------- -----------------------
  Invalid                 Documented validation   API maps to approved
  query/filter/top-k      exception               client error

  Empty index             Contract-defined empty  Consistent user-facing
                          result or not-ready     behavior
                          error                   

  Missing/corrupt index   Clear load error; do    Documented
                          not silently create an  rebuild/restore
                          empty production index  

  Embedding unavailable   Explicit dependency     Documented
                          error/approved fallback timeout/error mapping

  Timeout/resource        Bound work and fail     Temporary failure
  exhaustion              predictably             response

  Unsupported config      Fail during             Operator corrects
                          validation/startup      config
  -----------------------------------------------------------------------

Do not convert every failure to an empty list; that disguises outages.
Use existing configuration and logging conventions. Log aggregate
duration, result count, operation, and sanitized error category. Do not
log credentials, complete private issue bodies, or raw query text unless
policy explicitly permits it.

Illustrative aggregate logging:

``` python
import logging

logger = logging.getLogger(__name__)


def log_search_completion(*, duration_ms: float, result_count: int) -> None:
    logger.info(
        "retrieval_search_completed duration_ms=%.2f result_count=%d",
        duration_ms,
        result_count,
    )
```

Test invalid inputs, missing/corrupt index, mocked model failures,
timeouts, and invalid configuration where applicable. Assert exception
types and safe messages, not volatile stack traces.

# Section 15 --- Retrieval Evaluation and Relevance Testing

Correctness tests establish contract behavior; relevance evaluation
measures whether returned records help users.

-   **Precision@k:** fraction of top-k results that are relevant.
-   **Recall@k:** fraction of all known relevant records that appear in
    top-k.
-   **MRR:** average reciprocal rank of the first relevant result.
-   **NDCG@k:** rewards relevant items near the top and supports graded
    relevance.
-   **Latency:** response time under documented conditions.
-   **Index size/memory/build time:** operational cost, not relevance.

Illustrative example: query Q1 has relevant IDs `{A, C}` and returns
`[A, B, C]`. Precision@3 = 2/3; Recall@3 = 2/2 = 1; reciprocal rank of
the first relevant result = 1. These are sample calculations, not ORDO
results.

Metric helpers for binary relevance:

``` python
from collections.abc import Sequence, Set


def precision_at_k(ranked_ids: Sequence[str], relevant_ids: Set[str], k: int) -> float:
    if k < 1:
        raise ValueError("k must be positive")
    top = ranked_ids[:k]
    return sum(item in relevant_ids for item in top) / len(top) if top else 0.0


def recall_at_k(ranked_ids: Sequence[str], relevant_ids: Set[str], k: int) -> float:
    if k < 1:
        raise ValueError("k must be positive")
    if not relevant_ids:
        return 0.0
    return sum(item in relevant_ids for item in ranked_ids[:k]) / len(relevant_ids)


def reciprocal_rank(ranked_ids: Sequence[str], relevant_ids: Set[str]) -> float:
    for rank, item in enumerate(ranked_ids, start=1):
        if item in relevant_ids:
            return 1.0 / rank
    return 0.0
```

Test empty rankings, empty relevant sets, `k` larger than the result
list, and invalid `k`. If no labelled set exists, create a small
synthetic or manually reviewed set with known relevant IDs. Do not
fabricate labels or thresholds.

``` mermaid
flowchart TD
    A[Representative queries] --> B[Review relevant records]
    B --> C[Version dataset/corpus]
    C --> D[Run baseline]
    D --> E[Compute agreed metrics and latency]
    E --> F[Review failures]
    F --> G[Change ranking/query logic]
    G --> H[Regression evaluation]
    H --> I[Record trade-offs and limitations]
```

Ask the Team Lead/product owner to define acceptance thresholds. Report
strategy, dataset/corpus version, environment, metrics, latency
methodology, and limitations.

# Section 16 --- Testing Strategy

Use the repository's existing test framework. Test only implemented
modules; the sample tree is not mandatory.

``` text
tests/code_retrieval/
  test_query_processor.py
  test_document_mapper.py
  test_index_manager.py
  test_lexical_search.py
  test_semantic_search.py
  test_hybrid_search.py
  test_ranker.py
  test_retriever.py
  test_contracts.py
  test_security_filters.py
```

Minimum coverage: normal/empty/invalid queries, boundary lengths,
Unicode, missing metadata, duplicate IDs, ranking and stable ties, empty
results, top-k, filters, updates/deletions, index reload/failure, mocked
model failures, contract compatibility, repository isolation, and log
hygiene where applicable.

If pytest is confirmed:

``` bash
python -m pytest tests/code_retrieval/test_query_processor.py
python -m pytest tests/code_retrieval
python -m pytest
```

Ordinary unit tests must not require GitHub credentials, network access,
or paid model APIs. Mock external dependencies. Keep live integration
tests separately labelled and opt-in. When a test fails: read the
traceback, verify interpreter/dependencies, run the focused test,
compare with baseline, identify code/fixture/environment/contract cause,
fix the root cause, add regression coverage, and rerun focused then full
tests. Do not suppress failures to get a green suite.

# Section 17 --- Integration With Other ORDO Components

## Data ingestion

Confirm authoritative schema, stable IDs, metadata, null behavior,
update/delete semantics, and how records are delivered. Test with
sanitized representative records. Do not edit ingestion code without
approval.

## ML engine

Confirm whether embeddings are required; agree interface, model/version,
dimensions, normalization, batching, lifecycle, failure behavior, and
test mocks. Do not duplicate model loading/training.

## FastAPI

Agree request/response schema, validation ownership, exception-to-HTTP
mapping, dependency injection, caller identity, authorization scope,
pagination, and timeouts. Keep HTTP concerns in the API layer unless
repository architecture says otherwise.

## Streamlit/UI

UI should consume results through the approved API/application
interface. It should not duplicate ranking or load the index/model
unless explicitly assigned. Agree which title, repository, state,
snippet, URL, and score fields are actually available.

## Shared contracts

Document mismatches, propose the smallest change, identify the owner,
obtain approval, update contract tests, and coordinate consumers. Do not
silently change shared schemas.

``` mermaid
flowchart LR
    ING[Ingestion-owned records] -->|approved schema| RET[Retrieval package]
    ML[ML-owned embeddings] -. optional .-> RET
    RET -->|stable result contract| API[API backend]
    API --> UI[UI consumer]
    SH[Shared contracts / Team Lead] --- RET
    SEC[Security/privacy review] --- RET
```

Checklist: Team Lead approves strategy and shared changes; Data Engineer
confirms schema/updates; ML Engineer confirms embeddings if used; API
Engineer confirms contract/errors/auth; Web Engineer confirms UI fields;
Security Reviewer confirms privacy/access; DevOps confirms
runtime/CI/persistence. Isolated package tests do not prove integration.

# Section 18 --- Performance and Scalability

Measure before optimizing. Record corpus size and text-size
distribution, index build/rebuild time, median/p95 query latency when
sample volume supports it, throughput if required, memory and index
size, embedding cost/throughput if applicable, and refresh delay.
Include dataset version, hardware/runtime, configuration, and
measurement method. Do not invent benchmark numbers.

Practical process: 1. Freeze a representative sanitized corpus and query
set. 2. Warm up if normal runtime includes warm-up. 3. Run repeated
queries and record `time.perf_counter()` durations. 4. Report median/p95
with sample-size caveats. 5. Measure build time, memory, and index size
separately. 6. Repeat after a change under comparable conditions. 7.
Compare relevance and latency together.

Batching, incremental indexing, caching, and approximate
nearest-neighbor search are options only when the measured bottleneck
justifies them. Define cache invalidation, access scope, and retention
before caching. Avoid distributed infrastructure without evidence.

# Section 19 --- Security, Privacy, and Data Handling

-   Do not assume all repositories/issues are public.
-   Enforce the approved authorization contract; a UI filter is not
    access control.
-   Prevent cross-repository results, snippets, counts, and cache
    leakage.
-   Treat issue text as untrusted data; it may contain prompt-injection
    instructions or malicious links.
-   Validate filter names/types and parameterize backend queries.
-   Never commit credentials or private `.env` files.
-   Avoid sensitive query/content logging.
-   Protect indexes and backups; embeddings may still expose sensitive
    information.
-   Follow approved retention/deletion rules for indexes, caches, and
    temporary files.
-   Do not send private issue content to an external embedding/reranking
    service without approval.
-   Do not invent platform authorization policy; coordinate with the
    responsible owner.

Security tests should use synthetic records and verify repository
isolation, unknown-filter behavior, safe logging, and stale/deleted
record handling. Document unresolved ownership explicitly.

# Section 20 --- Documentation

Update actual approved documentation paths only. Relevant topics include
package purpose/status, installation, supported runtime, configuration,
public interface, index lifecycle, search examples, filters, test
commands, evaluation, troubleshooting, limitations, and integration
requirements.

README template:

``` markdown
# ORDO Code Retrieval
## Purpose
Describe the confirmed retrieval target and supported use cases.
## Status
List implemented strategies; identify experimental/deferred features.
## Inputs and outputs
Link to the authoritative source schema and public result contract.
## Installation and configuration
Use actual repository commands; document only implemented settings.
## Usage
Provide a minimal example using the actual public import path.
## Index lifecycle
Document build/update/delete/reload/recovery only if implemented.
## Testing and evaluation
Give reproducible commands, dataset version, metrics, and limitations.
## Security and privacy
Document repository scope, logging, storage, and retention assumptions.
## Limitations and troubleshooting
List known gaps and approved recovery steps.
```

Do not describe unimplemented semantic/hybrid search as available.
Ensure commands and examples match real code and are reviewed with the
PR.

# Section 21 --- Troubleshooting Guide

  --------------------------------------------------------------------------------------------------
  Problem            Likely cause                           Diagnostic check  Resolution
  ------------------ -------------------------------------- ----------------- ----------------------
  No results         Empty index, wrong field mapping,      Run known fixture Verify schema,
                     query mismatch                         query; inspect    indexing,
                                                            sanitized         normalization
                                                            count/mapping     

  Bad ranking        Tokenization/weighting/filter/fusion   Run labelled      Fix logic and add
                     issue                                  ranking fixtures  regression

  Duplicate results  Unstable IDs or duplicate source       Inspect candidate Deduplicate by
                     records                                IDs               approved stable ID

  Index load fails   Missing path, permission, corruption,  Check             Restore/rebuild
                     version mismatch                       path/version and  documented index
                                                            sanitized logs    

  Embedding failure  Model unavailable or dimensions        Test approved     Fix config or explicit
                     mismatch                               interface         failure handling
                                                            independently     

  CI tests fail      Runtime/dependency mismatch or         Compare CI and    Reproduce; fix
                     non-isolated tests                     local commands    environment/test
                                                                              isolation

  Cross-repository   Filter/auth scope applied too late     Run isolation     Enforce approved scope
  leak                                                      tests             before returning data

  Slow search        Unbounded corpus/candidates or rebuild Profile build and Optimize measured
                     per query                              query separately  bottleneck

  Update duplicates  Unstable upsert key                    Repeat upsert     Use authoritative
  entry                                                     with same ID in   stable ID
                                                            test              

  Deleted issue      Index/cache not refreshed              Test              Implement approved
  still appears                                             source-to-index   cleanup/invalidation
                                                            deletion path     

  Unicode fails      Query/document normalization differs   Test both paths   Align normalization
                                                            with Unicode      and add regression
                                                            fixtures          

  Empty index looks  Failure hidden as empty collection     Inspect           Fail clearly or report
  healthy                                                   startup/error     not-ready
                                                            path              

  Import failure     Example path differs from package      Inspect packaging Follow established
                     layout                                 and neighboring   import conventions
                                                            tests             

  Unknown filter     No allowlist/validation                Test unknown key  Reject or document
  ignored                                                                     behavior
  --------------------------------------------------------------------------------------------------

Do not expose private query text or issue content while diagnosing.
Attach sanitized logs and exact commands to the ticket/PR.

# Section 22 --- Final Verification

Complete sequentially and record actual results.

## Implementation and contracts

-   [ ] Repository structure and ownership inspected.
-   [ ] Approved architecture and retrieval target documented.
-   [ ] Public contract agreed.
-   [ ] Mapping uses authoritative schema and stable IDs.
-   [ ] Search, filters, ranking, empty/invalid behavior match
    requirements.
-   [ ] Index lifecycle tested if an index exists.
-   [ ] Semantic/hybrid components only included if approved.

## Tests and evaluation

-   [ ] Focused and full tests run.
-   [ ] Relevant contract/integration tests run.
-   [ ] Relevance evaluation run if required, with dataset/version and
    real metrics.
-   [ ] Performance tests run if required.
-   [ ] Security/privacy tests run for implemented scope.
-   [ ] Ordinary tests do not require live external services.

## Quality and Git

-   [ ] Formatter/linter run if configured.
-   [ ] No secrets/private data staged.
-   [ ] No unrelated files changed.
-   [ ] Documentation matches code.
-   [ ] Working tree and staged diff reviewed.
-   [ ] Feature branch based on approved base.
-   [ ] PR lists tests, limitations, dependencies, and unresolved
    issues.

Commands from repository root:

``` bash
git status --short
git diff --check
git diff --stat
git diff
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Use actual repository test/format/lint commands. `git diff --check`
catches whitespace errors; it does not prove correctness.

Verification record:

``` markdown
- Branch / base:
- Tests and exit statuses:
- Formatter/linter and exit statuses:
- Integration tests/environment:
- Evaluation dataset/version and metrics:
- Security/privacy checks:
- Docs updated:
- Known failures:
- Blockers and owners:
```

If a mandatory contract, test, authorization decision, or integration
remains unresolved, mark the work partial/blocked.

# Section 23 --- Pull Request and Handover

## Branch workflow

Proposed branch: `feature/code-retrieval/issue-search-and-ranking`. Use
it only if it follows team conventions. Use `develop` only if the Team
Lead/repository docs confirm it as the approved integration branch. If
the base branch is unknown, stop and ask.

``` bash
git status --short
git remote -v
git fetch origin
git switch <TEAM_APPROVED_BASE_BRANCH>
git pull --ff-only origin <TEAM_APPROVED_BASE_BRANCH>
git switch -c feature/code-retrieval/issue-search-and-ranking
git branch --show-current
```

Do not overwrite uncommitted changes. `fetch` updates remote-tracking
refs; `pull --ff-only` refuses non-fast-forward integration. If the
feature branch already exists, inspect it rather than overwriting it.

Stage only approved paths:

``` bash
git add <APPROVED_RETRIEVAL_FILES>
git diff --cached --check
git diff --cached
git commit -m "feat(code-retrieval): implement issue retrieval and ranking"
git status --short
git push -u origin feature/code-retrieval/issue-search-and-ranking
```

Replace placeholders with real paths. Do not use `git add .`
indiscriminately or invent a remote URL. Follow team merge/rebase
policy; coordinate conflicts in schemas/access logic; never force-push a
shared branch without authorization.

## PR title

`feat(code-retrieval): implement issue retrieval and ranking`

Adjust to the actual scope; do not imply semantic/hybrid search exists
if only a baseline was implemented.

## PR template

``` markdown
## Summary
- Retrieval behavior and strategy:
- Explicitly out of scope:

## Contracts and decisions
- Retrieval target / source schema / stable ID:
- Public interface and filters:
- Approvals:

## Implementation
- Files changed:
- Index/config/dependency changes:
- Error handling/logging:

## Tests
- Focused/full tests and results:
- Integration/contract tests:
- Format/lint:
- Environment and exact commands:

## Relevance evaluation
- Dataset/version:
- Metrics and baseline comparison:
- Limitations or reason not run:

## Security/privacy
- Repository isolation:
- Logging/storage/retention:
- Reviewer:

## Known limitations and blockers
- Decision, owner, follow-up issue:

## Rollback/recovery
- Revert and index rebuild steps, if relevant:
```

Reviewer checklist: architecture fits repo; schema/IDs are real;
filters/access safe; ranking deterministic; dependencies approved;
failures explicit; tests cover edge cases; evaluation genuine; no
sensitive data committed; docs accurate; ownership boundaries respected.

Handover: - **Team Lead:** strategy, acceptance criteria, blockers and
follow-ups. - **Data Engineer:** schema, IDs, update/delete semantics. -
**ML Engineer:** embedding interface/version and reindex requirements if
applicable. - **API Engineer:** public contract, errors, auth context,
integration test. - **Web Engineer:** result fields and empty/error
behavior. - **Security Reviewer:** isolation, logs, storage and
retention. - **DevOps/MLOps:** runtime, CI, persistence,
deployment/rebuild procedure.

# Section 24 --- Final Definition of Done

## Implementation complete

-   [ ] Existing functionality inspected before adding code.
-   [ ] Retrieval target and strategy approved.
-   [ ] Authoritative schema and public contract documented.
-   [ ] Stable IDs, mapping, filters, ranking and errors match contract.
-   [ ] Indexing/persistence only where needed and lifecycle tested.
-   [ ] No duplicate model loading or unrelated refactoring.

## Tests complete

-   [ ] Normal, empty, invalid, boundary, and Unicode inputs covered.
-   [ ] Ranking, filters, tie-breaking, duplicate behavior and top-k
    covered.
-   [ ] Update/delete/reload tested if applicable.
-   [ ] Contract/integration tests pass.
-   [ ] Tests are reproducible and mock external dependencies.
-   [ ] No meaningful failures suppressed.

## Relevance evaluation complete, if required

-   [ ] Queries and relevance labels approved/reviewed.
-   [ ] Dataset/corpus version recorded.
-   [ ] Metrics are from actual runs.
-   [ ] Baseline comparisons and limitations documented.
-   [ ] No invented benchmark or pass threshold.

## Integration complete

-   [ ] Data schema confirmed by owner.
-   [ ] ML contract confirmed if used.
-   [ ] API interface/errors/auth scope reviewed.
-   [ ] UI/application consumption path confirmed.
-   [ ] Integration evidence exists or blockers are explicit.

## Documentation complete

-   [ ] Setup, commands, interface, configuration and limitations match
    code.
-   [ ] Evaluation/testing instructions are reproducible.
-   [ ] Rebuild/recovery documented if relevant.

## Security/privacy complete

-   [ ] No secrets/private data committed.
-   [ ] Repository scope/access restrictions reviewed.
-   [ ] Logging and storage follow policy.
-   [ ] Untrusted issue content treated as data, not trusted
    instructions.

## Git/PR complete

-   [ ] Approved base branch and scoped commits.
-   [ ] Staged diff contains intended files only.
-   [ ] Checks run and reported honestly.
-   [ ] PR includes implementation, evidence, limitations and reviewers.

## Handover complete

-   [ ] Team Lead receives final status.
-   [ ] Cross-team dependencies confirmed or assigned.
-   [ ] Limitations, follow-ups, and owners listed.
-   [ ] Rollback/rebuild guidance supplied if relevant.

A mandatory unresolved contract, test, security decision, or integration
dependency means the feature is **not fully complete**.

# Appendix A --- Quick inspection commands

``` bash
git status --short
git branch --show-current
git branch -a
git log -5 --oneline
git remote -v
```

Windows CMD: `dir`, `tree /F`\
PowerShell: `Get-ChildItem -Force`\
macOS/Linux: `find . -maxdepth 3 -type f -not -path './.git/*' | sort`

Inspect repository instructions before running tests, formatters,
linters, or build commands.

# Appendix B --- Decisions that must not be guessed

  -------------------------------------------------------------------------
  Decision                  Evidence/owner          If missing
  ------------------------- ----------------------- -----------------------
  Retrieval target          Requirements/Team Lead  Stop and clarify

  Base branch               Team Lead/repository    Do not create branch
                            docs                    yet

  Source schema and stable  Data Engineer/source    Do not finalize mapper
  ID                        code                    

  Embedding interface/model ML Engineer             Do not implement
                                                    semantic search

  API contract              API Engineer/shared     Do not invent response
                            schema                  fields

  Authorization/retention   Security/platform owner Do not expose results
                                                    beyond approved scope

  Strategy and evaluation   Team Lead/product owner Record options; don't
  thresholds                                        invent targets

  Persistence/service       Measured requirements   Prefer existing
                            and deployment          simplest viable
                            constraints             approach

  CI commands               Repository workflows    Inspect; don't guess
  -------------------------------------------------------------------------

# Appendix C --- Honest status vocabulary

-   **Implemented:** code exists in the branch.
-   **Unit-tested:** named tests were run and passed in the recorded
    environment.
-   **Integration-tested:** named components were exercised together.
-   **Evaluated:** metrics were calculated from the named labelled
    dataset.
-   **Reviewed:** named owner approved the contract/change.
-   **Blocked:** a required decision/dependency is unavailable.
-   **Not run:** a check was not executed, with reason.
-   **Proposed / illustrative:** not yet verified repository behavior.

Do not use "production-ready" as a synonym for "tests pass." Production
readiness also depends on the project's operational, security,
performance, deployment, and ownership requirements.
