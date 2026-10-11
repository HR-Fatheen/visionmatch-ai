from sqlalchemy.orm import Session

from app.models.match_result import MatchResult
from app.services.match_result import RankedImage
from app.services.mismatch_guard import evaluate_match


def evaluate_and_save_match(
    db: Session,
    post_id: int,
    result: RankedImage,
    required_tags: list[str],
) -> MatchResult:
    decision = evaluate_match(
        result=result,
        required_tags=required_tags,
    )

    match_result = MatchResult(
        post_id=post_id,
        image_id=result.image.id,
        similarity_score=result.similarity_score,
        accepted=decision.accepted,
        explanation=decision.explanation,
    )

    db.add(match_result)
    db.commit()
    db.refresh(match_result)

    return match_result