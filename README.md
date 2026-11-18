# Daniel Costa Araújo — personal academic page

Static site (plain HTML/CSS, no Jekyll) served with GitHub Pages.
Layout inspired by the [Academic Pages](https://academicpages.github.io/) template.

## Editing

- Page content lives in `_src/pages/*.html` (one file per page; a small `title:`/`description:` header, then the body).
- The shared sidebar / menu / footer is `_src/layout.html`.
- Styles are in `style.css`.
- In `_src/pages/publications.html`, every `<li>` needs a `data-year="YYYY"` attribute: it drives the year filter.
- Run `python3 build.py` to regenerate `index.html`, then commit everything.
  All pages are bundled into the single `index.html`; the menu switches sections
  client-side (`#about`, `#publications`, ...) so navigation is instant. The other
  top-level `*.html` files are tiny redirects kept for old links.

## Theme and language

- Dark mode is the default; the ☀/☾ button in the masthead switches to light mode.
  The choice is saved in the visitor's browser (the course pages follow it too).
- The site is bilingual (English default; the PT/EN button switches, `?lang=pt` opens in Portuguese):
  - `_src/pages/<page>.pt.html` is the full Portuguese version of a page (About, Experience,
    Projects, Teaching, Students, Service). **When you edit the English page, edit its `.pt.html` too.**
  - Publications, Talks and Contact have no `.pt.html`: their short labels are written inline as
    `{{English || Português}}` (also used in `_src/layout.html`), so the publication list is kept only once.
  - Placeholders, aria-labels, titles and `<option>` text use `data-pt`, `data-pt-placeholder`,
    `data-pt-aria-label`, `data-pt-title`.

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

## Course slides

`pricom/` (FGA0092) and `eletromagnetismo/` (FGA0119) hold the lecture slides
(interactive HTML decks and/or PDFs, one entry per topic) and an index page,
The script also copies every local file a deck references (`figs/`, the `.en.html` English twin).
linked from Teaching. They are copied from `~/Documentos/UnB/Aulas/curso_*`:
edit the `COURSES` list in `sync_courses.py` if needed, run `python3 sync_courses.py`
and `python3 build.py`, then commit.

## Talks and slides

- Invited talks, seminars and research visits go in `_src/pages/talks.html` (menu entry "Talks").
- Slide and flyer PDFs live in `assets/talks/`, named `YYYY-MM_<host>_<topic>_slides.pdf`.
- Conference-presentation slides are linked next to the paper in `_src/pages/publications.html`,
  right after the doi link, always crediting the speaker:
  `<a class="link" href="assets/talks/....pdf">slides</a> <span class="presenter">presented by Name</span>`.
  Also list them under "Conference presentations" in `talks.html`.
