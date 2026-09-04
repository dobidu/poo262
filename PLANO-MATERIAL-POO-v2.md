# PLANO DO MATERIAL - POO v2

Reflexo do `PLANO_DE_ENSINO_POO_v2.md` no material da disciplina: site, exemplos
interativos e artefatos publicados. Substitui o escopo de site descrito em
`HANDOFF_POO_v2.md` §4.

Este documento se soma aos de design (`DESIGN-BRIEF-POO.md`,
`DESIGN-TELAS-POO.md`) - as correções que o plano novo impõe a eles estão em §6.

---

## 1. O que o plano novo muda

O plano v2 não é um ajuste de cronograma. Três decisões dele reorganizam o material:

**26 aulas, não 27.** A semana 15 E1 passa a ser encontro de reserva. Git e LLM se
fundem numa aula, e Concepts/Ranges deixa de ser aula para virar 20 minutos dentro da
aula de templates.

**A ordem mudou de verdade.** Infraestrutura sai do 4º para o 2º lugar. Herança e
funções virtuais passam **à frente** dos ponteiros inteligentes. A regra dos
zero/três/cinco se parte: zero e três na Unidade I, cinco junto com movimento na
Unidade II. Ponteiros inteligentes se partem em duas aulas, posse exclusiva e posse
compartilhada.

**O contador de instâncias vivas nasce na Aula 7 e não na 19.** É introduzido como o
exemplo canônico de membro estático, escrito à mão em três classes, e só na Aula 19 é
generalizado em `contador_de_instancias<T>` por CRTP. Isto é melhor do que eu havia
planejado: a repetição manual é o que motiva o template, em vez de o template chegar
como solução para um problema que o estudante nunca sentiu.

Consequência direta: **a numeração de aula deixa de coincidir com a de capítulo.**
Isso precisa de mapeamento explícito, ou conteúdo se perde na migração.

---

## 2. Mapeamento capítulo → aula

Verificado: os 27 capítulos do livro atual encontram destino, as 26 aulas ficam
cobertas, nada fica órfão.

| Aula | Título | Vem de | Página v1 |
|---|---|---|---|
| 1 | Da programação procedural à OO | Cap. 1 | `aula01-complexidade-oo` |
| 2 | Infraestrutura do programador C++ | Cap. 4 | `aula04-transicao-cpp` |
| 3 | Fundamentos de C++17 para POO | Cap. 2 | `aula02-conceitos-fundamentais` |
| 4 | Git, LLM como copiloto e a rubrica | **Cap. 5 + Cap. 6 + parte do Cap. 27** | `aula05` + `aula06` **fundidas** |
| 5 | Classificação de linguagens e tipos | Cap. 3 | `aula03-classificacao-linguagens` |
| 6 | UML leve | Cap. 7 | `aula07-uml-leve` |
| 7 | Classes e objetos; o contador `vivos` | Cap. 8 **+ conteúdo novo** | `aula08-classes-objetos` |
| 8 | Ciclo de vida e RAII | Cap. 9 + parte do Cap. 10 | `aula09-ciclo-de-vida` |
| 9 | Operações especiais: regra do zero e do três | **parte do Cap. 10** | `aula10-raii-rule-of-five` (fatia 1/3) |
| 10 | Herança simples | Cap. 15 | `aula15-heranca-simples` |
| 11 | Funções virtuais e classes abstratas | Cap. 17 | `aula17-funcoes-virtuais` |
| 12 | Ponteiros inteligentes I - posse exclusiva | **parte do Cap. 11** | `aula11-smart-pointers` (fatia 1/2) |
| 13 | Ponteiros inteligentes II - posse compartilhada | **parte do Cap. 11** | `aula11-smart-pointers` (fatia 2/2) |
| 14 | Movimento e a regra dos cinco | Cap. 12 + **parte do Cap. 10** | `aula12-move-semantics` + fatia de `aula10` |
| 15 | Sobrecarga de operadores | Cap. 13 | `aula13-sobrecarga-operadores` |
| 16 | Testes com Catch2 e replay determinístico | Cap. 14 **+ conteúdo novo** | `aula14-testes-catch2` |
| 17 | Herança múltipla e o diamante | Cap. 16 | `aula16-heranca-multipla` |
| 18 | Polimorfismo dinâmico e RTTI | Cap. 18 | `aula18-polimorfismo-dinamico` |
| 19 | Templates, CRTP e `contador_de_instancias<T>` | Cap. 19 + **Cap. 20 comprimido** | `aula19-templates-crtp` + `aula20` absorvida |
| 20 | Tratamento de erros | Cap. 21 | `aula21-tratamento-erros` |
| 21 | STL panorâmica e lambdas | Cap. 22 | `aula22-stl` |
| 22 | Concorrência em C++ - panorâmica | Cap. 23 | `aula23-concorrencia` |
| 23 | Serialização | Cap. 24 | `aula24-serializacao` |
| 24 | SOLID e invariância de comportamento | Cap. 25 | `aula25-solid` |
| 25 | Padrões de projeto | Cap. 26 | `aula26-design-patterns` |
| 26 | Qt e a separação domínio/apresentação | **parte do Cap. 27** | `aula27-qt-llms` (fatia Qt) |

