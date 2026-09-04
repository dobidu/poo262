#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build/render_livro.py - livro/capitulos + livro/anexos -> PDF de impressão.

O artefato primário do livro é o PDF de impressão, e é ele que define medida,
quebra de página e cor; a versão de tela herda o mesmo mundo. Aqui o markdown
vira LaTeX pelo pandoc, com `livro/estilo/livro.tex` de gabarito e
`livro/estilo/livro.lua` de filtro, e o XeLaTeX compõe.

O que este script faz e o pandoc não poderia:

  * abre cada capítulo com a unidade, a aula e a versão do Deriva, que vêm de
    `conteudo/mapa.py` e não do texto;
  * monta o bloco de código com o realce próprio (`build/comum.py`), a
    procedência embutida na moldura de cima, e a escala calculada por bloco -
    código não reflui, então quem decide o corpo é a linha mais larga;
  * carimba na margem externa cada número que a prosa afirma e o binário
    mediu, com o comando e o arquivo que o produziram.

Uso:  python3 build/render_livro.py [--tex] [--tela]
      --tex   para no .tex, sem chamar o XeLaTeX
      --tela  gera também livro/livro.html, a versão de tela
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
ESTILO = LIVRO / "estilo"
FONTES = RAIZ / "build" / "fontes-tex"
SAIDA = RAIZ / "build" / "tex"

sys.path.insert(0, str(RAIZ / "build"))
sys.path.insert(0, str(RAIZ / "conteudo"))
import mapa                                          # noqa: E402
import medidas                                       # noqa: E402
from comum import (MARCA_CODIGO, esc_tex, largura_maxima,   # noqa: E402
                   moldura, realcar, realcar_tex)

try:
    from codigo_deriva import CODIGO
except ModuleNotFoundError:
    CODIGO = {}

# 98 colunas é o que cabe em 174 mm de Plex Mono a 8,8 pt (avanço 0,6 em,
# escala 0,92), com folga para o recuo. Bloco mais largo encolhe, e nenhum
# reflui: das 147 amostras, duas passam de 98 e só elas mudam de corpo.
COLUNAS = 98
CORPO_CODIGO = 8.8
CORPO_MINIMO = 6.9


# ---------------------------------------------------------------------------
# os carimbos de aferição
#
# Um carimbo dispara quando o parágrafo diz a grandeza E o número. Exigir os
# dois é o que evita carimbar "16" de qualquer outra coisa como se fosse o
# sizeof de `entidade`. Cada medida carimba uma vez por capítulo: a margem é
# campo de conferência, não de repetição.
# ---------------------------------------------------------------------------
def tabela_de_carimbos() -> list[tuple]:
    M, P = medidas.MEDIDAS, medidas.PROCEDENCIA
    t: list[tuple] = []

    def por(chave, palavra, valor, grandeza, exibe=None):
        """`exibe` fixa o valor do carimbo quando o texto casado não é uma
        quantidade: `sem um aviso` casa a frase, mas o que o carimbo tem de
        mostrar é `0 avisos`."""
        cmd, arq = P[chave]
        t.append((re.compile(palavra, re.I), re.compile(valor), grandeza,
                  cmd, arq, exibe))

    # do maior nome para o menor: `celula_ingenua` tem de casar antes de `celula`
    for nome, v in sorted(M["sizeof"].items(), key=lambda kv: -len(kv[0])):
        por("sizeof", rf"\b{re.escape(nome)}\b",
            rf"\b{v}\s*(?:bytes|B)\b", rf"sizeof({nome})")

    por("vptr", r"\bvptr\b", rf"\b{M['vptr']}\s*(?:bytes|B)\b", "custo do vptr")
    por("testes", r"\btestes?\b", rf"\b{M['testes']}\s+testes\b", "testes verdes")
    por("ciclo_bytes", r"\bciclo\b", rf"\b{M['ciclo_bytes']}\s*(?:bytes|B)\b",
        "presos pelo ciclo")
    por("no", r"sizeof\(no\)|\bnó\b", rf"\b{M['no']}\s*(?:bytes|B)\b", "sizeof(no)")
    for nome, v in M["diamante"].items():
        por("diamante", rf"patrulha_{nome}\b", rf"\b{v}\s*(?:bytes|B)\b",
            f"sizeof(patrulha_{nome})")
    por("construcoes_de_texto", r"constru[cç]", r"\bduas constru|\b2 constru",
        "construções em de_texto")
    por("testes_deriva", r"\bDeriva\b", rf"\b{M['testes_deriva']}\s+testes\b",
        "testes do Deriva")
    por("testes_labs", r"laborat[óo]rio", rf"\b{M['testes_labs']}\s+(?:testes|laborat)",
        "laboratórios no ctest")
    por("variantes_escritas", r"variante", rf"\b{len(M['variantes_escritas'])}\s+variantes\b",
        "variantes quebradas")
    por("avisos", r"\bWall\b|\bWextra\b|\baviso", r"\bsem um aviso\b|\bzero aviso\b",
        "avisos do compilador", exibe=f"{M['avisos']} avisos")
    return t


