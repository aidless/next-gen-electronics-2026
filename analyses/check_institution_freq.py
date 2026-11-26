#!/usr/bin/env python3
"""项目级机构频次审计：统计专题与研究报告中调研机构出现次数，标记单点依赖。

退出码：0 全过 / 1 发现未披露的单点依赖 / 2 用法错 / 3 闸没执行（不等于通过）。
摘要首行：institutions=N docs=M flagged=K problems=P。
"""
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOCS = Path(os.environ.get("INST_FREQ_DOCS", BASE / "manuscript"))
# 单一机构依赖阈值：出现次数 >= 阈值且仅出现在单个专题时标记；已知披露项在 DISCLOSED 中列出
THRESHOLD = 7
INSTITUTIONS = [
    "TrendForce", "SemiAnalysis", "SIA", "WSTS", "UBI Research", "高盛", "Bernstein",
    "大摩", "中汽协", "Yole", "Omdia", "Gartner", "TechInsights", "Counterpoint",
]
DISCLOSED = {
    "SemiAnalysis": ["专题8", "专题22"],
    "UBI Research": ["专题15"],
    "TrendForce": ["专题5", "专题6"],
    "WSTS": ["专题5"],
    "SIA": ["专题5"],
    "高盛": ["专题4", "专题14"],
    "Bernstein": ["专题1", "专题13"],
    "TechInsights": ["专题13"],
    "Gartner": ["专题13"],
    "大摩": ["专题14"],
    "中汽协": ["专题19"],
}


def topic_of(name: str) -> str:
    m = re.match(r"(专题\d+)", name)
    return m.group(1) if m else "总报告/合集"


def main() -> int:
    files = sorted(DOCS.glob("专题*.md")) + sorted(DOCS.glob("新一代电子技术-研究报告-*.md"))
    if not files:
        print("exit3: 无文档可审，闸没执行，不等于通过")
        return 3
    counts = defaultdict(int)
    where = defaultdict(set)
    for p in files:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        topic = topic_of(p.name)
        for inst in INSTITUTIONS:
            n = len(re.findall(re.escape(inst), txt))
            if n:
                counts[inst] += n
                where[inst].add(topic)
    flagged = []
    rows = []
    for inst, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        topics = sorted(where[inst])
        disclosed = inst in DISCLOSED and set(DISCLOSED[inst]).issubset(set(topics))
        single = len(topics) == 1 and n >= THRESHOLD
        status = "单点依赖-已披露" if single and disclosed else ("单点依赖-未披露" if single else "多点交叉/低频")
        if single and not disclosed:
            flagged.append(inst)
        rows.append({"institution": inst, "count": n, "topics": topics, "status": status})
    first = f"institutions={len(rows)} docs={len(files)} flagged={len(flagged)} problems={len(flagged)}"
    print(first)
    for r in rows:
        print(f"{r['institution']}\t{r['count']}\t{','.join(r['topics'])}\t{r['status']}")
    out = Path(os.environ.get("INST_FREQ_OUT", BASE / "analyses" / "institution_freq_report.json"))
    out.write_text(json.dumps({"summary": first, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    if flagged:
        for inst in flagged:
            print("FAIL 未披露单点依赖: " + inst)
        return 1
    print("PASS 高频单点依赖均已在审计台账披露")
    return 0


if __name__ == "__main__":
    sys.exit(main())
