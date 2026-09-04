# -*- coding: utf-8 -*-
"""build/comum.py - o que o gerador de site e o de livro compartilham.

Realce de sintaxe próprio (não Prism de CDN), deep link para o Compiler
Explorer e as primitivas de box-drawing. O site v1 puxava Prism e Mermaid de
CDN e as fontes do Google Fonts por @import; nada aqui depende de rede.
"""
from __future__ import annotations

import base64
import html
import json
import re

# ---------------------------------------------------------------------------
# box-drawing - caracteres reais, título embutido na moldura de cima
# ---------------------------------------------------------------------------
def moldura(titulo=None, nota=None, sistema=False, base=False, arredondada=False):
    ce = ("╰" if arredondada else "└") if base else ("╭" if arredondada else "┌")
    cd = ("╯" if arredondada else "┘") if base else ("╮" if arredondada else "┐")
    t = ""
    if titulo:
        t = ('<span class="moldura__canto">─┤</span>'
             f'<span class="moldura__titulo">{titulo}</span>'
             '<span class="moldura__canto">├</span>')
    n = f'<span class="moldura__nota">┤ {nota} ├</span>' if nota else ""
    cls = "moldura moldura--sistema" if sistema else "moldura"
    return (f'<div class="{cls}" aria-hidden="true">'
            f'<span class="moldura__canto">{ce}─</span>{t}'
            f'<span class="moldura__regua" data-fill>────────</span>{n}'
            f'<span class="moldura__canto">─{cd}</span></div>')


def painel(titulo, corpo, nota=None, sistema=False, arredondada=True, classe=""):
    c = ("painel painel--sistema" if sistema else "painel") + (f" {classe}" if classe else "")
    return (moldura(titulo, nota, sistema, False, arredondada) +
            f'<div class="{c}">{corpo}</div>' +
            moldura(None, None, sistema, True, arredondada))


# ---------------------------------------------------------------------------
# realce de sintaxe - 60 blocos, vocabulário pequeno, zero dependência
# Mapeia para as classes .tk-* já definidas em css/pagina.css.
# ---------------------------------------------------------------------------
PALAVRAS = {
    "alignas", "alignof", "auto", "bool", "break", "case", "catch", "char",
    "class", "const", "const_cast", "constexpr", "continue", "decltype",
    "default", "delete", "do", "double", "dynamic_cast", "else", "enum",
    "explicit", "export", "extern", "false", "final", "float", "for", "friend",
    "goto", "if", "inline", "int", "long", "mutable", "namespace", "new",
    "noexcept", "nullptr", "operator", "override", "private", "protected",
    "public", "register", "reinterpret_cast", "return", "short", "signed",
    "sizeof", "static", "static_assert", "static_cast", "struct", "switch",
    "template", "this", "thread_local", "throw", "true", "try", "typedef",
    "typeid", "typename", "union", "unsigned", "using", "virtual", "void",
    "volatile", "while",
}
C20_PALAVRAS = {"concept", "requires", "consteval", "constinit", "co_await",
                "co_yield", "co_return"}
TIPOS = re.compile(r"\b(std::[a-z_0-9:]+|[a-z_][a-z_0-9]*_t)\b")

_TOKEN = re.compile(r"""
    (?P<com>//[^\n]*|/\*.*?\*/)
  | (?P<pre>^[ \t]*\#[^\n]*)
  | (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])')
  | (?P<num>\b0[xX][0-9a-fA-F']+\b|\b\d[\d'.]*(?:[eE][+-]?\d+)?[fFuUlL]*\b)
  | (?P<pal>[A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)
""", re.X | re.S | re.M)


