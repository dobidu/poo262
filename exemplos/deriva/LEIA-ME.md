# Deriva - v2.7

Roguelike de terminal por turnos. Uma sonda de inspeção percorre uma estação
orbital abandonada, através do console. É o sistema-base da disciplina de POO
(UFPB/CI): cada aula entrega uma versão que compila, e onde o erro ensina mais
que o acerto, uma variante deliberadamente quebrada.

**Alvo: C++17.** `CXX_EXTENSIONS OFF` - código que só compila com
`-std=gnu++17` não é C++17.

## Rodar

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel

./build/deriva --render                        # desenha o setor
./build/deriva --replay roteiro.txt --semente 7 # o roteiro, passo por passo
./build/deriva --replay roteiro.txt --traco     # + o traço de ciclo de vida
./build/deriva --leiaute                       # o sizeof de cada estrutura
make verifica                                  # as quatro condições do portão
```

## O portão: `make verifica`

```
  (1/4) warning     zero aviso com -Wall -Wextra -Wpedantic -Wconversion …
  (2/4) ctest       188 testes verdes
  (3/4) replay      despejo idêntico byte a byte (semente 7)
  (4/4) contadores  vivos=0 - nenhum destrutor deixou de rodar
```

Nenhuma das quatro depende de sanitizer, e isso é deliberado: o laboratório
não os tem. O lugar do ASan é a Aula 02, como ferramenta - `make sanitizers`
- , não como critério de aceitação.

O que substitui é o bloco de três técnicas sem dependência externa:

| técnica | onde entra | o que acusa |
|---|---|---|
| contador de instâncias vivas | Aula 07, `include/deriva/contador.hpp` | destrutor que não rodou |
| instrumentação de ciclo de vida | Aula 08, `src/instrumento.cpp` | ordem errada de construção/destruição |
| `gdb` com ponto de parada em destrutor | Aulas 08 e 11, `make gdb-dtor` | qual destrutor roda, e de onde é chamado |

## O que existe, aula por aula

**A trilha inteira está escrita**, da v0.0 à v2.7.

| unidade | versões | o que entra |
|---|---|---|
| I | v0.0 → v0.3 | CMake e portões · `vetor2`, `celula`, o contador `vivos` · `grade`, `terminal_bruto`, instrumentação · `mapa`, carregamento, primeiro render |
| II | v1.0 → v1.8 | hierarquia `entidade` com destrutor virtual · `mundo` com `vector<unique_ptr<entidade>>` · grafo da estação com `shared_ptr` e `weak_ptr` · movimento e a regra dos cinco · operadores · campo de visão puro e replay · o diamante · inspetor por RTTI |
| III | v2.0 → v2.7 | `grade<T>` e `contador_de_instancias<T>` por CRTP · hierarquia de erros com `optional`, `variant` e exceção · inventário com STL, lambdas e `clamp` · fila entre threads · serialização versionada · refatoração SOLID com Command, Observer, Factory, Strategy e Composite · segundo front-end em Qt |

Fora da trilha, três diretórios que existem para o material e não para o jogo:
`comparativo/` (o par C contra C++ da Aula 01), `revisao_ia/` (o código gerado
com três defeitos plantados, da Aula 04) e `tipos/` (os eixos de sistema de
tipos da Aula 05). Mais `laboratorios/`, com os doze preparatórios.

A tabela versão por versão, com as variantes quebradas, está em
`../../poo/trilha.html` e em `conteudo/mapa.py`.

## Variantes deliberadamente quebradas

Não são erro do material: são o melhor recurso pedagógico que o sistema-base
anterior tinha, e foram preservadas.

- **`variantes/v0.2-quebrada/`** - `terminal_bruto` sem destrutor. RAII com
  consequência física: o terminal fica inutilizável **depois** que o programa
  sai. Rode com `< /dev/null` primeiro.
- **`variantes/v0.3-quebrada/`** - cópia rasa em `grade`. Caça ao bug 1,
  semana 5. Destrutor declarado, cópia esquecida; `-Wall -Wextra -Wpedantic`
  não emite uma palavra.

Cada uma tem `LEIA-ME.md` com o roteiro de observação, na ordem: sem
ferramenta, com o contador, com o alocador, com o ASan, com o compilador.

## Números que o material exibe, e que o compilador afirma

`static_assert` em `celula.hpp` e `leiaute.hpp` mais os testes em
`testes/test_celula.cpp` e `testes/test_leiaute.cpp` fixam:

| estrutura | bytes | por quê |
|---|---|---|
| `celula` | 12 | agrupada por tamanho |
| `celula_ingenua` | 16 | a ordem "natural" custa 4 B por célula |
| `leiaute::entidade_simples` | 8 | só a posição, sem vtable |
| `leiaute::entidade` | 16 | + 8 do `vptr` |
| `leiaute::drone_com_carga` | 24 | o custo do `vptr` se soma, não desaparece |
| `medida::no` | 64 | `std::string` 32 + `shared_ptr` 16 + `weak_ptr` 16 |
| ciclo de `shared_ptr` | 160 presos | 2 × (64 do nó + 16 do bloco de controle) |
| `medida::patrulha_duplicada` | 40 | duas bases de 16, mais `rota` |
| `medida::patrulha_unica` | 48 | uma base, e mais um ponteiro por ramo virtual |
| `medida::patrulha_composta` | 56 | nenhum diamante, e o maior dos três |
| `mapa::de_texto` | 2 construções | com **e sem** construtor de movimento |

E um número que **não** entra em `medidas.py`, de propósito: quantos
incrementos a corrida de dados perde. Corrida é comportamento indefinido, o
resultado varia a cada execução, e travar um valor variável num portão que
exige igualdade faria o build falhar sozinho.

Medido em `testes/test_corrida.cpp`, duas threads somando 100.000 cada, dez
execuções em g++ 13.3 nesta máquina, e cinco rodadas da suíte deram **4, 9, 9,
8 e 7 execuções sem perda**, de dez, com a pior perda chegando a **63.116 de
200.000**. É essa distribuição que é a lição, e não a média: um defeito que
não aparece na maioria das tentativas é pior que um que
sempre aparece, porque o teste verde não prova nada. Rode
`./build/testes "*corrida perde*"` para ver os seus números.

O vazamento do ciclo não dá para travar em `static_assert`, porque o tamanho do
bloco de controle é escolha da implementação. Ele é **medido**, em
`testes/test_posse.cpp`, por um alocador que conta o que o `shared_ptr` pede -
e `./build/testes "*copiar*"` imprime o número para quem for atualizar o
material. O material dizia 96 bytes, herdado de uma estimativa do documento de
design; o medido nesta libstdc++ é 160.

Uma armadilha que custou depuração e virou comentário no cabeçalho:
`std::allocate_shared` **não** usa o alocador que você passa, ele o rebinda
para o tipo interno do bloco de controle. Contador `inline static` dentro do
template conta na instanciação errada, e a primeira versão da medida deu zero
byte vazado por isso.

Se o leiaute mudar, o Deriva **não compila** - e o interativo do site não
passa a exibir número errado em silêncio. É por isso que os trechos de código
do material são extraídos daqui por `build/extrair_codigo.py`, e não digitados
lá.

## Números do material que ainda NÃO têm lastro aqui

Um só, e está declarado em vez de exibido: a contagem de linhas de `mundo.cpp`
antes e depois da refatoração da v2.6 (o interativo trazia 612 e 168, que eram
estimativa). A v2.6 é da Unidade III e não existe em código, então a linha foi
**removida** do painel de estado em vez de mantida com número inventado. As 6 e
as 2 dependências de saída do nó central, que são o que a peça de fato ensina,
continuam lá: são estruturais e vêm do desenho, não de medição.

## O que ainda não está aqui

Três itens que esta seção listava saíram dela porque foram feitos, e vale
dizer o que eram: o alvo de C++20 do Anexo A ("não escrito"), que hoje compila
com zero aviso e tem o seu teste passando sob `-DDERIVA_COM_CPP20=ON`; o
`sizeof(unique_ptr)` com deletor com estado ("nenhum teste mede"), medido em
`testes/test_posse.cpp`; e os defeitos de memória para o sanitizer, que agora
existem em `sanitizers/defeitos_de_memoria.cpp`. Lista de pendência que não
encolhe quando o trabalho é feito deixa de ser lista e passa a ser ruído.

O que resta:

- **FTXUI e Qt**, os dois desligados por padrão e fixos em versão:
  `-DDERIVA_COM_FTXUI=ON` e `-DDERIVA_COM_QT=ON`. O laboratório não os tem, e a
  Aula 26 é demonstração do docente. O render atual é `std::cout` **através de
  `i_apresentacao`**, e é essa interface que faz o esqueleto Qt existir sem o
  núcleo mudar uma linha.
- **O alvo de C++20 fica fora do portão**, e isso é escolha e não falta:
  `make verifica` não o compila, porque o padrão-alvo da disciplina é C++17 e
  um portão que exigisse C++20 exigiria C++20 do laboratório. Ele vive em
  `c20/`, com `add_test(NAME anexo-a-cpp20)` sob a opção, e o Anexo A do livro
  diz isso no lugar de fingir que passa.
- **O contador de teste por versão da trilha** cobre 129 dos 176 casos. Os
  outros 47 medem material de aula - o par C contra C++ da Aula 01, os eixos
  de tipo da Aula 05, o código gerado da Aula 04, as relações da UML da Aula
  06, e as medidas de leiaute, posse, movimento e corrida. A separação está em
  `conteudo/medidas.py`, em `testes_por_versao` e `testes_por_aula`, e cada
  arquivo de `testes/` declara na primeira linha a qual dos dois pertence.
- **A v0.0 e a v1.1 não têm teste próprio.** A v0.0 é o esqueleto, e o teste
  de fumaça dela é o próprio `make verifica` compilando; a v1.1 acrescenta
  `virtual` e o destrutor virtual a uma hierarquia cujos testes vivem em
  `testes/test_entidade.cpp`, declarado v1.0. Nenhuma das duas é lacuna de
  cobertura, e a página da trilha diz "nenhum teste próprio" em vez de
  inventar um número.
