# 企业知识库 RAG 原型

这是一个不依赖外部向量数据库即可运行的 RAG 学习原型。它使用自造企业制度文档，通过词项匹配和确定性哈希向量完成混合检索，默认使用 Mock LLM 生成带来源的回答。

## 运行

```bash
python3 app.py
```

然后输入问题，例如：

```text
员工申请年假需要提前多久？
信息安全事件应该如何上报？
```

## 可选模型模式

```bash
export MODEL_MODE=api
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_API_KEY=你的Key
export OPENAI_MODEL=你的模型名
python3 app.py
```

项目不会读取或上传任何实习公司资料。
