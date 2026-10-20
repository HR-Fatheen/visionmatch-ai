# VisionMatch AI — AI Image Understanding & Content Matching Engine

VisionMatch AI is a Python backend project designed to analyze images, generate semantic embeddings, and match images with relevant content. It combines AI-powered image understanding, vector similarity search, mismatch detection, background processing, review records, and AI usage and cost estimation.

The project is built as a capstone for the Flyrank AI Backend Engineering track.

## 1. Project Overview

The goal of VisionMatch AI is to recommend relevant images for written content while avoiding incorrect matches.

For example, when matching images to an article about red foxes, the system should rank relevant fox images above unrelated wildlife images. It should also reject an unsuitable candidate, such as a wolf image, when the required subject is a fox.

### Key Features

* Image ingestion and metadata persistence.
* AI-powered image understanding using a vision provider.
* Structured image metadata, including captions, tags, and confidence.
* Text and image embedding service abstractions.
* Vector persistence and semantic similarity search.
* Similarity, confidence, and tag-based mismatch checks.
* Explanations for accepted and rejected match candidates.
* Image processing jobs with retry and failure handling.
* AI usage tracking and estimated cost calculation.
* Review records for approved or rejected matches.
* Evaluation dataset and report.
* Automated tests for important application behavior.

> **Implementation status:** The project contains services for image processing, embeddings, matching, and review workflows. However, the currently registered HTTP API exposes only the root and health endpoints. The complete matching workflow should not be considered available through HTTP until the necessary API routes are implemented and verified.

## 2. Technology Stack

| Technology                 | Purpose                              |
| -------------------------- | ------------------------------------ |
| Python                     | Primary programming language         |
| FastAPI                    | HTTP application framework           |
| SQLAlchemy                 | Database ORM                         |
| PostgreSQL                 | Relational database                  |
| pgvector                   | Vector storage and similarity search |
| Alembic                    | Database migrations                  |
| Pytest                     | Automated testing                    |
| Uvicorn                    | ASGI application server              |
| Google Gemini              | AI vision and embedding integration  |
| Python virtual environment | Isolated development dependencies    |

## 3. Architecture

The project separates database models, application services, AI provider integrations, and background processing.

```text
                     VisionMatch AI
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
    Image Ingestion                    Post Content
          |                                 |
          v                                 v
     Image Record                   Text Embedding Service
          |
          v
   Image Processing Job
          |
          v
      Vision Provider
          |
          v
  Caption, Tags, Confidence
          |
          +-----------------------+
          |                       |
          v                       v
   Metadata Persistence    Image Embedding Service
                                  |
                                  v
                         Image Vector Persistence

       Post Vector + Image Vectors
                  |
                  v
         Similarity Search
                  |
                  v
            Mismatch Guard
      (Similarity + Confidence + Tags)
                  |
          +-------+-------+
          |               |
          v               v
    Accepted Match    Rejected Match
          |               |
          +-------+-------+
                  |
                  v
       Match Result and Explanation
                  |
                  v
            Review Service

     AI Usage and Estimated Cost Tracking
```

### Main Processing Flow

1. An image is registered in the database.
2. An image processing job runs the vision analysis.
3. The vision provider returns image information such as a caption, tags, and confidence.
4. The generated metadata is saved.
5. Image and post embeddings can be generated and persisted through their respective services.
6. The matching service retrieves semantically similar image candidates.
7. The mismatch guard evaluates similarity, confidence, and required tags.
8. Match decisions and explanations can be persisted.
9. Review records can capture approval or rejection.
10. AI usage and estimated costs are recorded when usage information is available.

The diagram describes the intended service-level workflow. It does not imply that every step is exposed through a registered HTTP endpoint or has been verified end to end against a live AI provider.

## 4. Project Structure

The main project components include:

