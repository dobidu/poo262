# Anexo C - O Deriva: as 20 versões

*Novo. Cada versão com o capítulo que a introduz e as variantes deliberadamente quebradas. Mesmo conteúdo da trilha do site - uma fonte, dois meios.*

## C.1 Por que a trilha existe

O Deriva é um roguelike de terminal: uma sonda de inspeção percorre uma estação orbital abandonada, através do console. Ele é o artefato que atravessa a disciplina inteira, e a tabela adiante é a forma dessa travessia: **cada aula entrega uma versão que compila**, e a versão seguinte parte dela.

Três decisões estão embutidas nesse formato, e vale nomeá-las, porque nenhuma é óbvia.

A primeira é que **não há projeto final**. Não existe o momento em que o estudante recebe um enunciado grande e monta tudo de uma vez; existe uma sequência de vinte incrementos, cada um pequeno o bastante para caber num encontro e grande o bastante para acrescentar um conceito. O que isso resolve é o problema de quem não consegue começar: o começo é sempre a versão anterior, que compila.

A segunda é que **o conceito chega depois da necessidade**. A ordem da tabela não é a ordem do índice da linguagem, é a ordem em que o sistema pede as coisas. Ponteiro inteligente entra na v1.2 porque a v1.0 já tem uma hierarquia e alguém precisa possuir as entidades; template entra na v2.0 porque o contador já foi escrito à mão três vezes; serialização entra na v2.5 porque já existe partida a salvar. Conceito que chega antes de a necessidade aparecer é solução para um problema que o estudante não teve, e a §19.6 trata disso longamente.

A terceira é que **a versão anterior continua rodando**. Nenhum incremento quebra o anterior, e é o portão `make verifica` que garante isso, com as suas quatro condições: zero aviso, testes verdes, replay idêntico byte a byte, e o contador de instâncias vivas fechando em zero.

Uma nota de contagem, para que a tabela não pareça errada. Ela tem vinte e uma linhas: as **vinte** versões da trilha obrigatória, da v0.0 à v2.7, mais a **v2.1**, que é o alvo opcional de C++20 do Anexo A. A v2.1 não é pré-requisito de nada, e a trilha salta da v2.0 para a v2.2 sem ela.

E uma nota de estado, porque a tabela é promessa até que alguém a confira: em código, hoje, o repositório de exemplos está na **v2.7**, com o alvo opcional de C++20 ao lado, e as **quatro** variantes deliberadamente quebradas da coluna da direita existem, cada uma com o seu `LEIA-ME.md`. O que a tabela descreve é o que compila, e não o que se pretende compilar. Onde uma versão entrega menos do que a linha promete, o capítulo correspondente diz o que ficou de fora e por quê, em lugar de calar.

## C.2 A tabela

| versão | capítulo | entrega | conceitos | variante quebrada |
|---|---|---|---|---|
| `v0.0` | 2 | esqueleto que compila: CMake, FetchContent, main vazio | CMake, FetchContent, FTXUI v5.0.0 e Catch2 como SYSTEM, make verifica |  -  |
| `v0.1` | 7 | vetor2, celula e o contador `vivos` | encapsulamento, const-correctness, static, this, [[nodiscard]] |  -  |
| `v0.2` | 8 | grade e terminal_bruto | construtores, destrutor, lista de inicialização, RAII, instrumentação de ciclo de vida | v0.2-quebrada - terminal_bruto sem destrutor |
| `v0.3` | 9 | mapa, carregamento de arquivo e o PRIMEIRO render | composição, regra do zero e do três, std::optional, std::filesystem, string_view | v0.3-quebrada - cópia rasa em `grade` |
| `v1.0` | 10 | hierarquia entidade → sonda / drone / item | herança pública, override, final, subobjeto base |  -  |
| `v1.1` | 11 | desenhar() e agir() virtuais; destrutor virtual | funções virtuais, classe abstrata, vptr e vtable, destrutor virtual | v1.1-quebrada - destrutor não virtual na base |
| `v1.2` | 12 | mundo com vector<unique_ptr<entidade>> | posse exclusiva, unique_ptr, make_unique, ponteiro cru como contraexemplo |  -  |
| `v1.3` | 13 | grafo de conexões da estação com shared_ptr | posse compartilhada, shared_ptr, weak_ptr, contagem de referências, o ciclo que vaza |  -  |
| `v1.4` | 14 | movimento em grade e mapa | rvalue refs, std::move, regra dos cinco, noexcept, std::forward |  -  |
| `v1.5` | 15 | operadores de vetor2 e mapa[pos] | sobrecarga, funções livres, operator<<, operator[] const e não-const |  -  |
| `v1.6` | 16 | testes de FOV e caminho + replay determinístico | Catch2, semente fixa, roteiro gravado, despejo idêntico byte a byte |  -  |
| `v1.7` | 17 | sonda_reparadora: o diamante | herança múltipla, interface pura, herança virtual, ordem de construção |  -  |
| `v1.8` | 18 | inspetor de entidade no console | RTTI, dynamic_cast, typeid, quando NÃO usar |  -  |
| `v2.0` | 19 | grade<T> genérica e contador_de_instancias<T> | templates, if constexpr, static_assert, CRTP |  -  |
| `v2.1` *(opcional, C++20)* | Anexo A | restrições em grade<T> por concept | Concepts e Ranges - fora do padrão-alvo, alvo de compilação separado |  -  |
| `v2.2` | 20 | erros de carregamento de mapa | exceções, garantias, std::optional, std::variant, std::filesystem |  -  |
| `v2.3` | 21 | FOV e inventário com algoritmos | STL, lambdas, std::clamp, std::size |  -  |
| `v2.4` | 22 | thread de entrada separada do render | std::thread, std::mutex, corrida de dados - panorâmica |  -  |
| `v2.5` | 23 | salvar e carregar partida | serialização, versionamento de formato, compatibilidade regressiva |  -  |
| `v2.6` | 24, 25 | refatoração do mundo + os seis padrões | SOLID; Command, State, Observer, Factory, Strategy (lambda), Composite | v2.6-antes - `mundo` como god class |
| `v2.7` | 26 | front-end Qt sobre o mesmo núcleo | QObject, signals/slots, separação domínio/apresentação |  -  |

