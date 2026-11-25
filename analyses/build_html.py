# -*- coding: utf-8 -*-
"""把研究合集 Markdown 转成单文件 HTML（带侧边目录、搜索、锚点跳转）。"""
import re, io, sys, markdown

SRC = "manuscript/新一代电子技术-研究合集-2026-11-23.md"
OUT = "manuscript/新一代电子技术-研究合集-2026-11-25.html"

raw = io.open(SRC, encoding="utf-8").read()

# 去掉合集生成时插入的显式 HTML 锚点，改用 markdown toc 生成的 id
raw = re.sub(r'<a id="doc\d+(?:-s\d+)?"></a>\n?', '', raw)

md = markdown.Markdown(extensions=["toc", "tables", "fenced_code", "attr_list"],
                       extension_configs={"toc": {"permalink": False, "slugify": lambda v, s: re.sub(r'[^\w\u4e00-\u9fff-]', '-', v.strip().lower())}})
body = md.convert(raw)
toc = md.toc

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>新一代电子技术研究合集 2024–2026</title>
<style>
:root{--bg:#fafafa;--fg:#222;--accent:#1a5fb4;--border:#ddd;--sidew:320px}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif;color:var(--fg);background:var(--bg);line-height:1.7}
#sidebar{position:fixed;left:0;top:0;bottom:0;width:var(--sidew);overflow-y:auto;background:#f0f3f7;border-right:1px solid var(--border);padding:16px 12px;font-size:13px}
#sidebar h3{margin:0 0 10px;font-size:15px}
#search{width:100%;padding:7px 9px;border:1px solid var(--border);border-radius:5px;margin-bottom:12px}
#toc ul{list-style:none;padding-left:14px}
#toc>ul{padding-left:0}
#toc li{margin:3px 0}
#toc a{color:#333;text-decoration:none;display:block;padding:2px 4px;border-radius:3px}
#toc a:hover{background:#dce6f5;color:var(--accent)}
#toc .toclink-hidden{display:none}
main{margin-left:var(--sidew);padding:32px 48px;max-width:1100px}
h1{border-bottom:3px solid var(--accent);padding-bottom:10px}
h2{margin-top:2em;border-bottom:1px solid var(--border);padding-bottom:6px;color:#1a3a6b}
h3,h4{color:#244}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;background:#fff}
th,td{border:1px solid var(--border);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#eaf0f8}
tr:nth-child(even){background:#f7f9fc}
code{background:#eef;padding:1px 4px;border-radius:3px;font-size:13px}
pre{background:#1e1e2e;color:#e0e0e0;padding:14px;border-radius:6px;overflow:auto}
blockquote{border-left:4px solid var(--accent);background:#f0f5fc;margin:12px 0;padding:8px 16px;color:#444}
a{color:var(--accent)}
hr{border:none;border-top:1px solid var(--border);margin:30px 0}
#toggle{position:fixed;left:12px;bottom:12px;z-index:10;background:var(--accent);color:#fff;border:none;padding:8px 12px;border-radius:5px;cursor:pointer}
@media print{#sidebar,#toggle,#search{display:none}main{margin:0;padding:0;max-width:none}}
@media(max-width:800px){#sidebar{display:none}main{margin-left:0;padding:20px}}
</style>
</head>
<body>
<aside id="sidebar">
<h3>研究合集目录</h3>
<input id="search" placeholder="过滤目录…" autocomplete="off">
<nav id="toc">__TOC__</nav>
</aside>
<button id="toggle" onclick="document.getElementById('sidebar').style.display=document.getElementById('sidebar').style.display==='none'?'block':'none'">目录</button>
<main>__BODY__</main>
<script>
const s=document.getElementById('search');
s.addEventListener('input',()=>{const q=s.value.trim().toLowerCase();
 document.querySelectorAll('#toc li').forEach(li=>{const a=li.querySelector('a');if(a)li.style.display=a.textContent.toLowerCase().includes(q)?'':'none';});
 if(q){document.querySelectorAll('#toc ul').forEach(ul=>{const vis=[...ul.children].some(li=>li.style.display!=='none');ul.style.display=vis?'':'none';});}
 else{document.querySelectorAll('#toc ul').forEach(ul=>ul.style.display='');}
});
</script>
</body>
</html>"""

html = html.replace("__TOC__", toc).replace("__BODY__", body)
io.open(OUT, "w", encoding="utf-8").write(html)
print("HTML 生成:", OUT)
print("大小:", len(html), "字符")
print("目录链接:", html.count('href="#'))
