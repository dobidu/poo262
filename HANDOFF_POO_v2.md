# HANDOFF - POO v2 · Programação Orientada a Objetos (UFPB/CI)

Handoff para o Claude Code. Disciplina de POO em C++, Centro de Informática da UFPB.
Autor: Prof. Carlos Eduardo C. F. Batista (`bidu@ci.ufpb.br`).

Objetivo desta fase: atualizar o conteúdo com **foco na sintaxe de C++17**, trocar o
sistema-base pedagógico, e reconstruir o site com estética TUI/retrofuturista e
exemplos interativos.

---

## 1. Ponto de partida - inventário real

**Livro** (`poo.docx`, fonte canônica em DOCX): 27 capítulos + glossário +
referências, ~6.500 linhas em markdown. Estrutura por unidades:

| Unidade | Capítulos | Tema |
|---|---|---|
| I | 1 - 9 | Transição procedural→OO, fundamentos C++, infraestrutura, Git, LLMs, UML, classes, ciclo de vida |
| II | 10 - 18 | RAII, smart pointers, move, operadores, testes, herança, virtuais, polimorfismo |
| III | 19 - 27 | Templates/CRTP, concepts, erros, STL, concorrência, serialização, SOLID, padrões, Qt |

**Site** (`poo-zip.zip`): 27 aulas em 3 unidades, **131 slides**, 108 itens de
exercício, 98 callouts em 5 tipos (`warn` 36, `llm` 27, `tip` 16, `sintonia` 15,
`info` 4), 60 blocos de código. Prism para realce, Mermaid para diagramas.
Paleta Tokyo Night sobre `#0d1117` com azul UFPB `#1a56a0`; Source Serif 4 +
JetBrains Mono + Space Grotesk via Google Fonts. Uma única `@media`.

**Sistema-base atual - Sintonia**: mini-DAW construído em 17 versões (v0.1→v2.5),
uma por aula, com 72 testes e **variantes deliberadamente quebradas**
(`v1.0-broken` sem destrutor virtual, `v2.3-before` sem SOLID). Esse padrão de
variante quebrada é o melhor recurso pedagógico do material atual e **deve ser
preservado** no sistema novo.

**Ponto forte a não perder**: o site v1 de POO é bem construído - tem exercícios,
callouts tipados, realce de sintaxe e diagramas. Está bem à frente do que havia em LPII.
O que falta é interatividade e a atualização de sintaxe.

---

## 2. A lacuna central - o livro não ensina C++17

Auditoria feita por contagem no texto do livro. O livro se declara C++17 (12
menções) mas **as construções de sintaxe que caracterizam C++17 estão ausentes**:

| Construção | Ocorrências | Situação |
|---|---|---|
| `std::string_view` | **0** | ausente - e o Cap. 2 é justamente "de `char[]` a `std::string`" |
| Structured bindings (`auto [a,b] = …`) | **0** | ausente |
| `[[nodiscard]]`, `[[maybe_unused]]` | **0** | ausente |
| `std::tuple` | **0** | ausente |
| `std::forward` / encaminhamento perfeito | **0** | ausente - e o Cap. 12 é sobre semântica de movimento |
| Lambdas | **1** | uma menção em 27 capítulos |
| `if constexpr` | **1** | uma ocorrência, dentro de um exemplo do Sintonia |
| `constexpr` | 4 | subutilizado |
| `std::filesystem` | **0** | ausente |
| CTAD, fold expressions, `inline` variables, `std::byte`, `std::apply`, `std::invoke`, `std::clamp`, namespaces aninhados | **0** | ausentes |
| `std::optional` / `std::variant` | 8 / 9 | **presentes e bem usados** - a exceção positiva |

Enquanto isso, o **Cap. 20 ensina Concepts e Ranges, que são C++20**. O livro
ultrapassa o padrão-alvo num capítulo e não cobre o próprio padrão-alvo nos outros 26.

**Direção obrigatória desta fase.** C++17 é o teto e o foco. As construções acima
entram distribuídas nos capítulos onde são naturais - não num capítulo "features de
C++17" apartado, que é como se ensina uma lista em vez de um hábito:

- `string_view` no Cap. 2, junto com `std::string`, com a armadilha de tempo de vida explícita.
- Structured bindings no Cap. 2 e depois em todo iterador de `map`.
- `[[nodiscard]]` no Cap. 8, em getters e em funções que retornam status.
- `std::forward` e referências universais no Cap. 12, onde faltam.
- Lambdas no Cap. 22 (STL) e no Cap. 26 (Strategy sem herança).
- `if constexpr` no Cap. 19, substituindo SFINAE.
- `std::filesystem` no Cap. 21/24, no carregamento de arquivos.
- `std::clamp`, `std::size`, CTAD onde aparecerem naturalmente.

