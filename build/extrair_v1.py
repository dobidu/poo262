#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/extrair_v1.py - legado/site-v1 → conteudo/aulas/*.py

Extração determinística: roda duas vezes, dá o mesmo byte. Não reescreve
prosa, não inventa conteúdo, não descarta nada em silêncio. Onde o plano v2
parte uma página em fatias que atravessam um mesmo slide, o slide vai para as
duas fatias e a pendência é registrada - perder conteúdo calado é o risco
número um desta migração (PLANO-MATERIAL §2).

O que ele faz de fato:
  · casa cada página do v1 com a aula do v2, pelo mapa canônico;
  · separa slide, prosa, código, callout, tabela, mermaid, lista, exercício;
  · renomeia `callout-sintonia` → `deriva` e REGISTRA que a prosa dentro dele
    continua falando do Sintonia (o domínio muda por escrita humana, não por
    substituição cega de palavra);
  · marca cada trecho C++ que usa construção de C++20 e cada trecho onde o
    plano v2 exige sintaxe de C++17 que o v1 não tem;
  · emite `conteudo/aulas/aNN.py` e `conteudo/PENDENCIAS.md`.

Uso:  python3 build/extrair_v1.py [--conferir]
      --conferir  não escreve; só relata o que mudaria e as pendências.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

RAIZ = Path(__file__).resolve().parent.parent
V1 = RAIZ / "legado" / "site-v1"
# Dois destinos, e a distinção é o que protege o trabalho de reescrita.
#
# `conteudo/extraido/` é o recorte fiel do v1, sempre reescrito: ele é a prova,
# slide por slide, de que nenhum ficou órfão na migração.
# `conteudo/aulas/` é o material de verdade, e é semeado a partir do recorte
# SÓ quando o arquivo não existe ou quando ninguém o tocou desde a última
# extração. É a mesma arquitetura que `build/extrair_livro.py` já dava ao
# livro, e a falta dela aqui era uma bomba: a reescrita do site morria na
# primeira reextração, e o cabeçalho gerado se limitava a avisar "não rode
# isto de novo depois de editar".
EXTRAIDO = RAIZ / "conteudo" / "extraido"
SAIDA = RAIZ / "conteudo" / "aulas"

sys.path.insert(0, str(RAIZ / "conteudo"))
import mapa  # noqa: E402

# ---------------------------------------------------------------------------
# fatias: quais slides do v1 vão para qual fatia do v2.
# Um id marcado com "*" é COMPARTILHADO - vai para mais de uma fatia porque a
# divisão do plano cai dentro do slide. Isso gera pendência, nunca perda.
# ---------------------------------------------------------------------------
FATIAS = {
    ("unidade-2/aula10-raii-rule-of-five", "raii"):      ["intro", "llm*"],
    ("unidade-2/aula10-raii-rule-of-five", "zero-tres"): ["regra-zero", "regra-cinco*", "llm*"],
    ("unidade-2/aula10-raii-rule-of-five", "cinco"):     ["regra-cinco*", "llm*"],
    ("unidade-2/aula11-smart-pointers", "unique"):       ["intro", "unique", "llm*"],
    ("unidade-2/aula11-smart-pointers", "shared"):       ["shared-weak", "llm*"],
    ("unidade-3/aula27-qt-llms", "qt"):                  ["intro", "qobject", "separacao"],
    ("unidade-3/aula27-qt-llms", "llm"):                 ["retrospectiva", "llm"],
    # o Cap./aula 20 inteiro vira Anexo A; a Aula 19 só o referencia
    ("unidade-3/aula20-concepts-ranges", "absorve-20"):  [],
}

# páginas que se partem: os exercícios precisam ser redistribuídos à mão
PARTIDAS = {"unidade-2/aula10-raii-rule-of-five",
            "unidade-2/aula11-smart-pointers",
            "unidade-3/aula27-qt-llms"}