CARIMBOS = tabela_de_carimbos()


def carimbar(paragrafo: str, gastos: set, alvo: str = "tex") -> tuple[str, str]:
    """Devolve (parágrafo com o carimbo ancorado, grandeza), ou (paragrafo, "").

    O carimbo é ancorado NA FRASE que afirma o número, e não posto antes do
    parágrafo. `marginnote` ancora na linha em que é chamado, então basta
    injetá-lo imediatamente depois do valor que casou - e a posição do valor
    é justamente o que a busca já sabe.

    Antes o carimbo flutuava no topo do campo, sem vínculo visível com a
    afirmação, e a tese do livro chegava por reincidência em vez de por
    vínculo: o leitor via "0 avisos" na margem e tinha de descobrir sozinho a
    qual das frases da folha aquilo se referia.
    """
    for palavra, valor, grandeza, cmd, arq, exibe in CARIMBOS:
        if grandeza in gastos:
            continue
        if not palavra.search(paragrafo):
            continue
        m = valor.search(paragrafo)
        if not m:
            continue
        # Não ancorar dentro de trecho de código embutido: a crase abre um
        # `\texttt`, e um `marginnote` lá dentro sai deslocado.
        if paragrafo.count("`", 0, m.start()) % 2:
            continue
        gastos.add(grandeza)
        v = exibe or m.group().strip()
        if alvo == "html":
            from html import escape
            marca = ('<aside class="carimbo">'
                     f'<span class="carimbo__regua" aria-hidden="true">'
                     f'{"─" * 60}</span>'
                     f'<span class="carimbo__valor">{escape(v)}</span>'
                     f'<span class="carimbo__grandeza">{escape(grandeza)}</span>'
                     f'<span class="carimbo__como">aferido por</span>'
                     f'<code>{escape(cmd)}</code><br><code>{escape(arq)}</code>'
                     "</aside>")
            cru = "`" + marca + "`{=html}"
        else:
            cru = ("`\\carimbo{" + esc_tex(grandeza) + "}{" + esc_tex(v) + "}"
                   "{" + esc_tex(cmd) + "}{" + esc_tex(arq) + "}`{=latex}")
        return paragrafo[:m.end()] + cru + paragrafo[m.end():], grandeza
    return paragrafo, ""


# ---------------------------------------------------------------------------
# o bloco de código: prancha com procedência na moldura
# ---------------------------------------------------------------------------
# Um varredor de uma passada, e não duas regex.
#
# A primeira versão eram duas: uma para o bloco com legenda e procedência, e
# outra para a fence solta. A segunda passava DEPOIS da primeira e casava com
# a cerca de fechamento do LaTeX cru que a primeira tinha acabado de emitir,
# engolindo a prosa entre um bloco e o seguinte para dentro de um `codigo`. O
# varredor lê o markdown original uma vez e não tem esse buraco.
RX_ABRE = re.compile(r"^``` ?(\w*)\s*$")
RX_FECHA = re.compile(r"^```\s*$")


