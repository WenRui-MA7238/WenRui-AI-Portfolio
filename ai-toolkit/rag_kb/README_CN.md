# RAG Knowledge Base

> Tech Stack: Qwen3 (DashScope / Ollama / vLLM) + LangChain + FAISS

## 1. Goal
- Vectorize local documents and enable semantic retrieval
- Provide a runnable Retrieval-Augmented Generation (RAG) service
- Switch between online and offline LLMs for local debugging and production deployment

## 2. Project Structure

```
rag_kb/
├── data/                    # Raw documents (add your own)
├── vector_store/            # FAISS index persistence directory
├── src/
│   ├── __init__.py
│   ├── config.py            # Configuration hub (models, paths, hyperparameters)
│   ├── embeddings.py        # Embedding model wrapper
│   ├── vector_store.py      # FAISS index build/load/search
│   ├── loader.py            # Document parsing (txt/pdf/docx/md)
│   ├── rag_service.py       # Main RAG service
│   └── llm_clients.py       # Multiple Qwen3 access methods
├── scripts/
│   ├── ingest.py            # One-click document indexing
│   └── query.py             # CLI query
├── tests/
│   └── test_retrieval.py    # Retrieval unit tests
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Quick Start

### 3.1 Install Dependencies

```bash
cd ai-toolkit/rag_kb
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Configure API Key

Copy `.env.example` to `.env` and fill in your DashScope API Key:

```env
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen3-235b-a22b          # or qwen3-30b-a3b, qwen3-14b
EMBEDDING_MODEL=text-embedding-v3  # DashScope embedding model
VECTOR_STORE_DIR=./vector_store
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K=5
SIMILARITY_THRESHOLD=0.75
```

### 3.3 Local Mode (No Internet Required)

To use Ollama or vLLM locally, update `.env`:

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen3:14b
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```

### 3.4 Build Index

Place documents in `data/` and run:

```bash
python scripts/ingest.py --dir data/
```

### 3.5 Query

```bash
python scripts/query.py "Explain the principle of RAG"
```

## 4. Key Design

- **Chunking Strategy**: Default 512 tokens / 64 overlap, semantic paragraph-aware splitting
- **Retrieval**: FAISS + cosine similarity, supports metadata filtering (source, section, etc.)
- **Prompt**: Strictly answer based on reference materials; explicitly refuse when no relevant information is found
- **Evaluation Metrics**: Retrieval Recall@K, generation Faithfulness (requires evaluation dataset)
- **Fallback Strategy**: Return "No relevant information found" when retrieval fails, avoiding hallucination

## 5. Production Notes

- Deploy local inference with `vLLM` + `Qwen3` to reduce latency and cost
- FAISS is suitable for small-to-medium scale (< 10M entries); for large scale, migrate to Milvus/Zilliz
- Periodically detect data drift and re-index outdated documents
- Log retrieval results and generated outputs for offline evaluation and badcase review
