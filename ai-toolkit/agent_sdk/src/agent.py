"""
基于 OpenAI Agents SDK 的智能 Agent。
支持多后端 LLM、工具调用、会话记忆、RAG 集成。
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from agents import Agent, Runner

from src.llm_backend import LLMBackend
from src.memory import SessionMemory
from src.tools import calculate, get_weather, search_knowledge_base, web_search


_DEFAULT_SYSTEM_PROMPT = (
    Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"
).read_text(encoding="utf-8")


class SmartAgent:
    """可扩展的智能 Agent。"""

    def __init__(
        self,
        llm: LLMBackend = None,
        system_prompt: str = None,
        tools: List[Any] = None,
        memory: SessionMemory = None,
    ):
        self.llm = llm or LLMBackend()
        self.memory = memory or SessionMemory()
        self.tools = tools or [calculate, search_knowledge_base, get_weather, web_search]
        self.system_prompt = system_prompt or _DEFAULT_SYSTEM_PROMPT
        self._agent = Agent(
            name="智能助手",
            instructions=self.system_prompt,
            model=self.llm.chat_model,
            tools=self.tools,
        )

    async def run(
        self,
        user_input: str,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """运行一次对话轮次。"""
        conversation = context or self.memory.get_context()
        conversation.append({"role": "user", "content": user_input})

        result = await Runner.run(
            self._agent,
            input=conversation,
        )

        answer = result.final_output
        self.memory.add("user", user_input)
        self.memory.add("assistant", answer)

        return {
            "answer": answer,
            "tool_calls": getattr(result, "tool_calls", []),
            "model": self.llm.model_name,
        }

    async def run_stream(self, user_input: str):
        """流式运行（Agents SDK 支持时）。当前返回完整结果。"""
        return await self.run(user_input)
