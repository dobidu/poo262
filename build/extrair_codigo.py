#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/extrair_codigo.py - exemplos/deriva/ → conteudo/codigo_deriva.py

Extrai, por âncora de texto, os trechos declarados em `conteudo/trechos.py`.
Falha se uma âncora não existir mais: material apontando para código que já
não existe é pior que material sem código.

Uso:  python3 build/extrair_codigo.py [--conferir]
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "conteudo"))
import trechos as T  # noqa: E402

# `.mmd` entra aqui, e não como caso especial: o diagrama passa a ser trecho
# extraído como qualquer outro, com âncora e portão. Sem esta linha o bloco
# saía rotulado `cpp`, e um `classDiagram` com realce de C++ é ruído.
LINGUAGEM = {".cpp": "cpp", ".hpp": "cpp", ".h": "cpp", ".mmd": "mermaid",
             ".txt": "cmake", "": "make", ".cmake": "cmake"}


def linguagem_de(caminho: Path) -> str:
    if caminho.name == "CMakeLists.txt":
        return "cmake"
    if caminho.name == "Makefile":
        return "make"
    return LINGUAGEM.get(caminho.suffix, "cpp")


def comentario_acima(linhas: list, i: int) -> int:
    """Índice da primeira linha do bloco de comentário imediatamente acima."""
    j = i
    while j > 0:
        anterior = linhas[j - 1].strip()
        if anterior.startswith(("//", "#", "///")) or (
                anterior.startswith("*") or anterior.endswith("*/")):
            j -= 1
        else:
            break
    return j


def recortar(t: dict) -> tuple[str, str, int]:
    caminho = RAIZ / t["arquivo"]
    if not caminho.exists():
        raise SystemExit(f"ERRO: {t['id']}: {t['arquivo']} não existe")
    linhas = caminho.read_text(encoding="utf-8").splitlines()

    inicio = next((i for i, l in enumerate(linhas) if t["de"] in l), None)
    if inicio is None:
        raise SystemExit(f"ERRO: {t['id']}: âncora de início não encontrada em "
                         f"{t['arquivo']}: {t['de']!r}")

    if t.get("comentario"):
        inicio = comentario_acima(linhas, inicio)

    if not t["ate"]:
        # sem âncora de fim: até a primeira linha em branco depois do corpo
        fim = inicio
        for i in range(inicio + 1, len(linhas)):
            if not linhas[i].strip():
                break
            fim = i
    else:
        alvo = t["ate"].strip()
        fim = None
        for i in range(inicio + 1, len(linhas)):
            if linhas[i].strip() == alvo or (len(alvo) > 12 and alvo in linhas[i]):
                fim = i
                break
        if fim is None:
            raise SystemExit(f"ERRO: {t['id']}: âncora de fim não encontrada em "
                             f"{t['arquivo']}: {t['ate']!r}")

    corte = linhas[inicio:fim + 1]
    # remove a indentação comum: o trecho não herda a coluna do arquivo
    indentes = [len(l) - len(l.lstrip()) for l in corte if l.strip()]
    corta = min(indentes) if indentes else 0
    corte = [l[corta:] if l.strip() else "" for l in corte]
    return "\n".join(corte).rstrip(), linguagem_de(caminho), inicio + 1


CABECA = '''# -*- coding: utf-8 -*-
"""GERADO por build/extrair_codigo.py - não edite.

Trechos extraídos de `exemplos/deriva/`, que compila com
`-std=c++17 -Wall -Wextra -Wpedantic` e passa `make verifica`.
Para mudar um trecho, mude o CÓDIGO - não este arquivo.

{resumo}
"""

CODIGO = '''


def main():
    conferir = "--conferir" in sys.argv
    diverge = False
    saida = {}
    for t in T.TRECHOS:
        codigo, lang, linha = recortar(t)
        saida[t["id"]] = {
            "aula": t["aula"], "lang": lang, "codigo": codigo,
            "legenda": t["legenda"], "nota": t["nota"],
            "arquivo": t["arquivo"], "linha": linha,
            "quebrado_de_proposito": bool(t.get("quebrado")),
        }

    por_aula = {}
    for k, v in saida.items():
        por_aula.setdefault(v["aula"], []).append(k)
    resumo = " · ".join(f"aula {a:02d}: {len(v)}" for a, v in sorted(por_aula.items()))

    corpo = "{\n"
    for k, v in saida.items():
        corpo += f"    {k!r}: {{\n"
        for campo in ("aula", "lang", "legenda", "nota", "arquivo", "linha",
                      "quebrado_de_proposito"):
            corpo += f"        {campo!r}: {v[campo]!r},\n"
        cod = v["codigo"].replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        # trecho que termina em " colidiria com o delimitador de fechamento;
        # uma quebra de linha resolve, e o .rstrip() da leitura a descarta.
        if cod.endswith('"'):
            cod += "\n"
        corpo += f'        \'codigo\': """\\\n{cod}""",\n'
        corpo += "    },\n"
    corpo += "}\n"

    texto = CABECA.format(resumo=resumo) + corpo
    alvo = RAIZ / "conteudo" / "codigo_deriva.py"
    if conferir:
        antes = alvo.read_text(encoding="utf-8") if alvo.exists() else ""
        print(f"conferido: {len(saida)} trechos, "
              f"{'DIVERGE' if antes != texto else 'igual'}")
        diverge = antes != texto
        return 0
    alvo.write_text(texto, encoding="utf-8")
    linhas_tot = sum(v["codigo"].count("\n") + 1 for v in saida.values())
    print(f"código: {len(saida)} trechos · {linhas_tot} linhas · "
          f"{len(por_aula)} aulas · {resumo}")
    # Em `--conferir`, divergência REPROVA.
    #
    # Estes três terminavam em `return 0` mesmo tendo detectado desvio, e
    # `make verifica` imprimia "portões OK" logo abaixo de "DIVERGE". Um
    # portão que relata e não recusa deixa passar exatamente o que ele existe
    # para pegar: saída gerada editada à mão, ou gerador que mudou e saída que
    # ficou velha. Foi o que aconteceu quando o cabeçalho do extrator mudou.
    if conferir and diverge:
        print("  reprovado: rode `python3 build/extrair_codigo.py` "
              "para regravar conteudo/codigo_deriva.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
