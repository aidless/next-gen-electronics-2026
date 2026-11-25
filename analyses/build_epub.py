# -*- coding: utf-8 -*-
"""把研究合集 Markdown 转成 EPUB（一份主报告 + 每份专题一章）。"""
import re, io, markdown
from ebooklib import epub

SRC = "manuscript/新一代电子技术-研究合集-2026-11-23.md"
OUT = "manuscript/新一代电子技术-研究合集-2026-11-25.epub"
raw = io.open(SRC, encoding="utf-8").read()
raw = re.sub(r'<a id="doc\d+(?:-s\d+)?"></a>\n?', '', raw)

# 按 h1 切分章节
parts = re.split(r'(?m)^#\s+', raw)
parts = [p for p in parts if p.strip()]
print("检测到章节:", len(parts))

book = epub.EpubBook()
book.set_identifier("next-gen-electronics-2026-collection")
book.set_title("新一代电子技术研究合集 2024–2026")
book.set_language("zh-CN")
book.add_author("新一代电子技术研究项目")

CSS = """body{font-family:'Noto Sans CJK SC',sans-serif;line-height:1.7}
table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:5px;text-align:left}
h1{border-bottom:2px solid #36c}p{margin:0.6em 0}"""

chapters = []
for i, part in enumerate(parts):
    lines = part.split("\n")
    title = lines[0].strip()
    body_md = "\n".join(lines[1:])
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])
    body_html = md.convert(body_md)
    ch = epub.EpubHtml(title=title[:60], file_name="ch%02d.xhtml" % i, lang="zh-CN")
    ch.content = "<h1>%s</h1>%s" % (title, body_html)
    book.add_item(ch)
    chapters.append(ch)

nav_css = epub.EpubItem(uid="nav.css", file_name="style/nav.css", media_type="text/css", content=CSS)
book.add_item(nav_css)
book.toc = tuple(epub.Link(c.file_name, c.title, "ch%d" % j) for j, c in enumerate(chapters))
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = ["nav"] + chapters
epub.write_epub(OUT, book)
print("EPUB 生成:", OUT, "章节", len(chapters))
