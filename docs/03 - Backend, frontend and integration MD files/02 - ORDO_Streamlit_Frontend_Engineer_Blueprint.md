# ORDO Streamlit Frontend Engineer Implementation Blueprint

**Deliverable:** `ORDO_Streamlit_Frontend_Engineer_Blueprint.md`\
**Project:** ORDO --- AI-powered GitHub Issue Intelligence Platform\
**Role:** Streamlit Frontend Engineer\
**Status:** Implementation manual for a repository that has not yet been
created or inspected

> **Important project status:** The ORDO repository has not been
> supplied in this conversation, and the user has stated that the
> repository does not exist yet. Therefore, no repository structure,
> branch, dependency versions, API endpoint, request schema, response
> schema, authentication mechanism, or deployment target can be treated
> as confirmed. This manual separates mandatory engineering procedure
> from proposed examples. The scaffold below deliberately does not
> invent a search endpoint or a response schema. Once the repository and
> approved API contract exist, replace the marked integration
> placeholders before implementing production search behavior.

------------------------------------------------------------------------

## How to use this manual

Follow the phases in order. Do not skip contract approval because a UI
mockup looks plausible. The reference paths below assume the team
eventually approves `apps/web/` as the frontend location; they are
proposals, not claims about an existing repository.

Each major phase includes an objective, prerequisites, working
directory, files, implementation, explanation, commands, expected
result, tests, troubleshooting, and a completion checkpoint. Where no
API contract is known, the checkpoint is to obtain and approve it---not
to guess.

## Section 1 --- Role Overview

### Objective

Build a maintainable Streamlit user interface that presents ORDO's
approved GitHub issue search and intelligence capabilities and delegates
retrieval, ranking, and ML work to the backend.

### Responsibilities

The frontend engineer is responsible for: - Inspecting the repository
and product requirements before changing files. - Confirming the
approved user workflows and design direction with the Team Lead. -
Implementing Streamlit page layout, navigation, form controls, results,
and status/error feedback. - Calling approved backend endpoints through
a testable API client. - Mapping documented response fields into
readable UI elements. - Managing reruns and per-session state
correctly. - Writing frontend unit/UI tests and coordinating
contract/integration tests. - Maintaining frontend configuration and
documentation. - Following branch, review, security, and handover
procedures.

### Boundaries

The frontend displays backend results; it must not recreate retrieval
algorithms, rank issues independently, call model APIs directly unless
explicitly approved, or make up intelligence when an endpoint is
unavailable. The API Engineer owns endpoint paths and schemas. The Code
Retrieval Engineer owns retrieval semantics. The ML Engineer owns model
outputs. The Security/Privacy Reviewer approves handling of secrets and
private issue content. The Team Lead approves requirements, base branch,
and shared integration decisions.

### Expected deliverables

1.  A working Streamlit entry point and navigation appropriate to
    approved requirements.
2.  A dedicated API client with timeouts and safe error mapping.
3.  Search controls and result views only for confirmed contracts.
4.  Clear loading, empty, validation, and error states.
5.  Unit/UI tests that do not require live external services.
6.  Contract/integration verification notes.
7.  Frontend README and configuration example.
8.  A reviewed feature branch and pull request with honest test results.
9.  A handover note listing completed work, assumptions, blockers, and
    owners.

### Definition of done

Done means approved requirements are implemented against approved
contracts, tests and checks have been run and reported accurately, no
secrets or unapproved private data are exposed, documentation matches
behavior, and unresolved dependencies are visible. A page that merely
launches is not production-ready.

## Section 2 --- Application Architecture

### Proposed architecture (confirm against the eventual repository)

``` mermaid
flowchart TD
    U[User] --> UI[Streamlit Dashboard]
    UI --> FORM[Approved Search and Filter Controls]
    FORM --> CLIENT[Frontend API Client]
    CFG[Frontend Configuration] --> CLIENT
    CLIENT --> API[FastAPI Backend]
    API --> RET[Code Retrieval Package, if integrated]
    API --> ML[ML Engine, if integrated]
    RET --> API
    ML --> API
    API --> CLIENT
    CLIENT --> VALID[Contract-aligned response handling]
    VALID --> VIEW[Results and approved insights UI]
    VIEW --> U
    TEST[Unit/UI Tests with mocked client] --> UI
    TEST --> CLIENT
```

The retrieval and ML boxes are conditional until the backend
architecture confirms them. The Streamlit layer should not import
internal backend packages merely to bypass API contracts.

### Proposed frontend responsibilities

-   **Entry point:** initializes page configuration, session state,
    navigation, and top-level error handling.
-   **Page modules:** organize approved user workflows.
-   **Reusable components:** render repeated UI patterns without
    embedding API logic.
-   **API client:** owns HTTP communication, timeouts, status-code
    handling, and transport errors.
-   **Configuration:** reads non-secret settings from environment and
    approved secret stores.
-   **Session state:** retains user interaction state for one Streamlit
    session.
-   **Presentation mapping:** formats documented response fields; does
    not change business meaning.
-   **Tests:** verify request construction, error mapping, rendering,
    and state transitions.

### Search workflow

``` mermaid
flowchart TD
    A[User opens dashboard] --> B[Initialize session state]
    B --> C[Enter query and approved filters]
    C --> D{Input valid?}
    D -- No --> E[Show actionable validation message]
    D -- Yes --> F[Submit form]
    F --> G[Show loading feedback]
    G --> H[API client sends approved request]
    H --> I{Request outcome}
    I -- Valid non-empty response --> J[Render result fields from contract]
    I -- Valid empty response --> K[Show no-results state]
    I -- Timeout/network/status error --> L[Show safe error and recovery action]
    J --> M[Refine query or inspect supported detail]
    K --> M
    L --> M
```

### API request/response flow

``` mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant Client as API Client
    participant API as FastAPI
    User->>UI: Submit approved search form
    UI->>Client: Call contract-specific method
    Client->>API: HTTP request with timeout
    API-->>Client: Status and response body
    Client->>Client: Check status and validate expected shape
    Client-->>UI: Typed/validated result or safe exception
    UI-->>User: Results, empty state, or actionable error
```

### Prerequisites and checkpoint

Before implementing real search, obtain the API contract: endpoint path,
method, query/body schema, response schema, pagination, authentication,
error envelope, and example sanitized responses. **Owner:** API
Engineer; approval by Team Lead and relevant retrieval/ML owners. Do not
progress to a production search UI until this is resolved.

## Section 3 --- Development Environment Setup

### Objective

Create a reproducible local environment using the dependency manager and
Python version approved by the repository.

### Prerequisites

-   Repository URL supplied by the Team Lead or organization.
-   Approved base branch and repository access.
-   Python version and dependency manager documented by the project.
-   Backend run instructions and local API URL, once available.

### Working directory

Open a terminal in the cloned repository root. Do not run the commands
from an unrelated folder.

### Initial commands

Windows PowerShell:

``` powershell
# Verify Python and Git are available
py --version
git --version

# Clone only after receiving the real repository URL
git clone <TEAM_PROVIDED_REPOSITORY_URL>
Set-Location <CLONED_REPOSITORY_DIRECTORY>

git status --short
git branch --show-current
```

macOS/Linux:

``` bash
python3 --version
git --version
git clone <TEAM_PROVIDED_REPOSITORY_URL>
cd <CLONED_REPOSITORY_DIRECTORY>
git status --short
git branch --show-current
```

Do not copy the angle-bracket placeholders literally. Use the URL and
directory supplied by the team. If the repository is not yet created,
stop at this point and ask the Team Lead/organization administrator to
create it and grant access.

### Inspect dependency management first

``` bash
# Run only the commands relevant to files that actually exist
git status --short
```

Inspect `pyproject.toml`, `requirements.txt`, lockfiles, `README.md`,
and CI workflows. Follow the project's declared manager. Do not install
a second manager or create a second dependency list without approval.

If the project explicitly uses a standard Python virtual environment and
requirements file, a proposed Windows setup is:

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the frontend has its own approved requirements file, use that actual
path instead, for example `apps/web/requirements.txt` only if it exists
and is documented. macOS/Linux activation is:

``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Verify

``` bash
python --version
python -m pip --version
python -m pip show streamlit
```

If Streamlit is not installed, that is not by itself permission to add
it. Confirm the approved dependency declaration first, then install
through the project's manager.

### Troubleshooting

