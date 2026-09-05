---
name: Material de POO · UFPB
description: Fósforo âmbar sobre preto de viés esverdeado na tela, tinta sobre papel no impresso, e a mesma moldura de caractere nos dois.
colors:
  vazio: "#0A0C0B"
  painel: "#101413"
  painel-alto: "#161C1A"
  grade: "#1E2624"
  grade-alta: "#2C3835"
  fosforo: "#F2A93B"
  fosforo-alto: "#FFD79A"
  leitura: "#E4E7E2"
  apagado: "#8A928C"
  fantasma: "#4A524C"
  ok: "#6FD08C"
  falha: "#FF6B5E"
  frio: "#5FC3D6"
  outro: "#C08BE0"
  ufpb: "#1a56a0"
  papel: "#FFFFFF"
  tinta: "#1A1C1B"
  ambar-impresso: "#7E4A06"
  ambar-claro-impresso: "#C89A52"
  apagado-impresso: "#5C625E"
  fantasma-impresso: "#9AA09C"
  vazio-papel: "#FFFFFF"
  painel-papel: "#F4F5F3"
  painel-alto-papel: "#ECEEE9"
  grade-papel: "#C3C8C2"
  grade-alta-papel: "#9AA19A"
  fosforo-papel: "#7A4B00"
  fosforo-alto-papel: "#4D2F00"
  leitura-papel: "#161A18"
  apagado-papel: "#4A514C"
  fantasma-papel: "#656C66"
  ok-papel: "#1C6B34"
  falha-papel: "#A8201A"
  frio-papel: "#12586A"
  outro-papel: "#5A2F78"
typography:
  capa:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "clamp(30px, 7.5vw, 56px)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  h1:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "34px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  h2:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "23px"
    fontWeight: 600
    lineHeight: 1.25
  prosa:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.68
  codigo:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
  estado:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
  rotulo:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "max(11px, 11px)"
    fontWeight: 600
    letterSpacing: "0.12em"
    textTransform: "uppercase"
  legenda:
    fontFamily: "IBM Plex Sans, system-ui, -apple-system, sans-serif"
    fontSize: "14px"
    fontWeight: 400
spacing:
  e00: "2px"
  e0: "4px"
  e1: "6px"
  e2: "12px"
  e3: "18px"
  e4: "28px"
  e5: "40px"
  e6: "56px"
  e7: "84px"
  goteira: "32px"
  campo: "230px"
  arvore: "300px"
  medida: "68ch"
  pagina-max: "1500px"
components:
  moldura:
    textColor: "{colors.grade-alta}"
    typography: "{typography.rotulo}"
    rounded: "0"
    padding: "0"
  moldura-titulo:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
    padding: "0 0.35em"
  prancha:
    backgroundColor: "{colors.painel-alto}"
    textColor: "{colors.leitura}"
    typography: "{typography.codigo}"
    rounded: "0"
    padding: "18px"
  caixa-tipada:
    backgroundColor: "{colors.painel}"
    textColor: "{colors.leitura}"
    typography: "{typography.prosa}"
    rounded: "0"
    padding: "12px 18px"
  carimbo:
    textColor: "{colors.apagado}"
    typography: "{typography.rotulo}"
    padding: "0"
    width: "{spacing.campo}"
  carimbo-valor:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
  ficha:
    textColor: "{colors.leitura}"
    typography: "{typography.rotulo}"
    padding: "0 0 0 6px"
    width: "{spacing.campo}"
  ficha-rotulo:
    textColor: "{colors.apagado}"
    typography: "{typography.rotulo}"
  tabela-cabeca:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
    padding: "6px 12px"
  tabela-celula:
    textColor: "{colors.leitura}"
    typography: "{typography.estado}"
    padding: "6px 12px"
  botao-primario:
    backgroundColor: "{colors.fosforo}"
    textColor: "{colors.vazio}"
    typography: "{typography.estado}"
    rounded: "0"
    padding: "0 12px"
    height: "44px"
  botao-primario-hover:
    backgroundColor: "{colors.fosforo-alto}"
    textColor: "{colors.vazio}"
  botao:
    backgroundColor: "{colors.painel-alto}"
    textColor: "{colors.leitura}"
    typography: "{typography.estado}"
    rounded: "0"
    padding: "0 12px"
    height: "44px"
  botao-hover:
    backgroundColor: "{colors.painel-alto}"
    textColor: "{colors.fosforo}"
  unidade:
    backgroundColor: "{colors.painel}"
    textColor: "{colors.apagado}"
    typography: "{typography.estado}"
    padding: "12px"
---

# Design System: Material de POO · UFPB

## Overview

**Creative North Star: "O Caderno de Bordo da Sonda"**

O mundo é o terminal da estação que o estudante constrói: fósforo âmbar sobre
preto de viés esverdeado na tela, e a mesma estrutura traduzida para tinta sobre
papel no impresso. A estética é diegética, e essa é a razão de o box-drawing ser
a única primitiva de moldura: o painel do site é literalmente a interface do
Deriva. São três artefatos e uma fonte - 38 páginas de site, o livro em PDF
composto por XeLaTeX e a versão de tela do livro -, e o desenho existe para que
os três afirmem a mesma coisa.

