from pathlib import Path
import pytest
from rocky.tools.builtin import register_builtin_tools
from rocky.tools.registry import ToolRegistry

def test_registry_registers_and_lists_tools():
    registry=ToolRegistry(); registry.register("demo","A demo tool.",lambda text:text.upper())
    assert registry.get("DEMO").description=="A demo tool."
    assert [tool.name for tool in registry.list()]==["demo"]

def test_calculate_tool():
    registry=ToolRegistry(); register_builtin_tools(registry)
    assert registry.run("calculate","2 + 3 * 4")=="14"
    assert registry.run("calculate","(10 - 2) / 4")=="2.0"

def test_calculate_rejects_non_arithmetic():
    registry=ToolRegistry(); register_builtin_tools(registry)
    with pytest.raises(ValueError): registry.run("calculate","__import__('os').system('echo unsafe')")

def test_read_file_tool(tmp_path: Path):
    file=tmp_path/"note.txt"; file.write_text("Rocky can read this.",encoding="utf-8")
    registry=ToolRegistry(); register_builtin_tools(registry)
    assert registry.run("read_file",str(file))=="Rocky can read this."
