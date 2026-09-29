from rocky.memory.store import MemoryStore
from rocky.reasoning.self_evaluator import SelfEvaluator


def test_unknown_has_zero_confidence(tmp_path):
    evaluator = SelfEvaluator(MemoryStore(tmp_path / "memory.json"))
    result = evaluator.evaluate("Python")
    assert result.status == "UNKNOWN"
    assert result.confidence == 0.0


def test_legacy_fact_has_low_confidence(tmp_path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.remember_fact("Python", "Python is a programming language.")
    result = SelfEvaluator(memory).evaluate("Python")
    assert result.status == "LEGACY"
    assert result.confidence == 0.25


def test_unverified_evidence_has_medium_confidence(tmp_path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Python", "Python is a programming language.", "source-1")
    result = SelfEvaluator(memory).evaluate("Python")
    assert result.status == "UNVERIFIED"
    assert result.confidence == 0.5


def test_verified_fact_has_high_confidence(tmp_path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Python", "Python is a programming language.", "source-1")
    memory.add_evidence("Python", "Python is a programming language.", "source-2")
    from rocky.verification.verifier import Verifier
    Verifier(memory).verify("Python")
    result = SelfEvaluator(memory).evaluate("Python")
    assert result.status == "VERIFIED"
    assert result.confidence == 1.0


def test_conflict_has_zero_confidence(tmp_path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.add_evidence("Rocky", "Claim A", "source-1")
    memory.add_evidence("Rocky", "Claim B", "source-2")
    result = SelfEvaluator(memory).evaluate("Rocky")
    assert result.status == "CONFLICT"
    assert result.confidence == 0.0
