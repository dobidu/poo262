// v2.6 - Command, Observer, Factory, Strategy, Composite
#include <memory>
#include <string>

#include <catch2/catch_test_macros.hpp>

#include "deriva/apresentacao.hpp"
#include "deriva/mundo.hpp"

using namespace deriva;

namespace {
mundo montar() {
  auto m = mapa::de_texto("#######\n#.....#\n#..#..#\n#.....#\n#######\n", "setor");
  return mundo(std::move(*m));
}
}  // namespace

// ---- DIP -----------------------------------------------------------------
TEST_CASE("o nucleo desenha atraves da interface, e nao sabe onde") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));

  apresentacao_em_texto tela;
  i_apresentacao& como_interface = tela;      // e so isso que o nucleo ve
  como_interface.mensagem("inspecao iniciada");
  como_interface.desenhar(w);

  REQUIRE(tela.acumulado().find("> inspecao iniciada") == 0);
  REQUIRE(tela.acumulado().find("entidades 1") != std::string::npos);
}

// ---- Command -------------------------------------------------------------
TEST_CASE("Command guarda o suficiente para desfazer") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  historico h;

  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{1, 0}), w));
  REQUIRE(w.primeira_com('@')->pos() == vetor2{2, 1});
  REQUIRE(h.profundidade() == 1);

  REQUIRE(h.desfazer_ultimo(w));
  REQUIRE(w.primeira_com('@')->pos() == vetor2{1, 1});
  REQUIRE(h.profundidade() == 0);
  REQUIRE_FALSE(h.desfazer_ultimo(w));        // pilha vazia
}

TEST_CASE("comando que falha nao entra na pilha de desfazer") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  historico h;

  // Para cima e parede: o comando nao executa, e nao ha o que desfazer.
  REQUIRE_FALSE(h.aplicar(std::make_unique<mover_sonda>(vetor2{0, -1}), w));
  REQUIRE(h.profundidade() == 0);
  REQUIRE(w.primeira_com('@')->pos() == vetor2{1, 1});
}

TEST_CASE("desfazer em cadeia volta ao estado inicial") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  historico h;
  const std::string antes = w.despejar();

  // A coluna em (3,2) e parede: a sequencia desce ANTES de chegar nela.
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{1, 0}), w));   // (2,1)
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{0, 1}), w));   // (2,2)
  REQUIRE(h.aplicar(std::make_unique<mover_sonda>(vetor2{0, 1}), w));   // (2,3)
  REQUIRE(h.profundidade() == 3);
  REQUIRE(w.despejar() != antes);

  while (h.desfazer_ultimo(w)) {
  }
  REQUIRE(w.despejar() == antes);   // byte a byte, e e o mesmo criterio do replay
}

// ---- Observer ------------------------------------------------------------
TEST_CASE("Observer permite testar o log sem arquivo") {
  registro_em_memoria log;
  i_observador& como_interface = log;
  como_interface.aconteceu("sonda entrou no setor");
  como_interface.aconteceu("item recolhido");
  REQUIRE(log.eventos().size() == 2);
  REQUIRE(log.eventos().front() == "sonda entrou no setor");
}

// ---- Factory -------------------------------------------------------------
TEST_CASE("Factory cria por glifo, e quem le o mapa nao conhece as classes") {
  zerar_entidades();
  {
    auto s = criar_por_glifo('@', {1, 1});
    auto d = criar_por_glifo('d', {2, 2});
    auto i = criar_por_glifo('!', {3, 3});
    REQUIRE(s != nullptr);
    REQUIRE(s->nome() == "sonda");
    REQUIRE(d->glifo() == 'd');
    REQUIRE(i->glifo() == '!');
    REQUIRE(criar_por_glifo('#', {0, 0}) == nullptr);   // terreno, nao entidade
  }
  REQUIRE(entidades_vivas() == 0);
}

