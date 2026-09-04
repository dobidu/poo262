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
typography:
  capa:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "clamp(30px, 7.5vw, 56px)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "normal"
  h1:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "34px"
    fontWeight: 600
    lineHeight: 1.22
  h2:
    fontFamily: "IBM Plex Serif, Georgia, Times New Roman, serif"
    fontSize: "23px"
    fontWeight: 600
    lineHeight: 1.22
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
    fontSize: "13px"
    fontWeight: 400
spacing:
  e1: "6px"
  e2: "12px"
  e3: "18px"
  e4: "28px"
  e5: "40px"
  e6: "56px"
  e7: "84px"
  goteira: "28px"
  campo: "230px"
  medida: "68ch"
components:
  moldura:
    textColor: "{colors.grade-alta}"
    typography: "{typography.rotulo}"
    rounded: "0"
    padding: "0"
  moldura-titulo:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
    padding: "0 0.4em"
  prancha:
    backgroundColor: "{colors.painel}"
    textColor: "{colors.leitura}"
    typography: "{typography.codigo}"
    rounded: "0"
    padding: "18px 28px"
  caixa-tipada:
    backgroundColor: "{colors.painel}"
    textColor: "{colors.leitura}"
    typography: "{typography.prosa}"
    rounded: "0"
    padding: "14px 24px"
  carimbo:
    textColor: "{colors.apagado}"
    typography: "{typography.rotulo}"
    padding: "0"
    width: "{spacing.campo}"
  carimbo-valor:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
  tabela-cabeca:
    textColor: "{colors.fosforo}"
    typography: "{typography.rotulo}"
    padding: "6px 12px"
  unidade:
    backgroundColor: "{colors.painel}"
    textColor: "{colors.apagado}"
    typography: "{typography.prosa}"
    padding: "40px 24px"
---

# Design System: Material de POO · UFPB

## Overview

**Creative North Star: "O Caderno de Bordo da Sonda"**

O mundo é o terminal da estação que o estudante constrói: fósforo âmbar sobre
preto de viés esverdeado na tela, e a mesma estrutura traduzida para tinta sobre
papel no impresso. A estética é diegética, e essa é a razão de o box-drawing ser
a única primitiva de moldura: o painel do site é literalmente a interface do
Deriva. O artefato primário é o PDF A4 `oneside` de 296 folhas composto por
XeLaTeX; a folha de tela herda a estrutura dele e troca só o fundo.

A estrutura é o caderno de bordo, e ela tem três faixas: coluna de prosa em
Serif na medida de leitura, campo de aferição de Mono na margem externa onde
cada número afirmado recebe valor, comando e arquivo, e prancha de código
atravessando os dois, porque código não reflui. O campo fica sempre à direita, e
o livro é `oneside` por isso: se o campo trocasse de lado, a prancha deixaria de
caber. A densidade é alta e deliberada; o silêncio é raro e reservado à folha de
abertura de unidade, que é a única página do livro que gasta a largura inteira
sem dizer nada.

Cor nunca é o único portador de significado: todo estado semântico chega com
glifo geométrico e rótulo textual ao lado. Prosa nunca é âmbar. O âmbar é
moldura, rótulo, cursor, carimbo e ênfase de interface, e é a raridade dele que
o faz ler como interface e não como decoração.

**Key Characteristics:**
- Moldura de box-drawing como caractere real, nunca `border`
- Três famílias e três papéis semânticos, mais um suplemento geométrico
- Campo de aferição na margem externa, com procedência conferível
- Prancha de código atravessando texto mais campo, sem refluxo
- Um tema só, escuro na tela e claro no papel; nenhuma inversão de paleta
- Zero raio de canto, zero sombra, zero emoji

## Colors

Uma paleta de fósforo de tubo, quente num preto levemente verde, com quatro
canais semânticos que só se acendem acompanhados de glifo e rótulo. O impresso
recebe a tradução, não a inversão.

