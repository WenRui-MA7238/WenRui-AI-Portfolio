# Hi, I'm Wenrui Ma 👋

Generative AI Engineer | Machine Learning Engineer | Computer Vision Engineer

🎓 MSc Artificial Intelligence @ UKM  
🎓 BSc Artificial Intelligence @ APU

## Interests

- Generative AI
- Large Language Models (LLMs)
- AI Agents
- Computer Vision
- Multimodal AI
- Reinforcement Learning

## Tech Stack

Python • PyTorch • TensorFlow • OpenCV • Hugging Face • LangChain • Git • Linux

Currently building AI applications for Generative AI, RAG, and Computer Vision.

---

## Featured Project: AI Toolkit

This repository contains a runnable AI engineering toolkit with three integrated components:

| Component | Directory | Capability |
|-----------|-----------|------------|
| RAG Knowledge Base | [`ai-toolkit/rag_kb/`](./ai-toolkit/rag_kb/) | Document ingestion + FAISS semantic search + Qwen3 generation |
| AI Agent | [`ai-toolkit/agent_sdk/`](./ai-toolkit/agent_sdk/) | ReAct agent with tool calling (calculator / knowledge base / weather demo) |
| Multimodal Document Assistant | [`ai-toolkit/multimodal_doc/`](./ai-toolkit/multimodal_doc/) | OCR + table extraction + invoice parsing from images and PDFs |

### Quick Start

```bash
git clone https://github.com/WenRui-MA7238/WenRui-AI-Proftolio.git
cd WenRui-AI-Proftolio/ai-toolkit
cp .env.example .env
# Edit .env with your API keys, then install dependencies per component README
```

- [中文使用说明](./ai-toolkit/README_CN.md)
- [English Guide](./ai-toolkit/README_EN.md)

### Integrated Workflow

```text
Image/PDF → Multimodal extraction → RAG data/ → FAISS index → Agent Q&A
```

This project demonstrates end-to-end AI application engineering: retrieval augmentation, agent tool use, and multimodal understanding.
