# POO v2 - site e livro da disciplina

Programação Orientada a Objetos em C++17 · UFPB · Centro de Informática ·
Prof. Carlos Eduardo C. F. Batista · semestre-alvo **2026.2**.

Este repositório executa o que está em `PLANO_DE_ENSINO_POO_v2.md`,
`PLANO-MATERIAL-POO-v2.md` e `PLANO-LIVRO-POO-v2.md`: **26 aulas** (não 27),
Aula N = Capítulo N, sistema-base **Deriva**, alvo **C++17**, e oito tipos de
exemplo interativo.

## Uma fonte, dois meios

O motivo de existir deste pipeline é que livro e site divergem quando não há
fonte única - foi o que aconteceu no v1, e é o que a arquitetura abaixo impede.

```
conteudo/mapa.py          A TABELA CANÔNICA: 26 aulas, 3 anexos, 20 versões do
                          Deriva, 12 laboratórios, 8 interativos. Verifica os
                          próprios invariantes; mapa quebrado não gera nada.
conteudo/aulas/*.py       fonte de verdade do conteúdo (prosa, código, callouts,
                          exercícios), extraída do v1 e editável à mão
conteudo/PENDENCIAS.md    o que a migração não resolve sozinha (gerado)

conteudo/trechos.py       quais trechos do Deriva entram em qual aula, por âncora
conteudo/codigo_deriva.py os trechos, recortados (gerado)

build/extrair_v1.py       legado/site-v1 → conteudo/aulas/
build/extrair_livro.py    legado/poo.docx → livro/
build/extrair_codigo.py   exemplos/deriva/ → conteudo/codigo_deriva.py
build/build_site.py       conteudo/ → poo/
build/comum.py            realce de sintaxe próprio + deep link do Compiler Explorer
build/verifica_pecas.js   o contrato dos interativos, testado sem navegador

poo/                      O SITE. css/ e js/ vêm do Claude Design e não são
                          gerados; todo .html é gerado.
livro/                    O LIVRO. capitulos/, anexos/, MIGRACAO.md, poo-v2.docx
exemplos/deriva/          O PROJETO, compilando. v0.0 → v0.3 + 2 variantes quebradas
legado/                   site v1 + poo.docx - SOMENTE LEITURA
```

Número nenhum é digitado na prosa, tampouco: `conteudo/medidas.py` é gerado
medindo o binário, e o portão de números recusa afirmação que o código negue.
Na trilha, o glifo distingue contagem medida de meta - versão que ainda não
existe em código não exibe teste passando.

Nenhum trecho de código do material é digitado no material: `trechos.py`
declara âncoras dentro de `exemplos/deriva/`, e site e livro recebem o mesmo
recorte do mesmo arquivo que compila. Se uma âncora deixar de existir, o build
falha - material apontando para código que já não existe é pior que material
sem código.

`make` roda os portões e gera as duas coisas. Ver o topo do Makefile para os
alvos individuais: `make site`, `make livro`, `make deriva`, `make voz`,
`make sinais`, `make codigo`.

## A voz: uma só, e verificada

A prosa do site e do livro sai com o nome do autor, então ela obedece a um
padrão editorial único, e o padrão vale para prosa de aula, capítulo, callout,
legenda de interativo, introdução de página e este README. Não vale para
código, mensagem de commit nem saída de build.

O registro é **formal**, com o texto se dirigindo ao estudante - documentação,
e não manual técnico impessoal - em português.

`build/verifica_voz.py` é o portão, e ele trabalha em dois níveis: regras
**duras**, verificáveis sem julgamento, quebram o build; **sinais** brandos são
contados e relatados, para quem escreve decidir caso a caso. O princípio é
smell test e não lista negra, e o perfil de voz vence o detector, nunca o
contrário: "através de" e os conectivos formais são voz legítima, não defeito.
`make sinais` lista os brandos.

