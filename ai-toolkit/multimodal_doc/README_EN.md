# Multimodal Document Assistant

> Tech Stack: Qwen2.5-VL (local/OSS) or GPT-4.1 Vision (OpenAI API)

## 1. Goal
- Support multimodal understanding of images, scanned PDFs, and table screenshots
- Extract structured information (text, tables, charts, seals, etc.)
- Provide runnable CLI and API interfaces

## 2. Project Structure

```
multimodal_doc/
├── data/
│   ├── images/              # Test images
│   └── pdfs/                # Test PDFs
├── src/
│   ├── __init__.py
│   ├── config.py            # Configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── qwen_vl.py      # Qwen2.5-VL local/remote wrapper
│   │   └── openai_vision.py # GPT-4.1 Vision wrapper
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── image_loader.py  # Image preprocessing
│   │   ├── pdf_loader.py    # PDF to image conversion
│   │   └── ocr_prompts.py   # Structured prompt templates
│   ├── assistants/
│   │   ├── __init__.py
│   │   └── doc_assistant.py # Multimodal document assistant main class
│   └── utils.py
├── scripts/
│   ├── extract_text.py      # Image/PDF text extraction
│   ├── analyze_table.py     # Table analysis
│   └── describe_image.py    # Image description
├── tests/
│   └── test_qwen_vl.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Quick Start

### 3.1 Install Dependencies

```bash
cd ai-toolkit/multimodal_doc
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Configure

Copy `.env.example` to `.env`:

```env
# Option A: Alibaba Cloud DashScope / Bailian Qwen2.5-VL
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen2.5-vl-72b-instruct

# Option B: Local Qwen2.5-VL (transformers + torch)
# LOCAL_VL_MODEL=Qwen/Qwen2.5-VL-7B-Instruct
# USE_LOCAL_VL=true

# Option C: OpenAI GPT-4.1 Vision
# VISION_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxx
# VISION_MODEL=gpt-4.1-mini
```

### 3.3 Run Examples

Extract text from an image:

```bash
python scripts/extract_text.py --image data/images/invoice.png
```

Analyze a table:

```bash
python scripts/analyze_table.py --image data/images/table.png --output table.json
```

## 4. Key Design

- **Unified Input**: PDFs are first converted to images, then fed into the vision model
- **Prompt Templates**: Task-specific prompts for OCR / table / chart / invoice / contract tasks
- **Structured Output**: Ask the model to output JSON/Markdown for downstream parsing
- **Local vs Cloud**: Small models run locally (7B/14B), large models are called from cloud (72B), routed by accuracy requirements

## 5. Production Notes

- Local Qwen2.5-VL 7B requires ~16GB VRAM, 14B requires ~28GB VRAM
- For scanned PDFs, image enhancement (denoising, deskewing, binarization) can significantly improve OCR accuracy
- Use local models for sensitive documents to avoid uploading to the cloud
- Add regex validation and human review for critical fields (amounts, dates, ID numbers)
- Log model version, prompts, and input image hashes for result auditability

## 6. Integration with RAG Knowledge Base

Text extracted by the multimodal document assistant can be written to `rag_kb/data/`, then run `rag_kb/scripts/ingest.py` to build an index, enabling a complete pipeline: "scanned document → structured text → semantic retrieval".