A estrutura é o caderno de bordo, e ela tem três faixas: coluna de prosa em
Serif na medida de leitura, campo de aferição de Mono na margem externa onde
cada número afirmado recebe valor, comando e arquivo, e prancha de código
atravessando os dois, porque código não reflui. Desde a passada de leiaute do
site, essa terceira faixa deixou de ser exclusividade do livro: acima de 1360 px
a página de aula é a mesma grade de três colunas
(`poo/css/pagina.css:751-811`). A densidade é alta e deliberada; o silêncio é
raro e reservado à folha de abertura de unidade do livro.

Cor nunca é o único portador de significado: todo estado semântico chega com
glifo geométrico e rótulo textual ao lado. Prosa nunca é âmbar. O âmbar é
moldura, rótulo, cursor, carimbo e ênfase de interface, e é a raridade dele que
o faz ler como interface e não como decoração.

**Key Characteristics:**
- Moldura de box-drawing como caractere real, nunca `border`
- Três famílias e três papéis semânticos, mais um suplemento geométrico
- Campo de aferição na margem externa, agora nos três artefatos
- Prancha de código atravessando prosa mais campo, sem refluxo
- Um tema só, escuro na tela, e um remapeamento completo de tokens no papel
- Zero raio de canto, zero emoji
- Projeção é escala e não modo, com uma exceção declarada

### O diagrama é elemento, e não figura solta

Os quatro diagramas em Mermaid entram pelo caminho da prancha: vivem em
`exemplos/deriva/diagramas/*.mmd`, são declarados por âncora em
`conteudo/trechos.py`, e o slide os recebe por referência - a moldura mostra
`diagramas/mapa-tem-grade.mmd:8`, do mesmo modo que a prancha mostra
`src/mapa.cpp:66`. Diagrama digitado no texto pode afirmar uma hierarquia que o
código não tem, e nada o denuncia; por âncora, `build/extrair_codigo.py` falha
se a âncora sair do arquivo, e `testes/test_uml.cpp` afirma as relações que o
desenho declara. Um diagrama declara `inline` em `trechos.py`, e por isso não
entra na seção "O código, extraído do Deriva" do fim da página.

## Colors

Uma paleta de fósforo de tubo, quente num preto levemente verde, com quatro
canais semânticos que só se acendem acompanhados de glifo e rótulo. O papel
recebe tradução, nunca inversão parcial.

### Primary
- **Fósforo Âmbar** (`{colors.fosforo}`, `tokens.css:21`): a cor da interface.
  Moldura em foco, título de moldura, `§` de seção, valor do carimbo, cabeça de
  tabela, marcador de objetivo, cursor de texto, anel de foco, segmento corrente
  do mapa de seções e galho da aula corrente. Nunca prosa.
- **Fósforo Alto** (`{colors.fosforo-alto}`): o degrau aceso do âmbar. Ênfase
  forte, código em linha, tipo no realce, estado de hover.
- **Âmbar de Papel** (`{colors.ambar-impresso}`): o âmbar do livro impresso,
  escuro porque a 8 pt o traço é fino e a antialiasagem o clareia.
- **Âmbar Claro de Papel** (`{colors.ambar-claro-impresso}`): só régua de
  moldura e fio de cabelo no impresso, que não carregam texto.

### Secondary
- **Frio** (`{colors.frio}`): elo de hipertexto (com fio de 1 px a 40% de
  opacidade sob ele), número no realce de sintaxe da tela e caixa tipada de LLM.
- **Outro** (`{colors.outro}`): marcação de C++20, sempre rotulada como fora do
  padrão-alvo.

### Tertiary
- **OK** (`{colors.ok}`): exclusivamente *compila*, mais literal de texto no
  realce. Sempre com glifo `✓` e rótulo.
- **Falha** (`{colors.falha}`): exclusivamente *quebrado de propósito*. Sempre
  com glifo `▲` e rótulo.
- **Azul UFPB** (`{colors.ufpb}`): só badge institucional e rodapé, e o badge
  sai da barra abaixo de 860 px porque o rodapé já o traz.

### Neutral
- **Vazio** (`{colors.vazio}`): o fundo, e o único. Recebe uma vinheta radial
  estática (`pagina.css:20`), sem animação: é fósforo, não CRT.
- **Painel** (`{colors.painel}`): fundo de caixa tipada, exercício, cartão de
  unidade e pé de bloco de código.
- **Painel Alto** (`{colors.painel-alto}`): fundo de prancha, de moldura de
  interativo e de código em linha. Dois degraus de superfície e não mais.
- **Grade** (`{colors.grade}`): fio fraco - régua de tabela, de barra, de pé.
- **Grade Alta** (`{colors.grade-alta}`): régua da moldura em repouso, régua do
  carimbo, contorno de painel de sistema, polegar da barra de rolagem.
- **Leitura** (`{colors.leitura}`): a prosa, o corpo do código, o valor de
  tabela e o valor da ficha.
- **Apagado** (`{colors.apagado}`): comentário de código, legenda, rótulo da
  ficha, corpo do carimbo, seção já vista no mapa. É a cor de todo texto
  terciário que carrega informação (5,4:1 sobre `{colors.painel-alto}`).
- **Fantasma** (`{colors.fantasma}`): andaime, e não texto (2,14:1 sobre
  `{colors.painel-alto}`). Galho da árvore, número da aula, diretiva de
  pré-processador, separador `/` da migalha, fio inerte do mapa em hover. É o
  único degrau que a projeção promove: `html.proj` resolve `--fantasma` para
  `--apagado` (`tokens.css:95`).

