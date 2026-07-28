import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import SmartAgent


async def main():
    agent = SmartAgent()
    print("=== 智能 Agent 已启动（输入 exit 退出）===")
    context = []
    while True:
        user_input = input("\n用户：").strip()
        if user_input.lower() in ("exit", "quit", "退出"):
            break
        try:
            result = await agent.run(user_input, context)
            print(f"\nAgent：{result['answer']}")
            # 简单上下文维护
            context.append({"role": "user", "content": user_input})
            context.append({"role": "assistant", "content": result["answer"]})
            if len(context) > 20:
                context = context[-20:]
        except Exception as e:
            print(f"\n出错了：{e}")


if __name__ == "__main__":
    asyncio.run(main())
