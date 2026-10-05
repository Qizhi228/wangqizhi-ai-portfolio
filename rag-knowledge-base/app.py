"""企业知识库 RAG 学习原型。

默认使用本地 Mock 模式，便于没有 API Key 时运行；配置 MODEL_MODE=api
后，可调用 OpenAI 兼容的 Chat Completions 接口。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).parent
DOCS_DIR = ROOT / "data" / "sample_docs"


@dataclass
class Chunk:
    source: str
    index: int
    text: str
    tokens: tuple[str, ...]


def tokenize(text: str) -> tuple[str, ...]:
    """同时保留中文单字和英文/数字词，保持示例实现透明。"""
    chinese = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[A-Za-z0-9_]+", text.lower())
    return tuple(chinese + words)


def hashed_embedding(tokens: Iterable[str], dimension: int = 128) -> list[float]:
    vector = [0.0] * dimension
    for token in tokens:
        bucket = hash(token) % dimension
        vector[bucket] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def split_document(source: str, text: str, chunk_size: int = 180) -> list[Chunk]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[Chunk] = []
    buffer = ""
    index = 0
    for paragraph in paragraphs:
        candidate = f"{buffer}\n{paragraph}".strip()
        if buffer and len(candidate) > chunk_size:
            tokens = tokenize(buffer)
            chunks.append(Chunk(source, index, buffer, tokens))
            index += 1
            buffer = paragraph
        else:
            buffer = candidate
    if buffer:
        chunks.append(Chunk(source, index, buffer, tokenize(buffer)))
    return chunks


class HybridRetriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.vectors = [hashed_embedding(chunk.tokens) for chunk in chunks]

    def search(self, question: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        query_tokens = tokenize(question)
        query_set = set(query_tokens)
        query_vector = hashed_embedding(query_tokens)
        scored: list[tuple[Chunk, float]] = []
        for chunk, vector in zip(self.chunks, self.vectors):
            overlap = len(query_set.intersection(chunk.tokens))
            lexical = overlap / max(len(query_set), 1)
            semantic = cosine(query_vector, vector)
            score = 0.65 * lexical + 0.35 * semantic
            scored.append((chunk, score))
        return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


class MockLLM:
    def answer(self, question: str, contexts: list[tuple[Chunk, float]]) -> str:
        if not contexts or contexts[0][1] <= 0:
            return "资料中没有找到足够依据，我无法确认这个问题。"
        lines = [f"根据检索到的资料，关于“{question}”可以参考："]
        for chunk, score in contexts:
            lines.append(f"- {chunk.text.replace(chr(10), ' ')}（相关度 {score:.2f}）")
        lines.append("以上回答仅基于示例知识库内容，具体执行仍需以正式制度为准。")
        return "\n".join(lines)


class OpenAICompatibleLLM:
    def __init__(self) -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "")

    def answer(self, question: str, contexts: list[tuple[Chunk, float]]) -> str:
        context_text = "\n\n".join(chunk.text for chunk, _ in contexts)
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": "只根据给定资料回答；资料不足时明确说不知道。"},
                {"role": "user", "content": f"资料：\n{context_text}\n\n问题：{question}"},
            ],
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]


class KnowledgeBase:
    def __init__(self, docs_dir: Path = DOCS_DIR):
        chunks: list[Chunk] = []
        for path in sorted(docs_dir.glob("*.md")):
            chunks.extend(split_document(path.name, path.read_text(encoding="utf-8")))
        self.retriever = HybridRetriever(chunks)
        mode = os.getenv("MODEL_MODE", "mock").lower()
        self.llm = OpenAICompatibleLLM() if mode == "api" else MockLLM()

    def ask(self, question: str, top_k: int = 3) -> dict:
        contexts = self.retriever.search(question, top_k=top_k)
        answer = self.llm.answer(question, contexts)
        return {
            "question": question,
            "answer": answer,
            "sources": [{"file": c.source, "chunk": c.index, "score": round(s, 3)} for c, s in contexts],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG 知识库问答原型")
    parser.add_argument("--question", help="直接提问；不传则进入交互模式")
    args = parser.parse_args()
    kb = KnowledgeBase()
    if args.question:
        print(json.dumps(kb.ask(args.question), ensure_ascii=False, indent=2))
        return
    print("RAG 知识库已启动，输入 exit 退出。")
    while True:
        question = input("\n问题> ").strip()
        if question.lower() in {"exit", "quit", "退出"}:
            break
        if question:
            print(kb.ask(question)["answer"])


if __name__ == "__main__":
    main()
