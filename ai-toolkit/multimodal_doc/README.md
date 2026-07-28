# 多模态文档助手

> 技术栈：Qwen2.5-VL（本地/OSS）或 GPT-4.1 Vision（OpenAI API）

## 1. 目标
- 支持图片、扫描 PDF、表格截图的多模态理解
- 提取结构化信息（文本、表格、图表、印章等）
- 提供可运行的 CLI 和 API 接口

## 2. 项目结构

```
multimodal_doc/
├── data/
│   ├── images/              # 测试图片
│   └── pdfs/                # 测试 PDF
├── src/
│   ├── __init__.py
│   ├── config.py            # 配置
│   ├── models/
│   │   ├── __init__.py
│   │   ├── qwen_vl.py      # Qwen2.5-VL 本地/远程封装
│   │   └── openai_vision.py # GPT-4.1 Vision 封装
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── image_loader.py  # 图片预处理
│   │   ├── pdf_loader.py    # PDF 转图片
│   │   └── ocr_prompts.py   # 结构化提示词
│   ├── assistants/
│   │   ├── __init__.py
│   │   └── doc_assistant.py # 多模态文档助手主类
│   └── utils.py
├── scripts/
│   ├── extract_text.py      # 图片/PDF 文字提取
│   ├── analyze_table.py     # 表格分析
│   └── describe_image.py    # 图片描述
├── tests/
│   └── test_qwen_vl.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. 快速开始

### 3.1 安装依赖

```bash
cd ai-toolkit/multimodal_doc
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 配置

复制 `.env.example` 为 `.env`：

```env
# 方案 A：阿里云 DashScope / 百炼 Qwen2.5-VL
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen2.5-vl-72b-instruct

# 方案 B：本地 Qwen2.5-VL（ transformers + torch ）
# LOCAL_VL_MODEL=Qwen/Qwen2.5-VL-7B-Instruct
# USE_LOCAL_VL=true

# 方案 C：OpenAI GPT-4.1 Vision
# VISION_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxx
# VISION_MODEL=gpt-4.1-mini
```

### 3.3 运行示例

提取图片中的文字：

```bash
python scripts/extract_text.py --image data/images/invoice.png
```

分析表格：

```bash
python scripts/analyze_table.py --image data/images/table.png --output table.json
```

## 4. 关键设计

- **输入统一**：PDF 先转图片，再统一输入视觉模型
- **提示词模板**：按任务类型预设 OCR / 表格 / 图表 / 票据 / 合同等 prompt
- **结构化输出**：要求模型输出 JSON/Markdown，便于下游解析
- **本地 vs 云端**：小模型本地跑（7B/14B），大模型云端调用（72B），按精度需求路由

## 5. 生产注意事项

- 本地 Qwen2.5-VL 7B 需要 ~16GB 显存，14B 需要 ~28GB 显存
- 扫描 PDF 先做图像增强（去噪、纠偏、二值化）可显著提升 OCR 准确率
- 敏感文档优先使用本地模型，避免上传云端
- 对关键字段（金额、日期、身份证号）增加正则校验和人工复核
- 记录模型版本、提示词、输入图片 hash，确保结果可审计

## 6. 与 RAG 知识库联动

多模态文档助手提取的文本可以写入 `rag_kb/data/`，再运行 `rag_kb/scripts/ingest.py` 构建索引，实现"扫描件 → 结构化文本 → 语义检索"的完整链路。
