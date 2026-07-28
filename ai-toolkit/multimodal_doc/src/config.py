"""
Multimodal document assistant configuration.
"""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class VisionConfig:
    """多模态文档助手配置"""

    PROVIDER = os.getenv("VISION_PROVIDER", "dashscope")

    # DashScope Qwen2.5-VL
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    DASHSCOPE_BASE_URL = os.getenv(
        "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    DASHSCOPE_VL_MODEL = os.getenv("VISION_MODEL", "qwen2.5-vl-72b-instruct")

    # OpenAI GPT-4.1 Vision
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_VISION_MODEL = os.getenv("VISION_MODEL", "gpt-4.1-mini")

    # Local model
    USE_LOCAL_VL = os.getenv("USE_LOCAL_VL", "false").lower() == "true"
    LOCAL_VL_MODEL = os.getenv("LOCAL_VL_MODEL", "Qwen/Qwen2.5-VL-7B-Instruct")

    @property
    def model(self) -> str:
        if self.USE_LOCAL_VL:
            return self.LOCAL_VL_MODEL
        if self.PROVIDER == "openai":
            return self.OPENAI_VISION_MODEL
        return self.DASHSCOPE_VL_MODEL

    @property
    def base_url(self) -> Optional[str]:
        if self.USE_LOCAL_VL:
            return None
        if self.PROVIDER == "openai":
            return self.OPENAI_BASE_URL
        return self.DASHSCOPE_BASE_URL

    @property
    def api_key(self) -> Optional[str]:
        if self.USE_LOCAL_VL:
            return None
        if self.PROVIDER == "openai":
            return self.OPENAI_API_KEY
        return self.DASHSCOPE_API_KEY
