"""Command-line entry point for Project Rocky 0.7."""

from .brain.memory_brain import MemoryBrain
from .config import load_settings
from .learning.learner import Learner
from .logging_config import configure_logging
from .memory.store import MemoryStore
from .skills.builtin import register_builtin_skills
from .skills.registry import SkillRegistry
from .verification.verifier import Verifier


def parse_learn_command(command: str) -> tuple[str, str, str]:
    """Parse 'subject [source]: text', keeping a default source for simple use."""
    subject_and_source, source_text = command.split(":", 1)
    subject_and_source = subject_and_source.strip()
    source_text = source_text.strip()
    source = "user-supplied"
    if subject_and_source.endswith("]") and "[" in subject_and_source:
        subject, source_part = subject_and_source.rsplit("[", 1)
        subject = subject.strip()
        source = source_part[:-1].strip()
        if not subject or not source:
            raise ValueError("learn format must be: learn <subject> [source]: <source text>")
        return subject, source_text, source
    return subject_and_source, source_text, source


def print_memory(memory: MemoryStore) -> None:
    facts = memory.load()["facts"]
    experiences = memory.find_experiences()
    print(f"Rocky: Memory contains {len(facts)} fact(s) and {len(experiences)} experience(s).")
    for fact in facts:
        status = fact.get("verification", "LEGACY")
        print(f"  FACT [{status}] {fact['subject']}: {fact['text']}")
    for experience in experiences[-10:]:
        print(f"  EXPERIENCE [{experience.get('kind', 'unknown')}] {experience.get('timestamp', '')}: {experience.get('text', '')}")


def main() -> None:
    settings = load_settings()
    logger = configure_logging(settings.log_file)
    memory = MemoryStore(settings.memory_file)
    memory.load()
    brain = MemoryBrain(memory)
    learner = Learner(memory)
    verifier = Verifier(memory)
    skills = SkillRegistry()
    register_builtin_skills(skills)
    logger.info("Rocky started")

    print("Project Rocky 0.7 — Doing")
    print("I can learn, verify, remember, and perform reusable deterministic skills.")
    print("Commands: remember <subject>: <fact> | recall <subject> | learn <subject> [source]: <source text> | verify <subject> | ask <subject> | skills | do <skill>: <input> | experience <kind>: <text> | memories | forget <subject> | exit")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.casefold() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        lower = user_input.casefold()
        if lower.startswith("remember ") and ":" in user_input:
            command = user_input[len("remember "):]
            subject, fact = command.split(":", 1)
            try:
                response = brain.remember(subject, fact)
                memory.add_experience("memory", f"Explicitly remembered fact about {subject.strip()}.")
            except ValueError as exc:
                response = f"I could not remember that: {exc}"
            print(f"Rocky: {response}")
        elif lower.startswith("recall "):
            print(f"Rocky: {brain.recall(user_input[len('recall '):].strip())}")
        elif lower.startswith("learn ") and ":" in user_input:
            try:
                subject, source_text, source = parse_learn_command(user_input[len("learn "):])
                result = learner.learn(subject, source_text, source)
                print(f"Rocky: {result.message}")
            except ValueError as exc:
                print(f"Rocky: I could not learn that: {exc}")
        elif lower.startswith("verify "):
            subject = user_input[len("verify "):].strip()
            try:
                print(f"Rocky: {verifier.verify(subject).message}")
            except ValueError as exc:
                print(f"Rocky: I could not verify that: {exc}")
        elif lower.startswith("ask "):
            subject = user_input[len("ask "):].strip()
            result = learner.learn_if_unknown(subject)
            if result.status == "UNKNOWN":
                print(f"Rocky: {result.message}")
                print("Rocky: Provide a source with: learn <subject> [source]: <source text>")
            else:
                print(f"Rocky: {brain.recall(subject)}")
        elif lower == "skills":
            print("Rocky: Available skills:")
            for skill in skills.list():
                print(f"  {skill.name}: {skill.description}")
        elif lower.startswith("do ") and ":" in user_input:
            name, argument = user_input[len("do "):].split(":", 1)
            try:
                result = skills.run(name, argument)
                memory.add_experience("skill", f"Executed skill {name.strip()}: {argument.strip()}")
                print(f"Rocky: {result}")
            except (KeyError, ValueError) as exc:
                print(f"Rocky: I could not perform that skill: {exc}")
        elif lower.startswith("experience ") and ":" in user_input:
            kind, text = user_input[len("experience "):].split(":", 1)
            try:
                experience = memory.add_experience(kind, text)
                print(f"Rocky: I remembered that experience at {experience['timestamp']}.")
            except ValueError as exc:
                print(f"Rocky: I could not remember that experience: {exc}")
        elif lower == "memories":
            print_memory(memory)
        elif lower.startswith("forget "):
            subject = user_input[len("forget "):].strip()
            try:
                if memory.forget_fact(subject):
                    memory.add_experience("memory", f"Forgot facts and learning evidence about {subject}.")
                    print(f"Rocky: I forgot facts and learning evidence about {subject}.")
                else:
                    print(f"Rocky: I had no facts or learning evidence to forget about {subject}.")
            except ValueError as exc:
                print(f"Rocky: I could not forget that: {exc}")
        else:
            print("Rocky: Use 'remember', 'recall', 'learn', 'verify', 'ask', 'skills', 'do', 'experience', 'memories', or 'forget'.")


if __name__ == "__main__":
    main()
