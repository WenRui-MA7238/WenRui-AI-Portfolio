"""
Unit tests for image/pdf processors.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.processors.image_loader import ImageLoader
from src.processors.pdf_loader import PDFLoader


def test_image_loader_resize():
    loader = ImageLoader(max_size=(100, 100))
    # Create a dummy image in memory
    from PIL import Image
    img = Image.new("RGB", (200, 150), color="red")
    resized = loader.resize_if_needed(img)
    assert resized.width <= 100 and resized.height <= 100


def test_pdf_loader_creates_images(tmp_path):
    # PyMuPDF requires a real PDF; this test is skipped if no test PDF exists.
    pdf_path = Path(__file__).resolve().parent.parent / "data" / "pdfs" / "sample.pdf"
    if not pdf_path.exists():
        return
    loader = PDFLoader(dpi=72)
    images = loader.to_images(pdf_path, tmp_path)
    assert len(images) > 0


if __name__ == "__main__":
    test_image_loader_resize()
    test_pdf_loader_creates_images(Path("/tmp"))
    print("Processor tests passed.")
