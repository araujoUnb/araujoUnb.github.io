#!/usr/bin/env python3
"""Copy course slides into <course>/ and write <course>/index.html, one entry per topic.

Each topic can have an interactive HTML deck, a PDF (Beamer) or both; paths are
relative to the course folder under ~/Documentos/UnB/Aulas. Edit COURSES to add,
rename or reorder topics (modules are (folder, heading, topics)), then run `python3 sync_courses.py` and `python3 build.py`.
"""
import html, pathlib, re, shutil, unicodedata

ROOT = pathlib.Path(__file__).parent
AULAS = pathlib.Path.home() / "Documentos/UnB/Aulas"


def m(folder, stem, title):  # PriCom: one HTML deck per topic
    return (title, {"html": f"{folder}/html/{stem}.html"})


COURSES = {
    "pricom": dict(
        src="curso_pricom",
        title="FGA0092 — Princípios de Comunicação para Engenharia",
        intro="Aulas interativas, uma por tópico: abrem no navegador; use as setas do teclado para avançar. Versão em inglês disponível em cada aula (botão EN).",
        modules=[
            ("modulo0", "Módulo 0 — Apresentação", [m("Modulo0", "apresentacao", "Apresentação da disciplina")]),
            ("modulo1", "Módulo 1 — Análise e transmissão de sinais", [
                m("Modulo1", "transformada_fourier", "Transformada de Fourier"),
                m("Modulo1", "transformadas_uteis", "Transformadas de funções úteis"),
                m("Modulo1", "propriedades_fourier", "Propriedades da transformada de Fourier"),
                m("Modulo1", "sistemas_lti", "Transmissão através de sistemas LTI"),
                m("Modulo1", "energia_potencia", "Energia, potência e densidades espectrais"),
                m("Modulo1", "dft", "DFT e FFT"),
                m("Modulo1", "banda_base_passante", "Banda básica e banda passante"),
            ]),
            ("modulo2", "Módulo 2 — Modulações analógicas e ruído", [
                m("Modulo2", "am_convencional", "AM convencional"),
                m("Modulo2", "am_dsbsc", "AM DSB-SC"),
                m("Modulo2", "am_ssb_vsb", "AM SSB e VSB"),
                m("Modulo2", "modulacao_angular", "Modulação angular (PM e FM)"),
                m("Modulo2", "projeto_transmissor_fm", "Projeto de um transmissor FM"),
                m("Modulo2", "figura_de_ruido", "Figura de ruído"),
                m("Modulo2", "desempenho_am", "Desempenho de sistemas analógicos (AM)"),
                m("Modulo2", "desempenho_fm", "Desempenho de FM e PM"),
            ]),
            ("modulo3", "Módulo 3 — Conversão analógico-digital", [
                m("Modulo3", "amostragem", "Amostragem e reconstrução"),
                m("Modulo3", "quantizacao", "Quantização"),
                m("Modulo3", "forma_de_onda", "Codificação de forma de onda"),
                m("Modulo3", "vocoders", "Vocoders: análise e síntese"),
                m("Modulo3", "video", "Compressão de vídeo"),
            ]),
        ],
    ),
    "eletromagnetismo": dict(
        src="curso_eletromagnetismo/Slides",
        title="FGA0119 — Teoria de Eletromagnetismo",
        intro="Slides por tópico, em PDF e, quando disponível, em versão interativa no navegador. "
              "Disciplina em construção: novos tópicos serão adicionados ao longo do semestre.",
        modules=[
            ("introducao", "Introdução", [
                ("Aula introdutória", {"pdf": "aula_introducao/Latex-slide/main.pdf"}),
            ]),
            ("eletrostatica", "Eletrostática", [
                ("Campos eletrostáticos", {"pdf": "eletrostatica/latex-slide/campos_eletricos/main.pdf"}),
                ("Campos elétricos em meios materiais", {"pdf": "eletrostatica/latex-slide/campos_eletricos_material/main.pdf"}),
            ]),
            ("magnetostatica", "Magnetostática", [
                ("Campos magnetostáticos", {"pdf": "magnetostatica/latex-slide/campo_magnetostatico/main.pdf",
                                            "html": "magnetostatica/html/magnetostatica.html"}),
                ("Forças magnéticas", {"pdf": "magnetostatica/latex-slide/forca_magnetica/main.pdf"}),
            ]),
            ("maxwell", "Campos variantes no tempo", [
                ("Equações de Maxwell", {"pdf": "maxwell/Latex-slide/main.pdf", "html": "maxwell/html/maxwell.html"}),
            ]),
        ],
    ),
}

