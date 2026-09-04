#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/verifica_voz.py - o detector de sinais de escrita por IA, como portão.

O detector de voz do material, em dois níveis: regras DURAS, verificáveis sem
julgamento, quebram o build; SINAIS brandos são contados e relatados, para quem
escreve decidir caso a caso. O princípio é smell test e não lista negra, e o
perfil de voz vence o detector - conectivo formal é voz legítima, não defeito.
O princípio de lá vale aqui: **smell test, não blacklist**. Nenhum sinal
isolado condena uma frase, e o perfil de voz vence o detector, nunca o
contrário - "através de", "tais" e conectivos formais são voz legítima.

Por isso há dois níveis:

  DUROS   quebram o build. São regras tipográficas e de forma, verificáveis
          sem julgamento: travessão, en-dash, paralelismo negativo.
  SINAIS  são relatados e contados, e não quebram nada. Servem para o
          agente-escriba decidir caso a caso na passada final.

Uso:
    python3 build/verifica_voz.py                 # tudo que é autoral
    python3 build/verifica_voz.py arq1 arq2 ...   # só esses
    python3 build/verifica_voz.py --sinais        # relata também os brandos
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# `legado/` é somente leitura: os sinais de lá são do material antigo, e
# apontá-los não ajuda ninguém. `build/` de C++ e `.git` ficam fora.
# `livro/extraido/` é o recorte fiel do DOCX v1, e existe para preservar os
# defeitos dele: ele é a prova, seção por seção, de que nenhuma ficou órfã na
# migração. Conferir a voz do autor ali seria conferir a voz do documento
# antigo, que não é o que se publica.
IGNORAR = ("legado/", "livro/extraido/", "exemplos/deriva/build/", ".git/",
           "poo-zip.zip",
           "conteudo/aulas/", "conteudo/codigo_deriva.py",
           # este arquivo precisa CONTER os caracteres proibidos para achá-los
           "build/verifica_voz.py", "build/normaliza_tipografia.py",
           # documentos de plano do autor: entrada, não material gerado
           "HANDOFF_POO_v2.md", "PLANO-LIVRO-POO-v2.md",
           "PLANO-MATERIAL-POO-v2.md", "PLANO_DE_ENSINO_POO_v2.md")

# escotilha para exceção legítima, uma linha por vez
PERMITIDO = "voz:permitido"

# `livro/livro.md` NÃO entra: ele é a concatenação dos capítulos e dos anexos,
# que já estão aqui, e não carrega uma linha própria. Pior, ele é montado
# DEPOIS deste portão na ordem do Makefile, então uma correção nos capítulos
# só chegava nele na passada seguinte, e o portão acusava o arquivo velho -
# o mesmo defeito de ordenação que o portão de glifos teve com o site.
# O artefato composto é conferido por `build/verifica_pdf.py`.
ALVOS = ("poo/*.html", "poo/js/*.js", "poo/css/*.css",
         "livro/capitulos/*.md", "livro/anexos/*.md",
         "conteudo/mapa.py", "conteudo/trechos.py", "conteudo/*.md",
         "build/*.py", "build/*.js",
         "exemplos/deriva/**/*.hpp", "exemplos/deriva/**/*.cpp",
         "exemplos/deriva/**/*.md", "exemplos/deriva/CMakeLists.txt",
         "*.md", "Makefile")

