from dataclasses import dataclass

from app.services.match_result import RankedImage


SIMILARITY_THRESHOLD = 0.60
CONFIDENCE_THRESHOLD = 0.70


@dataclass
class GuardDecision:
    accepted: bool
    explanation: str


def evaluate_similarity(
    result: RankedImage,
) -> GuardDecision:
    if result.similarity_score < SIMILARITY_THRESHOLD:
        return GuardDecision(
            accepted=False,
            explanation=(
                "Rejected because semantic similarity "
                "is below the required threshold."
            ),
        )

    return GuardDecision(
        accepted=True,
        explanation=(
            "Accepted because semantic similarity "
            "meets the required threshold."
        ),
    )


def evaluate_confidence(
    result: RankedImage,
) -> GuardDecision:
    confidence = result.image.confidence

    if confidence is None:
        return GuardDecision(
            accepted=False,
            explanation=(
                "Rejected because vision confidence "
                "is unavailable."
            ),
        )

    if confidence < CONFIDENCE_THRESHOLD:
        return GuardDecision(
            accepted=False,
            explanation=(
                "Rejected because vision confidence "
                "is below the required threshold."
            ),
        )

    return GuardDecision(
        accepted=True,
        explanation=(
            "Accepted because vision confidence "
            "meets the required threshold."
        ),
    )

def evaluate_match(
    result: RankedImage,
    required_tags: list[str],
) -> GuardDecision:
    similarity_decision = evaluate_similarity(result)

    if not similarity_decision.accepted:
        return similarity_decision

    confidence_decision = evaluate_confidence(result)

    if not confidence_decision.accepted:
        return confidence_decision

    tag_decision = evaluate_tags(
        result,
        required_tags=required_tags,
    )

    if not tag_decision.accepted:
        return tag_decision

    return GuardDecision(
        accepted=True,
        explanation=(
            "Accepted because semantic similarity, vision confidence, "
            "and required content tags all meet the matching criteria."
        ),
    )

def evaluate_tags(
    result: RankedImage,
    required_tags: list[str],
) -> GuardDecision:
    if not required_tags:
        return GuardDecision(
            accepted=False,
            explanation="Rejected because no required tags were provided.",
        )

    image_tags = result.image.tags

    if not image_tags:
        return GuardDecision(
            accepted=False,
            explanation="Rejected because image tags are unavailable.",
        )

    image_tag_set = {
        tag.strip().lower()
        for tag in image_tags.split(",")
        if tag.strip()
    }

    required_tag_set = {
        tag.strip().lower()
        for tag in required_tags
        if tag.strip()
    }

    matching_tags = image_tag_set.intersection(required_tag_set)

    if not matching_tags:
        return GuardDecision(
            accepted=False,
            explanation=(
                "Rejected because the image tags do not match "
                "the required content tags."
            ),
        )

    return GuardDecision(
        accepted=True,
        explanation=(
            "Accepted because the image contains "
            "at least one required content tag."
        ),
    )