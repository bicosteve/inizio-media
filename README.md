# Inizio Media — Google Organic Search Extractor

A FastAPI application that performs Google searches through SerpAPI, extracts organic search results, displays them through a web interface, exposes them through a REST API, and stores search history in a JSON file.

## Features

- Google organic search through SerpAPI
- Server-rendered HTML search interface using Jinja2
- REST API returning structured JSON
- Search history persistence
- Pydantic data validation
- Layered architecture
- Unit and route tests with Pytest
- Docker support
- Docker Compose support
- GitHub Actions CI/CD

---

## Architecture

The application follows a layered architecture:

```text
Browser / API Client
        │
        ▼
      Routes
        │
        ▼
   Search Service
     │       │
     │       ├──────────────► Repository
     │       │                    │
     ▼       ▼                    ▼
 Provider   Parser           searches.json
     │
     ▼
  SerpAPI
```

Each layer has a specific responsibility:

| Layer         | Responsibility                                   |
| ------------- | ------------------------------------------------ |
| `routes/`     | HTTP endpoints and HTML rendering                |
| `services/`   | Application/business workflow                    |
| `providers/`  | Communication with SerpAPI                       |
| `parsers/`    | Extraction and transformation of organic results |
| `models/`     | Pydantic data models                             |
| `repository/` | Search-history persistence                       |
| `templates/`  | HTML pages                                       |
| `static/`     | CSS and frontend assets                          |
| `tests/`      | Automated tests                                  |

---

# Project Structure

```text
inizio-media/
│
├── .github/
│   └── workflow/
│       ├── ci.yml
│       └── deploy.yml
│
├── data/
│   └── searches.json
│
├── models/
│   └── search.py
│
├── parsers/
│   └── organic_parser.py
│
├── providers/
│   └── google_provider.py
│
├── repository/
│   └── search_history.py
│
├── routes/
│   └── search.py
│
├── services/
│   └── search_service.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── history.html
│   └── index.html
│
├── tests/
│   ├── test_parser.py
│   ├── test_provider.py
│   ├── test_routes.py
│   └── test_service.py
│
├── .dockerignore
├── .env
├── .env.example
├── docker-compose.prod.yml
├── docker-compose.yml
├── Dockerfile
└── main.py
```

---

# Application Flow

## Web Interface

The web interface is available at:

```text
GET /
```

The user submits a search through the HTML form:

```text
GET /search?q=fastapi
```

The request flows through:

```text
index.html
    ↓
/search
    ↓
SearchService
    ↓
SearchProvider
    ↓
SerpAPI
    ↓
Organic Parser
    ↓
SearchResponse
    ↓
SearchHistoryRepository
    ↓
data/searches.json
    ↓
index.html
```

The results are then rendered back into the HTML page.

## REST API

The same search functionality is available through:

```text
GET /api/search?q=fastapi
```

The API returns a JSON `SearchResponse`.

API searches and browser searches use the same service and repository, so both are stored in the search history.

---

# Search History

Searches are stored in:

```text
data/searches.json
```

The initial file should contain:

```json
[]
```

A stored search contains information such as:

```json
{
  "query": "fastapi",
  "engine": "google",
  "page": 1,
  "searched_at": "2026-09-24T10:00:00+00:00",
  "results": []
}
```

The JSON repository is intentionally simple for this project. A production application could replace it with PostgreSQL or another persistent database without changing the overall service architecture.

---

# Requirements

You can run the project either directly with Python or using Docker.

## Option 1 — Run Without Docker

### Prerequisites

Install:

- Python 3.14
- Pipenv
- Git

Verify Python:

```bash
python3 --version
```

Verify Pipenv:

```bash
pipenv --version
```

---

## 1. Clone the repository

```bash
git clone git@github.com:bicosteve/inizio-media.git
cd inizio-media
```

---

## 2. Create the environment

The project uses Pipenv for dependency and virtual-environment management.

```bash
pipenv install
```

This installs the dependencies defined in:

```text
Pipfile
Pipfile.lock
```

Enter the virtual environment:

```bash
pipenv shell
```

Create a `.env` file:

```bash
cp .env.example .env
```

Set your SerpAPI key:

```env
SERPAPI_KEY=your_serpapi_key
```

Do not commit `.env` to Git.

