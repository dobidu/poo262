// Aula 05 - os eixos do sistema de tipos
#include <string>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "../tipos/despacho.hpp"
#include "deriva/entidade.hpp"
#include "deriva/mapa.hpp"

using namespace deriva::tipos;

// EIXO 1 · o tipo e propriedade da EXPRESSAO, e o compilador o conhece. Estes
// static_assert respondem sem executar nada, e e isso que "estaticamente
// tipado" significa.
TEST_CASE("estaticamente tipado: a resposta vem em compilacao") {
  static_assert(classificar<int>() == "inteiro");
  static_assert(classificar<double>() == "ponto flutuante");
  static_assert(classificar<int*>() == "ponteiro");
  static_assert(classificar<std::string>() == "classe");
  SUCCEED("nenhuma linha executou para responder");
}

// EIXO 2 · forte por padrao, fraco por convite.
TEST_CASE("explicit e como se recusa a conversao implicita") {
  static_assert(std::is_convertible_v<double, celsius> == false,
                "celsius e agregado: precisa de chaves");
  static_assert(std::is_convertible_v<double, fahrenheit> == false,
                "explicit recusa o convite");
  static_assert(std::is_constructible_v<fahrenheit, double>,
                "mas a conversao escrita continua possivel");

  const celsius c{100.0};
  REQUIRE(para_fahrenheit(c).valor == 212.0);
}

// EIXO 3 · C++ tem despacho SIMPLES. A funcao `resolver` existe porque a
// linguagem nao resolve por dois tipos ao mesmo tempo.
TEST_CASE("despacho simples: virtual resolve por UM tipo") {
  const sonda_c s;
  const parede_c p;
  const colisao& a = s;
  const colisao& b = p;

  // Um tipo: `virtual` resolve, e a chamada chega no lugar certo.
  REQUIRE(a.quem() == "sonda");
  REQUIRE(b.quem() == "parede");

  // Dois tipos: nenhum `virtual` resolve, e alguem tem de perguntar.
  REQUIRE(resolver(s, p) == "sonda x parede: a sonda para");
  REQUIRE(resolver(p, s) == "parede x sonda: a sonda para");
  REQUIRE(resolver(s, s) == "sonda x sonda: as duas param");
  REQUIRE(resolver(p, p) == "parede x parede: nada acontece");
}

TEST_CASE("com N tipos, o despacho manual cresce com N ao quadrado") {
  // Dois tipos: quatro casos, e `resolver` tem os quatro. Tres tipos seriam
  // nove, e e nesse ponto que o Visitor da Aula 25 passa a valer.
  const int tipos = 2;
  const int casos = tipos * tipos;
  REQUIRE(casos == 4);
}

// EIXO 4 · trait em C++ e template que responde sobre um tipo, e nao
// construcao da linguagem.
TEST_CASE("trait escrito a mao, e ele responde sobre o Deriva") {
  static_assert(tem_glifo_v<com_glifo>);
  static_assert(!tem_glifo_v<sem_glifo>);

  // E sobre os tipos de verdade: `sonda` tem `glifo()`, `mapa` nao.
  static_assert(tem_glifo_v<deriva::sonda>);
  static_assert(!tem_glifo_v<deriva::mapa>);
  SUCCEED("o trait respondeu sobre quatro tipos, nenhum deles executado");
}

// A pergunta que a Aula 05 usa para decidir heranca contra composicao, e ela
// e verificavel no codigo.
TEST_CASE("mapa TEM uma grade; sonda E uma entidade") {
  static_assert(std::is_base_of_v<deriva::entidade, deriva::sonda>,
                "sonda E uma entidade: heranca");
  static_assert(!std::is_base_of_v<deriva::grade, deriva::mapa>,
                "mapa NAO e uma grade: composicao");
  SUCCEED("a decisao de projeto esta afirmada no codigo, e nao so na prosa");
}
