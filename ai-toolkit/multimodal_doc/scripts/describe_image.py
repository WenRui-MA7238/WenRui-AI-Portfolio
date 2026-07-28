import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="图片描述")
    parser.add_argument("--image", type=str, required=True, help="图片路径")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()
    description = assistant.describe(args.image)
    print(description)


if __name__ == "__main__":
    main()