-   **`py` not found:** install/use the Python launcher approved for the
    machine or use the documented interpreter path.
-   **Activation blocked in PowerShell:** use the team's approved
    execution-policy procedure or invoke `.venv\Scripts\python.exe`
    directly; do not weaken system policy broadly.
-   **Dependency conflict:** reproduce from the lockfile and report the
    conflict rather than arbitrarily upgrading packages.
-   **Repository URL unknown:** do not invent one. Request the actual
    URL and access.
-   **Backend not running:** follow the backend owner's README; do not
    infer the backend start command.

### Completion checkpoint

Repository exists, correct branch is known, dependency workflow is
documented, Python version matches project policy, and dependency
installation completes without unreviewed changes.

## Section 4 --- UI Requirements and User Workflows

### Objective

Turn approved product requirements and actual API contracts into a small
page inventory.

### Requirements discovery

Ask the Team Lead to identify: - Target user and primary task. - Whether
search, filters, details, insights, or status views are in scope for the
first release. - Which fields users may see for public and private
repositories. - Whether login/authentication is required and how it is
supplied. - Expected result volume and pagination behavior. - Design
references, accessibility requirements, and supported viewport sizes.

Confirm with the API Engineer which endpoint supports each approved
workflow. Treat features listed in the project concept as possible
capabilities, not implemented requirements.

### Proposed page inventory (approve or remove rows)

  -----------------------------------------------------------------------------------------
  Page/area          Purpose            Data source          Owner           Status
  ------------------ ------------------ -------------------- --------------- --------------
  Dashboard shell    Product identity,  Configuration;       Frontend + API  Proposed
                     navigation, API    optional health      Engineer        
                     status if an       endpoint                             
                     approved health                                         
                     endpoint exists                                         

  Issue Search       Submit a supported Approved search      Frontend +      Blocked on
                     search and show    endpoint and schema  API/Retrieval   contract
                     matching issues                         Engineers       

  Issue Detail       Display approved   Approved detail      Frontend + API  Optional
                     fields for one     endpoint, if present Engineer        
                     issue                                                   

  Insights           Display            Approved insight     Frontend +      Optional
                     backend-produced   endpoint/response,   ML/API          
                     intelligence only  if present           Engineers       

  Diagnostics/help   Explain            Local configuration  Frontend        Optional
                     configuration or   and safe API status                  
                     connection state                                        
                     without exposing                                        
                     secrets                                                 
  -----------------------------------------------------------------------------------------

### User workflow acceptance criteria

For every approved workflow, record: 1. Entry point and user action. 2.
Required inputs and validation rules. 3. Exact endpoint and method. 4.
Request field mapping. 5. Expected response fields and types. 6.
Empty-response behavior. 7. Error cases and recovery copy. 8.
Privacy/access restrictions. 9. Unit and integration test cases. 10.
Acceptance owner.

### Checkpoint

Team Lead approves the page inventory and first-release scope. API and
feature owners approve the relevant contracts. Unapproved features
remain absent or visibly marked as unavailable in internal
planning---not represented as working UI.

## Section 5 --- Visual Design and Layout

### Objective

Deliver a calm, legible dashboard appropriate for a developer
productivity tool.

### Layout principles

-   Use Streamlit-native containers, columns, forms, expanders, and
    status messages first.
-   Establish one clear page title, one primary action, and a
    predictable result area.
-   Keep filters close to the search form and make reset behavior
    explicit.
-   Use cards for a small number of result items with several fields;
    use tables for compact comparisons when the schema and screen width
    support them.
-   Avoid decorative metrics unless their meaning and source are
    defined.
-   Use consistent spacing, restrained color, and readable labels.
-   Use native controls and visible labels for keyboard accessibility.
-   Do not rely on undocumented Streamlit CSS class names.

### Textual layout preview

``` text
┌──────────────────────────────────────────────────────────────┐
│ ORDO — Issue Intelligence                   API: status TBD   │
├─────────────────────┬────────────────────────────────────────┤
│ Navigation          │ Issue Search (only if approved)        │
│                     │ [Enter search query              ]     │
│ Dashboard           │ [Approved filters only]       [Search] │
│ Issue Search        │                                        │
│ Insights (optional) │ Results / empty state / error message  │
│                     │ ┌────────────────────────────────────┐ │
│ Help                │ │ Title and fields returned by API   │ │
│                     │ └────────────────────────────────────┘ │
└─────────────────────┴────────────────────────────────────────┘
```

`API: status TBD` is a design placeholder, not a real status. Only show
a status indicator if an approved endpoint or safe connectivity check
exists.

### Theme and CSS

Prefer a committed `.streamlit/config.toml` only if the repository
approves Streamlit theme configuration. A proposed theme file may look
like this, but color tokens must be aligned with the team's design
system:

``` toml
[theme]
base = "light"
primaryColor = "#3157D5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F4F6FA"
textColor = "#172033"
font = "sans serif"
```

Do not create this file if a shared theme or deployment configuration
already governs the UI. If custom CSS is necessary, keep it in one
clearly named module, scope selectors conservatively, and test after
Streamlit upgrades.

### Visual review checklist

-   [ ] Heading hierarchy is obvious.
-   [ ] Inputs have explicit labels and help text where useful.
-   [ ] Primary action is visually distinct without relying only on
    color.
-   [ ] Long issue titles wrap without hiding controls.
-   [ ] Empty and error states tell users what they can do next.
-   [ ] No fake metrics, fake search results, or fabricated insights
    appear.
-   [ ] Desktop and narrow-width layouts remain usable.
-   [ ] Keyboard focus and contrast are acceptable.

### Checkpoint

Team Lead approves the visual direction; implementation uses supported
Streamlit APIs and does not depend on brittle selectors.

## Section 6 --- Streamlit Project Structure

### Objective

Choose the smallest structure that matches actual application
complexity.

### Proposed reference tree

``` text
apps/
└── web/
    ├── app.py
    ├── config.py
    ├── api_client.py
    ├── components/
    │   ├── header.py
    │   └── result_view.py
    ├── pages/
    │   └── issue_search.py
    ├── utils/
    │   └── formatting.py
    └── README.md
tests/
└── web/
    ├── test_api_client.py
    └── test_app.py
```

Use this tree only if the Team Lead approves `apps/web/` and no existing
convention supersedes it. A small first version may need only `app.py`,
`config.py`, and `api_client.py`.

  -------------------------------------------------------------------------------------------------
  File                                   Responsibility     Inputs/outputs        Status
  -------------------------------------- ------------------ --------------------- -----------------
  `apps/web/app.py`                      Configure page and Session state → UI    Proposed
                                         render shell                             

  `apps/web/config.py`                   Read and validate  Environment/secrets → Proposed
                                         settings           settings              

  `apps/web/api_client.py`               HTTP transport and Approved request →    Proposed
                                         safe errors        decoded response      

  `apps/web/components/header.py`        Shared header, if  Title/status text →   Optional
                                         reused             UI                    

  `apps/web/components/result_view.py`   Render             Validated response →  Blocked on schema
                                         contract-defined   UI                    
                                         result fields                            

  `apps/web/pages/issue_search.py`       Search form and    Inputs/client → UI    Blocked on
                                         results workflow                         contract

  `apps/web/README.md`                   Setup and          Documentation         Proposed
                                         operation                                
                                         instructions                             

  `tests/web/test_api_client.py`         Mocked HTTP        Test fixtures →       Proposed
                                         behavior tests     assertions            

  `tests/web/test_app.py`                UI smoke tests     Streamlit test        Proposed
                                                            harness → assertions  
  -------------------------------------------------------------------------------------------------

### Checkpoint

The actual repository tree and ownership map are reviewed before adding
files. Avoid duplicate modules or placing frontend code in backend-owned
packages.

## Section 7 --- Streamlit Entry Point and Navigation

### Objective

Create a minimal, runnable shell without claiming unsupported product
functionality.

### Prerequisites

-   Approved frontend path and dependency manager.
-   Streamlit version declared by the project.
-   Navigation requirements approved.

### Proposed minimal entry point

**File:** `apps/web/app.py` (create only if this path is approved and
does not conflict with an existing entry point)

