# AI Toolkit 使用说明

## 第一步：准备环境

### 1.1 安装 Python 依赖

打开 PowerShell，依次进入三个目录安装依赖：

```powershell
# 进入 RAG 知识库
cd $HOME\Desktop\ai-toolkit\rag_kb
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 进入 AI Agent
cd $HOME\Desktop\ai-toolkit\agent_sdk
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 进入多模态文档助手
cd $HOME\Desktop\ai-toolkit\multimodal_doc
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> 如果提示 `pip` 找不到，说明 Python 环境有问题，需要先安装 Python 3.10+。

### 1.2 选择运行模式

进入 `ai-toolkit` 目录，把 `.env.example` 复制为 `.env`：

```powershell
cd $HOME\Desktop\ai-toolkit
Copy-Item .env.example .env
notepad .env
```

下面提供两种模式，二选一。

---

## 模式 A：使用阿里云 DashScope API（推荐，效果最好）

适合：想快速体验、电脑配置一般、需要多模态识别

### 申请 Key

1. 访问 https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 进入控制台，创建 API Key
4. 新用户通常有免费额度

### 修改 .env

```env
DASHSCOPE_API_KEY=sk-你的真实Key
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

### 保存即可使用

---

## 模式 B：完全本地运行（无需 API，但需要硬件支持）

适合：不想联网调用 API、有较好电脑配置

### 安装 Ollama

1. 访问 https://ollama.com/download
2. 下载并安装 Ollama
3. 打开 PowerShell，拉取本地模型：

```powershell
# 拉取 Qwen3 14B（Agent + RAG 用）
ollama pull qwen3:14b

# 拉取嵌入模型（RAG 用）
ollama pull nomic-embed-text

# 拉取多模态模型（可选，需要较强显卡）
ollama pull x/xxx  # 注意：Ollama 上 Qwen2.5-VL 支持有限，多模态建议用 API
```

### 修改 .env

```env
# 本地 RAG
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen3:14b
EMBEDDING_PROVIDER=ollama
EMBEDDING_BASE_URL=http://localhost:11434/v1
EMBEDDING_MODEL=nomic-embed-text

# 本地 Agent
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:14b

# 多模态（本地门槛高，建议保留 API 模式）
VISION_PROVIDER=dashscope
VISION_MODEL=qwen2.5-vl-72b-instruct
```

---

## 第二步：使用 RAG 智能知识库

### 放入文档

把你要查询的文档复制到：

```
Desktop\ai-toolkit\rag_kb\data\
```

支持格式：`.txt`、`.md`、`.pdf`、`.docx`

### 构建索引

```powershell
cd $HOME\Desktop\ai-toolkit\rag_kb
.venv\Scripts\activate
python scripts/ingest.py --dir data/
```

看到"索引已保存"就成功了。

### 查询

```powershell
python scripts/query.py "这里输入你的问题"
```

例如：

```powershell
python scripts/query.py "这份文档主要讲了什么"
python scripts/query.py "合同里的付款条款是什么"
```

---

## 第三步：使用 AI Agent

```powershell
cd $HOME\Desktop\ai-toolkit\agent_sdk
.venv\Scripts\activate
python scripts/run_agent.py
```

启动后输入问题：

```
3.5 * 12 + 7 等于多少
查一下知识库里有 RAG 相关的内容
今天北京天气怎么样
```

输入 `exit` 退出。

---

## 第四步：使用多模态文档助手

### 识别图片文字

把图片放到：

```
Desktop\ai-toolkit\multimodal_doc\data\images\
```

然后执行：

```powershell
cd $HOME\Desktop\ai-toolkit\multimodal_doc
.venv\Scripts\activate
python scripts/extract_text.py --image data/images/你的图片.png
```

### 识别 PDF

```powershell
python scripts/extract_text.py --pdf data/pdfs/你的文件.pdf --output output.txt
```

### 提取表格

```powershell
python scripts/analyze_table.py --image data/images/表格.png --output table.json
```

### 图片描述

```powershell
python scripts/describe_image.py --image data/images/你的图片.png
```

---

## 第五步：三者联动（完整工作流）

把"图片/PDF → 文本 → 知识库 → Agent 问答"串起来：

```powershell
# 1. 提取 PDF 文字
cd $HOME\Desktop\ai-toolkit\multimodal_doc
.venv\Scripts\activate
python scripts/extract_text.py --pdf data/pdfs/合同.pdf --output contract.txt

# 2. 把文字放进 RAG 知识库
Move-Item contract.txt $HOME\Desktop\ai-toolkit\rag_kb\data\合同.txt

# 3. 构建索引
cd $HOME\Desktop\ai-toolkit\rag_kb
.venv\Scripts\activate
python scripts/ingest.py --dir data/

# 4. 用 Agent 查询
cd $HOME\Desktop\ai-toolkit\agent_sdk
.venv\Scripts\activate
python scripts/run_agent.py
# 输入：查一下合同里的付款条款
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| pip install 很慢 | 默认 PyPI 在国外 | 用清华镜像：`-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| 提示 API Key 无效 | Key 填错或没额度 | 检查 `.env` 里的 Key，或去 DashScope 控制台确认 |
| FAISS 安装失败 | 环境不兼容 | 当前 Python 3.11 应该没问题，可尝试 `pip install faiss-cpu` 单独装 |
| Agent 查知识库失败 | RAG 索引没建 | 先运行 `rag_kb/scripts/ingest.py` |
| 多模态运行很慢 | 本地没有 GPU | 改用 DashScope 云端模型 |
| Ollama 模型下载慢 | 默认源在国外 | 可以配置 Ollama 国内镜像 |

---

## 文件说明

- `.env`：你自己的配置文件，**不要分享给别人**
- `.env.example`：配置模板
- `requirements.txt`：依赖清单
- `scripts/`：可以直接运行的脚本
- `src/`：核心代码
- `README.md`：每个组件的详细说明

---

## 推荐学习顺序

1. 先跑通 RAG 知识库（最实用）
2. 再试 AI Agent（理解工具调用）
3. 最后多模态文档助手（识别图片/PDF）
4. 三者联动（完整 AI 应用链路）
