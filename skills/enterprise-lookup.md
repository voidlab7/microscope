---
id: enterprise-lookup
name: 企业信息查询
description: 查询企业注册信息、融资、股东、估值等公开数据
enabled: true
---

# 企业信息查询

## 触发条件
需要查询某家企业的详细信息时，或用户说「查一下这家公司」

## 输入
- 企业名称（必填）

## 输出
- 企业卡片（见 prompts/enterprise-lookup.md 模板）

## 查询字段
- 成立时间、注册资本、法人
- 融资历程（轮次、金额、投资方）
- 最新估值/市值
- 股东结构
- 主营产品、核心技术
- 最新动态

## 查询策略
1. **天眼查 Open API**（结构化查询）：注册/融资/股东/诉讼/专利
2. **web_search** 补充：搜索最新新闻、产品发布、人事变动
3. **web_fetch** 深入：抓取企业官网、公开年报

## 工具依赖
- **天眼查 Open API**：免费 100 次/天，数据最全
- **企查查 Open API**：备选，商业 API
- `web_search`（内置）：新闻和动态补充
- `web_fetch`（内置）：企业官网抓取

详细查询策略见 `prompts/enterprise-lookup.md`

## 标注规范
详见 `prompts/data-labeling.md`
