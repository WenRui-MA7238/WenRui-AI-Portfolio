"""
命令行交互式 Agent。
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import SmartAgent
from src.memory import SessionMemory


async def main():
    memory = SessionMemory()
    agent = SmartAgent(memory=memory)
    print("=== 智能 Agent 已启动（输入 exit 退出）===")

    while True:
        try:
            user_input = input("\n用户：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见。")
            break
        if user_input.lower() in ("exit", "quit", "退出"):
            break
        if not user_input:
            continue

        try:
            result = await agent.run(user_input)
            print(f"\nAgent：{result['answer']}")
        except Exception as e:
            print(f"\n出错了：{e}")


if __name__ == "__main__":
    asyncio.run(main())
