#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/gerar_plano_docx.py - o plano de ensino em .docx, a partir do .md.

A página `plano-de-ensino.html` oferece o plano para baixar, e o arquivo era
feito à mão. Duas consequências, as duas medidas:

  * ele ficou **17 horas atrás** do `PLANO_DE_ENSINO_POO_v2.md` que representa,
    e o site oferecia para baixar uma versão anterior do plano;
  * `make limpa` o apagava, e nada no repositório sabia refazê-lo - uma
    limpeza destruía um arquivo irrecuperável.

Agora ele é gerado, como o `.docx` do livro. O plano em markdown é do autor e
este script não o toca: ele só converte.

Uso:  python3 build/gerar_plano_docx.py [--conferir]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "PLANO_DE_ENSINO_POO_v2.md"
ALVO = RAIZ / "poo" / "plano-de-ensino.docx"


def main() -> int:
    if not ORIGEM.exists():
        print(f"ERRO: {ORIGEM.name} não existe")
        return 1
    conferir = "--conferir" in sys.argv

    if conferir:
        if not ALVO.exists():
            print(f"ERRO: {ALVO.relative_to(RAIZ)} não existe - "
                  "rode `python3 build/gerar_plano_docx.py`")
            return 1
        if ALVO.stat().st_mtime < ORIGEM.stat().st_mtime:
            print(f"ERRO: {ALVO.relative_to(RAIZ)} é mais antigo que "
                  f"{ORIGEM.name} - o site ofereceria a versão anterior")
            return 1
        print("plano .docx OK: em dia com o markdown")
        return 0

    r = subprocess.run(["pandoc", str(ORIGEM), "--toc", "--toc-depth=2",
                        "-o", str(ALVO)], capture_output=True, text=True)
    if r.returncode:
        print("pandoc falhou:", r.stderr[-600:])
        return 1
    print(f"plano .docx: {ALVO.relative_to(RAIZ)} · "
          f"{ALVO.stat().st_size // 1024} KB, de {ORIGEM.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
