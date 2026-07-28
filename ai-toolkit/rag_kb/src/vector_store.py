import os
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.config import RAGConfig
from src.embeddings import EmbeddingProvider


class VectorStore:
    """FAISS 向量库封装：构建、保存、加载、检索"""

    def __init__(self, config: RAGConfig):
        self.config = config
        self.index_path = config.vector_store_dir
        os.makedirs(self.index_path, exist_ok=True)
        self.embeddings = EmbeddingProvider(config).get_embeddings()
        self._store: Optional[FAISS] = None

    def build(self, documents: List[Document]) -> None:
        """从文档构建 FAISS 索引"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            separators=["\n\n", "\n", "。", " ", ""],
        )
        chunks = splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            chunk.metadata.setdefault("chunk_id", i)

        self._store = FAISS.from_documents(chunks, self.embeddings)
        self.save()

    def load(self) -> None:
        """加载已有 FAISS 索引"""
        if not os.path.exists(os.path.join(self.index_path, "index.faiss")):
            raise FileNotFoundError(f"未找到索引：{self.index_path}")
        self._store = FAISS.load_local(
            self.index_path, self.embeddings, allow_dangerous_deserialization=True
        )

    def save(self) -> None:
        """保存索引"""
        if self._store is None:
            raise RuntimeError("索引未构建")
        self._store.save_local(self.index_path)

    def search(self, query: str, top_k: Optional[int] = None, filters: Optional[dict] = None) -> List[dict]:
        """语义检索，返回带 score 的结果"""
        if self._store is None:
            self.load()

        k = top_k or self.config.top_k
        docs_with_score = self._store.similarity_search_with_score(query, k=k, filter=filters)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score),
            }
            for doc, score in docs_with_score
        ]
