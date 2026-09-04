# PENDÊNCIAS DA MIGRAÇÃO v1 → v2

Gerado por `build/extrair_v1.py`. **Dois números, e a diferença importa:** a tabela abaixo é o que a extração encontrou no site v1, e ela não muda; o que ainda está aberto é o que os arquivos de `conteudo/aulas/` declaram, e são **1**.

## Ainda aberto

- **a11.py** · `caca-bug` · CAÇA AO BUG 2: destrutor não virtual - semana 9. A variante e o roteiro existem em `variantes/v1.1-quebrada/`; falta o roteiro de condução em sala.

## O que a extração encontrou no v1

Histórico, e não lista de tarefas: estes são os itens que a migração determinística não podia resolver sozinha, e a maioria já foi resolvida à mão desde então.

| tipo | quantos | o que é |
|---|---|---|
| `dominio` | 46 | prosa ou código ainda no Sintonia - reescrever sobre o Deriva |
| `novo` | 16 | conteúdo novo exigido pelo plano v2 - escrever |
| `lab` | 12 | laboratório preparatório - esqueleto, solução e portão |
| `exercicios` | 7 | exercícios de página partida - redistribuir entre as fatias |
| `fatia` | 7 | slide que atravessa a divisão do plano - separar parágrafo por parágrafo |
| `bruto` | 5 | bloco HTML copiado sem interpretação - conferir o tipo |
| `caca-bug` | 3 | variante quebrada e roteiro da caça ao bug |

## marcação do v1 consertada na extração - 7

`<` literal que o v1 deixou solto no HTML e que quebrava qualquer validador. Escapado automaticamente; o conteúdo não mudou.

- **aula 21** - `<T>`
- **aula 21** - `<T>`
- **aula 21** - `<T>`
- **aula 21** - `<K,V>`
- **aula 21** - `<K,V>`
- **aula 21** - `<T>`
- **aula 21** - `<T,N>`


**Total: 96 pendências.**

## `dominio` - 46

- **aula 02** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 04** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 04** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 05** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 07** - callout `sintonia` → `deriva`: “Sintonia v0.1 - sample e track” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 07** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 08** - callout `sintonia` → `deriva`: “Sintonia - v0.2 - AudioBuffer com ciclo de vida” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 08** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 08** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 08** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 08** - callout `sintonia` → `deriva`: “Sintonia - v1.1 - effect_chain com RAII” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 09** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 10** - callout `sintonia` → `deriva`: “Sintonia - v1.0 - Hierarquia effect” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 10** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 11** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 11** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 12** - callout `sintonia` → `deriva`: “Sintonia - v1.1 - Cadeia de efeitos com unique_ptr” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 14** - callout `sintonia` → `deriva`: “Sintonia - v1.2 - audio_buffer com movimento” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 14** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 14** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 14** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 15** - callout `sintonia` → `deriva`: “Sintonia - v1.3 - Operadores em sample e audio_buffer” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 15** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 15** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 16** - callout `sintonia` → `deriva`: “Sintonia - v2.5 - 72 testes passando” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 16** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 16** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 17** - callout `sintonia` → `deriva`: “Sintonia v1.4 - Looper com diamante” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 18** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 18** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 19** - callout `sintonia` → `deriva`: “Sintonia - v2.0 - buffer<T>” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 19** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 19** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 20** - callout `sintonia` → `deriva`: “Sintonia - v2.1 - Erros modernos” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 20** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 20** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 22** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 23** - callout `sintonia` → `deriva`: “Sintonia - v2.2 - Serialização JSON” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 23** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 24** - callout `sintonia` → `deriva`: “Sintonia v2.3 - Refatoração SOLID” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 24** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 24** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 25** - callout `sintonia` → `deriva`: “Sintonia - v2.3 - Todos os padrões” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.
- **aula 25** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 25** - bloco de código do Sintonia - precisa ser reescrito sobre o Deriva e extraído de arquivo que compila.
- **aula 26** - callout `sintonia` → `deriva`: “Sintonia - v2.4 - Interface Qt” - a prosa dentro dele ainda fala do sistema antigo e precisa de reescrita humana para o Deriva.

## `novo` - 16

