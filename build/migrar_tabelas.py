#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/migrar_tabelas.py - tabela multilinha do pandoc -> tabela de pipe.

A extração do DOCX produziu 22 tabelas multilinha, cujo limite de coluna é um
DESLOCAMENTO de caractere, marcado pela régua `----- ----- -----`. Isso é
frágil por construção: qualquer reescrita da célula que mude a largura em um
caractere desloca todas as colunas seguintes, e o pandoc passa a cortar no
meio da palavra.

E foi o que aconteceu. A normalização de travessão trocou o travessão por
hífen mais espaço, o que
somou um caractere, e a tabela do Cap. 12 saiu impressa assim:

    unique_ptr<T> | Exclusiva - um único dono Nã | o Ze | ro overhead ...

"Não" partido em "Nã" e "o"; "Zero" em "Ze" e "ro". Silenciosamente: o pandoc
não avisa, porque para ele o corte por deslocamento é o formato.

A tabela de pipe não tem esse modo de falha: o limite é o `|`, e a largura da
célula é irrelevante. Este script converte, e a conversão é de mão única.

As células são reconhecidas por corrida de dois ou mais espaços, e não pelos
deslocamentos da régua - justamente porque os deslocamentos já não valem. Se
alguma linha der um número de células diferente do cabeçalho, o script
RECUSA aquela tabela e a relata, em vez de adivinhar.

Uso:  python3 build/migrar_tabelas.py [--conferir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

RX_MOLDURA = re.compile(r"^\s*-{10,}\s*$")
RX_COLUNAS = re.compile(r"^\s*-+(?:\s+-+)+\s*$")


def celulas(linha: str) -> list[str]:
    return [c.strip() for c in re.split(r"\s{2,}", linha.strip()) if c.strip()]


def converter(txt: str, nome: str, recusas: list) -> tuple[str, int]:
    L = txt.split("\n")
    fora, i, n, dentro = [], 0, 0, False

    while i < len(L):
        if L[i].lstrip().startswith("```"):
            dentro = not dentro
            fora.append(L[i])
            i += 1
            continue
        if dentro or not RX_MOLDURA.match(L[i]):
            fora.append(L[i])
            i += 1
            continue

        # moldura de cima, cabeçalho, régua de colunas, corpo, moldura de baixo
        j = i + 1
        while j < len(L) and not L[j].strip():
            j += 1
        if j >= len(L) or not L[j].strip():
            fora.append(L[i]); i += 1; continue
        cabeca = celulas(L[j])
        k = j + 1
        if k >= len(L) or not RX_COLUNAS.match(L[k]):
            fora.append(L[i]); i += 1; continue

        corpo, m = [], k + 1
        while m < len(L) and not RX_MOLDURA.match(L[m]):
            if L[m].strip():
                corpo.append(celulas(L[m]))
            m += 1
        if m >= len(L):
            fora.append(L[i]); i += 1; continue

        # a legenda vem depois da moldura de baixo, começando por ':'
        legenda, fim = "", m + 1
        if fim < len(L) and L[fim].strip().startswith(":"):
            legenda = L[fim].strip().lstrip(":").strip()
            fim += 1

        largura = len(cabeca)
        torto = [r for r in corpo if len(r) != largura]
        if torto or largura < 2:
            recusas.append((nome, cabeca, [r for r in torto][:2]))
            fora.append(L[i]); i += 1; continue

        fora.append("")
        fora.append("| " + " | ".join(cabeca) + " |")
        fora.append("|" + "|".join("---" for _ in cabeca) + "|")
        for r in corpo:
            fora.append("| " + " | ".join(r) + " |")
        if legenda:
            fora.append("")
            fora.append(f"*{legenda}*")
        fora.append("")
        n += 1
        i = fim

    return "\n".join(fora), n


def main() -> int:
    conferir = "--conferir" in sys.argv
    total, recusas = 0, []
    for p in sorted((RAIZ / "livro" / "capitulos").glob("*.md")) + \
             sorted((RAIZ / "livro" / "anexos").glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        novo, n = converter(txt, p.name, recusas)
        if n:
            total += n
            if not conferir:
                p.write_text(novo, encoding="utf-8")
    verbo = "a converter" if conferir else "convertidas"
    print(f"tabelas multilinha {verbo}: {total}")
    for nome, cabeca, torto in recusas:
        print(f"  RECUSADA em {nome}: cabeçalho de {len(cabeca)} células "
              f"{cabeca}; linha com {[len(t) for t in torto]}")
    if recusas:
        print("  (recusa é deliberada: adivinhar a coluna é o defeito que "
              "este script existe para tirar)")
    return 1 if (conferir and total) else 0


if __name__ == "__main__":
    sys.exit(main())
