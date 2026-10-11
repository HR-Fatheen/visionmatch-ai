from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.post import Post
from app.models.post_vector import PostVector
from app.services.gemini_embedding_provider import GeminiEmbeddingProvider
from app.services.post_embedding_service import (
    generate_and_save_post_embedding,
)


load_dotenv()

db = SessionLocal()

post = Post(
    title="Red Fox in the Forest",
    content=(
        "A red fox is walking through a forest surrounded by trees "
        "and natural vegetation."
    ),
)

db.add(post)
db.commit()
db.refresh(post)

try:
    embedding_provider = GeminiEmbeddingProvider()

    post_vector = generate_and_save_post_embedding(
        db=db,
        post_id=post.id,
        text=post.content,
        embedding_provider=embedding_provider,
    )

    print(f"Post ID: {post.id}")
    print(f"Vector ID: {post_vector.id}")
    print(f"Vector dimensions: {len(post_vector.embedding)}")

    assert post_vector.post_id == post.id
    assert len(post_vector.embedding) == 3072

    print("Post embedding integration test: PASSED")

finally:
    db.query(PostVector).filter(
        PostVector.post_id == post.id
    ).delete(synchronize_session=False)

    db.delete(post)
    db.commit()
    db.close()