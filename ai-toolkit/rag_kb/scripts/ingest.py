import argparse
import sys
from pathlib import Path

# 将 src 加入路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import RAGConfig
from src.loader import DocumentLoader
from src.vector_store import VectorStore


def main():
    parser = argparse.ArgumentParser(description="构建 RAG 知识库索引")
    parser.add_argument("--dir", type=str, default=RAGConfig().data_dir, help="文档目录")
    args = parser.parse_args()

    config = RAGConfig(data_dir=args.dir)
    print(f"正在加载文档：{config.data_dir}")
    documents = DocumentLoader(config.data_dir).load()
    print(f"共加载 {len(documents)} 个文件/页面")

    store = VectorStore(config)
    store.build(documents)
    print(f"索引已保存至：{config.vector_store_dir}")


if __name__ == "__main__":
    main()
