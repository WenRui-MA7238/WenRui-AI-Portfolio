# OpenAI Agents SDK 智能 Agent

> 技术栈：OpenAI Agents SDK + 多后端 LLM + 工具调用 + 会话记忆 + FastAPI 服务

## 1. 目标

构建一个可扩展的 ReAct 风格 Agent，包含企业级工程实践：

- 多后端 LLM：OpenAI / 阿里云 DashScope（Qwen3）/ Ollama / vLLM
- 工具调用：计算器、RAG 知识库搜索、天气、联网搜索
- 会话记忆：短期对话历史 + 多会话隔离存储
- HTTP API：基于 FastAPI 的会话隔离服务
- 生产就绪：安全求值、优雅错误、可扩展工具注册

## 2. 项目结构

```
agent_sdk/
├── src/
│   ├── __init__.py
│   ├── config.py            # 兼容旧版配置类
│   ├── llm_backend.py       # 统一 LLM 后端封装
│   ├── agent.py             # SmartAgent 主类
│   ├── prompts/
│   │   └── system_prompt.txt
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py    # 安全数学计算
│   │   ├── search_kb.py     # RAG 知识库集成
│   │   ├── weather.py       # 天气示例工具
│   │   └── web_search.py    # 联网搜索示例工具
│   └── memory/
│       ├── __init__.py
│       └── session_memory.py  # 会话级记忆存储
├── scripts/
│   ├── run_agent.py         # 命令行交互
│   └── run_server.py        # FastAPI 服务入口
├── tests/
│   └── test_tools.py        # 工具单元测试
├── requirements.txt
├── .env.example
└── README.md
```

## 3. 快速开始

### 3.1 安装

```bash
cd ai-toolkit/agent_sdk
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 配置

复制 `.env.example` 为 `.env`：

```env
# 方案 1：OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxx
OPENAI_MODEL=gpt-4o-mini

# 方案 2：DashScope Qwen3
# LLM_PROVIDER=dashscope
# DASHSCOPE_API_KEY=sk-xxxx
# DASHSCOPE_MODEL=qwen3-30b-a3b

# 方案 3：本地 Ollama / vLLM
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434/v1
# OLLAMA_MODEL=qwen3:14b
```

### 3.3 命令行运行

```bash
python scripts/run_agent.py
```

### 3.4 启动 FastAPI 服务

```bash
python scripts/run_server.py
```

调用示例：

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "3.5 * 12 等于多少？"}'
```

## 4. 核心设计

- **LLMBackend**：集中管理不同供应商的 API key、base URL 和模型选择。
- **工具注册**：每个工具都是带装饰器的函数，根据类型注解和 docstring 自动生成 schema。
- **SessionMemory**：每个会话保留最近 N 轮对话，防止上下文无限增长。
- **RAG 集成**：`search_knowledge_base` 动态导入 `rag_kb`，让 Agent 能基于索引文档回答问题。
- **安全性**：计算器使用白名单和 `{"__builtins__": {}}` 防止代码注入。

## 5. 扩展工具

在 `src/tools/` 新增文件：

```python
from agents import function_tool

@function_tool
def my_tool(param: str) -> str:
    """描述工具作用。"""
    return f"Result for {param}"
```

然后在 `src/tools/__init__.py` 导入，并传给 `SmartAgent`。

## 6. 生产注意事项

- 设置 `max_steps` 和请求超时，防止 Agent 失控。
- 将天气/联网搜索示例工具替换为真实 API。
- 使用 Redis/Postgres 持久化记忆，实现跨会话连续对话。
- 记录对话轨迹和工具输出，便于调试和审计。
- 对删除、下单、转账等敏感操作要求用户明确确认。
