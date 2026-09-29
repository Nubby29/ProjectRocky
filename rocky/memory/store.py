"""Persistent JSON-backed memory for Rocky 0.6."""

import json
from datetime import datetime, timezone
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

    def add_experience(self, kind: str, text: str) -> dict[str, str]:
        """Store a timestamped event in Rocky's episodic memory."""
        kind = kind.strip().casefold()
        text = text.strip()
        if not kind or not text:
            raise ValueError("experience kind and text are required")

        data = self.load()
        experience = {
            "kind": kind,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        data["experiences"].append(experience)
        self.save(data)
        return experience

    def find_experiences(self, kind: str | None = None) -> list[dict[str, str]]:
        """Return experiences, optionally filtered by kind."""
        data = self.load()
        if kind is None or not kind.strip():
            return list(data["experiences"])

        wanted = kind.strip().casefold()
        return [
            item for item in data["experiences"]
            if item.get("kind", "").casefold() == wanted
        ]

    def forget_fact(self, subject: str) -> bool:
        """Remove stored facts and evidence for a subject."""
        subject = subject.strip()
        if not subject:
            raise ValueError("subject is required")

        data = self.load()
        before = len(data["facts"]) + len(data["evidence"])
        data["facts"] = [
            item for item in data["facts"]
            if item.get("subject", "").casefold() != subject.casefold()
        ]
        data["evidence"] = [
            item for item in data["evidence"]
            if item.get("subject", "").casefold() != subject.casefold()
        ]
        changed = len(data["facts"]) + len(data["evidence"]) != before
        if changed:
            self.save(data)
        return changed
