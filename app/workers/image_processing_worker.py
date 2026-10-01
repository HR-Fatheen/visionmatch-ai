from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.image_processing_job import ImageProcessingJob
from app.services.image_service import save_vision_metadata
from app.services.image_processing_job_service import (
    can_retry,
    mark_completed,
    mark_failed,
    mark_processing,
    retry_job,
)
from app.services.vision_provider import VisionProvider


def process_job(
    db: Session,
    job: ImageProcessingJob,
    vision_provider: VisionProvider,
) -> ImageProcessingJob:
    """
    Process one image-processing job.

    Flow:
    pending → processing → completed

    Any processing error:
    processing → failed
    """

    job = mark_processing(db, job)

    try:
        image = db.get(Image, job.image_id)

        if image is None:
            raise ValueError(
                f"Image {job.image_id} not found"
            )

        metadata = vision_provider.analyze_image(
            image.filepath
        )

        save_vision_metadata(
            db=db,
            image_id=image.id,
            metadata=metadata,
        )

        job = mark_completed(db, job)

        return job

    except Exception as exc:
        mark_failed(
            db=db,
            job=job,
            error=str(exc),
        )

        raise


def process_with_retries(
    db: Session,
    job: ImageProcessingJob,
    vision_provider: VisionProvider,
) -> ImageProcessingJob:
    """
    Process a job and retry failed processing until
    the maximum attempt count is reached.

    Logs an error when the job exhausts all retries.
    """

    while True:
        try:
            return process_job(
                db=db,
                job=job,
                vision_provider=vision_provider,
            )

        except Exception:
            db.refresh(job)

            if not can_retry(job):
                print(
                    f"ALERT: Image processing job {job.id} "
                    f"failed after {job.attempts} attempts. "
                    f"Error: {job.last_error}"
                )

                return job

            job = retry_job(
                db=db,
                job=job,
            )