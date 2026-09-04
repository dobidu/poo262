#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build/build_site.py - conteudo/ → poo/

Gera o site v2 da disciplina a partir da fonte única em `conteudo/`, aplicando
o mapa canônico de `conteudo/mapa.py` (26 aulas, 3 anexos, 20 versões do
Deriva, 12 laboratórios, 8 tipos de interativo).

O design system (css/, js/) vem do Claude Design e NÃO é gerado: o build só
escreve HTML. Ao final, confere que todo link interno resolve - link morto
para o build.

Uso:  python3 build/build_site.py [--sem-notas] [--conferir]
      --sem-notas  omite as notas de migração (versão para estudante)
      --conferir   não escreve; diz o que mudaria
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "poo"
sys.path.insert(0, str(RAIZ / "build"))
sys.path.insert(0, str(RAIZ / "conteudo"))

import mapa                                     # noqa: E402
try:
    import codigo_deriva                        # noqa: E402
    CODIGO_DERIVA = codigo_deriva.CODIGO
except ModuleNotFoundError:      # ainda não rodou build/extrair_codigo.py
    CODIGO_DERIVA = {}
try:
    from medidas import MEDIDAS                 # noqa: E402
except ModuleNotFoundError:      # ainda não rodou build/medir_deriva.py
    MEDIDAS = {"versao": "?", "testes": 0, "variantes_escritas": []}
import trechos                                  # noqa: E402
from comum import esc, link_ce, moldura, realcar  # noqa: E402

SEM_NOTAS = "--sem-notas" in sys.argv
CONFERIR = "--conferir" in sys.argv

ICONE = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
         "<rect width='16' height='16' fill='%230A0C0B'/><text x='2' y='12' "
         "font-family='monospace' font-size='11' fill='%23F2A93B'>@</text></svg>")


# ---------------------------------------------------------------------------
# carregar conteudo/aulas/*.py
# ---------------------------------------------------------------------------
def carregar(slug):
    caminho = RAIZ / "conteudo" / "aulas" / f"{slug}.py"
    spec = importlib.util.spec_from_file_location(f"conteudo_{slug}", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.AULA


CONTEUDO = {a["slug"]: carregar(a["slug"]) for a in mapa.AULAS}
CONTEUDO["anexo-a"] = carregar("anexo-a")


def contar_exercicios():
    """Quantos itens de exercício existem de fato.

    A soma bruta por aula dá 124 porque os itens das três páginas partidas do
    v1 aparecem em cada fatia, à espera de redistribuição. O número honesto é
    o de itens distintos - 108, os mesmos do v1 - , e é esse que vai à capa.
    """
    vistos, dup = set(), 0
    for a in mapa.AULAS:
        for e in CONTEUDO[a["slug"]]["exercicios"]:
            chave = (e["origem"], e["n"])
            if chave in vistos:
                dup += 1
            vistos.add(chave)
    return len(vistos), dup


N_EX, N_EX_DUP = contar_exercicios()


# ---------------------------------------------------------------------------
# moldura da página
# ---------------------------------------------------------------------------
def pagina(*, titulo, descricao, corpo, css_extra=(), js_extra=(), prev=None,
           next=None, migalha="", classe_corpo="", og=None, com_arvore=True):
    links = "\n".join(f'<link rel="stylesheet" href="css/{c}">'
                      for c in ("tokens.css", "pagina.css") + tuple(css_extra))
    scripts = "\n".join(f'<script src="js/{j}" defer></script>'
                        for j in ("app.js",) + tuple(js_extra))
    rel = ""
    if prev:
        rel += f'\n<link rel="prev" href="{prev}">'
    if next:
        rel += f'\n<link rel="next" href="{next}">'
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(og or descricao)}">
<meta property="og:type" content="website">
<link rel="icon" href="{ICONE}">{rel}
{links}
{scripts}
</head>
<body{f' class="{classe_corpo}"' if classe_corpo else ''}>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>

<header class="barra">
  <div class="migalha">
    <span class="badge-ufpb">UFPB · CI</span>
    <span class="sep">/</span><a href="index.html" style="border:none;color:var(--fosforo)"><b>POO</b></a>
    {migalha}
  </div>
  <div class="ferramentas">
    {'<button class="tecla gaveta-abre" type="button" data-acao="gaveta" aria-expanded="false">▸ AULAS</button>' if com_arvore else ''}
    <a class="tecla" href="glossario.html">GLOSSÁRIO</a>
    <button class="tecla" type="button" data-acao="projecao" aria-pressed="false">F PROJEÇÃO</button>
  </div>
</header>

{corpo}

<footer class="pe">
  <span class="badge-ufpb">UFPB · CI · DI</span>
  <span>PROGRAMAÇÃO ORIENTADA A OBJETOS · {mapa.SEMESTRE}</span>
  <span>{mapa.EMAIL}</span>
  <span style="margin-left:auto">{mapa.PADRAO} · FTXUI v5.0.0 · Catch2</span>
</footer>
</body>
</html>
"""


def arvore(atual=None):
    """T6 · a árvore das 26 aulas mais os anexos. Vira gaveta em ≤860px."""
    out = ['<nav class="arvore" aria-label="Aulas da disciplina" data-aberta="0">']
    for u in mapa.UNIDADES:
        aulas = mapa.por_unidade(u["n"])
        slugs = ",".join(a["slug"] for a in aulas)
        out.append('<div class="arvore__unidade">'
                   f'<div class="arvore__rot">UNIDADE {u["n"]} · {esc(u["rot"]).upper()}</div>'
                   f'<div class="arvore__medidor" data-unidade-conta="{slugs}">'
                   f'<b>0</b>/{len(aulas)} lidas · Deriva {u["deriva"]}</div>'
                   "</div>")
        out.append("<ol>")
        for i, a in enumerate(aulas):
            galho = "╰" if i == len(aulas) - 1 else "├"
            cur = ' aria-current="page"' if a["slug"] == atual else ""
            marca = ('<span class="tem-int" title="tem exemplo interativo">▶</span>'
                     if a["interativos"] else "")
            out.append(f'<li><a href="aula-{a["n"]:02d}.html" data-slug="{a["slug"]}"{cur}>'
                       f'<span class="galho">{galho}</span>'
                       f'<span class="num">{a["n"]:02d}</span>'
                       f'{esc(a["curto"])}{marca}</a></li>')
        out.append("</ol>")
    out.append('<div class="arvore__unidade"><div class="arvore__rot">ANEXOS</div></div><ol>')
    for i, x in enumerate(mapa.ANEXOS):
        galho = "╰" if i == len(mapa.ANEXOS) - 1 else "├"
        cur = ' aria-current="page"' if x["slug"] == atual else ""
        selo = ' <span class="c20">C++20</span>' if x["c20"] else ""
        out.append(f'<li><a href="{x["slug"]}.html"{cur}><span class="galho">{galho}</span>'
                   f'<span class="num">{x["letra"]}</span>{esc(x["curto"])}{selo}</a></li>')
    out.append("</ol>")
    out.append('<div class="arvore__unidade"><div class="arvore__rot">MATERIAL</div></div><ol>')
    extras = [("trilha.html", "Trilha do Deriva"), ("galeria.html", "Os 8 instrumentos"),
              ("laboratorios.html", "12 laboratórios"), ("rubrica.html", "Rubrica de revisão"),
              ("verifica.html", "Portão make verifica"), ("exercicios.html", "Exercícios"),
              ("plano-de-ensino.html", "Plano de ensino")]
    for i, (href, rot) in enumerate(extras):
        galho = "╰" if i == len(extras) - 1 else "├"
        cur = ' aria-current="page"' if href == atual else ""
        out.append(f'<li><a href="{href}"{cur}><span class="galho">{galho}</span>'
                   f'<span class="num">▸</span>{esc(rot)}</a></li>')
    out.append("</ol></nav>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# blocos de conteúdo
# ---------------------------------------------------------------------------
def bl_prosa(b):
    return f"<p>{b['html']}</p>"


def bl_lista(b):
    tag = "ol" if b.get("ordenada") else "ul"
    itens = "".join(f"<li>{i}</li>" for i in b["itens"])
    return f"<{tag}>{itens}</{tag}>"


def bl_tabela(b):
    cab = "".join(f"<th>{c}</th>" for c in b["cabeca"])
    linhas = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>"
                     for l in b["linhas"])
    return ('<div style="overflow-x:auto;max-width:100%"><table class="tabela">'
            + (f"<thead><tr>{cab}</tr></thead>" if cab else "")
            + f"<tbody>{linhas}</tbody></table></div>")


def repo(txt):
    """Troca o lugar do endereço do repositório pelo endereço, se houver.

    O fonte do material escreve `<endereco-do-repositorio>`, e o motivo está
    escrito lá: URL em material didático envelhece calada, e a Aula 04 não
    pode mandar o estudante clonar um endereço morto - ela já mandou, e era o
    do sistema-base anterior. Com `mapa.REPOSITORIO` preenchido, a página sai
    com o endereço de verdade; vazio, sai o texto genérico.
    """
    r = getattr(mapa, "REPOSITORIO", None)
    if not r:
        return txt
    # o nome do diretório vem da URL, senão o `cd` da linha seguinte aponta
    # para uma pasta que o `clone` não criou - foi o que aconteceu quando a
    # URL entrou e o `cd` continuou com o nome do sistema-base
    nome = r.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
    return (txt.replace("<endereco-do-repositorio>", r)
               .replace("<nome-do-repositorio>", nome))


def bl_codigo(b):
    """Bloco de código: realce próprio, deep link para o CE com -std=c++17.

    O estado `falha` não é erro do material: é trecho quebrado de propósito, e
    o selo diz isso com glifo e rótulo, nunca só com cor.
    """
    quebrado = b.get("quebrado_de_proposito")
    estado = "falha" if quebrado else "ok"
    selo = ('<span class="selo-estado" data-t="falha">▲ QUEBRADO DE PROPÓSITO</span>'
            if quebrado else '<span class="selo-estado" data-t="ok">✓ COMPILA</span>')
    selos_c17 = "".join(f'<span class="tk-tipo">{esc(x)}</span>' for x in b.get("c17", []))
    selo_c20 = '<span class="c20">C++20</span>' if b.get("c20") else ""
    legenda = f'<span class="arq">{esc(b["legenda"])}</span>' if b["legenda"] else ""
    codigo = repo(b["codigo"])
    ce = link_ce(codigo) if b["lang"] in ("cpp", "c") else None
    pe = [selo]
    if selos_c17:
        pe.append("C++17: " + selos_c17)
    if selo_c20:
        pe.append(selo_c20)
    if b.get("arquivo"):
        pe.append(f'<span class="arq">{esc(b["arquivo"])}:{b["linha"]}</span>')
    if ce:
        pe.append(f'<a href="{ce}" rel="noopener" target="_blank">abrir no Compiler '
                  f'Explorer · -std=c++17 -Wall -Wextra</a>')
    return (f'<div class="codigo" data-estado="{estado}">'
            f'<div class="codigo__cab"><span>{esc(b["lang"])}</span>{legenda}'
            f'<div class="codigo__acoes">'
            f'<button class="tecla" type="button" data-acao="copiar">COPIAR</button></div></div>'
            f'<pre><code>{realcar(codigo, b["lang"])}</code></pre>'
            f'<div class="codigo__pe">' + " · ".join(pe) + "</div></div>")


def bl_callout(b):
    d = mapa.CALLOUTS[b["t"]]
    corpo = "".join(f"<p>{p}</p>" for p in b["paragrafos"])
    tit = esc(b["titulo"]) or d["rot"]
    return (f'<aside class="callout" data-t="{b["t"]}">'
            + moldura(f'{d["glifo"]} {d["rot"]} · {tit}')
            + f'<div class="callout__corpo">{corpo}</div>'
            + moldura(None, None, base=True) + "</aside>")


def bl_mermaid(b):
    """O diagrama, recebido por ÂNCORA e não digitado no material.

    O v1 puxava Mermaid de CDN. Aqui o diagrama fica como figura de texto em
    mono dentro de painel - legível sem JS, sem rede, e no idioma visual do
    resto. Os que precisam ser manipuláveis são o T9 interativo.

    O bloco declara `trecho`, que é o id de uma entrada de
    `conteudo/trechos.py` apontando para `exemplos/deriva/diagramas/*.mmd`.
    Digitado no material, um diagrama pode afirmar uma hierarquia que o código
    não tem e ninguém percebe; por âncora, `build/extrair_codigo.py` falha se
    a âncora sair do arquivo, e `testes/test_uml.cpp` afirma as relações que
    o desenho declara.
    """
    tid = b.get("trecho")
    if tid:
        d = CODIGO_DERIVA.get(tid)
        if not d:
            return ('<p style="color:var(--falha)">diagrama sem trecho '
                    'extraído: ' + esc(tid) + "</p>")
        fonte = d["codigo"]
        proc = f"{d['arquivo']}:{d['linha']}"
    else:
        fonte, proc = b.get("fonte", ""), "fonte mermaid digitada"
    return (moldura("DIAGRAMA", esc(proc), sistema=True)
            + '<div class="painel painel--sistema"><pre style="margin:0;padding:var(--e2);'
            'font-family:var(--maquina);font-size:var(--t-est);color:var(--apagado);'
            f'overflow-x:auto">{esc(fonte)}</pre></div>'
            + moldura(None, None, sistema=True, base=True))


def bl_bruto(b):
    return b["html"]


RENDER = {"prosa": bl_prosa, "lista": bl_lista, "tabela": bl_tabela,
          "codigo": bl_codigo, "callout": bl_callout, "mermaid": bl_mermaid,
          "bruto": bl_bruto, "objetivos": lambda b: bl_lista({"itens": b["itens"]})}


def blocos(bs):
    return "\n".join(RENDER[b["tipo"]](b) for b in bs if b["tipo"] in RENDER)


# ---------------------------------------------------------------------------
# interativos e trilha
# ---------------------------------------------------------------------------
def secao_interativo(chave, n_slide, aula_n):
    d = mapa.INTERATIVOS[chave]
    if chave == "uml":
        return uml_html(n_slide, aula_n)
    rot = f'<span class="slide__n">{n_slide}</span>'
    return (f'<section class="slide" id="int-{chave}">'
            f'<div class="slide__cab">{rot}<h2>{esc(d["titulo"])}</h2></div>'
            f'<p>{esc(d["nota"]).capitalize()}. O avanço do passo é seu: a peça não tem '
            f'<em>play</em>, e o estado exibido é função de <em>(cenário, passo)</em>, de '
            f'forma que voltar um passo devolva exatamente o quadro anterior.</p>'
            f'<section data-int="{chave}" tabindex="0"></section></section>')


def uml_html(n_slide, aula_n):
    botoes = [("entidade", "entidade", True), ("sonda", "sonda", True),
              ("drone", "drone", True), ("item", "item", False),
              ("i_reparo", "i_reparavel", False), ("reparadora", "sonda_reparadora", False),
              ("componente", "componente", False), ("mochila", "mochila", False)]
    bs = "".join(f'<button class="cen" type="button" data-add="{k}" '
                 f'aria-pressed="{"true" if on else "false"}">{esc(rot)}</button>'
                 for k, rot, on in botoes)
    return f"""<section class="slide" id="int-uml">
  <div class="slide__cab"><span class="slide__n">{n_slide}</span><h2>Diagrama de classes, como ferramenta</h2></div>
  <p>O diagrama aqui é ferramenta, e não figura pronta: você acrescenta classe e relação, e o
  desenho se reorganiza. Os níveis são <em>calculados</em> a partir da profundidade de
  herança, em vez de fixados por posições escolhidas à mão; remover uma classe leva os
  descendentes com ela, porque herança <em>é</em> dependência, e o diagrama não a esconde.</p>
  <section class="interativo" data-uml aria-label="Diagrama de classes interativo da hierarquia do Deriva">
    {moldura("HIERARQUIA DO DERIVA", "3 a 8 classes", sistema=True)}
    <div class="int__palco"><div class="uml" data-uml-palco></div></div>
    <div class="int__controles">
      <span class="cenarios__rot">ACRESCENTAR</span>
      <div class="cenarios">{bs}</div>
      <div class="grupo" style="margin-left:auto">
        <button class="bt" type="button" data-uml-reset>↺ INICIAL</button>
      </div>
    </div>
    <div class="int__estado" data-uml-estado aria-live="polite"></div>
    <div class="int__legenda">
      <span class="rot">LEGENDA</span>
      <p><span style="color:var(--fosforo)">△ ─ herança pública</span> ·
      <span style="color:var(--frio)">△ ┄ implementação de interface (moldura tracejada)</span> ·
      <span style="color:var(--apagado)">◆ ─ composição</span> · <em>nome em itálico</em> = abstrata ·
      <span style="color:var(--fosforo)">método em âmbar</span> = virtual ·
      <span style="color:var(--fosforo);font-style:italic">itálico</span> = puramente virtual.</p>
    </div>
    {moldura(None, None, sistema=True, base=True)}
  </section>
