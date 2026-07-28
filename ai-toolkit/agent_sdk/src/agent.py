import json
from typing import Any
import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool

from src.config import AgentConfig


class LLMBackend:
    """多后端 LLM 封装"""

    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.client = AsyncOpenAI(
            api_key=self.config.api_key or "",
            base_url=self.config.base_url,
        )
        self.model = OpenAIChatCompletionsModel(
            model=self.config.agent_model,
            openai_client=self.client,
        )

    def create_agent(self, name: str, instructions: str, tools: list) -> Agent:
        return Agent(
            name=name,
            instructions=instructions,
            model=self.model,
            tools=tools,
        )


# 工具函数定义
@function_tool
def calculate(expression: str) -> str:
    """计算数学表达式。"""
    try:
        # 安全计算：仅允许基本数学运算符
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "错误：仅支持数字和 + - * / ( ) 运算符。"
        result = eval(expression, {"__builtins__": {}}, {})
        return f"结果：{result}"
    except Exception as e:
        return f"计算失败：{e}"


@function_tool
def search_knowledge_base(query: str) -> str:
    """搜索 RAG 知识库。"""
    # 这里调用 rag_kb 的 RAGService，避免硬依赖
    try:
        import sys
        from pathlib import Path
        rag_path = Path(__file__).resolve().parent.parent.parent.parent / "rag_kb"
        if str(rag_path) not in sys.path:
            sys.path.insert(0, str(rag_path))
        from src.config import RAGConfig
        from src.vector_store import VectorStore
        from src.rag_service import LLMClient, RAGService

        config = RAGConfig()
        store = VectorStore(config)
        llm = LLMClient(config)
        service = RAGService(config, store, llm)
        result = service.query(query)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"知识库搜索失败：{e}"


@function_tool
def get_weather(city: str) -> str:
    """获取指定城市的天气（示例，实际接入天气 API）。"""
    return f"{city} 当前天气：晴朗，25°C。注意：这是示例数据，未接入真实 API。"


class SmartAgent:
    """基于 OpenAI Agents SDK 的智能 Agent"""

    SYSTEM_PROMPT = """你是一个多能力助手，可以调用工具完成任务。

可用工具：
- calculate: 计算数学表达式
- search_knowledge_base: 搜索内部知识库
- get_weather: 获取天气（示例数据）

原则：
1. 先分析用户需求，选择合适工具。
2. 多步骤任务要拆解执行。
3. 如果工具返回错误，向用户解释原因，不要编造结果。
4. 回答简洁、专业，使用中文。
"""

    def __init__(self, config: AgentConfig = None, llm: LLMBackend = None):
        self.config = config or AgentConfig()
        self.llm = llm or LLMBackend(self.config)
        self.tools = [calculate, search_knowledge_base, get_weather]
        self.agent = self.llm.create_agent(
            name="智能助手",
            instructions=self.SYSTEM_PROMPT,
            tools=self.tools,
        )

    async def run(self, user_input: str, conversation_context: list = None) -> dict:
        result = await Runner.run(
            self.agent,
            input=user_input,
            context=conversation_context or [],
        )
        return {
            "answer": result.final_output,
            "tool_calls": getattr(result, "tool_calls", []),
        }
