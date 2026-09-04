// v2.2 - as tres formas de dizer que algo nao deu certo
#include <filesystem>
#include <variant>

#include <catch2/catch_test_macros.hpp>

#include "deriva/erro.hpp"

using namespace deriva;

TEST_CASE("as tres formas de dizer que algo nao deu certo") {
  SECTION("ausencia e optional: nao e erro, e resposta") {
    REQUIRE_FALSE(mapa::carregar("nao/existe.txt").has_value());
  }
  SECTION("erro esperado com informacao e variant") {
    const auto r = interpretar("###\n##\n", "torto");
    REQUIRE(std::holds_alternative<razao>(r));
    REQUIRE(std::get<razao>(r) == razao::fileira_torta);
  }
  SECTION("o que rompe a operacao e excecao") {
    REQUIRE_THROWS_AS(carregar_ou_lancar("nao/existe.txt"), falha_de_leitura);
  }
}

TEST_CASE("cada razao de recusa e distinguivel, e por isso tratavel") {
  REQUIRE(std::get<razao>(interpretar("", "v")) == razao::vazio);
  REQUIRE(std::get<razao>(interpretar("###\n#.#\n###\n", "sem")) == razao::sem_entrada);
  REQUIRE(std::get<razao>(interpretar("#@#\n#@#\n", "dois")) == razao::entrada_duplicada);
  REQUIRE(std::get<razao>(interpretar("#@#\n#Z#\n", "z")) == razao::glifo_desconhecido);
}

TEST_CASE("o texto valido devolve o mapa, e nao uma razao") {
  auto r = interpretar("#####\n#.@.#\n#####\n", "bom");
  REQUIRE(std::holds_alternative<mapa>(r));
  REQUIRE(std::get<mapa>(r).entrada() == vetor2{2, 1});
}

TEST_CASE("a excecao carrega o que quem trata precisa saber") {
  try {
    (void)carregar_ou_lancar("nao/existe/em/lugar/algum.txt");
    FAIL("devia ter lancado");
  } catch (const falha_de_leitura& e) {
    REQUIRE(e.caminho().filename() == "algum.txt");
    REQUIRE(e.codigo() == std::errc::no_such_file_or_directory);
    REQUIRE(std::string(e.what()).find("nao foi possivel ler") == 0);
  }
}

TEST_CASE("a hierarquia permite tratar por nivel de especificidade") {
  const mapa_invalido especifico("x.txt", "fileira torta");
  const erro_de_deriva& como_deriva = especifico;
  const std::runtime_error& como_runtime = especifico;
  const std::exception& como_excecao = especifico;
  REQUIRE(std::string(como_deriva.what()) == std::string(como_excecao.what()));
  REQUIRE(std::string(como_runtime.what()).find("fileira torta") != std::string::npos);
}

// Garantia forte: ou devolve mapa valido, ou lanca sem deixar nada pela
// metade. E barata aqui porque a validacao acontece antes de qualquer
// construcao - e e por isso que a leitura e separada da aplicacao.
TEST_CASE("interpretar nao constroi nada quando vai recusar") {
  deriva::zerar_contadores();
  const auto r = interpretar("###\n##\n", "torto");
  REQUIRE(std::holds_alternative<razao>(r));
  REQUIRE(deriva::contador_mapa::criados == 0);
}