</section>"""


def secao_codigo_deriva(aula_n, numero):
    """O código da aula, recortado do Deriva que compila.

    Regra do handoff §5: todo trecho do material é extraído de arquivo que
    compila, nunca digitado. O rodapé de cada bloco diz de qual arquivo e de
    que linha - e `build/extrair_codigo.py` falha se a âncora deixar de existir.
    """
    # `inline` fica fora: o diagrama é renderizado dentro do slide que o
    # explica, e repeti-lo aqui o mostraria duas vezes na mesma página.
    ids = [t["id"] for t in trechos.por_aula(aula_n)
           if t["id"] in CODIGO_DERIVA and not t.get("inline")]
    if not ids:
        return ""
    blocos_html = []
    for i in ids:
        d = CODIGO_DERIVA[i]
        blocos_html.append(f'<p>{d["nota"]}</p>' + bl_codigo(d))
    quebrados = sum(1 for i in ids if CODIGO_DERIVA[i]["quebrado_de_proposito"])
    s = "s" if len(ids) > 1 else ""
    nota = (f'{len(ids)} trecho{s} do Deriva'
            + (f", {quebrados} deliberadamente quebrado{'s' if quebrados > 1 else ''}"
               if quebrados else ""))
    return (f'<section class="slide" id="codigo-deriva">'
            f'<div class="slide__cab"><span class="slide__n">{numero}</span>'
            f'<h2>O código, extraído do Deriva</h2></div>'
            f'<p style="font-family:var(--maquina);font-size:var(--t-est);'
            f'color:var(--apagado)">{nota}, recortado{s} por âncora do projeto que '
            f'compila · '
            f'<code>-std=c++17 -Wall -Wextra -Wpedantic</code>, zero warning · '
            f'<code>make verifica</code> 4 de 4</p>'
            + "".join(blocos_html) + "</section>")


def acumulado_ate(v):
    """Quantos testes da trilha existem até esta versão, inclusive.

    A soma é sobre a ORDEM da trilha, e não sobre o dicionário: `medidas.py`
    guarda por versão, e o acumulado é o que o estudante vê crescer.
    """
    total = 0
    por = MEDIDAS.get("testes_por_versao", {})
    for t in mapa.TRILHA:
        total += por.get(t["v"], 0)
        if t["v"] == v:
            return total
    return total


def selo_testes(t, acumulado):
    """O selo de testes de uma versão da trilha: MEDIDO, e não projetado.

    Antes o mapa declarava um número por versão e a marca `meta` dizia que
    aquilo era alvo; a legenda da página explicava `meta` como "versão ainda
    não escrita". Vinte das vinte e uma versões estavam marcadas assim, e a
    trilha inteira está escrita desde a v0.0 até a v2.7 - a página afirmava ao
    estudante o contrário do que o repositório contém.

    Agora o número vem de `conteudo/medidas.py`, contado por
    `build/medir_deriva.py` a partir da declaração de versão que cada arquivo
    de `testes/` traz na primeira linha. E a separação que faltava: os 129
    testes da trilha são os do jogo, e os outros 47 medem material de aula -
    o mapa somava os dois e declarava 141 onde a trilha tem 129.
    """
    proprios = MEDIDAS.get("testes_por_versao", {}).get(t["v"], 0)
    nota = t.get("nota_testes")
    if proprios:
        selo = ('<span style="color:var(--ok)">✓ ' + str(proprios)
                + " novos, " + str(acumulado) + " no total, medidos</span>")
    else:
        selo = ('<span style="color:var(--apagado)">◇ nenhum teste próprio</span>')
    if nota:
        selo += ' <span style="color:var(--apagado)">· ' + esc(nota) + "</span>"
    return selo


def callout_deriva(aula_n):
    vs = mapa.versoes_da_aula(aula_n)
    if not vs:
        return ""
    partes = []
    for t in vs:
        p = (f'<p><span class="versao">{t["v"]}</span> {esc(t["entrega"])}. '
             f'<span style="color:var(--apagado)">{esc(t["conceitos"])}</span> · '
             f'{selo_testes(t, acumulado_ate(t["v"]))}</p>')
        if t.get("quebrada"):
            tag, o_que, como = t["quebrada"]
            p += (f'<p><span class="versao" style="background:var(--falha)">{tag}</span> '
                  f'{esc(o_que)} - {esc(como)}</p>')
        partes.append(p)
    return (f'<aside class="callout" data-t="deriva">'
            + moldura("▸ DERIVA · O QUE VOCÊ ENTREGA NESTA AULA")
            + f'<div class="callout__corpo">{"".join(partes)}'
              f'<p style="font-family:var(--maquina);font-size:var(--t-rot);'
              f'color:var(--apagado)">A versão anterior e a seguinte estão na '
              f'<a href="trilha.html">trilha completa</a>.</p></div>'
            + moldura(None, None, base=True) + "</aside>")


def bloco_lab(aula_n):
    l = next((x for x in mapa.LABS if x["aula"] == aula_n), None)
    if not l:
        return ""
    return (f'<aside class="callout" data-t="tip">'
            + moldura(f'✓ LABORATÓRIO · {l["id"]}')
            + f'<div class="callout__corpo"><p><strong>{esc(l["titulo"])}</strong></p>'
              f'<p>Faça este laboratório antes desta aula. O portão de correção é: '
              f'{esc(l["portao"])}.</p>'
              f'<p><a href="laboratorios.html#{l["id"].lower()}">Ver o {l["id"]} na página '
              f'dos laboratórios</a></p></div>'
            + moldura(None, None, base=True) + "</aside>")


def nota_migracao(d):
    if SEM_NOTAS or not d.get("nota_migracao"):
        return ""
    orig = ", ".join(f"<code>{esc(o)}</code>" for o in d["origem_v1"])
    caps = ", ".join(f"Cap. {c}" for c in d["cap_v1"])
    fatia = f"<p>Fatia: <strong>{esc(d['fatia'][0])}</strong> - {esc(d['fatia'][1])}.</p>" if d["fatia"] else ""
    pend = ""
    if d["pendencias"]:
        itens = "".join(f"<li>{esc(p['o_que'])}</li>" for p in d["pendencias"])
        pend = f"<p>Pendências desta aula ({len(d['pendencias'])}):</p><ul>{itens}</ul>"
    return (f'<details class="callout" data-t="info" style="margin-top:var(--e5)">'
            f'<summary style="padding:var(--e2);cursor:pointer;font-family:var(--maquina);'
            f'font-size:var(--t-rot);letter-spacing:.14em;color:var(--apagado)">'
            f'NOTA DE MIGRAÇÃO v1 → v2 · para o docente</summary>'
            f'<div class="callout__corpo"><p>Vem de {caps} do livro v1 e de {orig}.</p>'
            f'{fatia}<p>{esc(d["nota_migracao"])}</p>{pend}</div></details>')


# ---------------------------------------------------------------------------
# páginas
# ---------------------------------------------------------------------------
def pag_aula(a):
    d = CONTEUDO[a["slug"]]
    n = a["n"]
    prev = f"aula-{n-1:02d}.html" if n > 1 else "index.html"
    next = f"aula-{n+1:02d}.html" if n < 26 else "anexo-a.html"
    prev_rot = mapa.aula(n - 1)["curto"] if n > 1 else "Índice das 26 aulas"
    next_rot = mapa.aula(n + 1)["curto"] if n < 26 else "Anexo A · Concepts e Ranges"

    conteudo = []
    if d["objetivos"]:
        conteudo.append('<section class="slide" id="objetivos">'
                        + '<div class="slide__cab"><span class="slide__n">00</span>'
                        + "<h2>O que você sai sabendo</h2></div>"
                        + bl_lista({"itens": d["objetivos"]}) + "</section>")
    numero = 1
    for s in d["slides"]:
        marca = ""
        if s["compartilhado"] and not SEM_NOTAS:
            marca = ('<span style="font-family:var(--maquina);font-size:var(--t-rot);'
                     'color:var(--falha);letter-spacing:.1em"> · ▲ FATIA A SEPARAR</span>')
        conteudo.append(f'<section class="slide" id="{esc(s["id"]) or f"s{numero}"}">'
                        f'<div class="slide__cab"><span class="slide__n">{numero:02d}</span>'
                        f'<h2>{esc(s["titulo"])}{marca}</h2></div>'
                        f'{blocos(s["blocos"])}</section>')
        numero += 1

    cod = secao_codigo_deriva(n, f"{numero:02d}")
    if cod:
        conteudo.append(cod)
        numero += 1

    for chave in a["interativos"]:
        conteudo.append(secao_interativo(chave, f"{numero:02d}", n))
        numero += 1

    extras = callout_deriva(n) + bloco_lab(n)
    if extras:
        conteudo.append(f'<section class="slide" id="deriva">'
                        f'<div class="slide__cab"><span class="slide__n">{numero:02d}</span>'
                        f'<h2>O Deriva nesta aula</h2></div>{extras}</section>')
        numero += 1

    if d["exercicios"]:
        itens = []
        for e in d["exercicios"]:
            aviso = ""
            if e.get("redistribuir") and not SEM_NOTAS:
                aviso = ('<p style="font-family:var(--maquina);font-size:var(--t-rot);'
                         f'color:var(--falha)">▲ vem de <code>{esc(e["origem"])}</code>, '
                         "que se parte - confirmar se este item é desta aula.</p>")
            itens.append(f'<div class="exercicio">'
                         + moldura(f'EXERCÍCIO {esc(e["n"])}')
                         + f'<div class="exercicio__corpo"><p>{e["html"]}</p>{aviso}</div>'
                         + moldura(None, None, base=True) + "</div>")
        conteudo.append(f'<section class="slide" id="exercicios">'
                        f'<div class="slide__cab"><span class="slide__n">{numero:02d}</span>'
                        f'<h2>Exercícios · {len(d["exercicios"])} itens</h2></div>'
                        + "".join(itens) + "</section>")
        numero += 1

    u = mapa.unidade(a["unidade"])
    barras = "".join('<i data-vista="0"></i>' for _ in range(numero - 1))
    sub = (f'UNIDADE {u["n"]} · AULA {n:02d} DE 26 · CAP. {n} DO LIVRO'
           + (f' · DERIVA {a["deriva"]}' if a["deriva"] else "")
           + (f' · {a["lab"]}' if a["lab"] else ""))

    corpo = f"""<div class="aula" data-aula-slug="{a['slug']}">
{arvore(a['slug'])}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>{esc(a['titulo'])}</h1>
    <p class="sub">{sub}</p>
    <div class="progresso" aria-hidden="true">{barras}</div>
  </div>
{chr(10).join(conteudo)}
{nota_migracao(d)}
  <nav class="nav-pe">
    <a href="{prev}" rel="prev"><div class="tecla-rot">◀ J · ANTERIOR</div><div class="alvo">{esc(prev_rot)}</div></a>
    <div class="meio">AULA {n:02d} / 26</div>
    <a href="{next}" rel="next"><div class="tecla-rot">PRÓXIMA · K ▶</div><div class="alvo">{esc(next_rot)}</div></a>
  </nav>
