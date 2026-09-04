// Aula 04 - o codigo gerado e os tres defeitos plantados
#include <memory>
#include <string>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "../revisao_ia/gerado.hpp"

using namespace deriva::revisao;

// O teste que o proprio modelo escreveu para o codigo dele. Passa. E nao prova
// nada do que importa - e essa e a licao do item R7 da rubrica.
TEST_CASE("o teste que veio com o codigo gerado passa") {
  sensor_termico t("termico-01");
  t.registrar(20.0);
  t.registrar(22.0);
  REQUIRE(t.media() == 21.0);
  REQUIRE(t.nome() == "termico-01");
}

TEST_CASE("os tres defeitos plantados estao declarados") {
  const auto ds = defeitos_plantados();
  REQUIRE(ds.size() == 3);
  REQUIRE(std::string(ds[0].item_da_rubrica).find("R1") == 0);
  REQUIRE(std::string(ds[1].item_da_rubrica).find("R5") == 0);
  REQUIRE(std::string(ds[2].item_da_rubrica).find("R3") == 0);
}

// DEFEITO 1 · R1: a invariante e contornavel de fora.
TEST_CASE("R1: o vetor publico anula a invariante da classe") {
  sensor_termico t("x");
  t.registrar(20.0);
  t.leituras_.push_back(-999.0);   // ninguem impede, e a media mente
  REQUIRE(t.media() < 0.0);

  SECTION("na versao revisada, registrar RECUSA e o vetor e privado") {
    revisado::sensor_termico r("x");
    REQUIRE(r.registrar(20.0));
    REQUIRE_FALSE(r.registrar(-999.0));
    REQUIRE(r.quantas() == 1);
    REQUIRE(r.media() == 20.0);
  }
}

// DEFEITO 2 · R5: o destrutor da derivada nao roda, e nenhum aviso aparece.
TEST_CASE("R5: destrutor nao virtual na base polimorfica") {
  static_assert(!std::has_virtual_destructor_v<sensor_base>,
                "o defeito 2 esta plantado aqui");
  static_assert(std::has_virtual_destructor_v<revisado::sensor_base>,
                "e corrigido aqui");

  SECTION("na versao revisada, o contador prova que o destrutor roda") {
    revisado::sensor_termico::vivos = 0;
    {
      std::unique_ptr<revisado::sensor_base> s =
          std::make_unique<revisado::sensor_termico>("t");
      REQUIRE(revisado::sensor_termico::vivos == 1);
    }
    REQUIRE(revisado::sensor_termico::vivos == 0);
  }
}

// DEFEITO 3 · R3: `nome()` nao e const, e o codigo correto nem compila.
TEST_CASE("R3: nome() sem const impede o uso correto") {
  static_assert(!std::is_invocable_v<decltype(&sensor_base::nome), const sensor_base&>,
                "chamar num objeto const nao compila: e o defeito 3");
  static_assert(std::is_invocable_v<decltype(&revisado::sensor_base::nome),
                                    const revisado::sensor_base&>,
                "na versao revisada, compila");

  const revisado::sensor_termico r("termico-01");
  REQUIRE(r.nome() == "termico-01");   // e devolve vista, sem copiar
}

TEST_CASE("o painel funciona nas duas versoes, e e por isso que o defeito passa") {
  painel p;
  p.acrescentar(std::make_unique<sensor_termico>("a"));
  p.acrescentar(std::make_unique<sensor_termico>("b"));
  REQUIRE(p.quantos() == 2);
  REQUIRE(p.media_geral() == 0.0);   // sem leituras, e nada reclama
}
