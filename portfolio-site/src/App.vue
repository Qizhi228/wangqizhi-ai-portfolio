<script setup>
const projects = [
  {
    tag: 'RAG / 知识库',
    title: '企业知识库问答原型',
    summary: '用文档切分、混合检索和来源引用，把企业资料转成可查询的知识服务。',
    stack: 'Python · FastAPI · 向量检索 · LLM API',
    status: '可运行原型',
    path: 'https://github.com/Qizhi228/wangqizhi-ai-portfolio/tree/main/rag-knowledge-base',
  },
  {
    tag: 'Text-to-SQL',
    title: '自然语言数据分析助手',
    summary: '从业务问题出发生成只读 SQL，经过安全校验后查询示例数据库并返回结果。',
    stack: 'Python · SQLite · SQL 校验 · Schema 增强',
    status: '可运行原型',
    path: 'https://github.com/Qizhi228/wangqizhi-ai-portfolio/tree/main/text2sql-assistant',
  },
  {
    tag: 'Agent / 工程代理',
    title: 'CodePilot Lite',
    summary: '终端式 AI 编程代理原型，包含文件读取、文本搜索、安全命令和测试闭环。',
    stack: 'Python · CLI · Tool Registry · Policy',
    status: '学习型原型',
    path: 'https://github.com/Qizhi228/wangqizhi-ai-portfolio/tree/main/codepilot-lite',
  },
]

const notes = [
  'RAG：为什么检索结果需要来源和拒答边界？',
  'Text-to-SQL：为什么 SQL 生成后仍必须做安全校验？',
  'Agent：工具、权限和测试闭环如何组成可交付产品？',
]
</script>

<template>
  <main>
    <nav class="nav shell">
      <a class="brand" href="#top">王启智<span> / AI Application</span></a>
      <div class="nav-links">
        <a href="#projects">项目</a>
        <a href="#notes">技术笔记</a>
        <a href="#about">关于我</a>
      </div>
    </nav>

    <section id="top" class="hero shell">
      <div class="hero-copy">
        <p class="eyebrow">AI 应用落地 · FDE · 大模型应用开发</p>
        <h1>把前沿 AI 能力<br /><em>变成可运行的业务原型。</em></h1>
        <p class="intro">我是王启智，软件工程本科毕业生。关注 RAG、Text-to-SQL、Agent 工作流，以及模型能力如何进入真实业务流程。</p>
        <div class="actions">
          <a class="button primary" href="#projects">查看作品</a>
          <a class="button ghost" href="https://github.com/Qizhi228/wangqizhi-ai-portfolio" target="_blank" rel="noreferrer">GitHub 仓库</a>
        </div>
      </div>
      <div class="hero-card">
        <span class="card-label">CURRENT FOCUS</span>
        <strong>从需求到交付</strong>
        <p>理解场景 → 快速验证 → 增加安全边界 → 测试效果 → 解释限制</p>
        <div class="signal"><i></i> Available for AI application roles</div>
      </div>
    </section>

    <section id="projects" class="section shell">
      <div class="section-heading">
        <p class="eyebrow">SELECTED WORK</p>
        <h2>三个小而完整的系统</h2>
        <p>不追求堆砌框架，重点展示我如何把一个 AI 想法拆成工具、流程、验证和边界。</p>
      </div>
      <div class="project-grid">
        <article v-for="project in projects" :key="project.title" class="project-card">
          <div class="project-top"><span class="tag">{{ project.tag }}</span><span class="status">{{ project.status }}</span></div>
          <h3>{{ project.title }}</h3>
          <p>{{ project.summary }}</p>
          <div class="stack">{{ project.stack }}</div>
          <a class="text-link" :href="project.path">查看项目说明 <span>↗</span></a>
        </article>
      </div>
    </section>

    <section id="notes" class="section shell split-section">
      <div class="section-heading">
        <p class="eyebrow">AI RADAR</p>
        <h2>关注新技术，更关注它能否落地。</h2>
        <p>我会把每次技术学习写成四个问题：解决什么问题、如何复现、适合什么业务、有什么限制。</p>
      </div>
      <div class="notes-list">
        <div v-for="(note, index) in notes" :key="note" class="note-item"><span>0{{ index + 1 }}</span>{{ note }}<b>↗</b></div>
      </div>
    </section>

    <section id="about" class="section shell about">
      <div>
        <p class="eyebrow">ABOUT</p>
        <h2>我想做的是<br /><em>能被业务使用的 AI。</em></h2>
      </div>
      <div class="about-copy">
        <p>我有企业级大模型应用实习经历，参与过 RAG 知识库问答和 Text-to-SQL 数据分析助手。现在重点补强 Python 工程、Agent 工具调用、部署调试和技术表达。</p>
        <div class="facts"><span>大连 / 沈阳优先</span><span>杭州可考虑</span><span>2026 届软件工程</span><span>可立即到岗：待确认</span></div>
      </div>
    </section>

    <footer class="footer shell">
      <span>王启智 · AI Application / FDE</span>
      <span>Built with Vue 3 + Vite</span>
    </footer>
  </main>
</template>
