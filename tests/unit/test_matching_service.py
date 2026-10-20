from unittest.mock import Mock

from app.services.matching_service import find_similar_images


def test_empty_candidate_ids_returns_empty_list_without_querying_db():
    db = Mock()

    result = find_similar_images(
        db=db,
        post_vector=[1.0, 0.0],
        candidate_image_ids=[],
    )

    assert result == []
    db.execute.assert_not_called()
    db.query.assert_not_called()