``` python
import streamlit as st

st.set_page_config(
    page_title="ORDO",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded",
)

def initialize_session_state() -> None:
    """Initialize only non-sensitive, UI-specific session values."""
    st.session_state.setdefault("last_search_submitted", False)
    st.session_state.setdefault("last_search_error", None)

def render_navigation() -> str:
    """Render approved navigation destinations."""
    pages = ["Dashboard"]
    # Add destinations only after product requirements approve them.
    return st.sidebar.radio("Navigation", pages, label_visibility="visible")

def main() -> None:
    initialize_session_state()
    selected_page = render_navigation()

    st.title("ORDO")
    st.caption("GitHub Issue Intelligence Platform")

    if selected_page == "Dashboard":
        st.info(
            "The dashboard shell is ready. Search and insight workflows "
            "will be enabled after the backend API contracts are approved."
        )

if __name__ == "__main__":
    main()
```

### Explanation

-   `st.set_page_config` must run before other Streamlit UI calls.
-   Session state stores only simple UI flags here; it does not store
    credentials or private issue bodies.
-   Navigation deliberately contains only `Dashboard`. Add pages after
    their requirements are approved.
-   The informational message is an honest development placeholder, not
    a simulated search feature.

### Commands

From the repository root, if the proposed path is adopted and
dependencies are installed:

``` bash
python -m streamlit run apps/web/app.py
```

### Expected result

The local browser opens a minimal ORDO shell. No API request is made and
no backend feature is implied.

### Tests

Run the project's configured test command. If `pytest` and Streamlit's
testing support are approved and installed, a smoke test can be added
after confirming the installed version. Do not add a new testing
dependency without updating the approved dependency manifest.

### Troubleshooting

-   **`File does not exist`:** verify the current directory and approved
    path.
-   **`No module named streamlit`:** install dependencies through the
    project's declared manager.
-   **Page configuration error:** ensure `st.set_page_config` is the
    first Streamlit command.
-   **Navigation target mismatch:** add only approved pages and keep
    labels aligned with product language.

### Completion checkpoint

The shell launches from the documented command, the entry point is
agreed, and no optional feature is presented as complete.

## Section 8 --- Configuration and Secrets Management

### Objective

Load the API base URL and timeouts from an approved configuration
source, without committing credentials.

### Proposed configuration

Use the existing configuration approach if one exists. The following
example uses the Python standard library and avoids assuming
`python-dotenv` is installed.

**File:** `apps/web/config.py`

``` python
from dataclasses import dataclass
import os
from urllib.parse import urlparse

class ConfigurationError(ValueError):
    """Raised when required frontend configuration is invalid."""

@dataclass(frozen=True)
class Settings:
    api_base_url: str
    request_timeout_seconds: float = 10.0
    app_environment: str = "development"

def load_settings() -> Settings:
    raw_url = os.getenv("ORDO_API_BASE_URL", "").strip()
    if not raw_url:
        raise ConfigurationError(
            "ORDO_API_BASE_URL is not configured. Set it using the "
            "approved local or deployment configuration."
        )

    parsed = urlparse(raw_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ConfigurationError(
            "ORDO_API_BASE_URL must be a valid http:// or https:// URL."
        )

    raw_timeout = os.getenv("ORDO_API_TIMEOUT_SECONDS", "10")
    try:
        timeout = float(raw_timeout)
    except ValueError as exc:
        raise ConfigurationError(
            "ORDO_API_TIMEOUT_SECONDS must be numeric."
        ) from exc

    if timeout <= 0:
        raise ConfigurationError(
            "ORDO_API_TIMEOUT_SECONDS must be greater than zero."
        )

    environment = os.getenv("ORDO_ENVIRONMENT", "development").strip()
    return Settings(
        api_base_url=raw_url.rstrip("/"),
        request_timeout_seconds=timeout,
        app_environment=environment or "development",
    )
```

**File:** `.env.example` at the repository root, only if `.env`
configuration is approved:

``` dotenv
# Copy to a local ignored .env file only if the project loads .env files.
ORDO_API_BASE_URL=http://127.0.0.1:8000
ORDO_API_TIMEOUT_SECONDS=10
ORDO_ENVIRONMENT=development
```

This example is not loaded automatically by `os.getenv`. If the project
does not already load `.env` files, set environment variables in the
shell or use the approved deployment secrets/configuration facility. Do
not add a dotenv dependency solely to make the example work without
approval.

**`.gitignore` should include**, subject to existing conventions:

``` gitignore
.env
.streamlit/secrets.toml
```

Do not overwrite the existing `.gitignore`; merge only missing relevant
patterns.

### Configuration commands

PowerShell for the current terminal session:

``` powershell
$env:ORDO_API_BASE_URL = "http://127.0.0.1:8000"
$env:ORDO_API_TIMEOUT_SECONDS = "10"
$env:ORDO_ENVIRONMENT = "development"
```

macOS/Linux:

``` bash
export ORDO_API_BASE_URL="http://127.0.0.1:8000"
export ORDO_API_TIMEOUT_SECONDS="10"
export ORDO_ENVIRONMENT="development"
```

The URL is a placeholder until the API owner confirms the local port. No
credential is required by this example; if authentication is later
approved, follow the Security/Privacy Reviewer's design.

### Verification

Test configuration without printing secrets:

``` bash
python -c "from apps.web.config import load_settings; s=load_settings(); print('API URL configured:', bool(s.api_base_url)); print('Timeout:', s.request_timeout_seconds)"
```

This import command assumes the repository root is on Python's import
path. If package conventions differ, use the project's approved
invocation.

### Checkpoint

Missing or invalid settings fail with a safe message. Secret values
never appear in source, screenshots, logs, or commits.

## Section 9 --- Implement the API Client

### Objective

Separate HTTP transport from Streamlit rendering and avoid inventing
endpoint-specific contracts.

### Contract gate

No actual ORDO API endpoint or response schema has been supplied.
Therefore, this phase implements only a **generic transport layer**, not
a production search method. The API Engineer must approve endpoint
paths, methods, parameters, request/response schemas, authentication,
pagination, and error formats before endpoint-specific methods are
added.

### Proposed dependency decision

Use the project's existing approved HTTP client. If none exists, ask the
API/Team Lead whether Python's `urllib` or an approved library such as
`requests` should be used. The following example uses `urllib` to avoid
adding a dependency.

**File:** `apps/web/api_client.py`

``` python
from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from apps.web.config import Settings

class ApiClientError(RuntimeError):
    """Base class for safe, user-presentable API failures."""

class ApiConnectionError(ApiClientError):
    pass

class ApiTimeoutError(ApiClientError):
    pass

class ApiHttpError(ApiClientError):
    def __init__(self, status_code: int, message: str = "The API request failed."):
        super().__init__(message)
        self.status_code = status_code

class ApiResponseError(ApiClientError):
    pass

class ApiClient:
    """Generic HTTP transport. Add endpoint-specific methods only from an approved contract."""

    def __init__(self, settings: Settings):
        self._settings = settings

    def request_json(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str | int | float | bool] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("API path must be an absolute path beginning with one slash.")

        url = f"{self._settings.api_base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"

        payload = None
        headers = {"Accept": "application/json"}
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(url, data=payload, headers=headers, method=method.upper())

        try:
            with urlopen(
                request,
                timeout=self._settings.request_timeout_seconds,
            ) as response:
                raw = response.read()
        except TimeoutError as exc:
            raise ApiTimeoutError("The API request timed out. Please try again.") from exc
        except HTTPError as exc:
            # Do not forward response bodies: they may contain private/internal details.
            raise ApiHttpError(exc.code) from exc
        except URLError as exc:
            reason = getattr(exc, "reason", None)
            if isinstance(reason, TimeoutError):
                raise ApiTimeoutError(
                    "The API request timed out. Please try again."
                ) from exc
            raise ApiConnectionError(
                "The API could not be reached. Check connectivity and try again."
            ) from exc

        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiResponseError("The API returned an invalid JSON response.") from exc
```

### Important constraints

-   `request_json` is a transport helper, not proof that any path
    exists.
-   Do not pass untrusted full URLs as `path`; only use approved fixed
    endpoint paths.
-   Do not add authentication headers until the approved authentication
    mechanism is documented.
-   Do not automatically retry non-idempotent requests. Add retries only
    after API owner approval and only when safe.
-   A JSON parse success is not schema validation. Endpoint-specific
    response validation must match the approved schema.
-   For private data, review redirect behavior, cache behavior, and
    logging before production use.

### Testing without a live backend

**File:** `tests/web/test_api_client.py` (adapt to actual test layout)

