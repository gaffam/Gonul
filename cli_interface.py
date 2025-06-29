"""Command-line interface for interacting with the GönülGrid agent."""

from pathlib import Path
import argparse
import agent_init


def main():
    parser = argparse.ArgumentParser(description="Run the GönülGrid CLI")
    parser.add_argument(
        "--model-path",
        "-m",
        type=Path,
        default=agent_init.MODEL_PATH,
        help="Path to the GGUF model file",
    )
    parser.add_argument(
        "--personality-path",
        type=Path,
        default=agent_init.PERSONALITY_PATH,
        help="Path to personality YAML file",
    )
    parser.add_argument(
        "--goals-path",
        type=Path,
        default=agent_init.GOALS_PATH,
        help="Path to goals YAML file",
    )
    parser.add_argument(
        "--yaml-overrides",
        "-y",
        help="YAML string or file path with configuration overrides",
    )
    args = parser.parse_args()

    agent_init.interactive_session(
        model_path=args.model_path,
        yaml_overrides=args.yaml_overrides,
        personality_path=args.personality_path,
        goals_path=args.goals_path,
    )


if __name__ == "__main__":
    main()