A primeira coisa que o portão pegou foi grande. A regra tipográfica dura
proíbe o travessão e a meia-risca (U+2014 e U+2013) em todos os registros,
exigindo o hífen espaçado no lugar, e o material gerado os usava em cerca de
**1960 lugares**. `build/normaliza_tipografia.py` consertou o que era autoral
de uma vez; o texto que vem de `legado/` é convertido na extração, porque
`legado/` é somente leitura. Daqui em diante é o portão que impede a
reincidência - e ele já pegou duas voltas por caminhos que ninguém previa: uma
ligadura do XeTeX que convertia `--` em meia-risca na composição, e o escritor
LaTeX do pandoc reintroduzindo aspa de TeX onde o filtro havia posto aspa
curva. Nos dois casos o fonte estava limpo e o artefato não.

Além dos dois níveis, três regras duras nasceram de erro real neste
repositório: **nenhum marcador de andaime** no material publicado (`REVISAR`,
`PENDENTE`, `TODO`, `a definir` - a pendência se resolve, e sinalizá-la
transfere ao leitor um trabalho que é nosso), **nenhum vocabulário do
sistema-base anterior**, e **nenhuma tabela multilinha do pandoc**, cujo limite
de coluna é um deslocamento de caractere e que se desalinha em silêncio quando
a célula muda de largura.

## Os quinze portões

Nenhum deles é decorativo - cada um já pegou um problema real neste repositório:

1. **`conteudo/mapa.py`** confere seus invariantes: 26 aulas contíguas, cada
   interativo declarado nas duas direções, 20 versões obrigatórias na trilha,
   12 laboratórios casando com as aulas, e nenhum capítulo do v1 sem destino.
2. **Cobertura da extração** (`extrair_v1.py`): todo slide de conteúdo do site
   v1 tem de cair em alguma aula ou anexo. Pegou dois slides `llm` que as
   fatias das páginas partidas deixavam de fora.
3. **Contrato dos interativos** (`verifica_pecas.js`): cada peça precisa de um
   cenário que demonstra a falha e um que a evita, `quadro(cenário, passo)`
   puro em todos os passos, painel de estado com ao menos três linhas, legenda
   dizendo onde olhar, e zero temporizador - autoplay é rejeição automática.
4. **Links internos** (`build_site.py`) e **seções órfãs**
   (`extrair_livro.py`): link morto e seção do livro sem destino param o build.
5. **`make verifica` do Deriva** (`exemplos/deriva/Makefile`), as quatro
   condições da disciplina: zero aviso com `-Wall -Wextra -Wpedantic
   -Wconversion`, 188 testes verdes, replay idêntico byte a byte, e o contador
   de instâncias vivas fechando em zero. Pegou dois defeitos: validação de
   argumento depois da construção do membro (o `std::vector` lançava
   `length_error` antes de o corpo do construtor rodar) e um
   `-Wsign-conversion` legítimo em `~(ICANON | ECHO)`.
6. **Âncoras de código** (`extrair_codigo.py`): os **156 trechos** publicados
   são recortados do Deriva por âncora de texto; âncora que não existe mais
   para o build. Quatro deles são os **diagramas** em Mermaid, que vivem em
   `exemplos/deriva/diagramas/*.mmd` e chegam ao slide por âncora como
   qualquer código - diagrama digitado no material pode afirmar uma hierarquia
   que o código não tem, e nada o denuncia.
7. **Voz** (`verifica_voz.py`): as regras duras do padrão editorial, em dois
   níveis - duras quebram o build, brandas são relatadas. `make sinais` lista
   as brandas.
8. **Medidas** (`medir_deriva.py`): roda o Deriva compilado e grava
   `conteudo/medidas.py` com os `sizeof`, a contagem de testes do ctest e os
   bytes que o ciclo de `shared_ptr` prende. Todo número que a prosa afirma sai
   daqui.
9. **Números** (`verifica_numeros.py`): confere as afirmações numéricas do
   material contra o que foi medido, e recusa contagem de versão ainda não
   escrita exibida como medição. Nasceu de três erros que a revisão pegou e
   ele não teria deixado passar: `celula.hpp` dizia "15 KB contra 23 KB" onde
   são 23 e 30; o interativo de posse dizia 96 bytes vazados onde são 160; e a
   trilha anunciava 188 testes onde o ctest passava 26.
10. **Glifos** (`verifica_fontes.py`): recusa o build se o site usar caractere
    que nenhuma face declarada cobre. As molduras deste material são
    box-drawing de verdade e os marcadores semânticos são glifos ao lado do
    rótulo, então glifo sem fonte chega com outro avanço dentro de painel
    alinhado por caractere. Pegou dezessete deles no design importado.
