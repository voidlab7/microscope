# MicroScope 工具说明

本目录存放 MicroScope 使用的工具脚本和依赖管理。

---

## 快速开始

```bash
# 检查环境
python3 tools/setup-check.py

# 安装基础依赖（PDF/Excel/报告生成）
pip install -r tools/requirements.txt

# 安装完整依赖（含 OCR，强烈建议）
pip install -r tools/requirements-full.txt
```

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `DEPENDENCIES.md` | 依赖全景图（分层架构 + 打包方案 + 与 CodeBuddy 内置 Skill 关系） |
| `requirements.txt` | 基础 Python 依赖（~50MB） |
| `requirements-full.txt` | 完整依赖含 OCR（~600MB） |
| `setup-check.py` | 环境检查脚本（一键检测所有依赖） |
| `paddleocr-install-guide.md` | PaddleOCR 安装详细指引 |

---

## 工具脚本（Phase 2 规划中）

| 工具 | 文件 | 说明 | 状态 |
|------|------|------|------|
| PDF 解析 | `scripts/pdf_extractor.py` | 提取 PDF 表格和正文 | 🔜 待开发 |
| Excel 解析 | `scripts/xlsx_reader.py` | 读取 Excel 多 sheet | 🔜 待开发 |
| 图片 OCR | `scripts/image_ocr.py` | 双引擎交叉验证（模型+PaddleOCR） | 🔜 待开发 |
| 报告生成 | `scripts/report_generator.py` | 生成 MD/Excel/HTML 报告 | 🔜 待开发 |

---

## 说明

**Phase 1 阶段**（当前），核心能力通过 AI 平台自带工具实现：
- CodeBuddy 的 `read_file` / `web_search` / `web_fetch` / `pdf` skill / `xlsx` skill
- OpenClaw / dotAgents 的内置工具链

**Phase 2+** 会开发独立的工具脚本，可通过 MCP Server 对外暴露，实现平台无关的完整能力。
