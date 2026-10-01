from sqlalchemy.orm import Session

from app.models.image_processing_job import ImageProcessingJob


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
    job.status = "processing"
    job.attempts += 1

    db.commit()
    db.refresh(job)

    return job


def mark_completed(
    db: Session,
    job: ImageProcessingJob,
) -> ImageProcessingJob:
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
    job.status = "failed"
    job.last_error = error

    db.commit()
    db.refresh(job)

    return job