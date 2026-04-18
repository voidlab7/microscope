# MicroScope 通用 Agent 结构说明

> 设计原则：核心层平台无关，适配层按需生成
> 参考规范：OAF、.agents Protocol、OpenClaw、CodeBuddy

---

## 设计理念

当前 AI Agent 生态没有统一标准，但正在收敛。主流平台（OpenClaw、Hermes、CodeBuddy、Claude、OAF、.agents Protocol）都收敛到 5 个核心概念：

| 概念 | 说明 | 所有平台都有 |
|------|------|------------|
| **人设（Identity）** | 你是谁，什么性格，什么边界 | ✅ |
| **技能（Skills）** | 你能做什么，触发条件是什么 | ✅ |
| **工具（Tools）** | 你用什么工具完成任务 | ✅ |
| **记忆（Memory）** | 你记住了什么，跨会话保留 | ✅（部分平台） |
| **流程（Workflow）** | 你按什么步骤工作 | ✅ |

格式也收敛到：**Markdown（人设/技能/流程）+ JSON（工具/配置）+ YAML frontmatter（元数据）**

---

## 目录结构（核心层 + 适配层）

```
MicroScope/
│
├── 📋 核心层（平台无关，所有平台共享）
│   ├── agent/
│   │   ├── AGENT.md              → 人设 + 铁律 + 工作流（核心定义文件）
│   │   └── config.json           → 模型/工具/参数配置
│   ├── skills/
│   │   ├── pdf-extract.md        → 技能：PDF 解析
│   │   ├── xlsx-extract.md       → 技能：Excel 解析
│   │   ├── image-ocr.md          → 技能：图片 OCR
│   │   ├── web-research.md       → 技能：网络信息补全
│   │   ├── enterprise-lookup.md  → 技能：企业信息查询
│   │   ├── market-analysis.md    → 技能：市场分析框架
│   │   ├── data-validation.md    → 技能：数据交叉验证
│   │   └── report-generate.md    → 技能：多格式报告生成
│   ├── prompts/
│   │   ├── analysis-frameworks.md → 分析框架（企业分层/产业链/竞争格局）
│   │   ├── enterprise-lookup.md   → 企业查询策略
│   │   └── data-labeling.md       → 数据标注规范
│   ├── templates/
│   │   ├── report-markdown.md     → Markdown 报告模板
│   │   └── enterprise-table-schema.md → Excel 字段定义
│   └── memory/
│       └── lessons.md             → 经验教训（跨会话积累）
│
├── 🔌 适配层（按平台生成，可自动转换）
│   ├── adapters/
│   │   ├── codebuddy/            → CodeBuddy 适配
│   │   │   ├── SKILL.md          → .codebuddy/skills/microscope/SKILL.md 格式
│   │   │   └── README.md         → 安装说明
│   │   ├── openclaw/             → OpenClaw 适配
│   │   │   ├── SOUL.md           → OpenClaw SOUL.md 格式
│   │   │   ├── AGENTS.md         → OpenClaw AGENTS.md 格式
│   │   │   └── README.md         → 安装说明
│   │   ├── dotagents/            → .agents Protocol 适配
│   │   │   ├── agent.md          → .agents/agents/microscope/agent.md 格式
│   │   │   ├── mcp.json          → .agents/mcp.json 格式
│   │   │   └── README.md         → 安装说明
│   │   └── oaf/                  → Open Agent Format 适配
│   │       ├── AGENTS.md          → OAF AGENTS.md 格式（frontmatter+正文）
│   │       └── README.md          → 安装说明
│
├── 🔧 工具层（可选，Phase 2+）
│   ├── tools/
│   │   └── README.md             → 工具脚本（MCP Server 等）
│
├── 📁 示例 & 文档
│   ├── examples/                 → 示例输入输出
│   ├── docs/                     → 设计文档
│   └── README.md                 → 项目介绍
│
└── 🔄 转换脚本（可选）
    └── scripts/
        └── generate-adapters.sh  → 从核心层自动生成各平台适配文件
```

---

## 各平台格式映射

### 核心层 → CodeBuddy

| 核心层文件 | → CodeBuddy 文件 | 说明 |
|-----------|-----------------|------|
| `agent/AGENT.md` | `.codebuddy/skills/microscope/SKILL.md` | frontmatter 格式略有差异 |
| `skills/*.md` | SKILL.md 内引用 | 作为子提示词 |
| `prompts/*.md` | `references/*.md` | 参考文档 |
| `templates/*.md` | `assets/*.md` | 资源文件 |

### 核心层 → OpenClaw

| 核心层文件 | → OpenClaw 文件 | 说明 |
|-----------|----------------|------|
| `agent/AGENT.md` 人设部分 | `SOUL.md` | 性格/语气/边界 |
| `agent/AGENT.md` 流程部分 | `AGENTS.md` | 操作手册 |
| `skills/*.md` | 内置 skill 系统 | OpenClaw 自动学习 |
| `memory/*.md` | `MEMORY.md` | 记忆条目 |

### 核心层 → .agents Protocol

| 核心层文件 | → .agents 文件 | 说明 |
|-----------|---------------|------|
| `agent/AGENT.md` | `.agents/agents/microscope/agent.md` | frontmatter + 正文 |
| `agent/config.json` | `.agents/agents/microscope/config.json` | 工具/模型配置 |
| `skills/*.md` | `.agents/skills/*/skill.md` | 技能目录 |
| `memory/*.md` | `.agents/memories/*.md` | 记忆目录 |

### 核心层 → OAF

| 核心层文件 | → OAF 文件 | 说明 |
|-----------|-----------|------|
| `agent/AGENT.md` | `AGENTS.md` | 唯一必需文件，合并人设+技能+流程 |
| `agent/config.json` | `ActiveMCP.json` | MCP 工具子集 |
| `skills/` | `skills/` | 目录结构一致 |

---

## 安装指南模板

### 安装到 CodeBuddy

```bash
# 复制 adapter 文件到 CodeBuddy skills 目录
cp -r MicroScope/adapters/codebuddy/ .codebuddy/skills/microscope/
# 复制参考文档
cp -r MicroScope/prompts/ .codebuddy/skills/microscope/references/
cp -r MicroScope/templates/ .codebuddy/skills/microscope/assets/
```

### 安装到 OpenClaw

```bash
# 复制 SOUL.md 到工作区根目录（或合并到已有 SOUL.md）
cp MicroScope/adapters/openclaw/SOUL.md ./SOUL.md
cp MicroScope/adapters/openclaw/AGENTS.md ./AGENTS.md
```

### 安装到 .agents Protocol

```bash
# 复制到 .agents 目录
mkdir -p .agents/agents/microscope .agents/skills
cp MicroScope/adapters/dotagents/agent.md .agents/agents/microscope/
cp MicroScope/adapters/dotagents/mcp.json .agents/
cp -r MicroScope/skills/ .agents/skills/
```

---

## 设计决策

| 决策 | 理由 |
|------|------|
| **核心层用 Markdown + JSON** | 所有平台都支持，最大公约数 |
| **适配层按平台分目录** | 一次写核心，多平台分发 |
| **技能独立为文件** | 可单独安装、组合、复用 |
| **记忆独立目录** | 跨会话积累，不混在代码里 |
| **不依赖任何平台特有功能** | 核心层可在任何平台运行 |

---

*核心层写一次，适配层自动生成，一个 Agent 跑遍所有平台。*
