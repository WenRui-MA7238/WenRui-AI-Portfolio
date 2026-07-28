import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="图片表格分析")
    parser.add_argument("--image", type=str, required=True, help="图片路径")
    parser.add_argument("--output", type=str, default="table.json", help="输出 JSON 路径")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()
    table = assistant.extract_table(args.image)
    print(json.dumps(table, ensure_ascii=False, indent=2))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=2)
    print(f"\n已保存至：{args.output}")


if __name__ == "__main__":
    main()
