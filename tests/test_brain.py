from pathlib import Path

from rocky.brain.memory_brain import MemoryBrain
from rocky.memory.store import MemoryStore


def test_brain_can_remember_and_recall(tmp_path: Path):
    brain = MemoryBrain(MemoryStore(tmp_path / "memory.json"))

    assert brain.remember("Jhave", "Jhave is building Rocky.") == "I learned: Jhave is building Rocky."
    assert brain.recall("jhave") == "Jhave: Jhave is building Rocky."


def test_brain_reports_unknown_subject(tmp_path: Path):
    brain = MemoryBrain(MemoryStore(tmp_path / "memory.json"))

    assert brain.recall("Python") == "I don't know anything about Python yet."