### Impressão de uma página do site
`@media print` em `pagina.css:892-901` remapeia a paleta inteira - dezenove
tokens, os catorze sólidos acima mais as cinco lavagens. Não é decoração: antes
o bloco fazia meia inversão (`body { background: #fff; color: #000 }` e mais
nada), os painéis continuavam a `{colors.painel}`, e no papel o âmbar dava 2,0:1
e a moldura 1,6:1. Imprimir uma aula saía pior do que não ter regra de impressão
nenhuma, porque o defeito é invisível na tela de quem escreveu. Todas as cores
de texto do remapeamento passam de 4,5:1 sobre a superfície em que assentam;
`{colors.fantasma-papel}`, que continua sendo andaime, mede 4,6:1 sobre
`{colors.painel-alto-papel}`. Como toda medida e toda cor derivam dos tokens, a
inversão completa é o remapeamento deles e nada mais.

### Named Rules
**A Regra da Prosa Sem Âmbar.** O âmbar nunca carrega texto corrido. Se um
parágrafo ficou âmbar, o erro é de papel semântico, não de tom.

**A Regra do Portador Duplo.** Nenhum estado é comunicado por cor sozinha.
`--ok` e `--falha` marcam exclusivamente *compila × quebrado de propósito*, e
sempre com glifo geométrico e rótulo textual ao lado. Na aula corrente da
árvore são três portadores: glifo grosso, lavagem de fundo e cor.

**A Regra do Andaime.** `{colors.fantasma}` é andaime, não texto. Se um trecho
em fantasma carrega informação que alguém precisa ler, ele é `{colors.apagado}`.
Cinco lugares violavam isso e nenhum viola hoje: o comentário de código, que é
prosa do programador, o rótulo da ficha, o número de seção do sumário, o medidor
da unidade e a nota do cartão da capa.

**A Regra do Raster.** O âmbar impresso foi medido no pixel, e não na
declaração: `#A0630F` declarava 4,9:1 e media 3,5:1 no raster a 8 pt. Ninguém o
clareia sem refazer a medição no raster.

## Typography

**Display Font:** IBM Plex Serif (com Georgia, Times New Roman)
**Body Font:** IBM Plex Serif (com Georgia, Times New Roman)
**Label/Mono Font:** IBM Plex Mono (com ui-monospace, SFMono-Regular)
**Legenda:** IBM Plex Sans (com system-ui, -apple-system)
**Suplemento:** Deriva Geometricos, subconjunto do Noto Sans Mono (SIL OFL 1.1)
de avanço 600/1000, o mesmo do Plex Mono

**Character:** três famílias, três papéis semânticos, e nenhum papel a mais.
Serif é a voz humana e é o único portador de título e de prosa; Mono é a voz da
máquina, e é a face de todo rótulo, carimbo, moldura, navegação, estado interno
e código; Sans é legenda de interativo e de figura, e só isso. As fontes são
auto-hospedadas em `poo/assets/fontes/`: nada de CDN e nada de `@import`, que
bloqueia o render e depende de rede.

### Hierarchy
- **Capa** (600, `{typography.capa.fontSize}`, 1.05, `-0.03em`): título da porta
  de entrada, em Serif romano, `max-width: 22ch` com `text-wrap: balance`.
- **H1 / aula** (600, `{typography.h1.fontSize}`, 1.2): título da aula,
  `max-width: 30ch` e `text-wrap: balance`; cai para 26 px abaixo de 860 px.
- **H2 / seção** (600, `{typography.h2.fontSize}`, 1.25, `max-width: 34ch`):
  seção do slide, prefixada pelo número em Mono âmbar de 11 px com `0.14em`.
- **Prosa** (400, `{typography.prosa.fontSize}`, 1.68, medida
  `{spacing.medida}`, `text-wrap: pretty`): o corpo.
- **Código** (400, `{typography.codigo.fontSize}`, 1.55, `tab-size: 4`): a
  prancha, sempre em `white-space: pre`.
- **Estado** (400, `{typography.estado.fontSize}`): árvore, corpo de tabela,
  botão, painel de estado interno, diagrama de classes, abertura POST.
- **Rótulo** (600, `{typography.rotulo.fontSize}`, caixa-alta): título de
  moldura (`0.16em`, e `0.18em` na caixa tipada), cabeça de tabela (`0.1em`),
  migalha (`0.14em`), rótulo de unidade (`0.16em`), ficha e carimbo. O piso é
  `max(11px, …)`: rótulo é o único degrau que não encolhe abaixo de 11 px.
- **Legenda** (400, `{typography.legenda.fontSize}`, Sans, `max-width: 76ch`):
  a legenda do interativo, do herói e do cartão de destino.

### Named Rules
**A Regra dos Três Papéis.** Mono é código, moldura, rótulo, estado interno e
navegação; Serif é prosa e todo título; Sans é legenda. Uma quarta família é
defeito, e foi por isso que o suplemento geométrico teve de ser renomeado para
`Deriva Geometricos`: o nome interno herdado, "Noto Sans Mono", fazia uma
revisão concluir, com razão, que o livro usava quatro famílias.

