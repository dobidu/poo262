// Aula 01 - o mesmo problema em C e em C++
#ifndef DERIVA_COMPARATIVO_HPP
#define DERIVA_COMPARATIVO_HPP

#include <cstddef>
#include <cstdlib>

namespace deriva::comparativo {

/// A grade da estação em estilo C: dado exposto, funções livres, e o
/// contrato inteiro na cabeça de quem chama.
///
/// Isto não é caricatura. É a forma que o C permite e que o C++ herdou, e
/// funciona - com uma condição: que todo mundo lembre das regras. As regras
/// são cinco, e nenhuma delas está escrita no código.
///
///   1. chame `criar` antes de qualquer outra coisa;
///   2. chame `destruir` exatamente uma vez, e nunca depois de copiar;
///   3. não copie a struct - ela leva o ponteiro, e não os dados;
///   4. não escreva em `largura` nem `altura` depois de criada;
///   5. confira o limite antes de indexar, porque ninguém confere por você.
struct grade_c {
  int largura;
  int altura;
  char* celulas;
};

[[nodiscard]] grade_c criar(int largura, int altura);
void destruir(grade_c* g);
[[nodiscard]] char em(const grade_c* g, int x, int y);
void escrever(grade_c* g, int x, int y, char c);

/// Quantas das cinco regras este trecho pode violar sem que nada reclame.
/// É a métrica da Aula 01: não é elegância, é quantas maneiras de errar o
/// desenho permite.
[[nodiscard]] int maneiras_de_errar_em_c();
[[nodiscard]] int maneiras_de_errar_em_cpp();

}  // namespace deriva::comparativo

#endif
