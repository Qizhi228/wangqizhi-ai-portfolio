import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from policy import SafeCommandRunner, WorkspacePolicy
from tools import WorkspaceTools


class CodePilotTests(unittest.TestCase):
    def test_path_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = WorkspacePolicy(Path(directory))
            with self.assertRaises(PermissionError):
                policy.safe_path("../secret.txt")

    def test_dangerous_command_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = SafeCommandRunner(WorkspacePolicy(Path(directory)))
            with self.assertRaises(PermissionError):
                runner.run("rm -rf .")

    def test_search_and_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "demo.txt").write_text("hello agent\n", encoding="utf-8")
            tools = WorkspaceTools(root)
            self.assertIn("demo.txt", tools.list_files())
            self.assertIn("hello", tools.read_file("demo.txt"))
            self.assertTrue(tools.search_text("agent"))


if __name__ == "__main__":
    unittest.main()