**Cap. 20 (Concepts/Ranges)** é reposicionado como "para onde a linguagem foi",
explicitamente rotulado C++20, sem virar dependência de nenhum exemplo. Mesmo
tratamento dado ao C++20 na disciplina de LPII.

---

## 3. Sistema-base novo - Deriva

Substitui o Sintonia. O critério pedido foi: conhecido por aluno de início de
graduação, mas não amorfo como sistema bancário ou acadêmico.

**Deriva** é um *roguelike* de terminal por turnos: o aluno opera uma sonda de
inspeção dentro de uma estação orbital abandonada, através do console. Grade,
glifos, campo de visão, entidades, inventário, turnos.

### Por que este, e não os outros

| Candidato | Por que perde |
|---|---|
| Sistema bancário / acadêmico | Exatamente o que foi descartado: amorfo, sem restrição própria, o aluno não sente o domínio |
| VM / assembler didático | Estética perfeita, mas fraco em hierarquia e polimorfismo - que são o núcleo de POO |
| Simulador de ecossistema | Boa cobertura OO, narrativa fina, nada obriga o aluno a se importar |
| Interpretador de linguagem | Excelente para Composite/Visitor, difícil demais para início de graduação, fraco em RAII |
| Editor de texto de terminal | Bom, mas o domínio é o próprio ferramental - confunde o objeto de estudo |

O que Deriva ganha:

1. **Feedback visual imediato.** No Sintonia, a saída é um WAV que precisa de um
   player. Aqui, a v0.1 já desenha no terminal. Para aluno de início de graduação
   isso muda a motivação de forma concreta.
2. **A estética é diegética.** O visual TUI/retrofuturista do site não é enfeite:
   é literalmente a interface do sistema que o aluno constrói. Site e projeto
   passam a ser a mesma coisa visualmente.
3. **RAII com consequência física.** A classe `terminal_bruto` põe o terminal em
   *raw mode* no construtor e restaura no destrutor. Se o aluno esquecer o
   destrutor, **o terminal dele fica quebrado ao sair**. É a melhor demonstração de
   RAII que existe, e não é uma metáfora.
4. **Herança natural, não forçada.** `entidade` → `sonda`/`drone`/`item` é
   hierarquia que o domínio pede, não taxonomia inventada para o exercício.
5. **O argumento final do Cap. 27.** O Qt entra como *segundo* front-end sobre o
   mesmo núcleo, provando separação domínio/UI - porque a TUI já existia. No
   Sintonia o Qt é a primeira interface, e o argumento não fecha.

Ressalva encontrada na pesquisa: o tutorial de roguelike em C++ mais difundido
(RogueBasin/libtcod) é criticado justamente por usar ponteiros crus com posse
espalhados pelo código e C++ pré-moderno. Não é referência de estilo - é
contraexemplo útil, e vale citar como tal no Cap. 11.

### Base técnica verificada

**FTXUI** para a camada de terminal, em vez de ncurses cru. Verifiquei
compilando, não pela documentação:

- A versão **v5.0.0** declara `target_compile_features(${library} PUBLIC cxx_std_17)`.
  Alinhada ao padrão-alvo da disciplina.
- Compilei um exemplo com `-std=c++17 -Wall -Wextra` usando `string_view` e
  structured bindings, com FTXUI via `FetchContent`: **zero warnings**, e renderiza
  caixas e *gauge* corretamente.
- Sem dependências externas; integra por `FetchContent`, que é o mesmo CMake já
  ensinado no Cap. 4.
- Cuidado: as versões v6/v7 são mais recentes e podem elevar o padrão exigido.
  **Fixar `GIT_TAG v5.0.0`** e não flutuar.

### Trilha de versões - mapeamento aula por aula

Mesma cadência do Sintonia: uma versão por aula, tudo compilando, variantes
quebradas onde o erro ensina.

