import json
from pathlib import Path
from types import SimpleNamespace

from app.services.match_result import RankedImage
from app.services.mismatch_guard import evaluate_match

DATASET_PATH = Path(__file__).resolve().parent / "dataset.json"


def main():
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    total = correct = false_accepts = false_rejects = 0

    print("VisionMatch AI - Evaluation Report")
    print("=" * 40)

    for case in dataset:
        print(f"\nCase: {case['case_id']}")
        print(f"Post: {case['post_text']}")

        for candidate in case["candidate_images"]:
            image = SimpleNamespace(
                id=candidate["image_key"],
                confidence=candidate["confidence"],
                tags=",".join(candidate["tags"]),
            )
            ranked = RankedImage(
                image=image,
                similarity_score=candidate.get("similarity", 1.0),
            )

            decision = evaluate_match(ranked, case["required_tags"])
            expected = candidate["should_be_accepted"]
            actual = decision.accepted

            total += 1
            correct += int(actual == expected)
            false_accepts += int(actual and not expected)
            false_rejects += int(not actual and expected)

            status = "PASS" if actual == expected else "FAIL"
            print(
                f"  [{status}] {candidate['image_key']}: "
                f"expected={expected}, actual={actual}"
            )
            if actual != expected:
                print(f"    Reason: {decision.explanation}")

    print("\n" + "=" * 40)
    print(f"Candidates evaluated: {total}")
    print(f"Correct decisions: {correct}")
    print(f"Accuracy: {correct / total:.1%}" if total else "Accuracy: N/A")
    print(f"False accepts: {false_accepts}")
    print(f"False rejects: {false_rejects}")


if __name__ == "__main__":
    main()
