// v0.1 · Aula 07 - leiaute em memória: a ordem de declaração muda o sizeof
#ifndef DERIVA_CELULA_HPP
#define DERIVA_CELULA_HPP

#include <cstddef>

namespace deriva {

/// Uma célula da grade da estação.
///
/// A ordem dos membros aqui NÃO é estética: agrupada por tamanho, a célula
/// ocupa 12 bytes. Declarada na ordem "natural" - o glifo primeiro, porque é
/// o que se vê - , ocupa 16. Numa grade de 80×24 são 1920 células, logo 23 KB
/// contra 30 KB, e é o mesmo código.
///
/// `celula_ingenua` existe só para ser medida: é o contraexemplo do
/// interativo "inspetor de objeto" (Aula 07), e os static_assert abaixo são o
/// que impede o material de mentir sobre esses números.
struct celula {
  int energia = 0;   // 4 B  @ 0
  int massa = 0;     // 4 B  @ 4
  char glifo = '.';  // 1 B  @ 8
  char sigla = ' ';  // 1 B  @ 9
                     //       + 2 B de padding no fim
};

/// A MESMA célula, na ordem em que se pensa nela. Não use.
struct celula_ingenua {
  char glifo = '.';  // 1 B  @ 0   + 3 B de padding
  int energia = 0;   // 4 B  @ 4
  char sigla = ' ';  // 1 B  @ 8   + 3 B de padding
  int massa = 0;     // 4 B  @ 12
};

static_assert(sizeof(celula) == 12, "agrupada por tamanho");
static_assert(sizeof(celula_ingenua) == 16, "a ordem ingênua custa 4 bytes por célula");
static_assert(alignof(celula) == 4, "o maior membro manda no alinhamento");
static_assert(offsetof(celula, glifo) == 8, "os dois int primeiro, sem buraco entre eles");

}  // namespace deriva

#endif