def escala(codigo: str) -> float:
    """O corpo do bloco. Código não reflui, então a linha mais larga decide."""
    larg = max(largura_maxima(codigo), 1)
    if larg <= COLUNAS:
        return CORPO_CODIGO
    return max(CORPO_MINIMO, round(CORPO_CODIGO * COLUNAS / larg, 2))


def emitir_codigo_html(codigo: str, lang: str, rot: str, nota: str) -> list[str]:
    """A mesma prancha em HTML, com a moldura de CARACTERE.

    Ela usa `comum.moldura()`, que é a mesma função que desenha as molduras do
    site: `┌─`, título embutido, régua de `─` de verdade e `─┐`. Uma revisão
    de fim mediu 30 declarações de `border` nesta folha contra 47 caracteres
    de box-drawing no HTML inteiro, e o PRODUCT.md nomeia justamente "moldura
    desenhada com `border` no lugar de caractere" como o que faz um resultado
    polido parecer errado. O impresso tem 33 mil `─`; a tela tinha borda.
    """
    from html import escape
    m = [moldura(escape(rot) if rot else None,
                 escape(nota) if nota else None, arredondada=False)]
    m.append('<div class="prancha"><pre><code class="lang-'
             + escape(lang or "cpp") + '">')
    m.append(realcar(codigo, lang or "cpp"))
    m.append("</code></pre></div>")
    m.append(moldura(None, None, base=True))
    return ["```{=html}", "".join(m), "```"]


def emitir_codigo(codigo: str, lang: str, legenda: str,
                  proc: str, quebrado: bool, alvo: str = "tex") -> list[str]:
    """A prancha: moldura com procedência à esquerda e o que o trecho mostra
    à direita.

    A procedência morava num carimbo de margem, e o bloco ocupa texto MAIS
    campo de aferição: o carimbo caía em cima da moldura. Ela volta para a
    régua, onde também deixa de ser redundante - a legenda gerada já começa
    pelo arquivo, e o que faltava era só a linha.
    """
    # `exemplos/deriva/` é prefixo de toda procedência, e a moldura da seção
    # já o diz. Repeti-lo em 147 réguas gastava 16 caracteres cada.
    curto = proc.replace("exemplos/deriva/", "")
    partes = legenda.split(" · ", 1)
    if len(partes) == 2 and partes[0] and partes[0] in curto:
        rot, nota = curto, partes[1]
    else:
        rot, nota = legenda or curto, ("" if legenda else "")
        if legenda and curto:
            nota = curto
    if quebrado:
        nota = ("quebrado de propósito · " + nota) if nota else "quebrado de propósito"
        rot = "▲ " + rot
    # A régua tem 174 mm, que a 8 pt de Plex Mono são 112 caracteres. O rótulo
    # mais longo do material tem 130 com o marcador de variante quebrada, e
    # transbordava por 52 pt. Como a contagem é conhecida aqui, o corpo que
    # cabe também é: a régua encolhe em vez de estourar, e nenhum bloco perde
    # a procedência nem a legenda.
    # +8 de moldura e +6 do marcador de variante quebrada, que é um glifo
    # do suplemento e mede mais que um caractere de Mono.
    largura_regua = len(rot) + len(nota) + 8 + (6 if quebrado else 0)
    corpo_regua = 8.0 if largura_regua <= 112 else max(6.2, round(8.0 * 112 / largura_regua, 2))
    if alvo == "html":
        return emitir_codigo_html(codigo, lang, rot, nota)
    rot_tex = esc_tex(rot).replace("▲", "{\\geo ▲}")
    # A prancha reserva a própria altura antes de começar.
    #
    # Sem isso ela parte na quebra de página, e a continuação chega ao leitor
    # com a régua de baixo e sem a de cima: uma linha solta, sem procedência e
    # sem legenda. O `\needspace` do ambiente era de 5 linhas, fixo.
    #
    # O teto de 46 é deliberado: a folha tem 58 linhas de código, e reservar
    # mais do que caberia empurraria uma folha em branco. Das 147 amostras,
    # 143 ficam abaixo de 46 e deixam de partir; as 4 restantes (47, 49, 62 e
    # 109 linhas) não caberiam em folha nenhuma, e para elas a quebra é o
    # comportamento correto.
    linhas = codigo.count("\n") + 1
    reserva = min(linhas + 3, 46)
    # a numeração começa na linha que o arquivo declara, e não em 1
    m_linha = re.search(r":(\d+)$", proc)
    primeira = int(m_linha.group(1)) if m_linha else 1
    return ["```{=latex}",
            f"\\begin{{codigo}}[{corpo_regua}]{{{escala(codigo)}}}{{{rot_tex}}}"
            f"{{{esc_tex(nota)}}}{{{reserva}}}{{{primeira}}}",
            realcar_tex(codigo, lang or "cpp"),
            "\\end{codigo}",
            "```"]


