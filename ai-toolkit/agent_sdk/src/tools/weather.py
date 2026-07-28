from agents import function_tool


@function_tool
def get_weather(city: str) -> str:
    """获取指定城市的天气（示例工具，未接入真实 API）。"""
    # 生产环境应接入天气 API，例如 OpenWeatherMap、和风天气等。
    return f"{city} 当前天气：晴朗，25°C。注意：这是示例数据。"
