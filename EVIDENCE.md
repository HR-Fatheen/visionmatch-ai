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

The project's automated test suite was executed successfully.

**Previously recorded result:**

| Metric | Result |
|---|---:|
| Tests passed | 18 |
| Tests failed | 0 |
| Total tests | 18 |
| Result | PASS |

Command used:

`python -m pytest -v`

**Note:** These results reflect a previous test run. They should not be interpreted as a new test execution performed while preparing this document.

---

## 4. Evaluation Evidence

The evaluation script was executed successfully using the available evaluation fixtures.

Command used:

`python -m evaluation.evaluate`

### Recorded Results

| Metric | Result |
|---|---:|
| Candidates evaluated | 9 |
| Correct decisions | 9 |
| Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |
| F1 score | 100% |
| False accepts | 0 |
| False rejects | 0 |
| True positives | 4 |
| True negatives | 5 |

### Interpretation

The evaluation script reported correct decisions for all nine candidate decisions in the supplied evaluation dataset.

The dataset contains five cases covering examples such as:

- Matching a fox image to wildlife content.
- Matching a wolf image to wildlife content.
- Matching a classroom image to AI education content.
- Matching a pizza image to food-related content.
- Rejecting a low-confidence candidate.

The evaluation includes both positive and negative candidate decisions.

### Important Limitations

These results represent performance on the supplied evaluation fixtures. They do not establish equivalent performance on a larger, independently labeled, real-world image dataset.

The similarity and confidence scores used by the current evaluation fixtures are predefined test values. Consequently, the reported metrics should not be interpreted as proof of real-world Gemini model accuracy.

The current evaluation dataset contains five cases and nine candidate decisions. The project design target calls for at least ten labeled evaluation posts, so that target should not be considered satisfied by these results alone.

The reported 100% precision is the candidate-level precision calculated by the existing evaluation script. It should not be presented as top-1 image-matching precision across ten or more posts.

---

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

The currently confirmed image corpus includes `data/images/gemini-test.jpg`. The complete image-corpus target has not been verified.

The following items should therefore not be claimed as completed without additional implementation and evidence:

- A verified corpus of at least 40 images across four or more categories.
- At least ten labeled evaluation posts.
- Real-world top-1 matching precision measured against the required evaluation dataset.
- A fully populated database containing the target image and post records.
- Background processing, retries, and failure alerts, unless demonstrated by the implementation.
- Cost and usage tracking for actual AI provider calls, unless supported by recorded logs.
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

The recorded test and evaluation results are limited to the implementation and fixtures available at the time of those runs. They do not independently verify every requirement in the original capstone brief.