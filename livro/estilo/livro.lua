-- livro/estilo/livro.lua - filtro do pandoc para o livro impresso.
--
-- Só o que precisa da árvore do pandoc mora aqui: cabeçalho de seção, que
-- carrega marcação inline no título, e as divs tipadas, cujo miolo é markdown
-- de verdade (tabela, lista, código embutido). Bloco de código e abertura de
-- capítulo já chegam como LaTeX cru, montados por build/render_livro.py, que
-- é quem tem acesso ao mapa e ao realce de sintaxe.

-- O glifo e o rótulo de cada caixa. Os cinco vêm de `conteudo/mapa.py`, que
-- é a tabela canônica; repetidos aqui porque o filtro do pandoc é Lua e não
-- importa Python. `build/verifica_numeros.py` confere que não divergiram.
-- O glifo já sai na face que o TEM, e não embrulhado em `\geo` por atacado.
--
-- O suplemento geométrico cobre os dez triângulos e losangos, e mais nada:
-- `✓` e `·` vivem no Plex Mono. O gabarito embrulhava os cinco em `\geo`, e
-- o marcador do DICA saía como retângulo vazio em onze folhas - inclusive na
-- folha que explica ao estudante o que cada caixa significa.
-- O glifo e a FACE que o tem, em campos separados.
--
-- Guardá-los juntos como "{\\geo ▲}" obrigava a tela a desmontar a string
-- por padrão de Lua, e o padrão não casava: os títulos da tela saíam
-- "{\\geo ▸ DERIVA". Separados, cada alvo compõe o que precisa e nenhum
-- desmonta nada.
--
-- A face não é decoração: o suplemento geométrico cobre os dez triângulos e
-- losangos, e `✓` e `·` vivem no Plex Mono. O gabarito embrulhava os cinco em
-- `\geo`, e o marcador do DICA saía como retângulo vazio em onze folhas -
-- inclusive na folha que explica ao estudante o que cada caixa significa.
-- O rótulo vem em CAIXA-ALTA aqui, literal, e não por `string.upper`.
--
-- `string.upper` do Lua trabalha em bytes: ele não sobe `ç` nem `ã`, e o
-- rótulo saía "ATENçãO" nas 28 caixas de aviso do livro. Como são cinco
-- rótulos fixos, declará-los prontos remove a transformação e o defeito
-- junto. Os cinco são os de `conteudo/mapa.py`, que é a tabela canônica.
local CAIXAS = {
  warn   = { glifo = "▲", face = "geo",      rot = "ATENÇÃO" },
  tip    = { glifo = "✓", face = "ttfamily", rot = "DICA" },
  llm    = { glifo = "◇", face = "geo",      rot = "LLM" },
  info   = { glifo = "·", face = "ttfamily", rot = "NOTA" },
  deriva = { glifo = "▸", face = "geo",      rot = "DERIVA" },
}

-- Um filtro, dois alvos. O impresso é o artefato primário e a tela herda a
-- estrutura dele; o que muda é a marcação, não o desenho.
local HTML = FORMAT:match("html")

local function cru(s)
  return pandoc.RawBlock(HTML and "html" or "latex", s)
end

-- A moldura de caractere, na tela.
--
-- Mesma primitiva do site e do impresso: `┌─`, título embutido na régua de
-- cima, e `─┐`. A régua é uma corrida de `─` de verdade, cortada por
-- `overflow: hidden`, e não uma `border` - que é o que o PRODUCT.md nomeia
-- como sinal de resultado errado. Sem JS: o traço vai escrito, para o
-- arquivo servir salvo e offline.
local TRACO = string.rep("─", 200)

local function molduraHtml(titulo, base)
  local canto_e = base and "└─" or "┌─"
  local canto_d = base and "─┘" or "─┐"
  local t = ""
  if titulo and titulo ~= "" then
    t = '<span class="moldura__canto">─┤</span>'
      .. '<span class="moldura__titulo">' .. titulo .. '</span>'
      .. '<span class="moldura__canto">├</span>'
  end
  return '<div class="moldura" aria-hidden="true">'
    .. '<span class="moldura__canto">' .. canto_e .. '</span>' .. t
    .. '<span class="moldura__regua">' .. TRACO .. '</span>'
    .. '<span class="moldura__canto">' .. canto_d .. '</span></div>'
end

