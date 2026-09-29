from pathlib import Path

from rocky.learning.learner import Learner
from rocky.memory.store import MemoryStore


def test_unknown_subject_is_detected(tmp_path: Path):
    learner = Learner(MemoryStore(tmp_path / "memory.json"))
    result = learner.learn_if_unknown("Python")
    assert result.status == "UNKNOWN"
    assert "don't know" in result.message


def test_learning_stores_supplied_source(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    learner = Learner(memory)
    result = learner.learn_if_unknown("Python", "Python is a programming language.")
    assert result.status == "LEARNED"
    assert memory.find_facts("python") == [{"subject": "Python", "text": "Python is a programming language."}]


def test_known_subject_is_not_relearned(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.remember_fact("Python", "Python is a programming language.")
    learner = Learner(memory)
    result = learner.learn_if_unknown("Python", "Different source.")
    assert result.status == "KNOWN"