**A Regra da Família Herdada na Tabela.** O corpo de tabela não declara família:
ele herda Serif do `body`, exatamente como o `td` do livro
(`livro.css:286-314`). Declarar `--rotulo` ali punha o corpo de 37 tabelas numa
família que a regra dos três papéis não lhe dá, e fazia site e livro
discordarem na mesma tabela.

**A Regra da Régua de Entrada.** No impresso, nenhuma família recebe
`Ligatures=TeX`, e todas recebem `Mapping=` vazio. Não é feature OpenType: é o
mapa de entrada `tex-text` do XeTeX, que converte `--` em meia-risca.
`cmake --build` compôs `cmake –build` em 13 lugares. <!-- voz:permitido -->

**A Regra do Caractere Literal.** Glifo se escreve como caractere, nunca como
`\char"NNNN`: `\char"00A7#1` fez o TeX ler o dígito seguinte como hexadecimal, e
`§5.4` saiu como retângulo vazio seguido de `.4`.

**A Regra da Face Por Tabela.** O roteamento de glifo é uma tabela de caractere
para face, e não uma classe de caracteres. Padrão de Lua trabalha em bytes, e
`[▲◇]` casa com os bytes de `ó`; a primeira versão embrulhou letra acentuada no
suplemento em 1111 lugares.

## Layout

**A escala.** Nove degraus de espaço, todos `calc(… * var(--s))`: 2 / 4 / 6 /
12 / 18 / 28 / 40 px em `tokens.css:71-77`, mais 56 e 84 px que existem só como
literais de reserva nas chamadas de `livro.css`. Os dois degraus mais baixos,
`--e00` e `--e0`, entraram porque faltavam: dezessete lugares usavam 1, 2, 3, 4,
5 e 7 px literais para ajuste óptico dentro de componentes - recuo de badge,
nudge de linha de base, vão entre células de byte -, e literal não escala. Em
projeção (`--s: 1.45`) tudo em volta crescia 45% e esses ficavam parados, de
modo que o ajuste óptico virava desalinhamento justamente na tela grande.

**A grade da página de aula.** A casca é `grid-template-columns: var(--arvore)
minmax(0, 1fr)`: 300 px de árvore das 26 aulas mais o corpo. Acima de 1360 px
(`pagina.css:751`), `.cabeca-aula` e `.slide` viram a grade de três colunas do
caderno de bordo:

```
[prosa] minmax(0, var(--medida))  [goteira] var(--goteira)  [campo] var(--campo) [campo-fim]
```

com `--goteira: 32px` e `--campo: 230px`. A linha de fim tem nome próprio:
nomear `[campo]` cria a linha `campo`, não a `campo-fim`, e sem `campo-fim`
toda regra que dizia atravessar cai numa coluna só. O bloco inteiro é centrado
na largura que sobra da árvore (`max-width: calc(var(--medida) + var(--goteira)
* 3 + var(--campo))`), porque encostado à esquerda com 600 px de vazio à direita
o desequilíbrio lia como erro.

A escolha de coluna é **por omissão larga**, e isso é o inverso do usual. Todo
filho direto atravessa `prosa / campo-fim`, e só os elementos de prosa - `h1`,
`.slide__cab`, `p`, `ul`, `ol`, `.callout`, `.exercicio`, `blockquote`, `h3`,
`h4` - ficam em `prosa` (`pagina.css:773-777`). A razão é de manutenção: onze
construtores de página usam `.corpo`, cada um com blocos próprios, e listar
quem atravessa deixaria de fora o que ninguém previu - o bloco esquecido ficaria
262 px mais estreito, numa regressão silenciosa. Assim ninguém estreita: só a
prosa fica limitada, e ela já tinha `max-width: var(--medida)`.

**As faixas.** Abaixo de 1360 px a grade some e tudo volta ao fluxo: o carimbo
desce para a coluna da prosa com fio à esquerda, e a ficha vira uma linha que
embrulha. Em 1100 px a árvore vira gaveta - havia um degrau intermediário de
`--arvore: 240px`, e em 240 px cabem 21 caracteres enquanto
`contador_de_instancias<T>` tem 25 sozinho, de modo que metade das 26 entradas
embrulhava em três linhas. Em 860 px a goteira cai para 16 px, o badge UFPB e a
tecla de projeção saem da barra, e os controles do interativo empilham. Na capa
as fronteiras são 1040 px (unidades e destinos) e 860 px.

**Projeção.** `html.proj` multiplica `--s` por 1,45, a régua de 1 px vira 2 px,
a goteira vai a 44 px e o texto terciário sobe um degrau, porque projetor come
as faixas baixas. Liga-se pela tecla `F` ou por `?projecao` no URL
(`app.js:245`), e o URL importa por dois motivos: o docente abre projetado sem
tocar no teclado, e a projeção passa a ser capturável sem navegador interativo.

**O impresso.** A4 `oneside` com `includemp` no `geometry`, que não é opcional:
sem ele o `textwidth` pedido é recalculado e o campo de aferição vai para 199 mm
da borda de um papel de 210 mm, fora da folha e sem aviso. A soma que fecha é
20 + 134 + 5 + 35 + 16 = 210 mm, com 22 de topo, 25 de pé, 7 de `headsep` e 14
de `footskip`. A largura larga é 174 mm.

### Named Rules
**A Regra da Coluna Larga Por Omissão.** Na grade de três colunas, atravessar é
o padrão e ficar na prosa é a exceção nomeada. Bloco novo nasce largo; quem quer
medida de leitura pede.

