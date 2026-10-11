from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.image import Image
from app.models.image_vector import ImageVector
from app.models.post import Post
from app.models.post_vector import PostVector
from app.services.gemini_embedding_provider import GeminiEmbeddingProvider
from app.services.post_embedding_service import (
    generate_and_save_post_embedding,
)
from app.services.post_matching_service import find_images_for_post


load_dotenv()

db = SessionLocal()

post = Post(
    title="Red Fox in the Forest",
    content=(
        "A red fox is walking through a forest surrounded by trees "
        "and natural vegetation."
    ),
)

images = [
    Image(
        filename="fox-test.jpg",
        filepath="data/images/fox-test.jpg",
    ),
    Image(
        filename="wolf-test.jpg",
        filepath="data/images/wolf-test.jpg",
    ),
]

db.add(post)
db.add_all(images)
db.commit()

db.refresh(post)

for image in images:
    db.refresh(image)

try:
    embedding_provider = GeminiEmbeddingProvider()

    # Generate the real embedding for the post.
    post_vector = generate_and_save_post_embedding(
        db=db,
        post_id=post.id,
        text=post.content,
        embedding_provider=embedding_provider,
    )

    # Use controlled vectors for the image candidates.
    #
    # The first image points in the same direction as the post vector.
    # The second points in the opposite direction.
    query_vector = list(post_vector.embedding)

    db.add(
        ImageVector(
            image_id=images[0].id,
            embedding=query_vector,
        )
    )

    db.add(
        ImageVector(
            image_id=images[1].id,
            embedding=[-value for value in query_vector],
        )
    )

    db.commit()

    results = find_images_for_post(
        db=db,
        post_id=post.id,
        limit=2,
    )

    print("Post matching results:")

    for result in results:
        print(
            f"{result.image.filename}: "
            f"similarity={result.similarity_score:.4f}"
        )

    assert len(results) == 2
    assert results[0].image.filename == "fox-test.jpg"
    assert results[0].similarity_score > results[1].similarity_score

    print("Post-to-image matching test: PASSED")

finally:
    db.query(ImageVector).filter(
        ImageVector.image_id.in_([image.id for image in images])
    ).delete(synchronize_session=False)

    db.query(PostVector).filter(
        PostVector.post_id == post.id
    ).delete(synchronize_session=False)

    for image in images:
        db.delete(image)

    db.delete(post)

    db.commit()
    db.close()