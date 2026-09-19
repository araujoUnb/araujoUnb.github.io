#!/usr/bin/env python3
"""Assemble the site: _src/layout.html + _src/pages/*.html -> index.html (+ redirect stubs)

Each page file starts with a small header block (`title:` / `description:`),
then `---`, then the page body. All pages are bundled into a single
index.html; the menu switches between them client-side (#about, #publications, ...),
so navigation is instant. For each non-index page a tiny <page>.html redirect
stub is also written so old links keep working. Run `python3 build.py` after editing.
"""
import datetime, pathlib

ROOT = pathlib.Path(__file__).parent
ORDER = ["index", "publications", "projects", "teaching", "students"]
SLUG = {"index": "about"}

layout = (ROOT / "_src" / "layout.html").read_text(encoding="utf-8")
updated = datetime.date.today().strftime("%B %Y")

views, description = [], ""
for stem in ORDER:
    src = ROOT / "_src" / "pages" / f"{stem}.html"
    head, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in head.strip().splitlines())}
    slug = SLUG.get(stem, stem)
    views.append(f'<section class="view" data-view="{slug}">\n{body.rstrip()}\n</section>')
    if stem == "index":
        description = meta.get("description", "")
    else:
        stub = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
                f'<meta http-equiv="refresh" content="0; url=./#{slug}">'
                f'<script>location.replace("./#{slug}")</script>'
                f'<title>{meta["title"]} — Daniel Costa Araújo</title></head>'
                f'<body><a href="./#{slug}">{meta["title"]}</a></body></html>\n')
        (ROOT / f"{stem}.html").write_text(stub, encoding="utf-8")
        print("wrote", f"{stem}.html", "(redirect)")

html = (layout.replace("{{views}}", "\n\n".join(views))
              .replace("{{description}}", description)
              .replace("{{updated}}", updated))
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("wrote index.html")
