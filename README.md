# VisionMatch AI

## AI Image Understanding & Content Matching Engine

VisionMatch AI is a backend capstone project that explores AI-assisted image understanding and semantic image-to-content matching.

The system is designed to extract structured metadata from images, generate embeddings for images and blog posts, rank potential matches, and reject unsuitable recommendations when confidence or relevance is insufficient.

## 1. Architecture

```text
Image
  |
  v
Image Processing Worker
  |
  v
Vision Provider (Gemini or Mock)
  |
  v
Validated Image Metadata
  |
  v
Image Embeddings
  |
  v
PostgreSQL + pgvector
  ^
  |
Blog Post -> Post Embedding
  |
  v
Semantic Candidate Ranking
  |
  v
Mismatch Guard
  |
  +----------------------+
  |                      |
  v                      v
Accept Candidate    Reject Candidate
                    with Explanation
```

Supporting services handle embedding generation, match results, reviews, AI usage tracking, and estimated AI costs.

## 2. Technology Stack

* **Programming Language:** Python
* **Web Framework:** FastAPI
* **Database ORM:** SQLAlchemy
* **Database:** PostgreSQL
* **Vector Search:** pgvector
* **Database Migrations:** Alembic
* **AI Integration:** Google Gemini
* **Testing Framework:** pytest
* **Environment Configuration:** python-dotenv
* **Containerization:** Docker Compose

## 3. Project Structure

```text
flyrank-capstone-image-relevance/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── services/
│   └── workers/
├── data/
│   └── images/
├── docs/
│   └── DESIGN.md
├── evaluation/
│   ├── dataset.json
│   ├── evaluate.py
│   └── report.json
├── migrations/
├── tests/
├── compose.yaml
├── requirements.txt
├── .env.example
├── README.md
├── capstone.yaml
├── EVIDENCE.md
└── BUILDLOG.md
```

## 4. Prerequisites

Before running the project, ensure the following are installed:

* Python 3.12
* Docker Desktop with Docker Compose
* Git
* A Google Gemini API key for live Gemini operations

## 5. Installation and Setup

Run the following commands in PowerShell from the project root directory.

### Step 1: Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 2: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If the virtual environment already exists and is activated, you can skip these two steps.

### Step 3: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

If `.env` already exists, do not overwrite it. Open the existing file instead.

Configure the database connection and Gemini API key in `.env`.

Example configuration:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/image_matching
GEMINI_API_KEY=
```

Replace the empty `GEMINI_API_KEY` value with your actual API key when live Gemini operations are required.

**Security Note:** Never commit your `.env` file or expose API keys, passwords, or other credentials in the repository.

### Step 5: Start PostgreSQL with pgvector

```powershell
docker compose up -d db
```

The database is exposed on localhost port `5433`.

### Step 6: Apply Database Migrations

```powershell
alembic upgrade head
```

### Step 7: Start the FastAPI Application

```powershell
uvicorn app.main:app --reload
```

The development server normally runs at:

`http://127.0.0.1:8000`

## 6. Currently Exposed HTTP Endpoints

The following endpoints are currently registered in the FastAPI application.

| HTTP Method | Endpoint  | Description                                      |
| ----------- | --------- | ------------------------------------------------ |
| GET         | `/`       | Returns the application name and running status. |
| GET         | `/health` | Returns a basic health status response.          |

Interactive API documentation is normally available at:

`http://127.0.0.1:8000/docs`

**Important:** Image processing, post matching, jobs, and reviews are part of the broader project design. Their presence in models, services, or documentation does not mean corresponding HTTP endpoints are currently exposed. Refer to `docs/DESIGN.md` for the intended broader API design.

## 7. Evaluation

The evaluation dataset is located at:

`evaluation/dataset.json`

Run the evaluation using:

```powershell
python -m evaluation.evaluate
```

The evaluator writes the results to:

`evaluation/report.json`

