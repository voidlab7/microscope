#!/usr/bin/env python3
"""
AI眼镜市场分析 - 完整提取与汇总脚本
支持：Excel、PDF、图片 OCR（EasyOCR）
"""

import os
import json
import pandas as pd
import pdfplumber
from PIL import Image
import easyocr
import re
from pathlib import Path
from datetime import datetime

# 路径配置
BASE_DIR = Path("/Users/vivibaby/Documents/workspace/microscope")
INPUT_DIR = BASE_DIR / "projects/ai-glasses/input"
OUTPUT_DIR = BASE_DIR / "projects/ai-glasses/output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 目标列名
TARGET_COLUMNS = [
    "序号", "企业名称", "注册资本", "融资历程", "前十大股东及股权比例",
    "主营产品", "最新估值", "市场份额及排名", "对标国际企业", "主营范围"
]

# 列名映射（标准化）
COLUMN_MAP = {
    # 序号
    "No.": "序号", "编号": "序号", "ID": "序号",
    # 企业名称
    "公司名称": "企业名称", "公司": "企业名称", "名称": "企业名称",
    "企业": "企业名称", "单位名称": "企业名称",
    # 注册资本
    "注册资金": "注册资本", "注册资本（万元）": "注册资本",
    # 融资历程
    "融资": "融资历程", "融资情况": "融资历程", "融资轮次": "融资历程",
    # 股东
    "股东": "前十大股东及股权比例", "股权结构": "前十大股东及股权比例",
    # 主营产品
    "产品": "主营产品", "核心产品": "主营产品",
    # 估值
    "估值": "最新估值", "公司估值": "最新估值",
    # 市场份额
    "市场份额": "市场份额及排名", "排名": "市场份额及排名",
    # 对标
    "对标": "对标国际企业", "对标企业": "对标国际企业",
    # 范围
    "经营范围": "主营范围", "业务范围": "主营范围",
}


def normalize_column_name(col):
    """标准化列名"""
    col = str(col).strip()
    return COLUMN_MAP.get(col, col)


def extract_from_excel(file_path):
    """从 Excel 提取表格"""
    print(f"[Excel] 解析: {file_path.name}")
    dfs = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
    all_data = []
    for sheet_name, df in dfs.items():
        df = df.rename(columns=lambda x: normalize_column_name(x))
        # 筛选目标列
        cols = [c for c in TARGET_COLUMNS if c in df.columns]
        if cols:
            all_data.append(df[cols])
            print(f"  - Sheet '{sheet_name}': {len(df)} 行")
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame(columns=TARGET_COLUMNS)


def extract_from_pdf(file_path):
    """从 PDF 提取表格"""
    print(f"[PDF] 解析: {file_path.name}")
    all_tables = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.rename(columns=lambda x: normalize_column_name(x))
                    # 筛选目标列
                    cols = [c for c in TARGET_COLUMNS if c in df.columns]
                    if cols:
                        all_tables.append(df[cols])
                        print(f"  - 第 {i+1} 页: {len(df)} 行")
    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame(columns=TARGET_COLUMNS)


def extract_from_image(file_path):
    """从图片 OCR 提取表格（EasyOCR）"""
    print(f"[Image] OCR: {file_path.name}")
    try:
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        result = reader.readtext(str(file_path))
        
        # 简单的表格结构识别
        # 将 OCR 结果按 Y 坐标排序，然后按行分组
        lines = {}
        for (bbox, text, conf) in result:
            if conf < 0.5:
                continue
            # 计算中心点 Y 坐标
            y_center = (bbox[0][1] + bbox[2][1]) / 2
            # 按 Y 坐标聚类（每行）
            line_key = int(y_center / 20)  # 假设行高约 20 像素
            if line_key not in lines:
                lines[line_key] = []
            # 按 X 坐标排序
            x_center = (bbox[0][0] + bbox[2][0]) / 2
            lines[line_key].append((x_center, text))
        
        # 按行排序，每行内按 X 排序
        sorted_lines = []
        for line_key in sorted(lines.keys()):
            line_items = sorted(lines[line_key], key=lambda x: x[0])
            sorted_lines.append([text for _, text in line_items])
        
        if not sorted_lines:
            print("  - 未识别到有效文本")
            return pd.DataFrame(columns=TARGET_COLUMNS)
        
        # 假设第一行是表头
        header = sorted_lines[0]
        data = sorted_lines[1:]
        
        df = pd.DataFrame(data, columns=header)
        df = df.rename(columns=lambda x: normalize_column_name(x))
        
        # 筛选目标列
        cols = [c for c in TARGET_COLUMNS if c in df.columns]
        if cols:
            print(f"  - 识别到 {len(df)} 行")
            return df[cols]
        else:
            print("  - 未匹配到目标列")
            return pd.DataFrame(columns=TARGET_COLUMNS)
    except Exception as e:
        print(f"  - OCR 失败: {e}")
        return pd.DataFrame(columns=TARGET_COLUMNS)


