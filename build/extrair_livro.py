#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/extrair_livro.py - legado/poo.docx → livro/

Reestrutura o livro de 27 capítulos para os 26 capítulos + 3 anexos do plano
v2, com Aula N = Capítulo N (PLANO-LIVRO §1). O DOCX continua sendo a fonte
canônica desta fase; a conversão de ida é feita por pandoc.

O ponto perigoso desta migração são as três divisões - Cap. 10 em três, Cap. 11
em dois e Cap. 27 em dois. O plano é explícito: extrair ANTES de escrever, e
conferir seção por seção que cada uma encontrou capítulo. É o que este script
faz, e ele se recusa a escrever se alguma seção do v1 ficar sem destino.

Uso:  python3 build/extrair_livro.py [--docx]
      --docx  também monta livro/poo-v2.docx com pandoc
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCX = RAIZ / "legado" / "poo.docx"
LIVRO = RAIZ / "livro"
sys.path.insert(0, str(RAIZ / "conteudo"))
import mapa  # noqa: E402
try:
    import codigo_deriva                      # noqa: E402
    CODIGO_DERIVA = codigo_deriva.CODIGO
except ModuleNotFoundError:     # ainda não rodou build/extrair_codigo.py
    CODIGO_DERIVA = {}
import trechos                                # noqa: E402

# ---------------------------------------------------------------------------
# as três divisões, por SEÇÃO. "intro" é o texto antes da primeira seção.
# Uma seção listada em duas fatias vira pendência, nunca perda.
# ---------------------------------------------------------------------------
FATIAS_LIVRO = {
    (10, "raii"):      ["intro"],
    (10, "zero-tres"): ["10.1", "10.2", "10.3"],
    (10, "cinco"):     ["10.4", "10.5"],
    (11, "unique"):    ["intro", "11.1", "11.2"],
    (11, "shared"):    ["11.3", "11.4", "11.5"],
    (27, "qt"):        ["intro", "27.1", "27.2"],
    (27, "llm"):       ["27.3"],
    (20, "absorve-20"): [],          # o Cap. 20 inteiro vira o Anexo A
}

CAB_CAP = re.compile(r"^#\s+\*\*Cap[íi]tulo\s+(\d+)\s*[ - - -]+\s*(.+?)\*\*\s*$")
CAB_OUTRO = re.compile(r"^#\s+\*\*(.+?)\*\*\s*$")
CAB_SEC = re.compile(r"^##\s+\*\*(?:(\d+\.\d+)\s+)?(.+?)\*\*\s*$")


def pandoc_md() -> str:
    r = subprocess.run(["pandoc", str(DOCX), "-t", "markdown", "--wrap=none"],
                       capture_output=True, text=True, check=True)
    return tracos(r.stdout)


def tracos(s: str) -> str:
    """Regra tipográfica do autor aplicada na saída da extração.

    O `poo.docx` usa travessão nos títulos de capítulo e no corpo. Ele é fonte
    canônica e somente leitura; a conversão acontece aqui.

    O pandoc escreve travessão como `---` no markdown, e é essa forma que
    sobrevive à conversão: 169 ocorrências nos capítulos. A linha que é
    *apenas* `---` fica intacta, porque ali é régua horizontal e não traço.
    """
    s = re.sub(r"(?<=\S) --- (?=\S)", " - ", s)
    s = re.sub(r"(?<=[^\s-])---(?=[^\s-])", " - ", s)
    s = re.sub(r" [\u2014\u2013] ", " - ", s)
    s = re.sub(r"(?<=\S)[\u2014\u2013](?=\S)", " - ", s)
    s = re.sub(r"(?<=\S)[\u2014\u2013] ", " - ", s)
    s = re.sub(r" [\u2014\u2013](?=\S)", " - ", s)
    return s.replace("\u2014", "-").replace("\u2013", "-")