RX_LEGENDA = re.compile(r"^\*\*(?P<legenda>.+?)\*\*(?P<aviso>.*)$")
RX_PROC = re.compile(r"^`(?P<proc>[^`]+:\d+)`$")


def converter_codigo(txt: str, alvo: str = "tex") -> str:
    """Toda fence vira prancha de código, com a procedência na moldura.

    A legenda e a procedência do bloco vêm das duas linhas que a seção gerada
    põe antes da cerca; quando não estão lá (prosa, Anexo B), a moldura sai
    vazia em vez de inventada.
    """
    L = txt.split("\n")
    fora, i = [], 0
    while i < len(L):
        m = RX_ABRE.match(L[i])
        if not m:
            fora.append(L[i])
            i += 1
            continue

        lang, j = m.group(1), i + 1
        while j < len(L) and not RX_FECHA.match(L[j]):
            j += 1
        codigo = "\n".join(L[i + 1:j])

        # olhar para trás: `**legenda**`, linha vazia, `` `arquivo:linha` ``,
        # linha vazia, cerca. Se o padrão inteiro não estiver lá, não há
        # procedência a exibir.
        legenda = proc = ""
        quebrado = False
        if len(fora) >= 4:
            mp = RX_PROC.match(fora[-2].strip())
            ml = RX_LEGENDA.match(fora[-4].strip())
            if mp and ml and not fora[-1].strip() and not fora[-3].strip():
                proc = mp.group("proc")
                legenda = ml.group("legenda").strip()
                quebrado = "quebrado de propósito" in ml.group("aviso")
                del fora[-4:]

        fora += [""] + emitir_codigo(codigo, lang, legenda, proc,
                                     quebrado, alvo) + [""]
        i = j + 1
    return "\n".join(fora)


# ---------------------------------------------------------------------------
# a abertura de capítulo, com os dados que só o mapa tem
# ---------------------------------------------------------------------------
RX_H1 = re.compile(r"^# (?P<titulo>[^\n]+)\n", re.M)


def abertura(n: int | None, rel: str):
    """(unidade, aula, versão) para a moldura do capítulo, tirados do mapa."""
    if n is None:
        return None
    a = next((x for x in mapa.AULAS if x["n"] == n), None)
    if a is None:
        return None
    u = mapa.unidade(a["unidade"])
    nome_u = f"Unidade {a['unidade']}"
    if isinstance(u, dict) and u.get("rot"):
        nome_u += " \\char\"00B7\\ " + esc_tex(u["rot"])
    # Nem toda aula entrega versão nova do Deriva, e inventar uma seria pior
    # que dizer que não há: a moldura diz o que é verdade.
    v = a.get("deriva")
    # O lugar da versão fica VAZIO quando a aula não entrega uma.
    #
    # Ele imprimia "sem versão nova", e carimbar a falta usa o device do
    # mundo para dizer que não há o que dizer. O contrato reservou aquele
    # lugar para a versão sob inspeção, e ausência de versão é ausência de
    # carimbo.
    versao = f"Deriva {v}" if v else ""
    # A cabeça corrida tem UM significado, e não três.
    #
    # Ela dizia "Deriva v0.0" onde havia versão, "Unidade I" onde não havia, e
    # nada nas folhas de abertura: o mesmo lugar carregando três coisas. Agora
    # ela diz sempre onde o leitor está na trilha, e acrescenta a versão sob
    # inspeção quando a aula entrega uma - que é o que o contrato prometeu,
    # sem inventar versão para a aula que não entrega nenhuma.
    cabeca = f"Unidade {a['unidade']}" + (f" · Deriva {v}" if v else "")
    return nome_u, f"{n:02d}", versao, cabeca


