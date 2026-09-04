#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/medir_fontes.py - as fontes de verdade → conteudo/glifos.py

Lê a cobertura real de cada face declarada e grava a tabela que
`build/verifica_fontes.py` usa para recusar glifo sem fonte.

Por que não ler os `.woff2` do repositório: o decodificador precisa da extensão
Brotli, que não está instalável neste ambiente. Os `.ttf` do mesmo lançamento
do IBM Plex têm a mesma cobertura, então este script os busca num diretório
temporário, mede, e grava o resultado - que fica no repositório e faz o portão
rodar sem rede.

Também regera `poo/assets/fontes/DerivaGeometricos.ttf`, o subconjunto de nove
glifos geométricos que nenhuma família Plex cobre.

Uso:  python3 build/medir_fontes.py [--sem-rede]
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "poo" / "assets" / "fontes"
PLEX = "https://cdn.jsdelivr.net/gh/IBM/plex@v6.4.0"

FAMILIAS = {
    "IBM Plex Mono": ("IBM-Plex-Mono", "IBMPlexMono-Regular"),
    "IBM Plex Serif": ("IBM-Plex-Serif", "IBMPlexSerif-Regular"),
    "IBM Plex Sans": ("IBM-Plex-Sans", "IBMPlexSans-Regular"),
}

# os que o material precisa e o Plex não tem. O 0x25C1 entrou com o livro: a
# seta de generalização da UML se escreve `◁──`, e o triângulo vazado
# apontando à esquerda é o glifo certo, não um `◀` virado por conveniência.
GEOMETRICOS = [0x25B2, 0x25B3, 0x25B6, 0x25B7, 0x25B8, 0x25BC, 0x25C0, 0x25C1,
               0x25C6, 0x25C7]
ORIGEM_GEO = Path("/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf")


def cobertura(caminho: Path) -> set:
    f = TTFont(str(caminho))
    c = set()
    for t in f["cmap"].tables:
        c |= set(t.cmap.keys())
    return c


def avanco(caminho: Path) -> float:
    f = TTFont(str(caminho))
    upm = f["head"].unitsPerEm
    nome = f.getBestCmap().get(0x20) or f.getBestCmap().get(0x25B2)
    return round(f["hmtx"][nome][0] / upm, 4)


def faixas(pontos: set) -> list:
    """Comprime o conjunto em faixas, para o arquivo gerado ficar legível."""
    out, atual = [], None
    for c in sorted(pontos):
        if atual and c == atual[1] + 1:
            atual[1] = c
        else:
            if atual:
                out.append(tuple(atual))
            atual = [c, c]
    if atual:
        out.append(tuple(atual))
    return out


def gerar_geometricos() -> Path:
    alvo = FONTES / "DerivaGeometricos.ttf"
    if not ORIGEM_GEO.exists():
        print(f"aviso: {ORIGEM_GEO} não existe; mantendo o subconjunto atual")
        return alvo
    opts = subset.Options()
    opts.drop_tables += ["DSIG"]
    opts.name_IDs = [1, 2, 3, 4, 6]
    opts.notdef_outline = True
    fonte = subset.load_font(str(ORIGEM_GEO), opts)
    s = subset.Subsetter(options=opts)
    s.populate(unicodes=GEOMETRICOS)
    s.subset(fonte)

    # O nome interno tem de dizer a verdade.
    #
    # O subsetter preserva o nome da fonte de origem, então o suplemento saía
    # do build chamando-se "Noto Sans Mono", e o PDF o declarava assim. Uma
    # revisão de fim leu a lista de faces embutidas e concluiu, com razão, que
    # o livro usava uma quarta família fora das três que o desenho declara -
    # quando são 5 KB com dez glifos, gerados aqui. Num livro cuja tese é que
    # todo número traz onde foi aferido, a fonte também diz de onde veio.
    NOME = "Deriva Geometricos"
    for reg in fonte["name"].names:
        if reg.nameID in (1, 3, 4, 6, 16):
            valor = {1: NOME, 3: f"{NOME}; suplemento do material de POO",
                     4: f"{NOME} Regular", 6: "DerivaGeometricos",
                     16: NOME}[reg.nameID]
            reg.string = valor.encode("utf-16-be") if reg.platformID == 3 \
                else valor.encode("latin-1")

    subset.save_font(fonte, str(alvo), opts)
    return alvo


def main() -> int:
    sem_rede = "--sem-rede" in sys.argv
    geo = gerar_geometricos()
    tabela = {}

    with tempfile.TemporaryDirectory() as tmp:
        for familia, (pasta, arquivo) in FAMILIAS.items():
            local = Path(tmp) / f"{arquivo}.ttf"
            if sem_rede:
                print(f"aviso: --sem-rede, não posso medir {familia}")
                continue
            url = f"{PLEX}/{pasta}/fonts/complete/ttf/{arquivo}.ttf"
            r = subprocess.run(["curl", "-sfL", "--max-time", "60", url,
                                "-o", str(local)])
            if r.returncode != 0 or not local.exists():
                print(f"ERRO: não baixei {familia} de {url}")
                return 1
            tabela[familia] = {"cobre": faixas(cobertura(local)),
                               "avanco": avanco(local)}

    if not tabela:
        print("ERRO: nada medido")
        return 1

    tabela["DerivaGeometricos"] = {"cobre": faixas(cobertura(geo)),
                                   "avanco": avanco(geo)}

    mono = tabela["IBM Plex Mono"]["avanco"]
    shim = tabela["DerivaGeometricos"]["avanco"]
    if abs(mono - shim) > 0.005:
        print(f"ERRO: avanço do suplemento ({shim}) não casa com o do Plex Mono "
              f"({mono}); a moldura desalinharia")
        return 1

    linhas = ['# -*- coding: utf-8 -*-',
              '"""GERADO por build/medir_fontes.py - não edite.',
              '',
              'Cobertura real de cada face declarada em poo/css/tokens.css, em faixas de',
              'pontos de código. `build/verifica_fontes.py` recusa o build se o site usar',
              'glifo que nenhuma delas cobre.',
              '',
              f'IBM Plex v6.4.0 (SIL OFL 1.1) · suplemento de {len(GEOMETRICOS)} glifos '
              f'do Noto Sans Mono (SIL OFL 1.1), avanço {shim} contra {mono} do Plex Mono.',
              '"""', '', 'FACES = {']
    for familia, d in tabela.items():
        linhas.append(f"    {familia!r}: {{")
        linhas.append(f"        'avanco': {d['avanco']!r},")
        linhas.append(f"        'cobre': [")
        for a, b in d["cobre"]:
            linhas.append(f"            (0x{a:04X}, 0x{b:04X}),")
        linhas.append("        ],")
        linhas.append("    },")
    linhas += ["}", "",
               "# trocados no código-fonte por não existirem em face nenhuma:",
               "# ⟲ → ↺ · ☰ → ▸ · ⏸ → ││",
               "SEM_COBERTURA_TROCADOS = {0x27F2: 0x21BA, 0x2630: 0x25B8, 0x23F8: None}",
               ""]
    (RAIZ / "conteudo" / "glifos.py").write_text("\n".join(linhas), encoding="utf-8")

    total = sum(b - a + 1 for d in tabela.values() for a, b in d["cobre"])
    print(f"fontes: {len(tabela)} faces medidas · {total} pontos de código cobertos · "
          f"suplemento com {len(GEOMETRICOS)} glifos, avanço {shim} = Plex Mono {mono}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
