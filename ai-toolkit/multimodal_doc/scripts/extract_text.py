"""
OCR text extraction from image or PDF.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="Image/PDF OCR text extraction")
    parser.add_argument("--image", type=str, help="Image path")
    parser.add_argument("--pdf", type=str, help="PDF path (will be converted to images)")
    parser.add_argument("--output", type=str, help="Output text file path")
    parser.add_argument("--page", type=int, default=0, help="PDF page index to use (0-based)")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()

    if args.image:
        image_path = args.image
    elif args.pdf:
        from src.processors.pdf_loader import PDFLoader
        loader = PDFLoader()
        out_dir = Path(args.pdf).parent / "pdf_images"
        images = loader.to_images(args.pdf, out_dir)
        print(f"PDF converted to {len(images)} images")
        if args.page >= len(images):
            raise ValueError(f"--page {args.page} exceeds total pages {len(images)}")
        image_path = images[args.page]
    else:
        raise ValueError("Please specify --image or --pdf")

    print(f"Extracting: {image_path}")
    text = assistant.ocr(image_path)
    print("\nOCR Result:\n")
    print(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