CALLOUT_V1_PARA_V2 = {v["classe_v1"]: k for k, v in mapa.CALLOUTS.items()}

# vocabulário do sistema-base antigo: onde aparecer, a prosa precisa de reescrita
SINTONIA = re.compile(
    r"\b(sintonia|audio_buffer|audio_source|sine_source|noise_source|gain_effect|"
    r"\beffect\b|oscilador|envelope|sample_rate|wav|daw|mixer|reverb|delay_line)\b",
    re.I)

# C++20 dentro de material cujo teto é C++17
C20 = re.compile(r"\b(concept|requires|std::ranges|std::views|co_await|co_yield|"
                 r"consteval|constinit|<=>|std::span|std::format)\b")

# as construções de C++17 que o plano v2 manda distribuir (HANDOFF §2)
C17_ALVO = {
    "std::string_view": "string_view",
    "auto [": "ligações estruturadas",
    "[[nodiscard]]": "[[nodiscard]]",
    "[[maybe_unused]]": "[[maybe_unused]]",
    "std::tuple": "std::tuple",
    "std::forward": "std::forward",
    "if constexpr": "if constexpr",
    "std::filesystem": "std::filesystem",
    "std::clamp": "std::clamp",
    "std::optional": "std::optional",
    "std::variant": "std::variant",
    "std::invoke": "std::invoke",
    "std::apply": "std::apply",
    "std::byte": "std::byte",
}


# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------
def limpar(s: str) -> str:
    """Normaliza espaço e tipografia sem tocar no conteúdo.

    `legado/` é somente leitura, então a regra tipográfica do autor - nunca
    travessão nem en-dash, hífen espaçado no lugar - é aplicada aqui, na saída
    da extração. O texto do v1 permanece intacto no lugar de origem.
    """
    s = unicodadata_normalizar(s)
    s = tracos(s)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"[ \t]{2,}", " ", s)).strip()


# Emoji que vazam da prosa do v1. O idioma visual do v2 é box-drawing e formas
# geométricas em IBM Plex Mono, e emoji não tem lugar nele - nem cobertura de
# fonte. Onde o glifo carregava sentido, ele é traduzido para o vocabulário do
# material; onde era enfeite, sai.
GLIFOS_V1 = {
    "\u2705": "\u2713",   # ✅ → ✓  compila / feito
    "\u26a0": "\u25b2",   # ⚠  → ▲  atenção
    "\u2b50": "\u00b7",   # ⭐ → ·  destaque sem peso
    "\U0001f4d0": "",      # 📐 rótulo de diagrama: sai
    "\U0001f3af": "",      # 🎯 objetivos: o rótulo já diz
    "\U0001f916": "",      # 🤖 callout de LLM: o tipo já diz
    "\U0001f4a1": "",      # 💡 dica
    "\u2139": "",          # ℹ  nota
    "\U0001f3b5": "",      # 🎵 herança do Sintonia
    "\ufe0f": "",          # seletor de variação, sempre sobra
    "\u21d2": "\u2192",    # ⇒ → →  o Plex Mono não tem a seta dupla
}


def tracos(s: str) -> str:
    for a, b in GLIFOS_V1.items():
        s = s.replace(a, b)
    s = re.sub(r" [\u2014\u2013] ", " - ", s)
    s = re.sub(r"(?<=\S)[\u2014\u2013](?=\S)", " - ", s)
    s = re.sub(r"(?<=\S)[\u2014\u2013] ", " - ", s)
    s = re.sub(r" [\u2014\u2013](?=\S)", " - ", s)
    return s.replace("\u2014", "-").replace("\u2013", "-")


def unicodadata_normalizar(s: str) -> str:
    return unicodedata.normalize("NFC", s)


# tags inline que o v1 realmente usa; qualquer outro "<" é literal esquecido
TAGS_OK = ("a", "b", "br", "code", "em", "i", "kbd", "li", "ol", "p", "span",
           "strong", "sub", "sup", "ul")
