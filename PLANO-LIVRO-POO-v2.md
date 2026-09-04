# PLANO DO LIVRO - POO v2

Reflexo do `PLANO_DE_ENSINO_POO_v2.md` no livro da disciplina.

Estado atual: **108 páginas**, 27 capítulos + glossário + referências, fonte canônica
em `poo.docx`.

Alvo: **26 capítulos + 3 anexos**, espelhando a ordem das 26 aulas, com a sintaxe de
C++17 distribuída e o Deriva no lugar do Sintonia.

---

## 1. A decisão estrutural

O livro passa a seguir a ordem do curso, capítulo por aula, em correspondência
estrita: **Aula N = Capítulo N**.

Isso custa uma reorganização grande e vale a pena por um motivo só: é o que garante
que o estudante encontre em casa exatamente o que viu projetado. Hoje a
correspondência existe por acidente, e o plano v2 acabou de rompê-la - infraestrutura
saiu do 4º para o 2º lugar, herança passou à frente de ponteiros inteligentes, e a
regra dos zero/três/cinco se partiu entre duas unidades. Manter a numeração antiga
significaria pedir ao estudante que consultasse uma tabela de conversão a cada aula.

Onde o curso divide um tema em dois encontros, o livro tem dois capítulos. Onde o
curso funde, o livro funde. A invariância é mais valiosa que a elegância da divisão.

---

## 2. Estrutura proposta

Legenda: **=** preservado, com renumeração · **↑** expandido · **↷** movido ·
**⊕** funde capítulos · **⊘** dividido · **NOVO** inédito.

### Unidade I - Fundamentos · ~40pp

| Cap | Título | Origem | O que muda |
|---|---|---|---|
| 1 | Da programação procedural à orientação a objetos | Cap. 1 · = | Exemplo comparativo migra de "Sistema de Alunos" para o Deriva |
| 2 | Infraestrutura do programador C++ | Cap. 4 · ↷↑ | Sobe de posição. Entra `FetchContent` com FTXUI e Catch2 como dependência `SYSTEM`, para o portão de zero warnings incidir só no código do estudante. Sai a seção de sanitizers como portão - o laboratório não os tem - e entra o `gdb` com ponto de parada em destrutor |
| 3 | Fundamentos de C++17 para POO | Cap. 2 · ↷↑ | O capítulo com maior déficit do livro. Entram `std::string_view` com a armadilha de tempo de vida, ligações estruturadas, `[[nodiscard]]` e `[[maybe_unused]]` - todos hoje com **zero** ocorrências no livro inteiro |
| 4 | Git, LLM como copiloto e a rubrica de revisão | **Cap. 5 ⊕ Cap. 6 ⊕ parte do Cap. 27** | Fusão de três origens. A rubrica de revisão de código OO gerado por IA sai do fim do livro e vem para cá, porque passa a ser instrumento das três caças ao bug - e um instrumento tem de chegar antes do uso |
| 5 | Classificação de linguagens e sistemas de tipos | Cap. 3 · ↷= | Renumeração |
| 6 | UML leve | Cap. 7 · ↷= | Diagramas passam a ser do Deriva |
| 7 | Classes e objetos; o contador de instâncias vivas | Cap. 8 · ↑ **+ NOVO** | Membros estáticos ganham o exemplo canônico da disciplina: `static int vivos`, incrementado no construtor e decrementado no destrutor. É o detector de vazamento que a disciplina usará por 19 capítulos |
| 8 | Ciclo de vida e RAII | Cap. 9 ⊕ parte do Cap. 10 · ↑ | Absorve o RAII que estava no Cap. 10. Entra a instrumentação de ciclo de vida - construtores e destrutores imprimindo a própria execução - e o `terminal_bruto` |
| 9 | Operações especiais: a regra do zero e do três | **⊘ Cap. 10 (fatia 1)** | Só cópia e atribuição. A regra dos cinco vai para o Cap. 14, na unidade seguinte |

### Unidade II - Hierarquias, posse e despacho · ~48pp