### Primary
- **Fósforo Âmbar** (`{colors.fosforo}`): a cor da interface. Moldura em foco,
  título de moldura, `§` de seção, valor do carimbo, cabeça de tabela, link,
  marcador de objetivo, cursor de texto e anel de foco. Nunca prosa.
- **Fósforo Alto** (`{colors.fosforo-alto}`): o degrau aceso do âmbar. Ênfase
  forte (`strong`), palavra-chave do realce de sintaxe, estado de hover.
- **Âmbar de Papel** (`{colors.ambar-impresso}`): o âmbar do impresso, escuro
  porque a 8 pt o traço é fino e a antialiasagem o clareia. Rótulo de moldura,
  carimbo, `§`, tipo e literal no realce, cabeça corrida esquerda.
- **Âmbar Claro de Papel** (`{colors.ambar-claro-impresso}`): só régua de
  moldura e fio de cabelo, que não carregam texto.

### Secondary
- **Frio** (`{colors.frio}`): nome de tipo no realce de sintaxe da tela.
- **Outro** (`{colors.outro}`): marcação de C++20, que no material é sempre
  rotulada como fora do padrão-alvo.

### Tertiary
- **OK** (`{colors.ok}`): exclusivamente *compila*, mais literal e número no
  realce. Sempre com glifo `✓` e rótulo.
- **Falha** (`{colors.falha}`): exclusivamente *quebrado de propósito*. Sempre
  com glifo `▲` e rótulo.
- **Azul UFPB** (`{colors.ufpb}`): só badge institucional e rodapé.

### Neutral
- **Vazio** (`{colors.vazio}`): o fundo da tela, e o único.
- **Painel** (`{colors.painel}`): fundo de prancha, caixa tipada e folha de
  unidade. É o único degrau de superfície que o livro usa.
- **Painel Alto** (`{colors.painel-alto}`) e **Grade** (`{colors.grade}`): fio
  de tabela e régua de separação fraca.
- **Grade Alta** (`{colors.grade-alta}`): régua da moldura em repouso, régua do
  carimbo, régua de `h1` e de pé.
- **Leitura** (`{colors.leitura}`): a prosa, o corpo do código e o valor de
  tabela.
- **Apagado** (`{colors.apagado}`): comentário de código, legenda, tema de
  unidade, corpo do carimbo, cabeça corrida direita.
- **Fantasma** (`{colors.fantasma}`): diretiva de pré-processador e número de
  linha da prancha. É o único degrau que a projeção promove.
- **Tinta** (`{colors.tinta}`) sobre **Papel** (`{colors.papel}`): o par do
  impresso; `{colors.fantasma-impresso}` é o número de linha da prancha no
  papel, clareado porque tinta de 6 pt em cinza-tela desapareceria.

### Named Rules
**A Regra da Prosa Sem Âmbar.** O âmbar nunca carrega texto corrido. Se um
parágrafo ficou âmbar, o erro é de papel semântico, não de tom.

**A Regra do Portador Duplo.** Nenhum estado é comunicado por cor sozinha.
`--ok` e `--falha` marcam exclusivamente *compila × quebrado de propósito*, e
sempre com glifo geométrico e rótulo textual ao lado.

**A Regra do Raster.** O âmbar impresso foi medido no pixel, e não na
declaração: `#A0630F` declarava 4,9:1 e media 3,5:1 no raster a 8 pt. `#7E4A06`
mede 4,74:1 e passa raspando. Ninguém o clareia sem refazer a medição no
raster.

## Typography

**Display Font:** IBM Plex Serif (com Georgia, Times New Roman)
**Body Font:** IBM Plex Serif (com Georgia, Times New Roman)
**Label/Mono Font:** IBM Plex Mono (com ui-monospace, SFMono-Regular)
**Legenda:** IBM Plex Sans (com system-ui, -apple-system)
**Suplemento:** Deriva Geometricos, subconjunto do Noto Sans Mono (SIL OFL 1.1)
de avanço 600/1000, o mesmo do Plex Mono