_TAG_VALIDA = re.compile(r"</?(?:%s)\b[^>]*>" % "|".join(TAGS_OK), re.I)

DEFEITOS_V1 = []


def sanear(s: str, onde: str) -> str:
    """Escapa `<` que o v1 deixou solto - `vector<T>` dentro de célula de tabela,
    por exemplo. Um `<` literal em HTML come o resto do documento no parser de
    quem valida; o v1 tinha um desses. Não é reescrita de conteúdo: é conserto
    de marcação, e cada ocorrência fica registrada."""
    saida, pos = [], 0
    for m in re.finditer(r"<", s):
        i = m.start()
        if i < pos:
            continue
        saida.append(s[pos:i])
        v = _TAG_VALIDA.match(s, i)
        if v:
            saida.append(v.group())
            pos = v.end()
        else:
            fim = s.find(">", i)
            trecho = s[i:fim + 1] if fim > -1 else s[i:]
            DEFEITOS_V1.append((onde, trecho[:40]))
            saida.append("&lt;")
            pos = i + 1
    saida.append(s[pos:])
    return "".join(saida)


def html_interno(el: Tag, onde: str = "?") -> str:
    return sanear(limpar("".join(str(c) for c in el.contents)), onde)


def texto(el) -> str:
    if isinstance(el, NavigableString):
        return tracos(str(el))
    return tracos(el.get_text(" ", strip=True))


def py_repr(v, ind=0):
    """Escreve literal Python legível e estável - o arquivo entra no git."""
    pad = "    " * ind
    if isinstance(v, str):
        if "\n" in v:
            marca = '"""'
            corpo = v.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
            return f'{marca}\\\n{corpo}{marca}'
        return repr(v)
    if isinstance(v, bool) or v is None or isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, list):
        if not v:
            return "[]"
        itens = ",\n".join(pad + "    " + py_repr(x, ind + 1) for x in v)
        return "[\n" + itens + ",\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{}"
        itens = ",\n".join(
            f"{pad}    {k!r}: {py_repr(x, ind + 1)}" for k, x in v.items())
        return "{\n" + itens + ",\n" + pad + "}"
    raise TypeError(type(v))