### Current Evaluation Results

The latest recorded evaluation produced the following results:

| Metric                        | Result |
| ----------------------------- | -----: |
| Candidate Decisions Evaluated |      9 |
| Correct Decisions             |      9 |
| Accuracy                      |   100% |
| Precision                     |   100% |
| Recall                        |   100% |
| F1 Score                      |   100% |
| False Accepts                 |      0 |
| False Rejects                 |      0 |

### Evaluation Dataset

The current evaluation dataset contains five cases and nine candidate decisions. It covers examples involving foxes, wolves, educational content, pizza, and low-confidence rejection.

The evaluation uses supplied similarity and confidence values as fixtures. Therefore, the results demonstrate the mismatch-guard decisions on the current test cases rather than real-world AI retrieval performance.

The current dataset does not yet meet the design target of at least ten labeled posts.

The reported metrics should be interpreted within the limits of the dataset and should not be treated as proof of production-level matching accuracy.

## 8. Running Tests

Run the complete test suite using:

```powershell
python -m pytest -v
```

The previously completed test run passed all 18 tests.

The existing successful test results are documented here for reference. A README documentation update alone does not require rerunning the test suite.

## 9. Database Migrations

Database migration configuration is maintained through Alembic.

The migration configuration is located in:

* `alembic.ini`
* `migrations/`

To apply available migrations, run:

```powershell
alembic upgrade head
```

## 10. Environment Variables

The project uses environment variables to configure database access and external AI services.

| Variable         | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| `DATABASE_URL`   | Configures the PostgreSQL database connection.   |
| `GEMINI_API_KEY` | Provides credentials for live Gemini operations. |

The `.env.example` file contains the example configuration.

Create and maintain a local `.env` file for actual credentials. Do not publish secrets in source control.

## 11. Design Documentation

The file `docs/DESIGN.md` describes the intended system architecture, data model, workflows, and broader API design.

The design covers the following areas:

* Image metadata processing
* Image and post embeddings
* Semantic candidate ranking
* Match decisions and mismatch rejection
* Database-backed data models
* AI usage and estimated cost tracking
* Reviews and supporting workflows

The design document describes the intended broader system. It should not be interpreted as confirmation that every planned feature is fully implemented or available through an HTTP endpoint.

## 12. Current Limitations

The current implementation has the following limitations:

1. The FastAPI application currently exposes only the root and health endpoints.
2. The labeled evaluation dataset contains five cases, below the target of ten or more labeled posts.
3. The current evaluation uses supplied similarity and confidence values rather than measuring complete live-model retrieval performance.
4. Live Gemini operations require valid credentials and appropriate provider access.
5. The design document includes a broader planned API surface than the endpoints currently registered in the FastAPI application.
6. The current evaluation results apply only to the supplied dataset and should not be generalized to production performance.
7. The project should not be considered to have met every capstone acceptance requirement solely because its existing tests pass.

## 13. Future Improvements

Potential improvements include:

* Implementing and exposing the remaining API endpoints.
* Expanding the image corpus across the required categories.
* Creating a labeled evaluation dataset containing at least ten posts.
* Evaluating actual embedding-based retrieval performance.
* Adding stronger integration tests for database-backed workflows.
* Verifying background-job retry and failure-handling behavior.
* Verifying AI usage logging and cost-budget enforcement.
* Capturing evidence for each capstone acceptance probe.

These are improvement areas and should not be interpreted as features already completed.

## 14. Running the Project: Quick Reference

Start the database:

```powershell
docker compose up -d db
```

Apply migrations:

```powershell
alembic upgrade head
```

Start the application:

```powershell
uvicorn app.main:app --reload
```

Run evaluation:

```powershell
python -m evaluation.evaluate
```

Run tests:

```powershell
python -m pytest -v
```

Open the API documentation:

`http://127.0.0.1:8000/docs`

## 15. License

No license has been specified for this project.
