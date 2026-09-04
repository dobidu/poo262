// v1.3 - estacao: posse compartilhada e weak_ptr
#include <memory>

#include <catch2/catch_test_macros.hpp>

#include "deriva/estacao.hpp"

using namespace deriva;

TEST_CASE("posse compartilhada: dois donos, e nenhum destroi sozinho") {
  zerar_estacao();
  {
    auto eclusa = std::make_shared<no_estacao>("eclusa");
    REQUIRE(eclusa.use_count() == 1);
    {
      auto corredor_a = std::make_shared<no_estacao>("corredor-a");
      auto corredor_b = std::make_shared<no_estacao>("corredor-b");
      no_estacao::ligar(corredor_a, eclusa);
      no_estacao::ligar(corredor_b, eclusa);
      REQUIRE(eclusa.use_count() == 3);   // este escopo mais os dois corredores
      REQUIRE(no_estacao::vivos == 3);
    }
    // os corredores morreram e a eclusa continua: era isso o requisito
    REQUIRE(eclusa.use_count() == 1);
    REQUIRE(no_estacao::vivos == 1);
  }
  REQUIRE(no_estacao::vivos == 0);
}

TEST_CASE("weak_ptr de volta impede o ciclo") {
  zerar_estacao();
  {
    auto a = std::make_shared<no_estacao>("a");
    auto b = std::make_shared<no_estacao>("b");
    no_estacao::ligar(a, b);

    REQUIRE(a.use_count() == 1);   // a ligacao de volta NAO conta
    REQUIRE(b.use_count() == 2);
    REQUIRE(b->anterior() != nullptr);
    REQUIRE(b->anterior()->nome() == "a");
  }
  REQUIRE(no_estacao::vivos == 0);   // com shared nas duas pontas, seria 2
}

TEST_CASE("weak_ptr obriga a perguntar, e por isso nao pendura") {
  zerar_estacao();
  std::shared_ptr<no_estacao> b;
  {
    auto a = std::make_shared<no_estacao>("a");
    b = std::make_shared<no_estacao>("b");
    no_estacao::ligar(a, b);
    REQUIRE(b->anterior() != nullptr);
  }
  // `a` morreu. O weak_ptr sabe, e devolve nullptr em vez de lixo.
  REQUIRE(b->anterior() == nullptr);
  b.reset();
  REQUIRE(no_estacao::vivos == 0);
}

TEST_CASE("percorrer e deterministico, na ordem de ligacao") {
  zerar_estacao();
  auto raiz = std::make_shared<no_estacao>("eclusa");
  auto n1 = std::make_shared<no_estacao>("corredor");
  auto n2 = std::make_shared<no_estacao>("deposito");
  no_estacao::ligar(raiz, n1);
  no_estacao::ligar(n1, n2);
  REQUIRE(percorrer(raiz) == "eclusa -> corredor -> deposito");
  REQUIRE(raiz->grau() == 1);
}