Resumo da migração: **20 páginas apenas renumeram**, 2 se fundem numa, 3 se partem, 1
sai de aula e vira anexo.

### As três migrações de risco

Estas são as que perdem conteúdo em silêncio se forem tratadas como renomeação:

1. **`aula10-raii-rule-of-five` se parte em três.** RAII vai para a Aula 8, a regra do
   zero e do três para a Aula 9, a regra dos cinco para a Aula 14 - que fica na
   unidade seguinte. É a migração mais perigosa do lote, porque o conteúdo atravessa
   fronteira de unidade e de prova.
2. **`aula27-qt-llms` se parte em duas metades que vão para pontas opostas do
   semestre.** Qt fica na Aula 26; a rubrica de revisão de código gerado por IA vai
   para a Aula 4, na semana 2, porque passa a ser instrumento das três caças ao bug.
3. **`aula20-concepts-ranges` deixa de ser aula.** O conteúdo não é descartado: vira
   anexo do livro e página de anexo do site, marcada C++20, referenciada em 20
   minutos da Aula 19.

---

## 3. Conteúdo que não existe no v1

Não é migração - é escrita nova. Ordenado pelo que trava a semana mais cedo:

| O que | Aula | Por que é novo |
|---|---|---|
| Contador `vivos` como exemplo canônico de membro estático | 7 | O plano o promove a instrumento central; o Cap. 8 atual trata `static` genericamente |
| Instrumentação de ciclo de vida (ctor/dtor/cópia/movimento imprimindo a própria execução) | 8, 14 | Substitui o sanitizer ausente |
| `gdb` com ponto de parada em destrutor | 8, 11 | Idem - e é como se prova que o destrutor da derivada nunca roda |
| Replay determinístico como portão de refatoração | 16, 24 | Não existe no material; é o oráculo da disciplina |
| `contador_de_instancias<T>` por CRTP | 19 | O Cap. 19 ensina CRTP em abstrato; agora tem alvo |
| Rubrica de revisão de código OO gerado por IA, publicada | 4 | Existe disperso nos Caps. 6 e 27; precisa virar artefato aplicável |
| Portão `make verifica` (warning + `ctest` + replay + contadores em zero) | todas | Novo |
| `DECISAO.md` e sua rubrica de correção | todas | Novo |
| Os 12 laboratórios preparatórios com esqueleto, solução e portão | - | Novos por inteiro |
| Deriva, 20 versões (v0.0 → v2.7) | todas | Substitui o Sintonia |

Duas observações sobre a lista. A primeira: o bloco das três técnicas sem ferramenta
externa - contador, instrumentação, `gdb` - é o que sustenta o portão de correção da
disciplina inteira. Se ele atrasar, os laboratórios da Unidade II não têm critério.
Precisa entrar antes de tudo.