11. **O PDF composto** (`verifica_pdf.py`): confere o artefato, e não o fonte,
    porque há classe de defeito que só nasce na composição. Recusa travessão e
    meia-risca, aspa de TeX literal, aspa reta em prosa, glifo ausente, tinta
    fora do papel, carimbo sobre carimbo e transbordo acima do teto. Pegou 35
    retângulos vazios que o fonte não tinha, 42 opções de linha de comando
    corrompidas por uma ligadura do XeTeX (`--replay` saía `–replay`, e o <!-- voz:permitido -->
    comando copiado do livro dava erro no shell) e 82 aspas que o escritor do
    pandoc reintroduzia.
12. **O arquivo do estudante** (`gerar_sem_marcas.py`): o exercício da Aula 04
    entrega código gerado por IA com três defeitos plantados. O cabeçalho
    prometia um `gerado_sem_marcas.hpp` "gerado no build" que não existia, e o
    estudante recebia as marcas `DEFEITO n` e, quarenta linhas abaixo, o
    `namespace revisado` com a correção dos três. Agora ele é gerado, e o
    portão o mantém em dia.
13. **O plano em .docx** (`gerar_plano_docx.py`): a página do plano oferece o
    arquivo para baixar, e ele era feito à mão - ficou 17 horas atrás do
    markdown que representa, e `make limpa` o apagava sem que nada soubesse
    refazê-lo.
14. **A evidência por assinatura** (`capturar_livro.py`): as folhas do PDF que
    servem de prova numa revisão são escolhidas por assinatura no texto
    extraído, e o script **recusa gravar** se a página não contém o elemento
    que o nome promete. Nasceu de uma revisão que parou no portão de evidência
    porque a captura da prancha de código saía de uma folha sem prancha
    nenhuma.
15. **Divergência reprova.** Os três conferidores - `extrair_codigo`,
    `extrair_v1` e `build_site` - imprimiam "DIVERGE" e saíam com sucesso, e
    `make verifica` dizia "portões OK" logo abaixo do relatório de desvio. Um
    portão que relata e não recusa deixa passar exatamente o que ele existe
    para pegar.

## O que está feito e o que não está

**Feito.** O **Deriva completo, v0.0 → v2.7**, em `exemplos/deriva/`: as
classes de valor, a hierarquia de entidades com destrutor virtual, `mundo` com
posse exclusiva e zero `delete`, o grafo da estação com `shared_ptr` e
`weak_ptr`, movimento com `noexcept`, operadores, campo de visão puro por
Bresenham inteiro, o diamante, o inspetor por RTTI, `grade<T>` e
`contador_de_instancias<T>` por CRTP, a hierarquia de erros com as três formas
de recusar, inventário com STL e lambdas, a fila entre threads, serialização
versionada, e a refatoração SOLID com Command, Observer, Factory, Strategy por
lambda e Composite. **188 testes verdes**, e a soma é declarada por arquivo:
**129 da trilha** (cada arquivo de `testes/` declara na primeira linha a que
versão pertence), **47 de material de aula** (o par C contra C++ da Aula 01,
os eixos de tipo da Aula 05, as medidas de leiaute, posse, movimento e
corrida) e **12 dos**
laboratórios, com `make verifica` 4 de 4 e as **quatro** variantes
deliberadamente quebradas escritas.

Os **12 laboratórios preparatórios**, com enunciado, esqueleto que compila e
falha o portão de propósito, e solução de referência - e as doze soluções são
compiladas e executadas pelo `ctest` a cada build, porque solução publicada que
não compila é pior que solução ausente.

As **fontes auto-hospedadas**, e não foi só baixar: o subconjunto
`latin` do Google Fonts, que era o caminho óbvio, **não tem o bloco de
box-drawing**, e as molduras deste material são caracteres reais. Os arquivos
são os `complete` do IBM Plex v6.4.0. Além disso, nenhuma das três famílias
Plex cobre a faixa de formas geométricas, e o material depende de nove glifos
dela como portadores semânticos ao lado da cor - daí
`DerivaGeometricos.ttf`, subconjunto de 5,6 KB do Noto Sans Mono, escolhido por
ter avanço de 600/1000, o mesmo do Plex Mono, e restrito por `unicode-range`.
Três glifos que nenhuma face cobre (`⟲`, `☰`, `⏸`) foram trocados no código por
`↺`, `▸` e `││`. Detalhes e licenças em `poo/assets/fontes/LEIA-ME.md`.