``` python
import json
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from io import BytesIO

import pytest

from apps.web.api_client import (
    ApiClient,
    ApiConnectionError,
    ApiHttpError,
    ApiResponseError,
    ApiTimeoutError,
)
from apps.web.config import Settings

@pytest.fixture
def client():
    return ApiClient(Settings(
        api_base_url="http://127.0.0.1:8000",
        request_timeout_seconds=1,
    ))

def test_request_json_returns_decoded_json(client):
    response = BytesIO(json.dumps({"ok": True}).encode("utf-8"))
    response.status = 200
    response.__enter__ = lambda: response
    response.__exit__ = lambda *args: None

    with patch("apps.web.api_client.urlopen", return_value=response):
        assert client.request_json("GET", "/health") == {"ok": True}

def test_invalid_json_raises_response_error(client):
    response = BytesIO(b"not-json")
    response.status = 200
    response.__enter__ = lambda: response
    response.__exit__ = lambda *args: None

    with patch("apps.web.api_client.urlopen", return_value=response):
        with pytest.raises(ApiResponseError):
            client.request_json("GET", "/health")

def test_http_error_does_not_expose_body(client):
    error = HTTPError(
        "http://127.0.0.1:8000/private",
        500,
        "server error",
        hdrs=None,
        fp=BytesIO(b"internal detail"),
    )
    with patch("apps.web.api_client.urlopen", side_effect=error):
        with pytest.raises(ApiHttpError) as caught:
            client.request_json("GET", "/private")
    assert caught.value.status_code == 500
    assert "internal detail" not in str(caught.value)

def test_connection_error_is_mapped(client):
    with patch(
        "apps.web.api_client.urlopen",
        side_effect=URLError("connection refused"),
    ):
        with pytest.raises(ApiConnectionError):
            client.request_json("GET", "/health")
```

> Test fixture note: depending on Python version and the project's test
> conventions, it may be simpler to mock `urlopen` with a small
> context-manager fake. Keep the test fixture deterministic and verify
> it against the installed Python version before merging.

### Commands

``` bash
python -m pytest tests/web/test_api_client.py -q
```

Run only if `pytest` and the test path are approved and present.

### Expected result

The generic client handles transport errors without exposing raw server
bodies. It does not prove `/health` exists; the test uses a mocked
response.

### Troubleshooting

-   **Import errors:** align package layout and test import paths with
    the real repository.
-   **Mock context-manager errors:** use a purpose-built fake
    implementing `__enter__` and `__exit__`.
-   **Contract unknown:** do not write a search method yet; request the
    schema from the API Engineer.

### Completion checkpoint

Transport tests pass in the actual environment. Endpoint-specific
methods are still blocked until the API contract is approved.

## Section 10 --- Implement Search and Filter Controls

### Objective

Implement only controls whose fields and semantics are confirmed by the
approved search contract.

### Contract required before coding

Record each approved item:

  -----------------------------------------------------------------------
  Contract item           Required decision       Owner
  ----------------------- ----------------------- -----------------------
  Search endpoint         Exact path and HTTP     API Engineer
                          method                  

  Query input             Parameter/body field,   API + Team Lead
                          type, length and        
                          empty-query behavior    

  Filters                 Supported fields and    API + Retrieval
                          allowed values          Engineer

  Result limit            Allowed range and       API Engineer
                          default                 

  Sorting/ranking         Supported options and   Retrieval Engineer
                          semantics               

  Response                Exact schema and        API Engineer
                          empty-result            
                          representation          

  Errors                  Status codes and safe   API Engineer
                          error contract          

  Access                  Public/private          Security Reviewer + API
                          repository              Engineer
                          authorization           
  -----------------------------------------------------------------------

### Implementation rule

Do not implement repository, state, label, sort, or limit controls
merely because they are common in issue search. They must map to real
backend parameters. Once approved, use a Streamlit `st.form` so the
request is sent on submission, not on every rerun.

### Generic interaction pattern

The final form must call a contract-specific client method such as
`client.search_issues(...)` **only after that method and its schema are
implemented from the approved contract**. Do not paste a guessed method
or response mapping into production.

``` python
# Pattern only — not a complete feature until the contract is approved.
with st.form("issue_search_form"):
    query = st.text_input("Search query")
    submitted = st.form_submit_button("Search")

if submitted:
    if not query.strip():
        st.warning("Enter a search query.")
    else:
        # Replace with the approved client method and exact schema.
        st.error("Search is not enabled: the API contract is pending approval.")
```

This pattern intentionally does not call a guessed endpoint. Replace the
last line only after contract approval.

### Required behavior

1.  Initialize defaults that match the contract.
2.  Validate input on the frontend for usability; backend validation
    remains authoritative.
3.  Construct the request only from approved fields.
4.  Show loading feedback while awaiting the request.
5.  Clear or clearly mark old results when a new request begins.
6.  Show a no-results message for a valid empty response.
7.  Show safe, actionable errors for transport/status/schema failures.
8.  Make reset behavior explicit.
9.  Preserve the last successful query only if product requirements
    approve it.
10. Test request mapping and rerun behavior.

### Test plan

-   Empty input does not call the API.
-   A valid submission calls the expected client method exactly once.
-   Filters map to exact approved parameter names.
-   Reset restores approved defaults.
-   A failed request does not masquerade as a successful empty result.
-   Changing a control alone does not trigger a request unless
    explicitly required.

### Completion checkpoint

Search UI is enabled only after contract approval, with tests proving
request mapping and all major states.

## Section 11 --- Session State and Rerun Behavior

### Objective

Make state transitions deterministic and avoid duplicate API calls.

### Proposed lifecycle

``` mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Validating: Submit
    Validating --> Idle: Invalid input
    Validating --> Loading: Valid input
    Loading --> Success: Valid non-empty response
    Loading --> Empty: Valid empty response
    Loading --> Error: API/timeout/schema failure
    Success --> Loading: New submission
    Empty --> Loading: New submission
    Error --> Loading: Retry
    Success --> Idle: Clear/reset
    Empty --> Idle: Clear/reset
    Error --> Idle: Clear/reset
```

### State rules

-   Keep only UI state required to render the current session.
-   Do not store credentials in `st.session_state`.
-   Store the last successful result separately from the latest request
    outcome if the UI intentionally preserves it; label it clearly as
    previous data.
-   When a new query begins, avoid displaying old results as though they
    belong to the new query.
-   Use forms and submit buttons to prevent requests on every widget
    rerun.
-   Avoid mutable global variables for user-specific state.
-   Be deliberate when using `st.cache_data`: cached values may be
    shared across sessions. Never cache private issue results without a
    reviewed user-specific isolation strategy.

### Example state initialization

``` python
import streamlit as st

def initialize_search_state() -> None:
    defaults = {
        "search_status": "idle",
        "search_results": None,
        "search_error": None,
        "submitted_query": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
```

Allowed `search_status` values should be constrained by application
code, for example `idle`, `loading`, `success`, `empty`, and `error`.
The example initializes state only; the real search page must update
transitions around the approved client method.

### Tests and manual verification

-   Submit the same query twice; confirm each intentional submission
    causes one request.
-   Change filters without submitting; confirm no unexpected request
    occurs.
-   Submit a new query after success; confirm old results are cleared or
    clearly marked.
-   Trigger an error then retry; confirm error state is reset on retry.
-   Navigate away and back; verify behavior matches the approved
    persistence requirement.
-   Clear/reset; verify query, filters, and displayed results reset
    consistently.

### Completion checkpoint

State transitions are documented, deterministic, tested, and do not
retain sensitive values unnecessarily.

## Section 12 --- Search Results Display

### Objective

Render only fields present in the approved response schema.

### Schema-driven field inventory

Complete this table after the API Engineer provides a sample response
and schema.

  ------------------------------------------------------------------------------------
  UI field     Exact       Format          Missing-value      Clickable?   Privacy
               response                    behavior                        approval
               path                                                        
  ------------ ----------- --------------- ------------------ ------------ -----------
  Issue title  Pending     Plain text      Contract-defined   Only if      Required
                                           fallback           approved URL 
                                                              exists       

  Repository   Pending     Plain text      Contract-defined   Only if      Required
                                           fallback           approved URL 
                                                              exists       

  State        Pending     Text/tag        Contract-defined   No by        Required
                                           fallback           default      

  Labels       Pending     Compact list    Empty list or      No by        Required
                                           fallback per       default      
                                           schema                          

  Summary      Pending     Plain           Omit or show       No by        Required
                           text/Markdown   unavailable        default      
                           policy                                          

  Relevance    Pending     Numeric format  Omit if absent     No           Retrieval
  score                    defined by                                      owner
                           owner                                           

  Timestamp    Pending     Explicit        Omit if absent     No           Required
                           timezone                                        
                           formatting                                      

  Issue URL    Pending     Validated HTTPS No link if         Yes          Security
                           link if         absent/invalid                  review
                           contract                                        
                           permits                                         
  ------------------------------------------------------------------------------------

