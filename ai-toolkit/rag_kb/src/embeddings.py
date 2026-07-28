import os
from typing import Optional
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings


class EmbeddingProvider:
    """统一嵌入模型封装，支持 OpenAI / DashScope / Ollama 兼容接口"""

    def __init__(self, config):
        self.config = config

    def get_embeddings(self) -> Embeddings:
        provider = self.config.embedding_provider.lower()

        if provider == "dashscope":
            # DashScope 兼容 OpenAI 接口
            return OpenAIEmbeddings(
                model=self.config.embedding_model,
                openai_api_key=self.config.embedding_api_key,
                openai_api_base=self.config.embedding_base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1",
                # 阿里云 text-embedding-v3 默认 1024 维
                dimensions=1024,
            )
        elif provider == "openai":
            return OpenAIEmbeddings(
                model=self.config.embedding_model,
                openai_api_key=self.config.embedding_api_key,
                openai_api_base=self.config.embedding_base_url or "https://api.openai.com/v1",
            )
        elif provider in ("ollama", "vllm", "local"):
            return OpenAIEmbeddings(
                model=self.config.embedding_model,
                openai_api_key=self.config.embedding_api_key or "ollama",
                openai_api_base=self.config.embedding_base_url or "http://localhost:11434/v1",
            )
        elif provider == "sentence-transformers":
            # 本地 HuggingFace 嵌入模型
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=self.config.embedding_model)
        else:
            raise ValueError(f"不支持的嵌入 provider: {provider}")
