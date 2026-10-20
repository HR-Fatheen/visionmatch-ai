from sqlalchemy.orm import Session
from app.services.ai_cost_service import estimate_gemini_cost
from app.services.ai_usage_service import record_ai_usage
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

        result = vision_provider.analyze_image(
            image.filepath
        )

        metadata = result.metadata

        if result.usage is not None:
            estimated_cost = estimate_gemini_cost(
                input_units=result.usage.input_units,
                output_units=result.usage.output_units,
            )

            record_ai_usage(
                db=db,
                operation="vision_analysis",
                model_name=result.usage.model_name,
                input_units=result.usage.input_units,
                output_units=result.usage.output_units,
                estimated_cost=estimated_cost,
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