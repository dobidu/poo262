// v1.4 - encaminhamento perfeito na fabrica
#include <memory>
#include <string>
#include <type_traits>

#include <catch2/catch_test_macros.hpp>

#include "deriva/encaminhamento.hpp"

using namespace deriva;

TEST_CASE("sem encaminhamento, a fabrica copia sempre") {
  como_chegou::limpar();
  carga_marcada original("peca");
  const auto p = criar_copiando(original);
  REQUIRE(p->rotulo() == "peca");

  // Duas entradas: a construcao e a COPIA que a fabrica fez.
  REQUIRE(como_chegou::traco.size() == 2);
  REQUIRE(como_chegou::traco[1].find("COPIADA") == 0);
}

TEST_CASE("com encaminhamento, o rvalue chega como rvalue") {
  como_chegou::limpar();
  const auto p = criar_encaminhando<carga_marcada>(carga_marcada("peca"));
  REQUIRE(p->rotulo() == "peca");
  REQUIRE(como_chegou::traco.size() == 2);
  REQUIRE(como_chegou::traco[1].find("MOVIDA") == 0);   // e nao COPIADA
}

TEST_CASE("e o lvalue continua chegando como lvalue") {
  como_chegou::limpar();
  carga_marcada original("peca");
  const auto p = criar_encaminhando<carga_marcada>(original);
  REQUIRE(p->rotulo() == "peca");
  REQUIRE(como_chegou::traco[1].find("COPIADA") == 0);
  // A origem continua utilizavel, e e isso que `std::move` no lugar de
  // `std::forward` teria estragado.
  REQUIRE(original.rotulo() == "peca");
}

TEST_CASE("a deducao e a que se diz, e o compilador confirma") {
  int x = 0;
  static_assert(deduziu_lvalue(x), "lvalue deduz T como int&");
  static_assert(!deduziu_lvalue(0), "rvalue deduz T como int");
  REQUIRE(x == 0);
}

namespace {
// Duas assinaturas para comparar. A primeira e referencia UNIVERSAL, porque `U`
// e dedutivel; a segunda e referencia a rvalue de verdade, porque o tipo esta
// fixo. Lambda em contexto nao avaliado resolveria isto em duas linhas, e e
// C++20 - o teto do alvo recusou, e a versao com template nomeado e a que
// compila em C++17.
template <class U>
void aceita_universal(U&&) {}
void aceita_rvalue(int&&) {}
}  // namespace

TEST_CASE("referencia universal nao e referencia a rvalue") {
  int x = 0;

  // A universal aceita os dois.
  aceita_universal(x);
  aceita_universal(0);

  // A de rvalue aceita so um: `aceita_rvalue(x);` nao compila.
  aceita_rvalue(0);
  static_assert(std::is_invocable_v<void (&)(int&&), int&&>);
  static_assert(!std::is_invocable_v<void (&)(int&&), int&>,
                "e essa recusa e a diferenca que o nome registra");
  REQUIRE(x == 0);
}
