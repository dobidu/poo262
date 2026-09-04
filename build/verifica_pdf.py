#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/verifica_pdf.py - o portão do livro impresso.

Os portões anteriores conferem o fonte. Este confere o PDF, que é o artefato
primário, e pega a classe de defeito que só nasce na composição:

  1. **travessão e meia-risca.** A regra 6.4 da voz do autor os proíbe, e o
     fonte está limpo - mas `Ligatures=TeX` no Plex Mono convertia `--` em
     meia-risca e `---` em travessão. Custou 42 meias-riscas e 6 travessões,
     e corrompeu toda opção de linha de comando do livro: `--replay` saiu
     `–replay`, e `ctest --test-dir` saiu `ctest –test-dir`. Um leitor que  (voz:permitido)
     copiasse o comando do livro receberia erro do shell.
  2. **glifo ausente.** O quadrado de tofu não é erro do XeLaTeX, é silêncio:
     `\\char"00A7#1` fez o TeX ler o dígito seguinte como hexadecimal e
     imprimir um ponto de código que não existe.
  3. **tinta fora do papel.** Sem `includemp`, o `geometry` recalculou a
     medida e pôs o campo de aferição a 199 mm da borda esquerda de um papel
     de 210 mm. Nenhum carimbo aparecia, e sem um aviso.
  4. **carimbo sobre carimbo.** `marginnote` não empilha: dois carimbos
     ancorados perto caem um sobre o outro.
  5. **linha transbordando.** Código não reflui, então transbordo é texto
     saindo da caixa, e não linha frouxa.

Uso:  python3 build/verifica_pdf.py [caminho.pdf]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "livro" / "poo-v2.pdf"
LOG = RAIZ / "build" / "tex" / "livro.log"

MM = 72 / 25.4
CAMPO_X0 = 159 * MM     # 20 mm de margem + 134 de texto + 5 de intervalo
CAMPO_X1 = 194 * MM     # até 194 mm; o papel tem 210

# As sentinelas de glifo ausente.
#
# U+FFFF é o que o XeLaTeX escreve quando nenhuma face resolvida tem o glifo,
# e ele NÃO estava aqui: o portão dizia "zero tofu" com 35 retângulos vazios
# no PDF, em 21 folhas, incluindo a folha que explica o vocabulário de caixas
# do livro com três marcadores em branco. U+FFFD e U+25A1 ficam porque outros
# caminhos os produzem.
TOFU = "\ufffe\uffff\ufffd□"

TETO_TRANSBORDO = 8