## C.3 A variante deliberadamente quebrada

A coluna da direita traz o recurso pedagógico mais valioso que o sistema-base anterior tinha, e que foi preservado por inteiro nesta migração: a **variante deliberadamente quebrada**.

Ela não é erro do material. É uma cópia da versão, com um defeito plantado, plausível, do tipo que se comete de verdade, e com uma propriedade que decide tudo: **o compilador não avisa.** As quatro variantes passam por `-Wall -Wextra -Wpedantic` sem uma palavra, porque em nenhuma delas a linguagem está fazendo algo diferente do que foi pedida. É esse silêncio que as torna úteis: elas ensinam que o portão de compilação é necessário e não é suficiente, e que a categoria de defeito que esta disciplina trata é justamente a que atravessa o portão.

::: {.callout .warn}

A variante quebrada é para ser **rodada**, e não lida. Ler o código de `variantes/v0.2-quebrada/` e concluir "falta o destrutor" ensina a reconhecer a ausência num arquivo de trinta linhas, que não é a habilidade cobrada. Rodar, ver o terminal parar de ecoar depois que o programa sai, e só então procurar a causa, é o que ensina. Cada variante tem `LEIA-ME.md` com o roteiro de observação na ordem certa: sem ferramenta, com o contador, com o alocador, com o ASan, com o compilador. E rode a v0.2 com `< /dev/null` na primeira vez, para não precisar digitar `reset` às cegas.

:::

A variante da v0.2 tem estatuto especial, e não é caça ao bug: ela é demonstração de aula. `terminal_bruto` sem destrutor põe o terminal em modo bruto e não o restaura, e a consequência acontece **depois** que o programa sai, no terminal do estudante, que fica sem eco e sem Enter. É a melhor demonstração de RAII que a disciplina tem, e não é metáfora.

## C.4 As três caças ao bug

Uma vez por unidade, em dupla, cada equipe recebe uma versão do Deriva plausível e errada. A ordem de trabalho é cobrada, e é sempre a mesma: **reproduzir** a falha; **explicar em uma frase antes de tocar no código**; **corrigir**; **provar** a correção. O instrumento é a rubrica de revisão do Cap. 4, e o item dela que mais pesa é o que distingue causa de sintoma.

**Caça ao bug 1, semana 5, `v0.3-quebrada`: a cópia rasa em `grade`.** A grade guarda `celula*` cru, declara destrutor e esquece a cópia, e portanto duas grades passam a apontar para o mesmo buffer. Os dois objetos são construídos e destruídos corretamente, e o segundo destrutor libera memória já liberada. O que a torna instrutiva é o que o contador faz: `vivos` **fecha em zero**, porque nada de errado aconteceu com objetos, e o defeito é de recurso. É o limite do instrumento, ensinado pelo próprio instrumento, e é assunto do Cap. 9. Ela acontece no mesmo encontro da Prova 1, e o Cap. 9 registra a consequência disso.

**Caça ao bug 2, semana 9, `v1.1-quebrada`: o destrutor não virtual na base.** Deletar uma `sonda` através de `entidade*` chama o destrutor da base e não o da derivada. Aqui o contador funciona, e é o oposto do caso anterior: `vivos` nunca volta a zero, e o `gdb` com ponto de parada em destrutor mostra que `~sonda()` nunca roda. As duas ferramentas do Cap. 2 se combinam, e o Cap. 11 conduz.

**Caça ao bug 3, semana 13, `v2.6-antes`: a refatoração que mudou a saída.** A mais difícil das três, porque não há travamento, não há vazamento, e o contador fecha em zero. O programa roda e parece certo; o replay acusa uma linha diferente no despejo. O oráculo é o do Cap. 16, a lição é a do Cap. 24, e ela é uma frase: refatoração correta é a que não muda a saída.

Repare na progressão que as três desenham, porque ela é o argumento de haver três e não uma. Na primeira, o contador **mente**: fecha em zero e a memória foi liberada duas vezes, porque ele conta objetos e não recursos. Na segunda, o contador **acusa**: não fecha em zero, e o `gdb` com ponto de parada em destrutor mostra qual destrutor não rodou. Na terceira, o contador **cala**: fecha em zero, os testes passam, e o único instrumento que sobra é a comparação byte a byte com a execução anterior. Cada caça retira uma ferramenta, e a última retira todas menos a que o Cap. 16 construiu com dezessete semanas de antecedência.
