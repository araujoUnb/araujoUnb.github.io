#!/usr/bin/env python3
"""Assemble the site: _src/layout.html + _src/pages/*.html -> index.html (+ redirect stubs)

Each page file starts with a small header block (`title:` / `description:`),
then `---`, then the page body. All pages are bundled into a single
index.html; the menu switches between them client-side (#about, #publications, ...),
so navigation is instant. For each non-index page a tiny <page>.html redirect
stub is also written so old links keep working. Run `python3 build.py` after editing.

The site is bilingual (English / Portuguese, toggled in the masthead):
  * if _src/pages/<page>.pt.html exists (same header format), it is the
    Portuguese version of the whole page;
  * otherwise, short bilingual fragments are written inline as
    {{English text || Texto em português}} (also works in the layout);
  * attributes and <option> text use data-pt / data-pt-placeholder /
    data-pt-aria-label / data-pt-title (swapped by the script in the layout).
"""
import datetime, pathlib, re

ROOT = pathlib.Path(__file__).parent
ORDER = ["index", "experience", "publications", "talks", "projects", "teaching", "students", "service", "contact"]
SLUG = {"index": "about"}

layout = (ROOT / "_src" / "layout.html").read_text(encoding="utf-8")
today = datetime.date.today()
updated = today.strftime("%B %Y")
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
updated_pt = f"{MESES[today.month - 1]} de {today.year}"

_PART = r"((?:(?!\{\{|\}\}|\|\|).)*?)"  # text that does not cross another marker
I18N = re.compile(r"\{\{" + _PART + r"\s*\|\|\s*" + _PART + r"\}\}", re.S)
def i18n(text):
    """{{en || pt}} -> <span class="l-en" lang="en">en</span><span class="l-pt" lang="pt-BR">pt</span>"""
    return I18N.sub(lambda m: f'<span class="l-en" lang="en">{m[1].strip()}</span>'
                              f'<span class="l-pt" lang="pt-BR">{m[2].strip()}</span>', text)

def read(src):
    head, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in head.strip().splitlines())}
    body = i18n(body.rstrip())
    if "{{" in body or "||" in body:
        raise SystemExit(f"{src.name}: unbalanced or nested {{{{en || pt}}}} marker")
    return meta, body

views, description = [], ""
for stem in ORDER:
    src = ROOT / "_src" / "pages" / f"{stem}.html"
    meta, body = read(src)
    src_pt = src.with_name(f"{stem}.pt.html")
    if src_pt.exists():
        body = (f'<div class="l-en" lang="en">\n{body}\n</div>\n'
                f'<div class="l-pt" lang="pt-BR">\n{read(src_pt)[1]}\n</div>')
    slug = SLUG.get(stem, stem)
    views.append(f'<section class="view" data-view="{slug}">\n{body}\n</section>')
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

layout = i18n(layout.replace("{{description}}", description)
                    .replace("{{updated}}", updated)
                    .replace("{{updated_pt}}", updated_pt))
html = layout.replace("{{views}}", "\n\n".join(views))
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("wrote index.html")
