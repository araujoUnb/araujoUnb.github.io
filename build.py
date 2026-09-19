#!/usr/bin/env python3
"""Assemble the site: _src/layout.html + _src/pages/*.html -> ./*.html

Each page file starts with a small header block:
    title: Publications
    description: ...
    ---
followed by the page body. Run `python3 build.py` after editing.
"""
import datetime, pathlib, re

ROOT = pathlib.Path(__file__).parent
layout = (ROOT / "_src" / "layout.html").read_text(encoding="utf-8")
updated = datetime.date.today().strftime("%B %Y")

for src in sorted((ROOT / "_src" / "pages").glob("*.html")):
    head, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(":", 1) for line in head.strip().splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    html = layout.replace("{{content}}", body.rstrip() + "\n")
    html = html.replace("{{title}}", meta["title"])
    html = html.replace("{{description}}", meta.get("description", ""))
    html = html.replace("{{updated}}", updated)
    html = re.sub(r"\{\{active:(\w+)\}\}",
                  lambda m: 'class="active"' if m.group(1) == src.stem else "", html)
    (ROOT / src.name).write_text(html, encoding="utf-8")
    print("wrote", src.name)
