# PaddleOCR 安装指引

> MicroScope 可选依赖 — 仅在处理复杂中文图片表格时需要

---

## 什么时候需要安装？

| 场景 | 需要 PaddleOCR？ |
|------|-----------------|
| 模型支持多模态（Claude/GPT-4V） | ❌ 不需要，模型直接看图 |
| 模型不支持图片（MiniMax/DeepSeek 文本版） | ✅ 需要 |
| 简单截图/照片文字识别 | ❌ 多模态模型够用 |
| 复杂中文表格图片（密集行列） | ✅ 推荐，精度更高 |
| 批量处理大量图片 | ✅ 推荐，成本更低（无 token 消耗） |

---

## 安装步骤

### macOS (Apple Silicon)

```bash
# 1. 安装 PaddlePaddle（CPU 版，约 500MB）
pip install paddlepaddle

# 2. 安装 PaddleOCR
pip install paddleocr

# 3. 验证安装
python -c "from paddleocr import PaddleOCR; print('PaddleOCR installed successfully')"
```

### macOS (Intel)

```bash
pip install paddlepaddle paddleocr
```

### Linux (Ubuntu/Debian)

```bash
# CPU 版
pip install paddlepaddle paddleocr

# GPU 版（如有 NVIDIA GPU，速度快 10x）
pip install paddlepaddle-gpu paddleocr
```

### Windows

```bash
pip install paddlepaddle paddleocr
```

---

## 首次运行

首次使用时会自动下载模型文件（约 100MB），需要联网：

```python
from paddleocr import PaddleOCR

# 初始化（首次会下载模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 识别图片
result = ocr.ocr('your_image.png', cls=True)

# 输出结果
for line in result[0]:
    text = line[1][0]
    confidence = line[1][1]
    print(f'{text} (置信度: {confidence:.2f})')
```

---

## 表格识别（PP-Structure）

```python
from paddleocr import PPStructure

# 初始化表格识别引擎
table_engine = PPStructure(show_log=False)

# 识别图片中的表格
result = table_engine('table_image.png')

# 输出 HTML 表格
for item in result:
    if item['type'] == 'table':
        print(item['res']['html'])  # HTML 格式的表格
```

---

## 常见问题

### Q: 安装报错 "No matching distribution"
```bash
# 确保 Python 版本 >= 3.8
python --version

# 尝试指定版本
pip install paddlepaddle==2.6.2
pip install paddleocr==2.8.1
```

### Q: 首次运行很慢
正常，首次需要下载模型文件。后续运行会使用缓存。

### Q: macOS M 芯片运行报错
```bash
# Apple Silicon 需要用 CPU 版
pip install paddlepaddle
# 不要装 paddlepaddle-gpu
```

### Q: 不想装 PaddleOCR 怎么办？
MicroScope 会自动降级：
1. 如果当前模型支持多模态 → 直接用模型看图（Claude/GPT-4V）
2. 如果模型不支持图片 → 提示用户安装 PaddleOCR
3. 如果都不行 → 跳过图片，只处理文本文件

---

## 卸载

```bash
pip uninstall paddleocr paddlepaddle -y
```

---

*PaddleOCR 是可选增强包，不安装不影响 MicroScope 其他功能。*
