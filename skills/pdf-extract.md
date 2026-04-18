---
id: pdf-extract
name: PDF 文件解析
description: 从 PDF 文件中提取表格、正文和图表描述
enabled: true
---

# PDF 文件解析

## 触发条件
用户提供 PDF 文件，或说「解析这个 PDF」「提取 PDF 里的表格」

## 输入
- PDF 文件路径（必填）

## 输出
- 表格 → Markdown 表格
- 正文 → 结构化摘要
- 图表 → 文字描述

## 流程
1. 使用 **Marker** 将 PDF 转为 Markdown（保留表格/公式/图表结构）
2. 使用 **pdfplumber** 精确提取表格数据，转为 Markdown table
3. 提取正文段落，按章节组织
4. 图表用文字描述内容
5. 输出格式化的提取结果

## 工具依赖
- `marker-pdf`：PDF→Markdown 全格式转换（表格+公式+图表）
- `pdfplumber`：精确表格提取（layout-first，纯 Python）
- 备选：`camelot-py`（复杂表格）、`MinerU`（中文 PDF 优化）

```bash
pip install marker-pdf pdfplumber
```
