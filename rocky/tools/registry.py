"""Registry for controlled, reusable Rocky tools."""

from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[[str], str]

class ToolRegistry:
    def __init__(self): self._tools: dict[str, Tool] = {}
    def register(self, name: str, description: str, handler: Callable[[str], str]) -> Tool:
        name, description = name.strip().casefold(), description.strip()
        if not name or not description: raise ValueError("tool name and description are required")
        tool = Tool(name, description, handler); self._tools[name] = tool; return tool
    def get(self, name: str) -> Tool | None: return self._tools.get(name.strip().casefold())
    def list(self) -> list[Tool]: return sorted(self._tools.values(), key=lambda tool: tool.name)
    def run(self, name: str, argument: str = "") -> str:
        tool = self.get(name)
        if tool is None: raise KeyError(f"unknown tool: {name.strip()}")
        return tool.handler(argument)
