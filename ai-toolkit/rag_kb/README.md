# RAG 智能知识库

> 技术栈：Qwen3 (DashScope / Ollama / vLLM) + LangChain + FAISS

## 1. 目标
- 支持本地文档向量化与语义检索
- 提供可运行的检索增强生成（RAG）服务
- 离线/在线 LLM 可切换，方便本地调试与生产部署

## 2. 项目结构

```
rag_kb/
├── data/                    # 原始文档（用户自行放入）
├── vector_store/            # FAISS 索引持久化目录
├── src/
│   ├── __init__.py
│   ├── config.py            # 配置中心（模型、路径、超参）
│   ├── embeddings.py        # 嵌入模型封装
│   ├── vector_store.py      # FAISS 索引构建/加载/搜索
│   ├── loader.py            # 文档解析（txt/pdf/docx/md）
│   ├── rag_service.py       # RAG 主服务
│   └── llm_clients.py       # Qwen3 多种接入方式
├── scripts/
│   ├── ingest.py            # 一键索引文档
│   └── query.py             # 命令行查询
├── tests/
│   └── test_retrieval.py    # 检索单元测试
├── requirements.txt
├── .env.example
└── README.md
```

## 3. 快速开始

### 3.1 安装依赖

```bash
cd ai-toolkit/rag_kb
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 DashScope API Key：

```env
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen3-235b-a22b          # 或 qwen3-30b-a3b, qwen3-14b
EMBEDDING_MODEL=text-embedding-v3  # DashScope 嵌入模型
VECTOR_STORE_DIR=./vector_store
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K=5
SIMILARITY_THRESHOLD=0.75
```

### 3.3 本地模式（无需联网）

如使用 Ollama 或 vLLM 本地 Qwen3，修改 `.env`：

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen3:14b
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```

### 3.4 构建索引

把文档放入 `data/`，然后运行：

```bash
python scripts/ingest.py --dir data/
```

### 3.5 查询

```bash
python scripts/query.py "介绍一下 RAG 的原理"
```

## 4. 关键设计

- **Chunk 策略**：默认 512 tokens / 64 overlap，按语义段落优先切分
- **检索**：FAISS + 余弦相似度，支持元数据过滤（文件来源、章节等）
- **Prompt**：严格约束基于参考资料回答，无相关信息时明确拒绝
- **评估指标**：检索 Recall@K、生成 Faithfulness（需接入评估数据集）
- **降级策略**：检索不到相关文档时返回"未找到相关信息"，不 hallucinate

## 5. 生产注意事项

- 使用 `vLLM` + `Qwen3` 部署本地推理服务，降低延迟和成本
- FAISS 仅适合中小规模（< 1000 万条），超大规模建议迁移到 Milvus/Zilliz
- 定期检测数据漂移，重新索引过期文档
- 记录每次查询的检索结果与生成结果，用于离线评估和 badcase 复盘
