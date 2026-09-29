from pathlib import Path

from rocky.memory.store import MemoryStore
from rocky.verification.verifier import Verifier


def test_single_source_is_unverified(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Python", "Python is a programming language.", "source-1")

    result = Verifier(memory).verify("Python")

    assert result.status == "UNVERIFIED"
    assert memory.find_facts("Python") == []


def test_agreeing_sources_become_verified(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Python", "Python is a programming language.", "source-1")
    memory.add_evidence("Python", "  Python is a programming language. ", "source-2")

    result = Verifier(memory).verify("Python")

    assert result.status == "VERIFIED"
    assert memory.find_facts("Python") == [
        {
            "subject": "Python",
            "text": "Python is a programming language.",
            "verification": "VERIFIED",
            "sources": ["source-1", "source-2"],
        }
    ]


def test_conflicting_sources_are_not_verified(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Rocky", "Rocky is version 0.4.", "source-1")
    memory.add_evidence("Rocky", "Rocky is version 0.5.", "source-2")

    result = Verifier(memory).verify("Rocky")

    assert result.status == "CONFLICT"
    assert memory.find_facts("Rocky") == []


def test_verified_fact_persists(tmp_path: Path):
    path = tmp_path / "memory.json"
    memory = MemoryStore(path)
    memory.add_evidence("Earth", "Earth is a planet.", "source-1")
    memory.add_evidence("Earth", "Earth is a planet.", "source-2")

    Verifier(memory).verify("Earth")

    reloaded = MemoryStore(path)
    assert reloaded.find_facts("earth")[0]["verification"] == "VERIFIED"
