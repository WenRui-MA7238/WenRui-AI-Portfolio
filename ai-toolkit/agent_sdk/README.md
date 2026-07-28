# OpenAI SDK / Agents SDK 智能 Agent

> 技术栈：OpenAI Agents SDK（Python） + 工具调用 + 记忆管理

## 1. 目标
- 基于 Agents SDK 构建一个可扩展的 ReAct Agent
- 支持函数调用、多轮记忆、上下文路由
- 提供 OpenAI / DashScope / 本地 vLLM 等多种 LLM 后端

## 2. 项目结构

```
agent_sdk/
├── src/
│   ├── __init__.py
│   ├── config.py            # 配置：API Key、模型、工具列表
│   ├── llm_backend.py       # 多后端 LLM 封装（OpenAI/DashScope/Ollama）
│   ├── agent.py             # Agent 主类
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_kb.py     # 调用 RAG 知识库
│   │   ├── calculator.py    # 计算器
│   │   ├── weather.py       # 天气查询（示例）
│   │   └── web_search.py    # 网络搜索（示例）
│   ├── memory/
│   │   ├── __init__.py
│   │   └── session_memory.py  # 会话级记忆
│   └── prompts/
│       └── system_prompt.txt
├── scripts/
│   ├── run_agent.py         # 命令行交互
│   └── run_server.py        # FastAPI 服务入口（可选）
├── tests/
│   └── test_tools.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. 快速开始

### 3.1 安装依赖

```bash
cd ai-toolkit/agent_sdk
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 配置

复制 `.env.example` 为 `.env`：

```env
# 使用 OpenAI 官方
OPENAI_API_KEY=sk-xxxx
AGENT_MODEL=gpt-4o-mini

# 或阿里 DashScope（Qwen3）
# LLM_PROVIDER=dashscope
# DASHSCOPE_API_KEY=sk-xxxx
# DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
# AGENT_MODEL=qwen3-30b-a3b

# 或本地 vLLM/Ollama
# LLM_PROVIDER=ollama
# LLM_BASE_URL=http://localhost:11434/v1
# AGENT_MODEL=qwen3:14b
```

### 3.3 运行命令行 Agent

```bash
python scripts/run_agent.py
```

## 4. 关键设计

- **ReAct 循环**：Agent 根据用户输入决定 `thought → action → observation → final_answer`
- **工具注册**：所有工具函数通过装饰器注册，支持自动 schema 生成
- **记忆**：会话级短期记忆 + 可扩展的持久化记忆接口
- **安全**：工具调用前校验参数，异常时返回友好提示
- **降级**：LLM 不可用时返回兜底回复并记录错误

## 5. 扩展工具

在 `src/tools/` 新增 Python 函数，加上 `@tool` 装饰器即可自动注册。Agent 会根据函数 docstring 和类型注解生成 tool schema。

## 6. 生产注意事项

- Agent 不适合长任务无限循环，必须设置 `max_steps` 和超时
- 工具调用失败要收敛，避免把原始堆栈直接暴露给用户
- 记录完整对话轨迹，便于复盘和优化 system prompt
- 对敏感操作（如下单、删除数据）增加人工确认节点