def realcar(codigo: str, lang: str = "cpp") -> str:
    """Marca comentário, pré-processador, string, número, palavra e tipo.

    Dois tons mais os semânticos, como pede o brief: sem arco-íris. C++20 sai
    em `--outro`, a mesma cor do selo, porque aqui é fora do padrão-alvo.
    """
    if lang not in ("cpp", "c", "bash", "sh", "cmake", "make"):
        return html.escape(codigo)
    if lang in ("bash", "sh", "make", "cmake"):
        out, pos = [], 0
        for m in re.finditer(r"(?P<com>#[^\n]*)|(?P<str>\"[^\"]*\"|'[^']*')", codigo):
            out.append(html.escape(codigo[pos:m.start()]))
            cls = "tk-com" if m.lastgroup == "com" else "tk-str"
            out.append(f'<span class="{cls}">{html.escape(m.group())}</span>')
            pos = m.end()
        out.append(html.escape(codigo[pos:]))
        return "".join(out)

    out, pos = [], 0
    for m in _TOKEN.finditer(codigo):
        out.append(html.escape(codigo[pos:m.start()]))
        txt, tipo = m.group(), m.lastgroup
        if tipo == "pal":
            if txt in C20_PALAVRAS:
                cls = "tk-c20"
            elif txt in PALAVRAS:
                cls = "tk-kw"
            elif TIPOS.fullmatch(txt) or txt.startswith("std::"):
                cls = "tk-tipo"
            else:
                cls = None
            out.append(html.escape(txt) if not cls
                       else f'<span class="{cls}">{html.escape(txt)}</span>')
        else:
            cls = {"com": "tk-com", "pre": "tk-pre", "str": "tk-str", "num": "tk-num"}[tipo]
            out.append(f'<span class="{cls}">{html.escape(txt)}</span>')
        pos = m.end()
    out.append(html.escape(codigo[pos:]))
    return "".join(out)


# ---------------------------------------------------------------------------
# Compiler Explorer - o payload que faltava no v1
# ---------------------------------------------------------------------------
def link_ce(codigo: str, padrao="c++17", compilador="g142") -> str:
    """URL de clientstate do godbolt, já com -std=c++17 -Wall -Wextra.

    O rodapé do bloco de código no v1 tinha o <a> e não tinha o payload.
    Aqui o estado da sessão vai embutido, gerado no build.
    """
    estado = {"sessions": [{
        "id": 1, "language": "c++", "source": codigo,
        "compilers": [{"id": compilador,
                       "options": f"-std={padrao} -Wall -Wextra -Wpedantic"}],
    }]}
    crua = json.dumps(estado, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "https://godbolt.org/clientstate/" + base64.urlsafe_b64encode(crua).decode("ascii")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# a seção de código do livro - gerada, e reinjetada a cada montagem
#
# Ela vive dentro de `livro/capitulos/*.md`, que passou a ser escrito à mão.
# Sem reinjeção, mudar um trecho em `conteudo/trechos.py` deixaria a versão
# antiga congelada no capítulo - foi o que aconteceu com a nota do contador da
# Aula 09, que sobreviveu à correção por uma passada.
# ---------------------------------------------------------------------------
MARCA_CODIGO = "## O código, extraído do Deriva"


def secao_codigo_md(aula_n, trechos_mod, codigo_mod):
    """O markdown da seção de código de uma aula, ou "" se ela não tem trechos."""
    # `inline` fora: o diagrama vive no slide que o explica, e o livro o
    # recebe pelo mesmo caminho.
    ids = [t["id"] for t in trechos_mod.por_aula(aula_n)
           if t["id"] in codigo_mod and not t.get("inline")]
    if not ids:
        return ""
    # A moldura varia com o alvo, porque a afirmação não é a mesma. O Anexo A
    # (aula 0) traz trechos do alvo OPCIONAL de C++20, que fica fora do portão
    # de propósito - dizer que eles passam `make verifica` seria falso, e a
    # frase estava sendo escrita em toda seção sem essa distinção.
    if aula_n == 0:
        moldura = ("Todo trecho abaixo vem de `exemplos/deriva/c20/`, que compila em "
                   "alvo **separado** com `-std=c++20 -Wall -Wextra -Wpedantic` sem um "
                   "aviso - e que fica **fora** do portão `make verifica`, porque o "
                   "padrão-alvo da disciplina é C++17. Nenhum foi digitado neste "
                   "texto, e nada do material obrigatório depende deles.")
    else:
        moldura = ("Todo trecho abaixo vem de `exemplos/deriva/`, que compila com "
                   "`-std=c++17 -Wall -Wextra -Wpedantic` sem um aviso e passa "
                   "`make verifica`. Nenhum foi digitado neste texto.")
    out = ["", MARCA_CODIGO, "", moldura, ""]
    for i in ids:
        d = codigo_mod[i]
        aviso = " - **quebrado de propósito**" if d["quebrado_de_proposito"] else ""
        out += [f"**{d['legenda']}**{aviso}", "",
                f"`{d['arquivo']}:{d['linha']}`", "",
                "``` " + d["lang"], d["codigo"], "```", "",
                d["nota"], ""]
    return "\n".join(out)


def reinjetar_codigo(texto, aula_n, trechos_mod, codigo_mod):
    """Troca a seção de código do capítulo pela versão recém-gerada.

    Devolve (texto, mudou). A seção vai do cabeçalho `MARCA_CODIGO` até o
    próximo `## ` de mesmo nível, ou até o fim do arquivo.
    """
    nova = secao_codigo_md(aula_n, trechos_mod, codigo_mod).strip("\n")
    i = texto.find(MARCA_CODIGO)

    # Os dois caminhos - acrescentar e substituir - têm de produzir o MESMO
    # byte, ou a montagem deixa de ser idempotente: a primeira passada
    # acrescentava com um espaçamento e a segunda substituía com outro, e o
    # build relatava mudança para sempre.
    if i == -1:
        if not nova:
            return texto, False
        antes, depois = texto.rstrip("\n"), ""
    else:
        fim = texto.find("\n## ", i + len(MARCA_CODIGO))
        antes = texto[:i].rstrip("\n")
        depois = "" if fim == -1 else texto[fim + 1:].strip("\n")

    partes = [antes]
    if nova:
        partes.append(nova)
    if depois:
        partes.append(depois)
    resultado = "\n\n".join(partes) + "\n"
    return resultado, resultado != texto

# ---------------------------------------------------------------------------
# o mesmo realce, saindo em LaTeX
#
# Um tokenizador, dois emissores. O site recebe `<span class="tk-kw">` e o
# livro recebe `\tkkw{}`, e a classificação é literalmente a mesma função -
# se ela errar, erra igual nos dois, e não em um só.
#
# Código não reflui: cada linha sai como `\codelinha{...}` e cada espaço como
# `\CS`, de avanço fixo. Sem `obeyspaces`, sem `verbatim`, e sem quebra
# automática no meio de uma expressão.
# ---------------------------------------------------------------------------
_TEX_ESCAPA = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$",
    "&": r"\&", "#": r"\#", "^": r"\textasciicircum{}", "_": r"\_",
    "~": r"\textasciitilde{}", "%": r"\%",
}


