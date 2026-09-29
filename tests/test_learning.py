from pathlib import Path

from rocky.learning.learner import Learner
from rocky.memory.store import MemoryStore


def test_unknown_subject_is_detected(tmp_path: Path):
    learner = Learner(MemoryStore(tmp_path / "memory.json"))
    result = learner.learn_if_unknown("Python")
    assert result.status == "UNKNOWN"
    assert "don't know" in result.message


def test_learning_stores_evidence_but_not_fact(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    learner = Learner(memory)
    result = learner.learn_if_unknown("Python", "Python is a programming language.", "source-1")
    assert result.status == "UNVERIFIED"
    assert memory.find_facts("python") == []
    assert memory.find_evidence("python") == [
        {"subject": "Python", "text": "Python is a programming language.", "source": "source-1"}
    ]
    assert memory.find_experiences("learning")


def test_known_subject_is_not_relearned(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.remember_verified_fact("Python", "Python is a programming language.", [])
    learner = Learner(memory)
    result = learner.learn_if_unknown("Python", "Different source.", "source-2")
    assert result.status == "KNOWN"


def test_legacy_fact_can_receive_verification_evidence(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.remember_fact("Python", "Python is a programming language.")
    learner = Learner(memory)

    result = learner.learn_if_unknown("Python", "Python is a programming language.", "source-1")

    assert result.status == "UNVERIFIED"
    assert len(memory.find_evidence("Python")) == 1