def preparar(rel: str, txt: str, alvo: str = "tex") -> str:
    n = None
    # `00-prefacio.md` casava com o padrão e virava "aula 0", que o mapa define
    # como o Anexo A: o prefácio recebia os trechos de C++20 do anexo, e a
    # folha 3 do livro abria com uma prancha de `std::views`.
    if (rel.startswith("capitulos/") and rel[10:12].isdigit()
            and rel != "capitulos/00-prefacio.md"):
        n = int(rel[10:12])

    # 1) os blocos de código, antes de tudo: eles contêm `#` e `|` que o resto
    #    das regras leria como cabeçalho e como tabela
    txt = converter_codigo(txt, alvo)

    # 2) a abertura de capítulo
    def h1(m):
        titulo = m.group("titulo").strip()
        dados = abertura(n, rel)
        if not dados:
            if alvo == "html":
                return f"\n# {titulo}\n"
            return ("\n```{=latex}\n"
                    "\\capituloabresimples{" + esc_tex(titulo) + "}\n```\n")
        nome_u, aula, versao, cabeca = dados
        num = str(n)
        # o título do capítulo já traz "Capítulo N - "; o número vai à moldura
        limpo = re.sub(r"^Cap[íi]tulo\s+\d+\s*[-\u2013\u2014]\s*", "", titulo)
        if alvo == "html":
            # Cabeçalho de markdown de verdade, e não HTML cru: como HTML cru
            # o pandoc não o via, e o sumário da tela saía com as 200 seções
            # aninhadas sob "Prefácio", sem um capítulo que as agrupasse.
            u = nome_u.replace('\\char"00B7\\ ', "· ")
            return (f"\n# Capítulo {num} - {limpo}\n\n"
                    f"[{u} · aula {aula} · {versao}]{{.cap__moldura}}\n")
        return ("\n```{=latex}\n"
                f"\\capituloabre{{{num}}}{{{esc_tex(limpo)}}}{{{nome_u}}}"
                f"{{{aula}}}{{{esc_tex(versao)}}}{{{esc_tex(cabeca)}}}\n```\n")

    txt = RX_H1.sub(h1, txt, count=1)

    # 3) os carimbos, parágrafo por parágrafo. Só na prosa: bloco cru, caixa e
    #    tabela ficam de fora, porque marginnote dentro deles sai deslocado.
    # O carimbo repete a cada SEÇÃO, e não uma vez por capítulo: um capítulo
    # de dez seções que afirma o mesmo número em três delas merece o lastro
    # nas três, porque o leitor de uma seção não viu a anterior.
    gastos: set = set()
    blocos = txt.split("\n\n")

    # A prancha de código atravessa texto MAIS campo de aferição, então um
    # carimbo vizinho de um bloco cai em cima da moldura. Era o que acontecia:
    # a nota direita da régua e o carimbo disputavam os mesmos 35 mm.
    #
    # A regra é de posição, e não de sorte: o carimbo só sai onde o campo
    # está livre, ou seja, com prosa suficiente antes do próximo bloco para
    # ele ter altura. Cinco linhas é a altura do carimbo.
    def campo_livre(i: int) -> bool:
        vistos = 0
        for j in range(i + 1, min(i + 4, len(blocos))):
            s = blocos[j].lstrip()
            if s.startswith("```"):
                return vistos >= 2
            if s and not s.startswith((":::", "|", "\\")):
                vistos += 1
        return True

    fora, dentro_cru, ultimo_carimbo = [], False, -99
    for i, par in enumerate(blocos):
        fora.append(par)
        crus = par.count("```")
        if crus % 2:
            dentro_cru = not dentro_cru
        if dentro_cru or crus:
            continue
        p = par.strip()
        if p.startswith("\\secaoabre") or p.startswith("## "):
            gastos = set()
        if not p or p.startswith(("#", ":::", "|", ">", "-", "*", "+")):
            continue
        if not campo_livre(i):
            continue
        # `marginnote` não empilha: dois carimbos ancorados a três parágrafos
        # de distância caem um sobre o outro, e foi o que aconteceu nas
        # páginas 112 e 160. Seis parágrafos é mais que a altura de uma
        # página, então dois carimbos nunca disputam o mesmo campo.
        if i - ultimo_carimbo < 6:
            continue
        novo_par, grandeza = carimbar(p, gastos, alvo)
        if grandeza:
            fora[-1] = novo_par
            ultimo_carimbo = i
    return "\n\n".join(fora)


