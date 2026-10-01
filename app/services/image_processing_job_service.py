from sqlalchemy.orm import Session

from app.models.image_processing_job import ImageProcessingJob


MAX_ATTEMPTS = 3


def can_retry(job: ImageProcessingJob) -> bool:
    return (
        job.status == "failed"
        and job.attempts < MAX_ATTEMPTS
    )


def create_job(
    db: Session,
    image_id: int,
) -> ImageProcessingJob:
    job = ImageProcessingJob(
        image_id=image_id,
        status="pending",
        attempts=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def mark_processing(
    db: Session,
    job: ImageProcessingJob,
) -> ImageProcessingJob:
    if job.status == "completed":
        raise ValueError(
            f"Job {job.id} is already completed"
        )

    if job.status != "pending":
        raise ValueError(
            f"Job {job.id} is not ready for processing"
        )

    if job.attempts >= MAX_ATTEMPTS:
        raise ValueError(
            f"Job {job.id} has reached the maximum number of attempts"
        )

    job.status = "processing"
    job.attempts += 1

    db.commit()
    db.refresh(job)

    return job


def mark_completed(
    db: Session,
    job: ImageProcessingJob,
) -> ImageProcessingJob:
    if job.status != "processing":
        raise ValueError(
            f"Job {job.id} cannot be completed from status '{job.status}'"
        )

    job.status = "completed"
    job.last_error = None

    db.commit()
    db.refresh(job)

    return job


def mark_failed(
    db: Session,
    job: ImageProcessingJob,
    error: str,
) -> ImageProcessingJob:
    if job.status != "processing":
        raise ValueError(
            f"Job {job.id} cannot be marked failed from status '{job.status}'"
        )

    job.status = "failed"
    job.last_error = error

    db.commit()
    db.refresh(job)

    return job


def retry_job(
    db: Session,
    job: ImageProcessingJob,
) -> ImageProcessingJob:
    if not can_retry(job):
        raise ValueError(
            f"Job {job.id} cannot be retried"
        )

    job.status = "pending"
    job.last_error = None

    db.commit()
    db.refresh(job)

    return job