**Character:** três famílias, três papéis semânticos, e nenhum papel a mais.
Serif é a voz humana e é o único portador de título; Mono é a voz da máquina, e
é a face de todo rótulo, carimbo, moldura e código; Sans é legenda. O suplemento
existe porque `▲ △ ▶ ▷ ▸ ▼ ◀ ◁ ◆ ◇` não existem em nenhuma família do Plex, e
esses glifos são os portadores semânticos que a acessibilidade exige.

### Hierarchy
- **Capa** (600, `{typography.capa.fontSize}` na tela, 31 pt no impresso, 1.05):
  título do livro, em Serif romano. Corpo fluido com `text-wrap: balance`,
  porque em 390 px o `C++` quebrava no meio.
- **H1 / capítulo** (600, `{typography.h1.fontSize}` na tela, `\LARGE` no
  impresso, 1.22): abertura de capítulo, precedida de régua de moldura com o
  rótulo `CAPÍTULO N` e seguida da régua de fecho com aula e versão do Deriva.
- **H2 / seção** (600, `{typography.h2.fontSize}`, 1.22): seção, prefixada pelo
  `§N.N` em Mono âmbar de peso médio.
- **H3 / subseção** (600, 1.12 × prosa): traz o tique `├──` da moldura em Mono
  âmbar antes do texto, para não se confundir com entrada de parágrafo em
  negrito.
- **Prosa** (400, `{typography.prosa.fontSize}`, 1.68, medida
  `{spacing.medida}`, 10,5 pt e `\linespread{1.10}` no impresso): o corpo.
  Parágrafo sem recuo, separado por `0.55\baselineskip`.
- **Código** (400, `{typography.codigo.fontSize}`, 1.55; 8,8 pt no impresso,
  piso 6,9 pt): a prancha. O corpo é calculado por bloco a partir da linha mais
  larga, com teto de 98 colunas em 174 mm; das 147 amostras só duas encolhem.
- **Estado** (400, `{typography.estado.fontSize}`): tabela densa, sumário,
  moldura de capítulo, dados da capa.
- **Rótulo** (600, `{typography.rotulo.fontSize}`, `0.12em`, caixa-alta; 6,4/8
  no carimbo impresso e `\footnotesize` na moldura): título de moldura, cabeça
  de tabela, rubrica de capa, rótulo de sumário.

### Named Rules
**A Regra dos Três Papéis.** Mono é código, moldura, rótulo, estado interno e
navegação; Serif é prosa e todo título; Sans é legenda. Uma quarta família é
defeito, e foi por isso que o suplemento geométrico teve de ser renomeado para
`Deriva Geometricos`: o nome interno herdado, "Noto Sans Mono", fazia uma
revisão concluir, com razão, que o livro usava quatro famílias.

**A Regra da Régua de Entrada.** Nenhuma família recebe `Ligatures=TeX`, e todas
recebem `Mapping=` vazio. Não é feature OpenType: é o mapa de entrada `tex-text`
do XeTeX, que o fontspec aplica por padrão e que converte `--` em meia-risca.
`cmake --build` compôs `cmake –build` em 13 lugares, e `--replay`, `--leiaute` e <!-- voz:permitido -->
`ctest --test-dir` saíram corrompidos. A regra 6.4 da voz do autor proíbe
travessão e meia-risca em qualquer registro; as ligaduras tipográficas de
verdade (`fi`, `fl`) são `liga` e continuam ligadas.

**A Regra do Caractere Literal.** Glifo se escreve como caractere, nunca como
`\char"NNNN`: `\char"00A7#1` fez o TeX ler o dígito seguinte como hexadecimal, e
`§5.4` saiu como retângulo vazio seguido de `.4`.

