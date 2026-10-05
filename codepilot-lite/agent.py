"""CodePilot Lite 的规则 Agent。

先使用透明的规则路由，方便学习工具调用；之后可把 route() 替换成模型规划器。
"""

from __future__ import annotations

from pathlib import Path

from tools import WorkspaceTools


class MockAgent:
    def __init__(self, root: Path):
        self.tools = WorkspaceTools(root)

    def handle(self, instruction: str) -> str:
        text = instruction.strip()
        if any(word in text for word in ["列出", "文件树", "有哪些文件"]):
            return "\n".join(self.tools.list_files())
        if text.startswith("读取") or text.startswith("read "):
            relative = text.replace("读取", "", 1).replace("read ", "", 1).strip()
            return self.tools.read_file(relative)
        if text.startswith("搜索") or text.startswith("search "):
            keyword = text.replace("搜索", "", 1).replace("search ", "", 1).strip()
            return "\n".join(self.tools.search_text(keyword)) or "没有找到匹配内容"
        if "运行测试" in text or "run tests" in text.lower():
            return self.tools.run_tests()
        if "修改" in text or "改代码" in text:
            return "我可以生成 Patch，但在写入文件前需要用户确认。请提供文件路径、原文和新文。"
        if any(word in text.lower() for word in ["rm -rf", "sudo", "删除全部"]):
            return "已拒绝：危险命令不在允许范围内。"
        return "当前 Mock Agent 支持：列出文件、读取文件、搜索文本、运行测试和安全边界演示。"
