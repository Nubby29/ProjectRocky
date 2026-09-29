"""Deterministic self-evaluation of Rocky's stored knowledge."""

from dataclasses import dataclass
from rocky.memory.store import MemoryStore


@dataclass(frozen=True)
class EvaluationResult:
    subject: str
    status: str
    confidence: float
    reason: str


class SelfEvaluator:
    """Estimates knowledge confidence from Rocky's explicit memory state.

    This is a memory-status signal, not a claim about real-world truth.
    """

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def evaluate(self, subject: str) -> EvaluationResult:
        subject = subject.strip()
        if not subject:
            raise ValueError("subject is required")

        facts = self.memory.find_facts(subject)
        evidence = self.memory.find_evidence(subject)
        sources = {item.get("source", "").casefold() for item in evidence if item.get("source")}

        if any(fact.get("verification") == "VERIFIED" for fact in facts):
            return EvaluationResult(subject, "VERIFIED", 1.0, "Rocky has explicitly verified knowledge stored for this subject.")

        if len(sources) >= 2:
            texts = {" ".join(item.get("text", "").casefold().split()) for item in evidence}
            if len(texts) > 1:
                return EvaluationResult(subject, "CONFLICT", 0.0, "Stored sources disagree, so Rocky should not treat the subject as verified.")

        if evidence:
            return EvaluationResult(subject, "UNVERIFIED", 0.5, f"Rocky has {len(sources)} distinct source(s), but the knowledge is not verified.")

        if facts:
            return EvaluationResult(subject, "LEGACY", 0.25, "Rocky has older knowledge without explicit verification metadata.")

        return EvaluationResult(subject, "UNKNOWN", 0.0, "Rocky has no stored knowledge or evidence for this subject.")
