"""CodePilot Lite 的工作区和命令安全策略。"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


class WorkspacePolicy:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def safe_path(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as error:
            raise PermissionError("路径超出 Agent 工作区范围") from error
        return candidate


class SafeCommandRunner:
    ALLOWED = {"python", "python3", "git"}
    BLOCKED = {"rm", "sudo", "chmod", "chown", "shutdown", "reboot", "mkfs"}

    def __init__(self, policy: WorkspacePolicy):
        self.policy = policy

    def run(self, command: str, timeout: int = 20) -> str:
        if any(symbol in command for symbol in [";", "&&", "||", "|", ">", "<", "`", "$("]):
            raise PermissionError("命令包含不允许的 shell 拼接符号")
        parts = shlex.split(command)
        if not parts:
            raise ValueError("命令不能为空")
        executable = Path(parts[0]).name
        if executable in self.BLOCKED or executable not in self.ALLOWED:
            raise PermissionError(f"命令未加入白名单：{executable}")
        if any(part in {"-c", "--command"} for part in parts):
            raise PermissionError("不允许通过解释器参数执行任意 shell 命令")
        completed = subprocess.run(
            parts,
            cwd=self.policy.root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        output = (completed.stdout + completed.stderr).strip()
        return f"exit_code={completed.returncode}\n{output}".strip()