def fatiar(md: str):
    """Divide o markdown em capítulos e, dentro deles, em seções."""
    caps, avulsos = {}, {}
    atual_cap = None
    atual_sec = None
    for linha in md.splitlines():
        m = CAB_CAP.match(linha)
        if m:
            atual_cap = int(m.group(1))
            caps[atual_cap] = {"titulo": m.group(2).strip(),
                               "secoes": {"intro": {"titulo": "", "linhas": []}},
                               "ordem": ["intro"]}
            atual_sec = "intro"
            continue
        m = CAB_OUTRO.match(linha)
        if m and not CAB_CAP.match(linha):
            atual_cap = None
            atual_sec = m.group(1).strip()
            avulsos[atual_sec] = []
            continue
        if atual_cap is not None:
            m = CAB_SEC.match(linha)
            if m:
                num, tit = m.group(1), m.group(2).strip()
                chave = num or tit
                caps[atual_cap]["secoes"][chave] = {"titulo": tit, "linhas": []}
                caps[atual_cap]["ordem"].append(chave)
                atual_sec = chave
                continue
            caps[atual_cap]["secoes"][atual_sec]["linhas"].append(linha)
        elif atual_sec is not None:
            avulsos[atual_sec].append(linha)
    return caps, avulsos


def secoes_para(cap_v1: int, fatia: str | None, caps: dict) -> list:
    """Quais seções do capítulo v1 entram nesta fatia do v2."""
    if cap_v1 not in caps:
        return []
    todas = caps[cap_v1]["ordem"]
    if fatia and (cap_v1, fatia) in FATIAS_LIVRO:
        querer = FATIAS_LIVRO[(cap_v1, fatia)]
        return [s for s in todas if s in querer or (s == "Exercícios Propostos" and querer)]
    if any(k[0] == cap_v1 for k in FATIAS_LIVRO):
        # capítulo que se parte, mas esta aula não declarou fatia: nada vem
        return []
    return todas


def corpo(cap: dict, chaves: list) -> str:
    out = []
    for k in chaves:
        s = cap["secoes"][k]
        if s["titulo"]:
            num = f"{k} " if re.match(r"^\d+\.\d+$", k) else ""
            out.append(f"## {num}{s['titulo']}\n")
        txt = "\n".join(s["linhas"]).strip("\n")
        if txt:
            out.append(txt + "\n")
    return "\n".join(out).strip() + "\n"


def revisar(texto: str, itens: list) -> str:
    if not itens:
        return ""
    linhas = ["", "> **REVISAR - " + texto + "**", ">"]
    linhas += [f"> - {i}" for i in itens]
    return "\n".join(linhas) + "\n"


def secao_codigo(aula_n: int) -> str:
    """Os mesmos trechos que o site publica, no livro.

    "Uma fonte, dois meios": o estudante encontra no PDF exatamente o bloco
    que viu projetado, e os dois vêm do arquivo que compila - não de duas
    transcrições que divergem no terceiro semestre.
    """
    ids = [t["id"] for t in trechos.por_aula(aula_n)
           if t["id"] in CODIGO_DERIVA and not t.get("inline")]
    if not ids:
        return ""
    out = ["", "## O código, extraído do Deriva", "",
           "Todo trecho abaixo vem de `exemplos/deriva/`, que compila com "
           "`-std=c++17 -Wall -Wextra -Wpedantic` sem um aviso e passa "
           "`make verifica`. Nenhum foi digitado neste texto.", ""]
    for i in ids:
        d = CODIGO_DERIVA[i]
        aviso = " - **quebrado de propósito**" if d["quebrado_de_proposito"] else ""
        out += [f"**{d['legenda']}**{aviso}", "",
                f"`{d['arquivo']}:{d['linha']}`", "",
                "``` " + d["lang"], d["codigo"], "```", "",
                d["nota"], ""]
    return "\n".join(out)