**A Regra da Face Por Tabela.** O roteamento de glifo é uma tabela de caractere
para face, e não uma classe de caracteres: `▲△▶▷▸▼◀◁◆◇` saem no suplemento, `─`
sai no Mono, `✓` e `·` saem no Mono e não no suplemento. Padrão de Lua trabalha
em bytes, e `[▲◇]` casa com os bytes de `ó`; a primeira versão embrulhou letra
acentuada no suplemento em 1111 lugares.

## Layout

A grade da tela é `1fr · [prosa] minmax(0, 68ch) · [goteira] 28px · [campo]
230px · [campo-fim] 1fr`, e a linha de fim do campo tem nome próprio: nomear
`[campo]` cria a linha `campo`, não a `campo-fim`, e sem `campo-fim` toda regra
que dizia atravessar caía numa coluna só. Prosa fica em `prosa`; prancha,
tabela, caixa de objetivos, moldura, `h1`, `hr`, sumário, capa, pé e moldura de
capítulo atravessam `prosa / campo-fim`.

O impresso é A4 `oneside` com `includemp` no `geometry`, e `includemp` não é
opcional: sem ele o `textwidth` pedido é recalculado e o campo de aferição vai
para 199 mm da borda de um papel de 210 mm, fora da folha e sem aviso. A soma
que fecha é 20 + 134 + 5 + 35 + 16 = 210 mm, com 22 mm de topo, 25 de pé, 7 de
`headsep` e 14 de `footskip`. A largura larga é `textwidth + marginparsep +
marginparwidth` = 174 mm, e é ela que prancha, tabela, moldura de capítulo,
sumário e régua de cabeça reclamam.

O ritmo é a escala de sete degraus 6 / 12 / 18 / 28 / 40 / 56 / 84 px. Registre
como está no build: `--e1` a `--e5` vivem em `tokens.css`, e `--e6` e `--e7`
existem apenas como literais de reserva (56 px e 84 px) nas chamadas de
`livro.css`; `--e4` é chamado com reserva 24 px contra os 28 px do token, então
a folha cai para 28 px quando `tokens.css` carrega e para 24 px quando não. Todo
`var()` de `livro.css` carrega literal de reserva de propósito: sem ele a folha
degrada para prosa clara sobre fundo claro.

Em telas até 68 rem o campo de aferição desce para o fluxo: goteira e campo vão
a zero juntos (com goteira em 28 px e campo em 0, quem atravessava ficava 28 px
mais largo e as molduras terminavam dois glifos desalinhadas), todo elemento
volta para `prosa`, o carimbo ganha fio à esquerda e o sumário cai para uma
coluna. A projeção em sala é escala e não modo: `html.proj` multiplica `--s` por
1,45, a régua de 1 px vira 2 px e o texto terciário sobe um degrau, porque
projetor come as faixas baixas.

### Named Rules
**A Regra do Código Que Não Reflui.** Prancha e tabela densa atravessam texto
mais campo (174 mm de 210) e nunca refluem: na tela rolam dentro de si, no papel
encolhem de corpo. A prosa fica na medida, em torno de 66 caracteres.

**A Regra da Altura Reservada.** A prancha reserva a própria altura antes de
começar, calculada do número de linhas com teto de 46. Sem isso ela partia na
quebra e a continuação chegava sem régua de cima, sem procedência e sem legenda;
o teto existe porque reservar mais do que cabe empurraria folha em branco.

## Elevation & Depth

Não há sombra em nenhum dos dois artefatos, e não é omissão: o mundo é um
terminal, e terminal não projeta sombra. A profundidade vem de duas fontes. A
primeira é tonal: `{colors.vazio}` para o fundo, `{colors.painel}` para tudo o
que é caixa, e um degrau só, porque um segundo degrau leria como painel de
sistema e o livro não tem painel de sistema. A segunda é a régua: `{colors.grade}`
para fio fraco, `{colors.grade-alta}` para régua de moldura, carimbo e `h1`. No
impresso a mesma hierarquia sai em `{colors.ambar-claro-impresso}` para régua e
`{colors.apagado-impresso}` para legenda.