-- O título do sumário COM a marcação, e não achatado.
--
-- Era `pandoc.utils.stringify`, e o sumário impresso saía com `make verifica`
-- e `printf/scanf` em Serif, enquanto o corpo e o sumário da tela os
-- mostravam em Mono. Neste material a face é o papel semântico, então os dois
-- irmãos discordavam na mesma tabela de conteúdo.
--
-- Isto funciona porque `Header` roda em passada PRÓPRIA (ver o `return` no
-- fim do arquivo): os `Code` ainda são `Code` aqui, e o escritor do pandoc os
-- rende como `\texttt`. O `\protect` vai por precaução, porque o `.toc` é
-- escrito e relido, e comando frágil não sobrevive à ida e volta.
local function chapo(inlines)
  local tex = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "latex")
  tex = tex:gsub("%s+$", ""):gsub("\n", " ")
  return (tex:gsub("\\(%a+)", "\\protect\\%1"))
end

function Header(el)
  if el.level == 1 then
    -- No impresso a abertura é montada em Python, que sabe a unidade, a aula
    -- e a versão do Deriva, e o H1 desaparece. Na tela ele FICA: sem um H1 de
    -- verdade o pandoc não constrói o sumário, e ele saía com as 200 seções
    -- soltas, sem o capítulo que as agrupa.
    if HTML then return el end
    return {}
  end

  local inlines = el.content
  local numero = ""
  local primeiro = inlines[1]
  if primeiro and primeiro.t == "Str" and primeiro.text:match("^[%dA-C]+%.[%d%.]+$") then
    numero = primeiro.text:gsub("%.$", "")
    inlines = pandoc.List(inlines):filter(function(_, i) return i > 1 end)
    while inlines[1] and inlines[1].t == "Space" do inlines:remove(1) end
  end

  -- O v1 embrulhava todo H3 em negrito. O nível já é o negrito; o embrulho
  -- duplicado deixava o Plex Serif SemiBold sobre SemiBold.
  if #inlines == 1 and inlines[1].t == "Strong" then inlines = inlines[1].content end

  local nivel = (el.level == 2) and "secao" or "subsecao"
  local toc = (nivel == "secao") and "section" or "subsection"
  local rotulo = numero ~= "" and ("\\protect\\numberline{" .. numero .. "}") or ""

  -- O número e o título vão no MESMO bloco.
  --
  -- Antes o número era um RawBlock e o título um Plain, e o pandoc separa
  -- bloco de bloco com linha vazia: o `\par` entre os dois punha `§5.4` numa
  -- linha e "Posicionando as Linguagens" na seguinte, em todas as 200 seções
  -- do livro. Como RawInline dentro do mesmo Plain, eles ficam na mesma linha.
  if HTML then
    -- O número entra como <span class="num">, que a folha de tela desenha em
    -- Mono âmbar, do mesmo modo que o § do impresso.
    local dentro = pandoc.List({})
    if numero ~= "" then
      dentro:insert(pandoc.Span({ pandoc.Str("§" .. numero) }, { class = "num" }))
      -- o espaço é explícito: no sumário o pandoc achata o span e saía
      -- `§1.1Gerenciamento`, sem separação
      dentro:insert(pandoc.Space())
    end
    dentro:extend(inlines)
    return pandoc.Header(el.level, dentro, el.attr)
  end

  local miolo = pandoc.List({})
  if nivel == "secao" then
    miolo:insert(pandoc.RawInline("latex", "\\secaoabre{" .. numero .. "}"))
  else
    miolo:insert(pandoc.RawInline("latex", "\\subsecaoabre "))
  end
  miolo:extend(inlines)
  miolo:insert(pandoc.RawInline("latex", "\\" .. nivel .. "fecha"))

  return {
    pandoc.Plain(miolo),
    -- Sem re-escapar: `chapo` já devolve LaTeX pronto do escritor do pandoc,
    -- e escapar de novo transformaria `\texttt{...}` em texto visível.
    cru("\\addcontentsline{toc}{" .. toc .. "}{" .. rotulo ..
        chapo(inlines) .. "}"),
  }
end

