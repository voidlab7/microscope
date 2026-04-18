---
id: web-research
name: 网络信息调研
description: 搜索网络公开信息，补全和验证文件中的数据
enabled: true
---

# 网络信息调研

## 触发条件
文件解析完成后自动触发，或用户说「帮我查一下」「补全信息」「验证数据」

## 输入
- 待查询的企业名称列表 或 行业关键词（必填）
- 查询深度：Quick / Standard / Deep（默认 Standard）

## 输出
- 企业信息补全表
- 行业数据补充
- 数据交叉验证结果

## 流程
1. 从文件解析结果中提取实体（企业名/产品名/技术名词）
2. 对每个实体执行 **web_search**（平台内置，优先使用）
3. 深度调研时使用 **Tavily** MCP（AI 优化搜索结果）
4. 对关键页面执行 **Firecrawl** 或 **web_fetch** 提取详情
5. 按 data-labeling.md 规范标注来源
6. 与文件数据交叉验证，标注 ⚠️ 冲突

## 工具依赖
- `web_search`（内置）：平台自带搜索，优先使用
- `web_fetch`（内置）：平台自带网页抓取
- **Tavily** MCP：AI 优化搜索，免费 1000 次/月
- **Firecrawl** MCP：网页→Markdown，JS 渲染支持

```json
// MCP 配置（可选增强）
{
  "tavily": { "command": "npx", "args": ["-y", "tavily-mcp"] },
  "firecrawl": { "command": "npx", "args": ["-y", "firecrawl-mcp"] }
}
```
