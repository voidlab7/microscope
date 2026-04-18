# MicroScope — 市场调研分析 Agent 🔬

> 把模糊的文件放大成清晰的市场图景

## 简介

MicroScope 是一个市场调研分析 Agent，能够：

- 📥 **多格式输入**：PDF / Excel / 图片 / Word / 网页
- 🔍 **网络补全**：结合公开数据验证和补全企业信息
- 🧠 **结构化分析**：企业图谱 / 竞争格局 / 产业链 / 投资热度
- 📤 **多格式输出**：Markdown / Excel / HTML 报告

## 目录结构

```
MicroScope/
├── agent/                → 🧠 Agent 核心定义
│   └── AGENT.md          → 人设 + 铁律 + 工作流
├── skills/               → ⚡ 8 个独立技能
│   ├── pdf-extract.md    → PDF 解析
│   ├── xlsx-extract.md   → Excel 解析
│   ├── image-ocr.md      → 图片 OCR
│   ├── web-research.md   → 网络调研
│   ├── enterprise-lookup.md → 企业查询
│   ├── market-analysis.md   → 市场分析
│   ├── data-validation.md   → 数据验证
│   └── report-generate.md   → 报告生成
├── prompts/              → 📝 提示词模板
│   ├── analysis-frameworks.md → 分析框架
│   ├── enterprise-lookup.md   → 企业查询策略
│   └── data-labeling.md       → 数据标注规范
├── templates/            → 📄 输出模板
│   ├── report-markdown.md         → Markdown 报告骨架
│   └── enterprise-table-schema.md → Excel 字段定义
├── memory/               → 🧠 跨会话记忆
│   └── lessons.md        → 经验教训积累
├── adapters/             → 🔌 平台适配层
│   ├── codebuddy/        → CodeBuddy 安装说明
│   ├── openclaw/         → OpenClaw 安装说明
│   ├── dotagents/        → .agents Protocol 安装说明
│   └── oaf/              → OAF 安装说明
├── tools/                → 🔧 工具脚本（Phase 2）
├── examples/             → 📁 示例
│   └── ai-glasses/       → AI 眼镜行业调研案例
│       ├── input/        → 原始文件（PDF/Excel/图片）
│       └── output/       → 产出报告（MD/HTML/Excel）
├── docs/                 → 📚 设计文档
│   ├── MicroScope-Agent设计文档.md
│   └── 通用Agent结构说明.md
└── README.md             → 本文件
```

## 安装

### CodeBuddy
```bash
cp MicroScope/agent/AGENT.md .codebuddy/skills/microscope/SKILL.md
cp MicroScope/prompts/*.md .codebuddy/skills/microscope/references/
cp MicroScope/templates/*.md .codebuddy/skills/microscope/assets/
```

### OpenClaw
```bash
cat MicroScope/agent/AGENT.md >> SOUL.md
```

### .agents Protocol
```bash
cp MicroScope/agent/AGENT.md .agents/agents/microscope/agent.md
cp MicroScope/skills/*.md .agents/skills/
```

详细说明见 `adapters/` 各目录。

## 使用

```
@MicroScope 帮我分析 AI 眼镜市场
+ 附件：PDF、Excel、图片
```

## 许可

MIT

## GitHub

https://github.com/voidlab7/microscope
