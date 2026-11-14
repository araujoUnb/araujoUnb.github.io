#!/usr/bin/env python3
"""Copy the FGA0092 (PriCom) HTML lecture decks into pricom/ and write pricom/index.html.

Source: ~/Documentos/UnB/Aulas/curso_pricom/Modulo*/html/*.html (self-contained decks).
Edit TOPICS to add, rename or reorder lectures, then run `python3 sync_pricom.py`.
"""
import html, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
SRC = pathlib.Path.home() / "Documentos/UnB/Aulas/curso_pricom"
DST = ROOT / "pricom"

# (module folder, module title, [(file stem, topic title), ...]) in teaching order
TOPICS = [
    ("Modulo0", "Módulo 0 — Apresentação", [
        ("apresentacao", "Apresentação da disciplina"),
    ]),
    ("Modulo1", "Módulo 1 — Análise e transmissão de sinais", [
        ("transformada_fourier", "Transformada de Fourier"),
        ("transformadas_uteis", "Transformadas de funções úteis"),
        ("propriedades_fourier", "Propriedades da transformada de Fourier"),
        ("sistemas_lti", "Transmissão através de sistemas LTI"),
        ("energia_potencia", "Energia, potência e densidades espectrais"),
        ("dft", "DFT e FFT"),
        ("banda_base_passante", "Banda básica e banda passante"),
    ]),
    ("Modulo2", "Módulo 2 — Modulações analógicas e ruído", [
        ("am_convencional", "AM convencional"),
        ("am_dsbsc", "AM DSB-SC"),
        ("am_ssb_vsb", "AM SSB e VSB"),
        ("modulacao_angular", "Modulação angular (PM e FM)"),
        ("projeto_transmissor_fm", "Projeto de um transmissor FM"),
        ("figura_de_ruido", "Figura de ruído"),
        ("desempenho_am", "Desempenho de sistemas analógicos (AM)"),
        ("desempenho_fm", "Desempenho de FM e PM"),
    ]),
    ("Modulo3", "Módulo 3 — Conversão analógico-digital", [
        ("amostragem", "Amostragem e reconstrução"),
        ("quantizacao", "Quantização"),
        ("forma_de_onda", "Codificação de forma de onda"),
        ("vocoders", "Vocoders: análise e síntese"),
        ("video", "Compressão de vídeo"),
    ]),
]

if DST.exists():
    shutil.rmtree(DST)
sections = []
for folder, mtitle, items in TOPICS:
    out = DST / folder.lower()
    out.mkdir(parents=True)
    rows = []
    for i, (stem, title) in enumerate(items, 1):
        shutil.copy2(SRC / folder / "html" / f"{stem}.html", out / f"{stem}.html")
        rows.append(f'    <li><a href="{folder.lower()}/{stem}.html">{html.escape(title)}</a></li>')
    sections.append(f"<h2>{html.escape(mtitle)}</h2>\n<ol>\n" + "\n".join(rows) + "\n</ol>")

page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FGA0092 — Princípios de Comunicação para Engenharia</title>
  <meta name="description" content="Slides por tópico da disciplina FGA0092 Princípios de Comunicação para Engenharia (UnB/FCTE), Prof. Daniel Costa Araújo.">
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
  <h1 class="page-title">FGA0092 — Princípios de Comunicação para Engenharia</h1>
  <p class="muted">Universidade de Brasília, Faculdade de Ciências e Tecnologias em Engenharia (FCTE). Prof. Daniel Costa Araújo.<br>
  Aulas interativas, uma por tópico: abrem no navegador; use as setas do teclado para avançar.</p>

{chr(10).join(sections)}
</main>
</body>
</html>
"""
(DST / "index.html").write_text(page, encoding="utf-8")
print("wrote", DST / "index.html", f"({sum(len(t[2]) for t in TOPICS)} decks)")
