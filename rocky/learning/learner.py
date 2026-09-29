"""First learning loop for Rocky 0.3."""

from dataclasses import dataclass
from rocky.memory.store import MemoryStore


@dataclass(frozen=True)
class LearningResult:
    status: str
    subject: str
    message: str


class Learner:
    """Learns from an explicitly supplied source and stores the result."""

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def learn(self, subject: str, source_text: str) -> LearningResult:
        subject = subject.strip()
        source_text = source_text.strip()
        if not subject or not source_text:
            raise ValueError("subject and source text are required")
        self.memory.remember_fact(subject, source_text)
        return LearningResult("LEARNED", subject, f"I learned about {subject}: {source_text}")

    def learn_if_unknown(self, subject: str, source_text: str | None = None) -> LearningResult:
        if self.memory.find_facts(subject):
            return LearningResult("KNOWN", subject, f"I already know something about {subject}.")
        if not source_text:
            return LearningResult("UNKNOWN", subject.strip(), f"I don't know {subject.strip()} yet, and no learning source was provided.")
        return self.learn(subject, source_text)