The `.env.example` file documents the required environment variables without exposing secrets.

---

## 4. Initialize search history

Make sure the history file exists and contains an empty JSON list:

```bash
mkdir -p data
echo '[]' > data/searches.json
```

---

## 5. Run the application

```bash
pipenv run uvicorn main:app --reload
```

The application starts on:

```text
http://127.0.0.1:8000
```

`--reload` enables automatic application reloads during development when Python source files change.


# Option 2 — Run With Docker

Docker allows the application to run without installing the Python dependencies directly on the host machine.

### Prerequisites

Install:

- Docker
- Docker Compose

Verify:

```bash
docker --version
```

and:

```bash
docker compose version
```

---

## 1. Configure environment variables

Create the `.env` file:

```bash
cp .env.example .env
```

Add your SerpAPI key:

```env
SERPAPI_KEY=your_serpapi_key
```

---

## 2. Initialize search history

```bash
mkdir -p data
echo '[]' > data/searches.json
```

---

## 3. Build the Docker image

```bash
docker compose build
```

This builds the image using the project's `Dockerfile`.

The Dockerfile:

1. Starts from the Python base image.
2. Installs Pipenv.
3. Installs the locked project dependencies.
4. Copies the application source.
5. Exposes port `8000`.
6. Starts Uvicorn.

---

## 4. Start the application

```bash
docker compose up
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Run it in detached mode:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

---

# Docker and Search History Persistence

The Docker Compose configuration mounts the local `data` directory into the container.

Conceptually:

```text
Host
~/inizio-media/data/searches.json
             │
             │ volume mount
             ▼
Container
/app/data/searches.json
```

This is important because containers are replaceable.

Without the volume, the JSON history would exist only inside the container filesystem and could be lost when the container is recreated.

---

# API Endpoints

## Web Interface

### Search page

```text
GET /
```

Displays the search form.

### Perform browser search

```text
GET /search?q=fastapi
```

Returns an HTML page containing the search results.

### Search history page

```text
GET /history/
```

Returns the HTML search history page.

---

## REST API

### Search

```text
GET /api/search?q=fastapi
```

Returns:

```json
{
  "query": "fastapi",
  "engine": "google",
  "page": 1,
  "results": []
}
```

### Search history

```text
GET /api/history
```

Returns previously stored searches.

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

The HTML-only routes are excluded from the OpenAPI schema where appropriate, keeping the API documentation focused on the REST interface.

---

# Testing

The project uses Pytest.

Run all tests:

```bash
pytest -q
```

or:

```bash
make test
```

The test suite is divided according to application responsibilities.

### `test_parser.py`

Tests transformation of raw SerpAPI responses into application search-result models.

### `test_provider.py`

Tests the search-provider integration and isolates the external SerpAPI dependency.

### `test_service.py`

Tests the search workflow independently from the HTTP layer.

The provider and repository can be replaced with test doubles.

### `test_routes.py`

Tests the FastAPI HTTP endpoints, including HTML and JSON responses.

---

# Docker Testing

Tests can also be executed inside the Docker environment if required by the development setup.

For example:

```bash
docker compose run --rm app pytest -q
```

The exact service name depends on the service name defined in `docker-compose.yml`.

---

# Environment Variables

The application currently requires:

| Variable      | Description                    |
| ------------- | ------------------------------ |
| `SERPAPI_KEY` | API key used to access SerpAPI |

Example:

```env
SERPAPI_KEY=your_serpapi_key
```

Never commit real credentials.

---

# CI/CD

The project contains GitHub Actions workflows:

```text
.github/workflow/
├── ci.yml
└── deploy.yml
```

## CI

`ci.yml` is responsible for automated verification of changes.

The CI pipeline can:

```text
Push / Pull Request
        ↓
Install dependencies
        ↓
Run tests
        ↓
Build Docker image
        ↓
Publish image when configured
```

## Deployment

`deploy.yml` handles deployment of the published Docker image to the target environment.

The deployment process follows the general pattern:

```text
GitHub
   ↓
Docker image
   ↓
Container registry
   ↓
Production VM
   ↓
docker compose pull
   ↓
