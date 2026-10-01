from app.database import SessionLocal
from app.models.image import Image
from app.services.image_processing_job_service import create_job
from app.workers.image_processing_worker import process_with_retries
from app.services.vision_provider import VisionProvider
from app.services.vision_schema import VisionMetadata


class FailingVisionProvider(VisionProvider):
    def analyze_image(self, image_path: str) -> VisionMetadata:
        raise RuntimeError("Simulated vision provider failure")


db = SessionLocal()

try:
    image = Image(
        filename="retry-test.jpg",
        filepath="data/images/retry-test.jpg",
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    job = create_job(db, image.id)

    result = process_with_retries(
        db=db,
        job=job,
        vision_provider=FailingVisionProvider(),
    )

    print("Final status:", result.status)
    print("Attempts:", result.attempts)
    print("Last error:", result.last_error)

    assert result.status == "failed"
    assert result.attempts == 3
    assert result.last_error == "Simulated vision provider failure"

    print("Retry test: PASSED")

finally:
    # Delete job first because it references the image.
    db.query(type(job)).filter(type(job).id == job.id).delete()
    db.commit()

    db.query(Image).filter(Image.id == image.id).delete()
    db.commit()

    db.close()

    print("Cleanup: done")