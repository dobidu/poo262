#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/verifica_numeros.py - o material não pode afirmar número que o código nega.

Confere as afirmações numéricas do site e do mapa contra `conteudo/medidas.py`,
que `build/medir_deriva.py` gera a partir do Deriva compilado.

Existe por três erros reais, todos encontrados por revisão e não por este
portão - que é justamente o motivo de ele existir:

  · o comentário de `celula.hpp` dizia "15 KB contra 23 KB" onde são 23 e 30;
  · o interativo de posse dizia 96 bytes vazados onde são 160;
  · a trilha anunciava 24 testes onde o portão já rodava 26.

Uso:  python3 build/verifica_numeros.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "conteudo"))

try:
    from medidas import MEDIDAS
except ModuleNotFoundError:
    print("ERRO: conteudo/medidas.py não existe. Rode: make medidas")
    sys.exit(1)
import mapa  # noqa: E402

S = MEDIDAS["sizeof"]

# (arquivo, o que tem de aparecer, o que NÃO pode aparecer, por quê)
AFIRMACOES = [
    ("poo/js/pecas.js", [str(MEDIDAS["ciclo_bytes"])], ["96 B", "96 bytes"],
     "o vazamento do ciclo de shared_ptr, medido em testes/test_posse.cpp"),
    ("poo/js/pecas.js", [f'{S["celula"]} B', f'{S["celula_ingenua"]} B'], [],
     "os dois sizeof de celula, travados por static_assert em celula.hpp"),
    ("poo/js/pecas.js", [f'{S["entidade"]} B', f'{S["entidade_simples"]} B'], [],
     "o objeto com e sem vptr, travados em leiaute.hpp"),
    ("poo/js/pecas.js", [f'{S["drone_com_carga"]} B'], [],
     "a derivada com dado próprio, travada em leiaute.hpp"),
    ("exemplos/deriva/include/deriva/celula.hpp",
     ["23 KB", "30 KB"], ["15 KB"],
     "1920 células a 12 e a 16 bytes"),
    ("poo/js/pecas.js", ["não-especificado"],
     ["deixa a origem intacta", "NÃO ESVAZIA", "não esvazia"],
     "o estado da origem depois do move, medido em testes/test_move_string.cpp: "
     "nesta libstdc++ ela esvazia nos quatro casos"),
    ("build/build_site.py", ["não-especificado"],
     ["deixa a origem intacta"],
     "o mesmo, no glossário e na prosa do site"),
    ("livro/capitulos/07-a07.md",
     [f'{S["celula"]}', f'{S["celula_ingenua"]}', "23 KB", "30 KB"], ["15 KB"],
     "o capítulo do leiaute em memória"),
]

# Prosa que anuncia a contagem de testes. Não dá para enumerar toda contagem
# obsoleta possível, então a regra é a inversa: nestes arquivos, TODA
# ocorrência de "N testes" tem de ser a medida - ou trazer a marca de meta.
# Foi assim que "24 testes" sobreviveu em quatro lugares depois de o ctest
# passar a 26.
PROSA_COM_CONTAGEM = (
    ["README.md", "Makefile", "exemplos/deriva/LEIA-ME.md"]
    # todos os capitulos, e nao so o 02: "31 testes" sobreviveu em tres lugares
    # do Cap. 16 porque o portao nao olhava para la.
    + sorted(str(p.relative_to(RAIZ)) for p in (RAIZ / "livro" / "capitulos").glob("*.md"))
)
MARCA_META = ("meta", "alvo", "projeç", "onde o ctest passava", "anunciava",
              # o material fala de contagens de teste que NAO sao a do ctest:
              # os quatro do LAB-02, os sete itens da rubrica, os 72 do Sintonia
              "lab-", "rubrica", "sintonia", "exercício", "exercicio")