# ---------------------------------------------------------------------------
# DUROS - quebram o build
# ---------------------------------------------------------------------------
DUROS = [
    ("travessao", re.compile("—"),
     'travessão "—" é proibido em todos os registros (regra 6.4): use "-", '
     'espaçado " - " quando faz função de aparte'),
    ("en-dash", re.compile("–"),
     'en-dash "–" é proibido (regra 6.4): use "-"'),
    # O material PUBLICADO não carrega marcador de andaime. Decisão do autor,
    # nas palavras dele: "temos que ajeitar TUDO do livro, sem deixar NADA a
    # revisar". Marcador de pendência transfere ao leitor um trabalho que é
    # nosso, e faz o estudante duvidar do que já está pronto - e esconder o
    # marcador é pior, porque a pendência continua e ninguém a vê.
    #
    # Vale para `livro/` e `poo/`. Os relatórios internos - `conteudo/PENDENCIAS.md`,
    # `livro/MIGRACAO.md`, `README.md` - existem justamente para carregar isso,
    # e estão isentos logo abaixo.
    # CAIXA ALTA e sem `re.I`, de propósito: `\bTODO\b` sem distinguir caixa
    # casa com "todo", que é palavra comuníssima em português - a primeira
    # versão desta regra acusou 203 falsos positivos por isso. E frases como
    # "a definir" ficaram fora: em prosa portuguesa elas são legítimas, e
    # marcador de andaime de verdade vem em caixa alta.
    # O sistema-base ANTIGO.
    #
    # O material v1 era construído sobre o "Sintonia", um mini-DAW de áudio,
    # e o v2 é construído sobre o Deriva. O livro foi reescrito e o site não,
    # e a divergência sobreviveu meses porque nada a media: eram 521
    # ocorrências nas 27 páginas de aula, ao lado do código correto do Deriva
    # na mesma página. Um portão é o que impede a volta.
    #
    # `project` e `build` NÃO entram: `project(deriva LANGUAGES CXX)` é comando
    # do CMake e "sistema de build" é português técnico corrente. `effect`
    # entra só com sublinhado, para não pegar palavra inglesa em citação de
    # bibliografia.
    ("sistema-base-antigo", re.compile(
        r"\b[Ss]intonia\b|\baudio_buffer\b|\bAudioBuffer\b|\bgain_effect\b"
        r"|\bdelay_effect\b|\beffect_chain\b|\baudio_engine\b"
        r"|\bsample_rate\b|\boscillator\b|\bmixer_window\b"
        r"|\bbuffer de [áa]udio\b|\btaxa de amostragem\b"),
     "vocabulário do Sintonia, que era o sistema-base do v1: o sistema-base "
     "é o Deriva, e o material se escreve sobre ele"),

    # Tabela multilinha do pandoc: o limite de coluna é um DESLOCAMENTO de
    # caractere, e qualquer reescrita que mude a largura da célula em um
    # caractere desloca as colunas seguintes. Aconteceu: a normalização de
    # travessão somou um caractere e a tabela do Cap. 12 saiu impressa com
    # "Não" partido em "Nã" e "o". Tabela é de pipe, e o portão o exige.
    # A régua SOLTA também: ela é a moldura de topo da tabela multilinha, e
    # sobrevive quando alguém converte a tabela e esquece a linha de cima.
    # Era o caso do §20.7, que ficou com uma régua de 110 hífens pendurada
    # acima de uma tabela de pipe perfeitamente boa.
    ("regua-orfa", re.compile(r"^\s*-{10,}\s*$", re.M),
     "régua de tabela multilinha sem tabela: apague a linha"),
    ("tabela-multilinha", re.compile(r"^\s*-+(?:\s+-+)+\s*$", re.M),
     "tabela multilinha do pandoc: converta para tabela de pipe "
     "(`python3 build/migrar_tabelas.py`), cujo limite é o `|` e não a coluna"),
    ("marcador-de-andaime", re.compile(
        r"\bREVISAR\b|\bPENDENTE\b|\bTODO\b|\bFIXME\b|\[preencher\]"),
     "marcador de andaime no material publicado: resolva a pendência, não a "
     "sinalize nem a esconda"),
    ("paralelismo-negativo", re.compile(
        r"\bnão (?:se trata|é) (?:apenas|só) (?:de )?\w+,? mas\b|"
        r"\bnão (?:é|são) só\b[^.]{0,60}\bé\b", re.I),
     'paralelismo negativo ("não se trata apenas de X, mas de Y"): afirme direto'),
]

# ---------------------------------------------------------------------------
# SINAIS - relatados, nunca fatais
# ---------------------------------------------------------------------------
SINAIS = [
    ("inflar-significancia", re.compile(
        r"desempenha um papel (?:fundamental|crucial|central)|verdadeiro testemunho|"
        r"legado duradouro|de suma importância|marco decisivo", re.I),
     "diga o que a coisa faz; deixe o leitor concluir a importância"),
    ("cauda-editorializante", re.compile(
        r"ressaltando a importância|evidenciando (?:seu|sua)|consolidando-se como|"
        r"refletindo uma tendência|o que demonstra que", re.I),
     "corte a cauda; termine no fato"),
    ("transicao-de-enchimento", re.compile(
        r"\b(?:além disso|ademais|outrossim|por conseguinte|em suma|"
        r"vale (?:ressaltar|destacar|mencionar)|é importante notar)\b", re.I),
     "conectivo de enchimento: corte, ou use os conectivos-assinatura com parcimônia"),
    ("lexico-ia", re.compile(
        r"\b(?:aprimorar|aprimorad[oa]s?|robust[oa]s?|abrangentes?|vasto leque|"
        r"mergulhar fundo|paisagem|tapeçaria)\b", re.I),
     "troque por termo específico do domínio"),
    ("negrito-em-excesso", None, "mais de 6 trechos em negrito no mesmo parágrafo"),
]

TRIADE = re.compile(r"\b(\w+(?:o|a|os|as|e|es))\, (\w+(?:o|a|os|as|e|es)) e "
                    r"(\w+(?:o|a|os|as|e|es))\b")


