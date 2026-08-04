#!/usr/bin/env python3
"""
读取 Excel 文件并生成 data.js，供网页前端通过 <script> 标签加载。
使用 <script> 而非 fetch() 可避免本地 file:// 协议下的 CORS 限制，
使网页既能在线上（GitHub Pages）正常工作，也能本地直接双击打开。
在 GitHub Actions 中每次 Excel 更新后自动运行此脚本。
"""

import json
import os
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

# Excel 文件名（与仓库根目录中的文件保持一致）
EXCEL_FILENAME = "甲基化检测试剂盒获批情况统计.xlsx"


def find_excel_file():
    """在脚本所在目录及上级目录查找 Excel 文件"""
    script_dir = Path(__file__).parent
    candidates = [
        script_dir / EXCEL_FILENAME,
        script_dir.parent / EXCEL_FILENAME,
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    print(f"ERROR: Cannot find {EXCEL_FILENAME}", file=sys.stderr)
    sys.exit(1)


def convert_value(val):
    """将 Excel 单元格值转换为 JSON 可序列化的值"""
    if val is None:
        return None
    if isinstance(val, float):
        # 保留 4 位小数
        if val == int(val):
            return int(val)
        return round(val, 4)
    return val


def format_date(val):
    """格式化获批年月"""
    if val is None:
        return ""
    if isinstance(val, (int, float)):
        s = str(int(val)) if isinstance(val, float) and val == int(val) else str(val)
        # 格式如 "2026.05" 或 "2015"
        if "." in s:
            parts = s.split(".")
            if len(parts) == 2:
                y, m = parts
                return f"{y}年{int(m)}月"
        return f"{s}年"
    return str(val)


def main():
    excel_path = find_excel_file()
    print(f"Reading: {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("ERROR: Empty sheet", file=sys.stderr)
        sys.exit(1)

    headers = [str(h).strip() if h else "" for h in rows[0]]
    print(f"Headers: {headers}")

    data = []
    for row in rows[1:]:
        if all(v is None for v in row):
            continue
        record = {}
        for i, val in enumerate(row):
            if i < len(headers):
                col_name = headers[i]
                if col_name == "获批年月":
                    record[col_name] = format_date(val)
                else:
                    record[col_name] = convert_value(val)
        data.append(record)

    # 同时输出 data.js（前端通过 <script> 标签加载）和 data.json（备用）
    script_dir = Path(__file__).parent
    payload = {"headers": headers, "data": data, "total": len(data)}

    # data.js — 用于 <script> 标签加载，兼容本地 file:// 打开
    js_path = script_dir / "data.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.pageData = ")
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write(";\n")

    # data.json — 备用
    json_path = script_dir / "data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Generated: {js_path} ({len(data)} records)")
    print(f"Generated: {json_path} ({len(data)} records)")


if __name__ == "__main__":
    main()
