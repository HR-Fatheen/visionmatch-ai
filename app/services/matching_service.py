from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.image_vector import ImageVector
from app.services.match_result import RankedImage


def find_similar_images(
    db: Session,
    post_vector: list[float],
    limit: int = 5,
    candidate_image_ids: list[int] | None = None,
) -> list[RankedImage]:
    distance = ImageVector.embedding.cosine_distance(post_vector)

    statement = (
        select(Image, distance.label("distance"))
        .join(
            ImageVector,
            ImageVector.image_id == Image.id,
        )
    )

    if candidate_image_ids is not None:
        if not candidate_image_ids:
            return []

        statement = statement.where(
            Image.id.in_(candidate_image_ids)
        )

    statement = (
        statement
        .order_by(distance)
        .limit(limit)
    )

    results = db.execute(statement).all()

    return [
        RankedImage(
            image=image,
            similarity_score=1.0 - float(distance_value),
        )
        for image, distance_value in results
    ]