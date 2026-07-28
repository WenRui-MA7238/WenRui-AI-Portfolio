"""
Extract ID card key fields from an image.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="ID card key-field extraction")
    parser.add_argument("--image", type=str, required=True, help="Image path")
    parser.add_argument("--output", type=str, default="id_card.json", help="Output JSON path")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()
    fields = assistant.extract_id_card(args.image)
    print(json.dumps(fields, ensure_ascii=False, indent=2))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(fields, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
