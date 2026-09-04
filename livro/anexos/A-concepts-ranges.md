# Anexo A - Concepts e Ranges (C++20)

*Vem do Cap. 20 do v1, íntegro · rotulado C++20 · Deriva v2.1 (opcional)*

Este anexo é o Cap. 20 do v1, íntegro. **O que mudou não foi o conteúdo, foi o estatuto.**

O v1 tratava Concepts e Ranges como aula, com duas horas, exercícios e lugar na sequência. O plano v2 desfez isso por um motivo aferido: o material se declarava C++17 em doze lugares e ensinava, como capítulo próprio, duas construções que são C++20, ao mesmo tempo que não tinha uma única ocorrência de `std::string_view`, de ligações estruturadas, de `[[nodiscard]]`, de `std::forward`, de `std::filesystem` ou de `std::tuple`. O tempo de aula gasto no padrão seguinte era tempo que faltava no padrão-alvo, e a correção foi trocar o capítulo por vinte minutos dentro do **Cap. 19**, como reconhecimento de API, com o conteúdo integral preservado aqui.

Três consequências valem estar explícitas, porque elas definem como este anexo se lê.

**Nada do material obrigatório depende deste anexo.** Nenhum exemplo, nenhum exercício, nenhum laboratório e nenhum item de prova o referenciam como pré-requisito. Ele pode ser saltado inteiro sem que uma linha do resto do livro deixe de fazer sentido.

**O código daqui compila em alvo separado, e só nele.** A v2.1 do Deriva é `exemplos/deriva/c20/`, atrás da opção `-DDERIVA_COM_CPP20=ON`, e o alvo `deriva_c20` é o único do repositório com `CXX_STANDARD 20`: o núcleo continua em C++17, e é essa separação que faz o rebaixamento ser real em vez de declarado. A trilha do Anexo C registra a v2.1 como opcional, e as versões seguintes partem da v2.0, e não dela. Leia com essa ressalva a linha de abertura da seção de código no fim deste anexo: ela é a mesma em todos os capítulos e fala de `-std=c++17`, porque é gerada uma vez para o livro inteiro; aqui, e só aqui, os trechos vêm do alvo de C++20 e ficam fora de `make verifica`.

**O padrão-alvo da disciplina segue sendo C++17.** O que está aqui serve para você reconhecer a construção quando a encontrar em código alheio, e para saber o que a linguagem fez depois com os problemas que o Cap. 19 resolveu com `static_assert` e `if constexpr`.

::: {.objetivos}

- Usar concepts para restringir parâmetros de template com mensagens de erro legíveis. **(C++20)**
- Definir concepts próprios com `requires`. **(C++20)**
- Usar ranges e views para expressão funcional sobre sequências. **(C++20)**
- Reconhecer, em código alheio, que a construção é de C++20 e não do padrão-alvo.

:::

::: {.callout .warn}

Nada deste anexo entra em prova, em laboratório ou em entrega, e o motivo não é de gosto. O portão da disciplina compila com `-std=c++17` e `CXX_EXTENSIONS OFF`, e código que só compila com `-std=c++20` **falha o portão**. Se você usar concept ou range numa entrega, ela não passa, mesmo estando correta. O lugar de exercitar o que está aqui é o alvo opcional, e ele é opcional de verdade: a v2.1 do Deriva não é pré-requisito de nenhuma versão posterior, e a trilha salta da v2.0 para a v2.2 sem ela.

:::

## A.1 O Problema dos Templates sem Restrições **(C++20)**

Templates de C++17 aceitam qualquer tipo - erros de tipo só são detectados ao tentar usar um tipo incompatível, gerando mensagens de erro dificilmente legíveis. Concepts resolvem isso declarando explicitamente o que um tipo deve suportar.

