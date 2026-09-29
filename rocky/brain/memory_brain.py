"""Basic memory-aware response layer for Rocky 0.2."""

from rocky.memory.store import MemoryStore


class MemoryBrain:
    """Turns explicit memory operations into deterministic responses."""

    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def remember(self, subject: str, text: str) -> str:
        self.memory.remember_fact(subject, text)
        return f"I learned: {text}"

    def recall(self, subject: str) -> str:
        facts = self.memory.find_facts(subject)
        if not facts:
            return f"I don't know anything about {subject.strip()} yet."
        return "\n".join(f"{fact['subject']}: {fact['text']}" for fact in facts)
