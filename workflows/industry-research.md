# MicroScope Workflow：Industry Research 投资向行业调研

> v0.1 / CodeBuddy-first  
> 目标：为投资/咨询/战略研究生成行业调研报告。  
> 强约束：主报告只做行业/投资分析，不输出 MicroLab MVP、小红书选题或 MicroPub Brief。

---

## 1. 触发方式

```text
@MicroScope 行业调研：AI 玩具，纯网络搜索，输出投资向行业报告。
```

或：

```text
@寻 MicroScope 调研 AI 玩具，for 投资，不要产品路线。
```

---

## 2. 输入参数

| 字段 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `topic` | 是 | AI 玩具 | 行业主题 |
| `mode` | 是 | industry-research | 固定为行业调研 |
| `scope` | 否 | global/china | 地域范围 |
| `focus` | 否 | 投资价值/竞争格局/产业链 | 关注维度 |
| `sources` | 否 | web/files | 数据源 |

---

## 3. 输出文件

```text
projects/{topic}/
├── project.json
├── input/
│   └── keywords.md
├── raw/
│   └── web-search-results.json
├── processed/
│   ├── market-signals.json
│   ├── companies.json
│   ├── investment-thesis.json
│   └── risks.json
└── output/
    ├── industry-report.md
    ├── report.md                  # 等同 industry-report，供 Viewer 默认读取
    ├── summary.md
    └── product-opportunity.md      # 可选附录，默认不生成
```

---

## 4. 主报告结构

```markdown
# {行业}行业调研报告（投资向）

## 1. 投资结论
- 是否值得关注
- 当前所处阶段
- 优先关注标的类型
- 回避类型

## 2. 市场规模与增速
- 全球市场
- 中国市场
- CAGR
- 统计口径说明

## 3. 行业驱动因素
- 技术驱动
- 需求驱动
- 供给/成本驱动
- 渠道/IP/政策驱动

## 4. 产业链结构
- 上游
- 中游
- 下游
- 价值量/壁垒判断

## 5. 竞争格局
- 海外玩家
- 国内玩家
- 大厂/IP 方
- 初创公司
- 供应链公司

## 6. 商业模式
- 硬件销售
- 订阅
- 内容/IP
- B 端方案

## 7. 融资与资本热度
- 融资事件
- 资本关注点
- 估值/退出可能性（无数据则标 †）

## 8. 壁垒分析
- 技术
- 供应链
- 渠道
- IP/内容
- 合规/信任

## 9. 风险
- 监管
- 隐私
- 内容安全
- 库存
- 续费率
- 同质化

## 10. 投资观察指标
- 未来 6-12 个月应该跟踪什么
```

---

## 5. 禁止混入主报告的内容

主报告不得出现以下主线：

```text
MicroLab 怎么切
个人/小团队 MVP
小红书验证笔记
MicroPub Brief
评论区 CTA
今天发什么
```

如果用户需要这些内容，另写：

```text
output/product-opportunity.md
```

---

## 6. 数据标注

- 每个数字必须标注 `[网络:来源名](URL)` 或 `[文件]`。
- 无法验证的数据标 `†`。
- 不同来源口径不一致必须标 `⚠️`。
- 结论和建议必须区分事实与判断。

---

## 7. 完成标准

- [ ] `project.json.mode = industry-research`
- [ ] 有 `output/industry-report.md`
- [ ] `output/report.md` 与行业主报告一致或说明跳转
- [ ] 有 `processed/market-signals.json`
- [ ] 有 `processed/companies.json`
- [ ] 有 `processed/investment-thesis.json`
- [ ] 主报告没有 MicroLab MVP / 小红书选题 / MicroPub Brief 主线
