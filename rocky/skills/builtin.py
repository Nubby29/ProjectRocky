"""Built-in deterministic skills for Rocky 0.7."""

from .registry import SkillRegistry


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register("echo", "Return the supplied text unchanged.", lambda text: text.strip())
    registry.register("uppercase", "Convert supplied text to uppercase.", lambda text: text.strip().upper())
    registry.register("lowercase", "Convert supplied text to lowercase.", lambda text: text.strip().lower())
    registry.register("length", "Count the characters in supplied text.", lambda text: str(len(text.strip())))