| Versão | Aula(s) | Entrega | Conceitos |
|---|---|---|---|
| v0.1 | 08 | `vetor2`, `celula` | encapsulamento, const-correctness, `static`, `this`, `[[nodiscard]]` |
| v0.2 | 09 | `grade` | construtores, destrutor, lista de inicialização, regra do zero |
| v0.3 | 09 | `mapa` + carregamento de arquivo; **primeiro render** | composição, `std::optional`, `std::filesystem`, `string_view` |
| v1.0 | 15, 17 | hierarquia `entidade` | herança, `virtual`, `override`, `final`, destrutor virtual · **v1.0-quebrada**: sem destrutor virtual |
| v1.1 | 10, 11 | `mundo` com `vector<unique_ptr<entidade>>` e `terminal_bruto` | RAII, regra 0/3/5, `unique_ptr`, `shared_ptr` · **v1.1-quebrada**: `terminal_bruto` sem destrutor - o terminal fica inutilizável |
| v1.2 | 12 | movimento em `grade`/`mapa` | rvalue refs, `std::move`, `std::forward`, `noexcept` |
| v1.3 | 13 | operadores em `vetor2`, `mapa[pos]` | sobrecarga, funções livres, `operator<<` |
| v1.4 | 16 | `sonda_reparadora`: o diamante | herança múltipla, herança virtual |
| v1.5 | 14 | testes de FOV e caminho | Catch2 - FOV é determinístico, portanto testável |
| v1.6 | 18 | inspetor de entidade no console | RTTI, `dynamic_cast`, `typeid` |
| v2.0 | 19 | `grade<T>` genérica | templates, `if constexpr`, `static_assert`, CRTP |
| v2.1 | 20 | *(opcional)* restrições em `grade<T>` | **C++20** - Concepts/Ranges, rotulado como fora do padrão-alvo |
| v2.2 | 21 | erros de carregamento de mapa | exceções, `std::optional`, `std::variant` |
| v2.3 | 22 | FOV e inventário com algoritmos | STL, lambdas, `std::clamp` |
| v2.4 | 23 | thread de entrada + render | panorâmica de concorrência |
| v2.5 | 24 | salvar/carregar partida | serialização JSON, versionamento |
| v2.6 | 25, 26 | refatoração | SOLID; Command (entrada), State (telas), Observer (log), Factory (spawn), Strategy (IA), Composite (inventário) · **v2.6-antes**: `mundo` como god class |
| v2.7 | 27 | front-end Qt sobre o mesmo núcleo | `QObject`, signals/slots, separação domínio/UI |

Repositório novo, espelhando a convenção do `github.com/dobidu/sintonia`: uma tag
por versão, testes verdes em todas, e as variantes quebradas em branches próprias.

**Migração**: o Sintonia não é apagado. Os 15 callouts `callout-sintonia` do site
viram `callout-deriva`, e o Sintonia fica disponível como trilha alternativa -
quem estiver no meio do semestre não perde o chão.

---

## 4. Site v2 - requisitos

Direção estética e visual: ver `DESIGN-BRIEF-POO.md` e `DESIGN-TELAS-POO.md`, que
são os documentos para o Claude Design. Este handoff cobre a engenharia.

### Arquitetura

Mesma decisão tomada em LPII, e pelo mesmo motivo: livro e site divergem quando não
há fonte única.

```
conteudo/aulas/*.py      única fonte de verdade (prosa, código, exercícios, callouts)
interativos/<slug>.py    um exemplo interativo por conceito
build/build_site.py      → site/
build/extrair_v1.py      legado → conteudo/ (extração determinística)
legado/                  site v1 + poo.docx - SOMENTE LEITURA
exemplos/deriva/         o projeto Deriva, compilando
```

O livro em DOCX continua sendo a fonte da prosa nesta fase. Migração para Typst é
possível depois, mas não está no escopo agora - em LPII já foi feita e o pipeline
está validado, então é reaproveitável quando fizer sentido.

### Exemplos interativos

O site v1 tem **zero** interatividade. Esta é a maior adição da fase.

Decisão de arquitetura: os interativos são **simulações determinísticas
autoradas**, não execução real de C++ no navegador. Isso não é limitação, é a
escolha certa - o que precisa ser visto (vtable, endereço na pilha, contagem de
referências, o objeto de origem depois do move) é exatamente o que a execução real
*não* mostra. Para compilar de verdade, cada bloco de código ganha *deep link* para
o Compiler Explorer, já com `-std=c++17` na linha de comando.

Seis tipos canônicos de interativo, reutilizados nas 27 aulas:

1. **Inspetor de objeto** - leiaute na memória: membros, ordem de declaração,
   *padding*, pilha × heap. Aluno reordena os membros e vê o tamanho mudar.
2. **Rastreador de ciclo de vida** - passo a passo por escopos, com a ordem exata
   de construção e destruição. Aluno abre/fecha escopos, lança exceção no meio e vê
   o desenrolar da pilha.
