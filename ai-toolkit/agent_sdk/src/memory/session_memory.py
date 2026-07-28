from typing import List, Dict, Any, Optional


class SessionMemory:
    """单会话短期记忆。"""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._history: List[Dict[str, Any]] = []

    def add(self, role: str, content: str, metadata: Dict[str, Any] = None):
        self._history.append({"role": role, "content": content, "metadata": metadata or {}})
        if len(self._history) > self.max_turns:
            self._history = self._history[-self.max_turns :]

    def get_context(self) -> List[Dict[str, Any]]:
        return [{"role": h["role"], "content": h["content"]} for h in self._history]

    def clear(self):
        self._history.clear()


class InMemorySessionStore:
    """内存中的会话存储，支持多用户/多会话。"""

    def __init__(self, max_turns: int = 20):
        self._sessions: Dict[str, SessionMemory] = {}
        self.max_turns = max_turns

    def get(self, session_id: str) -> SessionMemory:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionMemory(max_turns=self.max_turns)
        return self._sessions[session_id]

    def delete(self, session_id: str):
        self._sessions.pop(session_id, None)

    def list_sessions(self) -> List[str]:
        return list(self._sessions.keys())