function Div(el)
  local cls = el.classes

  if cls:includes("callout") then
    for tipo, d in pairs(CAIXAS) do
      if cls:includes(tipo) then
        local rot = d.glifo .. " " .. d.rot
        if HTML then
          return { cru(molduraHtml(rot, false)), el,
                   cru(molduraHtml(nil, true)) }
        end
        return { cru("\\begin{callout}{{\\" .. d.face .. " " .. d.glifo
                       .. "}}{" .. d.rot .. "}") }
            .. el.content .. { cru("\\end{callout}") }
      end
    end
    error("div .callout sem tipo conhecido: " .. table.concat(cls, " "))
  end

  if cls:includes("objetivos") then
    if HTML then
      return { cru(molduraHtml("O QUE ESTE CAPÍTULO ENTREGA", false)), el,
               cru(molduraHtml(nil, true)) }
    end
    return { cru("\\begin{objetivos}") } .. el.content .. { cru("\\end{objetivos}") }
  end

  if cls:includes("unidade") then
    local n = el.attributes["data-n"] or ""
    if HTML then
      return { cru(molduraHtml("UNIDADE " .. n, false)), el,
               cru(molduraHtml(nil, true)) }
    end
    return { cru("\\begin{unidade}{" .. n .. "}") } .. el.content
        .. { cru("\\end{unidade}") }
  end

  if cls:includes("figura") then
    if HTML then
      return { cru(molduraHtml("DIAGRAMA UML", false)), el,
               cru(molduraHtml(nil, true)) }
    end
    return { cru("\\begin{figurauml}") } .. el.content .. { cru("\\end{figurauml}") }
  end

  return el
end

-- Tabela densa: o pandoc emite longtable, que é o certo num livro (a tabela
-- atravessa a quebra de página em vez de saltar para a página seguinte).
-- Só o corpo encolhe, para caber a medida.
function Table(el)
  if HTML then return el end
  -- Sem `\\ttfamily`. O pandoc dimensiona as colunas contando caracteres para
  -- fonte proporcional, e o Plex Mono é mais largo: célula de prosa
  -- transbordava a coluna. Prosa em Serif, e o que é código na célula já vem
  -- em crase e sai em Mono pelo filtro de `Code`.
  --
  -- A tabela atravessa texto MAIS campo de aferição, como a prancha, e pela
  -- razão irmã: grade densa não reflui sem perder o alinhamento das colunas.
  -- A prosa mantém a medida de 66 caracteres; o que é grade reclama os
  -- 174 mm. O pandoc calcula largura de coluna como fração de `\linewidth`,
  -- então mudá-lo escala as colunas sozinho.
  return { cru("\\begin{tabelalarga}"), el, cru("\\end{tabelalarga}") }
end


-- Código embutido na prosa: `variantes/v0.3-quebrada/` e
-- `include/deriva/inventario.hpp` são uma palavra só para o TeX, e não tinham
-- onde ceder. A barra, o sublinhado, os dois-pontos e o ponto passam a ser
-- ponto de quebra; a hifenização de palavra de largura fixa (hyphenat/htt)
-- cuida do resto.
local ESC = {
  ["\\"] = "\\textbackslash{}", ["{"] = "\\{", ["}"] = "\\}",
  ["$"] = "\\$", ["&"] = "\\&", ["#"] = "\\#",
  ["^"] = "\\textasciicircum{}", ["_"] = "\\_",
  ["~"] = "\\textasciitilde{}", ["%"] = "\\%",
}

