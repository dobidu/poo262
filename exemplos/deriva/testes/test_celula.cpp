// v0.1 - celula e o custo da ordem de declaracao
#include <catch2/catch_test_macros.hpp>

#include "deriva/celula.hpp"

using deriva::celula;
using deriva::celula_ingenua;

// Estes números aparecem no interativo "inspetor de objeto" da Aula 07. Se o
// leiaute mudar, o teste falha ANTES de o material passar a mentir.
TEST_CASE("a ordem de declaracao muda o sizeof") {
  REQUIRE(sizeof(celula) == 12);
  REQUIRE(sizeof(celula_ingenua) == 16);

  SECTION("os dados uteis sao os mesmos nas duas") {
    constexpr std::size_t uteis = 2 * sizeof(int) + 2 * sizeof(char);
    REQUIRE(uteis == 10);
    REQUIRE(sizeof(celula) - uteis == 2);        // 2 B de padding no fim
    REQUIRE(sizeof(celula_ingenua) - uteis == 6); // 6 B, e nada em troca
  }

  SECTION("numa grade de 80x24 a diferenca e concreta") {
    constexpr std::size_t n = 80 * 24;
    REQUIRE(n * sizeof(celula) == 23040);
    REQUIRE(n * sizeof(celula_ingenua) == 30720);
  }
}

TEST_CASE("celula nasce como piso vazio") {
  const celula c;
  REQUIRE(c.glifo == '.');
  REQUIRE(c.energia == 0);
  REQUIRE(c.massa == 0);
}
