from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.post import Post
from app.models.post_vector import PostVector
from app.services.vector_service import save_post_vector


load_dotenv()

db = SessionLocal()

try:
    post = Post(
        title="Vector test post",
        content="A red fox standing in a forest.",
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    vector = [0.002] * 3072

    saved_vector = save_post_vector(
        db=db,
        post_id=post.id,
        vector=vector,
    )

    print("Post ID:", post.id)
    print("Vector ID:", saved_vector.id)
    print("Vector dimensions:", len(saved_vector.embedding))

    assert saved_vector.post_id == post.id
    assert len(saved_vector.embedding) == 3072

    stored_vector = db.query(PostVector).filter(
        PostVector.post_id == post.id
    ).first()

    assert stored_vector is not None
    assert len(stored_vector.embedding) == 3072

    print("Post vector storage test: PASSED")

finally:
    db.close()