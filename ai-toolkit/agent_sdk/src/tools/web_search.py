from agents import function_tool


@function_tool
def web_search(query: str) -> str:
    """联网搜索（示例工具，生产环境接入搜索引擎 API）。"""
    # 生产环境可接入：DuckDuckGo、Serper、Bing Search、Google Custom Search 等。
    return (
        f"搜索 '{query}' 的示例结果：\n"
        "1. 示例结果 A\n"
        "2. 示例结果 B\n"
        "注意：当前为占位实现，未调用真实搜索引擎。"
    )
