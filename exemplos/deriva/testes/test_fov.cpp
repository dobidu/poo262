// v1.6 - campo de visao puro e deterministico
#include <set>

#include <catch2/catch_test_macros.hpp>

#include "deriva/fov.hpp"

using namespace deriva;

namespace {
// Uma sala com uma coluna no meio, para haver o que bloquear.
constexpr const char* kSala =
    "#########\n"
    "#.......#\n"
    "#...#...#\n"
    "#.......#\n"
    "#########\n";
}  // namespace

TEST_CASE("a linha e inteira, e portanto a mesma em qualquer maquina") {
  const auto l = linha({0, 0}, {3, 0});
  REQUIRE(l.size() == 4);
  REQUIRE(l.front() == vetor2{0, 0});
  REQUIRE(l.back() == vetor2{3, 0});

  const auto d = linha({0, 0}, {3, 3});
  REQUIRE(d.size() == 4);
  REQUIRE(d.back() == vetor2{3, 3});

  // simetria: ir e voltar visita as mesmas celulas
  const auto ida = linha({1, 1}, {4, 3});
  auto volta = linha({4, 3}, {1, 1});
  std::set<vetor2> a(ida.begin(), ida.end()), b(volta.begin(), volta.end());
  REQUIRE(a == b);
}

TEST_CASE("visiveis inclui a origem e respeita o raio") {
  const auto m = mapa::de_texto(kSala, "sala");
  const auto v = visiveis(*m, {1, 1}, 2);
  REQUIRE(v.count(vetor2{1, 1}) == 1);
  REQUIRE(v.count(vetor2{3, 1}) == 1);          // dentro do raio
  REQUIRE(v.count(vetor2{5, 1}) == 0);          // fora do raio de Manhattan
}

TEST_CASE("a parede e vista e bloqueia o que esta atras") {
  const auto m = mapa::de_texto(kSala, "sala");
  const auto v = visiveis(*m, {1, 2}, 6);

  REQUIRE(v.count(vetor2{4, 2}) == 1);   // a coluna: vista, porque bloqueia
  REQUIRE(v.count(vetor2{5, 2}) == 0);   // logo atras dela: sombra

  SECTION("mas se ve em volta da coluna, por cima e por baixo") {
    REQUIRE(v.count(vetor2{4, 1}) == 1);
    REQUIRE(v.count(vetor2{4, 3}) == 1);
    REQUIRE(v.count(vetor2{6, 1}) == 1);   // na borda do raio, dist 6
  }
  SECTION("o raio e de Manhattan, e a borda e exata") {
    REQUIRE(vetor2{1, 2}.manhattan({6, 1}) == 6);
    REQUIRE(v.count(vetor2{6, 1}) == 1);
    REQUIRE(vetor2{1, 2}.manhattan({7, 1}) == 7);
    REQUIRE(v.count(vetor2{7, 1}) == 0);   // um passo alem, e ja nao se ve
  }
}

TEST_CASE("visiveis e funcao pura: mesma entrada, mesmo conjunto") {
  const auto m = mapa::de_texto(kSala, "sala");
  REQUIRE(visiveis(*m, {2, 2}, 3) == visiveis(*m, {2, 2}, 3));
  REQUIRE(despejar_fov(*m, {2, 2}, 3) == despejar_fov(*m, {2, 2}, 3));
}

TEST_CASE("fora do mapa nao se ve nada") {
  const auto m = mapa::de_texto(kSala, "sala");
  REQUIRE(visiveis(*m, {-1, -1}, 3).empty());
}
