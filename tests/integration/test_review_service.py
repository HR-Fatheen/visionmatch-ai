from app.database import SessionLocal
from app.models.image import Image
from app.models.match_result import MatchResult
from app.models.post import Post
from app.models.post_vector import PostVector
from app.models.review import Review
from app.services.review_service import create_review


def test_review_service():
    db = SessionLocal()

    post = None
    image = None
    match_result = None

    try:
        # Create test post
        post = Post(
            title="Review test post",
            content="A red fox in a forest.",
        )
        db.add(post)
        db.commit()
        db.refresh(post)

        # Create test image
        image = Image(
            filename="review-test.jpg",
            filepath="data/images/review-test.jpg",
            tags="red fox,wildlife",
            confidence=0.90,
        )
        db.add(image)
        db.commit()
        db.refresh(image)

        # Create match result
        match_result = MatchResult(
            post_id=post.id,
            image_id=image.id,
            similarity_score=0.85,
            accepted=True,
            explanation="Match passed all guard checks.",
        )
        db.add(match_result)
        db.commit()
        db.refresh(match_result)

        # Test approval review
        review = create_review(
            db=db,
            match_result_id=match_result.id,
            decision="approved",
            feedback="Correct image for the article.",
        )

        assert review.id is not None
        assert review.match_result_id == match_result.id
        assert review.reviewer_decision is True
        assert review.notes == "Correct image for the article."

        # Test rejection review
        rejected_review = create_review(
            db=db,
            match_result_id=match_result.id,
            decision="rejected",
            feedback="Reviewer found a better image.",
        )

        assert rejected_review.id is not None
        assert rejected_review.reviewer_decision is False
        assert rejected_review.notes == "Reviewer found a better image."

        # Test invalid decision
        try:
            create_review(
                db=db,
                match_result_id=match_result.id,
                decision="invalid",
            )
            raise AssertionError(
                "Expected ValueError for invalid decision"
            )
        except ValueError as exc:
            assert "approved" in str(exc)
            assert "rejected" in str(exc)

        # Test nonexistent match result
        try:
            create_review(
                db=db,
                match_result_id=999999,
                decision="approved",
            )
            raise AssertionError(
                "Expected ValueError for missing match result"
            )
        except ValueError as exc:
            assert "does not exist" in str(exc)

        print("Review service test: PASSED")

    finally:
        try:
            # Delete dependent records before parent records.
            db.rollback()

            if match_result is not None and match_result.id is not None:
                db.query(Review).filter(
                    Review.match_result_id == match_result.id
                ).delete(synchronize_session=False)

                db.query(MatchResult).filter(
                    MatchResult.id == match_result.id
                ).delete(synchronize_session=False)

            if post is not None and post.id is not None:
                db.query(PostVector).filter(
                    PostVector.post_id == post.id
                ).delete(synchronize_session=False)

            if image is not None and image.id is not None:
                db.query(Image).filter(
                    Image.id == image.id
                ).delete(synchronize_session=False)

            if post is not None and post.id is not None:
                db.query(Post).filter(
                    Post.id == post.id
                ).delete(synchronize_session=False)

            db.commit()

        finally:
            db.close()


if __name__ == "__main__":
    test_review_service()