O único efeito de estado é o anel de foco: contorno de 2 px em
`{colors.fosforo}` com deslocamento de 2 px, mais `caret-color` âmbar, porque o
cursor padrão do navegador é preto sobre preto neste fundo e desaparece. As
superfícies do navegador são parte do desenho: seleção em lavagem de âmbar,
barra de rolagem fina em `{colors.grade-alta}` sobre `{colors.vazio}`.

### Named Rules
**A Regra Sem Sombra.** Nenhuma superfície recebe `box-shadow`. Se algo precisa
se destacar, ele ganha moldura de caractere ou um degrau de painel, não sombra.

## Shapes

Zero raio de canto em toda a folha: nenhuma declaração de `border-radius`
existe. A forma é retangular, e o canto é um caractere.

A moldura é caractere de box-drawing de verdade, não `border`. Na tela é um flex
com `┌─`, o título embutido, uma corrida de 200 `─` escrita no HTML e `─┐`, com
a régua em `flex: 1 1 0` e `min-width: 0` sob `overflow: hidden`, e sem JS, para
o arquivo servir salvo e offline. A base `auto` era o defeito: o item partia dos
1300 px do conteúdo, e quem decidia a borda direita era onde o corte caía, com
molduras terminando em 362 e 373 px na mesma folha. No impresso a régua é o
mesmo caractere repetido com `\leaders`, e o PDF tem 33 mil `─`. Topo e base só,
sem os verticais: um `│` por linha não sobrevive a parágrafo que reflui.

Restam 20 usos de `border` em `livro.css`, e todos são fio e não moldura: fio de
tabela, `hr`, régua de `h1`, de sumário, de pé, de blockquote, fio à esquerda do
carimbo em tela estreita, e a nota de impressão. É onde o impresso usa `\hline`
e régua de cabeça.

### Named Rules
**A Regra da Moldura de Caractere.** Moldura é box-drawing; `border` é fio. Uma
moldura desenhada com `border`, ou box-drawing que desalinhe, é o que o
PRODUCT.md nomeia como sinal de resultado errado.

## Components

### Moldura
A primitiva do sistema. Régua em `{colors.grade-alta}`, título embutido em
`{colors.fosforo}` com entreletra de rótulo, cantos fixos, `aria-hidden` porque
é desenho e não conteúdo, `user-select: none`, `white-space: nowrap`. Quando
precede uma caixa tipada, a régua herda 45% da cor do tipo misturada com
`{colors.grade}`, e o título carrega glifo e rótulo. Sem raio, sem sombra, sem
preenchimento.

### Prancha de código
- **Forma:** moldura de caractere em cima com o rótulo à esquerda e a
  procedência à direita, corpo em `{colors.painel}`, moldura de fecho embaixo.
- **Largura:** atravessa `prosa / campo-fim` na tela e 174 mm no papel.
- **Procedência:** arquivo e linha vão embutidos na régua de cima, não em
  legenda solta embaixo: são parte do bloco, e o leitor os lê antes do código.
  Quando o rótulo e a nota passam de 112 caracteres, o corpo da régua encolhe
  em vez de transbordar (piso 6,2 pt).
- **Numeração:** começa no número que a régua declara, e não em 1, num recuo de
  3,2 em fora da medida do código. É o que torna a procedência conferível, e é
  a tese do livro.
- **Variante quebrada:** o rótulo ganha o glifo `▲` e a nota ganha "quebrado de
  propósito".
- **Realce:** sete classes na tela (`tk-kw`, `tk-tipo`, `tk-com`, `tk-str`,
  `tk-num`, `tk-pre`, `tk-c20`) e sete macros no papel, com os mesmos papéis.