# Relatórios internos existem para carregar pendência, e não são o material.
# `PRODUCT.md` cita o travessão e a meia-risca para NOMEAR a regra que os
# proíbe, e o detector o acusava por isso. Ele é documento de projeto, e não
# material publicado.
NAO_PUBLICADO = ("PRODUCT.md", ".impeccable/", "conteudo/PENDENCIAS.md", "livro/MIGRACAO.md", "README.md",
                 "exemplos/deriva/LEIA-ME.md", "exemplos/deriva/laboratorios/",
                 "exemplos/deriva/variantes/", "exemplos/deriva/sanitizers/",
                 ".claude/", "build/")


def publicado(rel) -> bool:
    """Material que o estudante lê: os capítulos, os anexos e o site."""
    r = str(rel)
    if any(r.startswith(x) or f"/{x}" in r for x in NAO_PUBLICADO):
        return False
    return r.startswith(("livro/capitulos/", "livro/anexos/", "livro/livro.md",
                         "poo/"))


def arquivos(argv: list) -> list:
    """Os arquivos a conferir: os do argumento, ou os ALVOS todos.

    Argumento que é DIRETÓRIO expande para os arquivos dentro dele. Antes ele
    era devolvido como caminho único, e o laço de `main` o descartava em
    silêncio: `verifica_voz.py conteudo/aulas` conferia zero arquivos e
    imprimia "OK". Um portão que passa sem olhar nada é pior que portão
    nenhum, porque ele dá confiança falsa a quem o rodou.
    """
    if argv:
        fora = []
        for a in argv:
            p = Path(a)
            if p.is_dir():
                fora += [q for q in sorted(p.rglob("*"))
                         if q.is_file() and q.suffix in (".md", ".py", ".html",
                                                         ".js", ".css")]
            else:
                fora.append(p)
        return fora
    vistos = []
    for padrao in ALVOS:
        for p in sorted(RAIZ.glob(padrao)):
            rel = str(p.relative_to(RAIZ))
            if any(rel.startswith(x) or f"/{x}" in rel for x in IGNORAR):
                continue
            if p.is_file() and p not in vistos:
                vistos.append(p)
    return vistos


def main() -> int:
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    mostrar_sinais = "--sinais" in sys.argv

    duros, sinais = [], {}
    n_arq = 0
    for p in arquivos(argv):
        try:
            texto = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        n_arq += 1
        rel = p.relative_to(RAIZ) if p.is_absolute() else p
        for i, linha in enumerate(texto.splitlines(), 1):
            if PERMITIDO in linha:
                continue
            for nome, padrao, dica in DUROS:
                # Duas regras valem só no material publicado: o marcador de
                # andaime e o vocabulário do sistema antigo. Os relatórios
                # internos existem justamente para nomeá-los.
                if (nome in ("marcador-de-andaime", "sistema-base-antigo")
                        and not publicado(rel)):
                    continue
                if padrao.search(linha):
                    duros.append((nome, f"{rel}:{i}", linha.strip()[:100], dica))
            for nome, padrao, _ in SINAIS:
                if padrao and padrao.search(linha):
                    sinais.setdefault(nome, []).append(f"{rel}:{i}")
            if TRIADE.search(linha):
                sinais.setdefault("triade", []).append(f"{rel}:{i}")

    if duros:
        por_nome = {}
        for nome, onde, trecho, dica in duros:
            por_nome.setdefault(nome, []).append((onde, trecho, dica))
        for nome, itens in por_nome.items():
            print(f"VOZ DURO [{nome}] {len(itens)} ocorrência(s) - {itens[0][2]}")
            for onde, trecho, _ in itens[:8]:
                print(f"    {onde}  {trecho}")
            if len(itens) > 8:
                print(f"    ... e mais {len(itens) - 8}")
        print(f"\n{len(duros)} violações duras em {n_arq} arquivos. "
              f"Regras duras em DUROS, sinais brandos em BRANDOS, neste arquivo.")
        return 1

    resumo = " · ".join(f"{k}:{len(v)}" for k, v in sorted(sinais.items())) or "nenhum"
    print(f"voz OK: {n_arq} arquivos, zero violação dura · sinais brandos: {resumo}")
    if mostrar_sinais:
        for nome, onde in sorted(sinais.items()):
            dica = next((d for n, _, d in SINAIS if n == nome), "tríade reflexiva de adjetivos")
            print(f"\n[{nome}] {len(onde)} - {dica}")
            for o in onde[:25]:
                print(f"    {o}")
            if len(onde) > 25:
                print(f"    ... e mais {len(onde) - 25}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
