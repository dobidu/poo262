# Anexo B - Referência rápida de C++17

*Novo. Tabela de consulta para prova e laboratório. Mesmo conteúdo da página do site - uma fonte, dois meios.*

Este anexo existe por uma razão aferida no material anterior, e vale registrá-la, porque ela é o argumento de por que a tabela merece páginas. O livro v1 **se declarava C++17 em doze lugares** e não tinha uma única ocorrência de `std::string_view`, de ligações estruturadas, de `[[nodiscard]]`, de `std::forward`, de `std::filesystem` ou de `std::tuple`, ao mesmo tempo que ensinava Concepts e Ranges, que são C++20, como capítulo próprio.

O padrão declarado, portanto, não era o padrão ensinado, e a distorção tinha as duas pontas: faltava o que o portão exige e sobrava o que o portão recusa. A correção foi distribuir as construções que faltavam por cerca de dez capítulos, rebaixar Concepts e Ranges ao **Anexo A**, e escrever esta tabela, que é a lista do que passou a ser exigido.

A tabela é de consulta, e as quatro colunas respondem a quatro perguntas. A primeira diz **o que** é a construção. A segunda diz **onde** ela entra, para que a consulta devolva também o lugar do material em que o mecanismo é desenvolvido, e não apenas a sintaxe. A terceira dá a **forma**, isto é a notação mínima que faz reconhecer a construção ao vê-la. A quarta é a que mais paga em prova: **a armadilha** que costuma acompanhar cada uma, escrita como a frase que você gostaria de ter lido antes de errar.

Uma observação de escopo, para que a terceira coluna não seja mal lida. Ela traz notação de referência rápida, e não trecho de programa: `auto [a, b] = par;` é a forma da ligação estruturada, sem contexto, sem inclusão e sem tipo declarado. Todo trecho de código deste livro que se pretende compilável vem extraído de `exemplos/deriva/`, e é sempre acompanhado do arquivo e da linha de onde saiu; nada aqui tem essa pretensão.

## B.1 As quinze construções

| construção | cap. | forma | o que costuma dar errado |
|---|---|---|---|
| `std::string_view` | 3 | `void f(std::string_view s)` | não possui os bytes que enxerga, e um `string_view` guardado além da vida da `string` de origem fica pendurado |
| `ligações estruturadas` | 3 | `for (auto& [pos, cel] : mapa)` | sem o `&` a ligação copia o elemento; use `const auto&` quando o laço apenas lê |
| `[[nodiscard]]` | 3, 7 | `[[nodiscard]] bool carregar(...)` | vale no que retorna status ou recurso, e o warning que ele provoca é o objetivo |
| `[[maybe_unused]]` | 3 | `[[maybe_unused]] int n = f();` | para o parâmetro que só é usado dentro de `assert` ou em um dos ramos compilados |
| `if constexpr` | 19 | `if constexpr (std::is_integral_v<T>)` | poda o ramo em tempo de compilação, e o ramo podado nem precisa ser válido para o `T` em questão |
| `std::optional` | 20 | `std::optional<mapa> carregar(...)` | modela ausência, e não falha; para reportar erro, use exceção ou `variant` |
| `std::variant` | 20 | `std::variant<mapa, erro>` | soma de tipos fechada, consultada com `std::visit`; o acesso por `get` com o tipo errado lança |
| `std::filesystem` | 20 | `fs::exists(caminho)` | verificar a existência e abrir são duas operações, e a corrida entre elas é real: abra e trate a falha |
| `std::clamp` | 21 | `std::clamp(x, 0, largura - 1)` | substitui o par `min`/`max` aninhado, porém devolve referência - não o alimente com temporário |
| `lambdas` | 21, 25 | `[&](const auto& e) { return e.vivo(); }` | Strategy sem herança; a captura por referência só é segura enquanto vive o escopo capturado |
| `std::forward` | 14 | `template<class T> void add(T&& x)` | encaminhamento perfeito; `T&&` em parâmetro de template dedutível é referência universal, e não referência a rvalue |
| `CTAD` | 15 | `std::pair p{1, 2.0};` | dedução a partir do construtor, o que dispensa `make_pair`; agregado próprio pode exigir guia de dedução |
| `fold expressions` | 19 | `return (... + args);` | variádico sem recursão; o pacote vazio exige valor inicial ou operador com identidade definida |
| `inline variables` | 7 | `inline static int vivos = 0;` | membro estático definido no próprio cabeçalho, sem a definição avulsa no `.cpp` que o C++14 exigia |
| `std::byte` | 7 | `std::byte b{0xFF};` | não é aritmético nem caractere, e a conversão para inteiro passa por `std::to_integer` |

## B.2 Como usar isto em prova

A prova desta disciplina é escrita, em papel, e não cobra sintaxe de memória. O que ela cobra, e onde esta tabela ajuda, é a quarta coluna: dado um trecho, dizer o que vai acontecer e por quê.

Três padrões de questão se repetem, e os três se preparam relendo a coluna da armadilha. O primeiro é o de **tempo de vida**: um `string_view`, uma view de ranges ou uma lambda com captura por referência que sobrevive ao que enxergava. Os três casos são o mesmo mecanismo, e reconhecer isso vale mais que memorizar os três.

O segundo é o de **momento da decisão**: o que é resolvido em compilação e o que é resolvido em execução. `if constexpr`, `static_assert` e CTAD estão do lado da compilação; `virtual`, `dynamic_cast` e `std::visit` estão do lado da execução. A pergunta "quando isto é decidido?" resolve a maioria das questões de despacho.

O terceiro é o de **quem tem a posse**: `optional` não possui o que não tem, `string_view` não possui os bytes, `unique_ptr` possui com exclusividade, e ponteiro cru não diz nada. É a pergunta central da disciplina, e ela reaparece em cada linha desta tabela que trate de referência ou de ponteiro.

## B.3 O que está fora, de propósito

Não está aqui o que é C++20 ou posterior, e a lista do que ficou de fora é curta e vale saber: Concepts e Ranges estão no Anexo A, rotulados; `std::expected` é C++23 e aparece como pergunta de pesquisa no fim do Cap. 20; módulos, corrotinas e `std::format` não aparecem em lugar nenhum. Nenhuma dessas construções passa pelo portão da disciplina, que compila com `-std=c++17` e `CXX_EXTENSIONS OFF`.

Também não estão aqui as construções de C++11 e C++14 que a disciplina usa sem cerimônia por serem anteriores ao padrão-alvo, tais como `auto`, `nullptr`, `override`, `final`, `noexcept`, os ponteiros inteligentes, `std::move` e a inicialização uniforme. Elas são pressuposto, e estão nos Caps. 3, 12, 13 e 14; esta tabela é o **delta** do C++17 sobre o que já se usava.

Uma ponta solta, que vale amarrar. A prosa de abertura cita `std::tuple` entre as construções de que o v1 não tinha uma ocorrência, e ele não tem linha própria na tabela. É deliberado: no Deriva o que se usa é `std::pair`, e ele entra por duas portas que **estão** na tabela, que são CTAD, no Cap. 15, e as ligações estruturadas, no Cap. 3 - a tabela de comandos de `src/main.cpp` é um array de pares percorrido com `for (const auto& [nome, delta] : tabela)`. `std::tuple` de três ou mais elementos não aparece em entrega nenhuma, e dar-lhe linha própria seria exibir como exigência o que é apenas reconhecível.
