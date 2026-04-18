---
id: xlsx-extract
name: Excel 文件解析
description: 读取 Excel/CSV 文件，解析多 sheet，识别字段含义
enabled: true
---

# Excel 文件解析

## 触发条件
用户提供 .xlsx/.xls/.csv 文件，或说「解析这个表格」「读取 Excel」

## 输入
- Excel 文件路径（必填）

## 输出
- 每个 sheet 的表头和数据
- 字段含义推断
- 数据质量评估（缺失值、异常值）

## 流程
1. 使用 **pandas** + **openpyxl** 引擎读取文件
2. 列出所有 sheet 名称和行数
3. 提取每个 sheet 的表头和前 10 行样本
4. 推断字段含义（企业名/金额/日期等）
5. 标注数据质量问题（缺失值、异常值）

## 工具依赖
- `pandas`：数据读取和分析
- `openpyxl`：Excel 引擎（.xlsx 格式）
- 备选：`xlrd`（旧版 .xls 格式）

```bash
pip install pandas openpyxl
```
