# AI 眼镜行业调研示例

## 输入文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `input/AI眼镜市场分析报告.pdf` | PDF | 原始行业报告 |
| `input/AI眼镜市场分析报告.xlsx` | Excel | 原始数据表 |
| `input/47b6336bc3420e7b4865630fbed61b1b.png` | 图片 | 报告配图（企业信息表） |

## 输出产物

| 文件 | 格式 | 说明 |
|------|------|------|
| `output/AI眼镜市场分析报告_表格.md` | Markdown | PDF 内表格提取 |
| `output/AI眼镜市场分析报告_表格2.md` | Markdown | 图片 OCR 表格提取 |
| `output/AI眼镜市场分析报告_企业汇总.md` | Markdown | 企业汇总（网络补全版） |
| `output/AI眼镜市场分析报告_企业汇总.html` | HTML | HTML 可视化版 |
| `output/AI眼镜行业企业汇总表.xlsx` | Excel | Excel 汇总表 |

## 触发的技能链路

```
pdf-extract → xlsx-extract → image-ocr → enterprise-lookup → market-analysis → report-generate
```