These are candidate fields, not confirmed fields.

### Rendering guidance

-   Prefer plain text for untrusted titles and descriptions.
-   Do not render arbitrary HTML from issue content.
-   Validate links before displaying them; use only approved URL schemes
    and destinations.
-   Use `st.dataframe` or a table for compact comparison, and
    cards/expanders for long text.
-   Avoid showing raw model payloads, internal prompts, stack traces,
    tokens, or private metadata.
-   Do not derive a score or summary in the frontend.

### Schema gate

Do not write a production `render_results(response)` function until the
response schema is available. At that point: 1. Validate the response at
the API-client boundary. 2. Normalize only presentation details, not
business meaning. 3. Handle optional/null fields according to the
schema. 4. Add a fixture based on a sanitized, approved example. 5. Test
normal, missing, malformed, and empty cases.

### Completion checkpoint

Every visible field has a source path, formatting rule, privacy
decision, and test.

## Section 13 --- Issue Details and Insights

### Objective

Expose detail and intelligence views only when the backend supplies
approved endpoints and fields.

### Required decisions

-   Is there a detail endpoint, or are details included in search
    results?
-   Does the endpoint accept an issue identifier, repository/issue pair,
    or another key?
-   Which description fields can be shown to which users?
-   Are summaries or related issues generated by the backend?
-   Is relevance metadata safe and meaningful for end users?
-   What happens when an issue is deleted, inaccessible, or no longer
    authorized?
-   How should model-generated content be labelled and caveated?

### Implementation rules

-   Do not fake summaries or related issues.
-   Do not calculate embeddings, ranking, or model predictions in
    Streamlit.
-   Treat issue descriptions and model-generated text as untrusted
    content.
-   If a detail request returns `403` or `404`, show a safe message
    without revealing whether a private issue exists unless the API
    contract explicitly permits that distinction.
-   If insights are unavailable, hide the view or label the feature as
    not enabled in a development-only status---not as an empty
    successful response.

### Test cases

-   Valid detail response.
-   Optional fields absent.
-   Issue no longer available.
-   Access denied.
-   Backend timeout.
-   Malformed response.
-   Generated content contains HTML-like or instruction-like text and is
    rendered safely.

### Completion checkpoint

Feature owners approve the data contract and privacy treatment before
detail or insight views are enabled.

## Section 14 --- Loading, Empty, and Error States

### Objective

Provide accurate and recoverable feedback for each request outcome.

### State mapping

  -------------------------------------------------------------------------------
  Condition                   UI treatment               Recovery
  --------------------------- -------------------------- ------------------------
  Initial page                Explain the next approved  Submit a valid request
                              action                     

  Loading                     `st.spinner` or equivalent Wait; avoid duplicate
                              supported status element   submission

  Valid results               Render schema-defined      Refine query
                              results                    

  Valid empty response        `st.info` or equivalent    Broaden/refine search

  Invalid input               `st.warning`/field-level   Correct input
                              message                    

  API unavailable             Safe connection message    Check
                                                         backend/configuration,
                                                         retry

  Timeout                     Timeout message            Retry or narrow request

  HTTP 4xx/5xx                Safe message based on      Correct input, access,
                              approved mapping           or report service issue

  Invalid JSON/schema         Generic invalid-response   Report request ID if
                              message                    available

  Authentication/permission   Approved access message    Sign in or contact
  failure                                                owner, if applicable

  Unexpected exception        Generic error and          Report safely
                              correlation ID if          
                              available                  
  -------------------------------------------------------------------------------

### Example safe UI handling

``` python
import streamlit as st
from apps.web.api_client import (
    ApiClientError,
    ApiConnectionError,
    ApiTimeoutError,
    ApiHttpError,
)

def show_api_error(exc: ApiClientError) -> None:
    if isinstance(exc, ApiTimeoutError):
        st.warning("The request timed out. Please try again.")
    elif isinstance(exc, ApiConnectionError):
        st.error("ORDO could not reach the API. Check service availability.")
    elif isinstance(exc, ApiHttpError):
        if exc.status_code == 401:
            st.error("Authentication is required.")
        elif exc.status_code == 403:
            st.error("You do not have permission to perform this action.")
        elif exc.status_code == 404:
            st.error("The requested resource is unavailable.")
        else:
            st.error("The API could not complete the request.")
    else:
        st.error("ORDO could not process the request. Please try again.")
```

The authentication copy above is an example mapping; only use it if the
backend's approved status semantics match it. Never print `repr(exc)` or
raw response bodies to users.

### State-flow diagram

``` mermaid
flowchart TD
    A[Submit] --> B[Validate]
    B -->|Invalid| C[Show validation message]
    B -->|Valid| D[Loading]
    D --> E{Outcome}
    E -->|Validated non-empty| F[Render results]
    E -->|Validated empty| G[Show no results]
    E -->|Timeout/network| H[Show connection/timeout message]
    E -->|HTTP error| I[Map approved status safely]
    E -->|Invalid schema| J[Show invalid response message]
    F --> K[Refine or clear]
    G --> K
    H --> K
    I --> K
    J --> K
```

### Tests

Test each branch with mocked responses/exceptions. Confirm no full stack
trace, token, private body, or internal error body appears in the UI.

### Completion checkpoint

Every request outcome has a defined, safe, testable UI state.

## Section 15 --- Reusable UI Components

### Objective

Extract repeated UI only when it improves consistency or testability.

### Candidate components

  ----------------------------------------------------------------------------------------------
  Component         Suggested path                         Parameters          Test strategy
  ----------------- -------------------------------------- ------------------- -----------------
  Header            `apps/web/components/header.py`        Product title;      UI smoke test
                                                           optional approved   
                                                           status              

  Result view       `apps/web/components/result_view.py`   Validated result    Missing/null
                                                           model/list          fields and
                                                                               rendering tests

  Error presenter   `apps/web/components/error_view.py`    Safe mapped error   Status mapping
                                                                               tests

  Formatting        `apps/web/utils/formatting.py`         Typed values        Pure unit tests
  helpers                                                                      

  Search form       `apps/web/components/search_form.py`   Approved filter     Submission and
                                                           metadata/defaults   validation tests
  ----------------------------------------------------------------------------------------------

Do not create a component for every single Streamlit call. Keep API
requests out of presentation-only components, and keep response-schema
validation out of decorative components.

### Example pure helper

``` python
def display_text(value: object, fallback: str = "Not available") -> str:
    """Return a safe, readable text representation for optional scalar fields."""
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback
```

This helper is only for display formatting; do not use it to silently
coerce fields that have strict contract types.

### Checkpoint

Extracted components have stable interfaces and tests. Components are
not coupled to undocumented API shapes.

## Section 16 --- UI Testing

### Objective

Test frontend behavior without requiring GitHub access, a live API, or
paid model inference.

### Strategy

Use the test tools already configured in the repository. If pytest and
Streamlit's `AppTest` are approved and supported by the installed
Streamlit version, use them for UI tests. Keep ordinary unit tests
deterministic and mock the API client/transport.

### Proposed test layout

``` text
tests/
└── web/
    ├── test_api_client.py
    ├── test_config.py
    ├── test_app.py
    ├── test_search_form.py
    ├── test_results.py
    └── test_error_states.py
```

### Configuration tests

``` python
import pytest
from apps.web.config import ConfigurationError, load_settings

def test_missing_api_url_is_rejected(monkeypatch):
    monkeypatch.delenv("ORDO_API_BASE_URL", raising=False)
    with pytest.raises(ConfigurationError):
        load_settings()

def test_invalid_timeout_is_rejected(monkeypatch):
    monkeypatch.setenv("ORDO_API_BASE_URL", "http://127.0.0.1:8000")
    monkeypatch.setenv("ORDO_API_TIMEOUT_SECONDS", "not-a-number")
    with pytest.raises(ConfigurationError):
        load_settings()

def test_valid_settings(monkeypatch):
    monkeypatch.setenv("ORDO_API_BASE_URL", "http://127.0.0.1:8000/")
    monkeypatch.setenv("ORDO_API_TIMEOUT_SECONDS", "3.5")
    settings = load_settings()
    assert settings.api_base_url == "http://127.0.0.1:8000"
    assert settings.request_timeout_seconds == 3.5
```

