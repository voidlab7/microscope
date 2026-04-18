---
id: market-analysis
name: 市场分析
description: 运用分析框架对行业进行结构化分析
enabled: true
---

# 市场分析

## 触发条件
文件解析 + 网络补全完成后自动触发，或用户说「分析一下市场」「竞争格局」

## 输入
- 已解析的文件数据 + 网络补全数据（必填）
- 分析深度：Quick / Standard / Deep（默认 Standard）

## 输出
- 市场概览（规模/增长率/细分）
- 企业图谱（按融资阶段分层）
- 产业链映射
- 竞争格局
- 投资热度判断

## 分析框架
详见 `prompts/analysis-frameworks.md`

## 输出模板
详见 `templates/report-markdown.md`