### Carimbo de aferição
O componente-tese. Vive no campo de 230 px na tela e no `marginparwidth` de
35 mm no papel. Régua de âmbar claro atravessando o campo inteiro em cima -
nunca `┌───` sem fecho, que numa folha sem outro carimbo lia como erro -, depois
o valor em âmbar semibold, a grandeza em cor de leitura, e em itálico "aferido
por", o comando e o arquivo. São 21 carimbos em 296 folhas.

### Caixa tipada
Cinco no vocabulário, com glifo e rótulo vindos da tabela canônica: `▲ ATENÇÃO`,
`✓ DICA`, `◇ LLM`, `· NOTA`, `▸ DERIVA`. Fundo `{colors.painel}`, recuo de
14 px por 24 px declarado como atalho e não como longhand lógico, sem `border`:
a moldura de caractere antes e depois é a moldura. Rótulos são literais em
caixa-alta, não `string.upper`: o `upper` do Lua trabalha em bytes e produzia
"ATENçãO" nas 28 caixas de aviso.

### Folha de abertura de unidade
A única página do livro que gasta a largura inteira em silêncio. Moldura com o
rótulo `UNIDADE N`, título em Serif SemiBold romano a 27/31 pt, tema em itálico
`{colors.apagado}` numa medida de 62 caracteres, régua de fecho. Romano e não
itálico: com o ambiente inteiro em itálico, o nível mais alto da estrutura era o
único título em itálico do livro.

### Tabela densa
Só fio horizontal. Cabeça em Mono âmbar caixa-baixa de 11 px com `0.05em`,
valores em 13 px com `font-variant-numeric: tabular-nums` para a coluna alinhar,
fio de `{colors.grade}` embaixo de cada linha e nenhum na última. Atravessa
prosa e campo; na tela rola dentro de si. No papel a `longtable` é ancorada à
esquerda (`\LTleft` 0, `\LTright` `\fill`), porque o padrão centralizado somava
`2·\tabcolsep` por fronteira e fazia 16 blocos vazarem dos dois lados.

### Sumário
Dois níveis com pesos distintos, porque com 200 entradas iguais ele era uma
parede: capítulo em âmbar sobre régua de `{colors.grade}`, seção recuada em
`{colors.leitura}` a 11 px em colunas de `26ch auto`, com quebra dentro da
palavra proibida (`columns: 2` fixo partia `C++` em "C+ / +"). Número de seção em
`{colors.apagado}`, e não em `{colors.fantasma}`, que dava 2,2:1.

### Cabeça corrida (impresso)
Versão do Deriva sob inspeção à esquerda em Mono âmbar, capítulo à direita em
Mono apagado, número de folha no pé à direita, e a régua de cabeça é uma corrida
de `─` de 174 mm em âmbar claro, não um `\headrule`.

## Do's and Don'ts

### Do:
- **Do** desenhar moldura com caractere de box-drawing: `┌─`, título embutido na
  régua de cima, `─┐`, e a régua sendo uma corrida de `─` de verdade.
- **Do** dar `flex: 1 1 0` com `min-width: 0` à régua da moldura, para o canto
  direito sentar na medida em vez de onde o corte cair.
- **Do** manter `includemp` no `geometry` e conferir que a soma fecha em 210 mm.
- **Do** declarar `Mapping=` vazio em toda família de fonte, e nenhuma com
  `Ligatures=TeX`.
- **Do** escrever glifo como caractere literal, e rotear a face por tabela de
  caractere.
- **Do** usar `\textcolor` e nunca `\color` no início de macro: `\color` no
  começo de célula `p{}` empurrou o conteúdo para a segunda linha e desalinhou
  uma fileira inteira em 9,1 pt.
- **Do** reservar a altura da prancha a partir do número de linhas, com teto de
  46.
- **Do** numerar a linha da prancha a partir do número que a régua declara.
- **Do** medir contraste de âmbar impresso no raster, e nunca na declaração.
- **Do** acompanhar todo estado de cor com glifo e rótulo textual.
- **Do** carregar literal de reserva em todo `var()` de `livro.css`.
- **Do** rodar duas passadas no filtro do pandoc: numa só, os inlines são
  percorridos antes dos blocos, e `Code` já havia virado `RawInline` quando
  `Header` chamava `stringify`.
