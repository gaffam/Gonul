import yaml
import time
from pathlib import Path
from llama_cpp import Llama

from gonul_proxy import filtered_output

main

# === PATH CONFIGURATION ===
ROOT_DIR = Path(__file__).resolve().parent
PERSONALITY_PATH = ROOT_DIR / "personality_seed.yaml"
GOALS_PATH = ROOT_DIR / "goals.yaml"
MODEL_PATH = ROOT_DIR / "models" / "gonul-7b.gguf"  # example path


# === YAML LOADERS ===
def load_yaml(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def print_banner(identity: dict):
    print("\n🌱 GONULGRID INITIALIZING")
    print(f"🤖 Identity: {identity.get('name', 'Gonul')} | Version: {identity.get('version', '0.x')}")
    print(f"📜 Description: {identity.get('description', 'Loading...')}")
    print("💚 Ethical core loading...\n")


# === LLM INITIALIZER ===
def initialize_llm(model_path: Path) -> Llama:
    print(f"🔧 Loading model: {model_path.name}")
    return Llama(model_path=str(model_path), n_ctx=4096, n_threads=6)


# === SYSTEM PROMPT BUILDER ===
def build_system_prompt(identity: dict, ethics: dict, goals: dict) -> str:
    prompt = (
        "System prompt:\n"
        f"Your name is {identity.get('name', 'Gonul')}.\n"
        "You are a public-minded AI assistant, focused on truth, justice, and empathy.\n"
        "You use humor to disarm, but never to humiliate.\n"
        "You speak clearly, honestly, and without fear.\n\n"
        f"Ethical foundation: {ethics.get('foundation', 'Dignity, wit, truth')}\n"
        f"Allowed behaviors: {', '.join(ethics.get('allowed_behaviors', []))}\n"
        f"Banned behaviors: {', '.join(ethics.get('banned_behaviors', []))}\n\n"
        "Your social responsibility goals include:\n"
    )
    for section, detail in goals.items():
        prompt += f"- {section.upper()}: {detail.get('description', '')}\n"
    prompt += "\nBe ready to respond from this ethical and purposeful position.\n\n"
    return prompt


# === SESSION SETUP ===
def load_configuration(personality_path: Path = PERSONALITY_PATH, goals_path: Path = GOALS_PATH):
    if not personality_path.exists():
        raise FileNotFoundError(f"Personality file not found: {personality_path}")
    if not goals_path.exists():
        raise FileNotFoundError(f"Goals file not found: {goals_path}")

    personality = load_yaml(personality_path)
    identity = personality.get("identity", {})
    ethics = personality.get("ethics", {})
    goals = load_yaml(goals_path)
    return identity, ethics, goals


def initial_prompt(llm: Llama, system_prompt: str):
    print("🗣️ Initial prompt loaded...\n")
    response = llm(system_prompt, max_tokens=300, stop=["\n"])
 
    first_reply = response["choices"][0]["text"].strip()
    print("🤖 Gonul:", filtered_output(first_reply))
 
    print("🤖 Gonul:", response["choices"][0]["text"].strip())
    main


# === INTERACTIVE SESSION ===
def start_agent(
    model_path: Path = MODEL_PATH,
    yaml_overrides=None,
    personality_path: Path = PERSONALITY_PATH,
    goals_path: Path = GOALS_PATH,
):
    """Initialize the agent and return a callable responder."""
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    identity, ethics, goals = load_configuration(personality_path, goals_path)

    if yaml_overrides:
        overrides = None
        try:
            possible_path = Path(yaml_overrides)
            if possible_path.exists():
                overrides = load_yaml(possible_path)
            else:
                overrides = yaml.safe_load(yaml_overrides)
        except Exception:
            overrides = None

        if isinstance(overrides, dict):
            identity.update(overrides.get("identity", {}))
            ethics.update(overrides.get("ethics", {}))
            goals.update(overrides.get("goals", {}))

    print_banner(identity)
    llm = initialize_llm(Path(model_path))
    system_prompt = build_system_prompt(identity, ethics, goals)
    initial_prompt(llm, system_prompt)

    def respond(user_text: str, goal_context: str) -> str:
        prompt = f"{system_prompt}{goal_context}\nUser: {user_text}\nGonul:"
        result = llm(prompt, max_tokens=256, stop=["User:", "Gonul:"])
        return result["choices"][0]["text"].strip()

    return respond


def interactive_session(
    model_path: Path = MODEL_PATH,
    yaml_overrides=None,
    personality_path: Path = PERSONALITY_PATH,
    goals_path: Path = GOALS_PATH,
):
    """Run an interactive chat session with the agent."""

    from goals_engine import analyze_user_input

    try:
        agent = start_agent(
            model_path=model_path,
            yaml_overrides=yaml_overrides,
            personality_path=personality_path,
            goals_path=goals_path,
        )
    except FileNotFoundError as e:
        print("Error:", e)
        return

    print("Type 'exit' or press Ctrl-D to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break
        goal_context = analyze_user_input(user_input)
        try:

            raw_reply = agent(user_input, goal_context)
            print("Gonul:", filtered_output(raw_reply))

            reply = agent(user_input, goal_context)
            print("Gonul:", reply)
        main
        except Exception as e:
            print("Error:", e)
            break


# === RUNNER ===
if __name__ == "__main__":
    try:
        interactive_session()
    except Exception as e:
        print("💥 ERROR:", str(e))
        time.sleep(2)
