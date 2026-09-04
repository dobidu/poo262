// v1.7 - sonda_reparadora: o diamante com base virtual
#include <catch2/catch_test_macros.hpp>

#include "deriva/diamante.hpp"
#include "deriva/mundo.hpp"
#include "deriva/reparadora.hpp"

using namespace deriva;
using namespace deriva::medida;

// O diamante COM ESTADO, medido. Sem heranca virtual, a base do meio e
// duplicada, e o objeto passa a ter dois subobjetos `nucleo` com enderecos
// diferentes - dois valores de `leituras`, e nenhum dos dois e "o" valor.
TEST_CASE("sem heranca virtual, a base do meio e duplicada") {
  REQUIRE(nucleos_em_duplicada() == 2);
  REQUIRE(nucleos_em_unica() == 1);
}

// Contraria a intuicao, e por isso esta medido: a heranca virtual e a MAIOR
// das tres. O que ela compra e correcao, nao tamanho.
TEST_CASE("a heranca virtual custa mais bytes que a duplicacao que evita") {
  REQUIRE(sizeof(nucleo) == 16);
  REQUIRE(sizeof(patrulha_duplicada) == 40);
  REQUIRE(sizeof(patrulha_unica) == 48);
  REQUIRE(sizeof(patrulha_composta) == 56);
  REQUIRE(sizeof(patrulha_unica) > sizeof(patrulha_duplicada));
}

TEST_CASE("com heranca comum, os dois ramos escrevem em campos diferentes") {
  patrulha_duplicada p;
  static_cast<movel&>(p).leituras = 7;
  static_cast<sensor&>(p).leituras = 9;
  REQUIRE(static_cast<movel&>(p).leituras == 7);
  REQUIRE(static_cast<sensor&>(p).leituras == 9);   // e este e o defeito
}

TEST_CASE("com heranca virtual, ha um campo so") {
  patrulha_unica p;
  static_cast<movel_v&>(p).leituras = 7;
  REQUIRE(static_cast<sensor_v&>(p).leituras == 7);
  static_cast<sensor_v&>(p).leituras = 9;
  REQUIRE(static_cast<movel_v&>(p).leituras == 9);
}

// A interface pura, que e o caso facil: nenhum estado, nenhum diamante de
// dados, e nenhuma heranca virtual necessaria.
TEST_CASE("sonda_reparadora e sonda e e i_reparavel") {
  zerar_entidades();
  auto m = mapa::de_texto("#####\n#.#.#\n#####\n", "t");
  mundo w(std::move(*m));

  auto& r = static_cast<sonda_reparadora&>(
      w.acrescentar(std::make_unique<sonda_reparadora>(vetor2{1, 1})));

  const entidade* como_entidade = &r;
  const sonda* como_sonda = &r;
  const i_reparavel* como_interface = &r;
  REQUIRE(como_entidade != nullptr);
  REQUIRE(como_sonda != nullptr);
  REQUIRE(como_interface != nullptr);
  REQUIRE(r.glifo() == 'R');

  SECTION("reparar troca parede por piso e cobra energia") {
    const int antes = r.energia();
    REQUIRE(w.setor()[{2, 1}].glifo == '#');
    REQUIRE(r.reparar(w.setor()[{2, 1}]));
    REQUIRE(w.setor()[{2, 1}].glifo == '.');
    REQUIRE(r.energia() == antes - 10);
    REQUIRE(r.reparos_feitos() == 1);
  }
  SECTION("nao repara o que nao e parede") {
    REQUIRE_FALSE(r.reparar(w.setor()[{1, 1}]));
    REQUIRE(r.reparos_feitos() == 0);
  }
}

TEST_CASE("a ordem de construcao e destruicao da reparadora fecha em zero") {
  zerar_entidades();
  {
    const sonda_reparadora r({1, 1});
    REQUIRE(sonda_reparadora::vivos == 1);
    REQUIRE(sonda::vivos == 1);   // ela TAMBEM e uma sonda, e conta nos dois
  }
  REQUIRE(sonda_reparadora::vivos == 0);
  REQUIRE(sonda::vivos == 0);
}
