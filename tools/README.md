# MicroScope 工具说明

本目录存放 MicroScope 使用的工具脚本。

---

## 工具清单（规划中）

| 工具 | 文件 | 说明 | 状态 |
|------|------|------|------|
| PDF 解析 | `pdf-extractor.py` | 提取 PDF 表格和正文 | 🔜 待开发 |
| Excel 解析 | `xlsx-reader.py` | 读取 Excel 多 sheet | 🔜 待开发 |
| 图片 OCR | `image-ocr.py` | 图片表格/文字识别 | 🔜 待开发 |
| 企业查询 | `enterprise-search.py` | 搜索企业公开信息 | 🔜 待开发 |
| 报告生成 | `report-generator.py` | 生成多格式报告 | 🔜 待开发 |

## 说明

Phase 1 阶段，这些能力通过 AI 平台自带工具实现：
- CodeBuddy 的 `read_file` / `web_search` / `web_fetch` / `xlsx` skill / `pdf` skill
- OpenClaw 的内置工具链

Phase 2+ 会开发独立的工具脚本，可通过 MCP Server 对外暴露。