O Cap. 19 chegou até a metade desse caminho com o que o padrão-alvo oferece, e vale reler a §19.4 ao lado desta seção. Um `static_assert` no corpo da classe troca o erro de dentro de `<vector>` por uma frase escrita à mão, no ponto em que o tipo errado foi escolhido, e resolve o caso prático. O que ele **não** faz é o que separa os dois recursos: a restrição não faz parte da assinatura, não participa da resolução de sobrecarga, e não há como perguntar se um tipo a satisfaz sem tentar instanciar.

Um concept é a mesma exigência promovida a entidade nomeada da linguagem. Ela tem nome, é reutilizável, compõe com outras através de conjunção e disjunção, aparece na assinatura no lugar de `typename`, e pode ser consultada numa expressão booleana. É por isso que ele permite duas coisas que o `static_assert` não permite: escrever duas sobrecargas do mesmo template, uma para tipos que satisfazem o concept e outra para os que não, deixando o compilador escolher; e receber, na violação, a mensagem que nomeia **qual** requisito falhou, em vez da que diz que nenhuma sobrecarga era viável.

O concept que o alvo opcional escreve chama-se `guardavel`, e ele é a tradução direta dos três `static_assert` de `grade_generica.hpp`: construtor padrão, não ser referência, e não ser `bool`. A forma dele está extraída no fim deste anexo, e são duas linhas com três conjunções. Duas coisas nelas valem atenção. A primeira é que os requisitos vêm de `<concepts>` já nomeados - `std::default_initializable`, `std::same_as` -, o que significa que a biblioteca padrão passou a ter vocabulário de restrição, e não só de tipo. A segunda é a composição: `&&` entre concepts produz outro concept, e é isso que o `static_assert` nunca soube fazer.

O uso aparece na declaração da classe, `template <guardavel T> class grade_restrita`, e é aqui que a diferença deixa de ser cosmética. A restrição passou a fazer parte da assinatura, o que tem três consequências: ela participa da resolução de sobrecarga, ela pode ser consultada numa expressão booleana - o arquivo termina em quatro `static_assert` que perguntam `guardavel<celula>`, `guardavel<int>`, `!guardavel<bool>` e `!guardavel<int&>`, e as quatro respostas são conferidas em compilação -, e a mensagem de erro muda de lugar. Com `static_assert`, o compilador aponta a linha do assert, dentro da classe. Com `concept`, ele aponta a **chamada** e diz qual restrição falhou. É essa mudança de endereço, e não a economia de digitação, que é a razão de os concepts existirem, e é o que o exercício 1 manda você transcrever.

## A.2 Ranges - Programação Funcional sobre Sequências **(C++20)**

Ranges é o assunto vizinho de Concepts no mesmo padrão, e resolve outro incômodo. O Cap. 21 apresenta os algoritmos da STL na forma clássica, com um par de iteradores por chamada, e essa forma tem dois custos de escrita. O primeiro é a repetição de `c.begin(), c.end()` em toda chamada, quando o que se quer quase sempre é o contêiner inteiro. O segundo é a composição: filtrar e depois transformar exige um contêiner intermediário para guardar o resultado do primeiro passo, com a alocação que isso implica.

Ranges resolve o primeiro passando o contêiner, e o segundo com **views**, que são composições preguiçosas: nada é calculado até que alguém percorra o resultado, e nenhum contêiner intermediário é criado. O operador `|` encadeia as views, e a leitura fica na ordem em que as coisas acontecem, da esquerda para a direita, que é o oposto da leitura de chamadas aninhadas.

No alvo opcional o exemplo é `glifos_de_parede`, extraída no fim deste anexo: ela percorre as células da grade, filtra as que têm o glifo de parede e para nas dez primeiras, tudo numa expressão só, com `views::filter` e `views::take` encadeados por `|`. Em C++17 o equivalente seria um `copy_if` para um vetor temporário e um segundo laço depois - dois percursos e uma alocação -, e é essa alocação que a composição preguiçosa não faz.

Vale registrar que o ganho aqui é de expressão, e não de desempenho: a versão com um laço explícito sobre a grade contígua é rápida, e a composição de views não a supera. O que ela dá é a leitura na ordem em que as coisas acontecem, e a ausência do contêiner que existia só para ser descartado.