| Cap | Título | Origem | O que muda |
|---|---|---|---|
| 10 | Herança simples | Cap. 15 · ↷= | Sobe cinco posições: passa à frente dos ponteiros inteligentes |
| 11 | Funções virtuais e classes abstratas | Cap. 17 · ↷↑ | O destrutor virtual ganha tratamento próprio: o vazamento que sua ausência produz, acusado pelo contador `vivos` do Cap. 7 e lido no `gdb` |
| 12 | Ponteiros inteligentes I - posse exclusiva | **⊘ Cap. 11 (fatia 1)** | `unique_ptr`; o ponteiro cru com posse como contraexemplo documentado - com menção ao tutorial de *roguelike* em C++ mais difundido, que é criticado justamente por isso |
| 13 | Ponteiros inteligentes II - posse compartilhada | **⊘ Cap. 11 (fatia 2)** | `shared_ptr`, `weak_ptr`, contagem de referências, o ciclo que o contador acusa |
| 14 | Semântica de movimento e a regra dos cinco | Cap. 12 ⊕ parte do Cap. 10 · ↑ | Recebe a regra dos cinco do Cap. 10. Entra `std::forward` e encaminhamento perfeito como panorama - hoje **zero** ocorrências num capítulo sobre movimento |
| 15 | Sobrecarga de operadores | Cap. 13 · = | Operadores do Deriva: `vetor2`, `operator[]` de `mapa` |
| 16 | Testes com Catch2 e replay determinístico | Cap. 14 · ↑ **+ NOVO** | O teste como especificação executável. Entra o replay: semente fixa, roteiro gravado, despejo idêntico byte a byte. É o oráculo dos Caps. 24 e 25 |
| 17 | Herança múltipla e o diamante | Cap. 16 · ↷= | Renumeração |
| 18 | Polimorfismo dinâmico e RTTI | Cap. 18 · = | Renumeração |

### Unidade III - Genericidade, robustez e projeto · ~46pp

| Cap | Título | Origem | O que muda |
|---|---|---|---|
| 19 | Templates, polimorfismo estático e CRTP | Cap. 19 · ↑ | `if constexpr` no lugar de SFINAE - hoje uma única ocorrência no livro. O CRTP ganha alvo concreto: generalizar em `contador_de_instancias<T>` o que foi escrito à mão em três classes desde o Cap. 7. A repetição anterior é o argumento do template |
| 20 | Tratamento de erros | Cap. 21 · ↑ | Entra `std::filesystem` no carregamento de mapa - hoje ausente. Garantias de exceção e desenrolar da pilha com destrutores ganham peso, por ligarem ao Cap. 8 |
| 21 | STL panorâmica e lambdas | Cap. 22 · ↑ | Lambdas passam de **uma** menção no livro inteiro a conteúdo de capítulo. Entra `std::clamp` |
| 22 | Concorrência em C++ - panorâmica | Cap. 23 · = | Ponte explícita com a disciplina de Programação Concorrente |
| 23 | Serialização | Cap. 24 · = | Salvar e carregar partida do Deriva; versionamento de formato |
| 24 | SOLID e invariância de comportamento | Cap. 25 · ↑ | A refatoração do `mundo` como *god class*, verificada por replay. A lição é que refatoração correta é a que não muda a saída |
| 25 | Padrões de projeto canônicos em C++ moderno | Cap. 26 · ↑ | Strategy com lambdas (não com herança); Command, State, Observer, Factory, Composite, Decorator sobre o Deriva; Singleton e seus problemas |
| 26 | Qt e a separação domínio/apresentação | **⊘ Cap. 27 (fatia Qt)** | A metade de LLM foi para o Cap. 4. Fica `QObject`, signals/slots, e o argumento do segundo front-end sobre o mesmo núcleo |

### Anexos · ~14pp