### UI test pattern

After the actual entry point and installed Streamlit version are
confirmed, use the supported testing API. A typical smoke-test shape is:

``` python
from streamlit.testing.v1 import AppTest

def test_dashboard_shell_renders():
    app = AppTest.from_file("apps/web/app.py").run()
    assert not app.exception
    assert any("ORDO" in title.value for title in app.title)
```

Check the installed version's API and adapt assertions if the UI uses
another layout. Do not treat this example as verified against an unknown
project version.

### Commands

``` bash
python -m pytest tests/web/test_config.py -q
python -m pytest tests/web/test_api_client.py -q
python -m pytest tests/web -q
```

Run only for paths and tools present in the repository. Use the
project's documented full-suite command for CI.

### Testing workflow

``` mermaid
flowchart TD
    A[Change frontend code] --> B[Run focused unit tests]
    B --> C{Pass?}
    C -- No --> D[Fix failure and rerun focused tests]
    D --> B
    C -- Yes --> E[Run UI tests]
    E --> F[Run contract/integration checks in controlled environment]
    F --> G[Run formatter/linter configured by repository]
    G --> H[Manual visual and accessibility review]
    H --> I[Record actual results for PR]
```

### Checkpoint

Tests are isolated from external services, failure cases are covered,
and commands/results are recorded honestly.

## Section 17 --- API Contract and Integration Testing

### Objective

Prove the frontend and FastAPI backend agree on the same interface.

### Contract checklist

-   [ ] Exact endpoint path and HTTP method.
-   [ ] Query parameters and request body.
-   [ ] Required/optional fields and types.
-   [ ] Response schema and nullability.
-   [ ] Empty-result semantics.
-   [ ] Pagination and sort semantics.
-   [ ] Authentication and authorization.
-   [ ] Rate limits and retry rules.
-   [ ] Error status codes and safe error body.
-   [ ] Request timeout and correlation/request ID behavior.
-   [ ] Versioning/backward compatibility.

### Integration procedure

1.  Use a controlled environment and non-sensitive test data.
2.  Start the backend using its own README/owner-approved command.
3.  Confirm the configured API base URL without printing credentials.
4.  Exercise the contract using the API's OpenAPI docs or approved API
    tests.
5.  Run frontend integration tests against the controlled backend.
6.  Test success, empty, validation, authorization, timeout, and
    malformed response behavior where feasible.
7.  Record backend version/commit and test environment.
8.  Report mismatches to the API Engineer; do not modify backend-owned
    files without approval.

### Ownership for mismatch resolution

  -----------------------------------------------------------------------
  Mismatch                Primary owner           Required coordination
  ----------------------- ----------------------- -----------------------
  Wrong                   API Engineer            Frontend Engineer +
  path/method/schema                              Team Lead

  Filter/ranking          Code Retrieval Engineer API Engineer + Team
  semantics                                       Lead

  Insight field/meaning   ML Engineer             API Engineer + Frontend
                                                  Engineer

  Data definition         Data Engineer           API/Retrieval owners

  Auth/privacy behavior   Security/Privacy        API Engineer + Team
                          Reviewer                Lead

  Product behavior        Team Lead               Relevant feature owners
  ambiguity                                       
  -----------------------------------------------------------------------

### Checkpoint

Integration results are recorded and no contract mismatch is silently
papered over in the UI.

## Section 18 --- Visual Quality, Accessibility, and Responsiveness

### Objective

Review usability on desktop and narrower browser windows.

### Checklist

-   [ ] Every input has a visible label.
-   [ ] Controls are usable by keyboard.
-   [ ] Focus indicators remain visible.
-   [ ] Color is not the only way to communicate state.
-   [ ] Text/background contrast is adequate.
-   [ ] Long titles and repository names wrap safely.
-   [ ] Error messages describe the issue and a next step.
-   [ ] Empty/loading states are understandable.
-   [ ] Tables do not force unusable horizontal scrolling on narrow
    screens.
-   [ ] Columns collapse or remain readable at narrower widths.
-   [ ] No content relies on hover alone.
-   [ ] Links have meaningful labels.
-   [ ] No raw HTML from issue content is executed.
-   [ ] UI remains usable at common desktop and mobile-width browser
    sizes.

### Manual visual test procedure

1.  Run the app locally with approved configuration.
2.  Test the default desktop viewport.
3.  Narrow the browser window and inspect columns, controls, and tables.
4.  Use keyboard-only navigation from the top of the page.
5.  Test a long title, missing optional fields, zero results, and each
    error state using fixtures or a controlled test environment.
6.  Confirm no sensitive content appears in terminal logs or error
    messages.
7.  Record issues and screenshots only where project policy permits.

### Checkpoint

Visual and accessibility issues are resolved or documented with an owner
and acceptance decision.

## Section 19 --- Performance and Caching

### Objective

Keep interaction responsive without introducing unsafe shared caching.

### Guidelines

-   Use forms to avoid calling the API on each rerun.
-   Use pagination if the backend supports it; do not load an unbounded
    result set.
-   Avoid expensive transformations inside repeated rendering loops.
-   Measure before optimizing.
-   Cache immutable configuration or public reference data only when
    appropriate.
-   Remember `st.cache_data` can share cached data across users; do not
    cache private issue results without a reviewed isolation strategy.
-   Use a reasonable request timeout.
-   Add retries only when idempotency, rate limits, and error semantics
    are understood.
-   Keep API result sizes and displayed fields within the approved
    contract.

### Verification

Compare request counts and response/render times before and after a
proposed optimization using safe instrumentation. Confirm that a rerun
without a new submission does not repeat the search. For private data,
test that one session cannot see another user's cached response.

### Checkpoint

Every cache has a documented reason, scope, TTL, and privacy review
where needed. No speculative cache is added merely for convenience.

## Section 20 --- Security and Privacy

### Frontend checklist

-   [ ] No real secrets in source, `.env.example`, screenshots, logs, or
    commits.
-   [ ] Actual `.env` and secrets files are ignored by Git.
-   [ ] Privileged GitHub tokens are not embedded in frontend source or
    sent to a user-controlled browser context.
-   [ ] Authentication uses only the approved mechanism.
-   [ ] Private repository results respect backend authorization.
-   [ ] The frontend does not assume all repositories are public.
-   [ ] Issue bodies and generated content are treated as untrusted.
-   [ ] Links are validated and restricted to approved schemes.
-   [ ] Raw API error bodies and stack traces are not shown.
-   [ ] Session state stores no unnecessary secrets or private payloads.
-   [ ] Shared caches do not cross user authorization boundaries.
-   [ ] Logs exclude authorization headers, tokens, full private issue
    bodies, and secrets.
-   [ ] Development and production configuration are separated.
-   [ ] Security-sensitive changes are reviewed by the Security/Privacy
    Reviewer.

### Safe handling rules

The backend must enforce authorization; hiding a UI element is not
access control. Do not expose credentials in query strings. Do not add
client-side authentication assumptions without an approved flow. For any
new credential requirement, stop and obtain the security-approved
design.

### Checkpoint

Security/privacy review is complete for the actual data flow. Any
unresolved risk is a blocker, not a documentation-only footnote.

## Section 21 --- Logging and Diagnostics

### Objective

Help engineers distinguish configuration, frontend, transport, API,
retrieval, and ML failures without exposing sensitive data.

### Diagnostic categories

-   **Configuration:** missing/invalid API URL or timeout.
-   **Connectivity:** DNS, refused connection, unavailable backend.
-   **Timeout:** backend did not respond within the configured timeout.
-   **HTTP status:** backend rejected or failed the request.
-   **Response parsing/schema:** response could not be decoded or did
    not match the contract.
-   **Rendering:** UI could not handle a valid response.
-   **Retrieval/ML:** backend returned a feature-specific failure;
    coordinate with that owner.

### Logging rules