def main() -> int:
    erros = []

    for rel, exigidos, proibidos, motivo in AFIRMACOES:
        caminho = RAIZ / rel
        if not caminho.exists():
            erros.append(f"{rel} não existe")
            continue
        texto = caminho.read_text(encoding="utf-8")
        baixo = texto.lower()
        for x in exigidos:
            if x.lower() not in baixo:
                erros.append(f"{rel}: falta “{x}” ({motivo})")
        for x in proibidos:
            if x.lower() in baixo:
                erros.append(f"{rel}: ainda contém “{x}”, que o código nega ({motivo})")

    # a rubrica: os rótulos têm de ser os mesmos nos três lugares.
    #
    # Ela já divergiu: a tabela do Cap. 04, a página do site e os comentários
    # do código com defeitos plantados numeravam os mesmos sete itens de três
    # maneiras. `conteudo/mapa.py` é a única definição, e este bloco recusa o
    # build se alguém voltar a numerar por conta própria.
    ids = {r["id"] for r in mapa.RUBRICA}
    titulos = {r["id"]: r["titulo"] for r in mapa.RUBRICA}

    for rel in ("poo/js/pecas-extra.js",
                "exemplos/deriva/revisao_ia/gerado.hpp",
                "exemplos/deriva/revisao_ia/gerado.cpp",
                "exemplos/deriva/testes/test_revisao_ia.cpp",
                "livro/capitulos/04-a04.md"):
        caminho = RAIZ / rel
        if not caminho.exists():
            continue
        texto = caminho.read_text(encoding="utf-8")
        usados = set(re.findall(r"\bR([1-9])\b", texto))
        fora = {f"R{n}" for n in usados} - ids
        if fora:
            erros.append(f"{rel}: usa {sorted(fora)}, que não estão em mapa.RUBRICA")

    # e o defeito plantado tem de apontar para o item que mapa.py declara
    gerado = RAIZ / "exemplos/deriva/revisao_ia/gerado.cpp"
    if gerado.exists():
        texto = gerado.read_text(encoding="utf-8")
        for numero, esperado in mapa.DEFEITOS_PLANTADOS.items():
            padrao = rf"\{{{numero}, \"({esperado})\b"
            if not re.search(padrao, texto):
                erros.append(f"revisao_ia/gerado.cpp: o defeito {numero} deveria "
                             f"apontar para {esperado} ({titulos[esperado]})")

    # prosa: nenhuma contagem de teste obsoleta
    for rel in PROSA_COM_CONTAGEM:
        caminho = RAIZ / rel
        if not caminho.exists():
            continue
        for i, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
            if any(m in linha.lower() for m in MARCA_META):
                continue
            for n in re.findall(r"\b(\d+) testes\b", linha):
                if int(n) != MEDIDAS["testes"]:
                    erros.append(f"{rel}:{i}: diz “{n} testes”, o ctest passa "
                                 f"{MEDIDAS['testes']}")

    # A trilha: a soma das medidas por versão tem de fechar com o ctest.
    #
    # Isto conferia outra coisa, e conferia errado. O campo `testes` do mapa
    # era uma PROJEÇÃO por versão, e a marca `meta` dizia "esta versão ainda
    # não existe em código" - vinte das vinte e uma estavam marcadas assim,
    # com a trilha inteira escrita desde a v0.0 até a v2.7.
    #
    # Agora o número é medido: `build/medir_deriva.py` conta os `TEST_CASE` de
    # cada arquivo de `testes/` pela declaração de versão que ele traz na
    # primeira linha, e separa os da trilha dos que medem material de aula. O
    # que este portão exige é que as duas somas fechem com o ctest, porque é
    # isso que impede uma contagem de sair da realidade sem ninguém ver.
    por_v = MEDIDAS.get("testes_por_versao", {})
    por_a = MEDIDAS.get("testes_por_aula", {})
    if not por_v:
        erros.append("medidas.py sem `testes_por_versao` - rode `make medidas`")
    else:
        soma = sum(por_v.values()) + sum(por_a.values())
        esperado = MEDIDAS.get("testes_deriva", MEDIDAS["testes"])
        if soma != esperado:
            erros.append(f"a soma por versão ({sum(por_v.values())}) mais a por "
                         f"aula ({sum(por_a.values())}) dá {soma}, e o ctest passa "
                         f"{esperado} fora dos laboratórios. Rode `make medidas`")
        fantasma = [v for v in por_v if not any(t["v"] == v for t in mapa.TRILHA)]
        if fantasma:
            erros.append(f"testes declarados para versão que a trilha não tem: "
                         f"{fantasma}")

    # A contagem de trechos nos documentos de projeto.
    #
    # `README.md`, `PRODUCT.md` e `DESIGN.md` afirmam quantos trechos o
    # material publica, e os três já ficaram velhos: o PRODUCT dizia 152 e o
    # DESIGN 147 depois de os quatro diagramas entrarem por âncora. Nada os
    # media, porque `AFIRMACOES` cobre o material e não os documentos que
    # descrevem o projeto - e é justamente neles que o número aparece solto.
    try:
        from codigo_deriva import CODIGO as _COD
    except ModuleNotFoundError:
        _COD = {}
    if _COD:
        n_trechos = len(_COD)
        for rel in ("README.md", "PRODUCT.md", "DESIGN.md"):
            caminho = RAIZ / rel
            if not caminho.exists():
                continue
            for m in re.finditer(r"\b(\d+)\s+(?:trechos|amostras)\b",
                                 caminho.read_text(encoding="utf-8")):
                if int(m.group(1)) != n_trechos:
                    erros.append(f"{rel}: diz “{m.group()}”, e "
                                 f"`extrair_codigo.py` publica {n_trechos}")

    # Colchete angular comido pelo HTML do v1.
    #
    # O site v1 deixava `<...>` sem escapar dentro de bloco de código, e o
    # navegador os engolia como marcação. A extração herdou o estrago, e o
    # material chegou a imprimir `#include` sem cabeçalho, `std::vector v` sem
    # argumento e, num caso, uma linha inteira fundida na seguinte. Código
    # impresso que não compila é pior que código ausente: o estudante o digita.
    import importlib.util as _u
    COMIDO = [
        (re.compile(r"#include\s*$", re.M), "#include sem cabeçalho"),
        (re.compile(r"\b(std::)?(vector|map|set|unique_ptr|shared_ptr|weak_ptr"
                    r"|optional|variant|pair|array|function|tuple)\s+[a-z_]\w*"
                    r"\s*[=;,)]"), "template sem argumento de tipo"),
        (re.compile(r"\b(static_cast|dynamic_cast|reinterpret_cast|const_cast"
                    r"|std::get)\s*\("), "cast sem argumento de tipo"),
    ]
    for arq in sorted((RAIZ / "conteudo" / "aulas").glob("*.py")):
        spec = _u.spec_from_file_location("aula", arq)
        mod = _u.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for sl in mod.AULA.get("slides", []):
            for b in sl["blocos"]:
                txt = b.get("codigo") or b.get("html") or ""
                for rx, rot in COMIDO:
                    for m in rx.finditer(txt):
                        erros.append(f"conteudo/aulas/{arq.name} [{sl['id']}]: "
                                     f"{rot} - {m.group().strip()[:40]!r} "
                                     "(colchete comido pelo HTML do v1)")

    if erros:
        for e in erros:
            print("NÚMERO ERRO:", e)
        print(f"\n{len(erros)} afirmação(ões) que o código não sustenta.")
        return 1

    print(f"números OK: {len(AFIRMACOES)} afirmações conferidas contra o Deriva "
          f"{MEDIDAS['versao']} ({MEDIDAS['testes']} testes, vptr {MEDIDAS['vptr']} B, "
          f"ciclo {MEDIDAS['ciclo_bytes']} B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
