import os
from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.document_loaders import Docx2txtLoader


class DocumentLoader:
    """多格式文档加载器"""

    SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".docx"}

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def load(self) -> List[Document]:
        documents = []
        for path in self.data_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in self.SUPPORTED_EXTS:
                docs = self._load_file(path)
                for doc in docs:
                    doc.metadata.setdefault("source", str(path))
                    doc.metadata.setdefault("filename", path.name)
                documents.extend(docs)
        return documents

    def _load_file(self, path: Path) -> List[Document]:
        ext = path.suffix.lower()
        if ext == ".txt":
            loader = TextLoader(str(path), encoding="utf-8")
        elif ext == ".md":
            loader = UnstructuredMarkdownLoader(str(path))
        elif ext == ".pdf":
            loader = PyPDFLoader(str(path))
        elif ext == ".docx":
            loader = Docx2txtLoader(str(path))
        else:
            raise ValueError(f"不支持的文件格式：{ext}")
        return loader.load()