Use the project's established logger if one exists. Log safe metadata
such as operation name, elapsed time, status code, and request ID when
the backend supplies one. Do not log full URLs if they can contain
sensitive query values. Never log access tokens, authorization headers,
full private issue bodies, prompts, or secret values.

### Diagnostic procedure

1.  Reproduce with a non-sensitive query.
2.  Check frontend terminal output.
3.  Check configured API URL presence without printing secret values.
4.  Test the backend using its documented health/diagnostic endpoint if
    one exists.
5.  Compare status and request ID with backend logs, if available.
6.  Route the issue to the correct owner using the mismatch table in
    Section 17.
7.  Include only sanitized details in the ticket/PR.

### Checkpoint

Diagnostics are actionable and privacy-preserving. Do not add verbose
logging of user content to make debugging easier.

## Section 22 --- Local Execution and Deployment

### Objective

Document a reproducible local launch and fit the frontend into existing
deployment infrastructure.

### Local launch

If the approved entry point is `apps/web/app.py` and the project
dependencies are installed:

``` bash
python -m streamlit run apps/web/app.py
```

Set `ORDO_API_BASE_URL` using the approved local backend URL before
launching if the app needs the API. The value `http://127.0.0.1:8000` is
only an example until confirmed by the API owner.

### Local execution workflow

``` mermaid
flowchart TD
    A[Clone approved repository] --> B[Use approved Python/dependency setup]
    B --> C[Set safe local configuration]
    C --> D[Start backend using its README]
    D --> E[Start Streamlit entry point]
    E --> F[Open local URL printed by Streamlit]
    F --> G[Verify UI and API connectivity]
    G --> H[Run tests and stop processes]
```

### Deployment rules

-   Inspect existing Docker/Compose/CI configuration before changing it.
-   Do not introduce a deployment platform or Docker service unless
    approved.
-   Configure non-secret environment values in the deployment
    environment.
-   Configure credentials only in the approved secret manager.
-   Bind/listen settings and network routing must match the existing
    platform.
-   Ensure the frontend can reach the API from the deployment network;
    `localhost` inside a container means that container, not
    automatically the API service.
-   Do not claim deployment readiness from a local launch alone.

### Stop and diagnose

Stop Streamlit with `Ctrl+C` in the terminal that launched it. Inspect
terminal output for startup errors. Do not paste secrets into issue
trackers when reporting failures.

### Checkpoint

Local launch, API connectivity, and deployment compatibility are
verified separately and documented accurately.

## Section 23 --- Documentation

### Objective

Keep developer setup and user-facing behavior aligned with the
implementation.

### Documentation to maintain

-   `apps/web/README.md` if that path is approved.
-   Root README links to the frontend guide.
-   Configuration variable reference.
-   API integration notes with links to approved contracts.
-   User workflow guide for implemented pages.
-   Testing commands.
-   Troubleshooting guide.
-   Known limitations and outstanding dependencies.
-   Screenshots only if they are real, current, and approved for
    sharing.

### Proposed frontend README outline

``` markdown
# ORDO Streamlit Frontend

## Status and supported workflows
Describe only implemented and approved features.

## Prerequisites
List the Python version and dependency manager from project configuration.

## Setup
Use the repository's approved installation commands.

## Configuration
Document each required environment variable, default, and safe example.

## Run locally
Provide the verified Streamlit entry-point command and backend startup reference.

## Test
Provide the focused and full test commands actually supported by the repository.

## API contract
Link to the approved endpoint/schema documentation.

## Troubleshooting
Document verified fixes for configuration, connectivity, timeout, and test failures.

## Limitations
List endpoints/features not yet available and identify their owners.
```

### Checkpoint

A new engineer can follow the documented commands without guessing
paths, endpoints, credentials, or feature availability.

## Section 24 --- Troubleshooting Guide

  ------------------------------------------------------------------------------------------
  Problem           Possible cause     Diagnostic step                   Resolution
  ----------------- ------------------ --------------------------------- -------------------
  Streamlit does    Wrong environment  `python --version`;               Activate approved
  not start         or missing         `python -m pip show streamlit`;   environment and
                    dependency         inspect terminal output           install declared
                                                                         dependencies

  Entry-point path  Command run from   `pwd`/`Get-Location`; inspect     Run from repository
  not found         wrong directory or tree                              root and use actual
                    path not approved                                    entry-point path

  Dashboard cannot  Wrong base URL or  Check `ORDO_API_BASE_URL` is set  Correct
  reach API         backend not        without printing credentials; use configuration or
                    running            documented health endpoint if one start backend using
                                       exists                            its README

  Search returns an Contract mismatch  Inspect status code and sanitized Coordinate with
  error             or backend failure response/request ID               API/Retrieval
                                                                         owner; do not guess
                                                                         response fields

  Results disappear Session-state      Reproduce sequence; inspect state Correct
  after interaction update or rerun    transitions using non-sensitive   initialization and
                    bug                values                            submission flow

  Search runs       Request made       Count mocked client calls during  Put API call behind
  repeatedly        outside submit     UI tests                          the approved form
                    handler                                              submission

  Missing values    Optional fields    Inspect sanitized fixture against Add
  render badly      not handled        schema                            contract-aligned
                                                                         missing-value
                                                                         handling

  UI tests fail     External service   Run one test with `-vv`           Mock the API and
                    dependency or                                        initialize state
                    state not isolated                                   deterministically

  Secrets           Incorrect          Verify variable presence, never   Configure the
  unavailable after deployment config  print secret values               approved deployment
  deployment                                                             secret/config
                                                                         source

  HTTP 404          Endpoint path not  Compare path with approved        Ask API Engineer to
                    present or         OpenAPI/contract                  confirm route and
                    resource                                             semantics
                    unavailable                                          

  HTTP 401/403      Auth missing or    Verify approved auth setup and    Follow
                    permission denied  role                              access-control
                                                                         process; do not
                                                                         bypass backend

  Timeout           Backend            Check request duration and        Coordinate with API
                    slow/unavailable   backend diagnostics               owner before
                    or timeout too low                                   changing
                                                                         timeout/retry
                                                                         policy

  Invalid JSON      Proxy/error page   Check status and content type in  Correct API
                    or backend         safe test environment             response; keep user
                    response defect                                      message generic

  Wrong filter      Frontend field     Assert exact request parameters   Correct mapping
  behavior          mapping differs    in unit tests                     with Retrieval/API
                    from contract                                        owner

  Port conflict     Another local      Inspect Streamlit terminal        Use a permitted
                    process uses the   message                           port or stop the
                    port                                                 conflicting process

  Private results   Unsafe shared      Run authorization-isolation tests Disable shared
  appear across     cache or state                                       caching and involve
  sessions                                                               Security Reviewer
                                                                         immediately
  ------------------------------------------------------------------------------------------

### Useful diagnostics

``` bash
git status --short
python --version
python -m pip show streamlit
python -m pytest tests/web -q
```

Only run test commands for paths/tools that exist. Do not dump
environment variables wholesale; they may contain secrets.

## Section 25 --- Final Verification Checklist

Complete in order before opening the pull request.

-   [ ] Requirements and page inventory are approved.
-   [ ] Repository structure and ownership boundaries are confirmed.
-   [ ] Correct entry point and navigation are used.
-   [ ] API base URL is configurable.
-   [ ] Endpoint paths/methods/request schemas match approved contracts.
-   [ ] Supported filters map to approved parameters.
-   [ ] Results show only approved response fields.
-   [ ] Loading, empty, validation, timeout, and error states work.
-   [ ] Session state is deterministic and does not show stale results
    as current.
-   [ ] Retrieval/ML business logic is not duplicated in Streamlit.
-   [ ] No real secrets are committed.
-   [ ] Private data is not unnecessarily logged or cached.
-   [ ] Unit/UI tests pass and the exact command is recorded.
-   [ ] Contract/integration checks have been run where environment is
    available.
-   [ ] Formatter/linter commands pass if configured by the repository.
-   [ ] Dashboard launches locally with the documented command.
-   [ ] API connectivity is verified separately from shell rendering.
-   [ ] Documentation matches the implementation.
-   [ ] Only approved files are changed.
-   [ ] Branch uses the Team Lead-approved base.
-   [ ] Pull request describes real changes and actual test results.
-   [ ] Outstanding API/product/security blockers are listed with
    owners.

### Git review commands

``` bash
git status --short
git diff --check
git diff --stat
git diff
```

