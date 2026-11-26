# -*- coding: utf-8 -*-
"""场景 A/C 中文结构化图，matplotlib 直出 PNG。两张：成熟度地图 + 五轮产业链全景。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

# 中文字体
FONT = "AR PL UMing CN"
plt.rcParams["font.sans-serif"] = [FONT]
plt.rcParams["axes.unicode_minus"] = False

OUT = "manuscript/figures/"
import os
os.makedirs(OUT, exist_ok=True)

# ---------- 图1：技术成熟度地图 ----------
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("新一代电子技术成熟度地图（截至 2026-11）", fontsize=18, fontweight="bold", pad=14)

tiers = [
    (7.0, "#2e7d32", "已规模量产",
     ["2nm N2 / GAA 纳米片", "CoWoS / HBM4", "CPO / 1.6T 光模块", "SiC / GaN 快充", "eMRAM 车规", "800V HVDC 目标推进中"]),
    (4.6, "#f9a825", "导入 / 扩产爬坡",
     ["HBM4E / CoPoS 面板级", "玻璃基板（验证期）", "6G 空口（标准定义）", "Intel 14A / High-NA", "RISC-V RVA23", "区域架构量产车"]),
    (2.2, "#c62828", "实验室 / 早期",
     ["CFET / 2D CFET", "光子计算 / 类脑", "超宽禁带 Ga2O3", "通用光计算 / qLDPC", "Majorana 拓扑（争议）", "BCI 临床试点"]),
]
for y, color, label, items in tiers:
    ax.add_patch(FancyBboxPatch((0.3, y - 1.05), 13.4, 2.0,
                 boxstyle="round,pad=0.02,rounding_size=8",
                 linewidth=2, edgecolor=color, facecolor=color, alpha=0.10))
    ax.text(0.6, y + 0.55, label, fontsize=15, fontweight="bold", color=color)
    for j, it in enumerate(items):
        col = j % 3
        row = j // 3
        ax.text(3.0 + col * 3.7, y + 0.5 - row * 0.65, "· " + it, fontsize=11, color="#222")

ax.text(0.3, 0.15, "判据：已出货量产有客户验证 > 标准/样品就绪 2026–2029 放量 > 器件/论文级突破",
        fontsize=10, color="#555", style="italic")
fig.tight_layout()
fig.savefig(OUT + "成熟度地图-2026-11.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("图1 完成")

# ---------- 图2：五轮 25 专题 + 第六波专题27，4 项 NOT_ASSESSED ----------
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title("新一代电子技术：五轮 25 专题 + 第六波专题27 产业链全景（4 项 NOT_ASSESSED）", fontsize=16, fontweight="bold", pad=14)

layers = [
    (8.4, "#1565c0", "材料与器件底座", "专题3 材料 · 专题2 后摩尔 · 专题23 功率模块 · 专题21 材料表征"),
    (6.6, "#2e7d32", "制造与设计工具", "专题1 制程 · 专题6 光刻 · 专题13 设备量测 · 专题8 EDA · 专题22 形式验证 · 专题27 EDA后端 · 专题14 基板材料"),
    (4.8, "#6a1b9a", "架构与计算新原理", "专题11 架构互连 · 专题16 光子 · 专题17 类脑 · 专题9 量子 · 专题24 量子互连 · 专题18 RISC-V"),
    (3.0, "#ef6c00", "系统与约束", "专题4 通信光电 · 专题7 存储 · 专题10 电力散热 · 专题5 产业主权 · 专题20 航天"),
    (1.2, "#00838f", "终端与应用", "专题12 感知 · 专题15 显示 · 专题19 汽车 · 专题25 BCI 临床"),
]
for y, color, label, items in layers:
    ax.add_patch(FancyBboxPatch((0.3, y - 0.72), 15.4, 1.42,
                 boxstyle="round,pad=0.02,rounding_size=6",
                 linewidth=1.8, edgecolor=color, facecolor=color, alpha=0.10))
    ax.text(0.55, y + 0.12, label, fontsize=12.5, fontweight="bold", color=color)
    ax.text(3.6, y + 0.12, items, fontsize=10, color="#222", va="center")
    if y > 1.2:
        ax.add_patch(FancyArrowPatch((8, y - 0.75), (8, y - 1.45),
                     arrowstyle="-|>", mutation_scale=16, color="#888", lw=1.4))
ax.text(0.4, 0.15, "自下而上：材料→制造→架构→系统→终端；五轮25专题完成，第六波仅专题27交付；专题26/28/29/30 NOT_ASSESSED",
        fontsize=9.5, color="#555", style="italic")
fig.tight_layout()
fig.savefig(OUT + "产业链全景-26专题-2026-11.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("图2 完成")
