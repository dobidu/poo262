# Prefácio

Esta apostila cobre integralmente o plano de ensino de Programação Orientada a Objetos em C++, no semestre 2026.2. Ela é o resultado da fusão e da expansão dos Volumes I e II utilizados em semestres anteriores, com material novo em todos os tópicos que o inventário de conteúdo apontou como ausentes ou rasos.

O livro tem **26 capítulos e 3 anexos**, e a correspondência com o curso é estrita: **Aula N = Capítulo N**. Onde o curso divide um tema em dois encontros, o livro tem dois capítulos; onde funde, o livro funde. A ordem é a do curso, e não a de uma exposição sistemática do C++, porque o que se pretende é que você encontre em casa exatamente o que viu projetado em aula. Concepts e Ranges, que eram um capítulo próprio, passaram ao Anexo A: deixaram de ser aula, e o conteúdo mudou de estatuto em vez de ser descartado.

A disciplina é organizada em torno de um projeto fio condutor chamado **Deriva**, um *roguelike* de terminal por turnos em que uma sonda de inspeção percorre uma estação orbital abandonada, através do console. O projeto evolui ao longo das três unidades: da posição e da célula da grade (`vetor2`, `celula`, `grade`, `mapa`) na Unidade I, passa pela hierarquia de entidades (`entidade` → `sonda`, `drone`, `item`) com posse por ponteiros inteligentes e testes na Unidade II, e chega a genericidade, refatoração sob SOLID e um segundo front-end em Qt na Unidade III. Cada capítulo mostra como as decisões de projeto discutidas afetam o Deriva, e cada exercício o faz crescer.

A escolha do Deriva tem uma razão que atravessa o livro inteiro: nele **RAII tem consequência física**. A classe `terminal_bruto` põe o terminal em modo bruto no construtor e o restaura no destrutor; sem o destrutor, o terminal fica sem eco e sem Enter *depois* que o programa sai, e o conserto é digitar `reset` às cegas. Vazamento de memória é abstrato, porque o sistema operacional devolve tudo quando o processo morre; vazamento do modo do terminal, não.

**O padrão-alvo é C++17**, e ele é o teto, não o piso: o laboratório compila com `g++ -std=c++17` e `CXX_EXTENSIONS OFF`, de forma que código que só compila com `-std=gnu++17` não conta como C++17. Onde algo de C++20 aparece, ele vem rotulado, e o Anexo A é o lugar em que se apresenta como reconhecimento de API, sem ser base de exemplo nem de entrega.

As máquinas do laboratório não têm sanitizer nem Valgrind, e neste livro isso é conteúdo, e não limitação. No lugar do detector automático estão três técnicas que você mesmo constrói, e que aparecem antes de serem exigidas: o **contador de instâncias vivas** (Cap. 7), a **instrumentação de ciclo de vida** (Cap. 8) e o **`gdb` com ponto de parada em destrutor** (Caps. 2, 8 e 11). Os sanitizers aparecem como ferramenta de confirmação no Cap. 2, e não como critério de aceitação.

Todo trecho de código deste livro é extraído de `exemplos/deriva/`, que compila sem um aviso sob `-Wall -Wextra -Wpedantic` e passa o portão `make verifica`; nenhum foi digitado no texto. Os números que a prosa afirma - tamanhos de estrutura, contagens de teste, bytes presos por um ciclo de `shared_ptr` - são medidos nesse código, e não estimados. Se o código mudar de forma a desmentir um número, o build falha antes de o livro sair errado.

Convenções adotadas:

- **Código:** `snake_case` para identificadores, identificadores e comentários em português, C++17 como padrão base, com o que for de C++20 explicitamente rotulado.
- **Caixas:** ▲ ATENÇÃO (situação em que o compilador não avisa), ✓ DICA (o idioma que a disciplina cobra), ◇ LLM (uso crítico de assistente), ▸ DERIVA (a ligação com o sistema-base).
- **UML:** diagramas de classes e de sequência em Mermaid, no Cap. 6.
- **Exercícios:** cada capítulo termina com exercícios graduados, do conceitual ao prático, e a maior parte deles é uma peça a mais no Deriva.

O material pressupõe familiaridade com programação em C (structs, ponteiros, funções) e noções básicas de Python. Não pressupõe experiência anterior com C++ nem com orientação a objetos.

*Prof. Carlos Eduardo Coelho Freire Batista*

João Pessoa, Setembro de 2026
