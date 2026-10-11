from app.models.image import Image
from app.services.match_result import RankedImage
from app.services.mismatch_guard import (
    CONFIDENCE_THRESHOLD,
    SIMILARITY_THRESHOLD,
    evaluate_confidence,
    evaluate_match,
    evaluate_similarity,
    evaluate_tags,
)


def test_accepts_high_similarity_match():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_similarity(result)

    assert decision.accepted is True
    assert "meets" in decision.explanation


def test_rejects_low_similarity_match():
    image = Image(
        filename="wolf.jpg",
        filepath="data/images/wolf.jpg",
    )

    result = RankedImage(
        image=image,
        similarity_score=0.30,
    )

    decision = evaluate_similarity(result)

    assert decision.accepted is False
    assert "below" in decision.explanation


def test_accepts_high_confidence_match():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_confidence(result)

    assert decision.accepted is True
    assert "meets" in decision.explanation


def test_rejects_low_confidence_match():
    image = Image(
        filename="uncertain.jpg",
        filepath="data/images/uncertain.jpg",
        confidence=0.50,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_confidence(result)

    assert decision.accepted is False
    assert "below" in decision.explanation


def test_rejects_missing_confidence():
    image = Image(
        filename="unknown.jpg",
        filepath="data/images/unknown.jpg",
        confidence=None,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_confidence(result)

    assert decision.accepted is False
    assert "unavailable" in decision.explanation


def test_accepts_matching_tag():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
        tags="red fox,wildlife,animal",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_tags(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is True
    assert "required content tag" in decision.explanation


def test_rejects_non_matching_tag():
    image = Image(
        filename="wolf.jpg",
        filepath="data/images/wolf.jpg",
        tags="wolf,wildlife,animal",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_tags(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is False
    assert "do not match" in decision.explanation


def test_rejects_missing_tags():
    image = Image(
        filename="unknown.jpg",
        filepath="data/images/unknown.jpg",
        tags=None,
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_tags(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is False
    assert "unavailable" in decision.explanation


def test_accepts_match_when_all_checks_pass():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
        tags="red fox,wildlife,animal",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_match(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is True
    assert "all" in decision.explanation


def test_rejects_match_when_similarity_fails():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
        tags="red fox,wildlife,animal",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.30,
    )

    decision = evaluate_match(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is False
    assert "similarity" in decision.explanation


def test_rejects_match_when_confidence_fails():
    image = Image(
        filename="fox.jpg",
        filepath="data/images/fox.jpg",
        tags="red fox,wildlife,animal",
        confidence=0.50,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_match(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is False
    assert "confidence" in decision.explanation


def test_rejects_match_when_tags_fail():
    image = Image(
        filename="wolf.jpg",
        filepath="data/images/wolf.jpg",
        tags="wolf,wildlife,animal",
        confidence=0.90,
    )

    result = RankedImage(
        image=image,
        similarity_score=0.85,
    )

    decision = evaluate_match(
        result,
        required_tags=["red fox"],
    )

    assert decision.accepted is False
    assert "tags" in decision.explanation


def test_thresholds_are_documented():
    assert SIMILARITY_THRESHOLD == 0.60
    assert CONFIDENCE_THRESHOLD == 0.70


if __name__ == "__main__":
    test_accepts_high_similarity_match()
    test_rejects_low_similarity_match()
    test_accepts_high_confidence_match()
    test_rejects_low_confidence_match()
    test_rejects_missing_confidence()
    test_accepts_matching_tag()
    test_rejects_non_matching_tag()
    test_rejects_missing_tags()
    test_accepts_match_when_all_checks_pass()
    test_rejects_match_when_similarity_fails()
    test_rejects_match_when_confidence_fails()
    test_rejects_match_when_tags_fail()
    test_thresholds_are_documented()

    print("Mismatch guard tests: PASSED")