def main() -> int:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF
    if not caminho.exists():
        print(f"ERRO: {caminho} não existe - rode `make livro-pdf`")
        return 1
    try:
        import pymupdf
    except ModuleNotFoundError:
        print("pymupdf ausente: o portão do PDF não roda, e o PDF não foi conferido")
        return 1

    d = pymupdf.open(str(caminho))
    falhas = []

    # 1) travessão e meia-risca
    riscas = []
    for n, pg in enumerate(d, 1):
        t = pg.get_text()
        for m in re.finditer(r"[—–]", t):  # voz:permitido
            i = max(0, m.start() - 22)
            riscas.append((n, t[i:m.end() + 22].replace("\n", " ")))
    if riscas:
        falhas.append(f"{len(riscas)} travessão/meia-risca no PDF "
                      "(regra 6.4 proíbe as duas; suspeite de Ligatures=TeX no Mono)")
        for n, ctx in riscas[:5]:
            falhas.append(f"      pg {n}: …{ctx}…")

    # 1b) aspa de TeX literal
    #
    # O escritor LaTeX do pandoc converte `“` e `”` para `` e '' , que é a
    # representação de aspa em TeX. Com `Mapping=tex-text` desligado - e ele
    # está desligado porque convertia `--` em meia-risca - aquilo sai
    # impresso como dois graves e dois apóstrofos. Eram 82 em 32 folhas.
    ligadas = []
    for n, pg in enumerate(d, 1):
        t = pg.get_text()
        for m in re.finditer(r"``|''", t):
            i = max(0, m.start() - 20)
            ligadas.append((n, t[i:m.end() + 20].replace("\n", " ")))
    if ligadas:
        falhas.append(f"{len(ligadas)} aspa de TeX literal no PDF "
                      "(``  ou '' no lugar de “ ”)")
        for n, ctx in ligadas[:4]:
            falhas.append(f"      pg {n}: …{ctx}…")

    # 1c) aspa reta na PROSA
    #
    # A extração do DOCX deixou 152 aspas escapadas (`\\"`), e o `smart` do
    # pandoc não trata aspa escapada como aspa: elas chegavam retas ao lado
    # das curvas na mesma folha. Desescapadas, a prosa ficou 100% curva.
    #
    # A aspa reta em código FICA, e é por isso que o portão olha a FACE: um
    # literal de string em C++ se escreve com aspa reta, e são 590 delas em
    # Plex Mono. Reta em Serif ou Sans é aspa de prosa que escapou.
    retas = []
    for n, pg in enumerate(d, 1):
        for bl in pg.get_text("dict")["blocks"]:
            for ln in bl.get("lines", []):
                for sp in ln["spans"]:
                    if '"' in sp["text"] and "Mono" not in sp["font"]:
                        retas.append((n, sp["font"], sp["text"][:40]))
    if retas:
        falhas.append(f"{len(retas)} aspa reta na prosa (face sem Mono): "
                      "desescape a aspa no fonte para o `smart` do pandoc a ver")
        for n, f, txt in retas[:4]:
            falhas.append(f"      pg {n} [{f}]: {txt!r}")

    # 2) glifo ausente
    tofu = [(n, pg.get_text().count(c))
            for n, pg in enumerate(d, 1) for c in TOFU if c in pg.get_text()]
    if tofu:
        falhas.append(f"glifo ausente em {len(tofu)} páginas: {tofu[:6]}")

    # 3) tinta fora do papel, e campo de aferição dentro dele
    largura = d[0].rect.width
    fora = [(n, round(b[2]))
            for n, pg in enumerate(d, 1) for b in pg.get_text("blocks")
            if b[4].strip() and b[2] > largura - 4]
    if fora:
        falhas.append(f"{len(fora)} blocos de texto tocando a borda do papel: {fora[:5]}")

    # 4) carimbo sobre carimbo
    colisoes = []
    for n, pg in enumerate(d, 1):
        bs = [b for b in pg.get_text("blocks") if b[4].strip()]
        campo = [b for b in bs if b[0] >= CAMPO_X0 - 6]
        for i, a in enumerate(campo):
            for b in campo[i + 1:]:
                if not (b[2] < a[0] or b[0] > a[2] or b[3] < a[1] or b[1] > a[3]):
                    colisoes.append((n, a[4].strip()[:24], b[4].strip()[:24]))
    if colisoes:
        falhas.append(f"{len(colisoes)} sobreposições no campo de aferição")
        for n, x, y in colisoes[:5]:
            falhas.append(f"      pg {n}: {x!r} sobre {y!r}")

    # 5) transbordo, do log do XeLaTeX
    transbordos = 0
    if LOG.exists():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        transbordos = len(re.findall(r"^Overfull \\hbox", log, re.M))
        if transbordos > TETO_TRANSBORDO:
            falhas.append(f"{transbordos} linhas transbordando (teto: {TETO_TRANSBORDO})")

    carimbos = sum(1 for pg in d if "aferido por" in pg.get_text())
    if falhas:
        print("── PDF REPROVADO")
        for f in falhas:
            print("   " + f)
        return 1
    print(f"pdf OK: {d.page_count} páginas · {carimbos} com carimbo de aferição · "
          f"{transbordos} transbordos · zero travessão, zero tofu, "
          "nada fora do papel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