- **aula 02** - conteúdo NOVO exigido pelo plano v2: gdb com ponto de parada em destrutor. Não existe no v1 - precisa ser escrito.
- **aula 02** - conteúdo NOVO exigido pelo plano v2: portão `make verifica`. Não existe no v1 - precisa ser escrito.
- **aula 03** - conteúdo NOVO exigido pelo plano v2: std::string_view e a pendência de tempo de vida. Não existe no v1 - precisa ser escrito.
- **aula 03** - conteúdo NOVO exigido pelo plano v2: ligações estruturadas. Não existe no v1 - precisa ser escrito.
- **aula 03** - conteúdo NOVO exigido pelo plano v2: [[nodiscard]] e [[maybe_unused]]. Não existe no v1 - precisa ser escrito.
- **aula 04** - conteúdo NOVO exigido pelo plano v2: rubrica de revisão de código OO gerado por IA, publicada como artefato. Não existe no v1 - precisa ser escrito.
- **aula 07** - conteúdo NOVO exigido pelo plano v2: o contador `vivos` como exemplo canônico de membro estático. Não existe no v1 - precisa ser escrito.
- **aula 08** - conteúdo NOVO exigido pelo plano v2: instrumentação de ciclo de vida. Não existe no v1 - precisa ser escrito.
- **aula 08** - conteúdo NOVO exigido pelo plano v2: terminal_bruto e o RAII com consequência física. Não existe no v1 - precisa ser escrito.
- **aula 14** - conteúdo NOVO exigido pelo plano v2: std::forward e encaminhamento perfeito. Não existe no v1 - precisa ser escrito.
- **aula 14** - conteúdo NOVO exigido pelo plano v2: correção: estado válido mas não-especificado, com SSO. Não existe no v1 - precisa ser escrito.
- **aula 16** - conteúdo NOVO exigido pelo plano v2: replay determinístico como portão de refatoração. Não existe no v1 - precisa ser escrito.
- **aula 19** - conteúdo NOVO exigido pelo plano v2: contador_de_instancias<T> por CRTP. Não existe no v1 - precisa ser escrito.
- **aula 20** - conteúdo NOVO exigido pelo plano v2: std::filesystem no carregamento de mapa. Não existe no v1 - precisa ser escrito.
- **aula 21** - conteúdo NOVO exigido pelo plano v2: lambdas como conteúdo de capítulo. Não existe no v1 - precisa ser escrito.
- **aula 21** - conteúdo NOVO exigido pelo plano v2: std::clamp. Não existe no v1 - precisa ser escrito.

## `lab` - 12

- **aula 02** - LAB-01 “Ambiente, CMake com FetchContent e portões de compilação” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 03** - LAB-02 “C++17 na prática: string_view, ligações estruturadas e [[nodiscard]]” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 04** - LAB-03 “Git como registro de decisão” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 07** - LAB-04 “UML leve do Deriva; vetor2 e celula, e o contador `vivos`” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 08** - LAB-05 “Ciclo de vida e terminal_bruto: RAII com consequência” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 11** - LAB-06 “O destrutor não virtual, acusado pelo contador `vivos`” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 13** - LAB-07 “Posse: unique_ptr, shared_ptr e o ciclo que vaza” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 14** - LAB-08 “Cópia versus movimento em grade, e o objeto de origem depois” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 16** - LAB-09 “Catch2 e o replay determinístico como especificação” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 19** - LAB-10 “CRTP e contador_de_instancias<T>: generalizar o próprio detector” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 20** - LAB-11 “Erros no carregamento de mapa: exceções, optional e variant” - esqueleto, solução de referência e portão precisam ser escritos.
- **aula 24** - LAB-12 “Refatorar o `mundo` sob SOLID sem mudar um byte da saída” - esqueleto, solução de referência e portão precisam ser escritos.

## `exercicios` - 7

- **aula 04** - 4 exercícios vêm de `unidade-3/aula27-qt-llms`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 08** - 4 exercícios vêm de `unidade-2/aula10-raii-rule-of-five`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 09** - 4 exercícios vêm de `unidade-2/aula10-raii-rule-of-five`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 12** - 4 exercícios vêm de `unidade-2/aula11-smart-pointers`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 13** - 4 exercícios vêm de `unidade-2/aula11-smart-pointers`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 14** - 4 exercícios vêm de `unidade-2/aula10-raii-rule-of-five`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.
- **aula 26** - 4 exercícios vêm de `unidade-3/aula27-qt-llms`, que se parte. Foram anexados aqui INTEIROS e marcados; a divisão entre as fatias é decisão de conteúdo.

## `fatia` - 7

- **aula 08** - o slide “LLMs neste Tópico” de `unidade-2/aula10-raii-rule-of-five` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 09** - o slide “Regra dos Três e Cinco” de `unidade-2/aula10-raii-rule-of-five` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 09** - o slide “LLMs neste Tópico” de `unidade-2/aula10-raii-rule-of-five` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 12** - o slide “LLMs neste Tópico” de `unidade-2/aula11-smart-pointers` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 13** - o slide “LLMs neste Tópico” de `unidade-2/aula11-smart-pointers` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 14** - o slide “Regra dos Três e Cinco” de `unidade-2/aula10-raii-rule-of-five` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.
- **aula 14** - o slide “LLMs neste Tópico” de `unidade-2/aula10-raii-rule-of-five` foi para MAIS DE UMA aula: a divisão do plano cai dentro dele. Separe a prosa parágrafo por parágrafo - é a migração de risco 1/3.

## `bruto` - 5

- **aula 06** - bloco <div class=uml-box> copiado sem interpretação - conferir o tipo.
- **aula 06** - bloco <div class=uml-box> copiado sem interpretação - conferir o tipo.
- **aula 07** - bloco <div class=uml-box> copiado sem interpretação - conferir o tipo.
- **aula 10** - bloco <div class=uml-box> copiado sem interpretação - conferir o tipo.
- **aula 17** - bloco <div class=uml-box> copiado sem interpretação - conferir o tipo.

## `caca-bug` - 3

- **aula 09** - CAÇA AO BUG 1: cópia rasa em `grade` - semana 5. A variante quebrada e o roteiro da caça precisam existir no repositório do Deriva.
- **aula 11** - CAÇA AO BUG 2: destrutor não virtual - semana 9. A variante quebrada e o roteiro da caça precisam existir no repositório do Deriva.
- **aula 24** - CAÇA AO BUG 3: refatoração que mudou a saída - semana 13. A variante quebrada e o roteiro da caça precisam existir no repositório do Deriva.
