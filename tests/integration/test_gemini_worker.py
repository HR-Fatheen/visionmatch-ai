from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.ai_usage import AIUsage
from app.models.image import Image
from app.models.image_processing_job import ImageProcessingJob
from app.services.gemini_vision_provider import GeminiVisionProvider
from app.services.image_processing_job_service import create_job
from app.workers.image_processing_worker import process_job


load_dotenv()

image_path = "data/images/gemini-test.jpg"

db = SessionLocal()

try:
    image = Image(
        filename="gemini-worker-test.jpg",
        filepath=image_path,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    job = create_job(
        db=db,
        image_id=image.id,
    )

    provider = GeminiVisionProvider()

    result = process_job(
        db=db,
        job=job,
        vision_provider=provider,
    )

    db.refresh(image)

    usage = (
        db.query(AIUsage)
        .filter(
            AIUsage.operation == "vision_analysis",
            AIUsage.model_name == "gemini-2.5-flash",
        )
        .order_by(AIUsage.id.desc())
        .first()
    )

    print("Job status:", result.status)
    print("Attempts:", result.attempts)
    print("Image caption:", image.caption)
    print("Image tags:", image.tags)
    print("Image confidence:", image.confidence)

    assert result.status == "completed"
    assert image.caption
    assert image.tags
    assert image.confidence is not None
    assert usage is not None

    print("Usage ID:", usage.id)
    print("Input units:", usage.input_units)
    print("Output units:", usage.output_units)
    print("Estimated cost:", usage.estimated_cost)

    assert usage.input_units > 0
    assert usage.output_units > 0
    assert usage.estimated_cost > 0

    print("Gemini worker integration test: PASSED")

finally:
    # Delete the AI usage record created by this test.
    if "usage" in locals() and usage is not None:
        db.delete(usage)
        db.commit()

    # Job must be deleted before image because of the foreign key.
    if "job" in locals():
        db.delete(job)
        db.commit()

    if "image" in locals():
        db.delete(image)
        db.commit()

    db.close()

    print("Cleanup: done")