from sqlalchemy.orm import Session

from app.services.embedding_provider import EmbeddingProvider
from app.services.post_embedding_service import generate_and_save_post_embedding
from app.services.post_matching_service import find_images_for_post
from app.services.match_result_service import evaluate_and_save_match


def match_post_to_images(
    db: Session,
    post_id: int,
    post_text: str,
    required_tags: list[str],
    embedding_provider: EmbeddingProvider,
    limit: int = 5,
    candidate_image_ids: list[int] | None = None,
):
    # Generate and persist the post embedding
    generate_and_save_post_embedding(
        db=db,
        post_id=post_id,
        text=post_text,
        embedding_provider=embedding_provider,
    )

    # Retrieve semantically ranked image candidates
    ranked_images = find_images_for_post(
    db=db,
    post_id=post_id,
    limit=limit,
    candidate_image_ids=candidate_image_ids,
    )

    # Apply mismatch guard and persist every candidate decision
    results = []

    for ranked_image in ranked_images:
        match_result = evaluate_and_save_match(
            db=db,
            post_id=post_id,
            result=ranked_image,
            required_tags=required_tags,
        )
        results.append(match_result)

    return results