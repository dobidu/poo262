// v1.2 - mundo: posse exclusiva por unique_ptr
#include <memory>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/mundo.hpp"

using namespace deriva;

namespace {
mundo montar() {
  auto m = mapa::de_texto("#######\n#.....#\n#.###.#\n#.....#\n#######\n", "setor");
  return mundo(std::move(*m));
}
}  // namespace

TEST_CASE("mundo e movivel e nao copiavel, e o tipo diz por que") {
  static_assert(std::is_move_constructible_v<mundo>);
  static_assert(!std::is_copy_constructible_v<mundo>,
                "copiar exigiria clonar polimorficamente: e decisao de projeto");
  SUCCEED("verificado em tempo de compilacao");
}

TEST_CASE("acrescentar toma posse, e o mundo destroi ao morrer") {
  zerar_entidades();
  {
    mundo w = montar();
    w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
    w.acrescentar(std::make_unique<drone>(vetor2{5, 3}));
    w.acrescentar(std::make_unique<item>(vetor2{1, 3}, "sucata", 4));
    REQUIRE(w.quantas() == 3);
    REQUIRE(entidades_vivas() == 3);
  }
  REQUIRE(entidades_vivas() == 0);   // nenhum delete no codigo, e nada vazou
}

TEST_CASE("primeira_com devolve observacao, nao posse") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  entidade* s = w.primeira_com('@');
  REQUIRE(s != nullptr);
  REQUIRE(s->nome() == "sonda");
  REQUIRE(w.primeira_com('X') == nullptr);
  REQUIRE(entidades_vivas() == 1);   // olhar nao transfere nada
}

TEST_CASE("retirar_de transfere a posse para quem chamou") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<item>(vetor2{1, 3}, "sucata", 4));
  REQUIRE(w.quantas() == 1);
  {
    std::unique_ptr<entidade> saiu = w.retirar_de({1, 3});
    REQUIRE(saiu != nullptr);
    REQUIRE(w.quantas() == 0);
    REQUIRE(item::vivos == 1);       // ainda vivo: o dono agora e este escopo
  }
  REQUIRE(item::vivos == 0);         // e morreu aqui, com o unique_ptr
}

TEST_CASE("a ordem do turno e a de insercao, e o replay depende dela") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<drone>(vetor2{1, 1}, vetor2{1, 0}));
  w.acrescentar(std::make_unique<drone>(vetor2{5, 3}, vetor2{-1, 0}));
  w.turno();
  REQUIRE(w.em(0).pos() == vetor2{2, 1});
  REQUIRE(w.em(1).pos() == vetor2{4, 3});
}

TEST_CASE("o despejo e deterministico e poe as entidades por cima do terreno") {
  zerar_entidades();
  mundo a = montar();
  a.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  mundo b = montar();
  b.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  REQUIRE(a.despejar() == b.despejar());
  REQUIRE(a.despejar().find("entidades 1") != std::string::npos);
  REQUIRE(a.despejar().find("@ sonda @ 1,1") != std::string::npos);
}

TEST_CASE("livre respeita parede e limite") {
  mundo w = montar();
  REQUIRE(w.livre({1, 1}));
  REQUIRE_FALSE(w.livre({0, 0}));      // parede
  REQUIRE_FALSE(w.livre({2, 2}));      // parede interna
  REQUIRE_FALSE(w.livre({-1, 1}));     // fora
}
