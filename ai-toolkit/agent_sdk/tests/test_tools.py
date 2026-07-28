"""
基础工具单元测试。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tools import calculate, get_weather, web_search


def test_calculate():
    result = calculate("2 + 3 * 4")
    assert "14" in result, result


def test_calculate_invalid_chars():
    result = calculate("__import__('os').system('ls')")
    assert "错误" in result, result


def test_weather():
    result = get_weather("上海")
    assert "上海" in result, result


def test_web_search():
    result = web_search("OpenAI")
    assert "示例结果" in result, result


if __name__ == "__main__":
    test_calculate()
    test_calculate_invalid_chars()
    test_weather()
    test_web_search()
    print("All tests passed.")
