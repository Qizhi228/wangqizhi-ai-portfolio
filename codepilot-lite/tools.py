"""CodePilot Lite 的最小工具集合。"""

from __future__ import annotations

from pathlib import Path

from policy import SafeCommandRunner, WorkspacePolicy


class WorkspaceTools:
    def __init__(self, root: Path):
        self.policy = WorkspacePolicy(root)
        self.runner = SafeCommandRunner(self.policy)

    def list_files(self) -> list[str]:
        files = []
        for path in sorted(self.policy.root.rglob("*")):
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
                files.append(str(path.relative_to(self.policy.root)))
        return files

    def read_file(self, relative_path: str) -> str:
        path = self.policy.safe_path(relative_path)
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        if path.stat().st_size > 200_000:
            raise ValueError("文件超过单次读取大小限制")
        return path.read_text(encoding="utf-8")

    def search_text(self, keyword: str) -> list[str]:
        matches = []
        for relative in self.list_files():
            try:
                content = self.read_file(relative)
            except (UnicodeDecodeError, ValueError):
                continue
            for line_number, line in enumerate(content.splitlines(), start=1):
                if keyword.lower() in line.lower():
                    matches.append(f"{relative}:{line_number}: {line.strip()}")
        return matches

    def apply_replace(self, relative_path: str, old: str, new: str) -> str:
        path = self.policy.safe_path(relative_path)
        original = self.read_file(relative_path)
        if old not in original:
            raise ValueError("未找到要替换的原文，拒绝盲目覆盖文件")
        updated = original.replace(old, new, 1)
        diff = "\n".join(
            __import__("difflib").unified_diff(
                original.splitlines(), updated.splitlines(),
                fromfile=relative_path, tofile=relative_path
            )
        )
        return f"预览 Patch（尚未写入）：\n{diff}"

    def run_tests(self) -> str:
        return self.runner.run("python3 -m unittest discover -s . -p 'test_*.py'")
