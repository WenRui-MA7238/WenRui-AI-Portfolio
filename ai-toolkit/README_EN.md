# AI Toolkit User Guide

## Step 1: Prepare the Environment

### 1.1 Install Python Dependencies

Open PowerShell and install dependencies for each component:

```powershell
# RAG Knowledge Base
cd $HOME\Desktop\ai-toolkit\rag_kb
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# AI Agent
cd $HOME\Desktop\ai-toolkit\agent_sdk
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Multimodal Document Assistant
cd $HOME\Desktop\ai-toolkit\multimodal_doc
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> If `pip` is not found, install Python 3.10+ first.

### 1.2 Choose a Runtime Mode

Go to the `ai-toolkit` folder, copy the environment template to `.env`:

```powershell
cd $HOME\Desktop\ai-toolkit
Copy-Item .env.example .env
notepad .env
```

Choose one of the two modes below.

---

## Mode A: Use Alibaba Cloud DashScope API (Recommended)

Best for: quick start, average hardware, multimodal recognition.

### Get an API Key

1. Visit https://dashscope.aliyun.com/
2. Register or log in with an Alibaba Cloud account
3. Go to the console and create an API Key
4. New users usually get free credits

### Edit `.env`

```env
DASHSCOPE_API_KEY=sk-your-real-key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# RAG
LLM_PROVIDER=dashscope
LLM_MODEL=qwen3-235b-a22b
EMBEDDING_PROVIDER=dashscope
EMBEDDING_MODEL=text-embedding-v3

# Agent
LLM_PROVIDER=dashscope
DASHSCOPE_MODEL=qwen3-30b-a3b

# Vision
VISION_PROVIDER=dashscope
VISION_MODEL=qwen2.5-vl-72b-instruct
```

Save and you are ready to go.

---

## Mode B: Fully Local (No API, Hardware Required)

Best for: no internet API calls, stronger local hardware.

### Install Ollama

1. Visit https://ollama.com/download
2. Download and install Ollama
3. Open PowerShell and pull models:

```powershell
# Qwen3 14B for Agent and RAG
ollama pull qwen3:14b

# Embedding model for RAG
ollama pull nomic-embed-text

# Multimodal model (optional, requires a strong GPU)
# Note: Qwen2.5-VL support on Ollama is limited; multimodal is recommended via API
```

### Edit `.env`

```env
# Local RAG
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen3:14b
EMBEDDING_PROVIDER=ollama
EMBEDDING_BASE_URL=http://localhost:11434/v1
EMBEDDING_MODEL=nomic-embed-text

# Local Agent
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:14b

# Vision (local is hard; keep API mode recommended)
VISION_PROVIDER=dashscope
VISION_MODEL=qwen2.5-vl-72b-instruct
```

---

## Step 2: Use the RAG Knowledge Base

### Add Documents

Copy documents to:

```
Desktop\ai-toolkit\rag_kb\data\
```

Supported formats: `.txt`, `.md`, `.pdf`, `.docx`

### Build the Index

```powershell
cd $HOME\Desktop\ai-toolkit\rag_kb
.venv\Scripts\activate
python scripts/ingest.py --dir data/
```

When you see "索引已保存" (index saved), it is ready.

### Query

```powershell
python scripts/query.py "your question here"
```

Examples:

```powershell
python scripts/query.py "What is this document about"
python scripts/query.py "What are the payment terms in the contract"
```

---

## Step 3: Use the AI Agent

```powershell
cd $HOME\Desktop\ai-toolkit\agent_sdk
.venv\Scripts\activate
python scripts/run_agent.py
```

Then type questions such as:

```
What is 3.5 * 12 + 7
Search the knowledge base for RAG related content
What is the weather in Beijing today
```

Type `exit` to quit.

---

## Step 4: Use the Multimodal Document Assistant

### Extract Text from an Image

Put images in:

```
Desktop\ai-toolkit\multimodal_doc\data\images\
```

Run:

```powershell
cd $HOME\Desktop\ai-toolkit\multimodal_doc
.venv\Scripts\activate
python scripts/extract_text.py --image data/images/your-image.png
```

### Extract Text from a PDF

```powershell
python scripts/extract_text.py --pdf data/pdfs/your-file.pdf --output output.txt
```

### Extract a Table

```powershell
python scripts/analyze_table.py --image data/images/table.png --output table.json
```

### Describe an Image

```powershell
python scripts/describe_image.py --image data/images/your-image.png
```

---

## Step 5: Combine All Three (Full Workflow)

Image/PDF → Text → Knowledge Base → Agent Q&A:

```powershell
# 1. Extract text from PDF
cd $HOME\Desktop\ai-toolkit\multimodal_doc
.venv\Scripts\activate
python scripts/extract_text.py --pdf data/pdfs/contract.pdf --output contract.txt

# 2. Move text into the RAG knowledge base
Move-Item contract.txt $HOME\Desktop\ai-toolkit\rag_kb\data\contract.txt

# 3. Build the index
cd $HOME\Desktop\ai-toolkit\rag_kb
.venv\Scripts\activate
python scripts/ingest.py --dir data/

# 4. Query via Agent
cd $HOME\Desktop\ai-toolkit\agent_sdk
.venv\Scripts\activate
python scripts/run_agent.py
# Then type: Search the knowledge base for payment terms in the contract
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `pip install` is slow | Default PyPI is overseas | Use Tsinghua mirror: `-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| Invalid API Key | Wrong key or no quota | Check `.env` or the DashScope console |
| FAISS install fails | Environment issue | Try installing separately: `pip install faiss-cpu` |
| Agent knowledge base search fails | RAG index not built | Run `rag_kb/scripts/ingest.py` first |
| Multimodal is slow | No local GPU | Use DashScope cloud model |
| Ollama model download is slow | Default source is overseas | Configure an Ollama domestic mirror |

---

## File Reference

- `.env`: your private config, **do not share**
- `.env.example`: config template
- `requirements.txt`: dependency list
- `scripts/`: runnable scripts
- `src/`: core source code
- `README.md`: detailed per-component guide

---

## Suggested Learning Order

1. Run the RAG knowledge base first (most practical)
2. Try the AI Agent (tool calling)
3. Try the multimodal assistant (image/PDF recognition)
4. Combine all three for a complete AI application pipeline
