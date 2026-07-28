# OpenAI SDK / Agents SDK Smart Agent

> Tech Stack: OpenAI Agents SDK (Python) + Tool Calling + Memory Management

## 1. Goal
- Build an extensible ReAct Agent based on the Agents SDK
- Support function calling, multi-turn memory, and context routing
- Provide multiple LLM backends: OpenAI / DashScope / local vLLM

## 2. Project Structure

```
agent_sdk/
├── src/
│   ├── __init__.py
│   ├── config.py            # Config: API keys, models, tool list
│   ├── llm_backend.py       # Multi-backend LLM wrapper (OpenAI/DashScope/Ollama)
│   ├── agent.py             # Agent main class
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_kb.py     # Call RAG knowledge base
│   │   ├── calculator.py    # Calculator
│   │   ├── weather.py       # Weather query (demo)
│   │   └── web_search.py    # Web search (demo)
│   ├── memory/
│   │   ├── __init__.py
│   │   └── session_memory.py  # Session-level memory
│   └── prompts/
│       └── system_prompt.txt
├── scripts/
│   ├── run_agent.py         # CLI interaction
│   └── run_server.py        # FastAPI service entry (optional)
├── tests/
│   └── test_tools.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Quick Start

### 3.1 Install Dependencies

```bash
cd ai-toolkit/agent_sdk
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Configure

Copy `.env.example` to `.env`:

```env
# Use official OpenAI
OPENAI_API_KEY=sk-xxxx
AGENT_MODEL=gpt-4o-mini

# Or Alibaba DashScope (Qwen3)
# LLM_PROVIDER=dashscope
# DASHSCOPE_API_KEY=sk-xxxx
# DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
# AGENT_MODEL=qwen3-30b-a3b

# Or local vLLM/Ollama
# LLM_PROVIDER=ollama
# LLM_BASE_URL=http://localhost:11434/v1
# AGENT_MODEL=qwen3:14b
```

### 3.3 Run CLI Agent

```bash
python scripts/run_agent.py
```

## 4. Key Design

- **ReAct Loop**: Agent follows `thought → action → observation → final_answer`
- **Tool Registration**: All tool functions register via decorators with automatic schema generation
- **Memory**: Session-level short-term memory + extensible persistent memory interface
- **Safety**: Validate parameters before tool execution and return friendly errors on exceptions
- **Fallback**: Return a default reply and log errors when the LLM is unavailable

## 5. Extending Tools

Add new Python functions in `src/tools/` with a `@tool` decorator to auto-register. The Agent generates tool schemas from docstrings and type annotations.

## 6. Production Notes

- Agents are not suitable for infinite long tasks; always set `max_steps` and timeout
- Tool failures should be gracefully handled; avoid exposing raw stack traces to users
- Log full conversation traces for review and system prompt optimization
- Add human confirmation nodes for sensitive actions (e.g., placing orders, deleting data)
