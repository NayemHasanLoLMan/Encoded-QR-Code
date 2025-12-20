import re
from collections import defaultdict
from skill_ontology import CANONICAL_SKILLS


def normalize_text(text: str) -> str:
    return re.sub(r'[^a-z0-9\s]', ' ', text.lower()).strip()


def normalize_skills(raw_skills):


    grouped = defaultdict(dict)

    for group in raw_skills:
        for item in group["items"]:
            text = normalize_text(item)

            for key, (canonical, category) in CANONICAL_SKILLS.items():
                if key in text:
                    entry = grouped[category].get(canonical, {
                        "confidence": 0.0,
                        "mentions": 0
                    })

                    entry["mentions"] += 1
                    entry["confidence"] = min(1.0, entry["mentions"] * 0.35)
                    grouped[category][canonical] = entry

    # Format output
    normalized = []
    for category, skills in grouped.items():
        normalized.append({
            "category": category,
            "items": [
                {"name": k, "confidence": round(v["confidence"], 2)}
                for k, v in skills.items()
            ]
        })

    return normalized
