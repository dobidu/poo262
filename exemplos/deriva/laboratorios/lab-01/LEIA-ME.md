# LAB-01 · Ambiente, CMake e portões de compilação

**Prepara a Aula 2 · semana 1, E2**

## Portão

Compilar **sem um único aviso** sob `-Wall -Wextra -Wpedantic -Wconversion`, e
o programa relatar `portao LAB-01: OK`.

## O que se aprende

Que o portão da disciplina não é "compila". É "compila sem aviso", e a
diferença é a distância entre um programa que roda hoje e um que continua
rodando quando alguém mexer nele.

Os três TODO do esqueleto são três avisos reais:

1. **detectar o padrão** - `__cplusplus == 201703L`. Comparar com o número, e
   não com uma macro do compilador, é o que torna a checagem portável;
2. **detectar as extensões GNU** - `__STRICT_ANSI__` é definida quando elas
   estão **desligadas**. É o que `set(CMAKE_CXX_EXTENSIONS OFF)` garante, e o
   motivo é direto: código que só compila com `-std=gnu++17` não é C++17;
3. **`-Wconversion` em `'0' + (n % 10)`** - a soma promove para `int`, e
   devolvê-la como `char` perde informação. O conserto é `static_cast<char>`, e
   o que se ganha não é silêncio: é a declaração de que a perda é intencional.

## O que NÃO resolve

Desligar o aviso. `#pragma GCC diagnostic ignored` faz o portão passar e é
reprovado na revisão - o portão existe para ser satisfeito, não contornado.

## Depois

Reproduza o mesmo no CMake: `CMakeLists.txt` com `CXX_STANDARD 17`,
`CXX_EXTENSIONS OFF` e o conjunto de avisos em `target_compile_options`. O do
Deriva está em `../../CMakeLists.txt` e serve de referência.