A segunda: os 12 laboratórios são publicados **com solução**, e isso é uma seção do
site que hoje não existe em nenhuma forma. Não é um apêndice de aula, é conteúdo com
volume próprio - esqueleto, solução de referência e portão, doze vezes.

---

## 4. Inventário do site v2

O site v1 tem 27 páginas de aula, 131 slides, 108 exercícios, 98 callouts, 60 blocos
de código, e nada além disso. O v2 tem seções que não existem hoje:

| Seção | Estado |
|---|---|
| 26 páginas de aula | migradas conforme §2 |
| Anexo: Concepts e Ranges (C++20) | conteúdo da `aula20`, rebaixada |
| Anexo: referência rápida C++17 | novo |
| Plano de ensino | novo - publicado no site, com download em `.docx` |
| Trilha Deriva (20 versões) | novo - substitui a trilha Sintonia |
| Laboratórios preparatórios (12, com solução) | novo |
| Rubrica de revisão de código gerado por IA | novo - artefato aplicável, não texto de aula |
| Portão de correção (`make verifica`) | novo - página de referência |
| Trilha Sintonia | preservada como alternativa |
| Glossário e referências | existentes, revisados |

Os 15 callouts `callout-sintonia` viram `callout-deriva`. Os 108 exercícios migram com
as aulas, redistribuídos pelas fusões e divisões de §2.

---

## 5. Exemplos interativos - 8 tipos, 26 aulas

Revisão do que eu havia proposto: eram 6 tipos, e o plano novo exige mais dois. O
pipeline de compilação passou para a Aula 2, na primeira semana, e precisa de peça
própria; e a rubrica de revisão de IA, usada nas três caças ao bug, só funciona como
instrumento se for aplicável e não só lida.

**Os 8 tipos canônicos.** Todos sob o mesmo contrato: estado determinístico, passo do
estudante, um cenário que demonstra a falha e um que a evita, estado interno legível
em mono, fallback sem movimento, legenda do que observar. Autoplay é rejeição
automática.

1. **Inspetor de objeto** - leiaute em memória, ordem de declaração, *padding*,
   subobjeto base dentro da derivada, membro estático fora do objeto.
2. **Rastreador de ciclo de vida** - ordem exata de construção e destruição,
   escopos, desenrolar da pilha por exceção, referência pendente.
3. **Despachante** - `vptr` e vtable, tipo estático versus dinâmico, resolução de
   sobrecarga, `dynamic_cast`.
4. **Copiar × mover** - com o estado do objeto de origem **depois** da operação.
5. **Grafo de posse** - `unique_ptr`, `shared_ptr`, `weak_ptr`, contagem de
   referências, o ciclo que vaza.
6. **Diferenciador de refatoração** - antes/depois, grafo de acoplamento, e o
   *diff* do despejo de estado que prova invariância.
7. **Expansor de compilação e template** - pipeline pré-processador/compilação/ligação
   e onde cada erro aparece; instanciação de template; `if constexpr` podando ramo em
   tempo de compilação.
8. **Revisor com rubrica** - código OO gerado, plausível e defeituoso, com cada item
   da rubrica acendendo a falha correspondente.

**Distribuição pelas aulas:**

| Tipo | Aulas |
|---|---|
| Inspetor de objeto | 7, 10, 17 |
| Rastreador de ciclo de vida | 3 (pendência do `string_view`), 8, 9, 20 |
| Despachante | 5, 11, 15, 18 |
| Copiar × mover | 14 |
| Grafo de posse | 12, 13 |
| Diferenciador de refatoração | 1, 16, 24, 25, 26 |
| Expansor de compilação e template | 2, 19, 21 |
| Revisor com rubrica | 4, 6, 23 |
| Reaproveitado de LPII | 22 - a peça de race condition, sob outra disciplina |

A Aula 22 merece nota. É panorâmica de concorrência, e a peça de *race condition* já
construída para LPII serve exatamente aqui, com a legenda trocada. É o primeiro
reaproveitamento entre as duas disciplinas, e é de graça.

