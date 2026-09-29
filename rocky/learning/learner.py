"""Learning pipeline for Rocky 0.4."""

from dataclasses import dataclass
from rocky.memory.store import MemoryStore


@dataclass(frozen=True)
class LearningResult:
    status: str
    subject: str
    message: str


class Learner:
    """Collects supplied evidence without treating it as verified fact."""

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def learn(self, subject: str, source_text: str, source: str = "user-supplied") -> LearningResult:
        subject = subject.strip()
        source_text = source_text.strip()
        source = source.strip()
        if not subject or not source_text or not source:
            raise ValueError("subject, source text, and source are required")

        facts = self.memory.find_facts(subject)
        if any(fact.get("verification") == "VERIFIED" for fact in facts):
            return LearningResult("KNOWN", subject, f"I already know verified information about {subject}.")

        # Legacy Rocky 0.3 facts remain readable but can receive Phase 4 evidence.
        self.memory.add_evidence(subject, source_text, source)
        count = len(self.memory.find_evidence(subject))
        return LearningResult(
            "UNVERIFIED",
            subject,
            f"I learned a candidate fact about {subject}, but it is not verified yet ({count} source{'s' if count != 1 else ''}).",
        )

    def learn_if_unknown(
        self, subject: str, source_text: str | None = None, source: str = "user-supplied"
    ) -> LearningResult:
        subject = subject.strip()
        facts = self.memory.find_facts(subject)
        if any(fact.get("verification") == "VERIFIED" for fact in facts):
            return LearningResult("KNOWN", subject, f"I already know verified information about {subject}.")
        if facts and not source_text:
            return LearningResult("UNVERIFIED", subject, f"I have older knowledge about {subject}, but it has not been verified yet.")
        if not source_text:
            return LearningResult(
                "UNKNOWN",
                subject,
                f"I don't know {subject} yet, and no learning source was provided.",
            )
        return self.learn(subject, source_text, source)
