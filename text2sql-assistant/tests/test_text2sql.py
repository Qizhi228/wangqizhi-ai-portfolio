import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from app import SafeSQLValidator, TextToSQLService


class TextToSQLTests(unittest.TestCase):
    def test_department_query(self):
        result = TextToSQLService().ask("查询每个部门有多少员工")
        self.assertIn("GROUP BY department", result.sql)
        self.assertGreater(len(result.rows), 0)

    def test_region_query(self):
        result = TextToSQLService().ask("查询华东区域的销售记录")
        self.assertIn("华东", result.sql)
        self.assertTrue(all(row[1] == "华东" for row in result.rows))

    def test_dangerous_sql_is_blocked(self):
        with self.assertRaises(ValueError):
            SafeSQLValidator().validate("DELETE FROM sales")

    def test_limit_is_added(self):
        self.assertIn("LIMIT 50", SafeSQLValidator().validate("SELECT * FROM sales"))


if __name__ == "__main__":
    unittest.main()
