# Evidence — VisionMatch AI

## 1. Project Information

**Project Name:** VisionMatch AI — AI Image Understanding & Content Matching Engine

**Track:** FlyRank Internship — Backend AI Engineering

**GitHub Repository:** https://github.com/HR-Fatheen/visionmatch-ai

**Purpose:** Build a backend system that uses AI-generated image understanding and similarity scoring to support content-to-image matching.

---

## 2. Implementation Evidence

The project uses the following technologies and components:

| Component | Technology |
|---|---|
| Backend framework | FastAPI |
| Programming language | Python |
| Database | PostgreSQL |
| Vector database extension | pgvector |
| ORM | SQLAlchemy |
| Database migrations | Alembic |
| AI vision provider | Google Gemini |
| Environment configuration | python-dotenv |
| Testing framework | pytest |
| Containerized database | Docker Compose |

### Application Entry Point

The FastAPI application is defined in `app/main.py`.

The currently registered HTTP endpoints are:

- `GET /` — Root endpoint.
- `GET /health` — Health-check endpoint.

Other functionality described in the design documentation should not be considered an exposed HTTP endpoint unless it is registered in the FastAPI application.

### Database Configuration

Database connection settings are loaded from environment variables.

The `.env.example` file provides the configuration template:

- `DATABASE_URL` — PostgreSQL connection string.
- `GEMINI_API_KEY` — API key for the Google Gemini provider.

The actual `.env` file contains local configuration and must not be committed to the repository.

### Database Migrations

Alembic is configured for database schema migrations.

The migration command is:

`alembic upgrade head`

This applies the available database migrations. It does not, by itself, populate the database with image records or evaluation data.

---

## 3. Automated Test Evidence

The default automated test suite was executed using:

`python -m pytest -q`

### Latest Result

| Metric | Result |
|---|---:|
| Tests passed | 15 |
| Tests failed | 0 |
| Result | PASS |

The pytest configuration excludes `tests/integration` from the default run. Therefore, this result applies to the tests collected by the default configuration, not to the integration tests.

The integration tests were not verified in the latest run because a live Gemini API request encountered a `429 RESOURCE_EXHAUSTED` quota error.

## 4. Evaluation Evidence

The evaluation script was executed using:

`python -m evaluation.evaluate`

### Latest Recorded Results

| Metric | Result |
|---|---:|
| Evaluation cases | 10 |
| Candidates evaluated | 19 |
| Correct decisions | 19 |
| Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |
| F1 score | 100% |
| False accepts | 0 |
| False rejects | 0 |

### Interpretation and Limitations

The evaluation dataset covers wildlife, technology, food, sports, low-confidence rejection, and a no-match scenario.

The similarity and confidence values used by the current evaluation fixtures are predefined test values. The reported metrics describe the decision logic on these supplied fixtures; they do not establish real-world Gemini model accuracy or production retrieval performance.

## 5. Evaluation Artifacts

The evaluation-related files include:

| File | Purpose |
|---|---|
| `evaluation/dataset.json` | Contains the evaluation cases and candidate decisions. |
| `evaluation/evaluate.py` | Runs the evaluation and calculates metrics. |
| `evaluation/report.json` | Stores the generated evaluation report. |

These files provide the available evidence for the recorded evaluation results.

---

## 6. Repository and Configuration Evidence

The repository includes the following project configuration and documentation files:

| File | Purpose |
|---|---|
| `README.md` | Project overview, setup instructions, architecture, and limitations. |
| `capstone.yaml` | Run command, migration command, test command, base URL, and currently exposed endpoint declarations. |
| `.env.example` | Template for required environment variables. |
| `compose.yaml` | Docker Compose configuration for PostgreSQL with pgvector. |
| `docs/DESIGN.md` | Architecture, data model, and intended API design. |
| `migrations/` | Alembic database migration files. |
| `app/` | Application source code. |
| `tests/` | Automated tests. |
| `evaluation/` | Evaluation dataset, script, and report. |

---

## 7. Scope and Outstanding Evidence

The design documentation describes a target image corpus of at least 40 images across at least four categories and an evaluation dataset containing at least ten labeled posts.

The repository contains 40 downloaded images across four categories, plus an additional `gemini-test.jpg` file. Source and attribution metadata is stored in `data/image_sources.json`.

The evaluation dataset contains ten cases and 19 candidate decisions. Its metrics are based on predefined fixtures, not an independent real-world retrieval benchmark.

The following items should not be claimed as completed without additional implementation and evidence:

- A fully populated database containing the target image and post records.
- Real-world top-1 matching precision measured against independently labeled data.
- Background processing, retries, and failure alerts beyond the behavior demonstrated by tests.
- Cost and usage tracking for actual AI provider calls, supported by recorded logs.
- Image-matching functionality exposed through HTTP endpoints that are not registered in the current FastAPI application.

This section distinguishes the functionality and results already confirmed from the broader project targets described in the design.

---

## 8. Evidence Summary

The following evidence has been recorded:

- The FastAPI application has root and health-check endpoints.
- PostgreSQL and pgvector are configured through Docker Compose.
- Database migrations are configured through Alembic.
- Environment-variable configuration is documented.
- The automated test suite previously passed all 18 tests.
- The evaluation script previously reported nine correct candidate decisions out of nine.
- Evaluation artifacts are present in the project structure.
- Project documentation identifies the current evaluation and dataset limitations.
- The default test suite passed 15 tests; integration tests were excluded from the latest run.
- The evaluation script reported 19 correct candidate decisions out of 19 on the supplied fixtures.
- The repository contains 40 downloaded images across four categories, with source metadata recorded in `data/image_sources.json`.

The recorded test and evaluation results are limited to the implementation and fixtures available at the time of those runs. They do not independently verify every requirement in the original capstone brief.