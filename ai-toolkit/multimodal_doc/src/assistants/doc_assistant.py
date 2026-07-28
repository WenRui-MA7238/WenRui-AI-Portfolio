import os
import base64
import json
from pathlib import Path
from typing import Union, Optional
import requests
from openai import OpenAI

from src.config import VisionConfig


class VisionProvider:
    """多模态视觉模型统一封装：DashScope Qwen2.5-VL / OpenAI GPT-4.1 Vision"""

    def __init__(self, config: VisionConfig = None):
        self.config = config or VisionConfig()
        self.client = OpenAI(
            api_key=self.config.api_key or "",
            base_url=self.config.base_url,
        )

    def _encode_image(self, image_path: Union[str, Path]) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _image_mime(self, image_path: Union[str, Path]) -> str:
        ext = Path(image_path).suffix.lower()
        mapping = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
        return mapping.get(ext, "image/jpeg")

    def ask_image(self, image_path: Union[str, Path], prompt: str, json_output: bool = False) -> str:
        """对单张图片进行提问"""
        b64 = self._encode_image(image_path)
        mime = self._image_mime(image_path)
        image_url = f"data:{mime};base64,{b64}"

        if json_output:
            system_prompt = "你是一个多模态文档助手。请按用户要求提取结构化信息，并只返回合法的 JSON 字符串，不要包含 markdown 代码块。"
        else:
            system_prompt = "你是一个多模态文档助手。请准确理解图片内容并回答用户问题。"

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ]

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=2048,
            temperature=0.1,
        )
        return response.choices[0].message.content


class MultimodalDocAssistant:
    """多模态文档助手：OCR / 表格 / 票据 / 描述"""

    def __init__(self, provider: VisionProvider = None):
        self.provider = provider or VisionProvider()

    def ocr(self, image_path: Union[str, Path], json_output: bool = False) -> str:
        """提取图片中的文字"""
        prompt = (
            "请提取图片中的所有文字内容，保留原始段落和排版。"
            "如果是表格，请输出 Markdown 表格。"
            "如果是表单，请输出字段名和值的对照。"
        )
        return self.provider.ask_image(image_path, prompt, json_output)

    def extract_table(self, image_path: Union[str, Path]) -> dict:
        """提取表格并返回 JSON"""
        prompt = (
            "请提取图片中的表格内容，并以 JSON 格式返回。"
            "JSON 格式为：{\"headers\": [...], \"rows\": [[...], ...]}。"
            "不要包含任何额外说明。"
        )
        raw = self.provider.ask_image(image_path, prompt, json_output=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw, "parse_error": True}

    def describe(self, image_path: Union[str, Path]) -> str:
        """描述图片内容"""
        prompt = "请用一段简洁的话描述这张图片的内容，包括主要物体、文字、布局和潜在含义。"
        return self.provider.ask_image(image_path, prompt)

    def extract_invoice(self, image_path: Union[str, Path]) -> dict:
        """提取发票关键字段"""
        prompt = (
            "请提取图片中发票的关键字段，以 JSON 格式返回："
            "{\"发票号码\": ..., \"开票日期\": ..., \"购买方\": ..., \"销售方\": ..., \"金额\": ..., \"税额\": ..., \"价税合计\": ..., \"备注\": ...}"
            "如果某字段未找到，值设为 null。不要包含额外说明。"
        )
        raw = self.provider.ask_image(image_path, prompt, json_output=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw, "parse_error": True}
