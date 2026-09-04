#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/verifica_fontes.py - nenhum glifo do site sem fonte que o cubra.

O idioma visual deste material é feito de caracteres: as molduras são
box-drawing de verdade, não `border`, e os marcadores semânticos (▲ falha,
✓ compila, ◇ LLM, ▸ Deriva) são glifos ao lado do rótulo, porque cor não pode
ser o único portador. Um glifo que cai em fonte do sistema chega com outro peso
e outro avanço, dentro de painel alinhado por caractere.

Este portão existe porque o defeito era real e invisível: o design importado
usava dezessete glifos que nenhuma das três famílias Plex cobre.

Uso:  python3 build/verifica_fontes.py [--tudo]
"""
from __future__ import annotations

import glob
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "conteudo"))

try:
    from glifos import FACES
except ModuleNotFoundError:
    print("ERRO: conteudo/glifos.py não existe. Rode: make fontes")
    sys.exit(1)

ALVOS = ("poo/*.html", "poo/js/*.js", "poo/css/*.css")

# o que não é glifo de página: dado embutido e nome de propriedade
IGNORAR_TRECHO = [
    re.compile(r'data:image/svg\+xml,[^"\']*'),   # o favicon inline
    re.compile(r"https?://[^\s\"'<>]+"),          # URL, inclusive o deep link do CE
]


def coberto(cp: int) -> bool:
    for d in FACES.values():
        for a, b in d["cobre"]:
            if a <= cp <= b:
                return True
    return False


def main() -> int:
    mostrar_tudo = "--tudo" in sys.argv
    usados = {}
    n_arq = 0

    for padrao in ALVOS:
        for rel in sorted(glob.glob(str(RAIZ / padrao))):
            texto = Path(rel).read_text(encoding="utf-8")
            for p in IGNORAR_TRECHO:
                texto = p.sub("", texto)
            n_arq += 1
            nome = Path(rel).name
            for ch in texto:
                if ord(ch) > 0x7F:
                    usados.setdefault(ch, set()).add(nome)

    sem_fonte = {c: v for c, v in usados.items() if not coberto(ord(c))}

    if sem_fonte:
        print(f"FONTE ERRO: {len(sem_fonte)} glifo(s) sem face que os cubra\n")
        for ch, arqs in sorted(sem_fonte.items(), key=lambda x: -len(x[1])):
            nome = unicodedata.name(ch, "sem nome")
            exemplos = ", ".join(sorted(arqs)[:3])
            print(f"  U+{ord(ch):04X}  {ch}  {nome[:44]:46s} {len(arqs)} arq  ({exemplos})")
        print("\nOu declare uma face que os cubra em poo/css/tokens.css e refaça "
              "`make fontes`, ou troque o glifo por um que o Plex já traga.")
        return 1

    faixa_geo = FACES.get("DerivaGeometricos", {}).get("cobre", [])
    geo_usados = [c for c in usados
                  if any(a <= ord(c) <= b for a, b in faixa_geo)]
    print(f"fontes OK: {len(usados)} glifos não-ASCII em {n_arq} arquivos, todos "
          f"cobertos · {len(geo_usados)} vêm do suplemento geométrico")
    if mostrar_tudo:
        for ch, arqs in sorted(usados.items()):
            print(f"  U+{ord(ch):04X} {ch} {len(arqs)} arq")
    return 0


if __name__ == "__main__":
    sys.exit(main())
