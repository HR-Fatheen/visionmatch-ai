from app.database import SessionLocal
from app.models.image import Image
from app.models.match_result import MatchResult
from app.models.post import Post
from app.services.match_result import RankedImage
from app.services.match_result_service import evaluate_and_save_match


def test_match_result_service():
    db = SessionLocal()

    post = None
    image_pass = None
    image_fail = None

    try:
        # Create test post
        post = Post(
            title="Red fox wildlife article",
            content="A red fox standing in a forest."
        )
        db.add(post)
        db.commit()
        db.refresh(post)

        # Image that should pass the guard
        image_pass = Image(
            filename="service-fox.jpg",
            filepath="data/images/service-fox.jpg",
            tags="red fox,wildlife,animal",
            confidence=0.90,
        )
        db.add(image_pass)
        db.commit()
        db.refresh(image_pass)

        ranked_pass = RankedImage(
            image=image_pass,
            similarity_score=0.85,
        )

        saved_pass = evaluate_and_save_match(
            db=db,
            post_id=post.id,
            result=ranked_pass,
            required_tags=["red fox"],
        )

        assert saved_pass.id is not None
        assert saved_pass.post_id == post.id
        assert saved_pass.image_id == image_pass.id
        assert saved_pass.similarity_score == 0.85
        assert saved_pass.accepted is True
        assert "all" in saved_pass.explanation

        # Image that should fail because tags do not match
        image_fail = Image(
            filename="service-wolf.jpg",
            filepath="data/images/service-wolf.jpg",
            tags="wolf,wildlife,animal",
            confidence=0.90,
        )
        db.add(image_fail)
        db.commit()
        db.refresh(image_fail)

        ranked_fail = RankedImage(
            image=image_fail,
            similarity_score=0.85,
        )

        saved_fail = evaluate_and_save_match(
            db=db,
            post_id=post.id,
            result=ranked_fail,
            required_tags=["red fox"],
        )

        assert saved_fail.id is not None
        assert saved_fail.post_id == post.id
        assert saved_fail.image_id == image_fail.id
        assert saved_fail.accepted is False
        assert "tags" in saved_fail.explanation

        print("Match result service test: PASSED")

    finally:
        # MatchResult rows must be deleted before their parent records
        if post is not None:
            db.query(MatchResult).filter(
                MatchResult.post_id == post.id
            ).delete(synchronize_session=False)

        if image_pass is not None:
            db.delete(image_pass)

        if image_fail is not None:
            db.delete(image_fail)

        if post is not None:
            db.delete(post)

        db.commit()
        db.close()


if __name__ == "__main__":
    test_match_result_service()