# ---------------------------------------------------------------------------
# extração de um slide
# ---------------------------------------------------------------------------
def extrair_blocos(corpo: Tag, pend: list, onde: str) -> list:
    blocos = []
    for filho in corpo.children:
        if isinstance(filho, NavigableString):
            if filho.strip():
                blocos.append({"tipo": "prosa", "html": limpar(str(filho))})
            continue
        if not isinstance(filho, Tag):
            continue
        cls = filho.get("class") or []

        if filho.name == "p":
            blocos.append({"tipo": "prosa", "html": html_interno(filho, onde)})

        elif filho.name in ("ul", "ol"):
            blocos.append({"tipo": "lista", "ordenada": filho.name == "ol",
                           "itens": [html_interno(li, onde) for li in filho.find_all("li", recursive=False)]})

        elif filho.name == "table":
            cab = [sanear(texto(th), onde) for th in filho.select("thead th")]
            linhas = [[html_interno(td, onde) for td in tr.find_all(["td", "th"], recursive=False)]
                      for tr in filho.select("tbody tr")]
            blocos.append({"tipo": "tabela", "cabeca": cab, "linhas": linhas})

        elif "code-block" in cls:
            pre = filho.find("pre")
            code = pre.find("code") if pre else None
            lang = "cpp"
            if code and code.get("class"):
                for c in code["class"]:
                    if c.startswith("language-"):
                        lang = c[len("language-"):]
            fonte = code.get_text() if code else (pre.get_text() if pre else "")
            legenda_el = filho.select_one(".code-caption")
            b = {"tipo": "codigo", "lang": lang,
                 "legenda": texto(legenda_el) if legenda_el else "",
                 "codigo": tracos(fonte.rstrip("\n"))}
            marcar_codigo(b, pend, onde)
            blocos.append(b)

        elif "callout" in cls:
            t = "info"
            for c in cls:
                if c in CALLOUT_V1_PARA_V2:
                    t = CALLOUT_V1_PARA_V2[c]
            tit = filho.select_one(".callout-title")
            conteudo = filho.select_one(".callout-content")
            partes = []
            if conteudo:
                for x in conteudo.children:
                    if isinstance(x, Tag) and x.name == "p":
                        partes.append(html_interno(x, onde))
                    elif isinstance(x, Tag) and x.name in ("ul", "ol"):
                        partes.append(str(x))
                    elif isinstance(x, NavigableString) and x.strip():
                        partes.append(limpar(str(x)))
            b = {"tipo": "callout", "t": t,
                 "titulo": texto(tit) if tit else "",
                 "paragrafos": [p for p in partes if p]}
            if t == "deriva":
                pend.append({
                    "tipo": "dominio",
                    "onde": onde,
                    "o_que": f"callout `sintonia` → `deriva`: “{b['titulo']}” - a prosa "
                             f"dentro dele ainda fala do sistema antigo e precisa de "
                             f"reescrita humana para o Deriva.",
                })
            blocos.append(b)

        elif "mermaid" in cls:
            blocos.append({"tipo": "mermaid", "fonte": filho.get_text().strip()})

        elif "objectives" in cls:
            blocos.append({"tipo": "objetivos",
                           "itens": [html_interno(li) for li in filho.select("li")]})

        elif "exercises" in cls:
            continue  # tratado à parte

        else:
            interno = filho.get_text(strip=True)  # só sonda se há conteúdo
            if interno:
                blocos.append({"tipo": "bruto", "html": tracos(str(filho))})
                pend.append({"tipo": "bruto", "onde": onde,
                             "o_que": f"bloco <{filho.name} class={' '.join(cls)}> "
                                      f"copiado sem interpretação - conferir o tipo."})
    return blocos


def marcar_codigo(b: dict, pend: list, onde: str):
    src = b["codigo"]
    c20 = sorted(set(C20.findall(src)))
    if c20:
        b["c20"] = c20
    achados = sorted({rot for lit, rot in C17_ALVO.items() if lit in src})
    if achados:
        b["c17"] = achados
    if SINTONIA.search(src):
        b["dominio_antigo"] = True
        pend.append({"tipo": "dominio", "onde": onde,
                     "o_que": "bloco de código do Sintonia - precisa ser reescrito "
                              "sobre o Deriva e extraído de arquivo que compila."})
    if "// ❌" in src or "BUG" in src:
        b["quebrado_de_proposito"] = True


def extrair_exercicios(pag: Tag, origem: str) -> list:
    out = []
    for i, item in enumerate(pag.select(".exercise-item"), 1):
        num = item.select_one(".exercise-num")
        spans = item.find_all("span", recursive=False)
        corpo = spans[-1] if len(spans) > 1 else item
        out.append({
            "n": (texto(num).rstrip(".") if num else f"{i:02d}"),
            "html": html_interno(corpo, origem),
            "origem": origem,
        })
    return out


def extrair_pagina(rel: str):
    caminho = V1 / f"{rel}.html"
    sopa = BeautifulSoup(caminho.read_text(encoding="utf-8"), "html.parser")
    titulo = sopa.title.get_text().split("|")[0].strip() if sopa.title else rel
    slides = []
    for sec in sopa.select("section.slide"):
        sid = sec.get("id") or ""
        num = sec.select_one(".slide-num")
        tit = sec.select_one(".slide-title")
        corpo = sec.select_one(".slide-body")
        slides.append({
            "id": sid,
            "num": texto(num) if num else "",
            "titulo": texto(tit) if tit else "",
            "corpo": corpo,
            "sec": sec,
        })
    return titulo, slides, sopa