**A Regra do Código Que Não Reflui.** Prancha e tabela densa atravessam prosa
mais campo e nunca refluem: na tela rolam dentro de si, no papel encolhem de
corpo. Código em linha pode quebrar (`overflow-wrap: anywhere`); bloco de código
nunca. São coisas diferentes.

**A Regra da Goteira Solidária.** Goteira e campo vão a zero juntos. Com goteira
em 28 px e campo em 0, quem atravessava ficava 28 px mais largo e as molduras
terminavam dois glifos desalinhadas.

**A Regra do Piso Que Escala.** Toda largura mínima é relativa a `--s`: a tabela
usa `min-width: min(100%, calc(42rem * var(--s)))`, porque `42rem` é relativo à
raiz e ficaria parado em 672 px enquanto o conteúdo cresce 45% em projeção.

## Elevation & Depth

Não há sombra declarada em nenhuma folha de estilo dos dois artefatos, e não é
omissão: o mundo é um terminal, e terminal não projeta sombra. A profundidade
vem de duas fontes. A primeira é tonal, com dois degraus de superfície acima do
vazio - `{colors.painel}` para caixa e `{colors.painel-alto}` para prancha e
painel de sistema - e nenhum terceiro. A segunda é a régua: `{colors.grade}`
para fio fraco, `{colors.grade-alta}` para régua de moldura, carimbo e painel de
sistema.

O único efeito de estado é o anel de foco: contorno de 2 px em
`{colors.fosforo}` com deslocamento de 2 px. A seleção é fósforo sólido com
texto em `{colors.vazio}`, o cursor de texto é âmbar (`caret-color`) porque o
cursor padrão do navegador é preto sobre preto neste fundo e desaparece, e a
barra de rolagem é fina em `{colors.grade-alta}` sobre `{colors.vazio}`, com
polegar em `{colors.fantasma}` no hover. Essas superfícies do navegador só
existiam na folha do livro; a folha das 38 páginas passou a tematizá-las porque
todo bloco de código tem `overflow-x: auto` e a árvore tem `overflow-y: auto`,
e ali o cinza padrão aparecia (`pagina.css:25-38`).

O movimento é curto e nenhum conteúdo depende dele: transições de 120 a 200 ms
em cor e contorno, `max-height` de 420 ms no log da abertura, e o cursor que
pisca. `prefers-reduced-motion` desliga tudo com `!important`.

### Named Rules
**A Regra Sem Sombra.** Nenhuma superfície recebe `box-shadow`. Se algo precisa
se destacar, ele ganha moldura de caractere, um degrau de painel ou `outline`.
O anel de seleção do diagrama de classes é `outline: 2px solid` com
`outline-offset: -1px` justamente por isso: `box-shadow: 0 0 0 2px` é border
disfarçada, e `outline` diz o que é (`pagina.css:626`).

**A Regra do Caractere No Lugar do Efeito.** Quando um efeito de CSS está
imitando um caractere que o alfabeto já tem, o caractere ganha. O marcador de
página corrente na árvore era `box-shadow: inset 2px 0 0`, uma barra âmbar de
2 px; hoje o gerador troca o galho fino pelo grosso - `┣` (U+2523) e `┗`
(U+2517), conferidos presentes nos 128 glifos de box-drawing do Plex Mono - e o
CSS só o acende (`build_site.py:144-155`).

## Shapes

Zero raio de canto em toda a folha: não existe uma declaração de `border-radius`
no build. A forma é retangular, e o canto é um caractere.

A moldura é box-drawing de verdade. Na tela é um flex com `┌─`, o título
embutido, uma corrida de `─` escrita no HTML e `─┐`, com a régua em
`flex: 1 1 0` e `min-width: 0` sob `overflow: hidden`, e sem JS, para o arquivo
servir salvo e offline. O título é `flex: 0 1 auto` com `min-width: 3ch` e
reticência: como `0 0 auto` ele não encolhia em 390 px, empurrava o `─┐` para
fora do `overflow: hidden` do pai e a caixa saía truncada sem o canto. O título
cede antes do canto.

**As laterais são compromisso consciente.** Elas não são `│` empilhado: são
régua de 1 px na mesma cor (`.painel`, `border-inline`, `pagina.css:69`).
Alinhar uma coluna de `│` à altura variável de conteúdo que reflui não
sobrevive ao reflow, e legibilidade vence pureza. O que se ganhou foi moldura
que continua fechada em qualquer largura e em qualquer corpo de fonte; o que se
perdeu é que só topo e base são caractere. No impresso a régua é o mesmo
caractere repetido com `\leaders`, e o PDF tem 33 mil `─`.

Todo o resto de `border` no build é fio, e não moldura: régua de tabela, `hr`,
fio de barra e de pé, contorno de botão, contorno de caixa do palco, e o fio à
esquerda do carimbo em tela estreita.

### Named Rules
**A Regra da Moldura de Caractere.** Moldura é box-drawing; `border` é fio. Uma
moldura desenhada com `border`, ou box-drawing que desalinhe, é o que o
PRODUCT.md nomeia como sinal de resultado errado. A caixa tipada do Deriva
chegou a ter `border` nos quatro lados **além** da moldura, e o resultado era
régua dobrada em cima e embaixo.

## Components

