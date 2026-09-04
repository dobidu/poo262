// v2.3 - inventario: STL, lambdas e clamp
#include <memory>
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/inventario.hpp"

using namespace deriva;

namespace {
std::unique_ptr<componente> nova(std::string rot, int massa) {
  return std::make_unique<peca>(std::move(rot), massa);
}
}  // namespace

TEST_CASE("guardar respeita a capacidade, e o retorno nao pode ser ignorado") {
  zerar_inventario();
  inventario inv(10);
  REQUIRE(inv.guardar(nova("chave", 4)));
  REQUIRE(inv.guardar(nova("cabo", 5)));
  REQUIRE_FALSE(inv.guardar(nova("gerador", 8)));   // nao cabe
  REQUIRE(inv.massa_total() == 9);
  REQUIRE(inv.folga() == 1);
  REQUIRE(inv.quantas() == 2);
}

TEST_CASE("std::clamp limita a capacidade sem min/max aninhado") {
  REQUIRE(inventario(-5).capacidade() == 0);
  REQUIRE(inventario(5000).capacidade() == 999);
  REQUIRE(inventario(42).capacidade() == 42);
}

TEST_CASE("max_element com lambda responde qual e a mais pesada") {
  zerar_inventario();
  inventario inv(100);
  REQUIRE(inv.mais_pesada() == nullptr);
  REQUIRE(inv.guardar(nova("chave", 4)));
  REQUIRE(inv.guardar(nova("gerador", 30)));
  REQUIRE(inv.guardar(nova("cabo", 5)));
  REQUIRE(inv.mais_pesada() != nullptr);
  REQUIRE(inv.mais_pesada()->rotulo() == "gerador");
}

TEST_CASE("o predicado vem de fora, e a funcao serve sem saber a pergunta") {
  zerar_inventario();
  inventario inv(100);
  REQUIRE(inv.guardar(nova("chave", 4)));
  REQUIRE(inv.guardar(nova("gerador", 30)));
  REQUIRE(inv.guardar(nova("cabo", 5)));

  REQUIRE(inv.contar_se([](const componente& c) { return c.massa() > 10; }) == 1);
  REQUIRE(inv.contar_se([](const componente& c) {
    return c.rotulo().find('c') == 0;
  }) == 2);
}

TEST_CASE("erase-remove descarta e devolve quantas sairam") {
  zerar_inventario();
  inventario inv(100);
  REQUIRE(inv.guardar(nova("chave", 4)));
  REQUIRE(inv.guardar(nova("gerador", 30)));
  REQUIRE(inv.guardar(nova("cabo", 5)));

  REQUIRE(inv.descartar_se([](const componente& c) { return c.massa() < 10; }) == 2);
  REQUIRE(inv.quantas() == 1);
  REQUIRE(inv.massa_total() == 30);
  REQUIRE(contador_de_instancias<peca>::vivos == 1);   // as duas foram destruidas
}

// O desempate pelo rotulo nao e capricho: sem ele, a ordem entre massas
// iguais seria a que o sort quisesse, e o despejo deixaria de ser
// deterministico - o replay quebraria.
TEST_CASE("a ordenacao e deterministica mesmo com massas iguais") {
  zerar_inventario();
  inventario a(100), b(100);
  for (const char* r : {"zinco", "alfa", "beta"}) {
    REQUIRE(a.guardar(nova(r, 5)));
  }
  for (const char* r : {"beta", "zinco", "alfa"}) {
    REQUIRE(b.guardar(nova(r, 5)));
  }
  a.ordenar_por_massa();
  b.ordenar_por_massa();
  REQUIRE(a.despejar() == b.despejar());
  REQUIRE(a.despejar().find("alfa") < a.despejar().find("beta"));
}

// Composite, que a Aula 25 nomeia: a mochila responde `massa` somando o que
// tem dentro, e o inventario nao sabe a diferenca.
TEST_CASE("a mochila e um componente que contem componentes") {
  zerar_inventario();
  auto m = std::make_unique<mochila>("mochila", 2);
  m->por_dentro(nova("chave", 4));
  m->por_dentro(nova("cabo", 5));
  REQUIRE(m->massa() == 11);      // tara 2 + 4 + 5
  REQUIRE(m->pecas() == 3);       // ela mesma + duas

  SECTION("mochila dentro de mochila continua respondendo certo") {
    auto externa = std::make_unique<mochila>("externa", 1);
    externa->por_dentro(std::move(m));
    REQUIRE(externa->massa() == 12);
    REQUIRE(externa->pecas() == 4);
  }
  SECTION("o inventario a trata como qualquer peca") {
    inventario inv(100);
    REQUIRE(inv.guardar(std::move(m)));
    REQUIRE(inv.massa_total() == 11);
    REQUIRE(inv.despejar().find("(3 pecas)") != std::string::npos);
  }
}

TEST_CASE("o contador por CRTP fecha em zero no inventario tambem") {
  zerar_inventario();
  {
    inventario inv(100);
    REQUIRE(inv.guardar(nova("a", 1)));
    auto m = std::make_unique<mochila>("m", 1);
    m->por_dentro(nova("b", 1));
    REQUIRE(inv.guardar(std::move(m)));
    REQUIRE(contador_de_instancias<peca>::vivos == 2);
    REQUIRE(contador_de_instancias<mochila>::vivos == 1);
  }
  REQUIRE(contador_de_instancias<peca>::fechou());
  REQUIRE(contador_de_instancias<mochila>::fechou());
}
