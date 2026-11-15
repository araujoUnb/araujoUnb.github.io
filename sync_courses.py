#!/usr/bin/env python3
"""Copy course slides into <course>/ and write <course>/index.html, one entry per topic.

Each topic can have an HTML deck, a PDF (Beamer) or both; paths are relative to
the course folder under ~/Documentos/UnB/Aulas. Titles are (Portuguese, English)
pairs; an English twin of a deck (<stem>.en.html) is picked up automatically and
linked from the English title. Edit COURSES to add, rename or reorder topics
(modules are (folder, (heading_pt, heading_en), topics); a deck split into one
file per section lists them under "parts"), then run `python3 sync_courses.py`.

Published file names must not change (they are linked from SIGAA): a PDF is named
after the slug of its Portuguese title, so renaming that title renames the PDF.
"""
import html, pathlib, re, shutil, unicodedata

ROOT = pathlib.Path(__file__).parent
AULAS = pathlib.Path.home() / "Documentos/UnB/Aulas"


def m(folder, stem, pt, en):  # PriCom: one HTML deck per topic (+ English twin)
    return ((pt, en), {"html": f"{folder}/html/{stem}.html"})


COURSES = {
    "pricom": dict(
        src="curso_pricom",
        code="FGA0092",
        title=("Princípios de Comunicação para Engenharia", "Communication Principles for Engineering"),
        about=(
            "Fundamentos dos sistemas de comunicação. A disciplina parte da análise espectral de sinais "
            "(série e transformada de Fourier, densidades espectrais de energia e de potência, sinais em banda "
            "básica e em banda passante), passa pelas modulações analógicas (AM e suas variantes DSB-SC, SSB "
            "e VSB, FM, PM e PLL) e pelo efeito do ruído sobre elas, e chega à conversão analógico-digital "
            "(amostragem, quantização, PCM e codificação de fonte) e à comunicação digital em banda básica "
            "(interferência entre símbolos e taxa de erro de bit). As aulas teóricas são acompanhadas de oito "
            "práticas de laboratório.",
            "An introduction to communication systems. The course starts from the spectral analysis of signals "
            "(Fourier series and transform, energy and power spectral densities, baseband and passband signals), "
            "covers analog modulation (AM and its DSB-SC, SSB and VSB variants, FM, PM and the PLL) and the "
            "effect of noise on it, and ends with analog-to-digital conversion (sampling, quantization, PCM and "
            "source coding) and baseband digital communication (intersymbol interference and bit error rate). "
            "Lectures are complemented by eight laboratory sessions.",
        ),
        prereq=("Sinais e Sistemas; Teoria de Circuitos Eletrônicos I.",
                "Signals and Systems; Electronic Circuit Theory I."),
        books="Lathi &amp; Ding, <i>Modern Digital and Analog Communication Systems</i>; "
              "Haykin &amp; Moher, <i>Communication Systems</i>; "
              "Proakis &amp; Salehi, <i>Fundamentals of Communication Systems</i>.",
        usage=("Os slides abrem no navegador; use as setas do teclado para avançar. "
               "Cada aula tem versão em português e em inglês.",
               "The slides open in the browser; use the arrow keys to move forward. "
               "Every lecture is available in Portuguese and in English."),
        modules=[
            ("modulo0", ("Módulo 0 — Apresentação", "Module 0 — Introduction"), [
                m("Modulo0", "apresentacao", "Apresentação da disciplina", "Course introduction"),
            ]),
            ("modulo1", ("Módulo 1 — Análise e transmissão de sinais", "Module 1 — Signal analysis and transmission"), [
                m("Modulo1", "transformada_fourier", "Transformada de Fourier", "Fourier transform"),
                m("Modulo1", "transformadas_uteis", "Transformadas de funções úteis", "Transforms of useful functions"),
                m("Modulo1", "propriedades_fourier", "Propriedades da transformada de Fourier", "Properties of the Fourier transform"),
                m("Modulo1", "sistemas_lti", "Transmissão através de sistemas LTI", "Transmission through LTI systems"),
                m("Modulo1", "energia_potencia", "Energia, potência e densidades espectrais", "Energy, power and spectral densities"),
                m("Modulo1", "dft", "DFT e FFT", "DFT and FFT"),
                m("Modulo1", "banda_base_passante", "Banda básica e banda passante", "Baseband and passband"),
            ]),
            ("modulo2", ("Módulo 2 — Modulações analógicas e ruído", "Module 2 — Analog modulation and noise"), [
                m("Modulo2", "am_convencional", "AM convencional", "Conventional AM"),
                m("Modulo2", "am_dsbsc", "AM DSB-SC", "AM DSB-SC"),
                m("Modulo2", "am_ssb_vsb", "AM SSB e VSB", "AM SSB and VSB"),
                m("Modulo2", "modulacao_angular", "Modulação angular (PM e FM)", "Angle modulation (PM and FM)"),
                m("Modulo2", "projeto_transmissor_fm", "Projeto de um transmissor FM", "Design of an FM transmitter"),
                m("Modulo2", "figura_de_ruido", "Figura de ruído", "Noise figure"),
                m("Modulo2", "desempenho_am", "Desempenho de sistemas analógicos (AM)", "Performance of analog systems (AM)"),
                m("Modulo2", "desempenho_fm", "Desempenho de FM e PM", "Performance of FM and PM"),
            ]),
            ("modulo3", ("Módulo 3 — Conversão analógico-digital", "Module 3 — Analog-to-digital conversion"), [
                m("Modulo3", "amostragem", "Amostragem e reconstrução", "Sampling and reconstruction"),
                m("Modulo3", "quantizacao", "Quantização", "Quantization"),
                m("Modulo3", "forma_de_onda", "Codificação de forma de onda", "Waveform coding"),
                m("Modulo3", "vocoders", "Vocoders: análise e síntese", "Vocoders: analysis and synthesis"),
                m("Modulo3", "video", "Compressão de vídeo", "Video compression"),
            ]),
        ],
    ),
    "eletromagnetismo": dict(
        src="curso_eletromagnetismo/Slides",
        code="FGA0119",
        title=("Teoria de Eletromagnetismo", "Electromagnetic Theory"),
        about=(
            "Fundamentos da teoria eletromagnética clássica e suas aplicações em engenharia. A disciplina cobre "
            "a eletrostática (lei de Coulomb, lei de Gauss, potencial elétrico, capacitância, dielétricos e "
            "energia elétrica), a magnetostática (corrente e condutividade, leis de Biot-Savart e de Ampère, "
            "forças magnéticas) e os campos variantes no tempo: a lei de Faraday, as equações de Maxwell, as "
            "ondas eletromagnéticas e sua propagação em meios materiais, potência, polarização, condições de "
            "contorno e reflexão. É a base para as disciplinas de comunicações, antenas e compatibilidade "
            "eletromagnética.",
            "Fundamentals of classical electromagnetic theory and its engineering applications. The course covers "
            "electrostatics (Coulomb's law, Gauss's law, electric potential, capacitance, dielectrics and electric "
            "energy), magnetostatics (current and conductivity, the Biot–Savart and Ampère laws, magnetic forces) "
            "and time-varying fields: Faraday's law, Maxwell's equations, electromagnetic waves and their "
            "propagation in material media, power, polarization, boundary conditions and reflection. It lays the "
            "groundwork for later courses on communications, antennas and electromagnetic compatibility.",
        ),
        prereq=("Física 1; Cálculo 3.", "Physics 1; Calculus 3."),
        books="Sadiku, <i>Elements of Electromagnetics</i>; Hayt &amp; Buck, <i>Engineering Electromagnetics</i>; "
              "Cheng, <i>Field and Wave Electromagnetics</i>; Griffiths, <i>Introduction to Electrodynamics</i>.",
        usage=("Slides em português, em PDF e, em alguns tópicos, também no navegador (setas do teclado para "
               "avançar). Novos tópicos são publicados ao longo do semestre.",
               "Slides in Portuguese, as PDF and, for some topics, also in the browser (arrow keys to move "
               "forward). New topics are added during the semester."),
        modules=[
            ("introducao", ("Introdução", "Introduction"), [
                (("Aula introdutória", "Introductory lecture"), {"pdf": "aula_introducao/Latex-slide/main.pdf"}),
            ]),
            ("eletrostatica", ("Eletrostática", "Electrostatics"), [
                (("Campos eletrostáticos", "Electrostatic fields"),
                 {"pdf": "eletrostatica/latex-slide/campos_eletricos/main.pdf"}),
                (("Campos elétricos em meios materiais", "Electric fields in material media"),
                 {"pdf": "eletrostatica/latex-slide/campos_eletricos_material/main.pdf"}),
            ]),
            ("magnetostatica", ("Magnetostática", "Magnetostatics"), [
                (("Campos magnetostáticos", "Magnetostatic fields"),
                 {"pdf": "magnetostatica/latex-slide/campo_magnetostatico/main.pdf",
                  "html": "magnetostatica/html/magnetostatica.html"}),
                (("Forças magnéticas", "Magnetic forces"), {"pdf": "magnetostatica/latex-slide/forca_magnetica/main.pdf"}),
            ]),
            ("maxwell", ("Campos variantes no tempo", "Time-varying fields"), [
                (("Equações de Maxwell", "Maxwell's equations"),
                 {"pdf": "maxwell/Latex-slide/main.pdf", "html": "maxwell/html/maxwell.html", "parts": [
                     ("maxwell-01-estatica.html", "Estática e regime variante", "Statics and time-varying fields"),
                     ("maxwell-02-faraday.html", "Lei de Faraday", "Faraday's law"),
                     ("maxwell-03-ampere-maxwell.html", "Lei de Ampère–Maxwell", "Ampère–Maxwell law"),
                     ("maxwell-04-onda.html", "Equação de onda 3D", "3D wave equation"),
                     ("maxwell-05-perdas.html", "Meios com perdas", "Lossy media"),
                     ("maxwell-06-poynting.html", "Vetor de Poynting", "Poynting vector"),
                     ("maxwell-07-polarizacao.html", "Polarização", "Polarization"),
                     ("maxwell-08-contorno.html", "Condições de contorno", "Boundary conditions"),
                     ("maxwell-09-reflexao-normal.html", "Reflexão em incidência normal", "Reflection at normal incidence"),
                     ("maxwell-10-reflexao-obliqua.html", "Reflexão em incidência oblíqua", "Reflection at oblique incidence"),
                     ("maxwell-11-dipolo-hertz.html", "Antena: o dipolo de Hertz", "Antenna: the Hertzian dipole"),
                 ]}),
            ]),
        ],
    ),
}


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


