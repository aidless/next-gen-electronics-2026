#!/usr/bin/env python3
"""2026-11 新一代电子技术研究年度进展时间轴（由 research-manifest.json 驱动）。"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
FONT = "AR PL UMing CN"
plt.rcParams["font.sans-serif"] = [FONT]
plt.rcParams["axes.unicode_minus"] = False

manifest = json.loads((BASE / "research-manifest.json").read_text(encoding="utf-8"))
history = manifest["loop"]["history"]
milestones = []
for h in history:
    day = h["at"][5:10].replace("-", "/")
    label = f"{day}\n{h['action'][:22]}"
    milestones.append((label, h["result"][:52]))
milestones += [
    ("11/25\n产品化闭环", "commit 955c2e2：三台账/HTML/PDF/EPUB/价值排序/两张图"),
    ("11/25\n五轮收口", "commit 0189b63：v5 合集 26 份/9555 行/389 锚点"),
    ("11/26\n第六波", "专题27落盘；26/28/29/30 三次续写未交付，记 NOT_ASSESSED"),
    ("11/27\n闸化与留痕", "数字一致性闸/机构频次闸 self-test 通过；定时更新落盘"),
]

fig, ax = plt.subplots(figsize=(16, 6.5))
ax.set_xlim(-0.6, len(milestones) - 0.4)
ax.set_ylim(-1.7, 1.7)
ax.axis("off")
ax.set_title("新一代电子技术研究：2026-11 六轮迭代时间轴", fontsize=18, fontweight="bold", pad=12)
ax.plot(range(len(milestones)), [0] * len(milestones), color="#607d8b", lw=2.5, zorder=1)
for i, (label, detail) in enumerate(milestones):
    color = "#2e7d32" if i < len(history) else "#1565c0"
    ax.scatter(i, 0, s=130, color=color, zorder=3, edgecolor="white", linewidth=1.2)
    up = i % 2 == 0
    y = 0.45 if up else -0.45
    ha = "center"
    ax.annotate(label, (i, 0), xytext=(i, y), ha=ha,
                va="bottom" if up else "top", fontsize=9.5, color=color,
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8))
    ax.text(i, y + (0.42 if up else -0.42), detail, ha=ha,
            va="bottom" if up else "top", fontsize=7.5, color="#333", wrap=True)
ax.text(0, -1.5, "判据：日期与结果取自 research-manifest.json + git commit；第六波未交付项如实标注，不计入完成数",
        fontsize=9, color="#555", style="italic")
fig.tight_layout()
out = BASE / "manuscript" / "figures" / "年度进展时间轴-2026-11.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"saved {out}")
