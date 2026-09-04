// v1.8 - inspetor: RTTI e o tipo dinamico
#include <memory>
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/inspetor.hpp"
#include "deriva/mundo.hpp"
#include "deriva/reparadora.hpp"

using namespace deriva;

namespace {
mundo montar() {
  auto m = mapa::de_texto("#######\n#.....#\n#######\n", "t");
  return mundo(std::move(*m));
}
}  // namespace

TEST_CASE("o inspetor responde pelo tipo dinamico") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}, 55));
  w.acrescentar(std::make_unique<drone>(vetor2{2, 1}, vetor2{0, 1}));
  w.acrescentar(std::make_unique<item>(vetor2{3, 1}, "sucata", 4));

  REQUIRE(inspecionar(w.em(0)).find("[sonda, energia 55]") != std::string::npos);
  REQUIRE(inspecionar(w.em(1)).find("[drone, rumo 0,1]") != std::string::npos);
  REQUIRE(inspecionar(w.em(2)).find("[item, massa 4]") != std::string::npos);
}

// A armadilha numero um da cadeia de dynamic_cast: a reparadora TAMBEM e
// sonda, entao testar `sonda` primeiro a capturaria e o ramo especifico nunca
// rodaria. A ordem do mais derivado para o menos e obrigatoria.
TEST_CASE("a ordem da cadeia importa: o mais derivado primeiro") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda_reparadora>(vetor2{1, 1}));

  const std::string s = inspecionar(w.em(0));
  REQUIRE(s.find("[reparadora,") != std::string::npos);
  REQUIRE(s.find("[sonda, energia") == std::string::npos);
}

TEST_CASE("dynamic_cast para a interface pergunta por capacidade, nao por tipo") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  w.acrescentar(std::make_unique<sonda_reparadora>(vetor2{2, 1}));
  w.acrescentar(std::make_unique<drone>(vetor2{3, 1}));

  const std::string s = listar_reparadoras(w);
  REQUIRE(s.find("reparadoras 1") == 0);
  REQUIRE(s.find("sonda_reparadora") != std::string::npos);
}

TEST_CASE("typeid responde sobre o tipo real, e o nome e da implementacao") {
  zerar_entidades();
  const sonda s({1, 1});
  const entidade& por_base = s;
  REQUIRE(tipo_cru(por_base) == tipo_cru(s));       // o mesmo tipo dinamico
  REQUIRE(tipo_cru(por_base).find("sonda") != std::string::npos);

  const drone d({2, 2});
  REQUIRE(tipo_cru(d) != tipo_cru(s));
}

TEST_CASE("descrever resolve o mesmo problema sem perguntar o tipo") {
  zerar_entidades();
  const drone d({4, 7});
  // Nenhum dynamic_cast, nenhum typeid: e a forma correta para o dominio.
  REQUIRE(d.descrever() == "d drone @ 4,7");
}