# ---------------------------------------------------------------------------
# montagem de uma aula do v2
# ---------------------------------------------------------------------------
def montar_aula(a: dict, pend_geral: list) -> dict:
    pend = []
    onde = f"aula {a['n']:02d}"
    slides_v2 = []
    exercicios = []
    objetivos = []
    fatia_id = a["fatia"][0] if a["fatia"] else None

    for rel in a["origem_v1"]:
        titulo_v1, slides, sopa = extrair_pagina(rel)

        chave = (rel, fatia_id)
        if chave in FATIAS:
            querer = FATIAS[chave]
            ids = {q.rstrip("*") for q in querer}
            comp = {q.rstrip("*") for q in querer if q.endswith("*")}
        else:
            ids, comp = None, set()

        for s in slides:
            if s["id"] == "exercicios":
                novos = extrair_exercicios(s["sec"], rel)
                if rel in PARTIDAS and novos:
                    for e in novos:
                        e["redistribuir"] = True
                    pend.append({
                        "tipo": "exercicios", "onde": onde,
                        "o_que": f"{len(novos)} exercícios vêm de `{rel}`, que se parte. "
                                 f"Foram anexados aqui INTEIROS e marcados; a divisão "
                                 f"entre as fatias é decisão de conteúdo.",
                    })
                exercicios += novos
                continue

            if ids is not None and s["id"] not in ids:
                continue

            blocos = extrair_blocos(s["corpo"], pend, onde) if s["corpo"] else []
            objs = [b for b in blocos if b["tipo"] == "objetivos"]
            if objs:
                objetivos += objs[0]["itens"]
                blocos = [b for b in blocos if b["tipo"] != "objetivos"]

            if s["id"] in comp:
                pend.append({
                    "tipo": "fatia", "onde": onde,
                    "o_que": f"o slide “{s['titulo']}” de `{rel}` foi para MAIS DE UMA "
                             f"aula: a divisão do plano cai dentro dele. Separe a prosa "
                             f"parágrafo por parágrafo - é a migração de risco 1/3.",
                })

            slides_v2.append({
                "id": s["id"], "titulo": s["titulo"],
                "origem": rel, "compartilhado": s["id"] in comp,
                "blocos": blocos,
            })

    if a.get("novo"):
        for x in a["novo"]:
            pend.append({"tipo": "novo", "onde": onde,
                         "o_que": f"conteúdo NOVO exigido pelo plano v2: {x}. "
                                  f"Não existe no v1 - precisa ser escrito."})
    if a.get("caca_bug"):
        rot, desc = a["caca_bug"]
        pend.append({"tipo": "caca-bug", "onde": onde,
                     "o_que": f"{rot}: {desc}. A variante quebrada e o roteiro da caça "
                              f"precisam existir no repositório do Deriva."})
    if a["lab"]:
        lab = next(l for l in mapa.LABS if l["id"] == a["lab"])
        pend.append({"tipo": "lab", "onde": onde,
                     "o_que": f"{lab['id']} “{lab['titulo']}” - esqueleto, solução de "
                              f"referência e portão precisam ser escritos."})

    pend_geral += pend
    return {
        "n": a["n"], "slug": a["slug"], "titulo": a["titulo"], "curto": a["curto"],
        "unidade": a["unidade"], "cap_v1": a["cap_v1"], "origem_v1": a["origem_v1"],
        "fatia": list(a["fatia"]) if a["fatia"] else None,
        "deriva": a["deriva"], "lab": a["lab"], "interativos": a["interativos"],
        "nota_migracao": a.get("nota_migracao", ""),
        "objetivos": objetivos,
        "slides": slides_v2,
        "exercicios": exercicios,
        "pendencias": pend,
    }