</main>
</div>"""

    return pagina(
        titulo=f"Aula {n:02d} - {a['titulo']} · POO · UFPB",
        descricao=(f"Aula {n:02d} de 26 da disciplina de Programação Orientada a Objetos "
                   f"em C++17 (UFPB/CI): {a['titulo']}."),
        corpo=corpo, prev=prev, next=next,
        js_extra=("interativo.js", "pecas.js", "pecas-extra.js", "uml.js"),
        migalha=(f'<span class="sep">/</span><span class="unid">UNIDADE {u["n"]}</span>'
                 f'<span class="sep">/</span><span class="atual">AULA {n:02d}</span>'))


def pag_index():
    unidades = []
    for u in mapa.UNIDADES:
        aulas = mapa.por_unidade(u["n"])
        li = []
        for i, a in enumerate(aulas):
            galho = "╰" if i == len(aulas) - 1 else "├"
            marca = '<span class="tem-int">▶</span>' if a["interativos"] else ""
            li.append(f'<li><a href="aula-{a["n"]:02d}.html" data-slug="{a["slug"]}">'
                      f'<span class="galho">{galho}</span><span class="num">{a["n"]:02d}</span>'
                      f'{esc(a["curto"])}{marca}</a></li>')
        slugs = ",".join(a["slug"] for a in aulas)
        unidades.append(f"""<section class="unidade">
  {moldura(f'UNIDADE {u["n"]}', esc(u["rot"]), arredondada=True)}
  <div class="unidade__corpo">
    <p class="unidade__tema" style="margin-top:0">{esc(u["tema"])}</p>
    <ol>{"".join(li)}</ol>
  </div>
  <div class="unidade__pe" data-unidade-conta="{slugs}"><b>0</b>/{len(aulas)} lidas · Deriva {u["deriva"]}</div>
</section>""")

    n_int = sum(len(a["interativos"]) for a in mapa.AULAS)
    n_ex = N_EX
    n_slides = sum(len(CONTEUDO[a["slug"]]["slides"]) for a in mapa.AULAS)
    obrig = [t for t in mapa.TRILHA if not t.get("opcional")]

    atalhos = [
        ("trilha.html", "▸ TRILHA", f"As {len(obrig)} versões do Deriva",
         f"v0.0 → v2.7 · {len(mapa.quebradas())} variantes quebradas de propósito, "
         f"{len(MEDIDAS['variantes_escritas'])} já escritas"),
        ("galeria.html", "▸ INTERATIVOS", "Os oito instrumentos",
         "leiaute · ciclo de vida · despacho · move · posse · SOLID · compilação · rubrica"),
        ("laboratorios.html", "▸ LABORATÓRIOS", "Doze, antes das aulas que os exigem",
         "esqueleto · solução de referência · portão executável"),
        ("rubrica.html", "▸ RUBRICA", "Revisão de código OO gerado por IA",
         "os sete itens das três caças ao bug"),
        ("verifica.html", "▸ PORTÃO", "make verifica",
         "warning · ctest · replay · contadores em zero"),
        ("plano-de-ensino.html", "▸ PLANO", f"Plano de ensino {mapa.SEMESTRE}",
         "15 semanas · 12 laboratórios · avaliação"),
        ("exercicios.html", "▸ EXERCÍCIOS", f"{n_ex} itens, aula por aula",
         "de todas as 26, numa página"),
        ("glossario.html", "▸ REFERÊNCIA", "Glossário e bibliografia",
         f"{len(GLOSSARIO)} verbetes · {len(BIBLIO)} referências auditadas"),
    ]
    ats = "".join(f'<a class="atalho" href="{h}"><span class="atalho__rot">{r}</span>'
                  f'<span class="atalho__nome">{esc(n)}</span>'
                  f'<span class="atalho__nota">{esc(o)}</span></a>'
                  for h, r, n, o in atalhos)

    corpo = f"""<main class="capa">
  <section class="abertura" data-abertura aria-label="Sequência de inicialização">
    <div data-post><span class="fa">$</span> <span class="am">deriva</span> --init</div>
    <div data-post><span class="fa">…</span> UFPB · CENTRO DE INFORMÁTICA · DEPARTAMENTO DE INFORMÁTICA</div>
    <div data-post><span class="fa">…</span> PROGRAMAÇÃO ORIENTADA A OBJETOS · {mapa.SEMESTRE}</div>
    <div data-post><span class="fa">…</span> alvo de linguagem <span class="fr">{mapa.PADRAO}</span> <span class="fa">(-std=c++17 -Wall -Wextra -Wpedantic)</span></div>
    <div data-post><span class="fa">…</span> ftxui v5.0.0 <span class="ok">OK</span> · catch2 <span class="ok">OK</span> · make verifica <span class="ok">OK</span></div>
    <div data-post><span class="fa">…</span> 26 aulas · {n_slides} slides · {n_ex} exercícios · {len(obrig)} versões do Deriva · 12 laboratórios</div>
    <div data-post><span class="fa">…</span> sonda de inspeção <span class="am">montada</span> - a estação orbital não responde</div>
    <div data-post><span class="ok">▸</span> sistema pronto <span class="cursor">█</span></div>
    <button class="saltar" type="button" data-saltar>pressione qualquer tecla para saltar</button>
  </section>

  <div class="capa__tit">
    <h1>Programação <em>Orientada a Objetos</em> em C++</h1>
    <p class="linha">A disciplina se organiza através de um sistema único, construído do começo
    ao fim do semestre: o <strong>Deriva</strong>, um roguelike de terminal no qual uma sonda de
    inspeção percorre uma estação orbital abandonada. Cada aula entrega uma versão que compila e,
    nas aulas em que o defeito ensina mais que o acerto, também uma variante deliberadamente
    quebrada, acompanhada do roteiro de observação.</p>
    <div class="capa__meta">
      <span>Prof. <b>{esc(mapa.AUTOR)}</b></span>
      <span>alvo <b>{mapa.PADRAO}</b></span>
      <span><b>26</b> aulas · <b>3</b> unidades · <b>3</b> anexos</span>
      <span><b>{n_ex}</b> exercícios</span>
      <span><b>12</b> laboratórios</span>
      <span><b>{n_int}</b> interativos em <b>8</b> tipos</span>
    </div>
  </div>

  <section class="heroi" data-heroi-vtable aria-label="Animação: uma chamada virtual sendo resolvida pela vtable">
    {moldura("DESPACHO DINÂMICO", "entidade* → desenhar()", sistema=True)}
    <div class="hv__palco" data-heroi-palco></div>
    <div class="hv__terminal">
      <span class="rot">TERMINAL DA ESTAÇÃO</span>
      <span class="hv__saida" data-heroi-saida></span>
    </div>
    <div class="hv__controles">
      <button class="bt" type="button" data-heroi="virtual" aria-pressed="true">✓ virtual LIGADO</button>
      <button class="bt" type="button" data-heroi="modo">││ PASSO A PASSO</button>
      <button class="bt bt--primario" type="button" data-heroi="passo" hidden>PASSO ▶</button>
      <span class="hv__est" data-heroi-est></span>
    </div>
    <div class="heroi__legenda">
      <span class="rot">ONDE OLHAR</span>
      <p>O que interessa aqui é o caminho da chamada, e não a disposição dos blocos: com
      <code>virtual</code>, a chamada entra no objeto, lê o <code>vptr</code> e alcança a
      função definida pela classe real. <strong>Desligue o <code>virtual</code></strong> e o
      caminho tracejado deixa de entrar no objeto, e as três entidades saem como
      <code>·</code>, porque a decisão passou a ser tomada pelo tipo do ponteiro, sem que o
      compilador emita um único warning. O mecanismo é desenvolvido na
      <a href="aula-11.html">Aula 11</a>.</p>
    </div>
    {moldura(None, None, sistema=True, base=True)}
  </section>

  <h2 id="conteudo" style="font-family:var(--maquina);font-size:var(--t-rot);letter-spacing:.18em;color:var(--fosforo);margin:var(--e5) 0 0;font-weight:500">├─ AS 26 AULAS</h2>
  <div class="unidades">{"".join(unidades)}</div>
  <div class="atalhos">{ats}</div>
