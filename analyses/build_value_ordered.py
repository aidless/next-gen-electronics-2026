# -*- coding: utf-8 -*-
"""按实际价值重排合集专题顺序（判据：已兑现规模 × 未来2年确定性 × 卡脖子/AI主线关联）。
复用 build_collection 的锚点方案，仅改变 docs 顺序，docN key 保持不变以免破坏已有链接。
"""
import re, io, importlib.util

# 加载主生成器（复用 clean_title / 锚点逻辑）
spec = importlib.util.spec_from_file_location("bc", "analyses/build_collection.py")
# 不直接 exec（会写文件），这里复制最小逻辑

docs_all = [
    ("doc0", "新一代电子技术-研究报告-2026-11-23.md"),
    ("doc1", "专题1-先进制程与先进封装-2026-11-23.md"),
    ("doc2", "专题2-后摩尔器件与计算新原理-2026-11-23.md"),
    ("doc3", "专题3-新材料宽禁带与柔性生物电子-2026-11-23.md"),
    ("doc4", "专题4-通信与光电融合-2026-11-23.md"),
    ("doc5", "专题5-产业格局政策与供应链-2026-11-23.md"),
    ("doc6", "专题6-High-NA EUV与先进光刻-2026-11-24.md"),
    ("doc7", "专题7-新型存储与存算一体-2026-11-24.md"),
    ("doc8", "专题8-EDA工具链与AI辅助设计-2026-11-24.md"),
    ("doc9", "专题9-量子计算硬件与纠错-2026-11-24.md"),
    ("doc10", "专题10-AI数据中心电力与散热-2026-11-24.md"),
    ("doc11", "专题11-AI芯片架构与互连-2026-11-24.md"),
    ("doc12", "专题12-图像传感器与感知芯片-2026-11-24.md"),
    ("doc13", "专题13-半导体制造设备与量测检测-2026-11-24.md"),
    ("doc14", "专题14-先进基板与封装材料-2026-11-24.md"),
    ("doc15", "专题15-新型显示与近眼显示-2026-11-24.md"),
    ("doc16", "专题16-光子计算与光AI芯片-2026-11-25.md"),
    ("doc17", "专题17-类脑与神经形态计算-2026-11-25.md"),
    ("doc18", "专题18-RISC-V生态-2026-11-25.md"),
    ("doc19", "专题19-汽车电子电气架构-2026-11-25.md"),
    ("doc20", "专题20-航天抗辐射电子-2026-11-25.md"),
    ("doc21", "专题21-电子材料表征与计量-2026-11-25.md"),
    ("doc22", "专题22-EDA形式验证-2026-11-25.md"),
    ("doc23", "专题23-功率模块封装-2026-11-25.md"),
    ("doc24", "专题24-量子经典互连-2026-11-25.md"),
    ("doc25", "专题25-脑机接口临床转化-2026-11-25.md"),
    ("doc27", "专题27-EDA后端工具链-2026-11-25.md"),
]
# 价值序：已规模兑现且卡脖子（1/4/10/11/23）→ 导入爬坡确定性高（6/7/8/13/14/22/21）
# → 产业主权（5/18）→ 材料/器件底座（3/2）→ 垂直应用（12/19/25/15/20）
# → 实验室新原理（9/24/16/17）
value_order = ["doc0", "doc1", "doc11", "doc10", "doc4", "doc23", "doc6", "doc7",
               "doc8", "doc27", "doc22", "doc13", "doc14", "doc21",
               "doc5", "doc18", "doc3", "doc2", "doc12", "doc19", "doc25",
               "doc15", "doc20", "doc9", "doc24", "doc16", "doc17"]
# 第六波仅 doc27 已交付，接 doc8；doc26/28/29/30 三次续写无交付，状态 NOT_ASSESSED，不入排序与合集。
by_key = {k: (k, path) for k, path in docs_all}
ranked = [by_key[k] for k in value_order if k in by_key]

def clean_title(t):
    return re.sub(r'^#{1,2}\s+', '', t.strip()).strip()

parsed = []
for key, path in ranked:
    lines = io.open("manuscript/" + path, encoding="utf-8").read().split("\n")
    h1 = next((clean_title(l) for l in lines if re.match(r'^#\s+', l)), None)
    h2s = [clean_title(l) for l in lines if re.match(r'^##\s+', l)]
    parsed.append((key, path, lines, h1, h2s))

out_body, toc = [], []
toc += ["# 新一代电子技术研究合集 — 价值排序版（2024–2026）", "",
        "> 排序判据：已兑现规模 × 未来 2 年确定性 × 与 AI 主线卡脖子程度；高价值/高确定性在前。",
        "> 原取证顺序版见 `新一代电子技术-研究合集-2026-11-23.md`。锚点 key（docN）与顺序版一致，链接不失效。", "",
        "## 价值排序目录", ""]
for key, path, lines, h1, h2s in parsed:
    toc.append("- [%s](#%s)" % (h1 or key, key))
    for i, t in enumerate(h2s, 1):
        toc.append("  - [%s](#%s-s%d)" % (t, key, i))
    toc.append("")
toc += ["---", ""]

for key, path, lines, h1, h2s in parsed:
    out_body.append('<a id="%s"></a>' % key)
    sidx = 0
    for ln in lines:
        if re.match(r'^##\s+', ln):
            sidx += 1
            out_body.append('<a id="%s-s%d"></a>' % (key, sidx))
        out_body.append(ln)
    out_body.append("")

final = "\n".join(toc) + "\n".join(out_body)
out = "manuscript/新一代电子技术-研究合集-价值排序版-2026-11-25.md"
io.open(out, "w", encoding="utf-8").write(final)
print("价值排序版生成:", out, "行数", final.count("\n") + 1)
print("顺序:", " > ".join(k for k in value_order))
