"""Command-line entry point for Project Rocky 0.2."""

from .brain.memory_brain import MemoryBrain
from .config import load_settings
from .logging_config import configure_logging
from .memory.store import MemoryStore


def main() -> None:
    settings = load_settings()
    logger = configure_logging(settings.log_file)
    memory = MemoryStore(settings.memory_file)
    memory.load()
    brain = MemoryBrain(memory)
    logger.info("Rocky started")

    print("Project Rocky 0.2 — Knowing")
    print("I can now remember and recall explicit facts.")
    print("Commands: remember <subject>: <fact> | recall <subject> | exit")

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
            logger.info("Fact remembered for subject=%s", subject.strip())
        elif lower.startswith("recall "):
            subject = user_input[len("recall "):].strip()
            print(f"Rocky: {brain.recall(subject)}")
            logger.info("Recall requested for subject=%s", subject)
        else:
            print("Rocky: Use 'remember' or 'recall' for memory operations.")


if __name__ == "__main__":
    main()
