#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/normaliza_tipografia.py - aplica a regra 6.4 uma vez, em tudo que é autoral.

Regra dura do padrão editorial: nunca travessão "—" nem meia-risca "–"; hífen
"-", espaçado " - " quando faz função de aparte. O material gerado a violava em
mais de mil e novecentos lugares, porque foi escrito antes de a regra estar
conhecida.

Isto é conserto pontual, não parte do build: depois de rodar uma vez, o portão
`build/verifica_voz.py` é que impede a reincidência. Textos derivados de
`legado/` são normalizados na extração, não aqui - `legado/` é somente leitura.

Uso:  python3 build/normaliza_tipografia.py [--conferir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

ALVOS = ("poo/js/*.js", "poo/css/*.css",
         "conteudo/mapa.py", "conteudo/trechos.py",
         "build/*.py", "build/*.js",
         "exemplos/deriva/include/deriva/*.hpp", "exemplos/deriva/src/*.cpp",
         "exemplos/deriva/testes/*.cpp", "exemplos/deriva/variantes/*/*.cpp",
         "exemplos/deriva/variantes/*/*.md", "exemplos/deriva/*.md",
         "exemplos/deriva/CMakeLists.txt", "exemplos/deriva/Makefile",
         "README.md", "Makefile", ".claude/agents/*.md")

# Os documentos de plano do autor são ENTRADA, como `legado/`: o pipeline lê,
# não reescreve. (Na primeira execução o glob "*.md" da raiz os pegou por
# engano; daí a lista explícita.)
PULAR = ("build/verifica_voz.py", "build/normaliza_tipografia.py",
         "HANDOFF_POO_v2.md", "PLANO-LIVRO-POO-v2.md",
         "PLANO-MATERIAL-POO-v2.md", "PLANO_DE_ENSINO_POO_v2.md")


PERMITIDO = "voz:permitido"


def normalizar(texto: str) -> str:
    """Traço em função de aparte vira " - "; o resto vira "-".

    A linha marcada com `voz:permitido` fica INTACTA, e a escotilha não é
    conveniência: há quatro linhas em `build/verifica_pdf.py` que precisam
    conter o travessão e a meia-risca para poder detectá-los no PDF, e uma no
    README que nomeia a regra ao explicá-la. Sem esta guarda, rodar o
    normalizador reescrevia justamente as linhas do portão que depende dos
    caracteres literais - e o portão passaria a não achar nada.

    É a mesma marca que `build/verifica_voz.py` respeita, e pela mesma razão.
    """
    return "\n".join(l if PERMITIDO in l else _linha(l)
                      for l in texto.split("\n"))


def _linha(texto: str) -> str:
    t = texto
    # já espaçado nos dois lados: troca só o caractere
    t = re.sub(r" [—–] ", " - ", t)
    # aberto/fechado sem espaço, ou colado a uma das pontas
    t = re.sub(r"(?<=\S)[—–](?=\S)", " - ", t)
    t = re.sub(r"(?<=\S)[—–] ", " - ", t)
    t = re.sub(r" [—–](?=\S)", " - ", t)
    # início de linha ou sobrou solto
    t = re.sub(r"^([ \t]*)[—–][ \t]*", r"\1- ", t, flags=re.M)
    t = t.replace("—", "-").replace("–", "-")
    # a troca pode ter criado espaço duplo dentro da linha
    t = re.sub(r"(?<=\S)  +- ", " - ", t)
    t = re.sub(r" -   +(?=\S)", " - ", t)
    return t


def main() -> int:
    conferir = "--conferir" in sys.argv
    mudados, ocorrencias, protegidos = 0, 0, 0
    for padrao in ALVOS:
        for p in sorted(RAIZ.glob(padrao)):
            rel = str(p.relative_to(RAIZ))
            if not p.is_file() or rel in PULAR:
                continue
            try:
                antes = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "—" not in antes and "–" not in antes:
                continue
            depois = normalizar(antes)
            if depois == antes:
                # tem o caractere, e ele está sob escotilha: nada a fazer
                protegidos += 1
                continue
            # quantos de fato mudam, e não quantos existem: a linha marcada
            # com `voz:permitido` conta o caractere e não conta a mudança, e
            # relatar a ocorrência fazia o portão parecer sujo estando limpo
            n = sum(1 for a, b in zip(antes, depois) if a != b)
            n = max(n, abs(len(antes) - len(depois)))
            ocorrencias += n
            mudados += 1
            if not conferir:
                p.write_text(depois, encoding="utf-8")
            print(f"  {rel}: {n}")
    print(f"{'conferido' if conferir else 'normalizado'}: "
          f"{ocorrencias} traço(s) a trocar em {mudados} arquivo(s)"
          + (f" · {protegidos} arquivo(s) com traço sob `voz:permitido`"
             if protegidos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
