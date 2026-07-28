# OpenAI Agents SDK Smart Agent

> Tech Stack: OpenAI Agents SDK + Multi-backend LLM + Tool Calling + Session Memory + FastAPI Service

## 1. Goal

Build an extensible ReAct-style Agent with real-world engineering patterns:

- Multi-backend LLM: OpenAI / DashScope (Qwen3) / Ollama / vLLM
- Tool calling: calculator, RAG KB search, weather, web search
- Session memory: short-term conversation history + multi-session store
- HTTP API: FastAPI service with session isolation
- Production-ready: safe eval, graceful errors, extensible tool registry

## 2. Project Structure

```
agent_sdk/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_backend.py
│   ├── agent.py
│   ├── prompts/
│   │   └── system_prompt.txt
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   ├── search_kb.py
│   │   ├── weather.py
│   │   └── web_search.py
│   └── memory/
│       ├── __init__.py
│       └── session_memory.py
├── scripts/
│   ├── run_agent.py
│   └── run_server.py
├── tests/
│   └── test_tools.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Quick Start

### 3.1 Install

```bash
cd ai-toolkit/agent_sdk
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Configure

Copy `.env.example` to `.env`:

```env
# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxx
OPENAI_MODEL=gpt-4o-mini

# Or DashScope Qwen3
# LLM_PROVIDER=dashscope
# DASHSCOPE_API_KEY=sk-xxxx
# DASHSCOPE_MODEL=qwen3-30b-a3b

# Or local Ollama / vLLM
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434/v1
# OLLAMA_MODEL=qwen3:14b
```

### 3.3 Run CLI

```bash
python scripts/run_agent.py
```

### 3.4 Run FastAPI Server

```bash
python scripts/run_server.py
```

Example request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 3.5 * 12?"}'
```

## 4. Key Design

- **LLMBackend**: Centralizes provider-specific API key, base URL, and model selection.
- **Tool Registry**: Each tool is a decorated function; schemas are auto-generated from type hints and docstrings.
- **SessionMemory**: Keeps N most recent turns per session; avoids unbounded context growth.
- **RAG Integration**: `search_knowledge_base` dynamically imports `rag_kb` so the Agent can answer from your indexed documents.
- **Safety**: Calculator uses an allow-list and `{"__builtins__": {}}` to prevent code injection.

## 5. Extending Tools

Add a new file in `src/tools/`:

```python
from agents import function_tool

@function_tool
def my_tool(param: str) -> str:
    """Describe what this tool does."""
    return f"Result for {param}"
```

Then import it in `src/tools/__init__.py` and pass it to `SmartAgent`.

## 6. Production Notes

- Set `max_steps` and request timeout to prevent runaway agents.
- Replace weather/web_search demo tools with real API integrations.
- Add persistent memory (Redis/Postgres) for cross-session continuity.
- Log conversation traces and tool outputs for debugging and audit.
- Require explicit user confirmation for destructive or costly actions.