def montar_anexo_a(pend_geral: list) -> dict:
    an = mapa.ANEXOS[0]
    pend = []
    slides = []
    for rel in an["origem_v1"]:
        _, ss, _ = extrair_pagina(rel)
        for s in ss:
            if s["id"] == "exercicios":
                continue
            blocos = extrair_blocos(s["corpo"], pend, "anexo A") if s["corpo"] else []
            blocos = [b for b in blocos if b["tipo"] != "objetivos"]
            slides.append({"id": s["id"], "titulo": s["titulo"], "origem": rel,
                           "compartilhado": False, "blocos": blocos})
    pend_geral += pend
    return {"n": 0, "slug": an["slug"], "titulo": an["titulo"], "curto": an["curto"],
            "unidade": "anexo", "cap_v1": [20], "origem_v1": an["origem_v1"],
            "fatia": None, "deriva": an["deriva"], "lab": None, "interativos": [],
            "nota_migracao": an["nota"], "objetivos": [], "slides": slides,
            "exercicios": [], "pendencias": pend, "c20": True}


CABECA = '''# -*- coding: utf-8 -*-
"""GERADO por build/extrair_v1.py - não edite à mão sem ler o aviso.

Origem no site v1: {origem}
{fatia}
Editar aqui é o caminho certo para MUDAR o conteúdo: este arquivo é a fonte de
verdade do site. Reextrair NÃO o sobrescreve: `build/extrair_v1.py` grava o
recorte fiel em `conteudo/extraido/` e só semeia daqui o arquivo que não existe
ou que ninguém tocou desde a última extração. Para descartar a reescrita e
voltar ao recorte cru, `make semear-site`, que é explícito e destrutivo.

Pendências desta aula: {npend} (ver conteudo/PENDENCIAS.md)
"""

AULA = '''


def escrever(d: dict, conferir: bool, semear: bool, contas: dict) -> bool:
    """Grava o recorte fiel, e SEMEIA o material só quando pode.

    Devolve True se o recorte divergiu do que estava em `conteudo/extraido/`.
    O que acontece com `conteudo/aulas/` é contado em `contas`, e o critério é
    um só: semeia quando o arquivo não existe, ou quando ele é byte-idêntico
    ao recorte anterior - isto é, quando ninguém o tocou. Tocado, preserva-se.
    """
    nome = f"{d['slug']}.py"
    fatia = ("Fatia: %s - %s" % (d["fatia"][0], d["fatia"][1])) if d["fatia"] else "Página inteira."
    txt = CABECA.format(origem=", ".join(d["origem_v1"]) or " - ",
                        fatia=fatia, npend=len(d["pendencias"]))
    corpo = {k: v for k, v in d.items()}
    txt += py_repr(corpo) + "\n"

    cru = EXTRAIDO / nome
    antes = cru.read_text(encoding="utf-8") if cru.exists() else ""
    divergiu = antes != txt
    if conferir:
        return divergiu

    cru.parent.mkdir(parents=True, exist_ok=True)
    cru.write_text(txt, encoding="utf-8")

    vivo = SAIDA / nome
    vivo.parent.mkdir(parents=True, exist_ok=True)
    if not vivo.exists():
        vivo.write_text(txt, encoding="utf-8")
        contas["novos"] += 1
    elif semear:
        vivo.write_text(txt, encoding="utf-8")
        contas["semeados"] += 1
    elif vivo.read_text(encoding="utf-8") == antes:
        # intocado desde a última extração: pode receber o recorte novo
        if divergiu:
            vivo.write_text(txt, encoding="utf-8")
            contas["atualizados"] += 1
        else:
            contas["intocados"] += 1
    else:
        contas["preservados"] += 1
    return divergiu