```text
flyrank-capstone-image-relevance/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │
│   ├── services/
│   │   ├── ai_cost_service.py
│   │   ├── ai_usage_service.py
│   │   ├── embedding_service.py
│   │   ├── image_embedding_service.py
│   │   ├── image_ingestion.py
│   │   ├── image_processing_job_service.py
│   │   ├── matching_pipeline_service.py
│   │   ├── matching_service.py
│   │   ├── mismatch_guard.py
│   │   ├── post_embedding_service.py
│   │   ├── post_matching_service.py
│   │   ├── review_service.py
│   │   └── vector_service.py
│   │
│   └── workers/
│       └── image_processing_worker.py
│
├── data/
│   ├── images/
│   │   ├── food/
│   │   ├── sports/
│   │   ├── technology/
│   │   ├── wildlife/
│   │   └── gemini-test.jpg
│   └── image_sources.json
│
├── evaluation/
│   ├── dataset.json
│   ├── report.json
│   └── evaluate.py
│
├── scripts_download_images.py
├── scripts_expand_evaluation.py
├── tests/
├── alembic/
├── alembic.ini
├── capstone.yaml
├── pytest.ini
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── EVIDENCE.md
└── BUILDLOG.md
```

The structure above summarizes the principal project components. Individual files and folders may vary as development continues.

## 5. Setup and Installation

### Prerequisites

Install the following:

* Python compatible with the project's dependencies.
* Git.
* Docker Desktop, if using the provided Docker Compose database configuration.
* A Google Gemini API key for operations that call Gemini.

### Step 1: Clone the Repository

```powershell
git clone https://github.com/HR-Fatheen/visionmatch-ai.git
cd visionmatch-ai
```

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with the appropriate local database settings and AI provider credentials.

**Important:** Replace placeholder values with your own configuration. Never commit `.env` or publish API keys, passwords, or other secrets.

### Step 5: Start the Database

If using the project's Docker Compose configuration, start its configured services:

```powershell
docker compose up -d
```

Check the database container status:

```powershell
docker compose ps
```

Confirm that the database connection settings in `.env` match the configuration used by Docker Compose.

### Step 6: Apply Database Migrations

After the database is running and the environment variables are configured, execute:

```powershell
alembic upgrade head
```

This applies the database migrations. It does not automatically populate the database with the image corpus or create a complete set of image and post embeddings.

### Step 7: Run the Application

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application should be available locally at:

```text
http://127.0.0.1:8000
```

## 6. Available HTTP Endpoints

The currently registered HTTP endpoints are:

| Method | Endpoint  | Purpose                                            |
| ------ | --------- | -------------------------------------------------- |
| GET    | `/`       | Returns application information and running status |
| GET    | `/health` | Returns a health status response                   |

### Root Endpoint

Request:

```http
GET /
```

Expected response:

```json
{
  "name": "AI Image Understanding & Content Matching Engine",
  "status": "running"
}
```

### Health Endpoint

Request:

