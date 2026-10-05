# 三个项目的架构说明

## 1. RAG 知识库

```text
用户问题
  -> 文本切分与特征化
  -> 混合检索（词项匹配 + 哈希向量相似度）
  -> Top-K 文档片段
  -> Mock LLM 或 OpenAI 兼容 API
  -> 带来源回答
```

## 2. Text-to-SQL

```text
自然语言问题
  -> Schema 获取
  -> 规则生成器或模型生成 SQL
  -> SELECT-only 校验
  -> SQLite 执行
  -> 结果与解释返回
```

## 3. CodePilot Lite

```text
终端输入
  -> Agent Orchestrator
  -> Tool Registry
       |- list_files
       |- read_file
       |- search_text
       |- run_safe_command
       |- apply_patch
  -> Policy 权限检查
  -> 执行并返回结果
```

## FDE 视角

三个项目分别覆盖：

- 知识获取：RAG
- 业务数据查询：Text-to-SQL
- 工程协作与自动化：代码代理

它们共同展示的是“理解业务问题、快速做出原型、增加安全边界、验证效果、解释限制”的能力。
