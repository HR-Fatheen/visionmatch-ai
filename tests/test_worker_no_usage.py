from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.image import Image
from app.models.image_processing_job import ImageProcessingJob
from app.services.vision_analysis_result import VisionAnalysisResult
from app.services.vision_schema import VisionMetadata
from app.workers.image_processing_worker import process_job


class NoUsageVisionProvider:
    def analyze_image(self, image_path):
        metadata = VisionMetadata(
            caption="Test image",
            tags=["test"],
            confidence=0.9,
        )
        return VisionAnalysisResult(metadata=metadata, usage=None)


def test_worker_completes_when_usage_is_none():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        image = Image(filename="test.jpg", filepath="test.jpg")
        db.add(image)
        db.commit()
        db.refresh(image)

        job = ImageProcessingJob(
            image_id=image.id,
            status="pending",
            attempts=0,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        result = process_job(db, job, NoUsageVisionProvider())

        assert result.status == "completed"
        db.refresh(image)
        assert image.caption == "Test image"
    finally:
        db.close()
        engine.dispose()
