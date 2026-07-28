"""
Agent 配置（向后兼容旧版）
"""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class AgentConfig:
    """Agent 配置"""

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    DASHSCOPE_BASE_URL = os.getenv(
        "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen3-30b-a3b")

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:14b")

    @property
    def agent_model(self) -> str:
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_MODEL
        elif self.LLM_PROVIDER == "dashscope":
            return self.DASHSCOPE_MODEL
        elif self.LLM_PROVIDER in ("ollama", "vllm"):
            return self.OLLAMA_MODEL
        return self.OPENAI_MODEL

    @property
    def base_url(self) -> Optional[str]:
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_BASE_URL
        elif self.LLM_PROVIDER == "dashscope":
            return self.DASHSCOPE_BASE_URL
        elif self.LLM_PROVIDER in ("ollama", "vllm"):
            return self.OLLAMA_BASE_URL
        return None

    @property
    def api_key(self) -> Optional[str]:
        if self.LLM_PROVIDER == "openai":
            return self.OPENAI_API_KEY
        elif self.LLM_PROVIDER == "dashscope":
            return self.DASHSCOPE_API_KEY
        return None
