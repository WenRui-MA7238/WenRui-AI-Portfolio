"""
Multimodal document assistant: OCR / table / invoice / receipt / ID card / description.
Supports cloud APIs (DashScope/OpenAI) and local Qwen2.5-VL.
"""

import json
from pathlib import Path
from typing import Union

from src.config import VisionConfig
from src.models.openai_vision import OpenAIVisionProvider
from src.models.qwen_vl import QwenVLProvider
from src.processors.ocr_prompts import (
    DESCRIBE_PROMPT,
    ID_CARD_PROMPT,
    INVOICE_PROMPT,
    OCR_PROMPT,
    RECEIPT_PROMPT,
    TABLE_PROMPT,
)


class VisionProviderFactory:
    """Factory for creating the right vision provider based on config."""

    @staticmethod
    def from_config(config: VisionConfig = None):
        config = config or VisionConfig()
        if config.USE_LOCAL_VL:
            return QwenVLProvider(model_name=config.LOCAL_VL_MODEL)
        return OpenAIVisionProvider(
            api_key=config.api_key or "",
            base_url=config.base_url,
            model=config.model,
        )


class MultimodalDocAssistant:
    """多模态文档助手主类。"""

    def __init__(self, provider=None, config: VisionConfig = None):
        self.config = config or VisionConfig()
        self.provider = provider or VisionProviderFactory.from_config(self.config)

    def _ask(self, image_path: Union[str, Path], prompt: str, json_output: bool = False) -> str:
        system_prompt = (
            "你是一个多模态文档助手。请按用户要求提取结构化信息，并只返回合法的 JSON 字符串，不要包含 markdown 代码块。"
            if json_output
            else "你是一个多模态文档助手。请准确理解图片内容并回答用户问题。"
        )
        return self.provider.ask_image(
            image_path=image_path,
            prompt=prompt,
            system_prompt=system_prompt,
        )

    def _parse_json(self, raw: str) -> dict:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw, "parse_error": True}

    def ocr(self, image_path: Union[str, Path]) -> str:
        """提取图片中的文字。"""
        return self._ask(image_path, OCR_PROMPT, json_output=False)

    def extract_table(self, image_path: Union[str, Path]) -> dict:
        """提取表格为 JSON。"""
        raw = self._ask(image_path, TABLE_PROMPT, json_output=True)
        return self._parse_json(raw)

    def extract_invoice(self, image_path: Union[str, Path]) -> dict:
        """提取发票关键字段。"""
        raw = self._ask(image_path, INVOICE_PROMPT, json_output=True)
        return self._parse_json(raw)

    def extract_receipt(self, image_path: Union[str, Path]) -> dict:
        """提取收据/小票关键字段。"""
        raw = self._ask(image_path, RECEIPT_PROMPT, json_output=True)
        return self._parse_json(raw)

    def extract_id_card(self, image_path: Union[str, Path]) -> dict:
        """提取身份证关键字段。"""
        raw = self._ask(image_path, ID_CARD_PROMPT, json_output=True)
        return self._parse_json(raw)

    def describe(self, image_path: Union[str, Path]) -> str:
        """描述图片内容。"""
        return self._ask(image_path, DESCRIBE_PROMPT, json_output=False)

    def ask(self, image_path: Union[str, Path], prompt: str) -> str:
        """自定义提问。"""
        return self._ask(image_path, prompt, json_output=False)
