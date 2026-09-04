// Aula 07/11 - os sizeof que os interativos exibem
#include <catch2/catch_test_macros.hpp>

#include "deriva/leiaute.hpp"

using namespace deriva::leiaute;

// Os números que o interativo "despachante virtual" (Aula 11) exibe. Se este
// teste falhar, é o MATERIAL que está errado, não o compilador.
TEST_CASE("o vptr custa 8 bytes por objeto") {
  REQUIRE(sizeof(entidade_simples) == 8);
  REQUIRE(sizeof(entidade) == 16);
  REQUIRE(sizeof(entidade) - sizeof(entidade_simples) == sizeof(void*));
}

TEST_CASE("herdar de classe nao-polimorfica nao custa nada") {
  REQUIRE(sizeof(drone_simples) == sizeof(entidade_simples));
}

TEST_CASE("a derivada sem dado novo nao cresce, e com dado novo soma") {
  REQUIRE(sizeof(drone) == 16);
  REQUIRE(sizeof(drone_com_carga) == 24);
}

TEST_CASE("entidade e abstrata - nao se instancia") {
  static_assert(!std::is_constructible_v<entidade>);
  static_assert(std::is_abstract_v<entidade>);
  static_assert(std::has_virtual_destructor_v<entidade>);
  SUCCEED("verificado em tempo de compilacao");
}