def merge_data(dfs):
    """合并多个 DataFrame"""
    if not dfs:
        return pd.DataFrame(columns=TARGET_COLUMNS)
    return pd.concat(dfs, ignore_index=True)


def deduplicate_by_company(df):
    """按企业名称去重"""
    if "企业名称" not in df.columns:
        return df
    # 去重：保留信息最全的记录
    df['_info_count'] = df.notna().sum(axis=1)
    df = df.sort_values('_info_count', ascending=False).drop_duplicates(subset=['企业名称'], keep='first')
    df = df.drop(columns=['_info_count'])
    return df


def to_markdown(df):
    """转换为 Markdown"""
    lines = ["# AI眼镜市场分析汇总\n"]
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"总计: {len(df)} 条记录\n")
    lines.append("\n## 数据表格\n\n")
    
    # 表头
    lines.append("| " + " | ".join(TARGET_COLUMNS) + " |\n")
    lines.append("| " + " | ".join(["---"] * len(TARGET_COLUMNS)) + " |\n")
    
    # 数据行
    for _, row in df.iterrows():
        values = [str(row.get(col, "")).replace("|", "\\|") for col in TARGET_COLUMNS]
        lines.append("| " + " | ".join(values) + " |\n")
    
    return "".join(lines)


def save_intermediate(df, name):
    """保存中间结果"""
    path = OUTPUT_DIR / f"{name}.json"
    df.to_json(path, orient='records', force_ascii=False, indent=2)
    print(f"[保存] {path}")


def main():
    print("=" * 50)
    print("AI眼镜市场分析 - 完整提取流程")
    print("=" * 50)
    
    # 收集输入文件
    excel_files = list(INPUT_DIR.glob("*.xlsx")) + list(INPUT_DIR.glob("*.xls"))
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    image_files = list(INPUT_DIR.glob("*.png")) + list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.jpeg"))
    
    print(f"\n找到文件:")
    print(f"  - Excel: {len(excel_files)} 个")
    print(f"  - PDF: {len(pdf_files)} 个")
    print(f"  - 图片: {len(image_files)} 个")
    
    dfs = []
    
    # 提取 Excel
    for f in excel_files:
        df = extract_from_excel(f)
        if not df.empty:
            dfs.append(df)
            save_intermediate(df, f"excel_{f.stem}")
    
    # 提取 PDF
    for f in pdf_files:
        df = extract_from_pdf(f)
        if not df.empty:
            dfs.append(df)
            save_intermediate(df, f"pdf_{f.stem}")
    
    # 提取图片
    for f in image_files:
        df = extract_from_image(f)
        if not df.empty:
            dfs.append(df)
            save_intermediate(df, f"image_{f.stem}")
    
    # 合并
    print("\n[合并] 数据...")
    merged = merge_data(dfs)
    print(f"  - 合并前: {sum(len(d) for d in dfs)} 行")
    print(f"  - 合并后: {len(merged)} 行")
    
    # 去重
    print("\n[去重] 按企业名称...")
    deduped = deduplicate_by_company(merged)
    print(f"  - 去重后: {len(deduped)} 行")
    
    # 保存中间结果
    save_intermediate(deduped, "merged_deduped")
    
    # 导出 Markdown
    print("\n[导出] Markdown...")
    md = to_markdown(deduped)
    md_path = OUTPUT_DIR / "market-summary.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  - {md_path}")
    
    # 导出 Excel
    print("\n[导出] Excel...")
    excel_path = OUTPUT_DIR / "企业汇总表.xlsx"
    deduped.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"  - {excel_path}")
    
    print("\n" + "=" * 50)
    print("完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
