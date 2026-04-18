#!/usr/bin/env python3
"""
AI眼镜市场分析 - 完整提取与汇总脚本 v2
支持：Excel、PDF、图片 OCR（EasyOCR）
正确解析 Excel 和 PDF 中的表格结构
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


def extract_from_excel(file_path):
    """从 Excel 提取表格"""
    print(f"[Excel] 解析: {file_path.name}")
    all_data = []
    
    xls = pd.ExcelFile(file_path)
    
    # 处理"企业融资情况" sheet - 包含企业名称、行业明细、企业简介、最新融资情况
    if "企业融资情况" in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name="企业融资情况", header=0)
        print(f"  - Sheet '企业融资情况': {len(df)} 行")
        
        # 映射列
        records = []
        for _, row in df.iterrows():
            record = {
                "企业名称": row.get("企业名称", ""),
                "主营范围": row.get("行业明细", ""),
                "主营产品": row.get("企业简介（摘要）", ""),
                "融资历程": row.get("最新融资情况", ""),
            }
            # 提取注册资本（从融资历程中）
            融资文本 = str(record["融资历程"])
            if "注册资本" in 融资文本:
                match = re.search(r'注册资本约?(\d+(?:\.\d+)?)\s*(万|亿)?元', 融资文本)
                if match:
                    val, unit = match.groups()
                    if unit == "亿":
                        record["注册资本"] = f"{val}亿元"
                    else:
                        record["注册资本"] = f"{val}万元"
            
            # 提取估值（从融资历程中）
            if "估值" in 融资文本:
                match = re.search(r'估值[达约]?(\d+(?:\.\d+)?)\s*(万|亿)?美元', 融资文本)
                if match:
                    val, unit = match.groups()
                    record["最新估值"] = f"{val}亿美元"
            
            records.append(record)
        
        all_data.extend(records)
    
    # 处理"整机及核心部件厂商" sheet
    if "整机及核心部件厂商" in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name="整机及核心部件厂商", header=0)
        print(f"  - Sheet '整机及核心部件厂商': {len(df)} 行")
        
        for _, row in df.iterrows():
            record = {
                "企业名称": row.get("企业名称", ""),
                "主营范围": row.get("行业明细", ""),
                "主营产品": row.get("企业简介（摘要）", ""),
            }
            # 提取注册资本
            简介 = str(record["主营产品"])
            if "注册资金" in 简介:
                match = re.search(r'注册资金(\d+(?:\.\d+)?)\s*(万|亿)?元', 简介)
                if match:
                    val, unit = match.groups()
                    if unit == "亿":
                        record["注册资本"] = f"{val}亿元"
                    else:
                        record["注册资本"] = f"{val}万元"
            
            all_data.append(record)
    
    # 处理"技术方案及应用厂商" sheet
    if "技术方案及应用厂商" in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name="技术方案及应用厂商", header=0)
        print(f"  - Sheet '技术方案及应用厂商': {len(df)} 行")
        
        for _, row in df.iterrows():
            record = {
                "企业名称": row.get("企业名称", ""),
                "主营范围": row.get("行业明细", ""),
                "主营产品": row.get("企业简介（摘要）", ""),
            }
            all_data.append(record)
    
    return pd.DataFrame(all_data)


def extract_from_pdf(file_path):
    """从 PDF 提取表格"""
    print(f"[PDF] 解析: {file_path.name}")
    all_data = []
    
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            
            for table in tables:
                if not table or len(table) < 2:
                    continue
                
                # 检查是否为企业信息表
                header = [str(cell).strip() if cell else "" for cell in table[0]]
                
                # 查找包含"企业名称"的表格
                if any("企业名称" in h for h in header):
                    print(f"  - 第 {page_num} 页: 找到企业信息表，{len(table)-1} 行")
                    
                    # 确定列索引
                    name_idx = 0
                    desc_idx = 1
                    intro_idx = 2
                    finance_idx = 3
                    
                    for i, h in enumerate(header):
                        if "行业" in h:
                            desc_idx = i
                        elif "简介" in h:
                            intro_idx = i
                        elif "融资" in h:
                            finance_idx = i
                    
                    # 提取数据
                    for row in table[1:]:
                        if len(row) < 4:
                            continue
                        
                        # 跳过注释行
                        name = str(row[name_idx]).strip() if row[name_idx] else ""
                        if not name or "注：" in name or "表格企业信息" in name:
                            continue
                        
                        record = {
                            "企业名称": name,
                            "主营范围": str(row[desc_idx]).strip() if len(row) > desc_idx and row[desc_idx] else "",
                            "主营产品": str(row[intro_idx]).strip() if len(row) > intro_idx and row[intro_idx] else "",
                            "融资历程": str(row[finance_idx]).strip() if len(row) > finance_idx and row[finance_idx] else "",
                        }
                        
                        # 提取注册资本
                        融资文本 = str(record["融资历程"])
                        if "注册资本" in 融资文本:
                            match = re.search(r'注册资本约?(\d+(?:\.\d+)?)\s*(万|亿)?元', 融资文本)
                            if match:
                                val, unit = match.groups()
                                if unit == "亿":
                                    record["注册资本"] = f"{val}亿元"
                                else:
                                    record["注册资本"] = f"{val}万元"
                        
                        # 提取估值
                        if "估值" in 融资文本:
                            match = re.search(r'估值[达约]?(\d+(?:\.\d+)?)\s*(万|亿)?美元', 融资文本)
                            if match:
                                val, unit = match.groups()
                                record["最新估值"] = f"{val}亿美元"
                        
                        all_data.append(record)
    
    return pd.DataFrame(all_data)


def extract_from_image(file_path):
    """从图片 OCR 提取表格（EasyOCR）"""
    print(f"[Image] OCR: {file_path.name}")
    try:
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        result = reader.readtext(str(file_path))
        
        # 简单的表格结构识别
        lines = {}
        for (bbox, text, conf) in result:
            if conf < 0.5:
                continue
            y_center = (bbox[0][1] + bbox[2][1]) / 2
            line_key = int(y_center / 20)
            if line_key not in lines:
                lines[line_key] = []
            x_center = (bbox[0][0] + bbox[2][0]) / 2
            lines[line_key].append((x_center, text))
        
        sorted_lines = []
        for line_key in sorted(lines.keys()):
            line_items = sorted(lines[line_key], key=lambda x: x[0])
            sorted_lines.append([text for _, text in line_items])
        
        if not sorted_lines:
            print("  - 未识别到有效文本")
            return pd.DataFrame()
        
        # 尝试解析为表格
        # 假设每行包含多个字段
        records = []
        for line in sorted_lines:
            if len(line) >= 2:
                # 简单的启发式：第一个字段可能是企业名称
                record = {
                    "企业名称": line[0],
                    "主营产品": " ".join(line[1:]) if len(line) > 1 else "",
                }
                records.append(record)
        
        if records:
            print(f"  - 识别到 {len(records)} 条记录")
            return pd.DataFrame(records)
        else:
            print("  - 未识别到有效记录")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"  - OCR 失败: {e}")
        return pd.DataFrame()


def merge_data(dfs):
    """合并多个 DataFrame"""
    if not dfs:
        return pd.DataFrame(columns=TARGET_COLUMNS)
    
    # 确保所有 DataFrame 都有相同的列
    result = pd.concat(dfs, ignore_index=True)
    
    # 填充缺失的列
    for col in TARGET_COLUMNS:
        if col not in result.columns:
            result[col] = ""
    
    return result[TARGET_COLUMNS]


def deduplicate_by_company(df):
    """按企业名称去重，保留信息最全的记录"""
    if "企业名称" not in df.columns:
        return df
    
    df['_info_count'] = df.notna().sum(axis=1)
    df = df.sort_values('_info_count', ascending=False)
    df = df.drop_duplicates(subset=['企业名称'], keep='first')
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
        values = []
        for col in TARGET_COLUMNS:
            val = str(row.get(col, "")).replace("|", "\\|").replace("\n", " ")
            # 限制长度
            if len(val) > 100:
                val = val[:97] + "..."
            values.append(val)
        lines.append("| " + " | ".join(values) + " |\n")
    
    return "".join(lines)


def save_intermediate(df, name):
    """保存中间结果"""
    path = OUTPUT_DIR / f"{name}.json"
    df.to_json(path, orient='records', force_ascii=False, indent=2)
    print(f"[保存] {path}")


def main():
    print("=" * 50)
    print("AI眼镜市场分析 - 完整提取流程 v2")
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
