import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import RAGConfig
from src.vector_store import VectorStore
from src.rag_service import LLMClient, RAGService


def main():
    parser = argparse.ArgumentParser(description="RAG 查询")
    parser.add_argument("question", type=str, help="问题")
    parser.add_argument("--store", type=str, default=RAGConfig().vector_store_dir, help="索引目录")
    args = parser.parse_args()

    config = RAGConfig(vector_store_dir=args.store)
    store = VectorStore(config)
    llm = LLMClient(config)
    service = RAGService(config, store, llm)

    print(f"\n问题：{args.question}\n")
    result = service.query(args.question)
    print(f"回答：\n{result['answer']}\n")
    print(f"引用来源：{result['sources']}")
    print(f"Token 用量：{result['tokens_used']}")


if __name__ == "__main__":
    main()