def escrever_capitulo(a: dict, caps: dict, pend: list) -> tuple[str, dict]:
    partes = []
    origens = []
    for cap_v1 in a["cap_v1"]:
        fatia = a["fatia"][0] if a["fatia"] else None
        chaves = secoes_para(cap_v1, fatia if cap_v1 in
                             {k[0] for k in FATIAS_LIVRO} else None, caps)
        if not chaves:
            continue
        origens.append((cap_v1, chaves))
        c = caps[cap_v1]
        if len(a["cap_v1"]) > 1:
            partes.append(f"<!-- do Cap. {cap_v1} do v1: {c['titulo']} -->\n")
        partes.append(corpo(c, chaves))

    frente = [f"# Capítulo {a['n']} - {a['titulo']}", ""]
    def rotular(c, ks):
        nomes = ["abertura" if k == "intro" else k for k in ks]
        return f"Cap. {c} do v1 (" + ", ".join(nomes) + ")" if nomes else f"Cap. {c} do v1"

    proc = ", ".join(rotular(c, ks) for c, ks in origens) or "conteúdo novo"
    frente += [f"*Unidade {a['unidade']} · vem de {proc} · "
               f"aula correspondente: {a['n']:02d}"
               + (f" · Deriva {a['deriva']}" if a["deriva"] else "") + "*", ""]

    aviso = ""
    if a.get("nota_migracao"):
        aviso += revisar("mudança de estatuto nesta migração", [a["nota_migracao"]])
    if a.get("novo"):
        aviso += revisar("conteúdo novo - não existe no v1, precisa ser escrito",
                         a["novo"])
        for x in a["novo"]:
            pend.append((f"Cap. {a['n']}", f"escrever: {x}"))
    if a.get("caca_bug"):
        rot, desc = a["caca_bug"]
        aviso += revisar(f"{rot} - a variante quebrada e o roteiro entram aqui", [desc])
    if a["fatia"]:
        aviso += revisar("este capítulo é uma FATIA",
                         [f"{a['fatia'][0]}: {a['fatia'][1]}"])
        pend.append((f"Cap. {a['n']}", f"fatia {a['fatia'][0]} - conferir parágrafo "
                                       f"por parágrafo que nada ficou de fora"))
    if any(re.search(r"\bSintonia\b|audio|effect|sample", p, re.I) for p in partes):
        aviso += revisar("prosa ainda no Sintonia",
                         ["exemplos e nomes precisam migrar para o Deriva; "
                          "o domínio muda por escrita, não por substituição de palavra"])
        pend.append((f"Cap. {a['n']}", "prosa/código do Sintonia a migrar para o Deriva"))

    texto = ("\n".join(frente) + aviso + "\n" + "\n".join(partes)
             + secao_codigo(a["n"]))
    return texto, {"origens": origens}


