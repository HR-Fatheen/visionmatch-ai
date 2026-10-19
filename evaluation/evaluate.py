import json
from pathlib import Path
from types import SimpleNamespace

from app.services.match_result import RankedImage
from app.services.mismatch_guard import evaluate_match

DATA_DIR = Path(__file__).resolve().parent
DATASET_PATH = DATA_DIR / "dataset.json"
REPORT_PATH = DATA_DIR / "report.json"


def main():
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

    total = correct = false_accepts = false_rejects = 0
    true_positives = true_negatives = 0
    case_results = []

    print("VisionMatch AI - Evaluation Report")
    print("=" * 40)

    for case in dataset:
        print(f"\nCase: {case['case_id']}")
        print(f"Post: {case['post_text']}")
        candidate_results = []

        for candidate in case["candidate_images"]:
            image = SimpleNamespace(
                id=candidate["image_key"],
                confidence=candidate["confidence"],
                tags=",".join(candidate["tags"]),
            )
            ranked = RankedImage(
                image=image,
                similarity_score=candidate["similarity"],
            )

            decision = evaluate_match(ranked, case["required_tags"])
            expected = candidate["should_be_accepted"]
            actual = decision.accepted

            total += 1
            correct += int(actual == expected)
            false_accepts += int(actual and not expected)
            false_rejects += int(not actual and expected)
            true_positives += int(actual and expected)
            true_negatives += int(not actual and not expected)

            status = "PASS" if actual == expected else "FAIL"
            print(
                f"  [{status}] {candidate['image_key']}: "
                f"expected={expected}, actual={actual}"
            )

            candidate_results.append({
                "image_key": candidate["image_key"],
                "expected": expected,
                "actual": actual,
                "similarity": candidate["similarity"],
                "confidence": candidate["confidence"],
                "correct": actual == expected,
                "explanation": decision.explanation,
            })

        case_results.append({
            "case_id": case["case_id"],
            "candidates": candidate_results,
        })

    precision = (
        true_positives / (true_positives + false_accepts)
        if true_positives + false_accepts else 0.0
    )
    recall = (
        true_positives / (true_positives + false_rejects)
        if true_positives + false_rejects else 0.0
    )
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    report = {
        "candidates_evaluated": total,
        "correct_decisions": correct,
        "accuracy": correct / total if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "false_accepts": false_accepts,
        "false_rejects": false_rejects,
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "cases": case_results,
        "note": (
            "Metrics reflect the supplied dataset and its similarity scores; "
            "synthetic scores do not measure real model performance."
        ),
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\n" + "=" * 40)
    print(f"Candidates evaluated: {total}")
    print(f"Correct decisions: {correct}")
    print(f"Accuracy: {report['accuracy']:.1%}")
    print(f"Precision: {precision:.1%}")
    print(f"Recall: {recall:.1%}")
    print(f"F1 score: {f1:.1%}")
    print(f"False accepts: {false_accepts}")
    print(f"False rejects: {false_rejects}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
