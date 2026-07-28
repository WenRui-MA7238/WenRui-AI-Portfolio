"""
Image preprocessing utilities for vision models.
"""

from pathlib import Path
from typing import Union, Tuple

from PIL import Image


class ImageLoader:
    """Load and preprocess images for vision models."""

    def __init__(self, max_size: Tuple[int, int] = (2048, 2048)):
        self.max_size = max_size

    def load(self, image_path: Union[str, Path]) -> Image.Image:
        return Image.open(image_path).convert("RGB")

    def resize_if_needed(self, image: Image.Image) -> Image.Image:
        """Resize image if it exceeds max_size, preserving aspect ratio."""
        if image.width <= self.max_size[0] and image.height <= self.max_size[1]:
            return image
        image.thumbnail(self.max_size)
        return image

    def save_temp(self, image: Image.Image, output_path: Union[str, Path]) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "PNG")
        return output_path
