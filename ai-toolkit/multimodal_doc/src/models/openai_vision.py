"""
OpenAI GPT-4.1 Vision provider wrapper.
"""

import base64
from pathlib import Path
from typing import Union

from openai import OpenAI


class OpenAIVisionProvider:
    """OpenAI-compatible vision model wrapper (GPT-4.1 Vision)."""

    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def _encode_image(self, image_path: Union[str, Path]) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _image_mime(self, image_path: Union[str, Path]) -> str:
        ext = Path(image_path).suffix.lower()
        mapping = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }
        return mapping.get(ext, "image/jpeg")

    def ask_image(
        self,
        image_path: Union[str, Path],
        prompt: str,
        system_prompt: str = "You are a helpful multimodal document assistant.",
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> str:
        b64 = self._encode_image(image_path)
        mime = self._image_mime(image_path)
        image_url = f"data:{mime};base64,{b64}"

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
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
