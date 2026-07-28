# Multimodal Document Assistant

> Tech Stack: Qwen2.5-VL (cloud/local) + GPT-4.1 Vision + PDF processing + structured output

## 1. Goal

Build a production-ready multimodal document understanding pipeline:

- Extract text, tables, invoices, receipts, and ID cards from images and scanned PDFs
- Support both cloud APIs (DashScope / OpenAI) and local vision models (Qwen2.5-VL)
- Provide task-specific prompt templates and structured JSON output
- Enable end-to-end flow: scanned document → structured data → RAG knowledge base

## 2. Project Structure

```
multimodal_doc/
├── data/
│   ├── images/
│   └── pdfs/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── openai_vision.py
│   │   └── qwen_vl.py
│   ├── processors/
│   │   ├── image_loader.py
│   │   ├── pdf_loader.py
│   │   └── ocr_prompts.py
│   └── assistants/
│       └── doc_assistant.py
├── scripts/
│   ├── extract_text.py
│   ├── analyze_table.py
│   ├── extract_invoice.py
│   ├── extract_receipt.py
│   ├── extract_id_card.py
│   └── describe_image.py
├── tests/
│   └── test_processors.py
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Quick Start

### 3.1 Install

```bash
cd ai-toolkit/multimodal_doc
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Configure

Copy `.env.example` to `.env`:

```env
# DashScope Qwen2.5-VL
VISION_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen2.5-vl-72b-instruct

# Or OpenAI GPT-4.1 Vision
# VISION_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxx
# OPENAI_BASE_URL=https://api.openai.com/v1
# VISION_MODEL=gpt-4.1-mini

# Or local Qwen2.5-VL
# USE_LOCAL_VL=true
# LOCAL_VL_MODEL=Qwen/Qwen2.5-VL-7B-Instruct
```

### 3.3 Run Examples

```bash
python scripts/extract_text.py --image data/images/invoice.png
python scripts/analyze_table.py --image data/images/table.png --output table.json
python scripts/extract_invoice.py --image data/images/invoice.png --output invoice.json
python scripts/extract_text.py --pdf data/pdfs/report.pdf --page 0 --output page1.txt
```

## 4. Key Design

- **Provider abstraction**: `VisionProviderFactory` switches between cloud and local models.
- **PDF pipeline**: PDFs are rasterized to images page-by-page.
- **Prompt templates**: Centralized for OCR, table, invoice, receipt, ID card, and description tasks.
- **Structured output**: Invoice/table/receipt tasks request JSON with parse fallback.
- **Image preprocessing**: Resize large images to respect model token limits.

## 5. Production Notes

- Local Qwen2.5-VL 7B needs ~16GB VRAM, 14B needs ~28GB VRAM.
- Add image enhancement (denoise, deskew, binarize) for scanned PDFs.
- Use local models for sensitive documents.
- Validate critical fields (amounts, dates, ID numbers) and add human review.
- Log model version, prompts, and image hashes for auditability.

## 6. RAG Integration

Extracted text can be written to `rag_kb/data/` and indexed with `rag_kb/scripts/ingest.py`:

```
scanned PDF → OCR text → structured JSON → vector index → RAG QA
```