- **Do** manter os portões, que são parte do sistema de desenho:
  `verifica_voz.py` para a voz do autor, o marcador de andaime, a tabela
  multilinha e a régua órfã; `verifica_pdf.py` para o artefato composto (risca,
  aspa de TeX, glifo ausente contando U+FFFF, tinta fora do papel entre 159 e
  194 mm, carimbo sobre carimbo, teto de 8 transbordos);
  `converter_fontes.py` para a cobertura dos 30 glifos exigidos; e
  `capturar_livro.py`, que recusa gravar evidência se a página não contiver a
  assinatura do elemento.
- **Do** desfazer a ligadura de aspa no pós-passe: o escritor LaTeX do pandoc
  reconverte `“` e `”` para as aspas de TeX, e como nem elas nem a risca são
  querida, toda ocorrência no `.tex` veio da escrita e desfazê-la é
  determinístico. A linha de código é poupada, porque pode conter dois
  apóstrofos de verdade.

### Don't:
- **Don't** desenhar moldura com `border`. `border` é fio de tabela, `hr` e
  régua; são 20 usos em `livro.css` e nenhum é moldura.
- **Don't** pôr âmbar na prosa, nem transformá-lo em cor de texto.
- **Don't** usar cor como único portador de significado, nem usar `--ok` e
  `--falha` para nada além de *compila × quebrado de propósito*.
- **Don't** deixar código refluir, na tela ou no papel: ele rola ou encolhe.
- **Don't** clarear `{colors.ambar-impresso}` sem refazer a medição no raster.
- **Don't** acrescentar uma quarta família de fonte, nem deixar um suplemento
  com nome interno de outra família.
- **Don't** usar emoji. O idioma é box-drawing e forma geométrica.
- **Don't** escrever travessão `—` nem meia-risca `–` em nenhum registro; hífen <!-- voz:permitido -->
  espaçado no lugar. <!-- voz:permitido -->
- **Don't** acrescentar `box-shadow` nem raio de canto: não há um de cada em
  todo o build.
- **Don't** inverter a paleta em `@media print` na versão de tela. O artefato de
  impressão é o PDF; a folha de tela apenas diz onde ele está.
- **Don't** usar modo matemático no impresso: as duas expressões que existiam
  puxavam três faces do Computer Modern para dentro do PDF só para imprimir "2"
  e "n". Expressão vira trecho de código na prosa.
- **Don't** carimbar a falta de um valor com pontuação: com aula sem versão, a
  régua terminava em "aula 01 ·" com o ponto médio pendurado.

### Duas decisões que contrariam a ferramenta, e constam como tais
- O detector de desenho acusa 137 ocorrências de `wide-tracking: letter-spacing
  0.12em on body text`, todas em `.moldura__titulo`. É rótulo em Mono caixa-alta
  dentro de moldura `aria-hidden`, e o PRODUCT.md declara que rótulo é
  exatamente isso; `.10em` foi testado e o achado permanece. Mantido, com a
  razão escrita no CSS.
- `line-height: 1` na moldura era herança de `pagina.css`, e o detector tinha
  razão: 1,35 não muda o desenho e tirou 239 achados do caminho de um achado
  real. Aceito.

### Duas pendências abertas, declaradas e não escondidas
- O código embutido nos títulos do sumário impresso sai em Serif:
  `\addcontentsline` recebe o título já achatado por `stringify`, e devolver a
  face exige carregar a marcação inline até a linha do sumário. Na tela a face
  está correta, e os dois irmãos discordam na mesma tabela de conteúdo.
- O carimbo de aferição não está ancorado à frase que ele mede: `marginnote`
  ancora no parágrafo, não na palavra. São 21 carimbos em 296 folhas, e a tese
  chega por reincidência e não por vínculo.
