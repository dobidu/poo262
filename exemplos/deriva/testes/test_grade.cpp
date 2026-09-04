// v0.2 - grade: limites, escrita e copia profunda
#include <stdexcept>

#include <catch2/catch_test_macros.hpp>

#include "deriva/grade.hpp"

using deriva::grade;
using deriva::vetor2;

TEST_CASE("grade conhece seus limites") {
  const grade g(20, 10);
  REQUIRE(g.largura() == 20);
  REQUIRE(g.altura() == 10);
  REQUIRE(g.dentro({0, 0}));
  REQUIRE(g.dentro({19, 9}));
  REQUIRE_FALSE(g.dentro({20, 9}));
  REQUIRE_FALSE(g.dentro({-1, 0}));
}

TEST_CASE("dimensao nao-positiva e erro de programacao") {
  REQUIRE_THROWS_AS(grade(0, 5), std::invalid_argument);
  REQUIRE_THROWS_AS(grade(5, -1), std::invalid_argument);
}

TEST_CASE("escrever numa celula nao afeta a vizinha") {
  grade g(4, 3);
  g.em({1, 1}).glifo = '#';
  REQUIRE(g.em({1, 1}).glifo == '#');
  REQUIRE(g.em({2, 1}).glifo == '.');
  REQUIRE(g.em({1, 2}).glifo == '.');
}

// Regra do zero: a grade não declara nenhuma das cinco operações especiais, e
// a cópia gerada pelo compilador é PROFUNDA porque o membro é um vector. É
// exatamente isto que a variante v0.3-quebrada perde ao usar ponteiro cru.
TEST_CASE("a copia gerada pelo compilador e profunda") {
  grade a(4, 3);
  a.em({0, 0}).glifo = '@';

  grade b = a;             // cópia
  b.em({0, 0}).glifo = '#';

  REQUIRE(a.em({0, 0}).glifo == '@');   // a original não mudou
  REQUIRE(b.em({0, 0}).glifo == '#');
}

TEST_CASE("bytes_das_celulas mede o que a Aula 07 discute") {
  const grade g(80, 24);
  REQUIRE(g.bytes_das_celulas() == 80u * 24u * sizeof(deriva::celula));
  REQUIRE(g.bytes_das_celulas() == 23040u);
}