function Code(el)
  if HTML then return el end
  -- Os caracteres em vetor, para saber qual é o ÚLTIMO.
  --
  -- Um `\\allowbreak` no fim do trecho abre quebra onde nada segue, e numa
  -- célula de tabela isso deslocava a fileira inteira em 9,1 pt: o
  -- `unique_ptr<T>` da primeira coluna sentava uma linha abaixo das outras
  -- três, em todas as fileiras. Nada quebra depois do último caractere.
  local chars = {}
  for c in el.text:gmatch(utf8 and utf8.charpattern or ".") do
    chars[#chars + 1] = c
  end
  local fora = {}
  for i, c in ipairs(chars) do
    fora[#fora + 1] = ESC[c] or c
    -- `<`, `>` e `,` faltavam, e `vector<std::unique_ptr<entidade>>` não
    -- tinha um único lugar onde ceder: 32 pt de transbordo.
    if i < #chars and c:match("[/_:%.<>,&%*%(%)]") then
      fora[#fora + 1] = "\\allowbreak{}"
    end
  end
  return pandoc.RawInline("latex", "\\texttt{" .. table.concat(fora) .. "}")
end

-- URL de referência bibliográfica: 92 pt de transbordo vinham de um href que
-- não quebra. O texto visível recebe os mesmos pontos de cessão.
--
-- A ordem importa e custou uma passada: escapar as chaves DEPOIS de inserir
-- `\\allowbreak{}` transformava o comando em texto, e o leitor via
-- `https:/\\allowbreak{}/en.\\allowbreak{}cppreference.com` impresso.
-- Escapa-se primeiro, insere-se depois.
function Link(el)
  if HTML then return el end
  local visivel = pandoc.utils.stringify(el.content)
  local eh_url = visivel == el.target
      or (el.target:find("^https?://") and visivel:find("^https?://"))
  if not eh_url then return el end
  local esc = visivel:gsub("([%%#&_%${}\\])", "\\%1")
  local quebrado = esc:gsub("([/%._%-%?&=])", "%1\\allowbreak{}")
  local alvo = el.target:gsub("([#%%])", "\\%1")
  return pandoc.RawInline("latex",
    "\\href{" .. alvo .. "}{\\texttt{\\small " .. quebrado .. "}}")
end

-- Aspas em Unicode, e não pela ligadura do TeX.
--
-- O pandoc emite `` e '' para aspa, e quem os transformava em “ ” era
-- `Ligatures=TeX`. A mesma opção convertia `--` em meia-risca, o que a regra
-- 6.4 proíbe, então ela saiu de todas as famílias. As aspas vêm daqui.
function Quoted(el)
  local a, f = "“", "”"
  if el.quotetype == "SingleQuote" then a, f = "‘", "’" end
  local fora = pandoc.List({ pandoc.Str(a) })
  fora:extend(el.content)
  fora:insert(pandoc.Str(f))
  return fora
end


-- Glifo que as famílias de texto não têm.
--
-- `▲△▶▷▸▼◀◁◆◇` não existem em nenhuma das três famílias do Plex, e `─` existe
-- só no Mono. Quando a prosa os escreve - e ela escreve: o prefácio nomeia o
-- vocabulário das caixas, a tabela de UML usa a notação de seta e de losango -
-- o XeLaTeX cai numa quarta face e imprime U+FFFF, um retângulo vazio. Eram
-- 35 ocorrências em 21 folhas, e o portão não as via porque contava U+FFFD e
-- U+25A1, e não U+FFFF, que é o que o XeLaTeX escreve.
--
-- Cada um é roteado para a face que o tem, caractere por caractere. Não é
-- fallback automático (o XeLaTeX não tem; o LuaLaTeX teria): é despacho
-- explícito, e por isso não falha em silêncio.
--
-- A busca é por TABELA e não por classe de caractere, e a diferença custou
-- uma passada: padrão do Lua trabalha em bytes, então `[▲◇]` casa com os
-- BYTES desses caracteres, e `ó` (0xC3 0xB3) casa com o 0xB2/0xB3 de `▲`.
-- A primeira versão embrulhou letra acentuada em `\geo` e produziu 1111
-- retângulos vazios, contra os 35 que existiam.
local FACE = {
  ["▲"] = "geo", ["△"] = "geo", ["▶"] = "geo", ["▷"] = "geo", ["▸"] = "geo",
  ["▼"] = "geo", ["◀"] = "geo", ["◁"] = "geo", ["◆"] = "geo", ["◇"] = "geo",
  ["─"] = "ttfamily",
}

function Str(el)
  if HTML then return el end
  local achou = false
  for ch in el.text:gmatch(utf8.charpattern) do
    if FACE[ch] then achou = true break end
  end
  if not achou then return el end

  local fora, acum = pandoc.List({}), {}
  local function despejar()
    if #acum > 0 then
      fora:insert(pandoc.Str(table.concat(acum)))
      acum = {}
    end
  end
  for ch in el.text:gmatch(utf8.charpattern) do
    local face = FACE[ch]
    if face then
      despejar()
      fora:insert(pandoc.RawInline("latex", "{\\" .. face .. " " .. ch .. "}"))
    else
      acum[#acum + 1] = ch
    end
  end
  despejar()
  return fora
end


-- DUAS passadas, e a ordem é o conserto.
--
-- Num filtro só, o pandoc percorre os inlines antes dos blocos: `Code` já
-- havia virado `RawInline` quando `Header` chamava `stringify` para montar a
-- linha do sumário, e `stringify` de um `RawInline` devolve "". O sumário
-- saía com "2.4 O portão" sem objeto, "3.2 Strings: de a" e "3.1 Entrada e
-- saída: de / a /".
--
-- Devolver uma LISTA de tabelas de filtro faz o pandoc rodar cada uma numa
-- passada: `Header` primeiro, com os `Code` ainda intactos, e o resto depois.
return {
  { Header = Header },
  { Div = Div, Code = Code, Link = Link, Table = Table,
    Quoted = Quoted, Str = Str },
}
