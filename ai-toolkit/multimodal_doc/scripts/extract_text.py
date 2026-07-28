import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.assistants.doc_assistant import MultimodalDocAssistant


def main():
    parser = argparse.ArgumentParser(description="图片/PDF OCR 文字提取")
    parser.add_argument("--image", type=str, help="图片路径")
    parser.add_argument("--pdf", type=str, help="PDF 路径（会先转为图片）")
    parser.add_argument("--output", type=str, help="输出文件路径")
    args = parser.parse_args()

    assistant = MultimodalDocAssistant()

    if args.image:
        image_path = args.image
    elif args.pdf:
        from src.processors.pdf_loader import PDFLoader
        loader = PDFLoader()
        out_dir = Path(args.pdf).parent / "pdf_images"
        images = loader.to_images(args.pdf, out_dir)
        print(f"PDF 已转为 {len(images)} 张图片")
        image_path = images[0]
    else:
        raise ValueError("请指定 --image 或 --pdf")

    print(f"正在提取：{image_path}")
    text = assistant.ocr(image_path)
    print("\n提取结果：\n")
    print(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n已保存至：{args.output}")


if __name__ == "__main__":
    main()
