#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/migrar_callouts.py - grid table do pandoc -> div cercada tipada.

A extração do DOCX transformou cada caixa do v1 numa grid table de uma célula
só, e trouxe o emoji do rótulo junto. Grid table não é callout: ela não diz o
tipo, não sobrevive a uma tabela de verdade dentro da caixa, e o pandoc a
renderiza como tabela em qualquer alvo.

Aqui ela vira `::: {.callout .warn}`, que é bloco estruturado: o renderizador
lê o tipo, e o rótulo e o glifo vêm de `conteudo/mapa.py` na hora de desenhar,
em vez de ficarem escritos no texto. O emoji morre com o rótulo.

Idempotente: rodar de novo em arquivo já convertido não muda um byte.

Uso:  python3 build/migrar_callouts.py [--conferir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# O rótulo escrito no v1 -> o tipo canônico. `objetivos` e `figura` não são
# callout: o primeiro é a abertura de todo capítulo e o segundo é figura, e
# tratá-los como caixa de aviso era o que fazia o livro ter sete caixas
# diferentes onde o mapa declara cinco.
TIPOS = [
    (re.compile(r"^\W*Objetivos deste (cap[íi]tulo|anexo)\W*$"), "objetivos"),
    (re.compile(r"^\W*Cuidado\W*$"),                            "callout warn"),
    (re.compile(r"^\W*Boa pr[áa]tica\W*$"),                     "callout tip"),
    (re.compile(r"^\W*Deriva\W*$"),                             "callout deriva"),
    (re.compile(r"^\W*LLM\W*$"),                                "callout llm"),
    (re.compile(r"^\W*DIAGRAMA UML\W*$"),                       "figura uml"),
]

ABRE = re.compile(r"^\+-{5,}\+$")
FECHA = re.compile(r"^\+[-=]{5,}\+$")


def classificar(rotulo: str) -> str | None:
    for rx, tipo in TIPOS:
        if rx.match(rotulo):
            return tipo
    return None


def celula(linhas: list[str]) -> list[str]:
    """As linhas de dentro da célula, desempilhadas em parágrafos.

    A grid table quebra a linha na largura da coluna, então duas linhas
    seguidas são um parágrafo só - juntar de volta é o que evita quebra dura
    no meio da frase.
    """
    cru = []
    for ln in linhas:
        if not ln.startswith("|"):
            return []
        cru.append(ln[1:].rstrip().rstrip("|").strip())

    paras, atual = [], []
    for ln in cru:
        if ln:
            atual.append(ln)
        elif atual:
            paras.append(" ".join(atual))
            atual = []
    if atual:
        paras.append(" ".join(atual))
    return paras


def converter(txt: str) -> tuple[str, int]:
    L = txt.split("\n")
    fora, i, n = [], 0, 0

    while i < len(L):
        if not ABRE.match(L[i]):
            fora.append(L[i])
            i += 1
            continue

        j = i + 1
        while j < len(L) and not FECHA.match(L[j]):
            j += 1
        if j >= len(L):
            fora.append(L[i])
            i += 1
            continue

        paras = celula(L[i + 1:j])
        rot = re.match(r"^\*\*(.+?)\*\*:?$", paras[0]) if paras else None
        tipo = classificar(rot.group(1)) if rot else None
        if not tipo:
            fora.append(L[i])
            i += 1
            continue

        corpo = paras[1:]
        # O `▸` era o marcador de lista do v1, escrito como texto. Lista de
        # verdade é o que deixa o renderizador paginar os objetivos sem cortar
        # um item no meio.
        if tipo == "objetivos":
            corpo = [re.sub(r"^[▸·\-\*]\s*", "- ", p) for p in corpo]
            corpo = ["\n".join(corpo)] if all(p.startswith("- ") for p in corpo) else corpo

        fora.append(f"::: {{.{tipo.replace(' ', ' .')}}}")
        fora.append("")
        for k, p in enumerate(corpo):
            fora.append(p)
            if k != len(corpo) - 1:
                fora.append("")
        fora.append("")
        fora.append(":::")
        n += 1
        i = j + 1

    return "\n".join(fora), n


def main() -> int:
    conferir = "--conferir" in sys.argv
    alvos = sorted((RAIZ / "livro" / "capitulos").glob("*.md")) + \
            sorted((RAIZ / "livro" / "anexos").glob("*.md"))
    total, tocados = 0, 0
    for p in alvos:
        txt = p.read_text(encoding="utf-8")
        novo, n = converter(txt)
        if n:
            total += n
            tocados += 1
            if not conferir:
                p.write_text(novo, encoding="utf-8")
    verbo = "a converter" if conferir else "convertidos"
    print(f"callouts {verbo}: {total} em {tocados} arquivos")
    return 1 if (conferir and total) else 0


if __name__ == "__main__":
    sys.exit(main())
