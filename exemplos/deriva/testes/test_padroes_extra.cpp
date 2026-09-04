// v2.6 - State, Decorator e o Singleton
#include <memory>
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/mundo.hpp"
#include "deriva/padroes.hpp"

using namespace deriva;

namespace {
mundo montar() {
  auto m = mapa::de_texto("#####\n#.@.#\n#####\n", "t");
  return mundo(std::move(*m));
}
}  // namespace

// ---- State ---------------------------------------------------------------
TEST_CASE("State: cada tela responde por si, e a transicao e o retorno") {
  console c;
  REQUIRE(c.tela() == "mapa");
  c.comando("i");
  REQUIRE(c.tela() == "inventario");
  c.comando("esc");
  REQUIRE(c.tela() == "mapa");
  c.comando("x");
  REQUIRE(c.tela() == "inspecao");
  c.comando("i");
  REQUIRE(c.tela() == "inventario");
}

TEST_CASE("State: comando que a tela nao trata deixa tudo onde esta") {
  console c;
  c.comando("esc");                    // o mapa nao trata `esc`
  REQUIRE(c.tela() == "mapa");
  c.comando("zzz");
  REQUIRE(c.tela() == "mapa");
  REQUIRE(c.historico().size() == 2);  // mas o comando foi registrado
}

TEST_CASE("State: a transicao e testavel sem console") {
  tela_mapa t;
  const auto proxima = t.comando("i");
  REQUIRE(proxima != nullptr);
  REQUIRE(proxima->nome() == "inventario");
  REQUIRE(t.comando("zzz") == nullptr);
}

// ---- Decorator -----------------------------------------------------------
TEST_CASE("Decorator: empilhar dois nao exige classe para cada combinacao") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{2, 1}));

  auto base = std::make_unique<apresentacao_em_texto>();
  apresentacao_em_texto* espiar = base.get();

  // numerado POR FORA da moldura: a ordem da pilha e observavel
  std::unique_ptr<i_apresentacao> tela = std::make_unique<com_numero_de_linha>(
      std::make_unique<com_moldura>(std::move(base), "SETOR"));

  tela->desenhar(w);
  const std::string saida = espiar->acumulado();

  REQUIRE(saida.find("┌─┤ SETOR ├─┐") != std::string::npos);
  REQUIRE(saida.find("[1]") != std::string::npos);
  REQUIRE(saida.find("└──┘") != std::string::npos);
}

TEST_CASE("Decorator: cada camada implementa a MESMA interface") {
  static_assert(std::is_base_of_v<i_apresentacao, com_numero_de_linha>);
  static_assert(std::is_base_of_v<i_apresentacao, com_moldura>);
  static_assert(std::is_base_of_v<i_apresentacao, apresentacao_em_texto>);
  // E nenhuma delas herda das outras: e isso que evita a explosao de classes.
  static_assert(!std::is_base_of_v<com_moldura, com_numero_de_linha>);
  SUCCEED("tres implementacoes irmas, e nao uma cadeia de heranca");
}

TEST_CASE("Decorator: sem decorador nenhum, a saida e a crua") {
  zerar_entidades();
  mundo w = montar();
  apresentacao_em_texto simples;
  simples.desenhar(w);
  REQUIRE(simples.acumulado().find("┌─┤") == std::string::npos);
}

// ---- Singleton, escrito para ser criticado -------------------------------
TEST_CASE("Singleton: e sempre a mesma instancia, e e esse o problema") {
  registro_global::instancia().limpar();
  registro_global& a = registro_global::instancia();
  registro_global& b = registro_global::instancia();
  REQUIRE(&a == &b);

  a.anotar("primeiro");
  REQUIRE(b.quantos() == 1);   // o teste seguinte herda isto
}

TEST_CASE("Singleton: o teste seguinte herda o estado do anterior") {
  // Nao chamamos `limpar()` de proposito: se o caso acima rodou antes, este ve
  // o evento dele. E o custo 2 dos quatro, e o que faz a ordem dos testes
  // passar a importar.
  const std::size_t antes = registro_global::instancia().quantos();
  registro_global::instancia().anotar("segundo");
  REQUIRE(registro_global::instancia().quantos() == antes + 1);
}

TEST_CASE("a alternativa que o material recomenda e substituivel no teste") {
  registro_em_memoria log;
  anotar_em(log, "sonda entrou");
  anotar_em(log, "item recolhido");
  REQUIRE(log.eventos().size() == 2);

  // Dois observadores independentes na mesma execucao: e o que o Singleton
  // nao permite.
  registro_em_memoria outro;
  anotar_em(outro, "so este");
  REQUIRE(outro.eventos().size() == 1);
  REQUIRE(log.eventos().size() == 2);
}
