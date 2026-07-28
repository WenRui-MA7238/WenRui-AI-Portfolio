# 多模态文档助手

> 技术栈：Qwen2.5-VL（云端/本地）+ GPT-4.1 Vision + PDF 处理 + 结构化输出

## 1. 目标

构建一个生产级的多模态文档理解流水线：

- 从图片和扫描 PDF 中提取文字、表格、发票、收据、身份证信息
- 同时支持云端 API（DashScope / OpenAI）和本地视觉模型（Qwen2.5-VL）
- 提供任务专用提示模板和结构化 JSON 输出
- 实现端到端流程：扫描文档 → 结构化数据 → RAG 知识库

## 2. 项目结构

```
multimodal_doc/
├── data/
│   ├── images/              # 测试图片
│   └── pdfs/                # 测试 PDF
├── src/
│   ├── __init__.py
│   ├── config.py            # 视觉模型配置
│   ├── models/
│   │   ├── __init__.py
│   │   ├── openai_vision.py  # GPT-4.1 Vision 封装
│   │   └── qwen_vl.py        # 本地 Qwen2.5-VL 封装
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── image_loader.py   # 图片预处理
│   │   ├── pdf_loader.py     # PDF 转图片
│   │   └── ocr_prompts.py    # 任务专用提示模板
│   └── assistants/
│       ├── __init__.py
│       └── doc_assistant.py  # 多模态文档助手主类
├── scripts/
│   ├── extract_text.py       # 图片/PDF 文字提取
│   ├── analyze_table.py      # 表格提取为 JSON
│   ├── extract_invoice.py    # 发票字段提取
│   ├── extract_receipt.py    # 收据/小票提取
│   ├── extract_id_card.py    # 身份证提取
│   └── describe_image.py     # 图片描述
├── tests/
│   └── test_processors.py    # 处理器单元测试
├── requirements.txt
├── .env.example
└── README.md
```

## 3. 快速开始

### 3.1 安装

```bash
cd ai-toolkit/multimodal_doc
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 配置

复制 `.env.example` 为 `.env`：

```env
# 方案 A：DashScope Qwen2.5-VL
VISION_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen2.5-vl-72b-instruct

# 方案 B：OpenAI GPT-4.1 Vision
# VISION_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxx
# OPENAI_BASE_URL=https://api.openai.com/v1
# VISION_MODEL=gpt-4.1-mini

# 方案 C：本地 Qwen2.5-VL（7B 约需 16GB 显存）
# USE_LOCAL_VL=true
# LOCAL_VL_MODEL=Qwen/Qwen2.5-VL-7B-Instruct
```

### 3.3 运行示例

图片 OCR：

```bash
python scripts/extract_text.py --image data/images/invoice.png
```

表格分析：

```bash
python scripts/analyze_table.py --image data/images/table.png --output table.json
```

发票字段提取：

```bash
python scripts/extract_invoice.py --image data/images/invoice.png --output invoice.json
```

处理 PDF：

```bash
python scripts/extract_text.py --pdf data/pdfs/report.pdf --page 0 --output page1.txt
```

## 4. 核心设计

- **Provider 抽象**：`VisionProviderFactory` 在云端和本地模型之间切换，无需改动业务逻辑。
- **PDF 流水线**：PDF 按页转为图片，再由视觉模型处理。
- **提示模板**：OCR、表格、发票、收据、身份证、描述等任务统一维护在 `src/processors/ocr_prompts.py`。
- **结构化输出**：发票/表格/收据任务要求返回 JSON，助手内置解析失败兜底。
- **图片预处理**：对大图进行缩放，避免超出模型上下文/Token 限制。

## 5. 生产注意事项

- 本地 Qwen2.5-VL 7B 约需 16GB 显存，14B 约需 28GB 显存。
- 对扫描 PDF 建议增加去噪、纠偏、二值化等图像增强。
- 敏感文档优先使用本地模型，避免上传云端。
- 对金额、日期、身份证号等关键字段增加正则校验和人工复核。
- 记录模型版本、提示词、输入图片哈希，便于结果审计。

## 6. 与 RAG 知识库集成

多模态文档助手提取的文本可写入 `rag_kb/data/`，然后运行 `rag_kb/scripts/ingest.py` 构建索引，实现完整流水线：

```
扫描 PDF → OCR 文字 → 结构化 JSON → 向量索引 → RAG 问答
```