REF = re.compile(r'(?:src|href|data-href)="([^"#:?$]+\.(?:png|jpe?g|gif|svg|webp|mp4|webm|css|js|html))(?:[#?][^"]*)?"')


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
        top = pathlib.PurePosixPath(ref).parts[0]
        if top == "lib" and (d.parent / top) not in seen:
            # Vendored libraries (reveal.js + plugins) load assets at runtime (e.g. the
            # chalkboard plugin's img/*.png) that no src/href names: copy the whole folder.
            seen.add(d.parent / top)
            shutil.copytree(s.parent / top, d.parent / top, dirs_exist_ok=True)
        copy_deck(s.parent / ref, d.parent / ref, seen)


def names(pt, en, href, href_en=None):
    """Portuguese and English name of a topic: two links when an English deck exists, else one."""
    pt, en = html.escape(pt), html.escape(en)
    if href_en:
        return f'<a href="{href}">{pt}</a> <span class="sep">·</span> <a href="{href_en}" lang="en" class="en">{en}</a>'
    return f'<a href="{href}">{pt} <span class="sep">·</span> <span lang="en" class="en">{en}</span></a>'


for name, c in COURSES.items():
    dst = ROOT / name
    if dst.exists():
        shutil.rmtree(dst)
    src = AULAS / c["src"]
    sections, n, seen = [], 0, set()
    for mdir, (hpt, hen), topics in c["modules"]:
        rows = []
        for (pt, en), files in topics:
            rel = {}
            for kind in ("html", "pdf"):
                if kind not in files:
                    continue
                s = src / files[kind]
                rel[kind] = f"{mdir}/{s.stem if kind == 'html' and s.stem != 'main' else slug(pt)}.{kind}"
                copy_deck(s, dst / rel[kind], seen)
                n += 1
                twin = s.with_name(s.stem + ".en.html")
                if kind == "html" and twin.exists():
                    copy_deck(twin, dst / mdir / twin.name, seen)
                    rel["en"] = f"{mdir}/{twin.name}"
            if "html" in rel:
                row = names(pt, en, rel["html"], rel.get("en"))
                if "pdf" in rel:
                    row += f' <span class="muted">(<a href="{rel["pdf"]}">PDF</a>)</span>'
            else:
                row = names(pt, en, rel["pdf"]) + ' <span class="muted">(PDF)</span>'
            if files.get("parts"):  # an HTML deck split into one file per section
                base = (src / files["html"]).parent
                for f, *_ in files["parts"]:
                    copy_deck(base / f, dst / mdir / f, seen)
                row += "\n      <ol>\n" + "\n".join(
                    f'        <li>{names(p, e, f"{mdir}/{f}")}</li>' for f, p, e in files["parts"]
                ) + "\n      </ol>\n    "
            rows.append(f"    <li>{row}</li>")
        sections.append(f'<h2>{html.escape(hpt)} <span class="sep">·</span> <span lang="en" class="en">{html.escape(hen)}</span></h2>\n'
                        "<ol>\n" + "\n".join(rows) + "\n</ol>")

    tpt, ten = c["title"]
    about_pt, about_en = c["about"]
    pre_pt, pre_en = c["prereq"]
    use_pt, use_en = c["usage"]
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{c["code"]} — {html.escape(tpt)} · {html.escape(ten)}</title>
  <meta name="description" content="{c["code"]} {html.escape(tpt)} ({html.escape(ten)}), UnB/FCTE, Prof. Daniel Costa Araújo: descrição e slides por tópico, em português e em inglês.">
  <link rel="stylesheet" href="../style.css?v=7">
  <style>
    .course {{ max-width: 820px; margin: 0 auto; padding: 2rem 16px 3rem; }}
    .course ol {{ padding-left: 1.4rem; }}
    .course li {{ margin: .3rem 0; }}
    .course li ol {{ margin: .2rem 0 .4rem; }}
    .back {{ font-size: .92rem; }}
    .course .en {{ font-style: italic; }}
    .course a .en, .course h2 .en {{ opacity: .8; }}
    .course .sep {{ opacity: .5; }}
    .course h1 .en {{ display: block; font-size: .6em; font-weight: 400; margin-top: .3rem; }}
    .about {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 2rem; margin: 1.2rem 0 .5rem; }}
    .about h2 {{ margin-top: 0; font-size: 1.05rem; }}
    .about p {{ margin: .4rem 0; }}
    @media (max-width: 680px) {{ .about {{ grid-template-columns: 1fr; gap: 1rem; }} }}
  </style>
