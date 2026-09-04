// v2.6 - LSP e ISP, violados de proposito
#include <stdexcept>
#include <string>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "deriva/solid.hpp"

using namespace deriva;
using namespace deriva::solid;

// ---- LSP -----------------------------------------------------------------
TEST_CASE("LSP: a violacao nao aparece na derivada, aparece no chamador") {
  caixa c({1, 1});
  parede_que_lanca p({5, 5});
  std::vector<obstaculo*> quais{&c, &p};

  // `empurrar_todos` foi escrita antes de a parede existir, e estava certa.
  REQUIRE_THROWS_AS(empurrar_todos(quais, {1, 0}), std::logic_error);

  // E o pior: a caixa JA foi movida quando a excecao subiu. A funcao deixou o
  // sistema no meio do caminho, sem ter feito nada errado.
  REQUIRE(c.pos() == vetor2{2, 1});
}

TEST_CASE("LSP: a correcao e honrar a promessa, e nao try/catch") {
  caixa c({1, 1});
  parede_honesta p({5, 5});
  std::vector<obstaculo*> quais{&c, &p};

  const std::string onde = empurrar_todos(quais, {1, 0});
  REQUIRE(onde == "2,1 5,5 ");     // a parede respondeu onde esta
  REQUIRE(c.pos() == vetor2{2, 1});
  REQUIRE(p.pos() == vetor2{5, 5});
}

TEST_CASE("LSP: a substituicao e o teste, e ele roda sobre a base") {
  // O mesmo roteiro, com a derivada trocada. Uma passa, a outra nao - e o
  // codigo que muda e o da DERIVADA, nunca o do roteiro.
  auto roteiro = [](obstaculo& o) {
    std::vector<obstaculo*> um{&o};
    return empurrar_todos(um, {0, 1});
  };
  caixa c({0, 0});
  parede_honesta ph({3, 3});
  parede_que_lanca pl({3, 3});

  REQUIRE(roteiro(c) == "0,1 ");
  REQUIRE(roteiro(ph) == "3,3 ");
  REQUIRE_THROWS(roteiro(pl));
}

// ---- ISP -----------------------------------------------------------------
TEST_CASE("ISP: metodo vazio e a confissao de que a interface pede demais") {
  so_desenha_gordo gordo;
  gordo.desenhar();
  REQUIRE(gordo.desenhou);
  // `salvar` e `reparar` existem, nao fazem nada, e mentem para quem os chama.
  gordo.salvar();
  gordo.reparar();
  REQUIRE(metodos_obrigados_gordo() == 3);
}

TEST_CASE("ISP: segregada, quem so desenha escreve um metodo") {
  so_desenha magro;
  magro.desenhar();
  REQUIRE(magro.desenhou);
  REQUIRE(metodos_obrigados_segregado() == 1);
  static_assert(!std::is_base_of_v<i_salvavel, so_desenha>,
                "quem nao salva nao herda de i_salvavel");
}

TEST_CASE("ISP: quem faz as duas coisas herda das duas interfaces") {
  desenha_e_salva ambos;
  ambos.desenhar();
  ambos.salvar();
  REQUIRE(ambos.desenhou);
  REQUIRE(ambos.salvou);
  static_assert(std::is_base_of_v<i_desenhavel, desenha_e_salva>);
  static_assert(std::is_base_of_v<i_salvavel, desenha_e_salva>);
  // Interfaces puras, entao o diamante que elas formam e inofensivo - e e o
  // mesmo argumento do Cap. 17.
  SUCCEED("heranca multipla de interface pura, que e o caso recomendado");
}

TEST_CASE("ISP: a metrica e contavel, e nao opiniao") {
  REQUIRE(metodos_obrigados_gordo() > metodos_obrigados_segregado());
  REQUIRE(metodos_obrigados_gordo() - metodos_obrigados_segregado() == 2);
}
