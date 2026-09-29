"""Built-in safe tools for Rocky 0.8."""
import ast, operator
from pathlib import Path
from .registry import ToolRegistry
_ALLOWED_OPERATORS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow,ast.USub:operator.neg,ast.UAdd:operator.pos}
def _calculate(expression: str)->str:
    expression=expression.strip()
    if not expression: raise ValueError("an arithmetic expression is required")
    def evaluate(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)) and not isinstance(node.value,bool): return node.value
        if isinstance(node,ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS: return _ALLOWED_OPERATORS[type(node.op)](evaluate(node.operand))
        if isinstance(node,ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS: return _ALLOWED_OPERATORS[type(node.op)](evaluate(node.left),evaluate(node.right))
        raise ValueError("only numeric arithmetic is allowed")
    try: result=evaluate(ast.parse(expression,mode="eval").body)
    except (SyntaxError,ZeroDivisionError,OverflowError) as exc: raise ValueError("invalid arithmetic expression") from exc
    return str(result)
def _read_text_file(argument: str)->str:
    raw_path=argument.strip()
    if not raw_path: raise ValueError("a file path is required")
    path=Path(raw_path)
    if not path.is_file(): raise ValueError(f"file does not exist: {path}")
    return path.read_text(encoding="utf-8")
def register_builtin_tools(registry: ToolRegistry)->None:
    registry.register("calculate","Safely evaluate a numeric arithmetic expression.",_calculate)
    registry.register("read_file","Read a UTF-8 text file from a supplied path.",_read_text_file)
