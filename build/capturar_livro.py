#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/capturar_livro.py - rasteriza as páginas do PDF que servem de evidência.

Escolher a página por chute custou uma rodada de revisão: `final-prancha.png`
saiu da folha 16, que não tem prancha de código nenhuma, e a revisão parou no
portão de evidência antes de olhar o desenho.

Aqui a página é escolhida por ASSINATURA no texto extraído, e o script recusa
gravar o arquivo se a assinatura não aparecer. Evidência que não mostra o que
o nome promete custa a rodada inteira.

Uso:  build/venv/bin/python build/capturar_livro.py
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "livro" / "poo-v2.pdf"
SAIDA = RAIZ / ".impeccable" / "review"

# nome -> (o que a página tem de ter, e o que ela NÃO pode ter)
ASSINATURAS = {
    "final-capa":            (lambda t: "O QUE ESTE LIVRO AFERE" in t.upper(), None),
    "final-sumario":         (lambda t: "Sumário" in t and "1.1" in t, None),
    "final-abre-cap":        (lambda t: "CAPÍTULO" in t[:400].upper()
                              and "O QUE ESTE CAPÍTULO ENTREGA" in t.upper(), None),
    "final-carimbo":         (lambda t: "aferido por" in t, None),
    # prancha: a moldura tem `┌──┤`, e a procedência traz `:` mais dígito
    "final-prancha":         (lambda t: "┌──┤" in t and any(
                                  c.isdigit() for c in t.split("┌──┤")[1][:60])
                              and "▲" not in t.split("┌──┤")[1][:40]
                              and "aferido por" not in t
                              and "O QUE ESTE CAPÍTULO ENTREGA" not in t.upper()
                              # a prancha quebrada tem capture própria, e as
                              # duas caindo na mesma folha desperdiça uma
                              and "quebrado de propósito" not in t, None),
    # prancha quebrada de propósito: o marcador ▲ na régua
    "final-prancha-quebrada": (lambda t: "┌──┤" in t
                               and "quebrado de propósito" in t, None),
    "final-tabela-larga":    (lambda t: "Smart Pointer" in t, None),
    # a divisória de unidade: folha própria, e o texto dela é curto
    "final-unidade":         (lambda t: "UNIDADE" in t and len(t) < 500, None),
}


def main() -> int:
    try:
        import pymupdf
    except ModuleNotFoundError:
        print("pymupdf ausente - rode `make venv`")
        return 1
    if not PDF.exists():
        print(f"{PDF} não existe - rode `make livro-pdf`")
        return 1

    SAIDA.mkdir(parents=True, exist_ok=True)
    d = pymupdf.open(str(PDF))
    faltando = []

    for nome, (tem, nao) in ASSINATURAS.items():
        escolhida = None
        for i, pg in enumerate(d):
            t = pg.get_text()
            try:
                if tem(t) and (nao is None or not nao(t)):
                    escolhida = i
                    break
            except (IndexError, ValueError):
                continue
        if escolhida is None:
            faltando.append(nome)
            print(f"  SEM PÁGINA para {nome}: nenhuma casa a assinatura")
            continue
        alvo = SAIDA / f"{nome}.png"
        d[escolhida].get_pixmap(dpi=110).save(str(alvo))
        print(f"  {nome}.png <- folha {escolhida + 1}")

    if faltando:
        print(f"\nFALHOU: {len(faltando)} evidência(s) sem página: {faltando}")
        return 1
    print(f"\ncapturas OK: {len(ASSINATURAS)} folhas, cada uma conferida por "
          "assinatura no texto extraído")
    return 0


if __name__ == "__main__":
    sys.exit(main())
