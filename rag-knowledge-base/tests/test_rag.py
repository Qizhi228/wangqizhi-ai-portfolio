import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from app import KnowledgeBase, split_document, tokenize


class RagTests(unittest.TestCase):
    def test_tokenize_keeps_chinese_and_words(self):
        tokens = tokenize("RAG 知识库 2026")
        self.assertIn("rag", tokens)
        self.assertIn("知", tokens)
        self.assertIn("2026", tokens)

    def test_split_document(self):
        chunks = split_document("demo.md", "第一段\n\n第二段", chunk_size=4)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].source, "demo.md")

    def test_answer_has_source(self):
        result = KnowledgeBase().ask("员工申请年假需要提前多久？")
        self.assertIn("提前", result["answer"])
        self.assertTrue(result["sources"])


if __name__ == "__main__":
    unittest.main()
