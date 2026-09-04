// v1.5 - operadores de vetor2 e mapa[pos]
#include <sstream>
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/mapa.hpp"
#include "deriva/vetor2.hpp"

using namespace deriva;

TEST_CASE("os operadores de vetor2 sao simetricos e constexpr") {
  REQUIRE(vetor2{1, 2} + vetor2{3, 4} == vetor2{4, 6});
  REQUIRE(vetor2{5, 5} - vetor2{1, 2} == vetor2{4, 3});
  REQUIRE(vetor2{2, 3} * 3 == vetor2{6, 9});
  REQUIRE(3 * vetor2{2, 3} == vetor2{6, 9});   // funcao livre: aceita os dois lados

  vetor2 v{1, 1};
  v += {2, 3};
  REQUIRE(v == vetor2{3, 4});
  v -= {1, 1};
  REQUIRE(v == vetor2{2, 3});
}

TEST_CASE("a distancia e de Manhattan porque a grade nao tem diagonal") {
  REQUIRE(vetor2{0, 0}.manhattan({3, 4}) == 7);   // e nao 5
  REQUIRE(vetor2{3, 4}.manhattan({0, 0}) == 7);   // simetrica
}

TEST_CASE("a ordem total serve de chave e da despejo estavel") {
  REQUIRE(vetor2{1, 0} < vetor2{0, 1});   // fileira antes de coluna
  REQUIRE(vetor2{0, 1} < vetor2{1, 1});
  REQUIRE_FALSE(vetor2{1, 1} < vetor2{1, 1});
}

TEST_CASE("o par const e nao-const de operator[] existe por uma razao") {
  auto m = mapa::de_texto("#####\n#.@.#\n#####\n", "t");
  REQUIRE(m.has_value());

  (*m)[{1, 1}].glifo = 'x';                   // nao-const: escreve
  REQUIRE((*m)[{1, 1}].glifo == 'x');

  const mapa& fixo = *m;
  REQUIRE(fixo[{1, 1}].glifo == 'x');         // const: le
  static_assert(std::is_const_v<std::remove_reference_t<decltype(fixo[{0, 0}])>>,
                "por mapa const, a celula vem const");
}

TEST_CASE("operator<< escreve o despejo, e e funcao livre") {
  const auto m = mapa::de_texto("###\n#.#\n###\n", "t");
  std::ostringstream os;
  os << *m;
  REQUIRE(os.str() == m->despejar());
}
