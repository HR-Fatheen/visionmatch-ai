import os

from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.image import Image
from app.services.gemini_vision_provider import GeminiVisionProvider
from app.services.image_ingestion import ingest_image

load_dotenv()

image_path = "data/images/gemini-test.jpg"

if not os.path.exists(image_path):
    raise FileNotFoundError(
        f"Test image not found: {image_path}"
    )

db = SessionLocal()

image = None

try:
    provider = GeminiVisionProvider()

    image, low_confidence = ingest_image(
        db=db,
        image_path=image_path,
        vision_provider=provider,
    )

    print("Image ID:", image.id)
    print("Filename:", image.filename)
    print("Caption:", image.caption)
    print("Tags:", image.tags)
    print("Confidence:", image.confidence)
    print("Low confidence:", low_confidence)

    assert image.caption
    assert image.tags
    assert image.confidence is not None
    assert 0.0 <= image.confidence <= 1.0

    print("Gemini ingestion test: PASSED")

finally:
    if image is not None:
        db.delete(image)
        db.commit()

    db.close()

    print("Cleanup: done")