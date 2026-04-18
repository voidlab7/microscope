---
id: report-generate
name: 报告生成
description: 将分析结果输出为多格式报告
enabled: true
---

# 报告生成

## 触发条件
分析完成后自动触发，或用户说「出报告」「生成报告」

## 输入
- 分析结果（必填）
- 输出格式：markdown / excel / html / summary（默认 markdown）

## 输出格式

| 格式 | 工具 | 模板 |
|------|------|------|
| **markdown** | Jinja2 模板引擎 | templates/report-markdown.md |
| **excel** | openpyxl（写入 .xlsx） | templates/enterprise-table-schema.md |
| **html** | Jinja2 + 内联样式 | 复用 forum-html-writer 思路 |
| **pdf** | markdown-pdf（MD→HTML→PDF） | 基于 markdown 输出转换 |
| **summary** | 提取报告前 3 个结论 | - |

## 工具依赖
- `jinja2`：模板引擎（MD/HTML 报告）
- `openpyxl`：Excel 写入（企业汇总表）
- `markdown-pdf`：MD→PDF 转换
- 备选：`reportlab`（复杂 PDF 布局）、`xlsxwriter`（Excel 图表）

```bash
pip install jinja2 openpyxl markdown-pdf
```

## 质量检查
输出前自检：
- [ ] 每个数字有来源标注
- [ ] 未验证数据标 †
- [ ] 冲突数据标 ⚠️
- [ ] 有明确分析结论