Review every diff before staging. These commands do not prove tests
passed; run the project's configured test suite separately and record
the real result.

## Section 26 --- Pull Request and Handover

### Suggested PR title

`feat(web): implement ORDO Streamlit dashboard`

Adjust the title to match the actual scope.

### PR template

``` markdown
## Summary
- What changed and why?

## Pages and components
- List implemented pages/components and link to requirements.

## API integration
- List exact endpoints/methods consumed and the approved contract reference.
- List any unresolved contract questions.

## Configuration
- List added/changed non-secret settings and deployment requirements.
- Confirm no real secrets are included.

## Tests
- Commands executed:
- Results:
- Tests not run and reason:

## Visual and accessibility verification
- Viewports checked:
- Keyboard/contrast checks:
- Screenshots, if approved:

## Security and privacy
- Private data and cache/logging review:
- Authentication assumptions:

## Deployment implications
- Confirmed impact or “none identified” with evidence.

## Known limitations
- List unimplemented or unavailable capabilities.

## Dependencies and blockers
- Owner, decision needed, and expected next step.

## Handover
- Team Lead:
- API Engineer:
- Code Retrieval Engineer:
- ML Engineer:
- Security/Privacy Reviewer:
```

### Git feature-branch and PR workflow

``` mermaid
flowchart TD
    A[Confirm repository and approved base branch] --> B[Fetch and inspect status]
    B --> C[Create frontend feature branch]
    C --> D[Implement in owned paths]
    D --> E[Run focused tests and review diff]
    E --> F{Checks and review ready?}
    F -- No --> D
    F -- Yes --> G[Commit logical changes]
    G --> H[Push feature branch]
    H --> I[Open PR against approved base]
    I --> J[Respond to review and rerun checks]
    J --> K[Team-approved merge and handover]
```

### Git commands

Do not execute branch-changing commands until the Team Lead confirms the
base branch. Then adapt the following to the actual branch and remote:

``` bash
git status --short
git remote -v
git fetch origin
git switch <TEAM_APPROVED_BASE_BRANCH>
git pull --ff-only origin <TEAM_APPROVED_BASE_BRANCH>
git switch -c feature/web/streamlit-dashboard

# After implementation and review
git diff --check
git diff --stat
git status --short
git add <APPROVED_FRONTEND_FILES>
git commit -m "feat(web): implement ORDO Streamlit dashboard"
git push -u origin feature/web/streamlit-dashboard
```

Never discard uncommitted changes. Never invent the remote URL. Stage
only reviewed frontend files; do not use `git add .` without reviewing
the complete working tree.

### Handover responsibilities

-   **Team Lead:** confirm scope, design decisions, base branch,
    acceptance criteria, and unresolved product decisions.
-   **API Engineer:** confirm endpoint contracts, auth, errors,
    pagination, and integration test results.
-   **Code Retrieval Engineer:** confirm query/filter/ranking semantics
    and relevance fields.
-   **ML Engineer:** confirm insight outputs, model-generated field
    meanings, and unavailable model capabilities.
-   **Security/Privacy Reviewer:** review secrets, private repository
    access, logs, links, and cache isolation.

The handover must distinguish completed, tested, unverified, and blocked
work. Do not claim success where tests were not run or contracts are
still pending.

## Section 27 --- Definition of Done

### Requirements

-   [ ] Scope and acceptance criteria approved.
-   [ ] Each implemented workflow maps to an approved requirement and
    API contract.
-   [ ] Unavailable features are not represented as working.

### UI implementation

-   [ ] Entry point, navigation, forms, results, and reusable components
    follow project conventions.
-   [ ] All displayed fields have known source paths and missing-value
    behavior.
-   [ ] No fake production data or fabricated insights are used.

### API integration

-   [ ] Endpoint paths, methods, request/response schemas, errors, and
    auth match approved contracts.
-   [ ] Timeouts and safe error mapping are implemented.
-   [ ] Contract/integration outcomes are documented.

### State and UX

-   [ ] Session-state transitions are deterministic.
-   [ ] Loading, empty, validation, timeout, permission, and
    unexpected-error states are handled.
-   [ ] Duplicate requests and stale-result confusion are prevented.

### Visual quality and accessibility

-   [ ] Layout is consistent, readable, keyboard-accessible, and
    responsive.
-   [ ] Long titles, missing fields, and large result sets have been
    checked.
-   [ ] CSS does not rely on fragile internal selectors.

### Security and privacy

-   [ ] No secrets are committed or logged.
-   [ ] Private data and authorization behavior are reviewed.
-   [ ] Caching and session state do not cross user boundaries.
-   [ ] Security-sensitive decisions are approved.

### Testing

-   [ ] Unit and UI tests run and results are recorded honestly.
-   [ ] External APIs are mocked in ordinary tests.
-   [ ] Relevant integration tests are completed or explicitly blocked
    with owner and reason.
-   [ ] Formatting/lint checks pass if configured.

### Documentation and operations

-   [ ] Setup, configuration, run, test, troubleshooting, and
    limitations are documented.
-   [ ] Local launch is verified.
-   [ ] Deployment compatibility is verified if deployment is in scope.
-   [ ] Diagnostics avoid sensitive data.

### Git and handover

-   [ ] Approved base branch and feature branch are used.
-   [ ] Only intended files are changed.
-   [ ] Diff is reviewed and whitespace checks pass.
-   [ ] PR describes real work and test outcomes.
-   [ ] Team Lead and relevant owners receive a handover with blockers.

**Final rule:** If a required endpoint, schema, security control,
acceptance decision, or mandatory test remains unresolved, the relevant
feature is not done. Record the blocker and its owner rather than
silently substituting an assumption.

------------------------------------------------------------------------

## Appendix A --- First actions when the ORDO repository is created

1.  Obtain the actual repository URL and access from the Team Lead.
2.  Clone the repository and inspect `README.md`, branches, dependency
    manifests, CI, tests, and existing app code.
3.  Confirm the approved integration branch; do not assume `develop`.
4.  Confirm whether `apps/web/` is the correct frontend path.
5.  Obtain the approved product requirements and API contract.
6.  Replace proposed paths/commands in this manual with verified
    repository paths.
7.  Implement the minimal shell and config first.
8.  Implement endpoint-specific API methods only after contract
    approval.
9.  Add UI behavior and tests in small, reviewable commits.
10. Open the PR with actual verification results and unresolved
    dependencies.

## Appendix B --- Contract approval worksheet

Complete before enabling search:

``` text
API contract document/version:
API owner:
Team Lead approval:
Endpoint path:
HTTP method:
Authentication/authorization:
Query parameters:
Request body:
Response schema:
Example sanitized success response:
Empty result representation:
Pagination:
Error statuses and error schema:
Timeout expectation:
Request/correlation ID:
Private repository handling:
Rate-limit behavior:
Contract test location:
Approval date:
```

## Appendix C --- Repository inspection report template

Complete this after the repository exists; do not fill it with guesses.

  --------------------------------------------------------------------------------
  Item              Observed value    Evidence/path              Owner/decision
  ----------------- ----------------- -------------------------- -----------------
  Project root      Pending           N/A                        Team Lead
                    inspection                                   

  Current branch    Pending           Git output                 Frontend Engineer
  and working tree  inspection                                   

  Approved base     Pending           Team decision/docs         Team Lead
  branch            confirmation                                 

  Python version    Pending           Manifest/CI                Team Lead
                    inspection                                   

  Streamlit version Pending           Dependency                 Frontend Engineer
                    inspection        manifest/lockfile          

  Dependency        Pending           Manifest/lockfile/README   Team Lead
  manager           inspection                                   

  Entry point       Pending           Actual source path         Frontend Engineer
                    inspection                                   

  API base URL      Pending           Config/deployment files    API Engineer
  configuration     inspection                                   

  Search            Pending contract  OpenAPI/schema document    API Engineer
  endpoint/schema                                                

  Authentication    Pending review    Security design            API + Security
                                                                 Reviewer

  Test/lint         Pending           CI/workflow/config         Frontend Engineer
  commands          inspection                                   

  Deployment target Pending           Existing infrastructure    Team Lead/DevOps
                    inspection        files                      
  --------------------------------------------------------------------------------

**Document status:** This is an implementation blueprint prepared before
repository creation. It contains a safe starter shell and generic
transport example, but endpoint-specific search/results/details/insights
code must be completed against the real ORDO repository and approved API
contracts.
