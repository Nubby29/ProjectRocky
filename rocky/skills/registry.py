"""Registry for deterministic reusable Rocky skills."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    handler: Callable[[str], str]


class SkillRegistry:
    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, name: str, description: str, handler: Callable[[str], str]) -> Skill:
        name = name.strip().casefold()
        description = description.strip()
        if not name or not description:
            raise ValueError("skill name and description are required")
        skill = Skill(name, description, handler)
        self._skills[name] = skill
        return skill

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name.strip().casefold())

    def list(self) -> list[Skill]:
        return sorted(self._skills.values(), key=lambda skill: skill.name)

    def run(self, name: str, argument: str = "") -> str:
        skill = self.get(name)
        if skill is None:
            raise KeyError(f"unknown skill: {name.strip()}")
        return skill.handler(argument)
