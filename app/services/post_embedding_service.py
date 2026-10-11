from sqlalchemy.orm import Session

from app.services.embedding_provider import EmbeddingProvider
from app.services.embedding_service import generate_embedding
from app.services.vector_service import save_post_vector


def generate_and_save_post_embedding(
    db: Session,
    post_id: int,
    text: str,
    embedding_provider: EmbeddingProvider,
):
    result = generate_embedding(
        db=db,
        text=text,
        embedding_provider=embedding_provider,
    )

    return save_post_vector(
        db=db,
        post_id=post_id,
        vector=result.vector,
    )