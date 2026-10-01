from sqlalchemy.orm import Session

from app.models.image import Image
from app.services.vision_schema import VisionMetadata


def save_vision_metadata(
    db: Session,
    image_id: int,
    metadata: VisionMetadata,
) -> Image:
    image = db.get(Image, image_id)

    if image is None:
        raise ValueError(f"Image {image_id} not found")

    image.caption = metadata.caption
    image.tags = ",".join(metadata.tags)
    image.confidence = metadata.confidence

    db.commit()
    db.refresh(image)

    return image