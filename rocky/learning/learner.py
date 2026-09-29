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

        if self.memory.find_facts(subject):
            return LearningResult("KNOWN", subject, f"I already know something about {subject}.")

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
        if self.memory.find_facts(subject):
            return LearningResult("KNOWN", subject, f"I already know something about {subject}.")
        if not source_text:
            return LearningResult(
                "UNKNOWN",
                subject,
                f"I don't know {subject} yet, and no learning source was provided.",
            )
        return self.learn(subject, source_text, source)
