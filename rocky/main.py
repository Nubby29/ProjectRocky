"""Command-line entry point for Project Rocky 0.1."""

from .config import load_settings
from .logging_config import configure_logging
from .memory.store import MemoryStore


def main() -> None:
    settings = load_settings()
    logger = configure_logging(settings.log_file)
    memory = MemoryStore(settings.memory_file)
    data = memory.load()
    logger.info("Rocky started; facts=%d experiences=%d", len(data["facts"]), len(data["experiences"]))

    print("Project Rocky 0.1 — The Seed")
    print("Foundation initialized. Learning capabilities arrive in later milestones.")
    print("Type 'exit' to quit.")

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
        print("Rocky: I received your message. My learning engine is not enabled yet.")
        logger.info("Conversation input received: %s", user_input)


if __name__ == "__main__":
    main()
