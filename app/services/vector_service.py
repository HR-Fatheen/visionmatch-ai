from sqlalchemy.orm import Session

from app.models.image_vector import ImageVector
from app.models.post_vector import PostVector


def save_image_vector(
    db: Session,
    image_id: int,
    vector: list[float],
) -> ImageVector:
    image_vector = db.query(ImageVector).filter(
        ImageVector.image_id == image_id
    ).first()

    if image_vector is None:
        image_vector = ImageVector(
            image_id=image_id,
            embedding=vector,
        )
        db.add(image_vector)
    else:
        image_vector.embedding = vector

    db.commit()
    db.refresh(image_vector)

    return image_vector


def save_post_vector(
    db: Session,
    post_id: int,
    vector: list[float],
) -> PostVector:
    post_vector = db.query(PostVector).filter(
        PostVector.post_id == post_id
    ).first()

    if post_vector is None:
        post_vector = PostVector(
            post_id=post_id,
            embedding=vector,
        )
        db.add(post_vector)
    else:
        post_vector.embedding = vector

    db.commit()
    db.refresh(post_vector)

    return post_vector