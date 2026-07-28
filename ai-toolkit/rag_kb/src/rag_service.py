from typing import List, Optional
from openai import OpenAI

from src.config import RAGConfig


class LLMClient:
    """统一的 LLM 客户端，兼容 OpenAI / DashScope / Ollama / vLLM 接口"""

    def __init__(self, config: RAGConfig):
        self.config = config
        self.client = OpenAI(
            api_key=config.llm_api_key or "ollama",
            base_url=config.llm_base_url,
        )

    def generate(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": "你是一个严谨的基于参考资料回答问题的助手。"},
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return {
            "text": response.choices[0].message.content,
            "usage": response.usage.model_dump() if response.usage else {},
        }


class RAGService:
    """检索增强生成服务"""

    def __init__(self, config: RAGConfig, vector_store, llm: LLMClient):
        self.config = config
        self.vector_store = vector_store
        self.llm = llm

    def query(self, question: str, filters: Optional[dict] = None) -> dict:
        docs = self.vector_store.search(
            query=question,
            top_k=self.config.top_k,
            filters=filters,
        )
        relevant = [d for d in docs if d["score"] >= self.config.similarity_threshold]

        if not relevant:
            return {
                "answer": "未找到相关信息，请尝试换一种表述或补充文档。",
                "sources": [],
                "tokens_used": 0,
            }

        context = "\n\n".join(
            f"[来源：{doc['metadata'].get('source', '未知')}，相关度：{doc['score']:.3f}]\n{doc['content']}"
            for doc in relevant
        )
        prompt = self._build_prompt(question, context)
        response = self.llm.generate(prompt)

        return {
            "answer": response["text"],
            "sources": [doc["metadata"] for doc in relevant],
            "tokens_used": response["usage"].get("total_tokens", 0),
        }

    def _build_prompt(self, question: str, context: str) -> str:
        return (
            "基于以下参考资料回答问题。如果资料中没有答案，请明确说明。\n\n"
            f"参考资料：\n{context}\n\n"
            f"问题：{question}\n\n"
            "回答："
        )