3. **Despachante virtual** - `vptr`, vtable e resolução dinâmica. Aluno escolhe tipo
   estático e tipo dinâmico separadamente; sem `virtual`, a chamada vai para o lugar
   errado e isso fica visível.
4. **Copiar × mover** - lado a lado, com o estado do objeto de origem **depois** da
   operação. É o mal-entendido mais comum de C++ e o mais fácil de mostrar.
5. **Grafo de posse** - `unique_ptr` e `shared_ptr` com contagem de referências ao
   vivo, incluindo o ciclo que `shared_ptr` não resolve e o `weak_ptr` que resolve.
6. **Diferenciador de refatoração** - antes/depois de SOLID e de cada padrão,
   com o acoplamento desenhado como grafo.

Contrato de todo interativo, herdado da spec de LPII e válido aqui:
estado determinístico; passo sob controle do aluno (nunca autoplay); ao menos um
cenário que **demonstra a falha** e um que a evita; estado interno legível em mono;
fallback estático sob `prefers-reduced-motion`; legenda de uma ou duas frases dizendo
onde olhar. Autoplay sem passo é rejeição automática.

### Correções de engenharia

- Uma única `@media` no CSS - insuficiente. O site precisa funcionar de 360px a
  projetor.
- Nenhum `prefers-reduced-motion`.
- Fontes vêm do Google Fonts por `@import` dentro do CSS, que é o pior caminho
  (bloqueia o render e depende de rede). Auto-hospedar em `assets/fontes/`.
- Prism e Mermaid vêm de CDN. Auto-hospedar ou fixar versão com `integrity`.
- Sem busca, sem âncora por seção, sem `<meta>` de descrição/OG, sem favicon.

Preservar: os 108 exercícios, os 5 tipos de callout (com `sintonia`→`deriva`), o
realce de sintaxe, os diagramas, e a navegação por slides.

---

## 5. Portões de qualidade

```bash
# núcleo Deriva
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
g++ -std=c++17 -Wall -Wextra -Wpedantic     # zero warnings
-fsanitize=address,undefined                 # ASan + UBSan limpos (Cap. 4 já os ensina)
ctest --test-dir build                       # todos os testes verdes
```

- Todo trecho de código do site e do livro é **extraído de arquivo que compila**,
  nunca digitado no material. Trecho literal solto é dívida.
- As variantes quebradas são marcadas como tais e acompanhadas da saída do
  sanitizer ou do bug observável que as acusa.
- `GIT_TAG v5.0.0` fixo para o FTXUI.
- Nenhum exemplo depende de C++20. Os rotulados C++20 compilam em alvo separado e
  opcional.

---

## 6. Sprints

| Sprint | Entrega | Portão |
|---|---|---|
| 0 | Este handoff + documentos de design | **aprovação do autor** |
| 1 | Extração do site v1 para `conteudo/` + gerador reproduzindo o v1 | `diff` contra `legado/` só com o que foi mudado de propósito |
| 2 | Deriva v0.1→v0.3 + design system aplicado | primeiro render no terminal e no site |
| 3 | Os 6 interativos canônicos, calibrados | revisão de estilo e de contrato |
| 4 | Atualização de sintaxe C++17 nos 27 capítulos | revisão de conteúdo |
| 5 | Deriva v1.x→v2.7 com testes e variantes quebradas | `ctest` verde, quebradas documentadas |
| 6 | Build final: site + livro atualizado + repositório Deriva | aceite |

---

## 7. Decisões pendentes com o autor

1. **Semestre-alvo.** O material todo diz "2026.1" e o exercício integrador tem
   prazo em julho de 2026. Confirmar a oferta a que esta versão se destina.
2. **Azul UFPB.** A paleta TUI/retrofuturista não convive bem com `#1a56a0` como cor
   dominante. Proposta nos documentos de design: manter o azul como marca
   institucional em badge e rodapé, e deixar a interface por conta da paleta de
   fósforo. Precisa de aval.
3. **Nome do sistema.** "Deriva" é proposta. Alternativas na mesma linha: Ártemis,
   Sonda, Perímetro. Trocar o nome é barato agora e caro depois de 27 aulas escritas.
4. **Destino do Sintonia.** Trilha alternativa preservada (recomendado) ou
   descontinuada.
5. **Central de Alertas.** O exercício integrador atual é independente de domínio e
   sobrevive à troca sem mudança. Confirmar se continua.
