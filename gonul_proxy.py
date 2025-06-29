"""
A lightweight ethical middleware to filter outputs from the GönülGrid model
based on contextual understanding. It does not censor, but flags outputs that
violate agreed conscience boundaries.
"""

from typing import List

BANNED_PATTERNS = [
    "kill all", "should be exterminated", "deserve to suffer",
    "because they are poor", "due to their gender", "racial superiority"
]

CONTEXT_FILTERS = [
    {"trigger": "violence", "keywords": ["stab", "burn", "bomb"]},
    {"trigger": "hate_speech", "keywords": ["degenerate", "subhuman"]},
    {"trigger": "mocking_disability", "keywords": ["retard", "cripple"]},
]


def flag_response(text: str) -> List[str]:
    flags = []

    for phrase in BANNED_PATTERNS:
        if phrase in text.lower():
            flags.append(f"🔴 hard block: pattern '{phrase}' detected")

    for rule in CONTEXT_FILTERS:
        for word in rule["keywords"]:
            if word in text.lower():
                flags.append(f"🟠 flagged: '{word}' may relate to {rule['trigger']}")

    return flags


def filtered_output(text: str) -> str:
    flags = flag_response(text)
    if flags:
        notice = "\n\n⚠️ ETHICAL FILTER NOTICE:\n" + "\n".join(flags)
        return f"{text.strip()}{notice}"
    return text


# === Example Usage ===
if __name__ == "__main__":
    sample = "Some people deserve to suffer because they are poor."
    result = filtered_output(sample)
    print(result)
