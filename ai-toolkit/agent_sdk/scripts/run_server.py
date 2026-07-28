"""
FastAPI 服务入口，提供 HTTP API 调用 Agent。
"""

import os
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from src.agent import SmartAgent
from src.llm_backend import LLMBackend
from src.memory import InMemorySessionStore

app = FastAPI(title="AI Agent Service", version="0.2.0")
store = InMemorySessionStore()


class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    provider: str = None
    model: str = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    model: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    memory = store.get(session_id)

    try:
        llm = LLMBackend(provider=req.provider, model=req.model)
        agent = SmartAgent(llm=llm, memory=memory)
        result = await agent.run(req.message)
        return ChatResponse(answer=result["answer"], session_id=session_id, model=result["model"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    store.delete(session_id)
    return {"deleted": session_id}


if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