O **Deriva v0.0→v0.3** compilando em `exemplos/deriva/`: `vetor2`,
`celula`, `grade`, `mapa`, `terminal_bruto`, o contador `vivos`, a
instrumentação de ciclo de vida, 188 testes com Catch2 v3.5.2, replay
determinístico, `make verifica` 4 de 4, ASan e UBSan limpos, e as duas
variantes deliberadamente quebradas (`terminal_bruto` sem destrutor; cópia rasa
em `grade` - caça ao bug 1) com o roteiro de observação de cada uma. Os 156
trechos que site e livro publicam saem de lá, com arquivo e linha no rodapé de
cada bloco.

As 38 páginas do site, geradas: 26 aulas, 3 anexos, capa com o herói
de despacho virtual, galeria dos 8 interativos, trilha das 20 versões, os 12
laboratórios, a rubrica de revisão, o portão `make verifica`, o plano de ensino
(com `.docx`), exercícios agregados, glossário e bibliografia. O livro
reestruturado em 26 capítulos + 3 anexos, com o manifesto que prova, seção por
seção, que nada do v1 ficou órfão. Os 9 interativos (8 tipos + a peça de corrida
reaproveitada de LPII), passando o contrato.

**Não está feito, e está registrado item a item** - 96 pendências em
`conteudo/PENDENCIAS.md` e 54 em `livro/MIGRACAO.md`:


- **a prosa e o código ainda no Sintonia** (46 ocorrências). O domínio muda por
  escrita humana, não por substituição de palavra - os 15 callouts já trocaram
  de tipo para `deriva`, o texto dentro deles não;
- **o conteúdo novo do plano v2** (16 itens): o contador `vivos`, a
  instrumentação de ciclo de vida, o `gdb` no destrutor, o replay
  determinístico, `contador_de_instancias<T>`, `std::forward`, `string_view`,
  ligações estruturadas, `[[nodiscard]]`;

- **o Deriva da v1.0 em diante** (16 das 20 versões): a hierarquia
  `entidade` → `sonda`/`drone`/`item`, os ponteiros inteligentes, o movimento,
  o diamante, os templates e o Qt. Estão especificados em `conteudo/mapa.py` e
  publicados na trilha; o código vai até a v0.3. As outras duas variantes
  quebradas (destrutor não virtual, `mundo` como god class) dependem delas;
- **FTXUI**: a integração está escrita e fixa em `v5.0.0`, atrás de
  `-DDERIVA_COM_FTXUI=ON`. O render atual é `std::cout` direto, e basta até a
  v1.x;
- **os 39 blocos de código do v1** que ainda não têm par no Deriva: 22 dos 61
  já foram substituídos por trecho extraído de arquivo que compila;
- **as três divisões de capítulo** conferidas parágrafo por parágrafo. A
  extração colocou cada seção em um capítulo e marcou as que atravessam a
  divisão; separar o texto é decisão de conteúdo;
- **a auditoria da bibliografia** do livro (duas correções já aplicadas no site:
  autoria do Catch2 e edição do Stroustrup de 2024).

## Como construir

O material publicado está versionado, então **ler não exige construir**: o
site abre em `poo/index.html` e o livro em `livro/poo-v2.pdf`. Construir é
para quem vai mudar algo.

```bash
make            # tudo: portões, site, livro em markdown, PDF e versão de tela
make verifica   # só os portões, sem gerar nada
make site       # as 38 páginas
make livro-pdf  # o PDF de impressão e a versão de tela
```

O que `make` precisa ter na máquina:

| ferramenta | para que | se faltar |
|---|---|---|
| `python3` | os geradores e os portões | nada roda |
| `g++` com C++17, `cmake`, `ctest` | o Deriva e as quatro condições do portão | `make verifica` para na condição 1 |
| `pandoc` | o livro em markdown, o `.docx` e o HTML de tela | o livro não monta |
| `xelatex` | o PDF de impressão | `make livro-pdf` para |
| `node` | o contrato dos interativos | o portão 3 não roda |