### Moldura
A primitiva do sistema. Régua em `{colors.grade-alta}`, título embutido em
`{colors.fosforo}` com entreletra de rótulo, cantos fixos, `aria-hidden` porque
é desenho e não conteúdo, `user-select: none`, `white-space: nowrap`,
`line-height: 1`. A altura de linha 1 é requisito e não descuido: a moldura de
tela é uma linha de flex, e com mais que 1 os caracteres de box-drawing deixam
de emendar com o painel que vem abaixo.

### Prancha de código
- **Forma:** cabeça em `{colors.painel-alto}` com rótulo à esquerda e
  procedência à direita, corpo em `{colors.painel-alto}` com recuo de 18 px
  (`--e3`) nos quatro lados, pé em `{colors.painel}` com o comando e a contagem.
- **Largura:** atravessa `prosa / campo-fim` na tela e 174 mm no papel.
- **Procedência:** arquivo e linha vão na régua de cima, não em legenda solta
  embaixo: são parte do bloco, e o leitor os lê antes do código.
- **Estado:** `data-estado="ok"` pinta os três fios de `{colors.ok}`,
  `data-estado="falha"` de `{colors.falha}`, sempre com o selo textual ao lado.
- **Realce:** sete classes (`tk-kw`, `tk-tipo`, `tk-str`, `tk-num`, `tk-com`,
  `tk-pre`, `tk-c20`). Comentário é `{colors.apagado}` em itálico e diretiva é
  `{colors.fantasma}`: comentário é prosa do programador e é para ser lido - a
  2,17:1 eram 41 ocorrências ilegíveis só na Aula 02.

### Carimbo de aferição
O componente-tese, e agora nos três artefatos. A tabela saiu de
`render_livro.py` para `comum.tabela_de_carimbos()` (`comum.py:312`), com as
mesmas expressões: o carimbo só dispara quando o parágrafo diz a grandeza **e**
o número, e o número tem de estar na prosa e não dentro de `<code>`.

- **No campo (acima de 1360 px):** `grid-column: campo`, régua de `─` em
  `{colors.grade-alta}` atravessando o campo, valor em âmbar semibold, grandeza
  em `{colors.leitura}`, e "aferido por" em itálico com comando e arquivo em
  Mono sobre `{colors.painel-alto}`.
- **Abaixo:** volta ao fluxo com fio de 1 px à esquerda, medida limitada a
  `--medida`, e o valor e a grandeza na mesma linha separados por ` · `.
- **Onde entra:** só depois de parágrafo de **primeiro nível** do slide, como
  irmão e não como filho. São 3 carimbos no site (aulas 04, 17 e 26), uma
  grandeza por aula. Carimbo dentro de `.callout__corpo` é recusado: ali o
  `aside` é neto da grade e nunca alcança a coluna do campo, e o que se via era
  caixa com fio dentro de painel tingido. As caixas já trazem a própria
  procedência.

### Ficha da aula
Seis pares de rótulo e valor - UNIDADE, AULA, CAPÍTULO, DERIVA, TESTES,
LABORATÓRIO - em Mono de 11 px com `tabular-nums`. Substituiu uma `.sub` de
cerca de 60 caracteres em maiúsculas espaçadas, que era a informação de
referência da página comprimida no formato mais difícil de ler que existe. No
campo (acima de 1360 px) ela é `grid-column: campo; grid-row: 1`, ao lado do
`h1`, empilhada, com rótulo e valor na **mesma linha** (`grid-template-columns:
8.5em 1fr`): empilhados, a ficha ficava mais alta que o `h1` e abria cerca de
100 px de vazio sob o título. Abaixo, é uma linha de flex que embrulha. Os
rótulos são `{colors.apagado}` e não `{colors.fantasma}`: são o único texto que
diz o que os números significam. As outras onze páginas continuam com `.sub`,
porque não têm versão do Deriva nem capítulo para fichar.

### Mapa de seções
Era enfeite morto: o gerador emitia `<i data-vista="0">` para cada seção e nada
em `poo/js/` escrevia `data-vista="1"`. Sete fios cinzas idênticos,
`aria-hidden`, no elemento mais largo da página. Hoje é um `<nav>` com
`aria-label`, um elo por seção com o nome da seção como nome acessível em texto
oculto, e `mapaDeSecoes()` acendendo o corrente por `IntersectionObserver`
(`app.js:200-238`). Fio de 3 px em `{colors.grade}`, `{colors.apagado}` para
seção já vista, e `{colors.fosforo}` a 5 px para a corrente; só a cor
transiciona, porque animar `height` num fio de 3 px anima leiaute em até dez
elementos de uma vez. O alvo clicável é maior que o fio (7 px de recuo vertical,
11 px em ponteiro grosso). O nome da seção corrente vai para a migalha grudada
no topo, que é o que sobra visível na projeção depois que a cabeça rola para
fora. **A cabeça de aula perdeu o `border-bottom` por causa dele**: o mapa é a
régua, e os dois corriam a 27 px um do outro lendo como régua quebrada. Nas onze
páginas sem mapa (`:not(:has(.progresso))`) e na impressão, o fio contínuo
volta.

