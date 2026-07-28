"""
多后端 LLM 封装：OpenAI / DashScope / Ollama / vLLM
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

load_dotenv()


class LLMBackend:
    """统一异步 LLM 后端。"""

    def __init__(
        self,
        provider: str = None,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
    ):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = self._build_client()

    def _build_client(self) -> AsyncOpenAI:
        if self.provider == "openai":
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            base_url = self.base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            model = self.model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        elif self.provider == "dashscope":
            api_key = self.api_key or os.getenv("DASHSCOPE_API_KEY")
            base_url = self.base_url or os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            model = self.model or os.getenv("DASHSCOPE_MODEL", "qwen3-30b-a3b")
        elif self.provider in ("ollama", "vllm"):
            api_key = self.api_key or os.getenv("OLLAMA_API_KEY", "ollama")
            base_url = self.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            model = self.model or os.getenv("OLLAMA_MODEL", "qwen3:14b")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        self._model_name = model
        return AsyncOpenAI(api_key=api_key or "", base_url=base_url)

    @property
    def chat_model(self) -> OpenAIChatCompletionsModel:
        return OpenAIChatCompletionsModel(model=self._model_name, openai_client=self.client)

    @property
    def model_name(self) -> str:
        return self._model_name