def ordem() -> list[str]:
    itens = ["capitulos/00-prefacio.md"]
    itens += [f"capitulos/{a['n']:02d}-{a['slug']}.md" for a in mapa.AULAS]
    itens += ["anexos/A-concepts-ranges.md", "anexos/B-referencia-c17.md",
              "anexos/C-deriva-20-versoes.md", "anexos/glossario.md",
              "anexos/referencias.md"]
    return itens


def main() -> int:
    if not FONTES.exists() or not any(FONTES.glob("*.ttf")):
        print("ERRO: faltam as fontes em build/fontes-tex/ - rode `make fontes-tex`")
        return 1
    SAIDA.mkdir(parents=True, exist_ok=True)

    partes = []
    for rel in ordem():
        p = LIVRO / rel
        if not p.exists():
            print("FALTA:", rel)
            return 1
        partes.append(preparar(rel, p.read_text(encoding="utf-8")).strip() + "\n")

    md = SAIDA / "livro-impressao.md"
    md.write_text("\n\n".join(partes), encoding="utf-8")

    M = medidas.MEDIDAS
    gab = (ESTILO / "livro.tex").read_text(encoding="utf-8")
    gab_usado = SAIDA / "gabarito.tex"
    gab_usado.write_text(gab.replace("FONTEDIR", str(FONTES)), encoding="utf-8")

    tex = SAIDA / "livro.tex"
    cmd = ["pandoc", str(md),
           "--from", "markdown+raw_attribute+fenced_divs+pipe_tables+grid_tables+"
         "tex_math_dollars+autolink_bare_uris+bracketed_spans",
           "--to", "latex",
           "--template", str(gab_usado),
           "--lua-filter", str(ESTILO / "livro.lua"),
           "--top-level-division=chapter",
           "-M", "title=Programação Orientada a Objetos em C++",
           "-M", "subtitle=Um curso construído sobre um sistema que compila",
           "-M", f"author={mapa.AUTOR}",
           "-M", f"semestre={mapa.SEMESTRE}",
           "-M", f"sistema=Deriva {M['versao']}, roguelike de terminal",
           "-M", f"padrao=C++17, e ele é teto",
           "-M", f"portao=4 de 4 · {M['testes']} testes verdes · {M['avisos']} avisos",
           "-M", f"estrutura={len(mapa.AULAS)} capítulos · {len(mapa.ANEXOS)} anexos",
           "-M", f"trechos={len(CODIGO)} extraídos por âncora, nenhum digitado",
           "-o", str(tex)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("pandoc falhou:\n" + r.stderr[-3000:])
        return 1
    if r.stderr.strip():
        print("pandoc avisou:", r.stderr.strip()[:600])

    # Desfazer a conversão de risca do pandoc.
    #
    # O `smart` do pandoc é o que dá aspas curvas à prosa portuguesa, e vale
    # mantê-lo. Ele também converte `--` em meia-risca e `---` em travessão, e
    # a regra 6.4 da voz do autor proíbe os dois caracteres em QUALQUER
    # registro. `verifica_voz.py` garante que o fonte não os tem; logo, todo
    # um que apareça aqui veio dessa conversão, e desfazê-la é determinístico
    # e não ambíguo. O `{}` no meio impede o LaTeX de religar.
    #
    # O que isso salvava: `--replay`, `--leiaute`, `ctest --test-dir` e as
    # réguas `// ------` saíam com risca, e um leitor que copiasse o comando
    # do livro receberia erro do shell.
    bruto = tex.read_text(encoding="utf-8")
    riscas = bruto.count("\u2013") + bruto.count("\u2014")
    if riscas:
        bruto = bruto.replace("\u2014", "-{}-{}-").replace("\u2013", "-{}-")

    # E desfazer a ligadura de ASPA, que vem do outro lado do pandoc.
    #
    # O filtro `Quoted` emite `“` e `”` em Unicode, e o ESCRITOR LaTeX do
    # pandoc os reconverte para ``  e '' , que é a representação de aspa em
    # TeX. Com `Mapping=tex-text` desligado - e ele está desligado porque
    # convertia `--` em meia-risca - aquilo sai impresso como dois graves e
    # dois apóstrofos: 82 aspas literais em 32 folhas.
    #
    # A linha de código é poupada: `\codelinha` pode conter dois apóstrofos
    # seguidos de verdade, num literal de caractere em C++.
    aspas = 0
    fora = []
    for linha in bruto.split("\n"):
        if linha.lstrip().startswith("\\codelinha"):
            fora.append(linha)
            continue
        aspas += linha.count("``") + linha.count("''")
        fora.append(linha.replace("``", "\u201c").replace("''", "\u201d"))
    bruto = "\n".join(fora)

    if riscas or aspas:
        tex.write_text(bruto, encoding="utf-8")
        print(f"  ligaduras desfeitas: {riscas} risca(s) e {aspas} aspa(s) "
              "que o pandoc introduz na escrita, e que a regra 6.4 e a "
              "tipografia portuguesa não querem")

    if "--tela" in sys.argv:
        render_tela()
    if "--tex" in sys.argv:
        print(f"tex: {tex.relative_to(RAIZ)} · {tex.stat().st_size // 1024} KB")
        return 0

    for passada in (1, 2):
        r = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "livro.tex"],
            cwd=SAIDA, capture_output=True, text=True)
        if r.returncode:
            erros = [l for l in r.stdout.splitlines()
                     if re.search(r":\d+:|^!", l)][:25]
            print(f"XeLaTeX falhou na passada {passada}:")
            print("\n".join(erros) or r.stdout[-3000:])
            return 1

    pdf = SAIDA / "livro.pdf"
    destino = LIVRO / "poo-v2.pdf"
    shutil.copy(pdf, destino)
    paginas = 0
    m = re.search(r"Output written on .*?\((\d+) pages", r.stdout)
    if m:
        paginas = int(m.group(1))
    over = len(re.findall(r"^Overfull \\hbox", r.stdout, re.M))
    print(f"PDF: {destino.relative_to(RAIZ)} · {destino.stat().st_size // 1024} KB · "
          f"{paginas} páginas · {over} linhas transbordando")
    return 0


