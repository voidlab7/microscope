#!/usr/bin/env python3
"""
MicroScope 环境检查脚本
运行: python3 setup-check.py
"""

import sys
import importlib

DEPS = {
    "基础依赖": [
        ("pdfplumber", "pdfplumber", "PDF 表格提取"),
        ("pypdf", "pypdf", "PDF 读写"),
        ("pandas", "pandas", "数据处理"),
        ("openpyxl", "openpyxl", "Excel 读写"),
        ("jinja2", "jinja2", "模板引擎"),
    ],
    "OCR 引擎（强烈建议）": [
        ("paddlepaddle", "paddle", "PaddleOCR 运行时"),
        ("paddleocr", "paddleocr", "图片 OCR"),
    ],
    "增强工具（可选）": [
        ("marker-pdf", "marker", "PDF→Markdown 转换"),
    ],
}


def check_module(import_name: str) -> bool:
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


def main():
    print("=" * 56)
    print("  🔬 MicroScope 环境检查")
    print("=" * 56)

    missing_basic = []
    missing_ocr = []
    missing_optional = []

    for category, deps in DEPS.items():
        print(f"\n  [{category}]")
        for pip_name, import_name, desc in deps:
            ok = check_module(import_name)
            status = "✅" if ok else "❌"
            print(f"  {status} {pip_name:<20s} — {desc}")
            if not ok:
                if category == "基础依赖":
                    missing_basic.append(pip_name)
                elif "OCR" in category:
                    missing_ocr.append(pip_name)
                else:
                    missing_optional.append(pip_name)

    print("\n" + "=" * 56)

    if missing_basic:
        print(f"\n  ⚠️  缺少基础依赖: {', '.join(missing_basic)}")
        print("  安装命令:")
        print("    pip install -r MicroScope/tools/requirements.txt")

    if missing_ocr:
        print(f"\n  ⚠️  缺少 OCR 引擎: {', '.join(missing_ocr)}")
        print("  图片 OCR 将降级为仅模型视觉（无法交叉验证）")
        print("  安装命令:")
        print("    pip install paddlepaddle paddleocr")

    if missing_optional:
        print(f"\n  ℹ️  可选增强未安装: {', '.join(missing_optional)}")

    if not missing_basic and not missing_ocr:
        print("\n  ✅ 所有依赖就绪，MicroScope 全功能可用！")
    elif not missing_basic:
        print("\n  ✅ 基础依赖就绪，可正常工作（OCR 降级模式）")

    print()
    return 1 if missing_basic else 0


if __name__ == "__main__":
    sys.exit(main())
