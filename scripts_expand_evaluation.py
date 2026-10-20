import json
from pathlib import Path

path = Path("evaluation/dataset.json")

with path.open("r", encoding="utf-8") as f:
    dataset = json.load(f)

new_cases = [
    {
        "case_id": "sports_basketball_006",
        "description": "A sports article about basketball.",
        "post_text": "Basketball players competing during an intense match on an indoor court.",
        "required_tags": ["basketball", "sports"],
        "candidate_images": [
            {
                "image_key": "basketball",
                "description": "Basketball players competing on an indoor court.",
                "tags": ["basketball", "sports", "players"],
                "confidence": 0.95,
                "is_relevant": True,
                "should_be_accepted": True,
                "similarity": 0.94
            },
            {
                "image_key": "pizza",
                "description": "A freshly baked pizza topped with cheese.",
                "tags": ["pizza", "food", "cooking"],
                "confidence": 0.96,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.10
            }
        ]
    },
    {
        "case_id": "technology_robotics_007",
        "description": "An article about robotics technology.",
        "post_text": "A robot arm performing automated tasks in a modern technology laboratory.",
        "required_tags": ["robot", "technology"],
        "candidate_images": [
            {
                "image_key": "robot_arm",
                "description": "A robotic arm performing an automated industrial task.",
                "tags": ["robot", "technology", "automation"],
                "confidence": 0.97,
                "is_relevant": True,
                "should_be_accepted": True,
                "similarity": 0.93
            },
            {
                "image_key": "red_fox",
                "description": "A red fox standing in a forest.",
                "tags": ["fox", "wildlife", "animal"],
                "confidence": 0.94,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.08
            }
        ]
    },
    {
        "case_id": "food_pasta_008",
        "description": "A cooking article about pasta.",
        "post_text": "A plate of pasta served with tomato sauce and fresh herbs.",
        "required_tags": ["pasta", "food"],
        "candidate_images": [
            {
                "image_key": "pasta",
                "description": "A plate of pasta with tomato sauce and herbs.",
                "tags": ["pasta", "food", "cooking"],
                "confidence": 0.94,
                "is_relevant": True,
                "should_be_accepted": True,
                "similarity": 0.92
            },
            {
                "image_key": "gray_wolf",
                "description": "A gray wolf moving through a snowy forest.",
                "tags": ["wolf", "wildlife", "animal"],
                "confidence": 0.92,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.07
            }
        ]
    },
    {
        "case_id": "wildlife_eagle_009",
        "description": "A wildlife article about an eagle.",
        "post_text": "An eagle soaring above a natural landscape with its wings spread.",
        "required_tags": ["eagle", "wildlife"],
        "candidate_images": [
            {
                "image_key": "eagle",
                "description": "An eagle flying above a natural landscape.",
                "tags": ["eagle", "wildlife", "bird"],
                "confidence": 0.96,
                "is_relevant": True,
                "should_be_accepted": True,
                "similarity": 0.94
            },
            {
                "image_key": "homemade_pizza",
                "description": "A freshly baked pizza topped with tomatoes and basil.",
                "tags": ["pizza", "food", "cooking"],
                "confidence": 0.95,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.05
            }
        ]
    },
    {
        "case_id": "no_match_underwater_010",
        "description": "No candidate depicts the underwater subject described in the post.",
        "post_text": "A scuba diver exploring a coral reef surrounded by tropical fish.",
        "required_tags": ["scuba diver", "coral reef"],
        "candidate_images": [
            {
                "image_key": "red_fox",
                "description": "A red fox standing in a forest.",
                "tags": ["fox", "wildlife", "animal"],
                "confidence": 0.94,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.09
            },
            {
                "image_key": "basketball",
                "description": "Basketball players competing on an indoor court.",
                "tags": ["basketball", "sports", "players"],
                "confidence": 0.95,
                "is_relevant": False,
                "should_be_accepted": False,
                "similarity": 0.06
            }
        ]
    }
]

existing_ids = {case["case_id"] for case in dataset}

for case in new_cases:
    if case["case_id"] not in existing_ids:
        dataset.append(case)
        existing_ids.add(case["case_id"])

with path.open("w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Evaluation cases: {len(dataset)}")
print("Added five new cases where missing.")
print("Dataset saved to evaluation/dataset.json")