</main>"""

    return pagina(titulo=f"Programação Orientada a Objetos em C++ · POO · UFPB",
                  descricao=("Material interativo de Programação Orientada a Objetos em "
                             "C++17 - UFPB, Centro de Informática. 26 aulas em 3 unidades, "
                             "com oito tipos de exemplo interativo e o sistema Deriva."),
                  og=(f"26 aulas, {n_slides} slides, {n_ex} exercícios e oito instrumentos "
                      "que mostram o que a execução real não mostra: vtable, leiaute de "
                      "objeto, contagem de referências."),
                  corpo=corpo, css_extra=("index.css",), js_extra=("heroi-vtable.js",),
                  next="aula-01.html", com_arvore=False,
                  migalha=f'<span class="sep">/</span><span class="atual">{mapa.SEMESTRE}</span>')


def pag_galeria():
    """T2 + T9 + T11 num só lugar: é aqui que os oito se calibram."""
    secoes = []
    ordem = ["inspetor", "ciclo", "virtual", "move", "posse", "refator",
             "expansor", "revisor", "corrida"]
    for i, chave in enumerate(ordem, 1):
        d = mapa.INTERATIVOS[chave]
        aulas = ", ".join(f'<a href="aula-{n:02d}.html">{n:02d}</a>' for n in d["aulas"])
        extra = ('<span style="color:var(--outro)"> · reaproveitado de LPII</span>'
                 if d.get("reaproveitado") else "")
        secoes.append(f"""<section class="slide">
  <div class="slide__cab"><span class="slide__n">{i:02d}</span><h2>{esc(d["titulo"])}
    <span style="font-family:var(--maquina);font-size:var(--t-rot);color:var(--apagado);letter-spacing:.1em">· AULAS {aulas}{extra}</span></h2></div>
  <p>{esc(d["nota"]).capitalize()}.</p>
  <section data-int="{chave}" tabindex="0"></section>
</section>""")

    secoes.append(uml_html("T9", 6))

    n_int = sum(len(a["interativos"]) for a in mapa.AULAS)
    n_ex = N_EX
    n_slides = sum(len(CONTEUDO[a["slug"]]["slides"]) for a in mapa.AULAS)

    corpo = f"""<main class="pg" style="padding:0 var(--goteira) var(--e5)">
  <div class="cabeca-aula">
    <h1>Os oito instrumentos</h1>
    <p class="sub">UMA MOLDURA · OITO TIPOS · {n_int} USOS NAS 26 AULAS</p>
  </div>

  <section class="slide" id="conteudo">
    <p>Os oito instrumentos compartilham a mesma moldura e o mesmo contrato: o estado exibido é
    função de <em>(cenário, passo)</em>, o avanço do passo é sempre seu, cada peça oferece ao
    menos um cenário que <strong>demonstra a falha</strong> e outro que a evita, e o painel de
    estado expõe aquilo que a execução real mantém invisível - o <code>vptr</code>, o
    <em>padding</em> entre membros, a contagem de referências, o objeto de origem depois de um
    <code>std::move</code> e o ramo que o <code>if constexpr</code> podou.</p>
    <p style="font-family:var(--maquina);font-size:var(--t-est);color:var(--apagado)">Com o
    foco dentro de uma peça, <b style="color:var(--fosforo)">←</b> e
    <b style="color:var(--fosforo)">→</b> movem o passo e <b style="color:var(--fosforo)">R</b>
    reinicia o cenário. Nenhuma das peças tem botão de <em>play</em>, porque autoplay sem
    controle de passo é recusado pelo contrato que <code>build/verifica_pecas.js</code>
    confere, e o motor não chega a ter tal função para oferecer.</p>
  </section>

{chr(10).join(secoes)}

  <section class="slide">
    <div class="slide__cab"><span class="slide__n">T11</span><h2>Estados vazios e de erro</h2></div>
    <p>A mensagem de sistema é nativa deste idioma visual, e o estado vazio se resolve no
    próprio terminal, com a busca que falhou e as três consultas mais próximas.</p>
    <div class="vazio-sistema">
      {moldura("BUSCA", sistema=True)}
      <div class="vazio-sistema__corpo">
        <div>$ buscar "monad"</div>
        <div><b>nenhum resultado em 26 aulas, {n_slides} slides, {n_ex} exercícios.</b></div>
        <div style="margin-top:var(--e2);color:var(--fantasma)">tente:
          <a href="glossario.html#polimorfismo">polimorfismo</a> ·
          <a href="glossario.html#raii">RAII</a> ·
          <a href="glossario.html#move">semântica de movimento</a></div>
        <div style="margin-top:var(--e2)">$ <span class="cursor">█</span></div>
      </div>
      {moldura(None, None, sistema=True, base=True)}
    </div>
  </section>

  <nav class="nav-pe">
    <a href="index.html" rel="prev"><div class="tecla-rot">◀ J · CAPA</div><div class="alvo">Índice das 26 aulas</div></a>
    <div class="meio">8 TIPOS + UML</div>
    <a href="trilha.html" rel="next"><div class="tecla-rot">TRILHA · K ▶</div><div class="alvo">As 20 versões do Deriva</div></a>
  </nav>
</main>"""

    return pagina(titulo="Os oito instrumentos · POO · UFPB",
                  descricao=("Os oito interativos canônicos da disciplina, mais o diagrama "
                             "de classes interativo: o que a execução real não mostra."),
                  corpo=corpo, prev="index.html", next="trilha.html", com_arvore=False,
                  js_extra=("interativo.js", "pecas.js", "pecas-extra.js", "uml.js"),
                  migalha='<span class="sep">/</span><span class="atual">OS OITO INSTRUMENTOS</span>')


def pag_trilha():
    linhas = []
    for t in mapa.TRILHA:
        aulas = ", ".join(f'<a href="aula-{n:02d}.html">Aula {n:02d}</a>' for n in t["aula"])
        selo = ' <span class="c20">C++20</span>' if t.get("c20") else ""
        opc = (' <span style="color:var(--outro)">· opcional, fora do padrão-alvo</span>'
               if t.get("opcional") else "")
        linhas.append(f"""<div class="versao">
  <div class="versao__tag">{t["v"]}{selo}<span class="aula">{aulas or "anexo A"}</span></div>
  <div class="versao__o">
    <div class="versao__entrega">{esc(t["entrega"])}{opc}</div>
    <div class="versao__conc">{esc(t["conceitos"])}</div>
    <div class="versao__testes">{selo_testes(t, acumulado_ate(t["v"]))}</div>
  </div>
</div>""")
        if t.get("quebrada"):
            tag, o_que, como = t["quebrada"]
            linhas.append(f"""<div class="versao versao--quebrada">
  <div class="versao__tag">{tag}<span class="aula">{aulas}</span></div>
  <div class="versao__o">
    <span class="aviso-proposito">▲ QUEBRADA DE PROPÓSITO</span>
    <div class="versao__entrega">{esc(o_que)}</div>
    <div class="versao__conc">{esc(como)}</div>
    <div class="versao__testes">▲ falha esperada - o erro é o conteúdo</div>
  </div>