docker compose up -d
```

Deployment credentials and application secrets are supplied through GitHub Actions secrets rather than committed to the repository.

---

# Production Docker Configuration

The project contains:

```text
docker-compose.prod.yml
```

The production configuration is intended to run the already-built application image rather than rebuilding the application directly on the production server.

The search-history directory is mounted as persistent storage:

```text
./data:/app/data
```

This allows the application to retain `searches.json` when the container is recreated.

---

# Development vs Production

|               | Development            | Production                     |
| ------------- | ---------------------- | ------------------------------ |
| Runtime       | Local Python or Docker | Docker                         |
| Server        | Uvicorn                | Uvicorn                        |
| Reload        | Enabled                | Disabled                       |
| Configuration | `.env`                 | Deployment secrets/environment |
| Image         | Locally built          | Published container image      |
| History       | Local `data/`          | Persistent mounted `data/`     |
| Deployment    | Manual                 | GitHub Actions                 |

---

# Design Decisions

## Service Layer

The search logic is kept in `SearchService` rather than inside the routes.

Both:

```text
/api/search
```

and:

```text
/search
```

call:

```text
SearchService.search()
```

This prevents duplicate business logic.

---

## Provider Layer

The application communicates with SerpAPI through `SearchProvider`.

This keeps the external API implementation isolated from the rest of the application.

A different search provider could be introduced later without forcing the routes to understand the provider's API format.

---

## Parser Layer

SerpAPI returns a raw dictionary containing more information than the application requires.

The parser extracts only organic results and converts them into application models.

```text
Raw external response
        ↓
Organic parser
        ↓
SearchResult
```

---

## Repository Layer

Persistence is isolated behind `SearchHistoryRepository`.

Currently:

```text
SearchHistoryRepository
        ↓
JSON file
```

The service does not need to know whether history is stored in JSON, PostgreSQL, Redis, or another storage system.

---

## Pydantic Models

Pydantic provides explicit data contracts for the application.

The main models are:

```text
SearchResult
SearchResponse
```

These models provide validation and serialization for API responses and internal application data.

---

# Security Considerations

- Never commit `.env`.
- Keep API keys in environment variables.
- Use `.env.example` for documenting required configuration.
- Do not expose SerpAPI credentials through API responses.
- External result links are opened with `rel="noopener noreferrer"`.
- Production deployments should use HTTPS.
- A production implementation should additionally consider authentication, rate limiting, request validation, and stronger persistence controls.

---

# Limitations

The current implementation uses a JSON file for search history.

This is suitable for a small demonstration/project but has limitations for concurrent production workloads.

Potential issues include:

- concurrent file writes
- lack of database transactions
- limited querying capabilities
- file-level locking requirements
- increasing file size over time

A relational database such as PostgreSQL would be a natural next step for production persistence.

---

# Future Improvements

Potential improvements include:

- PostgreSQL persistence
- SQL migrations
- Redis caching
- search pagination
- authentication and authorization
- API versioning
- rate limiting
- structured logging
- health-check endpoints
- metrics and monitoring
- asynchronous external API calls where appropriate
- additional search providers
- integration tests
- stronger repository interfaces
- background processing for long-running operations

---

# Quick Start

## Without Docker

```bash
git clone <repository-url>
cd inizio-media

pipenv install
cp .env.example .env

# Add SERPAPI_KEY to .env

mkdir -p data
echo '[]' > data/searches.json

pipenv run uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

---

## With Docker

```bash
git clone <repository-url>
cd inizio-media

cp .env.example .env

# Add SERPAPI_KEY to .env

mkdir -p data
echo '[]' > data/searches.json

docker compose build
docker compose up -d
```

Open:

```text
http://127.0.0.1:8000/
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

# Summary

Inizio Media is a layered FastAPI application demonstrating how to build a backend service that separates HTTP handling, business logic, external integrations, data transformation, and persistence.

The same search workflow powers both the web interface and REST API:

```text
                    ┌── /search ────────► HTML
                    │
Client ─────────────┤
                    │
                    └── /api/search ────► JSON
                             │
                             ▼
                      SearchService
                             │
                 ┌───────────┼───────────┐
                 ▼           ▼           ▼
              Provider     Parser     Repository
                 │                       │
                 ▼                       ▼
              SerpAPI              searches.json
```

This structure provides a foundation for evolving the project from a simple FastAPI application into a more production-oriented backend service.
