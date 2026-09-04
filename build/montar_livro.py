#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/montar_livro.py - livro/capitulos + livro/anexos → livro/livro.md e .docx

Separado da extração de propósito. `build/extrair_livro.py` recorta o DOCX e
semeia; a partir daí os capítulos são escritos à mão e pelo escriba de voz, e
reextrair não pode sobrescrevê-los. Este script só junta o que existe.

Relata, capítulo por capítulo, se ele ainda é a semente crua do v1 ou se já
foi trabalhado - a diferença é o mapa do que falta no livro.

Uso:  python3 build/montar_livro.py [--docx]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
sys.path.insert(0, str(RAIZ / "build"))
sys.path.insert(0, str(RAIZ / "conteudo"))
import mapa       # noqa: E402
import trechos    # noqa: E402
from comum import reinjetar_codigo  # noqa: E402

try:
    from codigo_deriva import CODIGO
except ModuleNotFoundError:      # ainda não rodou build/extrair_codigo.py
    CODIGO = {}


def ordem() -> list:
    itens = ["capitulos/00-prefacio.md"]
    itens += [f"capitulos/{a['n']:02d}-{a['slug']}.md" for a in mapa.AULAS]
    itens += ["anexos/A-concepts-ranges.md", "anexos/B-referencia-c17.md",
              "anexos/C-deriva-20-versoes.md", "anexos/glossario.md",
              "anexos/referencias.md"]
    return itens


def main() -> int:
    partes, faltando, crus, trabalhados, reinjetados = [], [], [], [], []

    for rel in ordem():
        vivo = LIVRO / rel
        if not vivo.exists():
            faltando.append(rel)
            continue
        txt = vivo.read_text(encoding="utf-8")

        # A seção de código é gerada, e o capítulo é escrito à mão: reinjetar a
        # cada montagem é o que impede a versão antiga de ficar congelada aqui
        # depois de o trecho mudar em `conteudo/trechos.py`.
        n_aula = None
        # `00-prefacio.md` casava com o padrão e virava "aula 0", que o mapa
        # define como o Anexo A: o prefácio recebia os trechos de C++20 do
        # anexo, e a folha 3 do livro abria com uma prancha de `std::views`.
        # O prefácio não tem aula, e não tem seção de código.
        if (rel.startswith("capitulos/") and rel[10:12].isdigit()
                and rel != "capitulos/00-prefacio.md"):
            n_aula = int(rel[10:12])
        elif rel == "anexos/A-concepts-ranges.md":
            n_aula = 0     # o Anexo A é a "aula 0" no mapa, e tem trechos próprios
        if n_aula is not None and CODIGO:
            novo, mudou = reinjetar_codigo(txt, n_aula, trechos, CODIGO)
            if mudou:
                vivo.write_text(novo, encoding="utf-8")
                txt = novo
                reinjetados.append(rel)

        partes.append(txt.strip() + "\n")

        cru = LIVRO / "extraido" / rel
        if cru.exists() and cru.read_text(encoding="utf-8") == txt:
            crus.append(rel)
        else:
            trabalhados.append(rel)

    if faltando:
        for f in faltando:
            print("FALTA:", f)
        print("rode `make semear-livro` para semear a partir do extraído")
        return 1

    cabeca = ["% Programação Orientada a Objetos em C++",
              f"% {mapa.AUTOR}",
              f"% UFPB · Centro de Informática · {mapa.SEMESTRE}", ""]
    montado = "\n\n".join(cabeca + partes)
    (LIVRO / "livro.md").write_text(montado, encoding="utf-8")

    if "--docx" in sys.argv:
        subprocess.run(["pandoc", str(LIVRO / "livro.md"), "--toc", "--toc-depth=2",
                        "-o", str(LIVRO / "poo-v2.docx")], check=True)

    # o que ainda é semente crua é o trabalho que falta, e vale ver por nome
    paginas = len(montado) // 2800   # ~2800 caracteres por página no gabarito
    print(f"livro montado: {len(partes)} arquivos · {len(montado) // 1024} KB · "
          f"~{paginas} páginas estimadas")
    print(f"  trabalhados: {len(trabalhados)} · ainda semente crua do v1: {len(crus)}"
          + (f" · seção de código reinjetada em {len(reinjetados)}" if reinjetados else ""))
    if crus:
        nomes = [c.split("/")[-1].replace(".md", "") for c in crus]
        print("  " + ", ".join(nomes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
