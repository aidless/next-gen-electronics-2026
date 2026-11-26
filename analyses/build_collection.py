# -*- coding: utf-8 -*-
import re, io

docs = [
    ("doc0", "总报告", "新一代电子技术-研究报告-2026-11-23.md"),
    ("doc1", "专题一 先进制程与先进封装", "专题1-先进制程与先进封装-2026-11-23.md"),
    ("doc2", "专题二 后摩尔器件与计算新原理", "专题2-后摩尔器件与计算新原理-2026-11-23.md"),
    ("doc3", "专题三 新材料宽禁带与柔性生物电子", "专题3-新材料宽禁带与柔性生物电子-2026-11-23.md"),
    ("doc4", "专题四 通信与光电融合", "专题4-通信与光电融合-2026-11-23.md"),
    ("doc5", "专题五 产业格局政策与供应链", "专题5-产业格局政策与供应链-2026-11-23.md"),
    ("doc6", "专题六 High-NA EUV与先进光刻", "专题6-High-NA EUV与先进光刻-2026-11-24.md"),
    ("doc7", "专题七 新型存储与存算一体", "专题7-新型存储与存算一体-2026-11-24.md"),
    ("doc8", "专题八 EDA工具链与AI辅助设计", "专题8-EDA工具链与AI辅助设计-2026-11-24.md"),
    ("doc9", "专题九 量子计算硬件与纠错", "专题9-量子计算硬件与纠错-2026-11-24.md"),
    ("doc10", "专题十 AI数据中心电力与散热", "专题10-AI数据中心电力与散热-2026-11-24.md"),
    ("doc11", "专题十一 AI芯片架构与互连", "专题11-AI芯片架构与互连-2026-11-24.md"),
    ("doc12", "专题十二 图像传感器与感知芯片", "专题12-图像传感器与感知芯片-2026-11-24.md"),
    ("doc13", "专题十三 半导体制造设备与量测检测", "专题13-半导体制造设备与量测检测-2026-11-24.md"),
    ("doc14", "专题十四 先进基板与封装材料", "专题14-先进基板与封装材料-2026-11-24.md"),
    ("doc15", "专题十五 新型显示与近眼显示", "专题15-新型显示与近眼显示-2026-11-24.md"),
    ("doc16", "专题十六 光子计算与光AI芯片", "专题16-光子计算与光AI芯片-2026-11-25.md"),
    ("doc17", "专题十七 类脑与神经形态计算", "专题17-类脑与神经形态计算-2026-11-25.md"),
    ("doc18", "专题十八 RISC-V生态", "专题18-RISC-V生态-2026-11-25.md"),
    ("doc19", "专题十九 汽车电子电气架构", "专题19-汽车电子电气架构-2026-11-25.md"),
    ("doc20", "专题二十 航天抗辐射电子", "专题20-航天抗辐射电子-2026-11-25.md"),
    ("doc21", "专题二十一 电子材料表征与计量", "专题21-电子材料表征与计量-2026-11-25.md"),
    ("doc22", "专题二十二 EDA形式验证", "专题22-EDA形式验证-2026-11-25.md"),
    ("doc23", "专题二十三 功率模块封装", "专题23-功率模块封装-2026-11-25.md"),
    ("doc24", "专题二十四 量子经典互连", "专题24-量子经典互连-2026-11-25.md"),
    ("doc25", "专题二十五 脑机接口临床转化", "专题25-脑机接口临床转化-2026-11-25.md"),
    ("doc27", "专题二十七 EDA后端工具链", "专题27-EDA后端工具链-2026-11-25.md"),
]

def clean_title(t):
    t = t.strip()
    t = re.sub(r'^#{1,2}\s+', '', t)
    return t.strip()

# 读取并解析每份文档
parsed = []
for key, label, path in docs:
    with io.open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    h1 = None
    h2s = []
    for ln in lines:
        if re.match(r'^#\s+', ln) and h1 is None:
            h1 = clean_title(ln)
        elif re.match(r'^##\s+', ln):
            h2s.append(clean_title(ln))
    parsed.append((key, label, path, lines, h1, h2s))

# 生成带锚点的正文
out_body = []
for key, label, path, lines, h1, h2s in parsed:
    out_body.append('<a id="%s"></a>' % key)
    sidx = 0
    for ln in lines:
        if re.match(r'^##\s+', ln):
            sidx += 1
            out_body.append('<a id="%s-s%d"></a>' % (key, sidx))
        out_body.append(ln)
    out_body.append('')  # 文档间空行

# 生成总目录
toc = []
toc.append('# 新一代电子技术研究合集（2024–2026）')
toc.append('')
toc.append('> 汇编日期：2026-11-26 ｜ 含 1 份总报告 + %d 份已交付专题（五轮完整 25 份 + 第六波专题27），共 %d 篇。' % (len(docs)-1, len(docs)))
toc.append('> 第六波仅收录已落盘的专题27 EDA 后端工具链；专题26/28/29/30 三次续写无交付、状态 `NOT_ASSESSED`，在主报告第十四节登记，不代写、不推断。')
toc.append('> 全部对齐至 2026-11 最新口径；数字附出处、冲突口径并列、未取一手源标 `UNVERIFIED`。')
toc.append('')
toc.append('## 总目录')
toc.append('')
for key, label, path, lines, h1, h2s in parsed:
    toc.append('- [%s](#%s)' % (h1 or label, key))
    for i, t in enumerate(h2s, 1):
        toc.append('  - [%s](#%s-s%d)' % (t, key, i))
    toc.append('')
toc.append('---')
toc.append('')

final = '\n'.join(toc) + '\n'.join(out_body)
with io.open('新一代电子技术-研究合集-2026-11-23.md', 'w', encoding='utf-8') as f:
    f.write(final)

print('合集生成完成，行数:', final.count('\n')+1)
for key, label, path, lines, h1, h2s in parsed:
    print('  %s (%d 节): %s' % (label, len(h2s), h1))