Três dependências de Python moram num venv do projeto, e não no sistema:
`brotli` para abrir as fontes em WOFF2, `fonttools` para o suplemento de
glifos, e `pymupdf` para o portão do PDF. `make venv` o cria, e `make` o
chama quando precisa.

O FTXUI e o Catch2 vêm por `FetchContent` em tag fixa, e o Qt é opcional
(`-DDERIVA_COM_QT=ON`), desligado por padrão porque o laboratório não o tem.

## Licenças

Três coisas, três licenças, e o mapa completo está em
[`LICENCAS.md`](LICENCAS.md):

- **O texto** - capítulos, páginas, diagramas, enunciados - sob
  [CC BY-SA 4.0](LICENSE-TEXTO). Adaptar exige crédito e manter aberto.
- **O código** - o Deriva, os geradores, os portões, os interativos - sob
  [MIT](LICENSE). Reusar o Deriva noutra disciplina não obriga a abrir nada.
- **As fontes** - subconjuntos do IBM Plex e o suplemento geométrico - sob
  SIL OFL 1.1, redistribuídas com o aviso que a licença delas exige.

O critério, quando a fronteira não for óbvia: se o arquivo é lido por uma
pessoa, é CC BY-SA; se é executado por uma máquina, é MIT.

## Verificado e não verificado

Conferido de fato: aninhamento de tags nas 38 páginas, todo link interno,
contrato das 9 peças em 118 quadros, cobertura de 131 slides e 108 exercícios do
v1, nenhuma seção do livro órfã, e o Deriva compilando com zero aviso, 188 testes
verdes, ASan/UBSan limpos e `gdb` parando no destrutor de `mapa` - o `bt` mostra
a cópia não pedida sendo destruída dentro de `de_texto`. **Não** conferido: contraste em projetor real e
render em navegador - não havia navegador headless utilizável no ambiente.
Projete `aula-11.html` com `F` na sala e ajuste `--fantasma` e `--rule-w` dentro
de `html.proj`, em `css/tokens.css`, se precisar.

## Uma referência fabricada, e o que ela custou

A página de glossário e bibliografia se anuncia com referências auditadas e
listava o FTXUI como **"Coelho, A."**. É invenção: `PLANO_DE_ENSINO_POO_v2.md`
traz *SONZOGNI, A.*, e a própria URL na mesma linha é
`github.com/ArthurSonzogni/FTXUI`. Foi o escriba que pegou, numa passada de
voz, e não um portão - autoria fabricada é o item 6.5 da spec, o epistêmico, e
é o único da lista que nenhuma expressão regular alcança. A bibliografia
inteira do livro segue sem auditoria (`livro/MIGRACAO.md`), e essa é a
pendência que mais merece um par de olhos humanos.

## Decisões que valem revisão do autor

Herdadas dos planos e implementadas com a leitura mais defensável; trocar agora
é barato.

- **A trilha tem 20 versões obrigatórias mais a `v2.1` opcional** rotulada
  C++20. É a única aritmética que fecha os "20 versões (v0.0 → v2.7)" do plano
  com as 26 aulas.
- **A numeração das aulas 12 e 13** (posse exclusiva e compartilhada) usa as
  versões `v1.2` e `v1.3` do Deriva, deslocando as demais em relação à tabela do
  handoff, que era numerada sobre as 27 aulas antigas.
- **`mapa` na v0.3 declara destrutor e cópia**, o que impede o compilador de
  gerar o movimento e faz cada `carregar` custar três construções para um
  objeto. Isso está afirmado em teste, não escondido: é o argumento da regra dos
  cinco, medido na Aula 09 antes de ser explicado na 14. Se preferir a v0.3 já
  com movimento, o teste `test_mapa.cpp` é o lugar de mexer - e o número da
  Aula 09 muda.
- **Azul UFPB** só em badge e rodapé, como o Claude Design decidiu.
- **O nome Deriva** segue como proposta. Está centralizado em
  `conteudo/mapa.py` e nos textos gerados; trocar depois de 26 capítulos
  escritos, não.
