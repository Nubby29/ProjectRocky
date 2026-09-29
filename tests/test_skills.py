from rocky.skills.registry import SkillRegistry
from rocky.skills.builtin import register_builtin_skills


def test_registry_registers_and_lists_skills():
    registry = SkillRegistry()
    registry.register("demo", "A demo skill.", lambda text: text.upper())

    assert registry.get("DEMO").description == "A demo skill."
    assert [skill.name for skill in registry.list()] == ["demo"]


def test_builtin_skills_execute():
    registry = SkillRegistry()
    register_builtin_skills(registry)

    assert registry.run("echo", " hello ") == "hello"
    assert registry.run("uppercase", "hello") == "HELLO"
    assert registry.run("lowercase", "HELLO") == "hello"
    assert registry.run("length", "hello") == "5"
