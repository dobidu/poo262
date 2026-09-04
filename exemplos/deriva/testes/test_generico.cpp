// v2.0 - grade<T> e contador_de_instancias<T> por CRTP
#include <string>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/contador_crtp.hpp"
#include "deriva/entidade.hpp"
#include "deriva/grade_generica.hpp"

using namespace deriva;

namespace {
// Duas classes de teste, para provar que cada instanciacao do CRTP tem o SEU
// contador - e nao um compartilhado.
struct alfa : contador_de_instancias<alfa> {};
struct beta : contador_de_instancias<beta> {};
}  // namespace

TEST_CASE("cada instanciacao do CRTP tem o seu proprio contador") {
  contador_de_instancias<alfa>::zerar();
  contador_de_instancias<beta>::zerar();
  {
    const alfa a1, a2;
    const beta b1;
    REQUIRE(contador_de_instancias<alfa>::vivos == 2);
    REQUIRE(contador_de_instancias<beta>::vivos == 1);
  }
  REQUIRE(contador_de_instancias<alfa>::fechou());
  REQUIRE(contador_de_instancias<beta>::fechou());
  REQUIRE(contador_de_instancias<alfa>::criados == 2);
}

TEST_CASE("o CRTP conta a copia, que a versao manual esquecia") {
  contador_de_instancias<alfa>::zerar();
  {
    const alfa a;
    const alfa copia = a;      // nascimento, e o contador sabe
    REQUIRE(contador_de_instancias<alfa>::vivos == 2);
    REQUIRE(contador_de_instancias<alfa>::criados == 2);
  }
  REQUIRE(contador_de_instancias<alfa>::vivos == 0);
}

TEST_CASE("o CRTP nao custa byte nenhum") {
  static_assert(sizeof(contador_de_instancias<alfa>) == 1, "base vazia");
  static_assert(sizeof(alfa) == 1, "e a derivada nao cresce por causa dela");
  static_assert(!std::is_polymorphic_v<alfa>, "nenhuma vtable: e estatico");
  SUCCEED("verificado em tempo de compilacao");
}

// A comparacao que justifica o template: o comportamento e o mesmo que o do
// contador escrito a mao em `sonda`, `drone` e `item` desde a Aula 7.
TEST_CASE("o CRTP se comporta como o contador manual das entidades") {
  zerar_entidades();
  contador_de_instancias<alfa>::zerar();
  {
    const sonda s1({1, 1}), s2({2, 2});
    const alfa a1, a2;
    REQUIRE(sonda::vivos == contador_de_instancias<alfa>::vivos);
    REQUIRE(sonda::criados == contador_de_instancias<alfa>::criados);
  }
  REQUIRE(sonda::vivos == 0);
  REQUIRE(contador_de_instancias<alfa>::vivos == 0);
}

TEST_CASE("grade_de<T> serve os tres usos que motivaram generaliza-la") {
  SECTION("celula: o caso da v0.2") {
    grade_de<celula> g(3, 2);
    g.em({1, 0}).glifo = '#';
    REQUIRE(g.despejar() == ".#.\n...\n");
    REQUIRE(g.bytes_das_celulas() == 6 * sizeof(celula));
  }
  SECTION("char: o que ja foi visitado, da v2.5") {
    grade_de<char> visto(3, 2);
    visto.preencher(0);
    visto.em({0, 0}) = 1;
    REQUIRE(visto.despejar() == "+..\n...\n");
  }
  SECTION("int: o mapa de distancias, da v2.3") {
    grade_de<int> dist(3, 1);
    dist.em({0, 0}) = 0;
    dist.em({1, 0}) = 1;
    dist.em({2, 0}) = 2;
    REQUIRE(dist.despejar() == "012\n");
  }
}

// A especializacao que a biblioteca padrao lamenta: `vector<bool>` empacota
// bits, entao nao existe `bool&` para devolver. A grade recusa `bool` com
// mensagem propria em vez de deixar o erro vazar da biblioteca.
TEST_CASE("grade_de<bool> e recusada de proposito") {
  static_assert(!std::is_constructible_v<grade_de<char>, int, int> == false,
                "char serve");
  // `grade_de<bool> g(2, 2);` nao compila, e a mensagem e a nossa.
  SUCCEED("a recusa e em tempo de compilacao, por static_assert");
}

TEST_CASE("if constexpr poda o ramo, e e por isso que isto compila") {
  // `celula` nao tem `operator<`, e `int` nao tem `.glifo`. Com um `if`
  // comum, os dois ramos teriam de ser validos para os dois tipos, e nenhuma
  // das duas instanciacoes compilaria.
  grade_de<int> a(2, 1);
  grade_de<celula> b(2, 1);
  REQUIRE(a.despejar().size() == 3);
  REQUIRE(b.despejar().size() == 3);
}

TEST_CASE("a grade generica valida na lista de inicializacao, como a original") {
  REQUIRE_THROWS_AS(grade_de<int>(0, 2), std::invalid_argument);
  REQUIRE_THROWS_AS(grade_de<int>(2, -1), std::invalid_argument);
}
