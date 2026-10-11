from sqlalchemy.orm import Session

from app.models.match_result import MatchResult
from app.models.review import Review


def create_review(
    db: Session,
    match_result_id: int,
    decision: str,
    feedback: str | None = None,
) -> Review:
    if decision not in {"approved", "rejected"}:
        raise ValueError("Decision must be 'approved' or 'rejected'.")

    match_result = (
        db.query(MatchResult)
        .filter(MatchResult.id == match_result_id)
        .first()
    )

    if match_result is None:
        raise ValueError(
            f"Match result {match_result_id} does not exist."
        )

    review = Review(
        match_result_id=match_result_id,
        reviewer_decision=(decision == "approved"),
        notes=feedback,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review