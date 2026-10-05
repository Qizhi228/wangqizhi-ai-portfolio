# 王启智 AI 应用作品集

这是一个面向 FDE（前沿部署 / 业务落地工程师）和 AI 应用开发岗位的学习型作品集，包含三个可运行原型：

1. `rag-knowledge-base`：企业知识库 RAG 问答
2. `text2sql-assistant`：自然语言转 SQL 数据分析助手
3. `codepilot-lite`：Claude Code 风格的终端 AI 编程代理

项目全部使用自造示例数据，不包含实习公司代码、文档或内部信息。默认提供 Mock 模式，不配置模型 API Key 也可以运行和学习。

## 快速开始

### RAG 知识库

```bash
cd rag-knowledge-base
python3 app.py
```

### Text-to-SQL

```bash
cd text2sql-assistant
python3 app.py
```

### CodePilot Lite

```bash
cd codepilot-lite
python3 devagent.py "列出项目文件"
python3 devagent.py "运行测试"
```

### 作品集网站

```bash
cd portfolio-site
npm install
npm run dev
```

## 文档

- [学习文档 Markdown](docs/LEARNING_GUIDE.md)
- [系统架构说明](docs/ARCHITECTURE.md)
- [腾讯云轻量服务器部署说明](docs/TENCENT_CLOUD_DEPLOYMENT.md)

## 项目边界

这些项目是用于学习和求职展示的原型，不是生产系统。重点展示：

- 如何把模型能力接入业务流程
- 如何设计工具和工作流
- 如何增加安全边界、测试和错误处理
- 如何把技术方案讲给业务人员听

## 许可证

MIT
