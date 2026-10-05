"""CodePilot Lite CLI 入口。"""

from __future__ import annotations

import argparse
from pathlib import Path

from agent import MockAgent


ROOT = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description="CodePilot Lite - 终端 AI 编程代理原型")
    parser.add_argument("instruction", nargs="?", help="自然语言指令")
    args = parser.parse_args()
    agent = MockAgent(ROOT)
    if args.instruction:
        print(agent.handle(args.instruction))
        return
    print("CodePilot Lite 已启动，输入 exit 退出。")
    while True:
        instruction = input("\n你> ").strip()
        if instruction.lower() in {"exit", "quit", "退出"}:
            break
        try:
            print(agent.handle(instruction))
        except Exception as error:  # CLI 要把错误变成可读反馈
            print(f"工具执行失败：{error}")


if __name__ == "__main__":
    main()
