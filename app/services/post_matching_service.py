from sqlalchemy.orm import Session

from app.models.post_vector import PostVector
from app.services.matching_service import find_similar_images

def find_images_for_post(
        db: Session,
        post_id: int,
        limit: int = 5,
        candidate_image_ids: list[int] | None = None,
    ):
    post_vector = (
        db.query(PostVector)
        .filter(PostVector.post_id == post_id)
        .first()
    )


    if post_vector is None:
        raise ValueError(
            f"No embedding found for post {post_id}"
        )

    return find_similar_images(
        db=db,
        post_vector=post_vector.embedding,
        limit=limit,
        candidate_image_ids=candidate_image_ids,
    )