| | Título | Origem |
|---|---|---|
| A | **Concepts e Ranges - C++20** | **Cap. 20 rebaixado.** Deixa de ser capítulo porque deixou de ser aula: são 20 minutos dentro do Cap. 19. O conteúdo não se perde, muda de estatuto |
| B | **Referência rápida de C++17** | **NOVO** - tabela de consulta para prova e laboratório |
| C | **O Deriva: as 20 versões** | **NOVO** - v0.0 a v2.7, cada uma com o capítulo que a introduz e as variantes quebradas |

Mais glossário e referências, revisados.

---

## 3. Orçamento de páginas

De 108 para aproximadamente 148, distribuídas ~40/48/46 por unidade mais 14 de anexos.

O crescimento não vem de capítulo novo - vem de três frentes: a sintaxe de C++17 que
falta e que se distribui por cerca de dez capítulos; o bloco de instrumentação sem
ferramenta externa, que precisa ser ensinado antes de ser exigido; e as divisões, que
custam páginas de moldura (contexto, fechamento, exercícios) em cada metade.

Não há teto rígido a defender aqui, ao contrário de LPII. O livro de POO é curto para
26 aulas: 108 páginas dão pouco mais de 4 por aula, e a densidade de prosa que o
material exige não cabe nisso.

---

## 4. Migração - os pontos de perda silenciosa

Três capítulos se partem, e é aí que conteúdo desaparece sem ninguém notar:

**Cap. 10 → Caps. 8, 9 e 14.** A pior das três. O texto atual trata RAII e as três
regras como um bloco contínuo, e o plano novo o distribui por duas unidades, com uma
prova no meio. Recomendação: extrair o Cap. 10 em três arquivos separados **antes**
de escrever qualquer coisa, e conferir parágrafo por parágrafo que cada um encontrou
capítulo. Sobra que não couber em nenhum é sinal de que a divisão do plano precisa de
uma nota, não de que o parágrafo é descartável.

**Cap. 11 → Caps. 12 e 13.** Mais simples, porque `unique_ptr` e
`shared_ptr`/`weak_ptr` já são seções distintas. O risco é a introdução comum - o
argumento de por que ponteiro inteligente existe - que precisa aparecer no Cap. 12 e
ser referenciada, não duplicada, no 13.

**Cap. 27 → Caps. 4 e 26.** As duas metades vão para pontas opostas do livro. A
metade de LLM não é só transplantada: ela ganha peso, porque no Cap. 4 passa a ser
instrumento operacional e não reflexão final.

---

## 5. Correções de bibliografia

O plano v2 já corrigiu o que eu havia errado - a autoria de Catch2 (Nash e
Hořeňovský, não Horák) e a edição de *Programming: Principles and Practice* (3ª ed.,
2024) - e acrescentou Josuttis, *C++17 - The Complete Guide*, que é a referência certa
para o eixo desta fase.

A bibliografia do livro deve ser alinhada à do plano, e não o contrário. Uma
verificação a fazer antes de publicar: a bibliografia atual do livro não foi auditada
neste ciclo. Vale rodar nela a mesma checagem que rodei na de LPII, onde apareceram
duas duplicatas, um título autopublicado sem valor de referência e uma autoria
trocada.

---

## 6. Pipeline

O livro continua em DOCX nesta fase, com `poo.docx` como fonte canônica. Migrar para
Typst é possível - o pipeline foi validado em LPII, com Inter e JetBrains Mono
embutindo corretamente e a acentuação PT-BR conferida no PDF - mas não está no escopo
agora, e a reestruturação de 27 para 26 capítulos já é mudança suficiente para um
ciclo.

Se a migração for feita depois, a armadilha a lembrar está registrada: em Typst,
`#set text(font: …)` dentro de bloco de código é ignorado pela show rule de `raw`, e o
PDF cai silenciosamente em DejaVu Sans Mono. O correto é `#show raw: set text(…)`, e a
verificação é ler o `/BaseFont` do PDF gerado em vez de confiar no visual.

Uma decisão que vale tomar junto: as figuras do livro passarem a ser exportadas dos
mesmos módulos que geram os 8 interativos do site. Uma fonte, dois meios - e o
estudante encontra no PDF exatamente o quadro que viu projetado.
