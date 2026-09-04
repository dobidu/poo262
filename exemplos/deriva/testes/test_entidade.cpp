// v1.0 - a hierarquia entidade e o subobjeto base
#include <memory>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/entidade.hpp"
#include "deriva/mundo.hpp"

using namespace deriva;

TEST_CASE("entidade e abstrata, e o compilador diz isso") {
  static_assert(std::is_abstract_v<entidade>);
  static_assert(!std::is_constructible_v<entidade, vetor2>);
  static_assert(std::has_virtual_destructor_v<entidade>);
  static_assert(!std::is_copy_constructible_v<entidade>,
                "base polimorfica nao se copia por valor: fatiaria o objeto");
  SUCCEED("verificado em tempo de compilacao");
}

TEST_CASE("o despacho virtual escolhe pelo tipo do OBJETO") {
  zerar_entidades();
  const sonda s({1, 1});
  const drone d({2, 2});
  const item i({3, 3}, "celula-de-energia", 5);

  const entidade* por_base[] = {&s, &d, &i};
  std::string glifos;
  for (const entidade* e : por_base) glifos.push_back(e->glifo());

  REQUIRE(glifos == "@d!");   // e nao "eee": o ponteiro e entidade* nos tres
}

TEST_CASE("descrever e Template Method: moldura da base, glifo da derivada") {
  zerar_entidades();
  const drone d({4, 7});
  REQUIRE(d.descrever() == "d drone @ 4,7");
  const item i({0, 0}, "sucata", 2);
  REQUIRE(i.descrever() == "! sucata @ 0,0");
}

// A prova do destrutor virtual: deletar por ponteiro da base tem de rodar o
// destrutor da derivada, e o contador de CADA classe concreta e o que acusa.
TEST_CASE("deletar por entidade* destroi a derivada") {
  zerar_entidades();
  {
    std::unique_ptr<entidade> e = std::make_unique<sonda>(vetor2{1, 1});
    REQUIRE(sonda::vivos == 1);
  }
  REQUIRE(sonda::vivos == 0);
  REQUIRE(sonda::criados == 1);
  REQUIRE(entidades_vivas() == 0);
}

TEST_CASE("o contador mora em cada classe concreta, e nao na base") {
  zerar_entidades();
  {
    const sonda s1({1, 1}), s2({2, 2});
    const drone d({3, 3});
    REQUIRE(sonda::vivos == 2);
    REQUIRE(drone::vivos == 1);
    REQUIRE(item::vivos == 0);
    REQUIRE(entidades_vivas() == 3);
  }
  REQUIRE(entidades_vivas() == 0);
}

TEST_CASE("item nao sobrescreve agir, e nao precisa") {
  zerar_entidades();
  auto m = mapa::de_texto("#####\n#...#\n#####\n", "t");
  mundo w(std::move(*m));
  item& i = static_cast<item&>(w.acrescentar(std::make_unique<item>(
      vetor2{2, 1}, "sucata", 3)));
  const vetor2 antes = i.pos();
  w.turno();
  REQUIRE(i.pos() == antes);
}

TEST_CASE("o drone anda e inverte o rumo ao bater na parede") {
  zerar_entidades();
  auto m = mapa::de_texto("#####\n#...#\n#####\n", "t");
  mundo w(std::move(*m));
  drone& d = static_cast<drone&>(w.acrescentar(std::make_unique<drone>(
      vetor2{1, 1}, vetor2{1, 0})));

  w.turno();
  REQUIRE(d.pos() == vetor2{2, 1});
  w.turno();
  REQUIRE(d.pos() == vetor2{3, 1});
  w.turno();                       // a proxima e parede: inverte, nao anda
  REQUIRE(d.pos() == vetor2{3, 1});
  REQUIRE(d.rumo() == vetor2{-1, 0});
  w.turno();
  REQUIRE(d.pos() == vetor2{2, 1});
}
