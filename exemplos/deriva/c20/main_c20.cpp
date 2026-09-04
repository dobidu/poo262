// Anexo A · o alvo de C++20, que existe para ser compilado e não para ser
// dependência de nada.
#include <cassert>
#include <cstdio>

#include "restricoes.hpp"

int main() {
  using namespace deriva;
  using namespace deriva::c20;

  grade_restrita<celula> g(5, 3);
  g.em({0, 0}).glifo = '#';
  g.em({1, 0}).glifo = '#';
  g.em({2, 0}).glifo = '.';

  const std::string paredes = glifos_de_parede(g);
  std::printf("grade restrita: %zu celulas · paredes vistas: %s\n",
              g.tamanho(), paredes.c_str());
  assert(paredes == "##");

  grade_restrita<int> dist(4, 2);
  dist.em({1, 1}) = 7;
  std::printf("grade de int:   %zu celulas · em(1,1) = %d\n",
              dist.tamanho(), dist.em({1, 1}));
  assert(dist.em({1, 1}) == 7);

  // `grade_restrita<bool> b(2, 2);` NAO compila, e a mensagem nomeia o
  // concept `guardavel` em vez de vazar de dentro do std::vector.
  static_assert(!guardavel<bool>);

  std::printf("\nC++%ld · alvo opcional, e nada do material obrigatorio depende dele\n",
              __cplusplus / 100 - 2000 + 2000);
  return 0;
}