```http
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

These endpoints provide basic application status. They do not prove that the database, Gemini API, background jobs, or complete matching workflow are operational.

The image ingestion, matching, and review services are not currently exposed through additional registered HTTP routes.

## 7. Image Dataset

The project includes a local image corpus intended to support development and evaluation.

### Dataset Summary

| Category                     | Downloaded Images |
| ---------------------------- | ----------------: |
| Food                         |                10 |
| Sports                       |                10 |
| Technology                   |                10 |
| Wildlife                     |                10 |
| **Total categorized images** |            **40** |

An additional image, `gemini-test.jpg`, is included for testing.

This gives the project **40 categorized downloaded images across four categories, plus one additional test image**.

### Dataset Locations

```text
data/
├── images/
│   ├── food/
│   ├── sports/
│   ├── technology/
│   ├── wildlife/
│   └── gemini-test.jpg
└── image_sources.json
```

The `data/image_sources.json` file records source and attribution information for the downloaded images.

### Important Distinction

Having image files in the repository does not mean they have all been inserted into the database, analyzed by Gemini, assigned schema-validated metadata, or embedded into the vector database.

Those processing steps must be executed and verified separately.

## 8. Evaluation

The evaluation dataset is located at:

```text
evaluation/dataset.json
```

The generated evaluation report is located at:

```text
evaluation/report.json
```

### Run the Evaluation

With the virtual environment activated, execute:

```powershell
python -m evaluation.evaluate
```

The script evaluates the cases defined in the evaluation dataset and saves a report.

### Current Evaluation Results

The latest recorded evaluation output contains:

| Metric                        | Result |
| ----------------------------- | -----: |
| Evaluation cases              |     10 |
| Candidate decisions           |     19 |
| Correct candidate decisions   |     19 |
| Incorrect candidate decisions |      0 |
| Accuracy                      |   100% |
| Precision                     |   100% |
| Recall                        |   100% |
| F1 score                      |   100% |
| False accepts                 |      0 |
| False rejects                 |      0 |

The evaluation includes cases covering:

* Fox-related wildlife content.
* Wolf-related mismatch rejection.
* Technology and education.
* Food and cooking.
* Low-confidence results.
* Sports content.
* Robotics.
* Pasta-related content.
* Eagle-related wildlife content.
* Content with no suitable match.

### Interpreting the Results

**The reported 100% scores are results from the current evaluation fixtures, not proof of 100% real-world AI matching accuracy.**

The evaluation uses predefined similarity, confidence, and candidate-decision values. These fixtures are useful for checking decision logic, expected acceptance and rejection behavior, and evaluation-report generation.

They do not establish that Gemini-generated embeddings or a live database retrieval pipeline will achieve the same performance on unseen images.

The 19 candidate decisions should also not be confused with 19 independent evaluation posts or a verified production top-1 precision measurement.

A stronger end-to-end evaluation would require processing the image corpus, generating real embeddings, running actual similarity searches, and comparing ranked results against independently labeled ground truth.

## 9. Automated Tests

The project uses Pytest.

### Run the Default Test Suite

```powershell
python -m pytest -v
```

The repository's default `pytest.ini` configuration excludes the integration tests under `tests/integration`, because those tests may make live external API calls.

### Latest Recorded Test Result

```text
15 passed
```

The latest recorded default test run completed with **15 passed and 0 failed**.

The tests include checks for application logic and worker behavior, including handling a vision provider response that does not contain usage metrics.

### Integration Tests

Integration tests that call Gemini or depend on external services must be executed separately when the required credentials, database configuration, and provider quota are available.

A previous integration test run encountered a Gemini API `429 RESOURCE_EXHAUSTED` response because the free-tier quota had been exhausted.

Consequently:

* The default test suite passed.
* The excluded integration tests are not represented by that passing result.
* The latest live Gemini integration behavior has not been fully verified after the quota error.
* A passing default test suite does not establish that all external integrations work.

## 10. AI Usage and Cost Tracking

The project contains services for estimating AI operation costs and recording usage information.

Relevant components include:

```text
app/services/ai_cost_service.py
app/services/ai_usage_service.py
app/services/embedding_service.py
app/services/image_embedding_service.py
app/workers/image_processing_worker.py
```

The implementation includes cost estimation for AI operations and usage-record persistence.

The image processing worker has also been updated to handle cases where the vision provider returns no usage information. In such cases, it avoids attempting to record usage from missing metrics.

### Cost Tracking Limitations

* Estimated costs are not necessarily identical to actual provider billing.
* If a provider does not return usage information, the corresponding usage record may not be created.
* Complete cost attribution across all vision and embedding calls must be verified using actual processing logs and database records.
* Live embedding and vision operations depend on provider credentials, quota, and model availability.

## 11. Background Processing and Failure Handling

The project includes an image processing job service and a worker.

The job service supports states such as pending, processing, completed, and failed.

The implementation includes:

* Tracking processing attempts.
* Restricting retries according to the configured attempt limit.
* Recording failure information.
* Clearing error information when a job is retried or completed.
* Handling exceptions during processing.
* Preserving failure information for diagnosis.

The configured maximum attempt count is three.

### Verification Status

Worker logic and regression tests exist, and retry behavior has been exercised in earlier integration checks.

However, the latest default test result does not independently verify every background processing scenario. Full verification should include actual database records, job status transitions, retry counts, failure logs, and successful processing of the local corpus.

## 12. Limitations and Future Improvements

VisionMatch AI contains core service-level components, but further work is required before the complete workflow can be treated as a production-ready application.

### Current Limitations

1. **Limited HTTP API:** Only the root and health endpoints are currently registered. Image ingestion, matching, and review workflows are not exposed through additional HTTP routes.

2. **Fixture-based evaluation:** The current evaluation scores are based on predefined test values. They do not establish real-world image retrieval accuracy.

3. **Database population:** The downloaded image corpus is present locally, but this alone does not prove that every image has been ingested, analyzed, and embedded in the database.

4. **External API dependency:** Gemini operations require valid credentials and available provider quota. The most recent integration run encountered a quota-related `429 RESOURCE_EXHAUSTED` response.

5. **Integration test coverage:** The default test configuration excludes integration tests that may call external services. Those tests require separate execution.

6. **End-to-end matching verification:** Real image embeddings, vector retrieval, ranking, mismatch rejection, and review workflows require additional end-to-end evidence.

7. **Cost verification:** Cost estimation code exists, but complete cost attribution for every actual AI call still needs verification.

8. **Production readiness:** The project should not be considered production-ready solely because the default tests pass or the evaluation fixtures report 100%.

### Future Improvements

* Add validated HTTP routes for image ingestion, matching, and review operations.
* Populate the database with the image corpus.
* Run real image and text embedding generation.
* Evaluate actual top-ranked image retrieval against independently labeled examples.
* Verify the fox-versus-wolf mismatch scenario using real retrieval results.
* Verify low-confidence handling with actual provider responses.
* Verify that the system returns no confident match when no candidate satisfies the configured rules.
* Run integration tests with working credentials and sufficient provider quota.
* Verify AI usage and cost records for real vision and embedding calls.
* Add end-to-end tests for the complete image processing and matching pipeline.
* Document reproducible command output and test evidence.

## 13. Quick Reference

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start configured Docker Compose services:

```powershell
docker compose up -d
```

Apply migrations:

```powershell
alembic upgrade head
```

Run the application:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Run the default test suite:

```powershell
python -m pytest -v
```

Run the evaluation:

```powershell
python -m evaluation.evaluate
```

Check the root endpoint:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Check the health endpoint:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

## 14. Repository

GitHub repository:

https://github.com/HR-Fatheen/visionmatch-ai

The repository includes the application source code, evaluation files, local dataset and attribution metadata, tests, migration configuration, and capstone documentation.

## 15. Final Status Summary

| Area                          | Current Status                                                    |
| ----------------------------- | ----------------------------------------------------------------- |
| Core service architecture     | Implemented                                                       |
| Image dataset                 | 40 categorized images across four categories, plus one test image |
| Evaluation dataset            | 10 cases                                                          |
| Fixture-based evaluation      | 19 of 19 candidate decisions correct                              |
| Default automated tests       | 15 passed                                                         |
| Gemini integration            | Requires further verification after quota exhaustion              |
| HTTP API                      | Root and health endpoints only                                    |
| Real-world retrieval accuracy | Not yet established                                               |
| Production readiness          | Further implementation and end-to-end verification required       |

VisionMatch AI establishes a foundation for semantic image-to-content matching. The current evaluation and test results provide useful evidence for specific decision logic and application behavior, while additional integration work and real-data validation are needed to demonstrate the complete matching system end to end.
