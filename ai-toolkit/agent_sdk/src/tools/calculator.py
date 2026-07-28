from agents import function_tool


@function_tool
def calculate(expression: str) -> str:
    """计算数学表达式，支持 + - * / ( ) 和数字。"""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "错误：仅支持数字和 + - * / ( ) 运算符。"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"结果：{result}"
    except Exception as e:
        return f"计算失败：{e}"
