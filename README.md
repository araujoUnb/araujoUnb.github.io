# Daniel Costa Araújo — personal academic page

Static site (plain HTML/CSS, no Jekyll) served with GitHub Pages.
Layout inspired by the [Academic Pages](https://academicpages.github.io/) template.

## Editing

- Page content lives in `_src/pages/*.html` (one file per page; a small `title:`/`description:` header, then the body).
- The shared sidebar / menu / footer is `_src/layout.html`.
- Styles are in `style.css`.
- Run `python3 build.py` to regenerate `index.html`, then commit everything.
  All pages are bundled into the single `index.html`; the menu switches sections
  client-side (`#about`, `#publications`, ...) so navigation is instant. The other
  top-level `*.html` files are tiny redirects kept for old links.

## Assets

- `assets/cv_daniel_araujo.pdf` — CV linked from the menu and sidebar
  (source: `~/Documentos/Pessoal/short_resume/resume/araujo_resume_en.tex`).
- `assets/profile.jpg` — profile photo (optional; a placeholder with initials is shown if the file is missing).
- `assets/unb.png`, `assets/labtelecom.png` — logos.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
