# -*- coding: utf-8 -*-
import re, io

docs = [
    ("doc0", "总报告", "新一代电子技术-研究报告-2026-11-23.md"),
    ("doc1", "专题一 先进制程与先进封装", "专题1-先进制程与先进封装-2026-11-23.md"),
    ("doc2", "专题二 后摩尔器件与计算新原理", "专题2-后摩尔器件与计算新原理-2026-11-23.md"),
    ("doc3", "专题三 新材料宽禁带与柔性生物电子", "专题3-新材料宽禁带与柔性生物电子-2026-11-23.md"),
    ("doc4", "专题四 通信与光电融合", "专题4-通信与光电融合-2026-11-23.md"),
    ("doc5", "专题五 产业格局政策与供应链", "专题5-产业格局政策与供应链-2026-11-23.md"),
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
toc.append('> 汇编日期：2026-11-23 ｜ 含 1 份总报告 + 5 份专题深度报告，共 6 篇。')
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