// ---- Strategy por lambda -------------------------------------------------
TEST_CASE("Strategy e funcao quando e uma operacao sem estado") {
  zerar_entidades();
  mundo w = montar();
  const drone& d = static_cast<const drone&>(
      w.acrescentar(std::make_unique<drone>(vetor2{1, 1}, vetor2{1, 0})));
  w.acrescentar(std::make_unique<sonda>(vetor2{5, 3}));

  SECTION("patrulha anda no rumo, e para na parede") {
    const estrategia patrulha = estrategia_de_patrulha({1, 0});
    REQUIRE(patrulha(d, w) == vetor2{2, 1});
    const estrategia contra_parede = estrategia_de_patrulha({0, -1});
    REQUIRE(contra_parede(d, w) == d.pos());
  }
  SECTION("perseguicao reduz a distancia de Manhattan") {
    const estrategia caca = estrategia_de_perseguicao('@');
    const vetor2 destino = caca(d, w);
    REQUIRE(destino.manhattan({5, 3}) < d.pos().manhattan({5, 3}));
  }
  SECTION("parada devolve a propria posicao") {
    REQUIRE(estrategia_parada()(d, w) == d.pos());
  }
  SECTION("trocar de estrategia e trocar de valor, nao de tipo") {
    estrategia atual = estrategia_parada();
    REQUIRE(atual(d, w) == d.pos());
    atual = estrategia_de_patrulha({1, 0});   // a mesma variavel
    REQUIRE(atual(d, w) == vetor2{2, 1});
  }
}

TEST_CASE("a captura da lambda e por valor, e tem de ser") {
  zerar_entidades();
  mundo w = montar();
  const drone& d = static_cast<const drone&>(
      w.acrescentar(std::make_unique<drone>(vetor2{1, 1})));

  estrategia guardada;
  {
    const vetor2 rumo_local{0, 1};
    guardada = estrategia_de_patrulha(rumo_local);
  }  // `rumo_local` morreu aqui
  // Capturado por valor, a lambda sobreviveu. Por referencia, isto seria
  // leitura de objeto destruido - a mesma armadilha do string_view da Aula 03.
  REQUIRE(guardada(d, w) == vetor2{1, 2});
}

// Aula 26 · a prova automatizada do critério da §26.1.
//
// O argumento do capítulo é que o núcleo não muda para ganhar uma segunda
// interface. Afirmar isso é fácil; estas três condições o VERIFICAM, e é a
// diferença entre separação demonstrada e separação afirmada.
TEST_CASE("o nucleo nao conhece apresentacao nenhuma") {
  // (1) `mundo` não depende de `i_apresentacao`: é o apresentador que recebe o
  //     mundo, e não o contrário. Se a dependência se invertesse, esta
  //     construção deixaria de compilar sem um apresentador em mãos.
  zerar_entidades();
  mundo sozinho = montar();
  REQUIRE(sozinho.quantas() == 0);
  static_assert(std::is_constructible_v<mundo, mapa>,
                "o mundo se constroi sem apresentador nenhum");
}

TEST_CASE("duas apresentacoes sobre o MESMO mundo, e ele nao sabe qual") {
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));

  // (2) Duas implementações independentes da mesma interface, no mesmo
  //     processo, sobre o mesmo mundo. É o que a v2.7 faz com Qt, e o que a
  //     variante `v2.6-antes` torna impossível.
  apresentacao_em_texto a;
  apresentacao_em_texto b;
  i_apresentacao& como_a = a;
  i_apresentacao& como_b = b;

  como_a.desenhar(w);
  como_b.mensagem("segunda interface");
  como_b.desenhar(w);

  REQUIRE(a.acumulado().find("entidades 1") != std::string::npos);
  REQUIRE(b.acumulado().find("> segunda interface") == 0);
  REQUIRE(b.acumulado().find("entidades 1") != std::string::npos);
}

TEST_CASE("trocar a apresentacao nao muda o estado do dominio") {
  // (3) O critério mais forte: desenhar não pode alterar o mundo. Se
  //     desenhar mudasse estado, a segunda interface veria um sistema
  //     diferente da primeira.
  zerar_entidades();
  mundo w = montar();
  w.acrescentar(std::make_unique<sonda>(vetor2{1, 1}));
  const std::string antes = w.despejar();

  apresentacao_em_texto tela;
  for (int k = 0; k < 5; ++k) tela.desenhar(w);

  REQUIRE(w.despejar() == antes);   // byte a byte, depois de cinco renders
}
