from pathlib import Path

from sqlalchemy.orm import Session

from app.models.image import Image
from app.services.image_service import save_vision_metadata
from app.services.vision_provider import VisionProvider
from app.services.vision_service import is_low_confidence


def ingest_image(
    db: Session,
    image_path: str,
    vision_provider: VisionProvider,
) -> tuple[Image, bool]:

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image(
        filename=path.name,
        filepath=str(path),
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    metadata = vision_provider.analyze_image(image_path)

    low_confidence = is_low_confidence(metadata)

    save_vision_metadata(
        db=db,
        image_id=image.id,
        metadata=metadata,
    )

    return image, low_confidence