# O que o sanitizer pega e o portão não

**Aula 02 · infraestrutura, e o lugar do ASan como ferramenta**

## Por que ela existe

O Deriva não tem um acesso fora de limite nem um estouro de `int` com sinal, e
não é sorte: `-Wconversion`, `-Wsign-conversion` e o par `dentro()`/`em()` os
impedem por construção. Mas a Aula 02 precisa mostrar o ASan e o UBSan
trabalhando, e para isso precisa de algo para eles pegarem.

Estes dois defeitos não podem morar no núcleo nem na suíte de testes: o
sanitizer abortaria, e as condições 1 e 2 do portão cairiam junto.

Este diretório **não é uma variante da trilha**, e o nome não finge que é: as
quatro variantes quebradas (`v0.2`, `v0.3`, `v1.1`, `v2.6-antes`) são versões
do Deriva com um defeito de projeto, e cada uma tem a sua caça ao bug. Aqui são
dois defeitos de memória escritos para uma aula, como `comparativo/`,
`revisao_ia/` e `tipos/`.

## Os dois defeitos

**1 · acesso fora de limite.** `em()` sem `dentro()` ao lado aceita qualquer
posição, e o `operator[]` do `vector` não confere - `at()` conferiria, e é a
escolha que a versão boa deixa explícita para quem chama. Escrever em `(2,3)`
numa grade de três fileiras calcula o índice 14 de doze células, e a escrita
acontece.

**2 · estouro de `int` com sinal.** `largura * altura` é calculado em `int` e
estoura antes de virar `size_t`. Nenhum `static_cast` depois conserta o que já
estourou - e é por isso que a versão boa converte **cada fator antes** de
multiplicar, com dois casts que parecem redundantes e não são.

E aqui está a parte que vale a aula, descoberta escrevendo este arquivo.
Escrito com literais, `const int p = 50000 * 50000;`, o g++ dobra a conta em
tempo de compilação, vê o estouro e **avisa**:

```
warning: integer overflow in expression of type 'int' results in '-1794967296' [-Woverflow]
```

O defeito não embarca. Com as dimensões vindo de fora - de linha de comando
aqui, de um arquivo de mapa no Deriva -, o compilador não tem o que dobrar, o
aviso desaparece, e o estouro passa a acontecer em execução.

**O compilador pega o que ele consegue ver.** É por isso que o defeito real
nunca chega com número escrito no código: ele chega com número lido de fora, e
é aí que o sanitizer passa a ser a única ferramenta que sobra.

## O que os dois têm em comum, e é o que a aula ensina

Nenhum produz aviso de compilação **como estão escritos aqui**, com os valores
vindo de fora. Os dois produzem comportamento indefinido.
E os dois **parecem funcionar**: o primeiro devolve o caractere que você
escreveu, o segundo imprime um número. Programa que parece funcionar é o pior
resultado possível, porque não há sintoma para investigar.

## Roteiro, na ordem

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic -Wconversion defeitos_de_memoria.cpp -o quebrado
./quebrado                       # roda, e mente

g++ -std=c++17 -g -fsanitize=address defeitos_de_memoria.cpp -o q-asan
./q-asan                         # aponta a linha, a alocação e o deslocamento

g++ -std=c++17 -g -fsanitize=undefined defeitos_de_memoria.cpp -o q-ubsan
./q-ubsan                        # nomeia: signed integer overflow
```

1. Rode sem sanitizer e leia a saída. Ela é coerente, e está errada.
2. Rode com o ASan: ele diz `heap-buffer-overflow`, a linha da escrita, e a
   linha da alocação. É a informação que faltava.
3. Rode com o UBSan: `signed integer overflow: 50000 * 50000 cannot be
   represented in type 'int'`.
4. Conserte os dois olhando a versão boa: `include/deriva/grade.hpp`, com o par
   `dentro()`/`em()`, e `src/grade.cpp`, com a conversão de cada fator.

## O lugar do sanitizer nesta disciplina

**Ferramenta, e não portão.** O laboratório não tem ASan nem Valgrind, e por
isso o portão de correção não pode depender deles. O que a disciplina exige é
o bloco de três técnicas sem dependência externa - contador de instâncias,
instrumentação de ciclo de vida e `gdb` no destrutor.

O sanitizer aparece em aula, na máquina de projeção, como **confirmação**: o
estudante primeiro reproduz e explica o defeito com o que construiu, e só
depois vê a ferramenta apontar o que ele já havia identificado. Aqui a ordem se
inverte de propósito, porque estes dois defeitos são justamente os que as três
técnicas **não** pegam - contador nenhum acusa índice fora de limite.
