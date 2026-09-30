# AI Image Understanding & Content Matching Engine

## 1. Problem

Build a backend service that understands an image library, automatically
organizes images using AI-generated structured metadata, and matches images
to blog posts based on semantic meaning rather than filenames or keywords.

The system should recommend a suitable image when confidence is sufficient
and safely reject a candidate when the system cannot establish a reliable
match.

## 2. Core Workflow

Images are processed through a vision model to generate structured metadata:

- subject
- category
- attributes
- caption
- confidence

The generated output is validated before being stored.

Image captions and blog post content are converted into embeddings.
The embeddings are used to rank candidate images by semantic similarity.

A mismatch guard then evaluates the candidate using:

- extracted tags
- semantic similarity
- confidence
- configured thresholds

The system either returns a suggested image with an explanation or rejects
the recommendation with an explanation.

## 3. Architecture

Images
    |
    v
Background Vision Job
    |
    v
Vision Model
    |
    v
Structured Metadata
    |
    v
Schema Validation
    |
    +----> Low Confidence -> Review
    |
    v
Image Caption Embedding
    |
    v
Vector Storage


Blog Post
    |
    v
Post Embedding
    |
    v
Similarity Ranking
    |
    v
Mismatch Guard
    |
    +----> Suggested Image
    |
    +----> No Good Match


Suggested/Rejected Result
    |
    v
Review API

## 4. Data Model

### Image

- id
- filename
- path
- subject
- category
- attributes
- caption
- confidence
- processing_status
- created_at
- updated_at

### Image Vector

- image_id
- embedding
- model
- created_at

### Post

- id
- title
- content
- created_at
- updated_at

### Post Vector

- post_id
- embedding
- model
- created_at

### Match Result

- id
- post_id
- image_id
- similarity_score
- guard_status
- explanation
- created_at

### Review

- id
- match_result_id
- decision
- reviewer_note
- created_at

### AI Usage

- id
- operation
- model
- input_units
- output_units
- estimated_cost
- created_at

## 5. API Surface

### Images

POST /images

Upload/register an image.

GET /images

List images and their processing status.

GET /images/{image_id}

Retrieve image metadata.

POST /images/process

Start batch processing.

### Posts

POST /posts

Create a blog post.

GET /posts

List blog posts.

GET /posts/{post_id}

Retrieve a blog post.

GET /posts/{post_id}/images

Return ranked image recommendations for a post.

### Reviews

POST /reviews

Approve or reject a suggested pairing.

GET /reviews

List review records.

### Jobs

POST /jobs/process-images

Start image processing.

GET /jobs/{job_id}

Check batch-job progress and status.

### Evaluation

POST /evaluation/run

Run the labeled evaluation set.

GET /evaluation/results

Retrieve evaluation results.

## 6. Matching Decision

The matching system first ranks candidates using semantic similarity.

The mismatch guard then determines whether the highest-ranked candidate
should actually be accepted.

A candidate may be rejected when:

1. semantic similarity is below the configured threshold;
2. image classification confidence is too low;
3. extracted tags indicate an incompatible category or subject.

Every rejection should contain an explanation.

## 7. Evaluation

The project will contain a labeled evaluation dataset with at least
10 blog posts.

Each post will have one manually identified correct image.

The primary metric will be top-1 precision.

The project will compare:

1. embedding-only retrieval;
2. retrieval with the mismatch guard.

The evaluation will also record rejected candidates and failure cases.

## 8. Background Processing

Vision and embedding operations will run through background jobs rather than
blocking normal API requests.

Jobs must support:

- progress tracking
- retries
- failure status
- per-call AI cost tracking
- idempotent processing

## 9. Non-Goals

A full production image-management frontend is explicitly out of scope.

The capstone can be demonstrated through API endpoints, Swagger/OpenAPI,
evaluation output, and a simple review interface if needed.

## 10. Initial Dataset

Target:

- at least 40 images
- at least 4 categories
- at least 10 evaluation posts

The initial dataset will focus on visually and semantically related
categories so that both correct retrieval and mismatch rejection can be
demonstrated.