def main():
    md = pandoc_md()
    caps, avulsos = fatiar(md)
    if len(caps) != 27:
        print(f"ERRO: o docx tem {len(caps)} capítulos, esperados 27")
        return 1

    pend = []
    escritos = {}
    usadas = {}

    for a in mapa.AULAS:
        texto, meta = escrever_capitulo(a, caps, pend)
        escritos[f"capitulos/{a['n']:02d}-{a['slug']}.md"] = texto
        for cap_v1, chaves in meta["origens"]:
            for k in chaves:
                usadas.setdefault((cap_v1, k), []).append(a["n"])

    # Anexo A - o Cap. 20 rebaixado, íntegro
    an = mapa.ANEXOS[0]
    c20 = caps[20]
    txt = (f"# Anexo A - {an['titulo']} (C++20)\n\n"
           f"*Vem do Cap. 20 do v1, íntegro · rotulado C++20 · "
           f"Deriva {an['deriva']}*\n"
           + revisar("mudança de estatuto", [an["nota"]]) + "\n"
           + corpo(c20, c20["ordem"]))
    escritos["anexos/A-concepts-ranges.md"] = txt
    for k in c20["ordem"]:
        usadas.setdefault((20, k), []).append("A")

    # Anexo B - referência rápida de C++17 (novo)
    escritos["anexos/B-referencia-c17.md"] = (
        "# Anexo B - Referência rápida de C++17\n\n"
        "*Novo. Tabela de consulta para prova e laboratório.*\n"
        + revisar("conteúdo novo - a tabela existe no site e precisa entrar aqui",
                  ["a versão canônica está em `poo/anexo-b.html`, gerada de "
                   "`build/build_site.py` (lista `C17_REF`)",
                   "o motivo de existir é aferido: o v1 se declarava C++17 em 12 "
                   "lugares e tinha zero ocorrência de string_view, ligações "
                   "estruturadas, [[nodiscard]], std::forward, std::filesystem e "
                   "std::tuple - enquanto ensinava Concepts e Ranges, que são C++20"]))
    pend.append(("Anexo B", "transcrever a referência rápida de C++17 do site"))

    # Anexo C - o Deriva
    obrig = [t for t in mapa.TRILHA if not t.get("opcional")]
    linhas = ["| versão | capítulo | entrega | conceitos | variante quebrada |",
              "|---|---|---|---|---|"]
    for t in mapa.TRILHA:
        caps_str = ", ".join(str(n) for n in t["aula"]) or "Anexo A"
        q = t["quebrada"][0] + " - " + t["quebrada"][1] if t.get("quebrada") else " - "
        linhas.append(f"| `{t['v']}`{' *(opcional, C++20)*' if t.get('opcional') else ''} "
                      f"| {caps_str} | {t['entrega']} | {t['conceitos']} | {q} |")
    escritos["anexos/C-deriva-20-versoes.md"] = (
        f"# Anexo C - O Deriva: as {len(obrig)} versões\n\n"
        f"*Novo. Cada versão com o capítulo que a introduz e as variantes "
        f"deliberadamente quebradas. Mesmo conteúdo da trilha do site - uma "
        f"fonte, dois meios.*\n\n" + "\n".join(linhas) + "\n")

    # glossário e referências, preservados e marcados para auditoria
    for rot, arq, nota in (
        ("Glossário", "anexos/glossario.md",
         "revisar: os verbetes novos da disciplina (contador `vivos`, replay "
         "determinístico, SSO, portão `make verifica`) precisam entrar"),
        ("Referências Bibliográficas", "anexos/referencias.md",
         "a bibliografia do livro NÃO foi auditada neste ciclo (PLANO-LIVRO §5). "
         "Duas correções já sabidas: autoria do Catch2 é Nash e Hořeňovský, e "
         "*Programming: Principles and Practice* está na 3ª ed., 2024. Falta "
         "acrescentar Josuttis, *C++17 - The Complete Guide*, e rodar a checagem "
         "de duplicatas")):
        if rot in avulsos:
            escritos[arq] = (f"# {rot}\n\n" + revisar("auditoria pendente", [nota])
                             + "\n" + "\n".join(avulsos[rot]).strip() + "\n")
            pend.append((rot, nota))

    if "Prefácio" in avulsos:
        escritos["capitulos/00-prefacio.md"] = (
            "# Prefácio\n\n"
            + revisar("atualizar o prefácio", [
                "o livro passou de 27 para 26 capítulos + 3 anexos",
                "o sistema-base é o Deriva, não o Sintonia",
                "o padrão-alvo é C++17, e o Cap. 20 do v1 virou o Anexo A",
                f"o semestre-alvo é {mapa.SEMESTRE}"])
            + "\n" + "\n".join(avulsos["Prefácio"]).strip() + "\n")

    # ---- portão: nenhuma seção do v1 sem destino --------------------------
    orfas = []
    for n, c in caps.items():
        for k in c["ordem"]:
            if (n, k) in usadas:
                continue
            if k == "intro" and not "\n".join(c["secoes"][k]["linhas"]).strip():
                continue
            orfas.append(f"Cap. {n} §{k} “{c['secoes'][k]['titulo'] or 'abertura'}”")
    if orfas:
        for o in orfas:
            print("ÓRFÃ:", o)
        print("nada foi escrito - corrija FATIAS_LIVRO em build/extrair_livro.py")
        return 2

    # duplicadas: seção que foi para mais de um capítulo v2
    duplas = {k: v for k, v in usadas.items() if len(v) > 1}
    for (n, k), destinos in duplas.items():
        pend.append((f"Cap. {n} §{k}",
                     f"foi para os capítulos {destinos} do v2 - separar o texto"))

    # ---- manifesto de migração -------------------------------------------
    man = ["# MIGRAÇÃO DO LIVRO - 27 capítulos → 26 + 3 anexos", "",
           "Gerado por `build/extrair_livro.py` a partir de `legado/poo.docx`.",
           "O script se recusa a escrever se alguma seção do v1 ficar sem destino;",
           "esta tabela é a prova, seção por seção, de que nenhuma ficou.", "",
           "## Destino de cada seção do v1", "",
           "| cap. v1 | seção | título | vai para |", "|---|---|---|---|"]
    for n in sorted(caps):
        c = caps[n]
        for k in c["ordem"]:
            if k == "intro" and not "\n".join(c["secoes"][k]["linhas"]).strip():
                continue
            dest = usadas.get((n, k), [])
            d = ", ".join(f"Cap. {x}" if isinstance(x, int) else f"Anexo {x}" for x in dest)
            marca = " **⚠ duas metades**" if len(dest) > 1 else ""
            man.append(f"| {n} | `{k}` | {c['secoes'][k]['titulo'] or '(abertura)'} "
                       f"| {d}{marca} |")

    man += ["", "## Orçamento de páginas", "",
            "| unidade | capítulos | páginas-alvo |", "|---|---|---|"]
    for u in mapa.UNIDADES:
        aulas = mapa.por_unidade(u["n"])
        man.append(f"| {u['n']} - {u['rot']} | {aulas[0]['n']} - {aulas[-1]['n']} "
                   f"| ~{u['paginas_livro']} |")
    total = sum(u["paginas_livro"] for u in mapa.UNIDADES) + 14
    man += [f"| anexos A - C | - | ~14 |", f"| **total** | **26 + 3** | **~{total}** |", "",
            "De 108 páginas para cerca de {}. O crescimento não vem de capítulo novo: vem "
            "da sintaxe de C++17 que falta e se distribui por dez capítulos, do bloco de "
            "instrumentação sem ferramenta externa, e das divisões - que custam páginas de "
            "moldura em cada metade.".format(total), ""]

    man += ["## Pendências", ""]
    for onde, o_que in pend:
        man.append(f"- **{onde}** - {o_que}")
    man += ["", f"**{len(pend)} pendências.**", ""]
    escritos["MIGRACAO.md"] = "\n".join(man)

    # ---- escrita em dois lugares, e o motivo importa ---------------------
    #
    # `livro/extraido/` é gerado e descartável: é o recorte cru do DOCX, e
    # existe para ser comparado. `livro/capitulos/` é O LIVRO, que passa a ser
    # escrito à mão e pelo escriba de voz - reextrair NÃO pode sobrescrevê-lo,
    # ou a reescrita de um capítulo morre no build seguinte.
    #
    # Um capítulo só é semeado a partir do extraído quando ainda não existe,
    # ou com --semear, que é explícito e destrutivo.
    semear = "--semear" in sys.argv
    novos, preservados, atualizados = 0, 0, 0

    for rel, txt in escritos.items():
        if rel == "MIGRACAO.md":
            (LIVRO / rel).write_text(txt, encoding="utf-8")
            continue

        cru = LIVRO / "extraido" / rel
        # o extraído ANTERIOR é o que diz se o capítulo vivo foi trabalhado
        anterior = cru.read_text(encoding="utf-8") if cru.exists() else None
        cru.parent.mkdir(parents=True, exist_ok=True)
        cru.write_text(txt, encoding="utf-8")

        vivo = LIVRO / rel
        if not vivo.exists():
            vivo.parent.mkdir(parents=True, exist_ok=True)
            vivo.write_text(txt, encoding="utf-8")
            novos += 1
            continue

        atual = vivo.read_text(encoding="utf-8")
        if semear:
            vivo.write_text(txt, encoding="utf-8")
            novos += 1
        elif anterior is not None and atual == anterior:
            # ainda é semente intocada: melhoria da extração pode entrar
            if txt != atual:
                vivo.write_text(txt, encoding="utf-8")
                atualizados += 1
            else:
                preservados += 1
        else:
            # trabalhado a mão ou pelo escriba: nunca sobrescrever
            preservados += 1

    n_cap = len([k for k in escritos if k.startswith("capitulos/")])
    kb = sum(len(t.encode()) for t in escritos.values()) // 1024
    print(f"livro extraído: {n_cap} capítulos + "
          f"{len([k for k in escritos if k.startswith('anexos/')])} anexos · {kb} KB · "
          f"{len(pend)} pendências · {len(duplas)} seções em duas metades · "
          f"nenhuma seção órfã")
    print(f"  livro/extraido/: reescrito · livro/: {novos} semeado(s), "
          f"{atualizados} semente(s) atualizada(s), {preservados} preservado(s)"
          + (" (--semear: sobrescrevi tudo)" if semear else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