### Tabela
São 37 tabelas em 27 páginas, e não havia uma linha de CSS para elas em nenhuma
das três folhas de tela: `th` saía serif negrito centralizado do navegador, sem
fio e sem `tabular-nums`. Hoje: corpo em Serif herdado a 13 px com
`tabular-nums`, cabeça em Mono âmbar de 11 px com `0.1em` e fio mais forte
embaixo, fio de `{colors.grade}` sob cada linha e nenhum na última, hover em
`{colors.painel}`, recuo de 6 por 12 px, legenda em Sans embaixo. O piso de
`min(100%, calc(42rem * var(--s)))` faz a tabela **rolar** dentro de `.rolo` em
vez de comprimir: em 900 px a coluna de assinaturas embrulhava `[[nodiscard]]`
fora da assinatura.

### Caixa tipada
Cinco no vocabulário, com glifo e rótulo vindos da tabela canônica: `▲ ATENÇÃO`,
`✓ DICA`, `◇ LLM`, `· NOTA`, `▸ DERIVA`. Laterais em régua de 1 px na cor do
tipo, fundo na lavagem do tipo, topo e base sendo a moldura de caractere, e
recuo de 12 por 18 px (`var(--e2) var(--e3)`): o recuo horizontal é maior que o
vertical porque a 12 px nos quatro lados a prosa encostava no fio lateral. A
variante Deriva traz a versão do sistema em selo âmbar sólido.

### Árvore das 26 aulas
Navegação em Mono de 13 px, `position: sticky` sob a barra, com galho de
box-drawing por entrada (`├`, `╰`, e o par grosso `┣`/`┗` na corrente).
`overflow-wrap: anywhere` no elo, mas `white-space: nowrap` no número, no galho
e no marcador de interativo: sem isso `02` saía como `0` numa linha e `2` na
seguinte. Aula visitada ganha `·` em `{colors.ok}` depois do número. Vira gaveta
fixa em `≤1100px` e em projeção.

### Botões e teclas
- **Tecla da barra** (`.tecla`): 30 px de altura, contorno de 1 px em
  `{colors.grade}`, Mono de 11 px, `{colors.apagado}`; hover e
  `aria-pressed="true"` levam contorno e texto a `{colors.fosforo}`. Em ponteiro
  grosso a altura vai a `--tap` (44 px).
- **Botão do palco** (`.bt`): 44 px de altura, fundo `{colors.painel-alto}`,
  contorno `{colors.grade-alta}`, Mono de 13 px. Hover pinta contorno e texto de
  âmbar. `aria-disabled="true"` é opacidade 0,4 e nenhum hover.
- **Primário** (`.bt--primario`): âmbar sólido com texto `{colors.vazio}` em
  600; hover sobe para `{colors.fosforo-alto}`.
- **Cenário** (`.cen`): botão de estado, colorido por `data-t` (`ok`/`falha`) e
  invertido quando `aria-pressed="true"`.

### Capa
- **Abertura POST:** diegética e precede, mas não mora ali. O log recolhe na
  última linha e o botão que servia para saltar passa a reabrir. **Falha
  recolhida**: `max-height: 0` é o padrão e o log só cresce sob
  `[data-rodando="1"]` ou `[data-aberta="1"]`, atributos postos pelo JS. Sem JS,
  com JS bloqueado, ou no intervalo entre o HTML pintar e o script correr, o
  visitante não recebe 290 px de log na porta de entrada - e não há pulo de
  leiaute no carregamento. O teto é numérico nos dois extremos (0 a 21em),
  porque `max-height: auto` não anima. A linha que fica é `▸ sistema pronto`.
- **Unidades:** `repeat(3, minmax(0, 1fr))` fixo, ou uma coluna abaixo de
  1040 px. `auto-fit` decidia a topologia no lugar do conteúdo e em 900 px dava
  2+1, com a Unidade III sozinha na segunda fila lendo como de outra natureza.
  Existem exatamente três unidades, e sempre existirão. O pé do painel
  ("0/8 lidas") mora no fundo, por `flex: 1 1 auto` no corpo.
- **Destinos:** três famílias nomeadas de quatro colunas, e não nove cartões
  iguais num `auto-fit` de `minmax(220px, 1fr)` - que dava 5+4 em 1440 e 6+3 em
  1920, sem nenhuma quebra caindo nas fronteiras reais. O cartão perdeu o
  sobrolho: o rótulo pequeno sobre o nome grande era etiqueta redundante, e o
  destino é o título.
- **O livro** tem faixa própria (`.levar`): ele não cabia num cartão de 220 px,
  e duas ações pedem dois botões, que não entram num `<a>`.

### Interativo
Cinco partes de contrato, em `{colors.painel-alto}` com laterais em
`{colors.grade-alta}`: moldura com título, palco de 190 px mínimos, controles em
`{colors.painel}`, painel de estado interno (o que a execução real não mostra,
com espaço de verdade e não um cantinho) e legenda em Sans com rótulo âmbar. O
passo é sempre do estudante: não há autoplay.

## Do's and Don'ts

### Do:
- **Do** desenhar moldura com caractere de box-drawing, com `flex: 1 1 0` e
  `min-width: 0` na régua e `line-height: 1` na linha, para o canto direito
  sentar na medida e os glifos emendarem com o painel.
- **Do** deixar a coluna larga ser o padrão na grade de três colunas, e nomear
  só quem fica na prosa.
- **Do** derivar toda medida de `--s`, inclusive as de ajuste óptico: 2 px é
  `--e00` e 4 px é `--e0`, nunca literal.
- **Do** remapear a paleta inteira em `@media print`, e conferir que todo texto
  passa de 4,5:1 sobre a superfície em que assenta.
