"""Persistent JSON-backed memory for Rocky 0.4."""

import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            data = {"facts": [], "experiences": [], "evidence": []}
            self.save(data)
            return data

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("facts", [])
        data.setdefault("experiences", [])
        data.setdefault("evidence", [])
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

    def remember_verified_fact(
        self, subject: str, text: str, evidence: list[dict[str, str]]
    ) -> dict[str, Any]:
        subject = subject.strip()
        text = text.strip()
        if not subject or not text:
            raise ValueError("subject and text are required")

        sources = []
        for item in evidence:
            source = item.get("source", "").strip()
            if source and source not in sources:
                sources.append(source)

        data = self.load()
        fact = {
            "subject": subject,
            "text": text,
            "verification": "VERIFIED",
            "sources": sources,
        }
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

    def add_evidence(self, subject: str, text: str, source: str) -> dict[str, str]:
        subject = subject.strip()
        text = text.strip()
        source = source.strip()
        if not subject or not text or not source:
            raise ValueError("subject, text, and source are required")

        data = self.load()
        evidence = {"subject": subject, "text": text, "source": source}
        duplicate = any(
            item.get("subject", "").casefold() == subject.casefold()
            and item.get("text", "") == text
            and item.get("source", "").casefold() == source.casefold()
            for item in data["evidence"]
        )
        if not duplicate:
            data["evidence"].append(evidence)
            self.save(data)
        return evidence

    def find_evidence(self, subject: str) -> list[dict[str, str]]:
        subject = subject.strip().casefold()
        if not subject:
            return []

        data = self.load()
        return [
            item for item in data["evidence"]
            if subject in item.get("subject", "").casefold()
        ]
