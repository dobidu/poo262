// v0.1 - vetor2: igualdade por valor e origem
#include <catch2/catch_test_macros.hpp>

#include "deriva/vetor2.hpp"

using deriva::vetor2;

TEST_CASE("vetor2 compara por valor") {
  REQUIRE(vetor2{3, 4} == vetor2{3, 4});
  REQUIRE(vetor2{3, 4} != vetor2{4, 3});
}

TEST_CASE("vetor2 nasce na origem") {
  const vetor2 v;
  REQUIRE(v == vetor2{0, 0});
}

// A comparação é constexpr: se deixar de ser, esta linha para de compilar.
// Teste em tempo de compilação também é teste.
static_assert(vetor2{1, 2} == vetor2{1, 2});
static_assert(vetor2{1, 2} != vetor2{2, 1});
