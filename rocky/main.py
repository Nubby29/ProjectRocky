"""Command-line entry point for Project Rocky 0.4."""

from .brain.memory_brain import MemoryBrain
from .config import load_settings
from .learning.learner import Learner
from .logging_config import configure_logging
from .memory.store import MemoryStore
from .verification.verifier import Verifier


def main() -> None:
    settings = load_settings()
    logger = configure_logging(settings.log_file)
    memory = MemoryStore(settings.memory_file)
    memory.load()
    brain = MemoryBrain(memory)
    learner = Learner(memory)
    verifier = Verifier(memory)
    logger.info("Rocky started")

    print("Project Rocky 0.4 — Verification")
    print("I can learn candidate information, compare supplied sources, and store only verified knowledge as facts.")
    print("Commands: remember <subject>: <fact> | recall <subject> | learn <subject>: <source text> | verify <subject> | ask <subject> | exit")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        lower = user_input.casefold()
        if lower.startswith("remember ") and ":" in user_input:
            command = user_input[len("remember "):]
            subject, fact = command.split(":", 1)
            try:
                response = brain.remember(subject, fact)
            except ValueError as exc:
                response = f"I could not remember that: {exc}"
            print(f"Rocky: {response}")
        elif lower.startswith("recall "):
            subject = user_input[len("recall "):].strip()
            print(f"Rocky: {brain.recall(subject)}")
        elif lower.startswith("learn ") and ":" in user_input:
            command = user_input[len("learn "):]
            subject, source_text = command.split(":", 1)
            try:
                result = learner.learn(subject, source_text)
                print(f"Rocky: {result.message}")
                logger.info("Learning result=%s subject=%s", result.status, subject.strip())
            except ValueError as exc:
                print(f"Rocky: I could not learn that: {exc}")
        elif lower.startswith("verify "):
            subject = user_input[len("verify "):].strip()
            try:
                result = verifier.verify(subject)
                print(f"Rocky: {result.message}")
                logger.info("Verification result=%s subject=%s", result.status, subject)
            except ValueError as exc:
                print(f"Rocky: I could not verify that: {exc}")
        elif lower.startswith("ask "):
            subject = user_input[len("ask "):].strip()
            result = learner.learn_if_unknown(subject)
            if result.status == "UNKNOWN":
                print(f"Rocky: {result.message}")
                print("Rocky: Provide a source with: learn <subject>: <source text>")
            else:
                print(f"Rocky: {brain.recall(subject)}")
        else:
            print("Rocky: Use 'remember', 'recall', 'learn', 'verify', or 'ask'.")


if __name__ == "__main__":
    main()