def render_tela() -> None:
    """A versão de tela: mesmo mundo, fundo de fósforo em vez de papel.

    Ela NÃO reaproveita o markdown do impresso: aquele carrega blocos de
    LaTeX cru, que o pandoc descarta ao escrever HTML - e o livro sairia sem
    um bloco de código e sem um carimbo. Cada alvo tem o seu emissor, e o
    tokenizador do realce é o mesmo dos dois.
    """
    partes = []
    for rel in ordem():
        p = LIVRO / rel
        if p.exists():
            partes.append(preparar(rel, p.read_text(encoding="utf-8"),
                                   "html").strip() + "\n")
    md = SAIDA / "livro-tela.md"
    md.write_text("\n\n".join(partes), encoding="utf-8")

    html = LIVRO / "livro.html"
    r = subprocess.run(
        ["pandoc", str(md),
         "--from", "markdown+raw_attribute+fenced_divs+pipe_tables+grid_tables+"
         "tex_math_dollars+autolink_bare_uris+bracketed_spans",
         "--to", "html5", "--toc", "--toc-depth=2", "--standalone",
         # Gabarito próprio, e não o do pandoc. Ele emitia três blocos <style>
         # separados - os dele, e um por `--css` - e o desenho perdia para o
         # primeiro. Aqui há um <style> só, com as duas folhas dentro, e o
         # <head> passa a ser nosso: lang, viewport, autor e descrição.
         "--template", str(ESTILO / "livro-tela.html"),
         "--lua-filter", str(ESTILO / "livro.lua"),
         "-M", "title=Programação Orientada a Objetos em C++",
         "-M", "subtitle=Um curso construído sobre um sistema que compila",
         "-M", "lang=pt-BR",
         "-M", f"author={mapa.AUTOR}",
         "-M", f"semestre={mapa.SEMESTRE}",
         "-M", f"sistema=Deriva {medidas.MEDIDAS['versao']}, roguelike de terminal",
         "-M", "padrao=C++17, e ele é teto",
         "-M", f"portao=4 de 4 · {medidas.MEDIDAS['testes']} testes verdes · "
               f"{medidas.MEDIDAS['avisos']} avisos",
         "-M", f"estrutura={len(mapa.AULAS)} capítulos · {len(mapa.ANEXOS)} anexos",
         "-M", f"trechos={len(CODIGO)} extraídos por âncora, nenhum digitado",
         # O template do pandoc traz CSS proprio, com fundo branco e medida
         # propria, e ele briga com a grade desta folha: o detector media o
         # contraste do ambar contra branco. `document-css=false` o remove, e
         # quem desenha a pagina passa a ser tokens.css mais livro.css.
         # `document-css=false` NÃO funciona: o template faz `$if(document-css)$`, e
         # a string "false" é não vazia, logo verdadeira. O valor tem de ser
         # VAZIO. Sem isso o pandoc injetava `html{background-color:#fdfdfd}` e
         # `body{max-width:36em;padding:50px}`, que pintavam um fundo quase
         # branco atrás do fósforo e brigavam com a grade de três colunas.
         "-V", "document-css=",
         "-o", str(html)],
        capture_output=True, text=True)
    if r.returncode:
        print("tela falhou:", r.stderr[-1500:])
        return

    # As folhas entram aqui, e não pelo `--css` do pandoc.
    #
    # Um arquivo só: o livro de tela é para o estudante salvar e abrir sem
    # rede, e folha externa por caminho relativo quebra assim que o arquivo
    # sai da pasta. E `--embed-resources` resolvia o caminho a partir do
    # diretório de trabalho, não da saída, e embutia nada em silêncio.
    folhas = [RAIZ / "poo" / "css" / "tokens.css", RAIZ / "poo" / "css" / "livro.css"]
    css = "\n\n".join(f"/* {f.name} */\n" + f.read_text(encoding="utf-8")
                       for f in folhas)
    txt = html.read_text(encoding="utf-8")
    assert "/* AS-FOLHAS */" in txt, "o gabarito de tela perdeu o lugar do CSS"
    html.write_text(txt.replace("/* AS-FOLHAS */", css), encoding="utf-8")
    print(f"tela: {html.relative_to(RAIZ)} · {html.stat().st_size // 1024} KB · "
          f"um arquivo, {len(css) // 1024} KB de folha embutida")


if __name__ == "__main__":
    sys.exit(main())
