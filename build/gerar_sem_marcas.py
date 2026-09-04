#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/gerar_sem_marcas.py - o cabeçalho da Aula 04 sem as marcas de defeito.

`revisao_ia/gerado.hpp` é o código que um modelo escreveu para a Aula 04: ele
compila sem um aviso, passa no teste que o próprio modelo escreveu, e tem três
defeitos plantados, um por item da rubrica. As marcas `DEFEITO n` existem para
o material, e o exercício é o estudante achá-los.

O cabeçalho prometia, em comentário, que o arquivo entregue ao estudante era
`gerado_sem_marcas.hpp`, "gerado no build". Ele não existia. A afirmação era
falsa e o exercício era impossível como descrito: o estudante recebia as
respostas escritas ao lado dos defeitos.

Aqui ele passa a existir. A remoção é conservadora: sai a linha de comentário
que começa por `DEFEITO n`, e saem as linhas de continuação dela - as que
seguem, também de comentário, sem abrir uma frase nova. Nada de código muda,
e o resultado tem de compilar igual ao original.

Uso:  python3 build/gerar_sem_marcas.py [--conferir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "exemplos" / "deriva" / "revisao_ia"
ORIGEM = DIR / "gerado.hpp"
ALVO = DIR / "gerado_sem_marcas.hpp"

RX_MARCA = re.compile(r"^(\s*)//\s*DEFEITO\s+\d+\b")
RX_TARJA = re.compile(r"^//\s*={10,}")
RX_COMENTARIO = re.compile(r"^\s*//")

CABECA = """// ===========================================================================
// GERADO por build/gerar_sem_marcas.py - não edite.
//
// É `revisao_ia/gerado.hpp` com as marcas `DEFEITO n` removidas, e é ESTE o
// arquivo que o estudante recebe na Aula 04. Os três defeitos continuam aqui,
// no mesmo lugar, e achá-los é a tarefa: cada um é um item da rubrica de
// revisão, e nenhum é erro de digitação.
//
// Para mudar o código, mude `gerado.hpp`.
// ===========================================================================

"""


def sem_marcas(txt: str) -> tuple[str, int, bool]:
    """Devolve (corpo, marcas removidas, versão revisada removida).

    Três remoções, e a terceira é a que mais importa:

    1. as linhas `// DEFEITO n` e as suas continuações;
    2. a tarja de abertura, que conta quantos defeitos são e diz que cada um é
       item da rubrica - informação do material, não do estudante;
    3. o `namespace revisado` INTEIRO, que é a versão corrigida dos três
       defeitos e vive no mesmo arquivo. Sem removê-lo, a cópia do estudante
       traria a resposta de cada defeito escrita quarenta linhas abaixo dele.
       Ela continua em `gerado.hpp`, onde `testes/test_revisao_ia.cpp` a usa.
    """
    L = txt.split("\n")
    fora, i, n = [], 0, 0
    tirou_revisado = False

    while i < len(L):
        # a tarja de abertura: do primeiro `// ===` ao segundo
        if RX_TARJA.match(L[i]) and not fora_tem_codigo(fora):
            j = i + 1
            while j < len(L) and not RX_TARJA.match(L[j]):
                j += 1
            i = j + 1
            continue

        # a versão revisada: da tarja que a anuncia até o fecho do namespace
        if L[i].startswith("namespace revisado"):
            # a tarja imediatamente acima também sai
            while fora and (RX_TARJA.match(fora[-1]) or fora[-1].startswith("//")
                            or not fora[-1].strip()):
                fora.pop()
            j = i
            while j < len(L) and not L[j].startswith("}  // namespace revisado"):
                j += 1
            i = j + 1
            tirou_revisado = True
            continue

        m = RX_MARCA.match(L[i])
        if not m:
            fora.append(L[i])
            i += 1
            continue
        n += 1
        i += 1
        while (i < len(L) and RX_COMENTARIO.match(L[i])
               and not RX_MARCA.match(L[i])
               and not re.match(r"^\s*///", L[i])
               and not RX_TARJA.match(L[i])):
            i += 1

    return "\n".join(fora), n, tirou_revisado


def fora_tem_codigo(fora: list) -> bool:
    """Já saiu código, ou ainda estamos no preâmbulo?"""
    return any(l.strip() and not l.lstrip().startswith(("//", "#", "namespace"))
               for l in fora)


def main() -> int:
    conferir = "--conferir" in sys.argv
    if not ORIGEM.exists():
        print(f"ERRO: {ORIGEM.relative_to(RAIZ)} não existe")
        return 1
    txt = ORIGEM.read_text(encoding="utf-8")
    corpo, n, tirou = sem_marcas(txt)
    if not n:
        print("ERRO: nenhuma marca `DEFEITO n` em gerado.hpp - "
              "o exercício da Aula 04 depende delas")
        return 1

    # a guarda de inclusão tem de ser própria, ou os dois cabeçalhos colidem
    corpo = corpo.replace("DERIVA_REVISAO_IA_HPP",
                          "DERIVA_REVISAO_IA_SEM_MARCAS_HPP")
    if not tirou:
        print("ERRO: o `namespace revisado` não foi encontrado em gerado.hpp - "
              "sem removê-lo, a cópia do estudante traz as respostas")
        return 1
    saida = CABECA + corpo.lstrip("\n")

    if conferir:
        antes = ALVO.read_text(encoding="utf-8") if ALVO.exists() else ""
        if antes != saida:
            print(f"ERRO: {ALVO.relative_to(RAIZ)} está desatualizado - "
                  "rode `python3 build/gerar_sem_marcas.py`")
            return 1
        print(f"sem-marcas OK: {n} marcas removidas, arquivo em dia")
        return 0

    ALVO.write_text(saida, encoding="utf-8")
    print(f"gerado_sem_marcas.hpp: {n} marcas `DEFEITO n` removidas, "
          f"tarja e `namespace revisado` fora · {len(saida.splitlines())} linhas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
