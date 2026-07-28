"""
Extract receipt / ticket key fields from an image.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="Receipt key-field extraction")
    parser.add_argument("--image", type=str, required=True, help="Image path")
    parser.add_argument("--output", type=str, default="receipt.json", help="Output JSON path")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()
    receipt = assistant.extract_receipt(args.image)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
