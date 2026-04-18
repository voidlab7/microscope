# 安装到 CodeBuddy

## 一键安装

```bash
# 在 MicroScope 目录下执行
python3 adapters/codebuddy/install.py
```

### 安装选项

| 命令 | 说明 |
|------|------|
| `python3 install.py` | 安装到当前项目的 `.codebuddy/skills/` |
| `python3 install.py --global` | 安装到用户级 `~/.codebuddy/skills/`（所有项目可用） |
| `python3 install.py --uninstall` | 卸载 |
| `python3 install.py --check` | 仅检查环境依赖 |

### 从 GitHub 安装（非本地）

```bash
# 1. 克隆仓库
git clone https://github.com/voidlab7/microscope.git /tmp/microscope

# 2. 运行安装脚本
cd /tmp/microscope
python3 adapters/codebuddy/install.py --global

# 3. 清理
rm -rf /tmp/microscope
```

## 安装后的目录结构

```
.codebuddy/skills/microscope/
├── SKILL.md                    ← 人设 + 铁律 + 工作流（来自 agent/AGENT.md）
├── references/                 ← 按需加载到 AI 上下文
│   ├── image-ocr.md            ← 图片 OCR 双引擎策略
│   ├── pdf-extract.md          ← PDF 解析
│   ├── xlsx-extract.md         ← Excel 解析
│   ├── web-research.md         ← 网络调研
│   ├── enterprise-lookup.md    ← 企业查询
│   ├── market-analysis.md      ← 市场分析
│   ├── data-validation.md      ← 数据验证
│   ├── report-generate.md      ← 报告生成
│   ├── analysis-frameworks.md  ← 分析框架
│   └── data-labeling.md        ← 数据标注规范
└── assets/                     ← 不加载上下文，用于输出产物
    ├── report-markdown.md      ← 报告模板
    └── enterprise-table-schema.md  ← Excel 字段定义
```

## 环境依赖

安装脚本会自动检查，也可以单独运行：

```bash
python3 adapters/codebuddy/install.py --check
```

### 基础依赖（PDF/Excel 解析）

```bash
pip install -r tools/requirements.txt
```

### 完整依赖（含 OCR）

```bash
pip install -r tools/requirements-full.txt
```

## 触发方式

在 CodeBuddy 中说以下任意关键词即可触发：

- 「市场分析」「行业调研」「企业调研」
- 「竞品分析」「市场报告」「做个调研」
- 「帮我分析这个行业」「帮我查这些企业」

或直接 `@MicroScope`。

## CodeBuddy Skill 加载机制

| 层级 | 加载时机 | 内容 |
|------|---------|------|
| 第1级：元数据 | 始终在上下文 | name + description（~100词） |
| 第2级：SKILL.md | Skill 触发时 | 人设 + 铁律 + 工作流（<5k词） |
| 第3级：references/ | AI 按需加载 | 技能/提示词参考文档 |
| 第3级：assets/ | 不加载上下文 | 模板、字段定义（用于输出） |