</div>""")

    obrig = [t for t in mapa.TRILHA if not t.get("opcional")]
    corpo = f"""<div class="aula">
{arvore("trilha.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>A trilha do Deriva</h1>
    <p class="sub">{len(obrig)} VERSÕES OBRIGATÓRIAS + 1 OPCIONAL (C++20) · {len(mapa.quebradas())} VARIANTES QUEBRADAS</p>
  </div>
  <section class="slide">
    <p>A trilha entrega uma versão por aula, todas compilando com <code>-std=c++17 -Wall
    -Wextra -Wpedantic</code> e zero warning no código do estudante; o FTXUI e o Catch2
    entram como dependência <code>SYSTEM</code> de forma que o portão incida apenas sobre o
    que você escreveu, sem contar o que essas bibliotecas emitem.</p>
    <!-- voz:permitido - a atribuição é histórica e verdadeira: as variantes
         vieram mesmo do sistema-base anterior, e dizer de onde veio o melhor
         recurso do material é honestidade, não resíduo de migração. -->
    <p>As variantes quebradas foram preservadas do sistema-base anterior, onde eram o
    recurso pedagógico de maior rendimento, e estão aqui como conteúdo, cada uma com tag
    própria e roteiro de observação. É delas que saem as três <strong>caças ao bug</strong>
    do semestre, nas semanas 5, 9 e 13.</p>
    <p style="font-family:var(--maquina);font-size:var(--t-rot);color:var(--apagado);letter-spacing:.08em">
    <span style="color:var(--ok)">✓ medidos</span> = o ctest passa esse número hoje, contado
    pela declaração de versão que cada arquivo de teste traz na primeira linha ·
    <span style="color:var(--apagado)">◇ nenhum teste próprio</span> = a versão existe e
    compila, e os testes dela vivem na versão vizinha ou no alvo opcional</p>
    <p style="font-family:var(--maquina);font-size:var(--t-rot);color:var(--apagado);letter-spacing:.08em">
    A trilha tem {sum(MEDIDAS.get("testes_por_versao", {}).values())} testes; os outros
    {sum(MEDIDAS.get("testes_por_aula", {}).values())} medem material de aula, fora do jogo,
    e os 12 laboratórios fecham os {MEDIDAS["testes"]} do portão.</p>
    <div class="trilha">{"".join(linhas)}</div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">·</span><h2>A trilha anterior</h2></div>
    <!-- Este slide dizia três coisas, e duas saíram.
         (1) "Os 15 callouts que o citavam passaram ao tipo deriva" era
             contabilidade interna da migração dirigida ao estudante, que não
             tem o que fazer com tipo de callout - e o número já era falso:
             foram 521 referências reescritas, não 15.
         (2) "o repositório e as tags seguem no ar" é afirmação sobre estado
             de infraestrutura que este material não tem como verificar, e
             material não afirma o que não pode conferir.
         O que ficou é a única das três que é decisão de ensino, e ela é do
         docente: a trilha anterior segue oferecida a quem estava no meio do
         caminho. -->
    <p>O sistema-base até 2026.1 era um mini-DAW de 17 versões, e ele segue oferecido como
    <strong>trilha alternativa</strong> a quem estiver no meio do semestre e preferir não
    trocar o chão sob os pés. Fale com o docente: a equivalência entre as duas trilhas é
    caso a caso, e a entrega é a mesma - o portão de quatro condições não muda.</p>
  </section>
  <nav class="nav-pe">
    <a href="galeria.html" rel="prev"><div class="tecla-rot">◀ J · INTERATIVOS</div><div class="alvo">Os oito instrumentos</div></a>
    <div class="meio">{len(obrig)} VERSÕES</div>
    <a href="laboratorios.html" rel="next"><div class="tecla-rot">LABORATÓRIOS · K ▶</div><div class="alvo">Os 12 preparatórios</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="A trilha do Deriva · POO · UFPB",
                  descricao=(f"As {len(obrig)} versões do Deriva, uma por aula, com as "
                             "variantes deliberadamente quebradas e as três caças ao bug."),
                  corpo=corpo, prev="galeria.html", next="laboratorios.html",
                  migalha='<span class="sep">/</span><span class="atual">TRILHA</span>')


EXTENSO = {0: "nenhum", 1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco",
           6: "seis", 7: "sete", 8: "oito", 9: "nove", 10: "dez", 11: "onze",
           12: "doze"}


def pag_laboratorios():
    """T12 - seção nova do site: esqueleto, solução revelável e portão, 12×.

    A distribuição por unidade não é digitada: sai de `mapa.LABS` cruzado com a
    unidade de cada aula, porque a prosa que conta o que a tabela canônica
    declara é a primeira a envelhecer quando a tabela muda.
    """
    itens = []
    n_labs = len(mapa.LABS)
    for l in mapa.LABS:
        a = mapa.aula(l["aula"])
        pasta = l["id"].lower().replace("lab-", "lab-")
        comando = (f'./portao.sh /caminho/do/seu/repo'
                   if l["id"] == "LAB-03"
                   else f'g++ -std=c++17 -Wall -Wextra -Wpedantic '
                        f'-I../../include esqueleto.cpp -o meu && ./meu')
        itens.append(f"""<section class="slide" id="{l["id"].lower()}">
  <div class="slide__cab"><span class="slide__n">{l["id"]}</span><h2>{esc(l["titulo"])}</h2></div>
  <p style="font-family:var(--maquina);font-size:var(--t-est);color:var(--apagado)">
    prepara a <a href="aula-{a["n"]:02d}.html">Aula {a["n"]:02d} · {esc(a["curto"])}</a>
    {f'· Deriva {a["deriva"]}' if a["deriva"] else ''}</p>
  <div class="exercicio">
    {moldura(f'PORTÃO DE CORREÇÃO · {l["id"]}')}
    <div class="exercicio__corpo">
      <p>{esc(l["portao"])}.</p>
      <details>
        <summary>ESQUELETO, SOLUÇÃO E COMO RODAR</summary>
        <div style="padding:var(--e2) 0">
          <p><code>exemplos/deriva/laboratorios/{pasta}/</code> traz o enunciado
          completo em <code>LEIA-ME.md</code>, o <code>esqueleto</code> que compila e
          falha o portão de propósito, e a <code>solução de referência</code>.</p>
          <div class="codigo__pe" style="border:var(--rule-w) solid var(--grade)">
            <code>{comando}</code>
          </div>
          <p>Começar de algo que constrói é deliberado: quem começa de arquivo que não
          compila gasta a primeira hora com erro de sintaxe em vez de com o conceito. A
          solução de referência não é a única resposta certa - o portão é que decide, e
          se o seu programa passa e você consegue explicar por quê, ele está certo mesmo
          sem se parecer com ela.</p>
          <p style="font-family:var(--maquina);font-size:var(--t-rot);color:var(--ok)">
          ✓ as {n_labs} soluções são compiladas e executadas pelo <code>ctest</code> a cada
          build - solução publicada que não compila é pior que solução ausente</p>
        </div>
      </details>
    </div>
    {moldura(None, None, base=True)}
  </div>
</section>""")

    por_unidade = {u["n"]: sum(1 for l in mapa.LABS
                               if mapa.aula(l["aula"])["unidade"] == u["n"])
                   for u in mapa.UNIDADES}
    partes_dist = [f'{EXTENSO[por_unidade[u["n"]]]} na Unidade {u["n"]}'
                   for u in mapa.UNIDADES]
    dist = ", ".join(partes_dist[:-1]) + " e " + partes_dist[-1]

    corpo = f"""<div class="aula">
{arvore("laboratorios.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Os 12 laboratórios preparatórios</h1>
    <p class="sub">UM ANTES DE CADA AULA QUE DEPENDE DELE · PORTÃO DE CORREÇÃO EXECUTÁVEL</p>
  </div>
  <section class="slide">
    <p>Cada laboratório se faz <em>antes</em> da aula que depende dele, e é composto de
    esqueleto, solução de referência e portão de correção. O portão é executável: é o mesmo
    <code>make verifica</code> pelo qual a entrega passa, de forma que o critério de aceitação
    esteja na sua mão antes da entrega.</p>
    <p>A distribuição segue a ordem em que o <a href="plano-de-ensino.html">plano de
    ensino</a> os pede, e é de {dist}.</p>
  </section>
{"".join(itens)}
  <nav class="nav-pe">
    <a href="trilha.html" rel="prev"><div class="tecla-rot">◀ J · TRILHA</div><div class="alvo">As 20 versões do Deriva</div></a>
    <div class="meio">12 LABORATÓRIOS</div>
    <a href="rubrica.html" rel="next"><div class="tecla-rot">RUBRICA · K ▶</div><div class="alvo">Revisão de código gerado por IA</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="Os 12 laboratórios preparatórios · POO · UFPB",
                  descricao=("Os doze laboratórios preparatórios da disciplina, com "
                             "esqueleto, solução de referência e portão de correção."),
                  corpo=corpo, prev="trilha.html", next="rubrica.html",
                  migalha='<span class="sep">/</span><span class="atual">LABORATÓRIOS</span>')


# A rubrica vive em `conteudo/mapa.py`, e só lá: ela existia aqui, no Cap. 04
# do livro e nos comentários do código com defeitos plantados, com três
# numerações diferentes.
RUBRICA = [(r["id"], r["titulo"], r["pergunta"], r["costuma_aparecer"])
           for r in mapa.RUBRICA]

def pag_rubrica():
    """T13 - a rubrica como instrumento com que se trabalha, não texto que se lê."""
    linhas = "".join(f"""<div class="versao">
  <div class="versao__tag">{r}<span class="aula">verifique</span></div>
  <div class="versao__o">
    <div class="versao__entrega">{esc(t)}</div>
    <div class="versao__conc">{p}</div>
    <div class="versao__testes" style="color:var(--falha)">▲ o que costuma aparecer: {c}</div>
  </div>
</div>""" for r, t, p, c in RUBRICA)

    corpo = f"""<div class="aula">
{arvore("rubrica.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Rubrica de revisão de código OO gerado por IA</h1>
    <p class="sub">7 ITENS · INSTRUMENTO DAS TRÊS CAÇAS AO BUG · AULA 04</p>
  </div>
  <section class="slide">
    <p>A rubrica chega na <a href="aula-04.html">Aula 04</a>, ainda na segunda semana,
    porque é com ela que você trabalha nas três caças ao bug das semanas 5, 9 e 13, e um
    instrumento de trabalho precisa estar disponível antes da tarefa que o exige.</p>
    <p>O código que um modelo de linguagem gera para um exercício de POO é quase sempre
    plausível, e quase sempre defeituoso nos mesmos sete lugares; a rubrica enumera tais
    lugares na ordem em que compensa olhar, de forma que a revisão comece pela posse do
    recurso e termine no que o teste efetivamente prova.</p>
    <div class="trilha">{linhas}</div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">·</span><h2>A rubrica em uso</h2></div>
    <p>O interativo do tipo 8 - <strong>revisor com rubrica</strong> - apresenta um trecho
    gerado, plausível e defeituoso, e acende a falha correspondente a cada item que você
    marca; assim a rubrica se exercita sobre código, em vez de ficar na própria descrição.
    A peça aparece nas Aulas <a href="aula-04.html">04</a>,
    <a href="aula-06.html">06</a> e <a href="aula-23.html">23</a>, e está calibrada na
    <a href="galeria.html#int-revisor">galeria</a>.</p>
    <section data-int="revisor" tabindex="0"></section>
  </section>
  <nav class="nav-pe">
    <a href="laboratorios.html" rel="prev"><div class="tecla-rot">◀ J · LABORATÓRIOS</div><div class="alvo">Os 12 preparatórios</div></a>
    <div class="meio">7 ITENS</div>
    <a href="verifica.html" rel="next"><div class="tecla-rot">PORTÃO · K ▶</div><div class="alvo">make verifica</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="Rubrica de revisão de código gerado por IA · POO · UFPB",
                  descricao=("Os sete itens da rubrica de revisão de código orientado a "
                             "objetos gerado por IA, instrumento das três caças ao bug."),
                  corpo=corpo, prev="laboratorios.html", next="verifica.html",
                  js_extra=("interativo.js", "pecas.js", "pecas-extra.js"),
                  migalha='<span class="sep">/</span><span class="atual">RUBRICA</span>')


def pag_verifica():
    portoes = [
        ("warning", "g++ -std=c++17 -Wall -Wextra -Wpedantic",
         "zero warning <strong>no código do estudante</strong>. O FTXUI e o Catch2 entram "
         "por <code>FetchContent</code> como <code>SYSTEM</code>, de forma que o que essas "
         "bibliotecas emitem fique fora da conta, porém também não sirva de abrigo para um "
         "warning seu."),
        ("testes", "ctest --test-dir build",
         "todos verdes. Nas variantes deliberadamente quebradas a falha é esperada, e o "
         "roteiro de observação de cada uma diz o que se deve ver."),
        ("replay", "./deriva --replay roteiro.txt --semente 7 | diff - esperado.txt",
         "despejo idêntico byte a byte. É o oráculo das Aulas 16, 24 e 25, nas quais uma "
         "refatoração se considera correta quando a saída do roteiro não muda."),
        ("contadores", "grep 'vivos=0' saida.txt",
         "o contador de instâncias vivas fecha em zero no fim de <code>main</code>, o que "
         "acusa qualquer destrutor que deixou de rodar, sem depender de ferramenta externa."),
    ]
    linhas = "".join(f"""<div class="versao">
  <div class="versao__tag">{p}<span class="aula">portão</span></div>
  <div class="versao__o">
    <div class="versao__entrega"><code>{esc(cmd)}</code></div>
    <div class="versao__conc">{txt}</div>
  </div>
</div>""" for p, cmd, txt in portoes)

    make = """verifica: build
\t@cmake --build build --parallel
\t@ctest --test-dir build --output-on-failure
\t@./build/deriva --replay roteiro.txt --semente 7 | diff - esperado.txt
\t@./build/deriva --contadores | grep -q 'vivos=0' \\
\t  || { echo "FALHA: contador de instancias nao fechou em zero"; exit 1; }
\t@echo "verifica: OK"
"""
    corpo = f"""<div class="aula">
{arvore("verifica.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>O portão <code>make verifica</code></h1>
    <p class="sub">WARNING · CTEST · REPLAY · CONTADORES EM ZERO</p>
  </div>
  <section class="slide">
    <p>São quatro condições, verificadas por uma linha de comando, e o critério é o mesmo
    para você e para a correção. Nenhuma nota de estilo subjetiva se esconde aqui: o portão
    aceita exatamente o que a disciplina exige, e o que ele recusa vem com a mensagem que
    diz por quê; você pode rodar a correção antes de entregar.</p>
    <p>Sanitizer <strong>não</strong> está na lista, e a ausência é deliberada: as máquinas
    do laboratório não os têm, de forma que o portão não pode depender deles, e o ASan
    aparece no <a href="aula-02.html">Cap. 2</a> como ferramenta de investigação. O que
    ocupa esse lugar é um bloco de três técnicas sem dependência externa: o contador
    <code>vivos</code> (<a href="aula-07.html">Aula 07</a>), a instrumentação de ciclo de
    vida (<a href="aula-08.html">Aula 08</a>) e o <code>gdb</code> com ponto de parada em
    destrutor (<a href="aula-11.html">Aula 11</a>).</p>
    <div class="trilha">{linhas}</div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">·</span><h2>O alvo, como está no Makefile</h2></div>
    {bl_codigo({"lang": "make", "legenda": "Makefile", "codigo": make})}
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">·</span><h2><code>DECISAO.md</code></h2></div>
    <p>Toda entrega vem acompanhada de um <code>DECISAO.md</code> curto, no qual você
    registra o que foi decidido, o que foi descartado e por qual razão. São poucas linhas, e
    valem nota. A correção verifica se a decisão está <em>declarada</em> e se o código a
    cumpre, e não se ela coincide com a que o docente teria tomado: alternativa defensável e
    assumida vale tanto quanto a canônica.</p>
  </section>
  <nav class="nav-pe">
    <a href="rubrica.html" rel="prev"><div class="tecla-rot">◀ J · RUBRICA</div><div class="alvo">Revisão de código gerado por IA</div></a>
    <div class="meio">4 CONDIÇÕES</div>
    <a href="plano-de-ensino.html" rel="next"><div class="tecla-rot">PLANO · K ▶</div><div class="alvo">Plano de ensino 2026.2</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="O portão make verifica · POO · UFPB",
                  descricao=("As quatro condições do portão de correção da disciplina: "
                             "warning, ctest, replay determinístico e contadores em zero."),
                  corpo=corpo, prev="rubrica.html", next="plano-de-ensino.html",
                  migalha='<span class="sep">/</span><span class="atual">PORTÃO</span>')


def pag_plano():
    """T14 - o plano de ensino publicado. Tabelas densas, cronograma de 15 semanas."""
    sem = []
    aulas = list(mapa.AULAS)
    for s in range(1, 16):
        if s == 15:
            sem.append((s, "reserva", ["Encontro de reserva - E1 saiu do cronograma fixo"]))
            continue
        par = aulas[(s - 1) * 2:(s - 1) * 2 + 2]
        rot = []
        for a in par:
            extra = []
            if a["deriva"]:
                extra.append(f'Deriva {a["deriva"]}')
            if a["lab"]:
                extra.append(a["lab"])
            rot.append(f'<a href="aula-{a["n"]:02d}.html">{a["n"]:02d} · {esc(a["curto"])}</a>'
                       + (f' <span style="color:var(--fantasma)">({", ".join(extra)})</span>'
                          if extra else ""))
        marca = ""
        if s == 5:
            marca = " · CAÇA AO BUG 1"
        elif s == 9:
            marca = " · CAÇA AO BUG 2"
        elif s == 13:
            marca = " · CAÇA AO BUG 3"
        sem.append((s, f"semana {s}{marca}", rot))

    linhas = "".join(f"""<div class="versao{' versao--quebrada' if 'CAÇA' in r else ''}">
  <div class="versao__tag">S{n:02d}<span class="aula">{esc(r.split(' · ')[-1]) if 'CAÇA' in r else ''}</span></div>
  <div class="versao__o">{''.join(f'<div class="versao__entrega">{x}</div>' for x in xs)}</div>
</div>""" for n, r, xs in sem)

    labs = "".join(f'<tr><td><a href="laboratorios.html#{l["id"].lower()}">{l["id"]}</a></td>'
                   f'<td>{esc(l["titulo"])}</td>'
                   f'<td><a href="aula-{l["aula"]:02d}.html">Aula {l["aula"]:02d}</a></td>'
                   f'<td>{esc(l["portao"])}</td></tr>' for l in mapa.LABS)

    corpo = f"""<div class="aula">
{arvore("plano-de-ensino.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Plano de ensino · {mapa.SEMESTRE}</h1>
    <p class="sub">26 AULAS · 15 SEMANAS · 12 LABORATÓRIOS · ALVO {mapa.PADRAO}</p>
  </div>
  <section class="slide">
    <p>Esta é a versão publicada do plano de ensino. O documento de origem é
    <code>PLANO_DE_ENSINO_POO_v2.md</code>, e tanto o site quanto o livro derivam dele
    através do mesmo build; assim, uma correção no plano chega às duas saídas de uma
    vez.</p>
    <div class="codigo__pe" style="border:var(--rule-w) solid var(--grade)">
      <a href="plano-de-ensino.docx">baixar em .docx</a> ·
      <span style="color:var(--falha)">▲ o .docx ainda não foi gerado neste build</span>
    </div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">01</span><h2>Cronograma</h2></div>
    <p>São duas aulas por semana ao longo de catorze semanas de conteúdo, mais uma décima
    quinta semana de reserva, que existe para absorver atraso sem que se perca conteúdo. As
    três caças ao bug caem nas semanas 5, 9 e 13, cada uma sobre uma variante
    deliberadamente quebrada do Deriva.</p>
    <div class="trilha">{linhas}</div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">02</span><h2>Os 12 laboratórios</h2></div>
    <div style="overflow-x:auto"><table class="tabela"><thead><tr><th>id</th><th>título</th>
    <th>prepara</th><th>portão</th></tr></thead><tbody>{labs}</tbody></table></div>
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">03</span><h2>Pendências declaradas</h2></div>
    <p>Três lacunas do plano dependem de fonte externa e ficam registradas aqui, em vez de
    preenchidas por adivinhação: o <strong>código do componente e o pré-requisito</strong>,
    que saem do SIGAA e do PPC; a <strong>ementa do PPC</strong> transcrita literalmente, já
    que a ementa em uso é de trabalho; e a decisão sobre a <strong>Central de
    Alertas</strong> como exercício integrador do semestre.</p>
  </section>
  <nav class="nav-pe">
    <a href="verifica.html" rel="prev"><div class="tecla-rot">◀ J · PORTÃO</div><div class="alvo">make verifica</div></a>
    <div class="meio">15 SEMANAS</div>
    <a href="anexo-a.html" rel="next"><div class="tecla-rot">ANEXO A · K ▶</div><div class="alvo">Concepts e Ranges</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo=f"Plano de ensino {mapa.SEMESTRE} · POO · UFPB",
                  descricao=("Plano de ensino da disciplina de Programação Orientada a "
                             "Objetos, UFPB/CI: 26 aulas, 15 semanas, 12 laboratórios."),
                  corpo=corpo, prev="verifica.html", next="anexo-a.html",
                  migalha='<span class="sep">/</span><span class="atual">PLANO DE ENSINO</span>')


C17_REF = [
    ("std::string_view", "3", "<code>void f(std::string_view s)</code>",
     "não possui os bytes que enxerga, e um <code>string_view</code> guardado além da vida "
     "da <code>string</code> de origem fica pendurado"),
    ("ligações estruturadas", "3", "<code>for (auto&amp; [pos, cel] : mapa)</code>",
     "sem o <code>&amp;</code> a ligação copia o elemento; use <code>const auto&amp;</code> "
     "quando o laço apenas lê"),
    ("[[nodiscard]]", "3, 7", "<code>[[nodiscard]] bool carregar(...)</code>",
     "vale no que retorna status ou recurso, e o warning que ele provoca é o objetivo"),
    ("[[maybe_unused]]", "3", "<code>[[maybe_unused]] int n = f();</code>",
     "para o parâmetro que só é usado dentro de <code>assert</code> ou em um dos ramos "
     "compilados"),
    ("if constexpr", "19", "<code>if constexpr (std::is_integral_v&lt;T&gt;)</code>",
     "poda o ramo em tempo de compilação, e o ramo podado nem precisa ser válido para o "
     "<code>T</code> em questão"),
    ("std::optional", "20", "<code>std::optional&lt;mapa&gt; carregar(...)</code>",
     "modela ausência, e não falha; para reportar erro, use exceção ou "
     "<code>variant</code>"),
    ("std::variant", "20", "<code>std::variant&lt;mapa, erro&gt;</code>",
     "soma de tipos fechada, consultada com <code>std::visit</code>; o acesso por "
     "<code>get</code> com o tipo errado lança"),
    ("std::filesystem", "20", "<code>fs::exists(caminho)</code>",
     "verificar a existência e abrir são duas operações, e a corrida entre elas é real: "
     "abra e trate a falha"),
    ("std::clamp", "21", "<code>std::clamp(x, 0, largura - 1)</code>",
     "substitui o par <code>min</code>/<code>max</code> aninhado, porém devolve "
     "referência - não o alimente com temporário"),
    ("lambdas", "21, 25", "<code>[&amp;](const auto&amp; e) { return e.vivo(); }</code>",
     "Strategy sem herança; a captura por referência só é segura enquanto vive o escopo "
     "capturado"),
    ("std::forward", "14", "<code>template&lt;class T&gt; void add(T&amp;&amp; x)</code>",
     "encaminhamento perfeito; <code>T&amp;&amp;</code> em parâmetro de template dedutível "
     "é referência universal, e não referência a rvalue"),
    ("CTAD", "15", "<code>std::pair p{1, 2.0};</code>",
     "dedução a partir do construtor, o que dispensa <code>make_pair</code>; agregado "
     "próprio pode exigir guia de dedução"),
    ("fold expressions", "19", "<code>return (... + args);</code>",
     "variádico sem recursão; o pacote vazio exige valor inicial ou operador com "
     "identidade definida"),
    ("inline variables", "7", "<code>inline static int vivos = 0;</code>",
     "membro estático definido no próprio cabeçalho, sem a definição avulsa no "
     "<code>.cpp</code> que o C++14 exigia"),
    ("std::byte", "7", "<code>std::byte b{0xFF};</code>",
     "não é aritmético nem caractere, e a conversão para inteiro passa por "
     "<code>std::to_integer</code>"),
]


def pag_anexos():
    saidas = {}

    # ---- Anexo A: o Cap. 20 rebaixado, com o conteúdo real do v1 -----------
    an = mapa.ANEXOS[0]
    d = CONTEUDO["anexo-a"]
    secoes = []
    for i, s in enumerate(d["slides"], 1):
        secoes.append(f'<section class="slide" id="{esc(s["id"]) or f"s{i}"}">'
                      f'<div class="slide__cab"><span class="slide__n">{i:02d}</span>'
                      f'<h2>{esc(s["titulo"])} <span class="c20">C++20</span></h2></div>'
                      f'{blocos(s["blocos"])}</section>')
    corpo = f"""<div class="aula">
{arvore("anexo-a.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Anexo A · Concepts e Ranges <span class="c20">C++20</span></h1>
    <p class="sub">CONTEÚDO FORA DO PADRÃO-ALVO · 20 MINUTOS NA AULA 19 · DERIVA {an["deriva"]}</p>
  </div>
  <section class="slide">
    <aside class="callout" data-t="info">
      {moldura("· NOTA · MUDANÇA DE ESTATUTO")}
      <div class="callout__corpo"><p>{esc(an["nota"])}</p>
      <p>Nenhum exemplo do material obrigatório depende deste anexo, e o que está aqui
      compila em alvo separado e opcional, com <code>-std=c++20</code>. A
      <a href="aula-19.html">Aula 19</a> o referencia em vinte minutos, como panorama de
      para onde a linguagem foi depois do padrão-alvo da disciplina.</p></div>
      {moldura(None, None, base=True)}
    </aside>
  </section>
{"".join(secoes)}
  <nav class="nav-pe">
    <a href="plano-de-ensino.html" rel="prev"><div class="tecla-rot">◀ J · PLANO</div><div class="alvo">Plano de ensino</div></a>
    <div class="meio">ANEXO A</div>
    <a href="anexo-b.html" rel="next"><div class="tecla-rot">ANEXO B · K ▶</div><div class="alvo">Referência rápida de C++17</div></a>
  </nav>
</main>
</div>"""
    saidas["anexo-a.html"] = pagina(
        titulo="Anexo A - Concepts e Ranges (C++20) · POO · UFPB",
        descricao=("Concepts e Ranges como anexo rotulado C++20: conteúdo que mudou de "
                   "estatuto porque o alvo da disciplina é C++17."),
        corpo=corpo, prev="plano-de-ensino.html", next="anexo-b.html",
        migalha='<span class="sep">/</span><span class="atual">ANEXO A</span>')

    # ---- Anexo B: referência rápida de C++17 (nova) ------------------------
    linhas = "".join(
        f'<tr><td><code>{c}</code></td><td>{cap}</td><td>{ex}</td><td>{nota}</td></tr>'
        for c, cap, ex, nota in C17_REF)
    corpo = f"""<div class="aula">
{arvore("anexo-b.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Anexo B · Referência rápida de C++17</h1>
    <p class="sub">CONSULTA DE PROVA E DE LABORATÓRIO · {len(C17_REF)} CONSTRUÇÕES</p>
  </div>
  <section class="slide">
    <p>A tabela existe por uma razão aferida no material anterior: o livro v1 se declarava
    C++17 em doze lugares e não tinha uma única ocorrência de <code>string_view</code>, de
    ligações estruturadas, de <code>[[nodiscard]]</code>, de <code>std::forward</code>, de
    <code>std::filesystem</code> ou de <code>std::tuple</code>, ao mesmo tempo que ensinava
    Concepts e Ranges, que são C++20. Está aqui o que passou a ser exigido, com o capítulo
    em que cada construção entra e a armadilha que costuma acompanhá-la.</p>
    <div style="overflow-x:auto"><table class="tabela"><thead><tr><th>construção</th>
    <th>cap.</th><th>forma</th><th>o que costuma dar errado</th></tr></thead>
    <tbody>{linhas}</tbody></table></div>
  </section>
  <nav class="nav-pe">
    <a href="anexo-a.html" rel="prev"><div class="tecla-rot">◀ J · ANEXO A</div><div class="alvo">Concepts e Ranges</div></a>
    <div class="meio">ANEXO B</div>
    <a href="anexo-c.html" rel="next"><div class="tecla-rot">ANEXO C · K ▶</div><div class="alvo">O Deriva: as 20 versões</div></a>
  </nav>
</main>
</div>"""
    saidas["anexo-b.html"] = pagina(
        titulo="Anexo B - Referência rápida de C++17 · POO · UFPB",
        descricao="Tabela de consulta das construções de C++17 exigidas pela disciplina.",
        corpo=corpo, prev="anexo-a.html", next="anexo-c.html",
        migalha='<span class="sep">/</span><span class="atual">ANEXO B</span>')

    # ---- Anexo C: o Deriva, as 20 versões ---------------------------------
    corpo = f"""<div class="aula">
{arvore("anexo-c.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Anexo C · O Deriva: as 20 versões</h1>
    <p class="sub">v0.0 → v2.7 · CADA UMA COM O CAPÍTULO QUE A INTRODUZ</p>
  </div>
  <section class="slide">
    <p>O anexo do livro e a <a href="trilha.html">trilha do site</a> publicam o mesmo
    conteúdo, a partir da mesma fonte em <code>conteudo/mapa.py</code>, e a coincidência é
    deliberada: divergência entre livro e site foi o defeito do v1 que esta arquitetura
    impede. A tabela completa, com as variantes deliberadamente quebradas e as três caças
    ao bug, está na trilha.</p>
    <p><a href="trilha.html">Ir para a trilha do Deriva →</a></p>
  </section>
  <nav class="nav-pe">
    <a href="anexo-b.html" rel="prev"><div class="tecla-rot">◀ J · ANEXO B</div><div class="alvo">Referência rápida de C++17</div></a>
    <div class="meio">ANEXO C</div>
    <a href="glossario.html" rel="next"><div class="tecla-rot">GLOSSÁRIO · K ▶</div><div class="alvo">Glossário e bibliografia</div></a>
  </nav>
</main>
</div>"""
    saidas["anexo-c.html"] = pagina(
        titulo="Anexo C - O Deriva: as 20 versões · POO · UFPB",
        descricao="As 20 versões do Deriva e o capítulo que introduz cada uma.",
        corpo=corpo, prev="anexo-b.html", next="glossario.html",
        migalha='<span class="sep">/</span><span class="atual">ANEXO C</span>')
    return saidas


def pag_exercicios():
    secoes = []
    total = 0  # soma bruta: conta duas vezes o item que espera redistribuição
    for a in mapa.AULAS:
        d = CONTEUDO[a["slug"]]
        if not d["exercicios"]:
            continue
        total += len(d["exercicios"])
        itens = "".join(
            f'<div class="exercicio">'
            + moldura(f'AULA {a["n"]:02d} · EXERCÍCIO {esc(e["n"])}')
            + f'<div class="exercicio__corpo"><p>{e["html"]}</p></div>'
            + moldura(None, None, base=True) + "</div>"
            for e in d["exercicios"])
        secoes.append(f'<section class="slide" id="{a["slug"]}">'
                      f'<div class="slide__cab"><span class="slide__n">{a["n"]:02d}</span>'
                      f'<h2><a href="aula-{a["n"]:02d}.html">{esc(a["curto"])}</a> '
                      f'<span style="font-family:var(--maquina);font-size:var(--t-rot);'
                      f'color:var(--apagado)">· {len(d["exercicios"])} itens</span></h2></div>'
                      + itens + "</section>")
    corpo = f"""<div class="aula">
{arvore("exercicios.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Exercícios</h1>
    <p class="sub">{N_EX} ITENS DISTINTOS · {N_EX_DUP} À ESPERA DE REDISTRIBUIÇÃO · POR AULA</p>
  </div>
  <section class="slide">
    <p>Os itens do site v1 foram preservados e redistribuídos pelas fusões e divisões que o
    plano v2 determina. Onde a divisão de uma aula do v1 em duas do v2 deixa dúvida sobre a
    qual delas pertence um item, o item aparece nas duas, marcado, e entra uma única vez na
    contagem: duplicar à vista custa menos que perder exercício em silêncio.</p>
  </section>
{"".join(secoes)}
  <nav class="nav-pe">
    <a href="index.html" rel="prev"><div class="tecla-rot">◀ J · CAPA</div><div class="alvo">Índice das 26 aulas</div></a>
    <div class="meio">{N_EX} ITENS</div>
    <a href="glossario.html" rel="next"><div class="tecla-rot">GLOSSÁRIO · K ▶</div><div class="alvo">Glossário e bibliografia</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="Exercícios · POO · UFPB",
                  descricao=f"Os {N_EX} itens de exercício da disciplina, agregados por aula.",
                  corpo=corpo, prev="index.html", next="glossario.html",
                  migalha='<span class="sep">/</span><span class="atual">EXERCÍCIOS</span>')


GLOSSARIO = [
    ("raii", "RAII", "Aquisição de recurso é inicialização: o construtor adquire, o "
     "destrutor libera, e a garantia vem da ordem de destruição, inversa à de construção e "
     "válida inclusive quando é uma exceção que desenrola a pilha.", 8),
    ("polimorfismo", "polimorfismo dinâmico", "A chamada resolve pelo tipo dinâmico do "
     "objeto, e não pelo tipo do ponteiro através do qual se chega até ele. Custa um "
     "<code>vptr</code> por objeto e uma indireção por chamada; sem <code>virtual</code>, a "
     "decisão passa ao tipo estático, sem que o compilador emita warning.", 11),
    ("move", "semântica de movimento", "Transferência de recurso em lugar de cópia. O "
     "<code>std::move</code> não move nada por si: muda a categoria de valor do argumento, "
     "de forma que a sobrecarga escolhida seja a que rouba o recurso. A origem permanece em "
     "estado <strong>válido mas não-especificado</strong>, que não é necessariamente "
     "vazio - e que nesta libstdc++ é vazio nos quatro casos, o que faz "
     "<code>REQUIRE(origem.empty())</code> passar e o erro embarcar.", 14),
    ("vivos", "contador de instâncias vivas", "<code>static int vivos</code>, incrementado "
     "no construtor e decrementado no destrutor. É o detector de vazamento que a disciplina "
     "usa da Aula 07 ao fim do semestre, sem depender de sanitizer, e é a quarta condição "
     "de <code>make verifica</code>.", 7),
    ("replay", "replay determinístico", "Semente fixa e roteiro gravado produzem despejo "
     "idêntico byte a byte, o que dá o oráculo com que se afirma que uma refatoração não "
     "alterou o comportamento observável.", 16),
    ("regra-zero", "regra do zero", "Se a classe não gerencia recurso, nenhuma das operações "
     "especiais deve ser declarada: as que o compilador gera são corretas e não envelhecem "
     "quando um membro é acrescentado.", 9),
    ("regra-cinco", "regra dos cinco", "Ao declarar uma das cinco operações especiais, "
     "decida sobre as outras quatro. Declarar o destrutor e esquecer a cópia é o caminho "
     "pelo qual se produz cópia rasa silenciosa, que é a caça ao bug 1 do semestre.", 14),
    ("sso", "otimização de string curta", "A <code>std::string</code> guarda cadeias curtas "
     "dentro do próprio objeto, sem alocar no heap - até 15 caracteres, neste alvo. A "
     "consequência prática, medida em "
     "<code>testes/test_move_string.cpp</code>: mover uma string curta <strong>copia os "
     "bytes</strong>, porque não há ponteiro a roubar, enquanto mover uma longa transfere o "
     "ponteiro de heap sem copiar conteúdo algum. Em nenhum dos dois casos a origem fica "
     "intacta nesta libstdc++, e é justamente por isso que o teste errado passa.", 14),
    ("slicing", "fatiamento de objeto", "Guardar um objeto de classe derivada por valor em "
     "contêiner da classe base descarta a parte específica da derivada. O sintoma é "
     "comportamento da base onde se esperava o da derivada, sem warning e sem erro de "
     "execução.", 10),
    ("crtp", "CRTP", "A classe derivada se passa como argumento de template para a própria "
     "base, o que resolve o polimorfismo em tempo de compilação, sem "
     "<code>vptr</code>. Aqui o alvo concreto é generalizar o contador <code>vivos</code> "
     "em <code>contador_de_instancias&lt;T&gt;</code>.", 19),
]

BIBLIO = [
    ("Stroustrup, B.", "The C++ Programming Language", "4ª ed., Addison-Wesley, 2013",
     "referência de linguagem, anterior ao C++17: consultar com o Josuttis ao lado"),
    ("Stroustrup, B.", "Programming: Principles and Practice Using C++",
     "3ª ed., Addison-Wesley, 2024", "introdução à programação com C++; a edição correta "
     "é a 3ª, e a bibliografia do v1 citava outra"),
    ("Josuttis, N.", "C++17 - The Complete Guide", "Leanpub, 2019",
     "cobre o padrão-alvo construção por construção, e é a referência do Anexo B"),
    ("Meyers, S.", "Effective Modern C++", "O'Reilly, 2014",
     "movimento, encaminhamento perfeito e posse, para as Aulas 12 a 14"),
    ("Sutter, H.; Alexandrescu, A.", "C++ Coding Standards", "Addison-Wesley, 2004",
     "as regras de projeto que envelheceram bem, úteis na rubrica da Aula 04"),
    ("Gamma, E. et al.", "Design Patterns", "Addison-Wesley, 1994",
     "os padrões na formulação original; no Cap. 25 aparecem em C++ moderno, com "
     "Strategy por lambda"),
    ("Martin, R. C.", "Clean Architecture", "Prentice Hall, 2017",
     "SOLID, a ser lido com a ressalva de que não traz exemplo em C++"),
    ("Nash, P.; Hořeňovský, M.", "Catch2 - documentação", "github.com/catchorg/Catch2",
     "o framework de teste do portão; a bibliografia do v1 trazia autoria trocada"),
    ("Sonzogni, A.", "FTXUI - documentação", "github.com/ArthurSonzogni/FTXUI",
     "fixar GIT_TAG v5.0.0, porque as versões v6 e v7 podem elevar o padrão de "
     "linguagem exigido"),
]


def pag_glossario():
    verbetes = "".join(
        f'<div class="exercicio" id="{k}">'
        + moldura(esc(t.upper()))
        + f'<div class="exercicio__corpo"><p>{txt}</p>'
          f'<p style="font-family:var(--maquina);font-size:var(--t-rot);color:var(--apagado)">'
          f'entra na <a href="aula-{cap:02d}.html">Aula {cap:02d}</a></p></div>'
        + moldura(None, None, base=True) + "</div>"
        for k, t, txt, cap in GLOSSARIO)
    bib = "".join(f'<tr><td>{esc(a)}</td><td><em>{esc(t)}</em></td><td>{esc(e)}</td>'
                  f'<td>{esc(n)}</td></tr>' for a, t, e, n in BIBLIO)
    corpo = f"""<div class="aula">
{arvore("glossario.html")}
<main class="corpo" id="conteudo">
  <div class="cabeca-aula">
    <h1>Glossário e bibliografia</h1>
    <p class="sub">{len(GLOSSARIO)} VERBETES · {len(BIBLIO)} REFERÊNCIAS AUDITADAS</p>
  </div>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">01</span><h2>Glossário</h2></div>
    <p>Cada verbete registra a aula em que o conceito entra, e a consulta devolve também o
    lugar do material onde o mecanismo é desenvolvido.</p>
    {verbetes}
  </section>
  <section class="slide">
    <div class="slide__cab"><span class="slide__n">02</span><h2>Bibliografia</h2></div>
    <p>Duas correções em relação ao v1 estão aplicadas: a autoria do Catch2, que é de Nash e
    Hořeňovský, e a edição de <em>Programming: Principles and Practice</em>, que é a 3ª, de
    2024. Entrou também o Josuttis, por cobrir o padrão-alvo capítulo por capítulo.</p>
    <div style="overflow-x:auto"><table class="tabela"><thead><tr><th>autoria</th>
    <th>título</th><th>edição</th><th>para que serve aqui</th></tr></thead>
    <tbody>{bib}</tbody></table></div>
  </section>
  <nav class="nav-pe">
    <a href="anexo-c.html" rel="prev"><div class="tecla-rot">◀ J · ANEXO C</div><div class="alvo">O Deriva: as 20 versões</div></a>
    <div class="meio">REFERÊNCIA</div>
    <a href="index.html" rel="next"><div class="tecla-rot">CAPA · K ▶</div><div class="alvo">Índice das 26 aulas</div></a>
  </nav>
</main>
</div>"""
    return pagina(titulo="Glossário e bibliografia · POO · UFPB",
                  descricao="Glossário dos conceitos da disciplina e bibliografia auditada.",
                  corpo=corpo, prev="anexo-c.html", next="index.html",
                  migalha='<span class="sep">/</span><span class="atual">GLOSSÁRIO</span>')


# ---------------------------------------------------------------------------
# portão: nenhum link interno morto
# ---------------------------------------------------------------------------
def conferir_links(paginas: dict) -> list:
    erros = []
    existentes = set(paginas) | {p.name for p in SAIDA.glob("*")}
    for nome, html_txt in paginas.items():
        for m in re.finditer(r'href="([^"#:]+)(#[^"]*)?"', html_txt):
            alvo = m.group(1)
            if alvo.startswith(("http", "mailto", "data:", "//")):
                continue
            if alvo not in existentes and not (SAIDA / alvo).exists():
                erros.append(f"{nome} → {alvo} não existe")
        for m in re.finditer(r'href="#([^"]+)"', html_txt):
            if f'id="{m.group(1)}"' not in html_txt:
                erros.append(f"{nome} → âncora #{m.group(1)} não existe na página")
    return sorted(set(erros))


def main():
    erros = mapa.verificar()
    if erros:
        for e in erros:
            print("mapa ERRO:", e)
        return 1

    paginas = {"index.html": pag_index(), "galeria.html": pag_galeria(),
               "trilha.html": pag_trilha(), "laboratorios.html": pag_laboratorios(),
               "rubrica.html": pag_rubrica(), "verifica.html": pag_verifica(),
               "plano-de-ensino.html": pag_plano(), "exercicios.html": pag_exercicios(),
               "glossario.html": pag_glossario()}
    paginas.update(pag_anexos())
    for a in mapa.AULAS:
        paginas[f"aula-{a['n']:02d}.html"] = pag_aula(a)

    # `plano-de-ensino.docx` deixou de ser exceção: ele é gerado por
    # `build/gerar_plano_docx.py` a partir do markdown do plano, então link
    # morto para ele volta a ser erro como qualquer outro. A tolerância
    # existia porque o arquivo era feito à mão, e foi ela que permitiu ele
    # ficar 17 horas atrás do plano que representa.
    faltando = conferir_links(paginas)
    duros = list(faltando)
    if duros:
        for e in duros:
            print("LINK ERRO:", e)
        print("nada foi escrito - corrija os links")
        return 2

    if CONFERIR:
        muda = [n for n, t in paginas.items()
                if not (SAIDA / n).exists() or (SAIDA / n).read_text(encoding="utf-8") != t]
        print(f"conferido: {len(paginas)} páginas, {len(muda)} divergem")
        for n in muda[:20]:
            print("  ~", n)
        # Divergência REPROVA. Antes isto devolvia 0 e `make verifica` dizia
        # "portões OK" logo abaixo do relatório de desvio.
        if muda:
            print(f"  reprovado: {len(muda)} página(s) fora de dia - "
                  "rode `python3 build/build_site.py`")
            return 1
        return 0

    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, txt in paginas.items():
        (SAIDA / nome).write_text(txt, encoding="utf-8")

    bytes_tot = sum(len(t.encode()) for t in paginas.values())
    print(f"site: {len(paginas)} páginas · {bytes_tot // 1024} KB · "
          f"26 aulas + 3 anexos + 9 páginas de material"
          + (" · sem notas de migração" if SEM_NOTAS else ""))
    if faltando:
        print("aviso:", faltando[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
