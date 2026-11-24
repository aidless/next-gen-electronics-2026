#!/usr/bin/env python3
"""统一自检：表格空行/列数、代码围栏、占位符残留、合集锚点一致。"""
import os, re, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(BASE, "manuscript")
files = [f for f in os.listdir(MD) if f.endswith(".md")]
fail = 0
for f in sorted(files):
    p = os.path.join(MD, f)
    s = open(p, encoding="utf-8").read()
    lines = s.split("\n")
    issues = []
    # 代码围栏配平
    if s.count("```") % 2: issues.append("代码围栏不配平")
    # 占位符残留
    for ph in ["PENDING", "TODO", "COMM_PENDING", "SECTIONS_PENDING", "[PLACEHOLDER]"]:
        if ph in s: issues.append(f"占位符残留:{ph}")
    # 表格列数一致性（连续表格行）
    in_tbl = []; tbl_no = 0
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("|"):
            in_tbl.append((i, ln.count("|")))
        else:
            if len(in_tbl) >= 2:
                cols = set(c for _, c in in_tbl)
                if len(cols) > 1:
                    tbl_no += 1
                    if tbl_no <= 3: issues.append(f"表格列数不一(行{in_tbl[0][0]}起):{sorted(cols)}")
            in_tbl = []
    status = "OK" if not issues else "FAIL"
    if issues: fail += 1
    print(f"[{status}] {f}: {len(lines)}行 {len(s)}字符" + (" | " + "; ".join(issues) if issues else ""))
# 合集锚点自检
col = os.path.join(MD, "新一代电子技术-研究合集-2026-11-23.md")
if os.path.exists(col):
    s = open(col, encoding="utf-8").read()
    anchors = set(re.findall(r'<a id="(doc\d+(?:-s\d+)?)"></a>', s))
    links = set(re.findall(r'\]\(#(doc\d+(?:-s\d+)?)\)', s))
    missing = links - anchors
    print(f"[合集] 锚点{len(anchors)} 链接{len(links)} 缺失{len(missing)}" + (f" {missing}" if missing else ""))
    if missing: fail += 1
print(f"\n总计: {fail} 份有问题" if fail else "\n全部通过")
sys.exit(1 if fail else 0)
