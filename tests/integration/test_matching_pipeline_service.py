from app.database import SessionLocal
from app.models.image import Image
from app.models.image_vector import ImageVector
from app.models.match_result import MatchResult
from app.models.post import Post
from app.models.post_vector import PostVector
from app.services.embedding_result import EmbeddingResult
from app.services.embedding_provider import EmbeddingProvider
from app.services.matching_pipeline_service import match_post_to_images


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed_text(self, text: str) -> EmbeddingResult:
        vector = [0.0] * 3072
        vector[0] = 1.0

        return EmbeddingResult(
            vector=vector,
            model_name="test-embedding-model",
            input_units=1,
        )


def test_matching_pipeline():
    db = SessionLocal()

    post = None
    image_fox = None
    image_wolf = None

    try:
        # Create test post
        post = Post(
            title="Red fox wildlife article",
            content="A red fox standing in a forest.",
        )
        db.add(post)
        db.commit()
        db.refresh(post)

        # Create matching fox image
        image_fox = Image(
            filename="pipeline-fox.jpg",
            filepath="data/images/pipeline-fox.jpg",
            tags="red fox,wildlife,animal",
            confidence=0.90,
        )

        # Create non-matching wolf image
        image_wolf = Image(
            filename="pipeline-wolf.jpg",
            filepath="data/images/pipeline-wolf.jpg",
            tags="wolf,wildlife,animal",
            confidence=0.90,
        )

        db.add_all([image_fox, image_wolf])
        db.commit()
        db.refresh(image_fox)
        db.refresh(image_wolf)

        # Controlled vectors:
        # fox = identical to post vector
        # wolf = opposite vector
        fox_vector = [0.0] * 3072
        fox_vector[0] = 1.0

        wolf_vector = [0.0] * 3072
        wolf_vector[0] = -1.0

        db.add(
            ImageVector(
                image_id=image_fox.id,
                embedding=fox_vector,
            )
        )

        db.add(
            ImageVector(
                image_id=image_wolf.id,
                embedding=wolf_vector,
            )
        )

        db.commit()

        # Run the complete pipeline
        results = match_post_to_images(
            db=db,
            post_id=post.id,
            post_text=post.content,
            required_tags=["red fox"],
            embedding_provider=FakeEmbeddingProvider(),
            limit=2,
            candidate_image_ids=[image_fox.id, image_wolf.id],
        )

        assert len(results) == 2

        print("Pipeline results:")
        for result in results:
            print(
                f"image_id={result.image_id}, "
                f"accepted={result.accepted}, "
                f"similarity={result.similarity_score:.4f}, "
                f"explanation={result.explanation}"
            )

        # Highest-ranked candidate should be the fox
        assert results[0].image_id == image_fox.id
        assert results[0].accepted is True
        assert results[0].similarity_score > 0.99

        # Wolf should be rejected by the mismatch guard
        wolf_result = next(
            result for result in results
            if result.image_id == image_wolf.id
        )

        assert wolf_result.accepted is False
        assert "similarity" in wolf_result.explanation

        # Verify results were actually persisted
        saved_results = (
            db.query(MatchResult)
            .filter(MatchResult.post_id == post.id)
            .all()
        )

        assert len(saved_results) == 2

        print("Matching pipeline test: PASSED")

    finally:

        db.rollback()

        if post is not None:
            db.query(MatchResult).filter(
                MatchResult.post_id == post.id
            ).delete(synchronize_session=False)

            db.query(PostVector).filter(
                PostVector.post_id == post.id
            ).delete(synchronize_session=False)

        if image_fox is not None:
            db.query(ImageVector).filter(
                ImageVector.image_id == image_fox.id
            ).delete(synchronize_session=False)

            db.delete(image_fox)

        if image_wolf is not None:
            db.query(ImageVector).filter(
                ImageVector.image_id == image_wolf.id
            ).delete(synchronize_session=False)

            db.delete(image_wolf)

        if post is not None:
            db.delete(post)

        db.commit()
        db.close()


if __name__ == "__main__":
    test_matching_pipeline()