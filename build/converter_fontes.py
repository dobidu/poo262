#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/converter_fontes.py - as fontes do site em formato que o XeLaTeX lê.

O site carrega WOFF2, que é o formato certo para a web e que o XeLaTeX não
abre. Aqui os mesmos arquivos viram TTF em `build/fontes-tex/`, que é
diretório GERADO: apagar e refazer não perde nada.

Converter em vez de baixar o Plex completo é deliberado. O site usa um subset,
e o livro tem de ficar no MESMO conjunto de glifos - senão um caractere que a
página desenha some da folha, ou o contrário, e `build/verifica_fontes.py`
deixaria de valer para os dois.

Precisa de `brotli` e `fonttools`, que moram no venv do projeto
(`build/venv`); o Makefile o cria.

Uso:  build/venv/bin/python build/converter_fontes.py [--conferir]
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "poo" / "assets" / "fontes"
DESTINO = RAIZ / "build" / "fontes-tex"

# O que o material usa, e que precisa ter glifo no livro impresso.
# Os dez geométricos vêm do suplemento; o resto, do Plex.
EXIGIDOS = "─│┌┐└┘├┤╭╮╰╯§·✓“”‘’…▲△▶▷▸▼◀◁◆◇"


def main() -> int:
    conferir = "--conferir" in sys.argv
    try:
        from fontTools.ttLib import TTFont
        from fontTools.ttLib.woff2 import decompress
    except ModuleNotFoundError as e:
        print(f"ERRO: {e.name} ausente - rode `make venv`")
        return 1

    DESTINO.mkdir(parents=True, exist_ok=True)
    feitos = []
    for w in sorted(ORIGEM.glob("*.woff2")):
        alvo = DESTINO / (w.stem + ".ttf")
        if not conferir and (not alvo.exists() or
                             alvo.stat().st_mtime < w.stat().st_mtime):
            with open(w, "rb") as entrada, open(alvo, "wb") as saida:
                decompress(entrada, saida)
            feitos.append(alvo.name)
        if not alvo.exists():
            print(f"FALTA: {alvo.relative_to(RAIZ)}")
            return 1

    # o suplemento geométrico já é TTF; ele só é copiado
    geo = ORIGEM / "DerivaGeometricos.ttf"
    if geo.exists():
        alvo = DESTINO / geo.name
        if not conferir and (not alvo.exists() or
                             alvo.stat().st_mtime < geo.stat().st_mtime):
            shutil.copy(geo, alvo)
            feitos.append(alvo.name)

    # cobertura: junta o cmap de todas e confere o que o material exige
    cobertos = set()
    for f in sorted(DESTINO.glob("*.ttf")):
        fonte = TTFont(str(f))
        for tabela in fonte["cmap"].tables:
            cobertos |= set(tabela.cmap.keys())
    falta = "".join(c for c in EXIGIDOS if ord(c) not in cobertos)
    if falta:
        print(f"ERRO: sem glifo para {falta!r} em nenhuma família - "
              "acrescente ao suplemento em build/medir_fontes.py")
        return 1

    n = len(list(DESTINO.glob("*.ttf")))
    print(f"fontes-tex: {n} faces · {len(cobertos)} pontos de código · "
          f"os {len(EXIGIDOS)} glifos exigidos têm cobertura"
          + (f" · convertidas: {len(feitos)}" if feitos else " · nada a fazer"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