E vale registrar a armadilha, que é a mesma do `std::string_view` do Cap. 3, pela mesma razão. **Uma view não possui os elementos que enxerga.** Guardar uma view cujo contêiner de origem já foi destruído, ou modificado de forma a invalidar iteradores, é referência pendurada, e o compilador não avisa. View se compõe e se percorre no mesmo escopo; o que se guarda é o resultado materializado.

## Exercícios Propostos

Os itens abaixo pressupõem o alvo opcional de C++20, e nenhum deles é exigido. Eles só fazem sentido depois dos exercícios 1 a 5 do Cap. 19, porque comparam com o que foi feito lá.

**1.** Compile `grade_de<bool>` no alvo de C++17 e `grade_restrita<bool>` no alvo de C++20, e transcreva as duas mensagens de erro inteiras, sem resumir. Aponte, em cada uma, qual linha o compilador culpou e qual requisito ele nomeou. Depois escreva o seu próprio concept, com nome diferente de `guardavel`, exigindo também que `T` seja copiável, e diga o que a terceira mensagem acrescenta.

**2.** Escreva um concept `desenhavel_como_glifo<T>` que exija de `T` a conversão para `char` através de uma função livre `glifo_de`. Use-o para restringir `grade<T>::despejar()`, e explique o que ele permite que o `if constexpr` do Cap. 19 não permitia.

**3.** Reescreva o cálculo do campo de visão com `std::views::filter` e `std::views::transform`, sem contêiner intermediário. Meça as duas versões com `std::chrono`, num setor grande, e diga qual é mais rápida e por quê.

**4.** Provoque a view pendurada: componha uma view sobre um `std::vector` local, devolva-a da função, e percorra-a no chamador. Explique por que o compilador aceitou, e compare com o caso do `string_view` do Cap. 3.

**5.** Compile o mesmo arquivo com `-std=c++17` e com `-std=c++20` e liste, a partir dos erros do primeiro, tudo o que o seu código passou a depender do padrão novo. É este o exercício que responde à pergunta de por que este material é um anexo.

## O código, extraído do Deriva

Todo trecho abaixo vem de `exemplos/deriva/c20/`, que compila em alvo **separado** com `-std=c++20 -Wall -Wextra -Wpedantic` sem um aviso - e que fica **fora** do portão `make verifica`, porque o padrão-alvo da disciplina é C++17. Nenhum foi digitado neste texto, e nada do material obrigatório depende deles.

**c20/restricoes.hpp · o concept no lugar do static_assert**

`exemplos/deriva/c20/restricoes.hpp:36`

``` cpp
concept guardavel = std::default_initializable<T> && !std::is_reference_v<T> &&
                    !std::same_as<T, bool>;
```

A diferença que se vê é a mensagem de erro: com `static_assert` o compilador aponta a linha do assert; com `concept`, aponta a CHAMADA e diz qual restrição falhou. É a razão de os concepts existirem.

**c20/restricoes.hpp · ranges, sem contêiner intermediário**

`exemplos/deriva/c20/restricoes.hpp:61`

``` cpp
/// Ranges no lugar do laço, sobre as células da grade.
///
/// O que se ganha é composição sem contêiner intermediário: `filter` e
/// `transform` são vistas preguiçosas, e nada é copiado até alguém iterar. Em
/// C++17 o equivalente seria um `copy_if` para um vetor temporário e um
/// `transform` depois - dois laços e uma alocação.
[[nodiscard]] inline std::string glifos_de_parede(const grade_restrita<celula>& g) {
  std::string s;
  for (const celula& c : g.todas()
                             | std::views::filter([](const celula& x) {
                                 return x.glifo == '#';
                               })
                             | std::views::take(10)) {
    s.push_back(c.glifo);
  }
```

`filter` e `transform` são vistas preguiçosas: nada é copiado até alguém iterar. Em C++17 o equivalente seria um `copy_if` para um vetor temporário e um `transform` depois - dois laços e uma alocação.
