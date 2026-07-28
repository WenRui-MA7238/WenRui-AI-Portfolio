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
│   ├── images/              # Test images
│   └── pdfs/                # Test PDFs
├── src/
│   ├── __init__.py
│   ├── config.py            # Vision provider configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── openai_vision.py  # GPT-4.1 Vision wrapper
│   │   └── qwen_vl.py        # Local Qwen2.5-VL wrapper
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── image_loader.py   # Image preprocessing
│   │   ├── pdf_loader.py     # PDF to image conversion
│   │   └── ocr_prompts.py    # Task-specific prompt templates
│   └── assistants/
│       ├── __init__.py
│       └── doc_assistant.py  # Multimodal document assistant main class
├── scripts/
│   ├── extract_text.py       # Image/PDF text extraction
│   ├── analyze_table.py      # Table extraction to JSON
│   ├── extract_invoice.py    # Invoice key-field extraction
│   ├── extract_receipt.py    # Receipt/ticket extraction
│   ├── extract_id_card.py    # ID card extraction
│   └── describe_image.py     # Image description
├── tests/
│   └── test_processors.py    # Unit tests for processors
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
# Option A: DashScope Qwen2.5-VL
VISION_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen2.5-vl-72b-instruct

# Option B: OpenAI GPT-4.1 Vision
# VISION_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxx
# OPENAI_BASE_URL=https://api.openai.com/v1
# VISION_MODEL=gpt-4.1-mini

# Option C: Local Qwen2.5-VL (requires ~16GB VRAM for 7B)
# USE_LOCAL_VL=true
# LOCAL_VL_MODEL=Qwen/Qwen2.5-VL-7B-Instruct
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

Extract invoice fields:

```bash
python scripts/extract_invoice.py --image data/images/invoice.png --output invoice.json
```

Process a PDF:

```bash
python scripts/extract_text.py --pdf data/pdfs/report.pdf --page 0 --output page1.txt
```

## 4. Key Design

- **Provider abstraction**: `VisionProviderFactory` switches between cloud and local models without changing business logic.
- **PDF pipeline**: PDFs are rasterized to images page-by-page, then processed by the vision model.
- **Prompt templates**: Centralized in `src/processors/ocr_prompts.py` for OCR, table, invoice, receipt, ID card, and description tasks.
- **Structured output**: Invoice/table/receipt tasks request JSON; the assistant handles parse fallback.
- **Image preprocessing**: Resize large images to stay within model context/token limits.

## 5. Production Notes

- Local Qwen2.5-VL 7B requires ~16GB VRAM, 14B requires ~28GB VRAM.
- For scanned PDFs, add image enhancement (denoising, deskewing, binarization) to improve OCR accuracy.
- Use local models for sensitive documents to avoid uploading to the cloud.
- Add regex validation and human review for critical fields (amounts, dates, ID numbers).
- Log model version, prompts, and input image hashes for result auditability.

## 6. Integration with RAG Knowledge Base

Text extracted by the multimodal document assistant can be written to `rag_kb/data/`, then run `rag_kb/scripts/ingest.py` to build an index, enabling a complete pipeline:

```
scanned PDF → OCR text → structured JSON → vector index → RAG QA
```
