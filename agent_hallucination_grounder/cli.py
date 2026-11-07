"""CLI for agent-hallucination-grounder."""
import sys
import argparse
from .grounder import AgentHallucinationGrounder


def main():
    parser = argparse.ArgumentParser(description="Agent Hallucination Grounder")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        grounder = AgentHallucinationGrounder(
            known_files={"src/main.py", "config.yaml"},
            known_symbols={"init_db", "run_server"}
        )
        text = "I modified 'src/main.py' and invoked `init_db()`. Then I edited 'fake/path.py' with `invented_func()`."
        res = grounder.verify_text(text)
        print(f"Grounding Report: {res.to_dict()}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
