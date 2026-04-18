# MicroScope 环境依赖全景图

> 哪些工具需要环境依赖？哪些可以打包进 MicroScope？

---

## 依赖矩阵

| Skill | 依赖工具 | 类型 | 是否需要安装 | 打包方案 |
|-------|---------|------|-------------|---------|
| **pdf-extract** | pdfplumber | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **pdf-extract** | marker-pdf | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **pdf-extract** | pypdf | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **xlsx-extract** | pandas | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **xlsx-extract** | openpyxl | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **image-ocr** | paddleocr + paddlepaddle | Python 包 | ✅ 需要 pip install（强烈建议） | 打包 scripts/ |
| **report-generate** | jinja2 | Python 包 | ✅ 需要 pip install | 打包 scripts/ |
| **report-generate** | openpyxl | Python 包 | ✅ 同上 | 打包 scripts/ |
| **web-research** | web_search / web_fetch | 平台内置 | ❌ 不需要 | — |
| **web-research** | Tavily MCP | MCP 服务 | ⚙️ 可选配置 | 打包 mcp-config/ |
| **web-research** | Firecrawl MCP | MCP 服务 | ⚙️ 可选配置 | 打包 mcp-config/ |
| **enterprise-lookup** | web_search / web_fetch | 平台内置 | ❌ 不需要 | — |
| **enterprise-lookup** | 天眼查 API | 外部 API | 🔑 需要 API Key | 打包 config 模板 |
| **market-analysis** | — | 纯 LLM 推理 | ❌ 不需要 | — |
| **data-validation** | — | 纯 LLM 推理 | ❌ 不需要 | — |

---

## 分层依赖架构

```
┌─────────────────────────────────────────────────────┐
│  Layer 0: 零依赖（纯 LLM 推理）                       │
│  market-analysis, data-validation, enterprise-lookup  │
│  → 只需要模型 + web_search/web_fetch 即可工作         │
└─────────────────────────────────────────────────────┘
                        ↑
┌─────────────────────────────────────────────────────┐
│  Layer 1: Python 包依赖（pip install）                │
│  pdf-extract, xlsx-extract, report-generate           │
│  → 需要 pdfplumber, pandas, openpyxl, jinja2 等      │
│  → 可通过 requirements.txt 一键安装                    │
└─────────────────────────────────────────────────────┘
                        ↑
┌─────────────────────────────────────────────────────┐
│  Layer 2: 重型依赖（大型 Python 包）                   │
│  image-ocr (PaddleOCR)                                │
│  → paddlepaddle ~500MB, paddleocr ~100MB 模型下载     │
│  → 首次运行需联网下载模型文件                           │
└─────────────────────────────────────────────────────┘
                        ↑
┌─────────────────────────────────────────────────────┐
│  Layer 3: 外部服务依赖（MCP / API Key）               │
│  Tavily, Firecrawl, 天眼查                            │
│  → 需要 API Key 或 MCP 配置                          │
│  → 增强能力，非必需                                    │
└─────────────────────────────────────────────────────┘
```

---

## 打包方案

### 方案：MicroScope 自带工具脚本 + requirements.txt

将需要 Python 环境依赖的能力，封装为独立脚本放在 `tools/scripts/` 中，并提供 `requirements.txt` 一键安装。

#### 目录结构

```
MicroScope/
└── tools/
    ├── DEPENDENCIES.md          ← 本文件（依赖全景图）
    ├── requirements.txt         ← Python 依赖一键安装
    ├── requirements-full.txt    ← 完整依赖（含 PaddleOCR）
    ├── setup-check.py           ← 环境检查脚本
    ├── paddleocr-install-guide.md
    └── scripts/
        ├── pdf_extractor.py     ← PDF 表格/正文提取
        ├── xlsx_reader.py       ← Excel 多 sheet 读取
        ├── image_ocr.py         ← 图片 OCR（PaddleOCR 封装）
        ├── report_generator.py  ← 报告生成（MD/Excel/HTML）
        └── __init__.py
```

#### requirements.txt（基础依赖，~50MB）

```
# MicroScope 基础依赖
pdfplumber>=0.10.0        # PDF 表格提取
pypdf>=4.0.0              # PDF 读写
pandas>=2.0.0             # 数据处理
openpyxl>=3.1.0           # Excel 读写
jinja2>=3.1.0             # 模板引擎
```

#### requirements-full.txt（完整依赖，含 OCR ~600MB）

```
# MicroScope 完整依赖（含 OCR）
-r requirements.txt
paddlepaddle>=2.6.0       # PaddleOCR 运行时
paddleocr>=2.8.0          # OCR 引擎
marker-pdf>=0.3.0         # PDF→Markdown 转换（含图表/公式）
```

#### setup-check.py（环境检查脚本）

开局运行，检测所有依赖状态，输出清晰的安装建议。

---

## 与 CodeBuddy 内置 Skill 的关系

| 能力 | CodeBuddy 内置 Skill | MicroScope 自带脚本 | 差异 |
|------|---------------------|-------------------|------|
| **PDF 处理** | `.codebuddy/skills/pdf/` | `tools/scripts/pdf_extractor.py` | 内置 Skill 更全（表单填写、合并、加密等），MicroScope 只需表格提取 |
| **Excel 处理** | `.codebuddy/skills/xlsx/` | `tools/scripts/xlsx_reader.py` | 内置 Skill 更全（公式、图表、格式），MicroScope 只需读取和输出 |
| **图片 OCR** | 无内置 | `tools/scripts/image_ocr.py` | MicroScope 独有，双引擎交叉验证 |
| **报告生成** | 无内置 | `tools/scripts/report_generator.py` | MicroScope 独有，多格式输出 |

**策略：**
- 在 CodeBuddy 环境中 → 优先使用内置 pdf/xlsx skill（更成熟、带脚本）
- 在其他环境中（OpenClaw/dotAgents/OAF）→ 使用 MicroScope 自带脚本
- image_ocr.py 和 report_generator.py → MicroScope 独有，所有环境都用自带脚本

---

## 初始化时的环境检查清单

MicroScope 启动时（Step 0），自动运行环境检查：

```
╔══════════════════════════════════════════════════════╗
║  🔬 MicroScope 环境检查                               ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  [基础依赖]                                           ║
║  ✅ pdfplumber    — PDF 表格提取                      ║
║  ✅ pypdf         — PDF 读写                          ║
║  ✅ pandas        — 数据处理                          ║
║  ✅ openpyxl      — Excel 读写                        ║
║  ✅ jinja2        — 模板引擎                          ║
║                                                      ║
║  [OCR 引擎]                                           ║
║  ❌ paddleocr     — 图片 OCR（强烈建议安装）            ║
║  ❌ paddlepaddle  — PaddleOCR 运行时                  ║
║                                                      ║
║  [增强工具]                                           ║
║  ⚙️ marker-pdf    — PDF→Markdown（可选）               ║
║  ⚙️ Tavily MCP    — AI 搜索（可选）                    ║
║  ⚙️ Firecrawl MCP — 网页抓取（可选）                   ║
║                                                      ║
║  安装基础依赖:                                         ║
║    pip install -r MicroScope/tools/requirements.txt   ║
║                                                      ║
║  安装完整依赖（含 OCR）:                                ║
║    pip install -r MicroScope/tools/requirements-full.txt ║
╚══════════════════════════════════════════════════════╝
```
