"""Deterministic source verification for Rocky 0.4."""

from dataclasses import dataclass
from rocky.memory.store import MemoryStore


@dataclass(frozen=True)
class VerificationResult:
    status: str
    subject: str
    message: str
    evidence_count: int


class Verifier:
    """Verifies a candidate when independent supplied sources agree exactly."""

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.casefold().split())

    def verify(self, subject: str) -> VerificationResult:
        subject = subject.strip()
        if not subject:
            raise ValueError("subject is required")

        evidence = self.memory.find_evidence(subject)
        if not evidence:
            return VerificationResult(
                "UNKNOWN", subject, f"I have no learning evidence for {subject}.", 0
            )

        groups: dict[str, list[dict[str, str]]] = {}
        for item in evidence:
            key = self._normalize(item["text"])
            groups.setdefault(key, []).append(item)

        if len(groups) > 1:
            return VerificationResult(
                "CONFLICT",
                subject,
                f"Sources disagree about {subject}; I will not store it as verified knowledge.",
                len(evidence),
            )

        if len(evidence) < 2:
            return VerificationResult(
                "UNVERIFIED",
                subject,
                f"I need another agreeing source before I can verify {subject}.",
                len(evidence),
            )

        verified_text = evidence[0]["text"]
        self.memory.remember_verified_fact(subject, verified_text, evidence)
        return VerificationResult(
            "VERIFIED",
            subject,
            f"I verified {subject} using {len(evidence)} agreeing sources.",
            len(evidence),
        )