LABEL = {"html": "aula interativa", "pdf": "PDF", "en": "English"}


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


REF = re.compile(r'(?:src|href|data-href)="([^"#:?$]+\.(?:png|jpe?g|gif|svg|webp|mp4|webm|css|js|html))"')


def copy_deck(s, d, seen):
    """Copy an HTML deck plus every local file it references (figs/, the .en.html twin, ...)."""
    if d in seen:
        return
    seen.add(d)
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
    if s.suffix != ".html":
        return
    for ref in set(REF.findall(s.read_text(encoding="utf-8"))):
        if ref.startswith("/") or ".." in pathlib.PurePosixPath(ref).parts:
            continue
        if not (s.parent / ref).exists():
            raise SystemExit(f"{s}: missing local file {ref}")
        copy_deck(s.parent / ref, d.parent / ref, seen)


for name, c in COURSES.items():
    dst = ROOT / name
    if dst.exists():
        shutil.rmtree(dst)
    src = AULAS / c["src"]
    sections, n, seen = [], 0, set()
    for mdir, mtitle, topics in c["modules"]:
        rows = []
        for title, files in topics:
            links = []
            for kind in ("html", "pdf"):
                if kind not in files:
                    continue
                s = src / files[kind]
                rel = f"{mdir}/{s.stem if kind == 'html' and s.stem != 'main' else slug(title)}.{kind}"
                copy_deck(s, dst / rel, seen)
                links.append((kind, rel))
                n += 1
                en = s.with_name(s.stem + ".en.html")
                if kind == "html" and en.exists():
                    copy_deck(en, dst / mdir / en.name, seen)
                    links.append(("en", f"{mdir}/{en.name}"))
            head = f'<a href="{links[0][1]}">{html.escape(title)}</a>'
            extra = " · ".join(f'<a href="{r}">{LABEL[k]}</a>' for k, r in links) if len(links) > 1 else LABEL[links[0][0]]
            rows.append(f'    <li>{head} <span class="muted">({extra})</span></li>')
        sections.append(f"<h2>{html.escape(mtitle)}</h2>\n<ol>\n" + "\n".join(rows) + "\n</ol>")

    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(c["title"])}</title>
  <meta name="description" content="Slides por tópico da disciplina {html.escape(c["title"])} (UnB/FCTE), Prof. Daniel Costa Araújo.">
  <link rel="stylesheet" href="../style.css?v=7">
  <style>
    .course {{ max-width: 820px; margin: 0 auto; padding: 2rem 16px 3rem; }}
    .course ol {{ padding-left: 1.4rem; }}
    .course li {{ margin: .3rem 0; }}
    .back {{ font-size: .92rem; }}
  </style>
</head>
<body>
<main class="course">
  <p class="back"><a href="../#teaching">← Daniel Costa Araújo · Teaching</a></p>
  <h1 class="page-title">{html.escape(c["title"])}</h1>
  <p class="muted">Universidade de Brasília, Faculdade de Ciências e Tecnologias em Engenharia (FCTE). Prof. Daniel Costa Araújo.<br>
  {html.escape(c["intro"])}</p>

{chr(10).join(sections)}
</main>
</body>
</html>
"""
    (dst / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {name}/index.html ({n} topic files, {len(seen)} files copied)")