---

## 6. Correções aos documentos de design

O plano novo invalida números que estão nos documentos de design. Antes de levá-los
ao Claude Design, corrija:

- **`DESIGN-TELAS-POO.md`, cabeçalho:** "27 aulas em 3 unidades" → **26 aulas**.
- **T5 · Trilha Deriva:** eram 17 versões, agora são **20** (v0.0 → v2.7). E as
  variantes quebradas agora têm nome e lugar definidos pelas três caças ao bug: cópia
  rasa em `grade` (semana 5), destrutor não virtual (semana 9), refatoração que mudou
  a saída (semana 13).
- **T8 · Marcador C++20:** o uso encolheu. Concepts e Ranges não são mais aula, são
  anexo. O selo continua necessário, mas aparece num anexo e em 20 minutos de uma
  aula, não numa aula inteira - o peso visual deve acompanhar.
- **Telas novas, a acrescentar à lista:**
  - **T12 · Laboratório preparatório.** Esqueleto, solução revelável e portão de
    correção, doze vezes. É seção nova do site, não variação de página de aula.
  - **T13 · Rubrica aplicável.** A rubrica de revisão de código gerado por IA como
    instrumento com o qual se trabalha, não texto que se lê. É a base da tela T13 e
    do interativo tipo 8.
  - **T14 · Plano de ensino.** Tabelas densas, cronograma de 15 semanas, tabela de
    12 laboratórios, com download em `.docx`. A referência de renderização é a
    versão publicada do plano de LPII.
- **`DESIGN-BRIEF-POO.md`** permanece válido sem alteração. A direção de fósforo
  âmbar, os três papéis do IBM Plex, o box-drawing como primitiva e as regras de
  movimento não são afetados pela reorganização de conteúdo.

---

## 7. Ordem de execução revista

A mudança de prioridade em relação ao handoff: o bloco de instrumentação sem
ferramenta externa sobe para o Sprint 1, porque sem ele os laboratórios da Unidade II
não têm portão.

| Sprint | Entrega |
|---|---|
| 1 | Extração do v1 + gerador reproduzindo o v1 + **mapeamento de §2 aplicado explicitamente**, com as três migrações de risco conferidas item a item |
| 2 | Deriva v0.0→v0.3 · contador `vivos`, instrumentação de ciclo de vida, `gdb` no destrutor, `make verifica` |
| 3 | Os 8 interativos canônicos, calibrados nas Aulas 8, 11 e 14 |
| 4 | Unidade I completa: 9 aulas, LAB-01 a LAB-05, rubrica publicada |
| 5 | Unidade II: 9 aulas, LAB-06 a LAB-09, Deriva v1.0→v1.8, as duas primeiras caças ao bug |
| 6 | Unidade III: 8 aulas, LAB-10 a LAB-12, Deriva v2.0→v2.7, anexos |
| 7 | Livro reestruturado (ver `PLANO-LIVRO-POO-v2.md`) e build final |

---

## 8. Pendências

1. **Código do componente e pré-requisito** continuam marcados para preencher a partir
   do SIGAA e do PPC.
2. **Ementa do PPC.** O plano v2 marca a ementa como "de trabalho" até que a do PPC
   seja transcrita literalmente. Se a do PPC for mais restritiva - por exemplo, se não
   mencionar C++17 - , o material continua válido, mas o plano precisa de nota
   conciliatória.
3. **Nome do sistema.** "Deriva" segue como proposta. Trocar agora é barato; depois
   de 26 aulas e 20 versões escritas, não é.
4. **Qt sem entrega obrigatória.** O plano v2 rebaixa a Aula 26 a demonstração do
   docente com esqueleto publicado. Isso reduz o esforço de material, mas enfraquece o
   argumento de separação domínio/apresentação, que era uma das três razões para
   escolher o Deriva. Vale decidir se o esqueleto publicado é suficiente ou se cabe
   um laboratório opcional sem nota.
