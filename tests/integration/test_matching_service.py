from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.image import Image
from app.models.image_vector import ImageVector
from app.services.matching_service import find_similar_images


load_dotenv()

db = SessionLocal()

try:
    images = [
        Image(
            filename="match-test-a.jpg",
            filepath="data/images/match-test-a.jpg",
        ),
        Image(
            filename="match-test-b.jpg",
            filepath="data/images/match-test-b.jpg",
        ),
        Image(
            filename="match-test-c.jpg",
            filepath="data/images/match-test-c.jpg",
        ),
    ]

    db.add_all(images)
    db.commit()

    for image in images:
        db.refresh(image)

    vectors = [
        [1.0] + [0.0] * 3071,
        [0.9] + [0.1] * 3071,
        [-1.0] + [0.0] * 3071,
    ]

    for image, vector in zip(images, vectors):
        db.add(
            ImageVector(
                image_id=image.id,
                embedding=vector,
            )
        )

    db.commit()

    query_vector = [1.0] + [0.0] * 3071

    results = find_similar_images(
        db=db,
        post_vector=query_vector,
        limit=3,
        candidate_image_ids=[image.id for image in images],
    )

    print("Ranking results:")

    for result in results:
        print(
            f"{result.image.filename}: "
            f"similarity={result.similarity_score:.4f}"
        )

        result_image_ids = [
        result.image.id
        for result in results
    ]

    expected_image_ids = {
        image.id
        for image in images
    }

    assert len(results) == 3, (
        f"Expected 3 results, got {len(results)}: "
        f"{[(r.image.filename, r.similarity_score) for r in results]}"
    )

    assert set(result_image_ids) == expected_image_ids, (
        f"Expected image IDs {expected_image_ids}, "
        f"but got {result_image_ids}"
    )

    assert results[0].image.filename == "match-test-a.jpg"
    assert results[0].similarity_score > results[1].similarity_score
    assert results[1].similarity_score > results[2].similarity_score

    print("Semantic ranking test: PASSED")

finally:
    for image in images:
        db.query(ImageVector).filter(
            ImageVector.image_id == image.id
        ).delete(synchronize_session=False)

    for image in images:
        db.delete(image)

    db.commit()
    db.close()