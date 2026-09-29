"""Small JSON-backed memory store used as Rocky's first persistence layer."""

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"facts": [], "experiences": []}
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict[str, Any]) -> None:
        temp = self.path.with_suffix(".tmp")
        with temp.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
        temp.replace(self.path)
