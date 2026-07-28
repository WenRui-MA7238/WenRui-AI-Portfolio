"""
Local Qwen2.5-VL provider wrapper using transformers.
Requires significant VRAM for 7B/14B models.
"""

from pathlib import Path
from typing import Union


class QwenVLProvider:
    """Local Qwen2.5-VL model wrapper."""

    def __init__(self, model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct", device: str = "auto"):
        self.model_name = model_name
        self.device = device
        self._model = None
        self._processor = None

    def _lazy_load(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
            from qwen_vl_utils import process_vision_info

            self._torch = torch
            self._process_vision_info = process_vision_info
            self._processor = AutoProcessor.from_pretrained(self.model_name, trust_remote_code=True)
            self._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=torch.bfloat16,
                device_map=self.device,
                trust_remote_code=True,
            )
            self._model.eval()
        except Exception as e:
            raise RuntimeError(
                f"Failed to load local Qwen2.5-VL: {e}\n"
                "Make sure transformers, torch, torchvision, qwen-vl-utils are installed."
            ) from e

    def ask_image(
        self,
        image_path: Union[str, Path],
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ) -> str:
        self._lazy_load()

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": str(image_path)},
                    {"type": "text", "text": prompt},
                ],
            },
        ]

        text = self._processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = self._process_vision_info(messages)
        inputs = self._processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to(self._model.device)

        with self._torch.no_grad():
            generated_ids = self._model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
            )
        generated_ids_trimmed = [
            out_ids[len(in_ids) :]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self._processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        return output_text[0]
