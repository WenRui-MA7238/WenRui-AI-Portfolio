from dataclasses import dataclass, field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RAGConfig:
    """RAG 服务配置"""
    # 向量库
    vector_store_dir: str = os.getenv("VECTOR_STORE_DIR", "./vector_store")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "64"))
    top_k: int = int(os.getenv("TOP_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.75"))

    # 嵌入模型
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "dashscope")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")
    embedding_base_url: Optional[str] = os.getenv("EMBEDDING_BASE_URL")
    embedding_api_key: Optional[str] = os.getenv("EMBEDDING_API_KEY") or os.getenv("DASHSCOPE_API_KEY")

    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "dashscope")
    llm_model: str = os.getenv("LLM_MODEL", "qwen3-235b-a22b")
    llm_base_url: Optional[str] = os.getenv("LLM_BASE_URL") or os.getenv("DASHSCOPE_BASE_URL")
    llm_api_key: Optional[str] = os.getenv("LLM_API_KEY") or os.getenv("DASHSCOPE_API_KEY")

    # 文档目录
    data_dir: str = os.getenv("DATA_DIR", "./data")

    # 生成参数
    temperature: float = float(os.getenv("TEMPERATURE", "0.1"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1024"))

    # 元数据过滤字段
    metadata_fields: list[str] = field(default_factory=lambda: ["source", "page"])
