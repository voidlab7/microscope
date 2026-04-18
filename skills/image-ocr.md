---
id: image-ocr
name: 图片 OCR 识别
description: 从图片中识别表格和文字，转为结构化数据
enabled: true
---

# 图片 OCR 识别

## 触发条件
用户提供图片文件（.png/.jpg），或说「识别这张图」「提取图片里的表格」

## 输入
- 图片文件路径（必填）

## 输出
- 表格 → Markdown 表格
- 文字 → 结构化文本
- 图表 → 数据描述

## 流程（自动降级）

```
检测当前环境：
  ↓
路径 A: 模型支持多模态（Claude/GPT-4V）？
  → 直接用 read_file 读取图片，模型"看图识字"
  → 适合简单截图、照片、少量图片

路径 B: PaddleOCR 已安装？
  → 调用 PaddleOCR / PP-Structure 精确识别
  → 适合复杂中文表格、批量图片、高精度需求

路径 C: 都不行？
  → 提示用户：
    "当前模型不支持图片输入，建议安装 PaddleOCR：
     pip install paddlepaddle paddleocr
     详见 tools/paddleocr-install-guide.md"
  → 跳过图片，继续处理其他文件
```

### 路径 A 详细步骤（多模态模型）
1. 使用 read_file 读取图片
2. 让模型识别图片内容（表格/文字/图表）
3. 表格 → 要求模型输出 Markdown table
4. 文字 → 要求模型输出结构化文本
5. 标注"[OCR:模型视觉]"来源

### 路径 B 详细步骤（PaddleOCR）
1. 使用 PaddleOCR 识别图片
2. 表格区域 → PP-Structure → Markdown table
3. 文字区域 → OCR 提取并组织
4. 标注识别置信度和"[OCR:PaddleOCR]"来源

## 工具依赖

**必需**：无（多模态模型自带图片识别）

**可选增强**（复杂中文表格/批量处理/离线运行）：
- `paddleocr` + `paddlepaddle`
- 安装指引：`tools/paddleocr-install-guide.md`

```bash
# 可选安装
pip install paddlepaddle paddleocr
```
