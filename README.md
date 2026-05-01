# MicroScope

> 投资向行业调研与市场分析产品。  
> MicroScope 现在只做 **Industry Research**：市场规模、产业链、竞争格局、融资情况、壁垒风险和投资判断。

---

## 产品边界

MicroLab 调研产品现在分三层：

| 层级 | 名称 | 职责 |
|---|---|---|
| 底座 | `MicroEngine` | 通用采集、解析、补全、来源标注、报告规范 |
| 产品 A | `MicroScope` | 投资向行业调研 / 市场分析 |
| 产品 B | `MicroRadar` | 内容机会雷达 / 小红书需求 / MicroPub Brief |

MicroScope 不再负责：

```text
内容机会
小红书选题
评论区需求挖掘
产品 MVP 建议
MicroPub Brief
```

这些归 `products/MicroRadar/`。

---

## MicroScope 回答什么

```text
这个行业值不值得看？
市场规模和增长如何？
产业链怎么分？
哪些公司值得关注？
商业模式是否成立？
融资和资本热度怎样？
壁垒在哪里？
风险是什么？
投资上应该优先看哪类标的？
```

---

## 功能

- 多格式输入：PDF / Excel / 图片 / Word / 网页
- 网络补全：结合公开数据验证和补全企业信息
- 结构化分析：企业图谱 / 竞争格局 / 产业链 / 投资热度
- 投资判断：优先关注标的、谨慎关注标的、风险和观察指标
- 多格式输出：Markdown / Excel / HTML 报告

---

## 目录结构

```text
MicroScope/
├── agent/                         # Agent 核心定义
│   └── AGENT.md
├── workflows/                     # 行业调研工作流
│   └── industry-research.md
├── skills/                        # 文件解析、数据补全、报告生成技能
│   ├── pdf-extract.md
│   ├── xlsx-extract.md
│   ├── image-ocr.md
│   ├── web-research.md
│   ├── enterprise-lookup.md
│   ├── market-analysis.md
│   ├── data-validation.md
│   └── report-generate.md
├── prompts/                       # 行业调研 Prompt
│   ├── analysis-frameworks.md
│   ├── enterprise-lookup.md
│   └── data-labeling.md
├── templates/                     # 行业报告模板
│   ├── report-markdown.md
│   └── enterprise-table-schema.md
├── projects/                      # 行业调研项目
│   ├── ai-glasses/
│   └── ai-toys/
├── tools/                         # PDF/XLSX/OCR 工具
├── docs/
└── README.md
```

---

## 使用方式

### 纯网络行业调研

```text
@MicroScope 行业调研：AI 玩具，纯网络搜索，输出投资向行业报告。
```

### 带附件行业调研

```text
@MicroScope 帮我分析 AI 眼镜市场
+ 附件：PDF、Excel、图片
```

MicroScope 会：

1. 创建 `projects/{topic}/` 项目目录；
2. 解析输入文件，或执行网络搜索；
3. 补全企业、融资、市场规模、产业链信息；
4. 交叉验证数据来源；
5. 输出投资向行业报告。

---

## 标准输出

```text
projects/{topic}/
├── project.json
├── input/
├── raw/
├── processed/
│   ├── market-signals.json
│   ├── companies.json
│   ├── investment-thesis.json
│   └── risks.json
└── output/
    ├── industry-report.md
    ├── report.md
    └── summary.md
```

可选附录：

```text
output/product-opportunity.md
```

注意：产品机会附录只能作为补充，不得污染 `industry-report.md`。

---

## 数据标注规范

| 标注 | 含义 |
|---|---|
| `[文件]` | 来自用户提供的文件 |
| `[网络:来源名](URL)` | 来自网络搜索或网页抓取 |
| `[推测:依据]` | 基于已知信息推断 |
| `†` | 未公开/无法验证 |
| `⚠️` | 文件与网络数据冲突 |

---

## 和 MicroRadar 的区别

| 问题 | 用哪个产品 |
|---|---|
| “AI 玩具行业值不值得投？” | `MicroScope` |
| “AI 玩具产业链怎么分？” | `MicroScope` |
| “AI 玩具有哪些公司？” | `MicroScope` |
| “小红书上 AI 玩具有哪些需求？” | `MicroRadar` |
| “今天写什么 AI 玩具选题？” | `MicroRadar` |
| “生成 MicroPub Brief” | `MicroRadar` |

---

## 安装

适配 6 种 AI 编程环境，按平台选择：

### CodeBuddy

```bash
python3 adapters/codebuddy/install.py --global
```

### Claude Code

```bash
cat MicroScope/agent/AGENT.md >> CLAUDE.md
```

---

## 许可

MIT