def esc_tex(s: str) -> str:
    """Escapa o que o LaTeX lê como comando, e mais nada."""
    return "".join(_TEX_ESCAPA.get(c, c) for c in s)


def _tex_pedaco(txt: str, cls: str | None) -> str:
    """Um pedaço já classificado, com os espaços virando avanço fixo."""
    partes = []
    for i, seg in enumerate(txt.split(" ")):
        if i:
            partes.append(r"\CS{}")
        if seg:
            partes.append(esc_tex(seg))
    corpo = "".join(partes)
    if not cls:
        return corpo
    return "\\" + cls + "{" + corpo + "}"


def realcar_tex(codigo: str, lang: str = "cpp") -> str:
    """As linhas de `\\codelinha{}` de um bloco, na ordem."""
    marcado = []
    if lang in ("bash", "sh", "make", "cmake"):
        pos = 0
        for m in re.finditer(r"(?P<com>#[^\n]*)|(?P<str>\"[^\"]*\"|'[^']*')", codigo):
            marcado.append((codigo[pos:m.start()], None))
            marcado.append((m.group(), "tkcom" if m.lastgroup == "com" else "tkstr"))
            pos = m.end()
        marcado.append((codigo[pos:], None))
    elif lang in ("cpp", "c"):
        pos = 0
        for m in _TOKEN.finditer(codigo):
            marcado.append((codigo[pos:m.start()], None))
            txt, tipo = m.group(), m.lastgroup
            if tipo == "pal":
                if txt in C20_PALAVRAS:
                    cls = "tkctwenty"
                elif txt in PALAVRAS:
                    cls = "tkkw"
                elif TIPOS.fullmatch(txt) or txt.startswith("std::"):
                    cls = "tktipo"
                else:
                    cls = None
            else:
                cls = {"com": "tkcom", "pre": "tkpre",
                       "str": "tkstr", "num": "tknum"}[tipo]
            marcado.append((txt, cls))
            pos = m.end()
        marcado.append((codigo[pos:], None))
    else:
        marcado.append((codigo, None))

    # Remontar por linha: um pedaço pode atravessar a quebra (comentário de
    # bloco, string com `\n`), e a classe tem de sobreviver à divisão.
    linhas = [[]]
    for txt, cls in marcado:
        pedacos = txt.split("\n")
        for k, pedaco in enumerate(pedacos):
            if k:
                linhas.append([])
            if pedaco:
                linhas[-1].append((pedaco, cls))

    return "\n".join(
        "\\codelinha{" + "".join(_tex_pedaco(t, c) for t, c in ln) + "}"
        for ln in linhas
    )


def largura_maxima(codigo: str) -> int:
    """A linha mais larga, em caracteres. Decide a escala do bloco impresso."""
    return max((len(l) for l in codigo.split("\n")), default=0)
