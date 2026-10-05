# Text-to-SQL 数据分析助手

这是一个使用 SQLite 示例数据库的自然语言查询原型。它展示：

```text
自然语言问题 -> Schema 获取 -> SQL 生成 -> SQL 安全校验 -> 数据库执行 -> 结果解释
```

默认使用规则生成器，保证不配置 API Key 也能运行。之后可以替换为大模型生成器，但 SQL 仍然必须经过只读校验。

## 运行

```bash
python3 app.py
```

示例问题：

```text
查询销售额最高的商品
查询每个部门有多少员工
查询华东区域的销售记录
```

## 安全规则

- 只允许 `SELECT` 查询
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`
- 自动添加或限制 `LIMIT`
- 使用 SQLite 内存数据库，避免误操作真实数据