- **Do** usar `{colors.fantasma}` só para andaime, e `{colors.apagado}` para
  todo texto que carrega informação.
- **Do** trocar o efeito de CSS pelo caractere quando o alfabeto já tem o
  caractere, conferindo antes que o glifo existe na face.
- **Do** ancorar o carimbo como irmão de parágrafo de primeiro nível, e uma
  grandeza por página.
- **Do** fazer a tabela rolar em vez de comprimir, com piso que escala com
  `--s`.
- **Do** tematizar as superfícies do navegador - barra de rolagem, `caret-color`,
  seleção, `text-underline-offset` - onde houver `overflow` no desenho.
- **Do** fazer o progressivo falhar do lado seguro: o que o JS abre nasce
  fechado.
- **Do** acompanhar todo estado de cor com glifo e rótulo textual.
- **Do** manter `includemp` no `geometry` e conferir que a soma fecha em 210 mm.
- **Do** escrever glifo como caractere literal e rotear a face por tabela de
  caractere.
- **Do** medir contraste de âmbar impresso no raster, e nunca na declaração.
- **Do** carregar literal de reserva em todo `var()` de `livro.css`.
- **Do** manter os portões, que são parte do sistema de desenho:
  `verifica_voz.py` para a voz do autor e o marcador de andaime;
  `verifica_pdf.py` para o artefato composto; `converter_fontes.py` para a
  cobertura de glifos; e `capturar_livro.py`, que recusa gravar evidência se a
  página não contiver a assinatura do elemento.

### Don't:
- **Don't** desenhar moldura com `border`. `border` é fio de tabela, `hr`,
  régua e contorno de botão.
- **Don't** pôr âmbar na prosa, nem transformá-lo em cor de texto.
- **Don't** usar cor como único portador de significado, nem usar `--ok` e
  `--falha` para nada além de *compila × quebrado de propósito*.
- **Don't** deixar código refluir, na tela ou no papel: ele rola ou encolhe.
- **Don't** acrescentar `box-shadow` nem raio de canto: use `outline`, moldura
  de caractere ou degrau de painel.
- **Don't** pôr sobrolho em cartão. Se o rótulo pequeno acima do nome repete o
  nome, ele é etiqueta redundante e o destino é o título.
- **Don't** deixar `auto-fit` decidir a topologia quando a contagem é conhecida
  e semântica: três unidades são três colunas.
- **Don't** pôr carimbo dentro de caixa tipada: ele é neto da grade e nunca
  alcança o campo.
- **Don't** deixar meia inversão em `@media print`. Ou remapeia todos os tokens,
  ou o defeito fica invisível para quem escreveu.
- **Don't** acrescentar uma quarta família de fonte, nem declarar família no
  corpo da tabela.
- **Don't** usar emoji. O idioma é box-drawing e forma geométrica.
- **Don't** escrever travessão `—` nem meia-risca `–` em nenhum registro; hífen <!-- voz:permitido -->
  espaçado no lugar. <!-- voz:permitido -->
- **Don't** usar modo matemático no impresso: as duas expressões que existiam
  puxavam três faces do Computer Modern para dentro do PDF só para imprimir "2"
  e "n".
- **Don't** carimbar a falta de um valor com pontuação: com aula sem versão, a
  régua terminava em "aula 01 ·" com o ponto médio pendurado.

### Decisões que contrariam a ferramenta, e constam como tais
- O detector de desenho acusa 137 ocorrências de `wide-tracking:
  letter-spacing 0.12em on body text`, todas em `.moldura__titulo`. É rótulo em
  Mono caixa-alta dentro de moldura `aria-hidden`, e o PRODUCT.md declara que
  rótulo é exatamente isso; `.10em` foi testado e o achado permanece. Mantido,
  com a razão escrita no CSS.
- `line-height: 1` na moldura foi registrado como recusado numa passada
  anterior ("1,35 não muda o desenho … Aceito"), e o build **manteve o 1**
  (`pagina.css:75`). O registro estava contra o build, e quem tem razão é o
  build: a moldura de tela é uma linha de flex, e com mais que 1 os caracteres
  de box-drawing deixam de emendar com o painel. O valor de 1 é regra do
  sistema, não achado pendente.
- As laterais das molduras são régua de 1 px, e não `│` empilhado. É
  compromisso: perdeu-se a pureza do alfabeto nas verticais, ganhou-se moldura
  que continua fechada em qualquer largura, em qualquer corpo e depois de
  qualquer reflow.

### Pendências abertas, declaradas e não escondidas
- Resta **um** `box-shadow` no build, e ele não está em folha de estilo:
  `poo/js/pecas-extra.js:266` emite `style="…;box-shadow:inset 3px 0 0
  var(--falha)"` na linha marcada do revisor de código gerado. É a mesma barra
  de 2 px que saiu da árvore, sobrevivendo num estilo em linha. Não é regra do
  sistema: é dívida, e o caminho é o mesmo - régua de `border-inline` ou o
  caractere.
- O código embutido nos títulos do sumário impresso sai em Serif:
  `\addcontentsline` recebe o título já achatado por `stringify`. Na tela a face
  está correta, e os dois irmãos discordam na mesma tabela de conteúdo.
- O carimbo de aferição do impresso não está ancorado à frase que ele mede:
  `marginnote` ancora no parágrafo, não na palavra.
