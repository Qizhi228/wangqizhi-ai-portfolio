# CodePilot Lite

CodePilot Lite 是一个 Claude Code 风格的终端 AI 编程代理学习原型，重点学习：

- 项目文件读取
- 文本搜索
- 安全命令执行
- 代码修改前的 Patch 思维
- 用户确认和工作区边界
- 测试驱动的 Agent 闭环

它不是 Claude Code 的复制品，也不包含任何第三方产品源码。

## 运行

```bash
python3 devagent.py "列出项目文件"
python3 devagent.py "读取 sample_project/calculator.py"
python3 devagent.py "搜索 TODO"
python3 devagent.py "运行测试"
```

进入交互模式：

```bash
python3 devagent.py
```

默认只允许访问 `codepilot-lite` 目录，并且只执行白名单命令。真实模型接入暂时保留为下一阶段扩展点，先把工具、权限和验证机制学明白。
