"""Persistent JSON-backed memory for Rocky 0.2."""

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            data = {"facts": [], "experiences": []}
            self.save(data)
            return data

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("facts", [])
        data.setdefault("experiences", [])
        return data

    def save(self, data: dict[str, Any]) -> None:
        temp = self.path.with_suffix(".tmp")
        with temp.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
        temp.replace(self.path)

    def remember_fact(self, subject: str, text: str) -> dict[str, str]:
        subject = subject.strip()
        text = text.strip()
        if not subject or not text:
            raise ValueError("subject and text are required")

        data = self.load()
        fact = {"subject": subject, "text": text}
        data["facts"] = [
            existing for existing in data["facts"]
            if existing.get("subject", "").casefold() != subject.casefold()
        ]
        data["facts"].append(fact)
        self.save(data)
        return fact

    def find_facts(self, subject: str) -> list[dict[str, Any]]:
        subject = subject.strip().casefold()
        if not subject:
            return []

        data = self.load()
        return [
            fact for fact in data["facts"]
            if subject in fact.get("subject", "").casefold()
        ]
