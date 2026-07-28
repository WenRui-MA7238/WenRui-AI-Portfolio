import json
import sys
from pathlib import Path

from agents import function_tool


@function_tool
def search_knowledge_base(query: str) -> str:
    """搜索内部 RAG 知识库，返回相关文本片段。"""
    try:
        rag_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "rag_kb"
        if str(rag_path) not in sys.path:
            sys.path.insert(0, str(rag_path))
        from src.config import RAGConfig
        from src.vector_store import VectorStore
        from src.rag_service import LLMClient, RAGService

        config = RAGConfig()
        store = VectorStore(config)
        llm = LLMClient(config)
        service = RAGService(config, store, llm)
        result = service.query(query)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"知识库搜索失败：{e}"
