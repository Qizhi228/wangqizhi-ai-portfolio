"""Text-to-SQL 学习原型：规则生成、只读校验和 SQLite 执行。"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import dataclass


@dataclass
class QueryResult:
    question: str
    sql: str
    columns: list[str]
    rows: list[tuple]
    explanation: str


class DemoDatabase:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self._seed()

    def _seed(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                product TEXT NOT NULL,
                region TEXT NOT NULL,
                amount REAL NOT NULL,
                sold_at TEXT NOT NULL
            );
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                city TEXT NOT NULL
            );
            INSERT INTO sales(product, region, amount, sold_at) VALUES
                ('知识库服务', '华东', 12800, '2026-09-01'),
                ('数据分析助手', '华北', 9800, '2026-09-03'),
                ('知识库服务', '华南', 15600, '2026-09-07'),
                ('智能工单', '东北', 7600, '2026-09-08'),
                ('数据分析助手', '华东', 11200, '2026-09-11');
            INSERT INTO employees(name, department, city) VALUES
                ('林一', '研发', '大连'),
                ('周二', '研发', '沈阳'),
                ('吴三', '交付', '大连'),
                ('郑四', '销售', '杭州');
            """
        )

    def schema(self) -> str:
        return (
            "sales(id, product, region, amount, sold_at)\n"
            "employees(id, name, department, city)"
        )


class SafeSQLValidator:
    FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|replace|attach|detach|pragma|vacuum)\b", re.I)

    def validate(self, sql: str) -> str:
        clean = sql.strip().rstrip(";").strip()
        if not clean:
            raise ValueError("SQL 不能为空")
        if not re.match(r"^select\b", clean, re.I):
            raise ValueError("只允许执行 SELECT 查询")
        if self.FORBIDDEN.search(clean):
            raise ValueError("检测到危险 SQL 关键词")
        if ";" in clean:
            raise ValueError("不允许执行多条 SQL")
        if not re.search(r"\blimit\s+\d+\b", clean, re.I):
            clean = f"{clean} LIMIT 50"
        return clean


class RuleBasedSQLGenerator:
    def generate(self, question: str) -> str:
        q = question.lower()
        if "部门" in question and ("员工" in question or "人数" in question):
            return "SELECT department, COUNT(*) AS employee_count FROM employees GROUP BY department ORDER BY employee_count DESC"
        if "最高" in question or "最多" in question:
            return "SELECT product, SUM(amount) AS total_amount FROM sales GROUP BY product ORDER BY total_amount DESC"
        if "华东" in question:
            return "SELECT product, region, amount, sold_at FROM sales WHERE region = '华东' ORDER BY amount DESC"
        if "员工" in question:
            return "SELECT name, department, city FROM employees"
        if "销售" in question or "收入" in question or "金额" in question:
            return "SELECT product, region, amount, sold_at FROM sales ORDER BY sold_at DESC"
        if "sales" in q:
            return "SELECT product, region, amount, sold_at FROM sales"
        raise ValueError("当前规则生成器无法理解这个问题，请补充业务词或接入模型生成器")


class TextToSQLService:
    def __init__(self) -> None:
        self.database = DemoDatabase()
        self.generator = RuleBasedSQLGenerator()
        self.validator = SafeSQLValidator()

    def ask(self, question: str) -> QueryResult:
        raw_sql = self.generator.generate(question)
        sql = self.validator.validate(raw_sql)
        cursor = self.database.connection.execute(sql)
        rows = [tuple(row) for row in cursor.fetchall()]
        columns = [item[0] for item in cursor.description or []]
        explanation = f"系统根据问题匹配 Schema：{self.database.schema()}；生成并校验了只读查询。"
        return QueryResult(question, sql, columns, rows, explanation)


def main() -> None:
    parser = argparse.ArgumentParser(description="Text-to-SQL 数据分析助手")
    parser.add_argument("--question", help="直接提问；不传则进入交互模式")
    args = parser.parse_args()
    service = TextToSQLService()
    if args.question:
        result = service.ask(args.question)
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
        return
    print("Text-to-SQL 助手已启动，输入 exit 退出。")
    while True:
        question = input("\n问题> ").strip()
        if question.lower() in {"exit", "quit", "退出"}:
            break
        try:
            result = service.ask(question)
            print(f"SQL: {result.sql}")
            print(f"字段: {result.columns}")
            for row in result.rows:
                print(row)
            print(result.explanation)
        except ValueError as error:
            print(f"无法执行：{error}")


if __name__ == "__main__":
    main()
