import os
import glob
import json
import pandas as pd
import pdfplumber

ROOT = "/Users/vivibaby/Documents/workspace/microscope"
INPUT = os.path.join(ROOT, "projects", "ai-glasses", "input")
OUTPUT_DIR = os.path.join(ROOT, "projects", "ai-glasses", "output")
OUT_MD = os.path.join(OUTPUT_DIR, "market-summary.md")

COLUMNS = [
    "序号","企业名称","注册资本","融资历程","前十大股东及股权比例",
    "主营产品","最新估值","市场份额及排名","对标国际企业","主营范围"
]
ALIASES = {
    "企业名称": ["企业名称","公司名称","公司名","企业/公司名称"],
    "注册资本": ["注册资本","注册资金"],
    "融资历程": ["融资历程","融资情况","融资记录","投融资"],
    "前十大股东及股权比例": ["前十大股东及股权比例","股东","股权结构","股权比例"],
    "主营产品": ["主营产品","主要产品","产品"],
    "最新估值": ["最新估值","估值"],
    "市场份额及排名": ["市场份额及排名","市场份额","排名"],
    "对标国际企业": ["对标国际企业","对标企业","国际对标"],
    "主营范围": ["主营范围","主营业务","业务范围"]
}


def normalize_col(name: str) -> str:
    n = str(name).strip()
    for tgt, alts in ALIASES.items():
        for a in alts:
            if a in n:
                return tgt
    if n in COLUMNS:
        return n
    return n


def load_xlsx(xlsx_path: str):
    data = []
    sheets = pd.read_excel(xlsx_path, sheet_name=None)
    for _, df in sheets.items():
        df = df.copy()
        df.columns = [normalize_col(c) for c in df.columns]
        keep = [c for c in df.columns if c in COLUMNS or c == "序号"]
        if not keep:
            continue
        df = df[keep]
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = None
        cols = ["序号"] + [c for c in COLUMNS if c != "序号"]
        df = df.reindex(columns=cols, fill_value=None)
        for _, row in df.iterrows():
            item = {c: ("" if pd.isna(row.get(c)) else str(row.get(c)).strip()) for c in cols}
            if any(item.values()):
                data.append(item)
    return data


def extract_tables_from_pdf(pdf_path: str):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            try:
                tables = page.extract_tables()
            except Exception:
                tables = []
            for tbl in tables or []:
                if not tbl or len(tbl) < 2:
                    continue
                header = [normalize_col(h) for h in tbl[0]]
                for r in tbl[1:]:
                    if r is None:
                        continue
                    row = {}
                    for i, h in enumerate(header):
                        val = r[i] if i < len(r) else None
                        row[h] = (val or "").strip() if isinstance(val, str) else ("" if val is None else str(val))
                    item = {c: row.get(c, "") for c in COLUMNS}
                    if not item.get("企业名称"):
                        for k in header:
                            if k in ["企业名称","公司名称","公司名"] and row.get(k):
                                item["企业名称"] = row.get(k)
                                break
                    item["序号"] = row.get("序号", "")
                    if any(v for v in item.values()):
                        rows.append(item)
    return rows


def merge(primary, secondary):
    def key(d):
        name = (d.get("企业名称") or "").strip()
        idx = (d.get("序号") or "").strip()
        return (name, idx)
    merged = {}
    for src in [secondary, primary]:
        for d in src:
            k = key(d)
            if k not in merged:
                merged[k] = d.copy()
            else:
                for c in COLUMNS + ["序号"]:
                    if (not merged[k].get(c)) and d.get(c):
                        merged[k][c] = d.get(c)
    out = []
    run = 1
    for _, v in merged.items():
        if not v.get("序号"):
            v["序号"] = str(run)
        run += 1
        out.append(v)
    return out


def to_markdown(rows):
    headers = ["序号","企业名称","注册资本","融资历程","前十大股东及股权比例","主营产品","最新估值","市场份额及排名","对标国际企业","主营范围"]
    md = []
    md.append("|" + "|".join(headers) + "|")
    md.append("|" + "|".join(["-" for _ in headers]) + "|")
    for r in rows:
        md.append("|" + "|".join([str(r.get(h, "")) for h in headers]) + "|")
    return "\n".join(md)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    xlsx_files = glob.glob(os.path.join(INPUT, "*.xlsx"))
    pdf_files = glob.glob(os.path.join(INPUT, "*.pdf"))
    xrows, prows = [], []
    for xf in xlsx_files:
        try:
            xrows += load_xlsx(xf)
        except Exception:
            pass
    for pf in pdf_files:
        try:
            prows += extract_tables_from_pdf(pf)
        except Exception:
            pass
    rows = merge(xrows, prows)
    md = to_markdown(rows)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(json.dumps({
        "xlsx_rows": len(xrows),
        "pdf_rows": len(prows),
        "merged_rows": len(rows),
        "out": OUT_MD,
        "note": "图片 OCR 未启用，暂未参与汇总"
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