</head>
<body>
<main class="course">
  <p class="back"><a href="../#teaching">← Daniel Costa Araújo · Teaching</a></p>
  <h1 class="page-title">{c["code"]} — {html.escape(tpt)} <span lang="en" class="en">{html.escape(ten)}</span></h1>
  <p class="muted">Universidade de Brasília (UnB), Faculdade de Ciências e Tecnologias em Engenharia (FCTE). Prof. Daniel Costa Araújo.</p>

  <div class="about">
    <section>
      <h2>Sobre a disciplina</h2>
      <p>{html.escape(about_pt)}</p>
      <p><strong>Pré-requisitos:</strong> {html.escape(pre_pt)}</p>
      <p class="muted">{html.escape(use_pt)}</p>
    </section>
    <section lang="en">
      <h2>About the course</h2>
      <p>{html.escape(about_en)}</p>
      <p><strong>Prerequisites:</strong> {html.escape(pre_en)}</p>
      <p class="muted">{html.escape(use_en)}</p>
    </section>
  </div>
  <p class="muted"><strong>Bibliografia · Textbooks:</strong> {c["books"]}</p>

{chr(10).join(sections)}
</main>
</body>
</html>
"""
    (dst / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {name}/index.html ({n} topic files, {len(seen)} files copied)")