def conferir_cobertura(aulas: list) -> list:
    """Nenhum slide de conteúdo do v1 pode ficar sem destino.

    É este portão, e não a boa vontade de quem escreve o mapa, que garante o
    que PLANO-MATERIAL §2 pede: as três migrações de risco conferidas item a
    item. Se uma fatia esquecer um slide, o build para aqui.
    """
    destino = {}
    for d in aulas:
        for s in d["slides"]:
            destino.setdefault((s["origem"], s["id"]), []).append(d["slug"])

    faltam = []
    for rel in sorted({r for a in mapa.AULAS for r in a["origem_v1"]} |
                      {r for x in mapa.ANEXOS for r in x["origem_v1"]}):
        _, slides, _ = extrair_pagina(rel)
        for s in slides:
            if s["id"] == "exercicios":
                continue
            if (rel, s["id"]) not in destino:
                faltam.append(f"{rel}#{s['id']} “{s['titulo']}” não foi para "
                              f"nenhuma aula nem anexo")
    return faltam


def main():
    conferir = "--conferir" in sys.argv
    erros = mapa.verificar()
    if erros:
        for e in erros:
            print("mapa ERRO:", e)
        return 1

    pend = []
    aulas = [montar_aula(a, pend) for a in mapa.AULAS]
    aulas.append(montar_anexo_a(pend))

    faltam = conferir_cobertura(aulas)
    if faltam:
        for f in faltam:
            print("COBERTURA ERRO:", f)
        print("nada foi escrito - corrija FATIAS em build/extrair_v1.py")
        return 2

    # `--semear` é explícito e DESTRUTIVO: descarta a reescrita e volta ao
    # recorte cru do v1.
    semear = "--semear" in sys.argv
    contas = dict(novos=0, semeados=0, atualizados=0, intocados=0, preservados=0)
    mudou = 0
    for d in aulas:
        if escrever(d, conferir, semear, contas):
            mudou += 1

    # relatório de pendências: o que a migração NÃO resolve sozinha
    por_tipo = {}
    for p in pend:
        por_tipo.setdefault(p["tipo"], []).append(p)
    # O que a migração ACHOU e o que AINDA está aberto são dois números.
    #
    # Este relatório dizia 96 pendências, das quais 46 eram "prosa ou código
    # ainda no Sintonia" - e eram zero, porque a reescrita já tinha
    # acontecido. Ele lista o que a extração encontrou no v1, e isso não muda
    # nunca; quem sabe o que resta é o arquivo VIVO, em `conteudo/aulas/`, que
    # declara as próprias pendências. Lista que não encolhe quando o trabalho
    # é feito faz o leitor concluir que nada foi feito.
    import importlib.util as _u
    abertas = []
    for _arq in sorted(SAIDA.glob("*.py")):
        _s = _u.spec_from_file_location("aula", _arq)
        _m = _u.module_from_spec(_s)
        _s.loader.exec_module(_m)
        for _x in (_m.AULA.get("pendencias") or []):
            abertas.append((_arq.name, _x))

    # e um portão: pendência de laboratório cujo laboratório existe é falsa
    _labs = RAIZ / "exemplos" / "deriva" / "laboratorios"
    _falsas = [(a, x) for a, x in abertas
               if x.get("tipo") == "lab"
               and (m2 := re.search(r"LAB-(\d+)", x.get("o_que", "")))
               and (_labs / f"lab-{m2.group(1)}" / "solucao.cpp").exists()]

    if _falsas:
        for a, x in _falsas:
            print(f"PENDÊNCIA FALSA: {a} declara {x.get('o_que')[:60]!r}, "
                  "e o laboratório existe com solução de referência")
        print("  apague a pendência: relatório que lista trabalho feito faz o "
              "leitor concluir que nada foi feito")
        return 1

    linhas = ["# PENDÊNCIAS DA MIGRAÇÃO v1 → v2", "",
              "Gerado por `build/extrair_v1.py`. **Dois números, e a diferença "
              "importa:** a tabela abaixo é o que a extração encontrou no site "
              "v1, e ela não muda; o que ainda está aberto é o que os arquivos "
              "de `conteudo/aulas/` declaram, e são "
              f"**{len(abertas)}**.", "",
              "## Ainda aberto", ""]
    if abertas:
        for a, x in abertas:
            linhas.append(f"- **{a}** · `{x.get('tipo')}` · {x.get('o_que')}")
    else:
        linhas.append("Nada. Todas as pendências da migração foram resolvidas.")
    linhas += ["", "## O que a extração encontrou no v1", "",
               "Histórico, e não lista de tarefas: estes são os itens que a "
               "migração determinística não podia resolver sozinha, e a maioria "
               "já foi resolvida à mão desde então.", "",
              "| tipo | quantos | o que é |", "|---|---|---|"]
    rotulos = {
        "fatia": "slide que atravessa a divisão do plano - separar parágrafo por parágrafo",
        "exercicios": "exercícios de página partida - redistribuir entre as fatias",
        "dominio": "prosa ou código ainda no Sintonia - reescrever sobre o Deriva",
        "novo": "conteúdo novo exigido pelo plano v2 - escrever",
        "lab": "laboratório preparatório - esqueleto, solução e portão",
        "caca-bug": "variante quebrada e roteiro da caça ao bug",
        "bruto": "bloco HTML copiado sem interpretação - conferir o tipo",
    }
    for t in sorted(por_tipo, key=lambda x: -len(por_tipo[x])):
        linhas.append(f"| `{t}` | {len(por_tipo[t])} | {rotulos.get(t, ' - ')} |")
    if DEFEITOS_V1:
        linhas += ["", f"## marcação do v1 consertada na extração - {len(DEFEITOS_V1)}", "",
                   "`<` literal que o v1 deixou solto no HTML e que quebrava qualquer "
                   "validador. Escapado automaticamente; o conteúdo não mudou.", ""]
        for onde, trecho in DEFEITOS_V1:
            linhas.append(f"- **{onde}** - `{trecho}`")
        linhas.append("")
    linhas += ["", f"**Total: {len(pend)} pendências.**", ""]
    for t in sorted(por_tipo, key=lambda x: -len(por_tipo[x])):
        linhas += [f"## `{t}` - {len(por_tipo[t])}", ""]
        for p in por_tipo[t]:
            linhas.append(f"- **{p['onde']}** - {p['o_que']}")
        linhas.append("")
    alvo = RAIZ / "conteudo" / "PENDENCIAS.md"
    if not conferir:
        alvo.write_text("\n".join(linhas), encoding="utf-8")

    n_slides = sum(len(d["slides"]) for d in aulas)
    n_ex = sum(len(d["exercicios"]) for d in aulas)
    n_cod = sum(1 for d in aulas for s in d["slides"] for b in s["blocos"] if b["tipo"] == "codigo")
    n_call = sum(1 for d in aulas for s in d["slides"] for b in s["blocos"] if b["tipo"] == "callout")
    if not conferir:
        print(f"  conteudo/extraido/: reescrito · conteudo/aulas/: "
              f"{contas['novos']} novo(s), {contas['atualizados']} semente(s) "
              f"atualizada(s), {contas['preservados']} preservado(s)")
    print(f"{'conferido' if conferir else 'extraído'}: {len(aulas)} arquivos "
          f"({mudou} {'divergem' if conferir else 'escritos'}) · "
          f"{n_slides} slides · {n_ex} exercícios · {n_cod} blocos de código · "
          f"{n_call} callouts · {len(pend)} pendências")
    # Em `--conferir`, divergência REPROVA.
    #
    # Estes três terminavam em `return 0` mesmo tendo detectado desvio, e
    # `make verifica` imprimia "portões OK" logo abaixo de "DIVERGE". Um
    # portão que relata e não recusa deixa passar exatamente o que ele existe
    # para pegar: saída gerada editada à mão, ou gerador que mudou e saída que
    # ficou velha. Foi o que aconteceu quando o cabeçalho do extrator mudou.
    if conferir and mudou:
        print(f"  reprovado: {mudou} arquivo(s) de conteudo/extraido/ "
              "desatualizado(s) - rode `python3 build/extrair_v1.py`")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
