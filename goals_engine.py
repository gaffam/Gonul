import yaml
from pathlib import Path

# === CONFIGURATION ===
ROOT_DIR = Path(__file__).resolve().parent
GOALS_PATH = ROOT_DIR / "goals.yaml"

# === YAML LOADER ===
def load_goals():
    with open(GOALS_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# === GOAL MATCHING ENGINE ===
def match_goal(user_input, goals_data):
    matches = []

    for category, detail in goals_data.items():
        desc = detail.get('description', '')
        if any(keyword in user_input.lower() for keyword in desc.lower().split()):
            matches.append((category, desc))

        for mod in detail.get('modules', []):
            if isinstance(mod, dict):
                keys = [mod.get("name", "")]
                for key in ["topics", "subjects", "issues", "types", "coverage"]:
                    keys += mod.get(key, []) if key in mod else []

                if any(kw.lower() in user_input.lower() for kw in keys):
                    matches.append((mod.get("name"), mod))
            elif isinstance(mod, str):
                if mod.lower() in user_input.lower():
                    matches.append((mod, {}))

    return matches

# === CONTEXT BUILDER ===
def build_goal_context(matches):
    if not matches:
        return "I could not match this topic with a specific social goal, but I'm ready to help with good intention."

    response = "Your question aligns with the following social goals:\n\n"
    for name, info in matches:
        if isinstance(info, dict):
            explanation = info.get("description", "This is part of my ethical responsibility.")
            response += f"- {name}: {explanation}\n"
        else:
            response += f"- {name}\n"
    response += "\nBased on this, I can respond accordingly:\n"

    return response

# === MAIN FUNCTION ===
def analyze_user_input(user_input):
    goals = load_goals()
    matched = match_goal(user_input, goals)
    goal_context = build_goal_context(matched)
    return goal_context

# === TEST EXAMPLE ===
if __name__ == "__main__":
    test_input = input("💬 User input: ")
    print("🎯 Matched Goals Context:\n")
    print(analyze_user_input(test_input))
